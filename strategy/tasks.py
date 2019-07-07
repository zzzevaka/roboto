from roboto.celery_app import app


@app.task
def tick_all_strategies():
    print('tick all strategies')
