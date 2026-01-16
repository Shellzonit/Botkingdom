import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.personality import PersonalityEngine
from app.db_init import SessionLocal
from app.db_schema import Message, ConversationHistory

class ClaudeRequest(BaseModel):
    prompt: str
    bot_id: str
    user_id: str

class ClaudeResponse(BaseModel):
    response: str

router = APIRouter()
personality_engine = PersonalityEngine()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "your-anthropic-api-key")
CLAUDE_API_URL = "https://api.anthropic.com/v1/complete"  # Update if endpoint changes

@router.post("/claude", response_model=ClaudeResponse)
async def call_claude(request: ClaudeRequest):
    # Get system prompt from personality engine
    system_prompt = personality_engine.get_system_prompt(request.bot_id)

    # Fetch short-term memory (last 10 messages)
    db = SessionLocal()
    history = db.query(ConversationHistory).filter_by(user_id=request.user_id, bot_id=request.bot_id).first()
    context_messages = []
    if history and history.message_ids:
        ids = history.message_ids.split(",")
        messages = db.query(Message).filter(Message.id.in_(ids)).order_by(Message.timestamp.desc()).limit(10).all()
        for msg in reversed(messages):  # chronological order
            context_messages.append(f"{msg.user_id}: {msg.content}")
    db.close()

    # Build context string
    context_str = "\n".join(context_messages)

    # Combine system prompt, context, and user prompt
    full_prompt = f"{system_prompt}\n{context_str}\nUser: {request.prompt}"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": full_prompt,
        "model": "claude-2",  # Update model as needed
        "max_tokens_to_sample": 256
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(CLAUDE_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            raw_reply = data.get("completion", "")
            # Apply bot personality to Claude's response
            final_reply = personality_engine.apply_personality(request.bot_id, raw_reply)
            return ClaudeResponse(response=final_reply)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
