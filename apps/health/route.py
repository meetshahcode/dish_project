from fastapi import APIRouter, status, Depends
from fastapi_limiter.depends import RateLimiter
from fastapi_redis_cache import cache
from config import get_settings
from exceptions import Message
router = APIRouter()


@router.get("/", response_model=Message, responses={
    200: {
        "description": "Successful Response",
        "content": {"application/json": {"example": {"detail": "Hello World."}}}
    }
}, dependencies=[Depends(RateLimiter(times=30, seconds=60))])
@cache(expire=10)
async def root():
    return {"detail": "Hello World."}

@router.get("/health", 
         tags=["Health Check"], 
         summary="Health Check Endpoint", 
         description="Endpoint to check the health of the service",
         response_model=Message,
         status_code=status.HTTP_200_OK,
         responses={
             200: {
                 "description": "Service is healthy",
                 "content": {"application/json": {"example": {"detail": get_settings().app_name + " is healthy."}}}
             }
         }
         )
@cache(expire=10)
async def health():
    return {"detail": get_settings().app_name + " is healthy."}