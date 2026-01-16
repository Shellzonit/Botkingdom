from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.personality import PersonalityEngine
from typing import Dict, Any
import os

router = APIRouter()
p_engine = PersonalityEngine()

class SoulFile(BaseModel):
    data: Dict[str, Any]

@router.get("/bots/{bot_id}/personality")
def get_personality(bot_id: str):
    soul = p_engine.load_soul(bot_id)
    if not soul:
        raise HTTPException(status_code=404, detail="Soul file not found")
    return soul

@router.post("/bots/{bot_id}/personality")
def create_or_update_personality(bot_id: str, soul_file: SoulFile):
    p_engine.save_soul(bot_id, soul_file.data)
    return {"message": "Personality saved", "bot_id": bot_id}

@router.delete("/bots/{bot_id}/personality")
def delete_personality(bot_id: str):
    soul_path = os.path.join(p_engine.soul_dir, f"{bot_id}.json")
    if os.path.exists(soul_path):
        os.remove(soul_path)
        return {"message": "Personality deleted", "bot_id": bot_id}
    raise HTTPException(status_code=404, detail="Soul file not found")
