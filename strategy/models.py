import logging
from datetime import timedelta
from django.db import models
from django.utils import timezone

import re
import pandas as pd
from learning.features import LearningFeatureStore
from learning.preprocessing import (
    transform_datetime_index_to_values, transform_categorial,
    drop_until_first_full_field, time_series_difference
)
from oanda.models import Trade

logger = logging.getLogger('strategy')


class StrategyInterface(object):
    def get_data_for_predict(self, end_time):
        fstore = LearningFeatureStore.get_all_features_store()
        features = [f for f in fstore.features.values() if re.search('open|close', f.name)]
        data = None
        for feature in features:
            tmp_data = feature.load(
                end_time=end_time,
            )
            if data is None:
                data = tmp_data
            else:
                data = pd.concat([data, tmp_data], axis=1, ignore_index=False)
        data = drop_until_first_full_field(data)
        data = data.fillna(method='ffill')
        data = transform_datetime_index_to_values(data)
        data = transform_categorial(data, ['weekday', 'day', 'month', 'hour'])

        time_series_columns = [x for x in data.columns if re.match('open|close', x)]
        difference_values = [240, 216, 192, 168, 144, 120, 96, 72, 48, 24, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, ]

        return time_series_difference(
            data[:end_time],
            columns=time_series_columns,
            difference_values=difference_values,
            shape3d=True
        )

    def open_trade(self, end_time):
        X = self.get_data_for_predict(end_time)[-1:]
        will_raise = self.model.model.predict_classes([X])[0]
        units = 5 if will_raise else -5
        trade = self.trades.create(
            account=self.account,
            instrument=self.instrument,
            units=units,
        )
        trade.open()

    def close_trade(self):
        trades = self.trades.opened()
        for trade in trades:
            trade.close()

    def tick(self, now=None):
        if not now:
            now = timezone.now()

        if self.last_tick and (now - self.last_tick).seconds < 3600:
            return

        if now.minute < 1 or now.minute > 5:
            return

        self.close_trade()
        self.open_trade(now)

        self.last_tick = now
        self.save()


class Strategy(models.Model, StrategyInterface):

    instrument = models.ForeignKey('roboto.Instrument', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    model = models.ForeignKey(
        'learning.LearningModel',
        related_name='strategies',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    account = models.ForeignKey(
        'oanda.Account',
        related_name='strategies',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    trades = models.ManyToManyField(
        'oanda.Trade',
        through='StrategyToTrade',
        through_fields=('strategy', 'trade')
    )
    is_active = models.BooleanField(default=False)
    last_tick = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} ({}active)'.format(
            self.name,
            '' if self.is_active else 'not '
        )


class StrategyToTrade(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    trade = models.OneToOneField('oanda.Trade', on_delete=models.CASCADE)
