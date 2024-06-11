import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kernel.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('priceChecker', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Warsaw',
    enable_utc=True,
)

app.conf.beat_schedule = {
    'run-spider-every-day-at-20-40': {
        'task': 'priceChecker.tasks.run_spider_task_with_combined_keywords',
        'schedule': crontab(hour=20, minute=40)
    },
}

app.autodiscover_tasks(['priceChecker.tasks'])