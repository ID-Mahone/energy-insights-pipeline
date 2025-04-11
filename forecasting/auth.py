from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis
from typing import Optional
from fastapi import Depends
import redis

# Initialize HTTPBearer for API Key handling
security = HTTPBearer()

API_KEY = "your-api-key-here"

# Dependency for API Key Auth
def api_key_auth(api_key: str = Depends(security)) -> str:
    """""
    Check if the provided API key is valid
    """""
    if api_key.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            details="Invalid API Key"
        )
    return api_key.credentials

# Initialize Redis and limiter for rate limiting
redis_client = Redis(host="localhost", port=6379, db=0)

# FastAPI Limiter
async def init_limiter():
    await FastAPILimiter.init(redis_client)