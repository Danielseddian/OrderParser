import os

from celery import Celery

from OrderParser import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OrderParser.settings")
app = Celery("OrderParser")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "sync-db-from-google-sheets": {"task": "api.tasks.get_sync", "schedule": settings.SYNC_DB_GHEETS_TASK_TIMEOUT},
    "check-delivery-date": {"task": "api.tasks.get_sync", "schedule": settings.CHECK_DELIVERY_DATE},
}
