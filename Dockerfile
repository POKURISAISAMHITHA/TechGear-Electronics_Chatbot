# ============================================================================
# TechGear Electronics Chatbot - Docker Image
# Multi-stage build for optimized production deployment
# ============================================================================

# Stage 1: Base Python image with dependencies
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# ============================================================================
# Stage 2: Dependencies installation
# ============================================================================
FROM base as dependencies

# Copy requirements file
COPY requirements.txt requirements_api.txt ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements_api.txt

# ============================================================================
# Stage 3: Production image
# ============================================================================
FROM base as production

# Copy installed dependencies from previous stage
COPY --from=dependencies /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Create non-root user for security
RUN useradd -m -u 1000 chatbot && \
    chown -R chatbot:chatbot /app

# Copy application files
COPY --chown=chatbot:chatbot . .

# Switch to non-root user
USER chatbot

# Create necessary directories
RUN mkdir -p chroma_db logs

# Set environment variables for production
ENV PYTHONPATH=/app \
    PORT=8000 \
    HOST=0.0.0.0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# ============================================================================
# Startup Commands
# ============================================================================

# Default command: Run the FastAPI server
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Alternative commands (use with docker run --entrypoint):
# - Embed and store products: ["python", "embed_and_store.py"]
# - Run tests: ["python", "test_chatbot.py"]
