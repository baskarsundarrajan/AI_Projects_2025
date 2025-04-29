from celery import Celery
from .settings import settings
celery = Celery(
    "task", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

celery.conf.task_routes = {"task.file_processing.process_file": {"queue": "file_processing"}}
celery.conf.update(task_track_started=True)

import task.file_processing