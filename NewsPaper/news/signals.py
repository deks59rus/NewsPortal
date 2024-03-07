from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

#from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

from .models import Post, Category, User, Subscriber, PostCategory




@receiver(m2m_changed, sender=PostCategory)
def notify_post_created(sender, instance, **kwargs):
    # Добавить условие проверки ИМЕННО СОЗДАНИЯ поста
    # Например что-то типа этого: if kwargs['action'] == 'post_add':
    emails = []
    categories = instance.post_category.all()
    for cat in categories:
        subscribers = Subscriber.objects.filter(category=cat)
        emails += [n.user.email for n in subscribers]

    subject = f'Опубликована новость в интересующей вас категории: {sender.category}'

    text_content = (
        f'Автор: {instance.author_post}\n'
        f'Заголовок: {instance.post_name}\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Автор: {instance.author_post}<br>'
        f'Заголовок:  {instance.post_name}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на новость</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()