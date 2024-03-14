from celery import shared_task
import time
from .models import Subscriber, PostCategory, Post
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Post, Category
from NewsPaper.settings import SITE_URL, DEFAULT_FROM_EMAIL
#from ..NewsPaper import settings

@shared_task
def send_messadge(id):
    print("Задача начала выполняться!")
    print(f" ID рассылаемого поста: {id}!")
    instance = Post.objects.get (id = id)

    emails = []
    categories = instance.post_category.all()
    for cat in categories:
        subscribers = Subscriber.objects.filter(category=cat)
        emails += [n.user.email for n in subscribers]


    print(f"Письмо будет отправленно на emails: {emails}")

    html_content = render_to_string(
        'messaging/notification_template.html',
        {
            'link': SITE_URL,
            'instance': instance,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Свежая новость на нашем сайте',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=emails
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def weekly_sending():

    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(time_of_creation__gte=last_week)
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subs = set(
        Category.objects.filter(category_name__in=categories).values_list('subscriptions__user__email', flat=True))
    html_content = render_to_string(
        'messaging/new_posts.html',
        {
            'link': SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Новые публикации за неделю!',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subs
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)