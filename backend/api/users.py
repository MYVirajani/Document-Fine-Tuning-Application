from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..db import crud
from ..db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ModuleCreate(BaseModel):
    module_code: str

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user.username, user.password)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not crud.verify_user_password(db_user, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": db_user.id, "username": db_user.username}

@router.post("/{user_id}/module")
def create_module(user_id: int, module: ModuleCreate, db: Session = Depends(get_db)):
    return crud.create_model_record(db, user_id=user_id, moduleCode=module.module_code)
