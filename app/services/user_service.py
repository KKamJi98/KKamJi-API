from sqlalchemy.orm import Session
from app import schemas
from app.models import user
from app.core.security import get_password_hash


# 유저 생성(회원가입)
def create_user(db: Session, new_user: schemas.UserCreate):
    hashed_password = get_password_hash(new_user.password)
    db_user = user.User(username=new_user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# user_id로 유저 조회
def get_user(db: Session, user_id: int):
    return db.query(user.User).filter(user.User.id == user_id).first()


# 아이디로 유저 조회
def get_user_by_username(db: Session, username: str):
    return db.query(user.User).filter(user.User.username == username).first()


# 모든 유저 목록 조회
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user.User).offset(skip).limit(limit).all()


# 유저 비밀번호 변경
def update_user_password(db: Session, user_id: int, password: str):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.password = get_password_hash(password)
        db.commit()
        db.refresh(db_user)
    return db_user


# 특정 유저 삭제
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
