
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db_init import SessionLocal
from app.db_schema import Bot
from pydantic import BaseModel
from typing import Optional, List


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Delete a bot
@router.delete("/bots/{bot_id}")
def delete_bot(bot_id: str, db: Session = Depends(get_db)):
    bot = db.query(Bot).filter_by(id=bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    db.delete(bot)
    db.commit()
    return {"message": "Bot deleted", "bot_id": bot_id}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BotCreate(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    soul_file: Optional[str] = None
    bot_avatar: Optional[str] = None

class BotRead(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    soul_file: Optional[str] = None
    bot_avatar: Optional[str] = None

@router.post("/bots", response_model=BotRead)
def create_bot(bot: BotCreate, db: Session = Depends(get_db)):
    db_bot = Bot(**bot.dict())
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

@router.get("/bots/{bot_id}", response_model=BotRead)
def get_bot(bot_id: str, db: Session = Depends(get_db)):
    bot = db.query(Bot).filter_by(id=bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot

# List all bots
@router.get("/bots", response_model=List[BotRead])
def list_bots(db: Session = Depends(get_db)):
    bots = db.query(Bot).all()
    return bots
