FROM python:3.13-slim
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
COPY . .
ENV SECRET_NAME="kkamji-app-secrets" \
    USE_AWS_SECRETS="true"
# Step 7: Uvicorn을 사용해 FastAPI 앱 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "2"]