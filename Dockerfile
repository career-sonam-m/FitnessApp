# Use Python 3.12 slim image
FROM python:3.12-slim

# HuggingFace Spaces strongly recommends a non-root user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install curl for health check
USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

USER user

# Copy requirements first for better caching
COPY --chown=user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=user streamlit_app.py .

# Copy .env if it exists (for local development)
COPY --chown=user .env* ./

# Expose HuggingFace Spaces default port
EXPOSE 7860

# Health check
HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health || exit 1

# Run Streamlit app on HuggingFace default port
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0"]
