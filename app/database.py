from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings
from urllib.parse import quote

DATABASE_URL: str = (
    f"mysql+pymysql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}"
    f"@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

# 데이터베이스 연결을 위한 Engine 객체 생성
engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 요청마다 독립적인 세션을 생성하여 트랜젝션 제어
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
