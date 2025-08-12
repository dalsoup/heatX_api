# ---- base ----
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 시스템 의존성(필요 시 추가)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

# 파이썬 의존성
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# 앱 소스
COPY app ./app
COPY models ./models
COPY .env

# 기본 포트
ENV HOST=0.0.0.0
ENV PORT=8000

# 유비콘 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
