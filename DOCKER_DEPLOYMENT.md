# 🐳 Docker Deployment Guide - TechGear Electronics Chatbot

Complete guide for building and deploying the TechGear Electronics Chatbot using Docker.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Docker Commands](#docker-commands)
5. [Docker Compose](#docker-compose)
6. [Environment Variables](#environment-variables)
7. [Volume Management](#volume-management)
8. [Troubleshooting](#troubleshooting)
9. [Production Deployment](#production-deployment)

---

## 🚀 Prerequisites

### Required Software

- **Docker**: Version 20.10 or higher
  ```bash
  docker --version
  ```

- **Docker Compose**: Version 2.0 or higher
  ```bash
  docker-compose --version
  ```

### Required Files

- Google Gemini API Key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))
- `product_info.txt` - Product catalog (included in repo)
- `.env` file with API credentials

---

## ⚡ Quick Start

### 1. Clone Repository (if not already done)
```bash
git clone <your-repo-url>
cd TechGear-Electronics_Chatbot
```

### 2. Set Up Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit with your API key
nano .env  # or use your preferred editor
```

Add your Google API key:
```env
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Build and Run with Docker Compose
```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Access the Application
- **Web Interface**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Endpoint**: http://localhost:8000/chat

### 5. Test the Chatbot
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What smartwatches do you have?"}'
```

---

## 🔧 Detailed Setup

### Step 1: Prepare Environment File

Create `.env` file with all required variables:

```env
# Required
GOOGLE_API_KEY=AIza...your_key_here

# Optional (with defaults)
HOST=0.0.0.0
PORT=8000
```

### Step 2: Build Docker Image

#### Option A: Using Docker Compose (Recommended)
```bash
docker-compose build
```

#### Option B: Using Docker CLI
```bash
docker build -t techgear-chatbot:latest .
```

### Step 3: Initialize ChromaDB (First Time Only)

If you don't have a `chroma_db` directory, you need to embed the products:

```bash
# Run embed script in container
docker-compose run --rm chatbot python embed_and_store.py
```

Or build the database locally before building the image:
```bash
python embed_and_store.py
```

### Step 4: Start the Application

```bash
docker-compose up -d
```

---

## 🐳 Docker Commands

### Building Images

```bash
# Build with docker-compose
docker-compose build

# Build with docker CLI
docker build -t techgear-chatbot:latest .

# Build with no cache (clean build)
docker build --no-cache -t techgear-chatbot:latest .

# Build specific stage
docker build --target production -t techgear-chatbot:latest .
```

### Running Containers

```bash
# Start with docker-compose
docker-compose up -d

# Start with docker CLI
docker run -d \
  --name techgear-chatbot \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key_here \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/logs:/app/logs \
  techgear-chatbot:latest

# Run in foreground (see logs)
docker-compose up

# Run with specific service
docker-compose up chatbot
```

### Managing Containers

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart containers
docker-compose restart

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f chatbot

# Execute commands in running container
docker-compose exec chatbot bash

# View container stats
docker stats techgear-chatbot
```

### Cleaning Up

```bash
# Remove stopped containers
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove images
docker rmi techgear-chatbot:latest

# Clean up all unused Docker resources
docker system prune -a
```

---

## 📦 Docker Compose

### Basic Usage

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up -d --build
```

### Advanced Configuration

Edit `docker-compose.yml` to customize:

```yaml
services:
  chatbot:
    # Change port mapping
    ports:
      - "9000:8000"  # External:Internal
    
    # Adjust resource limits
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 4G
    
    # Change restart policy
    restart: always
```

### Multiple Environments

Create environment-specific files:

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | `AIza...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `PYTHONUNBUFFERED` | Python output buffering | `1` |

### Setting Environment Variables

#### Method 1: .env file (Recommended)
```bash
# Create .env file
cat > .env << EOF
GOOGLE_API_KEY=your_key_here
PORT=8000
EOF
```

#### Method 2: Docker Compose environment section
```yaml
services:
  chatbot:
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - PORT=8000
```

#### Method 3: Docker CLI
```bash
docker run -e GOOGLE_API_KEY=your_key -e PORT=8000 techgear-chatbot
```

---

## 💾 Volume Management

### Persistent Data

The application uses volumes for:

1. **ChromaDB Database** - Vector store with embedded products
2. **Logs** - Application logs
3. **Product Info** - Product catalog (read-only)

### Volume Configuration

```yaml
volumes:
  # Bind mounts (sync with host)
  - ./chroma_db:/app/chroma_db
  - ./logs:/app/logs
  - ./product_info.txt:/app/product_info.txt:ro
```

### Managing Volumes

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect techgear-electronics_chatbot_chroma_data

# Remove volumes
docker-compose down -v

# Backup volume
docker run --rm -v techgear-electronics_chatbot_chroma_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/chroma_backup.tar.gz /data

# Restore volume
docker run --rm -v techgear-electronics_chatbot_chroma_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/chroma_backup.tar.gz -C /data --strip 1
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Container Won't Start

**Problem**: Container exits immediately

**Solution**:
```bash
# Check logs
docker-compose logs chatbot

# Check if port is already in use
sudo netstat -tulpn | grep 8000

# Try different port
docker-compose down
# Edit docker-compose.yml to change port
docker-compose up -d
```

#### 2. API Key Not Found

**Problem**: Error: "GOOGLE_API_KEY not found"

**Solution**:
```bash
# Verify .env file exists
cat .env

# Restart container
docker-compose restart

# Or pass explicitly
docker-compose run -e GOOGLE_API_KEY=your_key chatbot
```

#### 3. ChromaDB Empty

**Problem**: "No products found" error

**Solution**:
```bash
# Rebuild ChromaDB
docker-compose run --rm chatbot python embed_and_store.py

# Or mount existing chroma_db
docker-compose up -d
```

#### 4. Permission Denied

**Problem**: Permission errors accessing volumes

**Solution**:
```bash
# Fix permissions
sudo chown -R 1000:1000 chroma_db logs

# Or run as root (not recommended)
docker-compose run --user root chatbot
```

#### 5. Out of Memory

**Problem**: Container killed due to OOM

**Solution**:
```bash
# Increase memory limit in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 4G

# Or disable limits temporarily
docker-compose run --rm chatbot
```

### Health Check Issues

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' techgear-chatbot

# View health logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' techgear-chatbot

# Manual health check
curl http://localhost:8000/health
```

### Debug Mode

```bash
# Run container with interactive shell
docker-compose run --rm chatbot bash

# Run with verbose logging
docker-compose run --rm -e LOG_LEVEL=DEBUG chatbot

# Access running container
docker-compose exec chatbot bash
```

---

## 🚀 Production Deployment

### Security Best Practices

1. **Use Environment Files Securely**
```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Use secrets management in production
docker secret create google_api_key ./google_api_key.txt
```

2. **Run as Non-Root User** (already configured in Dockerfile)
```dockerfile
USER chatbot
```

3. **Limit Resources**
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

4. **Use HTTPS in Production**
```bash
# Use reverse proxy (nginx/traefik) with SSL
```

### Production docker-compose.yml

```yaml
version: '3.8'

services:
  chatbot:
    image: techgear-chatbot:latest
    restart: always
    ports:
      - "127.0.0.1:8000:8000"  # Only localhost
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - chroma_data:/app/chroma_db
      - chatbot_logs:/app/logs
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  chroma_data:
  chatbot_logs:
```

### Deployment with Nginx Reverse Proxy

1. **Create nginx configuration**:
```nginx
server {
    listen 80;
    server_name chatbot.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **Deploy with docker-compose**:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Monitoring

```bash
# View resource usage
docker stats techgear-chatbot

# View logs
docker-compose logs -f --tail=100

# Set up log rotation
# Already configured in docker-compose.yml
```

### Backup Strategy

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker run --rm -v techgear-electronics_chatbot_chroma_data:/data \
  -v $(pwd)/backups:/backup alpine \
  tar czf /backup/chroma_backup_$DATE.tar.gz /data
```

---

## 📊 Docker Image Information

### Image Details

- **Base Image**: `python:3.10-slim`
- **Final Size**: ~800MB (optimized multi-stage build)
- **Architecture**: linux/amd64
- **User**: Non-root user (chatbot:1000)

### Image Layers

1. Base Python image
2. System dependencies
3. Python packages
4. Application code
5. Configuration files

### Build Optimization

```bash
# Build with BuildKit for better caching
DOCKER_BUILDKIT=1 docker build -t techgear-chatbot:latest .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t techgear-chatbot:latest .
```

---

## 🎯 Example Workflows

### Development Workflow

```bash
# 1. Make code changes
vim main.py

# 2. Rebuild and restart
docker-compose up -d --build

# 3. View logs
docker-compose logs -f

# 4. Test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### Updating Products

```bash
# 1. Update product_info.txt
vim product_info.txt

# 2. Rebuild ChromaDB
docker-compose run --rm chatbot python embed_and_store.py

# 3. Restart application
docker-compose restart
```

### Running Tests

```bash
# Run test suite
docker-compose run --rm chatbot python test_chatbot.py

# Run quick tests
docker-compose run --rm chatbot python test_chatbot.py --quick

# Run single test
docker-compose run --rm chatbot python test_chatbot.py --single "What smartwatches?"
```

---

## 📝 Useful Commands Cheat Sheet

```bash
# Build
docker-compose build                    # Build images
docker-compose build --no-cache         # Clean build

# Run
docker-compose up -d                    # Start detached
docker-compose up                       # Start with logs
docker-compose run --rm chatbot bash    # Interactive shell

# Manage
docker-compose ps                       # List containers
docker-compose logs -f                  # Follow logs
docker-compose restart                  # Restart services
docker-compose down                     # Stop and remove

# Debug
docker-compose exec chatbot bash        # Access running container
docker-compose logs chatbot --tail=50   # View last 50 log lines
docker stats techgear-chatbot           # View resource usage

# Clean
docker-compose down -v                  # Remove containers + volumes
docker system prune -a                  # Clean all Docker resources
```

---

## 🆘 Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify environment: `docker-compose config`
3. Test health: `curl http://localhost:8000/health`
4. Check resources: `docker stats techgear-chatbot`

---

**Happy Dockerizing! 🐳**
