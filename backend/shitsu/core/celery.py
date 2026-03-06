from celery import Celery

from backend.shitsu.core.redis import redis_url

celery_app = Celery("worker", backend=redis_url, broker=redis_url)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_contetn=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)
