import time
import uuid
import redis
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def check_rate_limit(user_id: str):
    current_time = int(time.time())
    window_start = current_time - 60
    
    key = f"rate_limit:{user_id}"
    
    # Remove old requests
    r.zremrangebyscore(key, 0, window_start)
    
    # Count requests in the last minute
    request_count = r.zcard(key)
    
    if request_count >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
    # Add current request
    unique_id = str(uuid.uuid4())
    r.zadd(key, {unique_id: current_time})
    r.expire(key, 60)
    
    return True
