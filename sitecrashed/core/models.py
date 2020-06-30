import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from sitecrashed.core.tasks import notify_user


class Site(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.url


class Event(models.Model):
    UP = 'UP'
    DOWN = 'DOWN'
    NOTIFICATION = 'NOTIFICATION'
    TYPE_CHOICES = (
        (UP, 'UP'),
        (DOWN, 'DOWN'),
        (NOTIFICATION, 'NOTIFICATION'),
    )

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=UP)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.site} - {self.type}"


@receiver(post_save, sender=Event)
def verify_event(sender, instance, **kwargs):
    last_six_events = Event.objects.order_by('-created_at')[:6]
    downs = [event.type for event in last_six_events if event.type == Event.DOWN]
    if len(downs) == 6:
        notify_user.delay(website=instance.site.url, owner=instance.site.owner.email)
        Event.objects.create(site=instance.site, type=Event.NOTIFICATION)
