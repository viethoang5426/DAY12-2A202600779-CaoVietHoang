import time
import random

def generate_response(prompt: str) -> str:
    """Mock LLM response for testing without API keys"""
    responses = [
        "That's an interesting question! Let me think about it...",
        "Based on my knowledge, the answer is quite complex.",
        f"You asked about '{prompt}'. Here is what I found.",
        "I am a mock AI agent. I can't really answer that, but I'm working perfectly!",
        "Deployment is going smoothly, isn't it?"
    ]
    time.sleep(random.uniform(0.5, 1.5)) # Simulate network delay
    return random.choice(responses)
