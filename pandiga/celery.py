import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pandiga.settings')

app = Celery('pandiga')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check_technique':{
        'task':'technique.tasks.check_technique',
        'schedule' : crontab(minute=0, hour=0)
        #'schedule' : crontab(minute='*/1', )

    }
}
