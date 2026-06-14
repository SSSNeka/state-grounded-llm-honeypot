# State-Grounded LLM Honeypot — middleware image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests/ ./tests/

# Week 1: run the demo so `docker compose up middleware` proves the toolchain.
# Later weeks: replace with the long-running middleware service entrypoint.
CMD ["python", "-m", "state_grounded"]
