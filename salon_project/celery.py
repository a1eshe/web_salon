from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project.settings')

app = Celery('salon_project')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
