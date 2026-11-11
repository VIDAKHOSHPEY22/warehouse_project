# ----------------------------------------------------------------
# Dockerfile بک‌اند - تصویر سبک مبتنی بر Python 3.12
# ----------------------------------------------------------------
FROM python:3.12-slim

WORKDIR /app

# نصب پیش‌نیازهای سیستمی لازم برای psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
