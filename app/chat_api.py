from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db_init import SessionLocal
from app.db_schema import Message, ConversationHistory, User, Bot
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MessageCreate(BaseModel):
    user_id: str
    bot_id: str
    content: str

class MessageRead(BaseModel):
    id: str
    user_id: str
    bot_id: str
    content: str
    timestamp: datetime
    user_profile_image: str = None
    bot_avatar: str = None

@router.post("/messages", response_model=MessageRead)
def create_message(msg: MessageCreate, db: Session = Depends(get_db)):
    message = Message(
        id=str(uuid.uuid4()),
        user_id=msg.user_id,
        bot_id=msg.bot_id,
        content=msg.content,
        timestamp=datetime.utcnow()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    # Update conversation history
    history = db.query(ConversationHistory).filter_by(user_id=msg.user_id, bot_id=msg.bot_id).first()
    if not history:
        history = ConversationHistory(user_id=msg.user_id, bot_id=msg.bot_id, message_ids=message.id)
        db.add(history)
    else:
        ids = history.message_ids.split(",") if history.message_ids else []
        ids.append(message.id)
        history.message_ids = ",".join(ids)
    db.commit()
    return message

@router.get("/history/{user_id}/{bot_id}", response_model=List[MessageRead])
def get_conversation_history(user_id: str, bot_id: str, db: Session = Depends(get_db)):
    history = db.query(ConversationHistory).filter_by(user_id=user_id, bot_id=bot_id).first()
    if not history or not history.message_ids:
        return []
    ids = history.message_ids.split(",")
    messages = db.query(Message).filter(Message.id.in_(ids)).order_by(Message.timestamp).all()
    # Attach user profile image and bot avatar to each message
    user = db.query(User).filter_by(id=user_id).first()
    profile_image = user.profile_image if user and user.profile_image else ""
    bot = db.query(Bot).filter_by(id=bot_id).first()
    bot_avatar = bot.bot_avatar if bot and bot.bot_avatar else ""
    result = []
    for msg in messages:
        result.append(MessageRead(
            id=msg.id,
            user_id=msg.user_id,
            bot_id=msg.bot_id,
            content=msg.content,
            timestamp=msg.timestamp,
            user_profile_image=profile_image if msg.user_id == user_id else "",
            bot_avatar=bot_avatar if msg.user_id != user_id else ""
        ))
    return result

# Short-term memory: last N messages
@router.get("/memory/short/{user_id}/{bot_id}", response_model=List[MessageRead])
def get_short_term_memory(user_id: str, bot_id: str, n: int = 10, db: Session = Depends(get_db)):
    history = db.query(ConversationHistory).filter_by(user_id=user_id, bot_id=bot_id).first()
    if not history or not history.message_ids:
        return []
    ids = history.message_ids.split(",")
    messages = db.query(Message).filter(Message.id.in_(ids)).order_by(Message.timestamp.desc()).limit(n).all()
    return list(reversed(messages))  # Return in chronological order

# Long-term memory: all messages (optionally summarized)
@router.get("/memory/long/{user_id}/{bot_id}", response_model=List[MessageRead])
def get_long_term_memory(user_id: str, bot_id: str, db: Session = Depends(get_db)):
    history = db.query(ConversationHistory).filter_by(user_id=user_id, bot_id=bot_id).first()
    if not history or not history.message_ids:
        return []
    ids = history.message_ids.split(",")
    messages = db.query(Message).filter(Message.id.in_(ids)).order_by(Message.timestamp).all()
    return messages
