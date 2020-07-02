release: python manage.py migrate --noinput
web: gunicorn -b 0.0.0.0:$PORT sitecrashed.wsgi
worker: celery -A sitecrashed worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info
