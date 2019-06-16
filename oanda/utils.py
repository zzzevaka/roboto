import logging
import dateutil.parser
from math import ceil


from django.utils import timezone
from django.db import IntegrityError
from oanda.api_client import get_oanda_api_client

from roboto.models import Instrument, Candle
from roboto.exceptions import DataLoadingError

api_client = get_oanda_api_client()


logger = logging.getLogger('oanda')


def collect_instrument_candles(instrument, price='M', granularity='H1', count=None):
    if not count:
        last_time = instrument.candles.last().time
        delta = (timezone.now() - last_time)
        count = ceil(delta.total_seconds() / 3600) + 100

    api = get_oanda_api_client()
    candle_response = api.instrument.candles(
        instrument.name,
        price=price,
        granularity=granularity,
        count=count,
    )

    if candle_response.status != 200:
        raise DataLoadingError('oanda api response status is not 200')

    for candle in candle_response.body['candles']:
        try:
            Candle.objects.create(
                instrument=instrument,
                time=dateutil.parser.parse(candle.time),
                granularity=Candle.GRAN_H1,
                open=candle.mid.o,
                close=candle.mid.c,
                low=candle.mid.l,
                high=candle.mid.h,
            )
        except IntegrityError:
            logger.debug('duplicate {} ({})'.format(instrument.name, dateutil.parser.parse(candle.time)))
