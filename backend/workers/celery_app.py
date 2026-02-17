"""Celery application configuration."""
from celery import Celery
from ..app.config import settings

broker = settings.REDIS_URL
backend = settings.REDIS_URL

celery_app = Celery("worker", broker=broker, backend=backend)
celery_app.conf.task_routes = {"app.workers.tasks.*": {"queue": "default"}}
