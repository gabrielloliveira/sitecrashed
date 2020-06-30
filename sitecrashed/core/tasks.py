# Create your tasks here
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from sitecrashed.core.models import Site, Event


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


@shared_task
def check_websites_status():
    websites = Site.objects.all()
    for website in websites:
        response = requests.get(website.url)
        if response.status_code == 200:
            Event.objects.create(site=website, type=Event.UP)
        else:
            Event.objects.create(site=website, type=Event.DOWN)


@shared_task
def clean_events():
    Event.objects.all().delete()
