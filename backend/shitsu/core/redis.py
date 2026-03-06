import redis

from backend.shitsu.core.config import settings

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

redis_url = settings.get_redis_url()
