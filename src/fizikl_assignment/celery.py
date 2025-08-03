import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings
from django_structlog.celery.steps import DjangoStructLogInitStep

from fizikl_assignment.loggers import setup_logger

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fizikl_assignment.settings")

app = Celery("fizikl_assignment")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ["utils"])

# A step to initialize django-structlog
app.steps["worker"].add(DjangoStructLogInitStep)


@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):
    setup_logger()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")  # noqa: T201
