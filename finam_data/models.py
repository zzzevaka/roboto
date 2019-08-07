from enum import IntEnum
from roboto.models import AbstractInstrument, AbstractCandle
from django.db import models


class ExtendedMarket(IntEnum):
    """
    Markets mapped to ids used by finam.ru export

    List is incomplete, extend it when needed
    """

    BONDS = 2
    COMMODITIES = 24
    CURRENCIES = 45
    ETF = 28
    ETF_MOEX = 515
    FUTURES = 14  # non-expired futures
    FUTURES_ARCHIVE = 17  # expired futures
    FUTURES_USA = 7
    INDEXES = 6
    SHARES = 1
    SPB = 517
    USA = 25

    MOSCOW_CURRENCIES = 45
    WORLD_CURRENCIES = 5


class Instrument(AbstractInstrument):
    MARKET_CHOICES = (
        (ExtendedMarket.MOSCOW_CURRENCIES, 'Moscow currencies'),
        (ExtendedMarket.WORLD_CURRENCIES, 'World currencies'),
    )

    market = models.SmallIntegerField(choices=MARKET_CHOICES)

    class Meta:
        verbose_name = 'Frinam instrument'
        verbose_name_plural = 'Finame models'

    @property
    def finam_market(self):
        return ExtendedMarket(self.market)


class Candle(AbstractCandle):

    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name='candles',
    )

    class Meta:
        unique_together = ('granularity', 'time', 'instrument')
        verbose_name = 'Finam candle'
        verbose_name_plural = 'Finam candles'
