import os
import rollbar
from celery import Celery
from celery.signals import task_failure

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roboto.settings')

app = Celery('roboto')

app.config_from_object('roboto.celeryconfig')

app.autodiscover_tasks()


@task_failure.connect
def handle_task_failure(**kwargs):
    rollbar.report_exc_info(extra_data=kwargs)
