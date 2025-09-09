FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy dependency manifests first for better layer caching (if they rarely change)
COPY requirements.txt requirements.dev.txt* ./
RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential && rm -rf /var/lib/apt/lists/* && \
  python -m pip install --upgrade pip wheel setuptools && \
  pip install -r requirements.txt || echo "(dev requirements file optional)"

# Copy application source
COPY . /app/

# Ensure flat src layout is on PYTHONPATH
ENV PYTHONPATH=/app/src

# Set service-specific environment variables
ENV SERVICE_NAME=fks-worker \
  SERVICE_TYPE=worker \
  SERVICE_PORT=8006 \
  WORKER_SERVICE_PORT=8006

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${SERVICE_PORT}/health || exit 1

EXPOSE 8006

# Create non-root user (appuser) if security hardening desired
RUN adduser --disabled-password --gecos "" appuser || useradd -m appuser || true
USER appuser

# Run the worker entrypoint directly (template or fallback)
CMD ["python", "src/main.py"]
