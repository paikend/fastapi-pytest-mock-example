import pytest

from src.utils.redis import redis


@pytest.mark.asyncio
async def test_aioredis_set():
    item = 10
    await redis.create()
    await redis.pool.set("add", item)
    response = await redis.pool.get("add")
    assert response == "10"
