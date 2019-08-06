from roboto.models import AbstractInstrument, AbstractCandle
from django.db import models


class ExtendedMarket(object):
    WORLD_CURRENCIES = 5
    MOSCOW_CURRENCIES = 45

    # from finam.export.Market
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


class Instrument(AbstractInstrument):
    MARKET_CURRENCIES = 0

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
