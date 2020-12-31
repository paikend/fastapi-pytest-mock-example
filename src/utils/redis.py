import aioredis

from src.configs import settings


class Redis(object):
    pool = None

    @classmethod
    async def create(cls):
        if cls.pool is None or cls.pool.closed:
            cls.pool = await aioredis.create_redis_pool(
                address=settings.redis_url
            )
        return cls.pool


redis = Redis()
