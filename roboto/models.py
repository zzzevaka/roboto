from django.db import models


class Instrument(models.Model):

    VALUE_TYPE_FLOAT = 1
    VALUE_TYPE_TEXT = 2

    VALUE_TYPE_CHOICES = (
        (VALUE_TYPE_FLOAT, 'Float'),
        (VALUE_TYPE_TEXT, 'Text'),
    )

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100)
    value_type = models.IntegerField(choices=VALUE_TYPE_CHOICES)
    source = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.source)


class Candle(models.Model):

    GRAN_S5 = '1'
    GRAN_H1 = '2'

    GRAN_CHOICES = (
        (GRAN_S5, 'S5'),
        (GRAN_H1, 'H1'),
    )

    instrument = models.ForeignKey(Instrument, related_name='candles', on_delete=models.CASCADE)
    granularity = models.IntegerField(choices=GRAN_CHOICES)
    time = models.DateTimeField(db_index=True)

    open = models.FloatField()
    close = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()

    def __str__(self):
        return '{} {}'.format(self.instrument.name, self.time)

    class Meta:
        unique_together = (
            ('instrument', 'time')
        )


class InstrumentValue(models.Model):

    instrument = models.ForeignKey(Instrument, related_name='history_values', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    value = models.TextField()

    class Meta:
        unique_together = (
            ('instrument', 'time')
        )
