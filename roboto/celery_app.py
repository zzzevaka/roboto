import os
from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roboto.settings')

app = Celery('roboto')

app.config_from_object('roboto.celeryconfig')

app.autodiscover_tasks()
