from fastapi import Header, HTTPException
from .config import settings

def verify_api_key(x_api_key: str = Header(..., description="API Key for authentication")):
    if x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return "authorized_user" # Normally we extract user_id, but here we can just return a dummy string or rely on body input.
