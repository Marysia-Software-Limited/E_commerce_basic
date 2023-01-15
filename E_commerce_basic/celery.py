import os
from celery import Celery


# set up the default Django settings module for the 'celery' program

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_commerce_basic.settings')
app = Celery('E_commerce_basic')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
