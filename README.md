# SiteCrashed

A simple application to notify when a website goes down.

## Requirements

* Python >= 3.6
* Redis Server == 6.0.3 | [Download Here.](https://redis.io/download)

## Installation

* Clone the repository:

```console
git clone https://github.com/gabrielloliveira/sitecrashed.git
```

* Change to the project directory and create a virtualenv.

```console
cd sitecrashed && python -m venv env
```

* Activate virtualenv and install the project requirements.

```console
source env/bin/activate && pip install -r requirements.txt
```

* Create an .env file with environment variables.

```console
cp contrib/env-example sitecrashed/.env
```

> 😘👆 Don't forget to fill in your settings.

* Run migrations.

```console
python manage.py migrate
```

* Create superuser (and insert your email)

```console
python manage.py createsuperuser
```

## Run application

First, you need to be running the Redis Server. After that, 
run the Celery (responsible for executing the scheduled tasks).

* To run the Celery

```console
celery -A sitecrashed worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info
```

Now you can run the Django

```console
python manage.py runserver
```

## How it works

The celery will check for a user-defined period of time 
that registered sites are responding with status code 200.

The result of the request is processed and an event 
type object is written.

These are the types:

| Type         | When                            |
| ------------ |:-------------------------------:|
| UP           | response.status_code == 200     |
| DOWN         | response.status_code != 200     |
| NOTIFICATION | Owner website received an email |

> 😄 The website owner will receive a notification that the 
> website has crashed when the web application logs 5 consecutive DOWN events.

## Time Settings

I prefer to check my websites every minute. So, if any of 
them doesn't respond for 5 minutes, I will receive an 
email with a notification that the site crashed.

To set this up in django, I create a 1 minute interval in 
periodic tasks.

And in periodic tasks, I list this interval of 1 minute 
for the execution of the check_website_status task.

> If you want to delete the data, there is a task that 
> deletes all events (clean_events). Just schedule it with a  period of time you like.
