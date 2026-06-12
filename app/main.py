import logging
import json
import signal
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Body
from pydantic import BaseModel
import redis

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget
from utils.mock_llm import generate_response

# Configure JSON Logging
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_record)

logger = logging.getLogger("agent")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(settings.LOG_LEVEL)

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

# Graceful Shutdown signal handler
def shutdown_handler(signum, frame):
    logger.info("Received termination signal. Shutting down gracefully...")
    # Clean up can happen here (e.g. closing db connections explicitly)
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

class AskRequest(BaseModel):
    user_id: str
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    try:
        r.ping()
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        return HTTPException(status_code=503, detail="Service not ready")

@app.post("/ask")
def ask(
    req: AskRequest,
    _auth: str = Depends(verify_api_key)
):
    user_id = req.user_id
    question = req.question
    
    # Check rate limit and budget per user explicitly
    check_rate_limit(user_id)
    check_budget(user_id)

    logger.info(f"Processing request for user: {user_id}")
    
    history_key = f"history:{user_id}"
    history = r.lrange(history_key, 0, -1)
    
    response_text = generate_response(question)
    
    # Save conversation
    r.rpush(history_key, f"User: {question}")
    r.rpush(history_key, f"Agent: {response_text}")
    # Keep only last 10 messages
    r.ltrim(history_key, -10, -1)
    
    return {
        "response": response_text,
        "history_length": len(history) + 2
    }
