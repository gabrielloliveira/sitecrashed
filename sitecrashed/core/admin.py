from django.contrib import admin
from .models import Site, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ['site', 'type', 'created_at']


admin.site.register(Site)
admin.site.register(Event, EventAdmin)
