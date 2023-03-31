import os

import celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardo_ai.settings')

BROKER_URL = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/0'
BACKEND_URL = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT")}/1'

app = celery.Celery('cardo_ai', broker=BROKER_URL, backend=BACKEND_URL)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
