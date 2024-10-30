# app/main.py

from fastapi import FastAPI
from app.api import users, posts, health_check
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(health_check.router, prefix="", tags=["healthcheck"])
