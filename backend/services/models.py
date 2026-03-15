from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    interactions = relationship("Interaction", back_populates="user", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    pass

class Interaction(Base):
    __tablename__ = "interactions"
    pass

