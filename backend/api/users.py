# backend/api/users.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..db import crud, models
from sqlalchemy.orm import Session
from ..db.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user.name, user.email)
    return db_user

@router.get("/{user_id}/models")
def list_user_models(user_id: int):
    base_path = f"models/user_{user_id}"
    if not os.path.exists(base_path):
        return {"models": []}
    moduleCodes = os.listdir(base_path)
    return {"models": moduleCodes}

@router.post("/module/create", response_model=schemas.DomainModel)
def create_module_for_user(module: schemas.ModuleCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_user_module(db=db, user_id=current_user.id, module_code=module.module_code)


