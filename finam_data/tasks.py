from roboto.celery_app import app
from finam_data.models import Instrument
from finam_data.utils import collect_instrument_candles


@app.task
def collect_finam_candles():
    instruments = Instrument.objects.all()

    for istrument in instruments:
        collect_instrument_candles(istrument)
