# Enterprise-grade Dockerfile for WeatherDataPortal
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && \
    pip install -r tests/requirements.txt && \
    pip install gunicorn

# Add a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Add a HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:8080/health || exit 1

EXPOSE 8080
CMD ["gunicorn", "-c", "tests/gunicorn_config.py", "src.app:app"]
