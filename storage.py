from aiogram.fsm.storage.redis import RedisStorage
from aioredis.client import Redis

from config import REDIS_DB, REDIS_HOST, REDIS_PORT

redis_client = Redis.from_url(
    f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}", encoding='utf-8'
)
storage = RedisStorage(redis_client)


def cache(key, ex=None):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            data = await redis_client.get(key)
            if not data:
                try:
                    data = await func(*args, **kwargs)
                    if data:
                        await redis_client.set(key, data, ex)
                except:
                    data = None
                    await redis_client.delete(key)
            return data
        return wrapper
    return decorator
