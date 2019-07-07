import logging
from django.db import models
from django.utils import timezone

import re
import pandas as pd
from roboto.models import Instrument
from learning.features import LearningFeatureStore
from learning.preprocessing import (
    transform_datetime_index_to_values, transform_categorial,
    drop_until_first_full_field, time_series_difference
)

logger = logging.getLogger('strategy')


class Strategy(models.Model):

    instrument = models.ForeignKey(Instrument, on_delete=models.SET_NULL, null=True)
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
    is_active = models.BooleanField(default=False)

    def get_data_for_predict(self, end_time):
        fstore = LearningFeatureStore.get_all_features_store()
        features = [f for f in fstore.features.values(end_time=end_time) if re.search('open|close', f.name)]
        data = pd.concat([f.load() for f in features], axis=1, ignore_index=False)
        data = drop_until_first_full_field(data)
        data = data.fillna(method='ffill')
        data = transform_datetime_index_to_values(data)
        data = transform_categorial(data, ['weekday', 'day', 'month', 'hour'])

        time_series_columns = [x for x in data.columns if re.match('open|close', x)]
        difference_values = [240, 216, 192, 168, 144, 120, 96, 72, 48, 24, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, ]
        return time_series_difference(
            data,
            columns=time_series_columns,
            difference_values=difference_values,
            shape3d=True
        ).loc[end_time]

    def open_trade(self, end_time):
        X = self.get_data_for_predict(end_time)
        predict_class = self.model.predict_classes([X])[0]
        return predict_class

    def close_trade(self):
        trades = self.trades.opened()
        for trade in trades:
            trade.close()

    def tick(self, now=None):
        if not now:
            now = timezone.now()
        self.close_trade()
        self.open_trade(now)
