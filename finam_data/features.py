import pandas as pd
from learning.features import LearningFeature, LearningFeatureStore
from finam_data.models import Instrument, Candle


class FinamInstrumentFeature(LearningFeature):

    def __init__(self, intrument_name, target_column):
        self.intrument_name = intrument_name
        self.target_column = target_column

    def load(self, start_time=None, end_time=None):
        candles = Candle.objects.filter(
            instrument__name=self.intrument_name
        ).values_list(
            'time', self.target_column,
        )
        if start_time:
            candles = candles.filter(time__gte=start_time)
        if end_time:
            candles = candles.filter(time__lte=end_time)

        data = pd.DataFrame(
            columns=('time', self.name),
            data=list(candles),
        )
        return data.set_index(['time'])

    @property
    def name(self):
        return '{}_{}_finam'.format(self.intrument_name, self.target_column)


class FinamFeatureStore(LearningFeatureStore):
    name = 'finam'

    def register_all(self):
        for instrument in Instrument.objects.all():
            for column in ('open', 'close', 'low', 'high'):
                self.register(FinamInstrumentFeature(instrument.name, column))
