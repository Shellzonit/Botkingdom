from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.db_init import SessionLocal
from app.db_schema import Message, ConversationHistory, User, Bot
from app.personality import PersonalityEngine
import httpx
import os
import uuid
from datetime import datetime
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: dict, user_id: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/chat/{user_id}/{bot_id}")
async def websocket_chat(websocket: WebSocket, user_id: str, bot_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Save user message
            db = SessionLocal()
            message = Message(
                id=str(uuid.uuid4()),
                user_id=user_id,
                bot_id=bot_id,
                content=data,
                timestamp=datetime.utcnow()
            )
            db.add(message)
            db.commit()
            db.refresh(message)
            # Update conversation history
            history = db.query(ConversationHistory).filter_by(user_id=user_id, bot_id=bot_id).first()
            if not history:
                history = ConversationHistory(user_id=user_id, bot_id=bot_id, message_ids=message.id)
                db.add(history)
            else:
                ids = history.message_ids.split(",") if history.message_ids else []
                ids.append(message.id)
                history.message_ids = ",".join(ids)
            db.commit()
            # Claude integration for bot reply
            personality_engine = PersonalityEngine()
            system_prompt = personality_engine.get_system_prompt(bot_id)
            # Fetch short-term memory (last 10 messages)
            history = db.query(ConversationHistory).filter_by(user_id=user_id, bot_id=bot_id).first()
            context_messages = []
            if history and history.message_ids:
                ids = history.message_ids.split(",")
                messages = db.query(Message).filter(Message.id.in_(ids)).order_by(Message.timestamp.desc()).limit(10).all()
                for msg in reversed(messages):
                    context_messages.append(f"{msg.user_id}: {msg.content}")
            context_str = "\n".join(context_messages)
            full_prompt = f"{system_prompt}\n{context_str}\nUser: {data}"
            CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "your-anthropic-api-key")
            CLAUDE_API_URL = "https://api.anthropic.com/v1/complete"
            headers = {
                "x-api-key": CLAUDE_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": full_prompt,
                "model": "claude-2",
                "max_tokens_to_sample": 256
            }
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(CLAUDE_API_URL, json=payload, headers=headers)
                    response.raise_for_status()
                    data_claude = response.json()
                    raw_reply = data_claude.get("completion", "")
                    final_reply = personality_engine.apply_personality(bot_id, raw_reply)
                except Exception as e:
                    final_reply = "[Bot Error] Unable to get response."
            # Save bot message
            bot_message = Message(
                id=str(uuid.uuid4()),
                user_id=bot_id,
                bot_id=bot_id,
                content=final_reply,
                timestamp=datetime.utcnow()
            )
            db.add(bot_message)
            db.commit()
            db.refresh(bot_message)
            # Update conversation history
            if history:
                ids = history.message_ids.split(",") if history.message_ids else []
                ids.append(bot_message.id)
                history.message_ids = ",".join(ids)
                db.commit()
            # Send bot reply to user
            await manager.send_personal_message({"user_id": bot_id, "bot_id": bot_id, "content": final_reply}, user_id)
            db.close()
    except WebSocketDisconnect:
        manager.disconnect(user_id)
