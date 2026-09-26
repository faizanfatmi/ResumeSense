# ============================================================
# ResumeSense — single-service production image
# Builds the React/Vite frontend, then serves it (plus the API and admin)
# from one Django/Gunicorn process. Build context must be the repo root.
# ============================================================

# ---------- Stage 1: build the React/Vite frontend ----------
FROM node:20-alpine AS frontend
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
# Produces /frontend/dist with assets referenced under /static/ (see vite.config.ts)
RUN npm run build

# ---------- Stage 2: Django backend that serves the SPA ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (PDF/OCR + postgres client libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Backend source
COPY backend/ /app/

# Compiled frontend — Django collects this into staticfiles and serves index.html
COPY --from=frontend /frontend/dist /app/frontend_build

EXPOSE 8000

# Render (and other PaaS) inject $PORT; default to 8000 for local use.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py seed_demo_data && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120"]
