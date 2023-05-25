import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NearestTrucksTestCase.settings')
celery_app = Celery('NearestTrucksTestCase')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.conf.timezone = "Europe/Moscow"
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'run-every-3-minutes': {
        'task': 'cargo.tasks.change_location',
        'schedule': crontab(minute="*/3"),
    },
}
