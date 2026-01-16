from pydantic import BaseModel
from typing import List, Optional

class Bot(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    soul_file: Optional[str] = None

class User(BaseModel):
    id: str
    username: str
    profile: Optional[str] = None

class Message(BaseModel):
    id: str
    user_id: str
    bot_id: str
    content: str
    timestamp: str

class ConversationHistory(BaseModel):
    user_id: str
    bot_id: str
    messages: List[Message]
