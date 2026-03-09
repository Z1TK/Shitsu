import json
from backend.shitsu.core.redis import r_cache

async def get_cache(key: str):
    data = await r_cache.get(key)
    return json.loads(data) if data else None

async def set_cache(key: str, data: dict, expire: int = 300):
    return await r_cache.setex(key, expire, json.dumps(data, default=str))

async def delete_cache(keys: list[str] | str):
    if isinstance(keys, str):
        keys = [keys]
    await r_cache.delete(*keys)

async def delete_pattern_cache(pattern: str):
    async for key in r_cache.scan_iter(pattern):
        await r_cache.delete(key)