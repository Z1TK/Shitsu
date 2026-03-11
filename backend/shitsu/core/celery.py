from celery import Celery

from backend.shitsu.core.redis import redis_backend, redis_worker

app = Celery("worker", backend=redis_backend, broker=redis_worker)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_contetn=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)
