import json
from pydantic import Field
from pydantic_settings import BaseSettings
import os
import boto3


# 초기환경 세팅
# TODO Secrets Manager로 수정 필요
class Settings(BaseSettings):
    DATABASE_USERNAME: str = Field(..., env="DATABASE_USERNAME")
    DATABASE_PASSWORD: str = Field(..., env="DATABASE_PASSWORD")
    DATABASE_HOST: str = Field(..., env="DATABASE_HOST")
    DATABASE_PORT: str = Field(..., env="DATABASE_PORT")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")
    SECRET_NAME: str = Field(..., env="SECRET_NAME")
    USE_AWS_SECRETS: bool = Field(..., env="USE_AWS_SECRETS")

    class Config:
        env_file = ".env"

    @classmethod
    def from_aws_secrets(cls):
        secret_name = os.getenv("SECRET_NAME")  # Secret 이름을 환경변수로 전달
        region_name = "ap-northeast-2"
        client = boto3.client("secretsmanager", region_name=region_name)
        response = client.get_secret_value(SecretId=secret_name)
        print(response)
        # SecretsManager에서 반환한 비밀값을 JSON 형태로 파싱
        secret_dict = json.loads(response["SecretString"])

        # 파싱한 데이터를 Settings 클래스의 인스턴스 생성에 사용
        return cls(**secret_dict)  # secret_dict의 키-값을 Settings 필드로 전달


def get_settings():
    if os.getenv("USE_AWS_SECRETS") == "true":  # 환경변수로 구분
        return Settings.from_aws_secrets()  # AWS Secrets Manager에서 가져오기
    return Settings()  # 로컬에서 .env 파일 사용


settings = get_settings()
print(settings)
