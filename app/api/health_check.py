from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy import text

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/healthz", summary="Health Check")
def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        value = result.scalar()
        if value != 1:
            raise Exception("Unexpected result from database")
    except Exception as e:
        print(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

    return JSONResponse(content={"status": "ok"})
