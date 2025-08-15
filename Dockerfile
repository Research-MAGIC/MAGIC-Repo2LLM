# MAGIC Research GitHub Repository Analyzer
# Multi-stage build for optimized image size

FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

LABEL maintainer="MAGIC Research <support@researchmagic.com>"
LABEL author="Dr. Rodrigo Masini de Melo - Chief AI Officer"
LABEL description="GitHub Repository Analyzer - Transform repositories into AI-ready single text files"
LABEL version="1.0.0"

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY app.py .

RUN useradd -m -u 1000 magicuser && \
    chown -R magicuser:magicuser /app

USER magicuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080')" || exit 1

CMD ["python", "app.py"]
