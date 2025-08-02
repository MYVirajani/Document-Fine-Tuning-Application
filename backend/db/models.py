from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    models = relationship("FineTunedModel", back_populates="owner")

class FineTunedModel(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    moduleCode = Column(String, index=True)
    path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="models")
