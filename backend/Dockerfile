# ─── CareerBridge Backend ───────────────────────────────────────────────────
# Used for:
#   Flask API    → CMD gunicorn -c gunicorn.conf.py run:app
#   Celery Worker→ CMD celery -A celery_worker.celery worker --loglevel=info
#   Celery Beat  → CMD celery -A celery_worker.celery beat  --loglevel=info
# Render lets you set a custom start command per service, all using this image.
# ────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# System deps (psycopg2 needs libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory (Cloudinary handles storage, but keep local fallback)
RUN mkdir -p uploads

# Expose Flask port
EXPOSE 5000

# Default: run production Flask via gunicorn + eventlet (for SocketIO)
CMD ["gunicorn", "-c", "gunicorn.conf.py", "run:app"]
