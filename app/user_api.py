from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db_init import SessionLocal
from app.db_schema import User
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    id: str
    username: str
    profile: Optional[str] = None
    profile_image: Optional[str] = None

class UserRead(BaseModel):
    id: str
    username: str
    profile: Optional[str] = None
    profile_image: Optional[str] = None

@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
