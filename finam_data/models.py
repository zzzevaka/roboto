from roboto.models import AbstractInstrument, AbstractCandle
from django.db import models
from finam.export import Exporter, Market, LookupComparator, Timeframe


class Instrument(AbstractInstrument):
    MARKET_CURRENCIES = 0

    MARKET_CHOICES = (
        (MARKET_CURRENCIES, 'Currencies'),
    )

    market = models.SmallIntegerField(choices=MARKET_CHOICES)

    class Meta:
        verbose_name = 'Frinam instrument'
        verbose_name_plural = 'Finame models'

    @property
    def finam_market(self):
        if self.market == self.MARKET_CURRENCIES:
            return Market.CURRENCIES
        raise ValueError('unknown market type')


class Candle(AbstractCandle):

    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name='candles',
    )

    class Meta:
        verbose_name = 'Finam candle'
        verbose_name_plural = 'Finam candles'
