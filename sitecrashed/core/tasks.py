# Create your tasks here
from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task
from decouple import config
from django.conf import settings
from django.core.mail import send_mail

from sitecrashed.core.models import Site, Event


BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", default=None)
CHANNEL_ID = config("TELEGRAM_CHANNEL_ID", default=None)


@shared_task
def notify_user(website, owner):
    subject = f'Site {website} caiu!'
    message = f'O site {website} caiu.'
    to = [owner]
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        to,
        fail_silently=False,
    )
    if BOT_TOKEN:
        telegram_api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id=-{CHANNEL_ID}&text={message}"
        requests.get(telegram_api)


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
