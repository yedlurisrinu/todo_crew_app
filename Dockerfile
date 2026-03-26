# ── Stage 1: Builder ──────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ── Stage 2: Runtime ──────────────────────────────────────
FROM python:3.12-slim AS runtime

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages \
                    /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source code and static files
COPY src/ ./src/
COPY . .
COPY static/ ./static/

# Set PYTHONPATH so imports resolve cleanly
ENV PYTHONPATH=src

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser
#Create folder for log files and giving user write permissions
RUN mkdir -p /app/logs/ && chown -R appuser:appuser /app/logs

USER appuser

# Expose FastAPI port
EXPOSE 8000

# Run with Gunicorn + Uvicorn workers for production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#vault Secrets Path
# secret/AI
