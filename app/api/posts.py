from app import schemas
from app.services import post_service
from fastapi import APIRouter, HTTPException, Depends, Response
from app.database import SessionLocal
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


# 포스트 생성
@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, user_id: int, db: Session = Depends(get_db)):
    return post_service.create_post(db=db, new_post=post, user_id=user_id)


# 모든 포스트 조회
@router.get("/", response_model=list[schemas.PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = post_service.get_posts(db, skip=skip, limit=limit)
    return posts


# 특정 게시글 조회
@router.get("/{post_id}", response_model=schemas.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_service.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return db_post


# 특정 포스트 업데이트
@router.put("/{post_id}")
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = post_service.update_post(db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시글을 업데이트 할 수 없습니다.")
    return Response(status_code=204)


# 특정 포스트 삭제
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    success = post_service.delete_post(db, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="게시글을 삭제 할 수 없습니다.")
    return Response(status_code=204)
