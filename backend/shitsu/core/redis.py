import redis
from redis import asyncio as aioredis

from backend.shitsu.core.config import settings

r_brocker = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

r_cache = aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)

redis_url = settings.get_redis_url()
