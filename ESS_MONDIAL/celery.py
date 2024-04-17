from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ESS_MONDIAL.settings')
app = Celery('ESS_MONDIAL')
app.conf.enable_utc = False
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()



@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')