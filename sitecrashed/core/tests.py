from django.contrib.auth.models import User
from django.test import TestCase

from sitecrashed.core.models import Site, Event


class TestSite(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', email='gabrielloliveiradev@gmail.com', password='test')
        self.site = Site.objects.create(url='https://ohmycode.com.br/', owner=self.user)

    def test_site_created(self):
        """There should be a site."""
        self.assertTrue(Site.objects.exists())

    def test_site_quantity(self):
        """The number of sites must be equal to 1."""
        self.assertEqual(Site.objects.count(), 1)

    def test_site_url(self):
        """The site url should be https://ohmycode.com.br/"""
        expected = 'https://ohmycode.com.br/'
        self.assertEqual(self.site.url, expected)


class TestEvent(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test', email='gabrielloliveiradev@gmail.com', password='test')
        self.site = Site.objects.create(url='https://ohmycode.com.br/', owner=self.user)
        self.event = Event.objects.create(site=self.site)

    def test_event_created(self):
        """There should be a event."""
        self.assertTrue(Event.objects.exists())

    def test_event_quantity(self):
        """The number of events must be equal to 1."""
        self.assertEqual(Event.objects.count(), 1)

    def test_event_is_up(self):
        """Event type should be UP"""
        self.assertEqual(self.event.type, Event.UP)

    def test_event_is_down(self):
        """Event type should be DOWN"""
        self.event.type = Event.DOWN
        self.event.save()
        self.assertEqual(self.event.type, Event.DOWN)

    def test_event_is_notification(self):
        """Event type should be NOTIFICATION"""
        self.event.type = Event.NOTIFICATION
        self.event.save()
        self.assertEqual(self.event.type, Event.NOTIFICATION)

    # def test_send_notifiation(self):
    #     """If the site has 6 down events, then a notification must be sent to the owner."""
    #     Event.objects.create(site=self.site, type=Event.DOWN)
    #     Event.objects.create(site=self.site, type=Event.DOWN)
    #     Event.objects.create(site=self.site, type=Event.DOWN)
    #     Event.objects.create(site=self.site, type=Event.DOWN)
    #     Event.objects.create(site=self.site, type=Event.DOWN)
    #     self.assertEqual(Event.objects.filter(site=self.site).first().type, Event.NOTIFICATION)

