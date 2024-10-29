from pydantic_settings import BaseSettings


# 초기환경 세팅
# TODO Secrets Manager로 수정 필요
class Settings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
