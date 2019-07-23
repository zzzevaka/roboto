from datetime import timedelta
from celery.schedules import crontab


BROKER_BACKEND = "redis"
BROKER_URL = 'redis://redis:6379/0'


CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

CELERYBEAT_SCHEDULE = {

    #
    # OANDA
    #

    'collect_oanda_candles': {
        'task': 'oanda.tasks.collect_oanda_candles',
        'schedule': crontab(minute=0),
    },

    #
    # STRATEGY
    #

    'tick_all_strategies': {
        'task': 'strategy.tasks.tick_all_strategies',
        'schedule': timedelta(seconds=10),
    },

}
