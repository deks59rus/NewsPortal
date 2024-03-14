from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

#from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from .models import Post, Category, User, Subscriber, PostCategory

from .tasks import send_messadge


@receiver(post_save, sender=Post)
def notify_post_created(sender, instance, **kwargs):
    send_messadge.delay(instance.id)

