from app import models, schemas
from app.services import user_service
from fastapi import HTTPException, Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.core.security import verify_password
from fastapi import APIRouter


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


# 사용자 생성
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 사용자입니다.")
    return user_service.create_user(db=db, new_user=user)


# 모든 사용자 조회
@router.get("/", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


# 사용자 조회
@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return db_user


# 아이디로 사용자 조회
@router.get("/username/{username}", response_model=schemas.UserResponse)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return db_user


# 로그인
@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, username=user.username)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다."
        )
    return {
        "message": "로그인 성공",
        "user_id": db_user.id,
        "username": db_user.username,
    }


# 유저 비밀번호 변경
@router.patch("/{user_id}/password")
def update_user_password(
    user_id: int, user: schemas.UserUpdatePassword, db: Session = Depends(get_db)
):
    db_user = user_service.update_user_password(
        db, user_id=user_id, password=user.password
    )
    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return {"message": "비밀번호가 성공적으로 변경되었습니다."}


# 특정 유저 삭제
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return {"message": "사용자가 성공적으로 삭제되었습니다."}
