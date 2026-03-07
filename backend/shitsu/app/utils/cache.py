import json
from backend.shitsu.core.redis import r_cache

async def get_cache(key: str):
    data = await r_cache.get(key)
    return json.load(data) if data else None

async def set_cache(key: str, data: dict, expire: int = 300):
    return await r_cache.setex(key, expire, json.dump(data))

async def delete_cache(key: str):
    await r_cache.delete(key)