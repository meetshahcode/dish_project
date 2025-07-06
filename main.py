
import uvicorn
from fast import app

from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_redis_cache import FastApiRedisCache

from config import get_settings

@app.on_event("startup")
async def startup():
    redis_client = await redis.from_url(get_settings().redis_url, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis_client)
    await FastApiRedisCache().init(host_url=get_settings().redis_url, prefix="fastapi-cache")

from apps.health.route import router as health_router
app.include_router(health_router)

from apps.user.route import router as user_router
app.include_router(user_router)

from apps.dish.route import router as dish_router
app.include_router(dish_router)

if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)