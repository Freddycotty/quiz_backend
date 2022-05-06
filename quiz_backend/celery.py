
import os
from celery import Celery
from datetime import timedelta
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_backend.settings')
app = Celery('quiz_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
 
app.conf.timezone = 'America/Caracas'

app.autodiscover_tasks()
 
 
