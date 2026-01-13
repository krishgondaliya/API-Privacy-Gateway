import time
import os
import redis.asyncio as redis
from fastapi import HTTPException

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

_redis = None

async def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(REDIS_URL, decode_responses=True)
    return _redis

async def check_rate_limit(
    key: str,
    limit: int,
    window_seconds: int,
):
    r = await get_redis()

    now = int(time.time())
    window = now // window_seconds
    redis_key = f"rate:{key}:{window}"

    count = await r.incr(redis_key)
    if count == 1:
        await r.expire(redis_key, window_seconds)

    # TEMP DEBUG PRINT
    print(f"[RATE LIMIT] key={redis_key}, count={count}")

    if count > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
