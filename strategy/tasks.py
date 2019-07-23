from roboto.celery_app import app
from strategy.models import Strategy


@app.task
def tick_all_strategies():
    for strategy in Strategy.objects.filter(is_active=True):
        strategy.tick()
