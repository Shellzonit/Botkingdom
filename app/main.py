from fastapi import FastAPI
from app.db_init import init_db
from app.ws_chat import router as ws_chat_router
from app.bot_api import router as bot_router
from app.user_api import router as user_router
from app.chat_api import router as chat_router
from app.claude import router as claude_router
from app.personality_api import router as personality_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(ws_chat_router)
app.include_router(bot_router)
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(claude_router)
app.include_router(personality_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Bot Kingdom Hub!"}
