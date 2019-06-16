from datetime import timedelta

BROKER_BACKEND = "redis"
BROKER_URL = 'redis://redis:6379/0'


CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

CELERYBEAT_SCHEDULE = {

    #
    # OANDA
    #

    'collect_oanda_candles': {
        'task': 'oanda.tasks.collect_oanda_candles',
        'schedule': timedelta(hours=1),
    },

}
