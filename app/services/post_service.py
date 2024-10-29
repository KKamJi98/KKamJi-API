from sqlalchemy.orm import Session
from app import schemas, models
from app.models import post


# 포스트 생성
def create_post(db: Session, new_post: schemas.PostCreate, user_id: int):
    db_post = post.Post(
        title=new_post.title, content=new_post.content, owner_id=user_id
    )
    db.add(db_post)
    db.commit()  # 변경 사항 확정
    db.refresh(db_post)  # 세션 새로고침
    return db_post


# 특정 포스트 조회
def get_post(db: Session, post_id: int):
    return db.query(post.Post).filter(post.Post.id == post_id).first()


# 모든 포스트 조회(기본 최대 100개)
def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(post.Post).offset(skip).limit(limit).all()


# 특정 포스트 수정
def update_post(db: Session, post_id: int, post: schemas.PostCreate):
    db_post = get_post(db, post_id)
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        db.commit()
        db.refresh(db_post)
    return db_post


# 특정 포스트 삭제
def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
