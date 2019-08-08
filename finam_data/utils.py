import logging
import pytz
from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError
from finam.export import Exporter, Timeframe, LookupComparator
from finam_data.models import Instrument, Candle


def collect_instrument_candles(instrument, start_time=None, end_time=None):
    candles_to_create = []

    if not start_time:
        if instrument.candles.exists():
            last_time = instrument.candles.last().time
            start_time = last_time - timedelta(seconds=3600)
        else:
            start_time = timezone.now() - timedelta(days=365*4)

    if not end_time:
        end_time = timezone.now()

    exporter = Exporter()

    rub = exporter.lookup(
        name=instrument.name,
        market=instrument.finam_market,
        name_comparator=LookupComparator.EQUALS,
    )

    data = exporter.download(
        rub.index[0],
        market=instrument.finam_market,
        start_date=start_time,
        end_date=end_time,
        timeframe=Timeframe.HOURLY
    )

    for candle_time, value in data.iterrows():
        # convert Moscow time to UTC
        candle_time = candle_time.to_pydatetime().astimezone() - timedelta(hours=3)
        # finam-export use candle start time. Convert to end of candles
        candle_time = candle_time + timedelta(hours=1)

        if candle_time > timezone.now():
            continue

        candle = Candle(
            instrument=instrument,
            time=candle_time,
            granularity=Candle.GRAN_H1,
            open=value['<OPEN>'],
            close=value['<CLOSE>'],
            low=value['<LOW>'],
            high=value['<HIGH>'],
        )
        candles_to_create.append(candle)
    return Candle.objects.bulk_create(candles_to_create, ignore_conflicts=True)
