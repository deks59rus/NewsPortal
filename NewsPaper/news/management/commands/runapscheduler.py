import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand

from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from news.models import Post, Category
from datetime import datetime, timedelta

print("операция начата")
logger = logging.getLogger(__name__)


def my_job():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(time_of_creation__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subs = set(
        Category.objects.filter(category_name__in=categories).values_list('subscriptions__user__email', flat=True))
    html_content = render_to_string(
        'new_posts.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Новые публикации за неделю!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subs
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            #trigger=CronTrigger(second= "*/30"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            #trigger=CronTrigger(second= "*/30"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")