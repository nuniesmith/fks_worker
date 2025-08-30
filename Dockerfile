# Multi-stage Dockerfile extending shared Python template

# Build stage - extends shared Python template
FROM shared/python:3.13-slim AS build
COPY . /app/src/
RUN python -m pip install --no-deps -e .

# Runtime stage - extends shared Python template for production  
FROM shared/python:3.13-slim AS runtime

# Copy built application from build stage
COPY --from=build /app/src/ /app/src/

# Set service-specific environment variables
ENV SERVICE_NAME=fks-worker \
  SERVICE_TYPE=worker \
  SERVICE_PORT=8006 \
  WORKER_SERVICE_PORT=8006

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${SERVICE_PORT}/health || exit 1

EXPOSE 8006

USER appuser

# Run the worker entrypoint directly (template or fallback)
CMD ["python", "src/main.py"]
