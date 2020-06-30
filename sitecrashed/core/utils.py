def handle_notification(website, owner):
    from sitecrashed.core.tasks import notify_user
    notify_user.delay(website=website, owner=owner)
