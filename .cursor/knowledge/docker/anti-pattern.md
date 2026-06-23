# Docker Knowledge Base - Anti-Patterns

## Tổng quan

Document này liệt kê các anti-patterns phổ biến khi sử dụng Docker và đề xuất giải pháp thay thế. Mỗi anti-pattern được mô tả chi tiết với ví dụ về cách phát hiện và khắc phục.

## Anti-Pattern 1: Using :latest Tag in Production

### Mô tả

Sử dụng `:latest` tag trong production dẫn đến unpredictable behavior vì image được pull mỗi lần deploy có thể khác nhau.

### Ví dụ xấu

```dockerfile
# ❌ ANTI-PATTERN: Using latest in Dockerfile
FROM node:latest
FROM python:latest
FROM nginx:latest
```

```yaml
# ❌ ANTI-PATTERN: Using latest in docker-compose
services:
  api:
    image: myregistry.io/myapp:latest  # Changes on every deploy!
  db:
    image: postgres:latest  # Might break between deploys!
```

```bash
# ❌ ANTI-PATTERN: Always pulling latest
docker pull myapp:latest
```

### Giải pháp

```dockerfile
# ✅ SOLUTION: Use specific version tags
FROM node:18.17.0-alpine3.18
FROM python:3.11.7-slim-bookworm
FROM nginx:1.25.3-alpine

# ✅ SOLUTION: Use environment variables for versioning
ARG VERSION=1.0.0
FROM node:${VERSION}-alpine
```

```yaml
# ✅ SOLUTION: Use semantic versioning in compose
services:
  api:
    image: myregistry.io/myapp:1.2.3
    # Or use build args
    build:
      args:
        - IMAGE_TAG=1.2.3
  
  db:
    image: postgres:15.4-alpine  # Specific minor version
```

```bash
# ✅ SOLUTION: Use image digests for absolute immutability
docker pull myapp@sha256:a1b2c3d4e5f6...
```

## Anti-Pattern 2: Not Using Non-Root Users

### Mô tả

Chạy container với root user là security risk nghiêm trọng vì user có thể escape container và affect host system.

### Ví dụ xấu

```dockerfile
# ❌ ANTI-PATTERN: Running as root
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]
# Container runs as root by default!
```

```yaml
# ❌ ANTI-PATTERN: No user specification
services:
  api:
    build: .
    # No user specified - runs as root
```

### Giải pháp

```dockerfile
# ✅ SOLUTION: Create and use non-root user
FROM node:18-alpine

# Create application group and user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

WORKDIR /app

# Copy files with proper ownership
COPY --chown=appuser:appgroup package*.json ./
RUN npm ci && npm cache clean --force

COPY --chown=appuser:appgroup . .

# Switch to non-root user before running
USER appuser

CMD ["node", "index.js"]
```

```dockerfile
# ✅ SOLUTION: Use numeric UID for better compatibility
FROM node:18-alpine
RUN mkdir /app && chown -R 1001:1001 /app
WORKDIR /app
USER 1001
CMD ["node", "index.js"]
```

```yaml
# ✅ SOLUTION: Specify user in compose
services:
  api:
    image: myapp:latest
    user: "1001:1001"
    # Or by name
    user: "node:node"
```

## Anti-Pattern 3: Not Setting Resource Limits

### Mô tả

Container không có resource limits có thể consume tất cả available memory hoặc CPU, affecting other containers và host.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: No limits at all
docker run -d myapp:latest
# Container can use ALL system resources!
```

```yaml
# ❌ ANTI-PATTERN: No resource limits in compose
services:
  api:
    image: myapp:latest
    # No deploy.resources specified
  worker:
    image: myworker:latest
    # No limits - can starve other services
```

### Giải pháp

```bash
# ✅ SOLUTION: Set both memory and CPU limits
docker run \
  --name myapp \
  --memory=1g \
  --memory-swap=2g \
  --cpus=1.5 \
  --cpuset-cpus=0,1 \
  --restart=on-failure:3 \
  myapp:latest
```

```yaml
# ✅ SOLUTION: Comprehensive resource limits in compose
version: '3.8'
services:
  api:
    image: myapi:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
          pids: 100
        reservations:
          cpus: '0.5'
          memory: 512M
    mem_limit: 2g
    memswap_limit: 4g
    cpus: 2.0
  
  worker:
    image: myworker:latest
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M
  
  redis:
    image: redis:7-alpine
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Anti-Pattern 4: Large Image Sizes

