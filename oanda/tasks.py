from roboto.celery_app import app
from roboto.models import Instrument
from oanda.utils import collect_instrument_candles


@app.task
def collect_oanda_candles():
    instruments = Instrument.objects.filter(source='oanda')

    for istrument in instruments:
        collect_instrument_candles(istrument)
