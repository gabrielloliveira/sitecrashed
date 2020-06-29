import uuid

from django.db import models


class Site(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    url = models.URLField()

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

    def __str__(self):
        return f"{self.site} - {self.type}"
