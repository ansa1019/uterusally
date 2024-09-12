from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Api.settings')

app = Celery('Api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()




app.conf.beat_schedule = {
    'unban-every-midnight': {
        'task': 'userdetail.models.unban_expired_bans',
        'schedule': crontab(minute='0', hour='0'),
    },
}