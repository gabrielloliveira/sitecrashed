# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def notify_user(website, owner):
    subject = 'Site caiu!'
    message = f'O site {website} caiu.'
    to = [owner]
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        to,
        fail_silently=False,
    )
