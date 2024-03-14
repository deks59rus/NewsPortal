import os
from celery import Celery
from celery.schedules import crontab #,solar


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Реализуем еженедельную рассылку через celery.schedules import crontab

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.weekly_sending',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}