### Mô tả

Images quá lớn làm chậm deployment, tăng storage costs, và có thể introduce security vulnerabilities từ unnecessary packages.

### Ví dụ xấu

```dockerfile
# ❌ ANTI-PATTERN: Full Ubuntu with everything
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    nano \
    python3 \
    python3-pip \
    nodejs \
    npm \
    openjdk-11-jdk \
    # ... 100+ more packages
    && rm -rf /var/lib/apt/lists/*

# ❌ ANTI-PATTERN: Not cleaning up after install
RUN pip install numpy pandas scikit-learn
# Cache files remain in image!

# ❌ ANTI-PATTERN: Including development dependencies
RUN npm install  # Installs devDependencies too
```

### Giải pháp

```dockerfile
# ✅ SOLUTION: Use minimal base images
FROM alpine:3.18  # ~5MB vs Ubuntu's ~80MB
FROM node:18-alpine  # ~180MB vs node's ~1GB

# ✅ SOLUTION: Multi-stage builds
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci  # Production deps only
COPY . .
RUN npm run build

FROM node:18-alpine AS production
WORKDIR /app
# Copy only what's needed
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/main.js"]

# ✅ SOLUTION: Clean up in same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        package1 \
        package2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
```

## Anti-Pattern 5: COPY Everything Without .dockerignore

### Mô tả

Copy tất cả files vào image bao gồm .git, node_modules, .env files không cần thiết, làm image lớn hơn và có thể có security issues.

### Ví dụ xấu

```dockerfile
# ❌ ANTI-PATTERN: COPY . . without .dockerignore
FROM node:18-alpine
WORKDIR /app
COPY . .  # Copies everything including .git, node_modules, .env!
RUN npm install  # Redundant if node_modules copied!
```

### Giải pháp

```bash
# ✅ SOLUTION: Create comprehensive .dockerignore
cat > .dockerignore << 'EOF'
# Git
.git
.gitignore

# Dependencies
node_modules/
__pycache__/
*.pyc

# Environment files
.env
.env.*
!.env.example

# IDE
.vscode/
.idea/

# Build artifacts
dist/
build/
target/

# Tests
coverage/
*.test.js
__tests__/

# Documentation
*.md
LICENSE
docs/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
EOF
```

```dockerfile
# ✅ SOLUTION: Copy only what's needed
FROM node:18-alpine
WORKDIR /app

# Copy dependency files first (better caching)
COPY package*.json ./
RUN npm ci --only=production

# Then copy application code
COPY tsconfig.json ./
COPY src/ ./src/
RUN npm run build

# Final copy with built artifacts
COPY . .
```

## Anti-Pattern 6: Not Using Health Checks

### Mô tả

Containers không có health checks không được Docker monitor cho health status, dẫn đến traffic được routed đến unhealthy containers.

### Ví dụ xấu

```dockerfile
# ❌ ANTI-PATTERN: No health check
FROM node:18-alpine
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
# Docker has no way to know if app is healthy!
```

### Giải pháp

```dockerfile
# ✅ SOLUTION: Add HTTP health check
FROM node:18-alpine
WORKDIR /app
COPY . .
EXPOSE 3000

# Health check configuration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

CMD ["node", "server.js"]
```

```yaml
# ✅ SOLUTION: Health check in compose
version: '3.8'
services:
  api:
    image: myapi:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      db:
        condition: service_healthy
  
  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
```

## Anti-Pattern 7: Improper Signal Handling

### Mô tả

Container không handle SIGTERM properly có thể cause data loss hoặc inconsistent state khi stop hoặc scale down.

### Ví dụ xấu

```dockerfile
# ❌ ANTI-PATTERN: Shell form doesn't pass signals
CMD npm start
# Shell form runs as: /bin/sh -c "npm start"
# Signals go to shell, not the app!

# ❌ ANTI-PATTERN: Wrong PID 1 setup
CMD python manage.py runserver
# Python process is not PID 1, doesn't receive signals
```

### Giải pháp

