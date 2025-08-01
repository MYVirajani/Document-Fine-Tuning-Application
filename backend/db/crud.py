# backend/db/crud.py

from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str):
    hashed_pw = pwd_context.hash(password)
    user = models.User(username=username, password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_user_password(db_user: models.User, password: str):
    return pwd_context.verify(password, db_user.password)

def create_model_record(db: Session, user_id: int, moduleCode: str, model_path: str):
    model = models.FineTunedModel(
        moduleCode=moduleCode, path=model_path, user_id=user_id
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

def get_model_by_moduleCode(db: Session, user_id: int, moduleCode: str):
    return db.query(models.FineTunedModel).filter_by(user_id=user_id, moduleCode=moduleCode).first()
