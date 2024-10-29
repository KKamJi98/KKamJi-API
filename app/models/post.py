# app/models/post.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(String(255))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")
