# ─── CareerBridge Backend ───────────────────────────────────────────────────
# Runs Flask API, Celery Worker, and Celery Beat in a single container
# using supervisord so it can be deployed on a single free Render Web Service.
# ────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# System deps (psycopg2 needs libpq, supervisor runs the multiple processes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    supervisor \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose Flask port
EXPOSE 5000

# Run everything via supervisord
CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]
