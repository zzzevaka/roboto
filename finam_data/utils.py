import logging
import pytz
from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError
from finam.export import Exporter, Timeframe
from finam_data.models import Instrument, Candle


def collect_instrument_candles(instrument, start_time=None):
    if not start_time:
        if instrument.candles.exists():
            last_time = instrument.candles.last().time
            start_time = last_time - timedelta(seconds=3600)
        else:
            start_time = timezone.now() - timedelta(days=365*4)

    exporter = Exporter()

    rub = exporter.lookup(
        name=instrument.name,
        market=instrument.market,
    )

    data = exporter.download(
        rub.index[0],
        market=instrument.market,
        start_date=start_time,
        timeframe=Timeframe.HOURLY
    )

    for candle_time, value in data.iterrows():
        # convert Moscow time to UTC
        candle_time = candle_time.to_pydatetime().astimezone() - timedelta(hours=3)
        # finam-export use candle start time. Convert to end of candles
        candle_time = candle_time + timedelta(hours=1)

        if candle_time > timezone.now():
            continue

        try:
            Candle.objects.create(
                instrument=instrument,
                time=candle_time,
                granularity=Candle.GRAN_H1,
                open=value['<OPEN>'],
                close=value['<CLOSE>'],
                low=value['<LOW>'],
                high=value['<HIGH>'],
            )
        except IntegrityError:
            pass
