from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    profile = Column(Text)
    profile_image = Column(String)  # URL to profile image
    messages = relationship("Message", back_populates="user")

class Bot(Base):
    __tablename__ = "bots"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    soul_file = Column(String)
    bot_avatar = Column(String)  # URL to bot avatar
    messages = relationship("Message", back_populates="bot")

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    bot_id = Column(String, ForeignKey("bots.id"))
    content = Column(Text)
    timestamp = Column(DateTime)
    user = relationship("User", back_populates="messages")
    bot = relationship("Bot", back_populates="messages")

class ConversationHistory(Base):
    __tablename__ = "conversation_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    bot_id = Column(String, ForeignKey("bots.id"))
    message_ids = Column(Text)  # Comma-separated message IDs