```dockerfile
# ✅ SOLUTION: Use exec form (JSON array)
CMD ["node", "server.js"]
# Process runs as PID 1, receives signals directly

# ✅ SOLUTION: Use exec form with arguments
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]

# ✅ SOLUTION: Explicitly handle signals in Python
# main.py
import signal
import sys

def graceful_shutdown(signum, frame):
    print("Received SIGTERM, shutting down gracefully...")
    # Cleanup operations
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

# ✅ SOLUTION: Shell wrapper only when needed
# Use only if you need shell features
CMD ["/bin/sh", "-c", "echo $VAR_NAME"]  # Variable expansion needed
```

## Anti-Pattern 8: Storing Secrets in Environment Variables

### Mô tả

Lưu trữ sensitive data như passwords, API keys trong environment variables có thể expose chúng qua docker inspect và logs.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Secrets in plain text environment
services:
  api:
    image: myapp:latest
    environment:
      - DATABASE_PASSWORD=super_secret_password
      - API_KEY=sk_live_abc123xyz
      - STRIPE_SECRET=sk_test_...
# These are visible in:
# - docker inspect
# - docker-compose config
# - docker-compose logs
```

### Giải pháp

```yaml
# ✅ SOLUTION: Use Docker secrets (Swarm)
services:
  api:
    image: myapp:latest
    secrets:
      - db_password
      - api_key
    environment:
      - DATABASE_PASSWORD_FILE=/run/secrets/db_password
      - API_KEY_FILE=/run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

```yaml
# ✅ SOLUTION: Use Kubernetes secrets or external secret store
services:
  api:
    image: myapp:latest
    env_file:
      - path: /run/secrets/db_password
        required: true
```

```bash
# ✅ SOLUTION: Pass secrets at runtime (not in image)
docker run -d \
  --env-file prod.env \  # File not committed to repo
  myapp:latest
```

## Anti-Pattern 9: Not Using Health Checks in Dependencies

### Mô tả

Services depends_on other services without health check conditions có thể start trước khi dependencies ready.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: depends_on without health check
version: '3.8'
services:
  api:
    image: myapi:latest
    depends_on:
      - db  # Just waits for container to start, not be ready!
      - redis
  
  db:
    image: postgres:15-alpine
    # No healthcheck - might not be ready when api starts!
```

### Giải pháp

```yaml
# ✅ SOLUTION: Health checks + service_healthy condition
version: '3.8'
services:
  api:
    image: myapi:latest
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379
  
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Anti-Pattern 10: Multiple Services Per Container

### Mô tả

Running multiple services (nginx + php-fpm + mysql) trong một container vi phạm single responsibility principle và khó quản lý.

### Ví dụ xấu

```dockerfile
# ❌ ANTI-PATTERN: Supervisord with multiple services
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    nginx \
    php-fpm \
    supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY php.ini /etc/php/8.1/fpm/php.ini

CMD ["/usr/bin/supervisord", "-n"]
```

### Giải pháp

```yaml
# ✅ SOLUTION: One service per container
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_files:/usr/share/nginx/html
    depends_on:
      - php
      - api
    networks:
      - app-network
  
  php:
    image: php:8.2-fpm-alpine
    volumes:
      - ./code:/var/www/html
    depends_on:
      - db
    networks:
      - app-network
  
  api:
    image: myapi:latest
    environment:
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - app-network
  
  db:
    image: postgres:15-alpine
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  db_data:
  static_files:

networks:
  app-network:
    driver: bridge
```

## Anti-Pattern 11: Not Cleaning Up in the Same Layer

### Mô tả

Cleanup commands trong separate layer không giảm image size vì layers are read-only.

### Ví dụ xấu

```dockerfile
# ❌ ANTI-PATTERN: Cleanup in separate layer
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y package
RUN apt-get clean  # Doesn't reduce image size!
RUN rm -rf /var/lib/apt/lists/*  # Separate layer!
```

### Giải pháp

```dockerfile
# ✅ SOLUTION: Clean up in same RUN instruction
FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install -y --no-install-recommends package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ✅ SOLUTION: Use BuildKit cache mounts
# syntax=docker/dockerfile:1
FROM ubuntu:22.04
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y package
# Cache persists between builds, doesn't add to image size
```

## Related Documents

- [Docker Glossary](../glossary.md)
- [Docker Architecture](../architecture.md)
- [Docker Best Practices](../best-practice.md)
- [Docker Checklist](../checklist.md)
- [Docker FAQ](../faq.md)
- [Docker Decision Tree](../decision-tree.md)
