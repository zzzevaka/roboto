from django.db import models


class Account(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    alias = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)


class Instrument(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    type = models.CharField(max_length=100, db_index=True)


class Candle(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)

    bid_open = models.FloatField(blank=True, null=True)
    bid_close = models.FloatField(blank=True, null=True)
    bid_low = models.FloatField(blank=True, null=True)
    bid_high = models.FloatField(blank=True, null=True)

    ask_open = models.FloatField(blank=True, null=True)
    ask_close = models.FloatField(blank=True, null=True)
    ask_low = models.FloatField(blank=True, null=True)
    ask_high = models.FloatField(blank=True, null=True)

    mid_open = models.FloatField(blank=True, null=True)
    mid_close = models.FloatField(blank=True, null=True)
    mid_low = models.FloatField(blank=True, null=True)
    mid_high = models.FloatField(blank=True, null=True)

    # @classmethod
    # def from_oanda(cls, oanda_candle):
    #     return cls(
    #         oanda_candle.
    #     )
