# ★ ML-Ops Flask API Docker Image
# Serves trained model as REST API

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY models/ models/

# Security: Run as non-root user
RUN useradd -m -u 1001 mlops && chown -R mlops:mlops /app
USER mlops

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Expose port
EXPOSE 5000

# Production: use gunicorn, Development: use flask run
ENV FLASK_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "src.flask_api:app"]
