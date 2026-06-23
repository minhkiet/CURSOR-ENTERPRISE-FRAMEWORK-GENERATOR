# Docker Knowledge Base - Best Practices

## Tổng quan

Document này cung cấp 10+ best practices cho việc sử dụng Docker trong Cursor Enterprise Framework, kèm theo code examples cụ thể cho từng practice.

## Practice 1: Use Specific Base Image Tags

### Mô tả

Luôn sử dụng specific version tags thay vì `latest` để đảm bảo reproducibility và tránh unexpected updates.

```dockerfile
# ❌ BAD: Using latest
FROM node:latest
FROM python:latest
FROM ubuntu:latest

# ✅ GOOD: Using specific tags
FROM node:18.17.0-alpine3.18
FROM python:3.11.7-slim-bookworm
FROM ubuntu:22.04

# ✅ BETTER: Pin to major version with alpine for smaller images
FROM node:18-alpine
FROM python:3.11-slim
FROM nginx:1.25-alpine
```

### Tại sao quan trọng

- **Reproducibility**: Cùng Dockerfile build ra cùng image mọi lúc
- **Security**: Tránh auto-update có thể introduce vulnerabilities
- **CI/CD Stability**: Build results predictable
- **Audit Trail**: Dễ dàng track dependencies

## Practice 2: Use Multi-Stage Builds for Smaller Images

### Mô tả

Multi-stage builds cho phép tách biệt build-time và runtime dependencies, giảm final image size đáng kể.

```dockerfile
# ❌ BAD: Single stage - large image
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]

# Image size: 900MB+

# ✅ GOOD: Multi-stage build
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:18-alpine AS production
WORKDIR /app

# Security: Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001

# Copy built artifacts
COPY --from=builder --chown=nodeuser:nodejs /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY package*.json ./

# Set environment
ENV NODE_ENV=production
ENV PORT=3000

# Switch to non-root user
USER nodeuser

EXPOSE 3000
CMD ["node", "dist/main.js"]

# Image size: 150MB-

# ✅ BEST: Distroless for even smaller images
FROM node:18 AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM gcr.io/distroless/nodejs18-debian11 AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["dist/main.js"]

# Image size: 80MB-
```

## Practice 3: Optimize Dockerfile Layer Caching

### Mô tả

Sắp xếp instructions để maximize cache hits và giảm build time trong CI/CD pipelines.

```dockerfile
# ❌ BAD: Cache invalidation
COPY . .
RUN npm install  # Invalidates when ANY file changes

# ✅ GOOD: Dependency-first caching
COPY package*.json ./
RUN npm ci  # Cached unless package.json changes
COPY . .  # Now source changes don't invalidate npm install
RUN npm run build

# ✅ BETTER: Separate dependency and source layers
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY tsconfig.json ./
COPY src/ ./src/
RUN npm run build

COPY public/ ./public/
```

### Layer ordering principles

1. **Instructions ítuz thay đổi lên đầu**: Base image, system packages
2. **Dependencies sau**: package.json, requirements.txt
3. **Source code cuối**: Application code

## Practice 4: Use .dockerignore Effectively

### Mô tả

Exclude không cần thiết files từ build context để giảm build time và image size.

```bash
# .dockerignore
# Version control
.git
.gitignore
.gitattributes
.github/

# Development files
.vscode/
.idea/
*.md
*.txt
docker-compose*.yml
.env*
.DS_Store

# Dependencies (will be installed inside container)
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
.venv/

# Build artifacts
dist/
build/
target/
*.o
*.so

# Test and coverage
tests/
coverage/
*.test.js
*.spec.js
__tests__/

# Documentation
docs/
LICENSE
```

```bash
# Check what's being sent to Docker daemon
docker build --no-cache -t test . 2>&1 | grep "Sending build context"
# Output: Sending build context to Docker daemon  2.5MB
# Without .dockerignore might be: Sending build context to Docker daemon  500MB+
```

## Practice 5: Run as Non-Root User

### Mô tả

Container nên chạy với non-root user để giảm security risks và follow principle of least privilege.

```dockerfile
# ✅ GOOD: Create and use non-root user
FROM node:18-alpine

# Create group and user
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

WORKDIR /app

# Copy files with correct ownership
COPY --chown=appuser:appgroup package*.json ./
RUN npm ci && npm cache clean --force

# Copy source with correct ownership
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

CMD ["node", "index.js"]
```

```yaml
# docker-compose.yml
services:
  api:
    image: myapi:latest
    user: "1001:1001"
    # Or use named user
    user: "appuser:appgroup"
```

```bash
# Verify container runs as non-root
docker run -it myimage whoami
# Output: appuser

docker run -it myimage id
# Output: uid=1001(appuser) gid=1001(appgroup)
```

## Practice 6: Set Health Checks

### Mô tả

Define health checks để Docker có thể monitor container health và tự động restart khi cần.

```dockerfile
# HTTP health check
FROM nginx:alpine
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Command-based health check
FROM postgres:15-alpine
ENV POSTGRES_DB=myapp
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD pg_isready -U postgres -d myapp || exit 1

# Custom script health check
FROM node:18-alpine
WORKDIR /app
COPY healthcheck.sh .
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD /app/healthcheck.sh

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml với health check
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
```

## Practice 7: Use Proper Resource Limits

### Mô tả

Luôn set memory và CPU limits để ngăn containers consume excessive resources.

```yaml
version: '3.8'
services:
  api:
    image: myapi:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
    
    # Alternative: CLI flags
    # docker run -m 2g --cpus=2 myapp:latest

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

```bash
# Common mistakes to avoid
# ❌ NO limits - container can consume all resources
docker run myapp:latest

# ✅ WITH limits - controlled resource usage
docker run \
  --memory=1g \
  --memory-swap=2g \
  --cpus=1.5 \
  --cpuset-cpus=0,1 \
  --restart=on-failure:3 \
  myapp:latest
```

## Practice 8: Handle Signals Properly

### Mô tả

Container cần handle SIGTERM gracefully để enable graceful shutdown khi stop hoặc scale down.

```dockerfile
# Node.js with proper signal handling
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Use exec form (JSON array) - PID 1 receives signals directly
CMD ["node", "server.js"]

# If using shell form, wrap with exec
# CMD node server.js  # ❌ Shell form - doesn't pass signals properly
```

```typescript
// Node.js: Proper signal handling in application code
const server = app.listen(PORT);

const shutdown = async (signal) => {
  console.log(`Received ${signal}, starting graceful shutdown...`);
  
  // Stop accepting new connections
  server.close(() => {
    console.log('HTTP server closed');
  });
  
  // Wait for existing connections
  setTimeout(async () => {
    await closeDatabaseConnections();
    await closeRedisConnections();
    console.log('All connections closed, exiting');
    process.exit(0);
  }, 10000); // 10 second grace period
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
```

```dockerfile
# Python/FastAPI with signal handling
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Use exec form
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Practice 9: Use Labels for Metadata

### Mô tả

Add labels để document images và enable better organization, discovery, và automation.

```dockerfile
# Basic labels
FROM node:18-alpine
LABEL maintainer="team@example.com"
LABEL description="My application image"

# Standard labels following OCI spec
LABEL org.opencontainers.image.title="My Application"
LABEL org.opencontainers.image.description="Application description"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Team <team@example.com>"
LABEL org.opencontainers.image.source="https://github.com/org/repo"
LABEL org.opencontainers.image.vendor="Enterprise"
LABEL org.opencontainers.image.licenses="MIT"

# Custom business labels
LABEL com.enterprise.team="platform"
LABEL com.enterprise.cost-center="CC-1234"
LABEL com.enterprise.environment="production"
LABEL com.enterprise.tier="backend"
LABEL com.enterprise.prometheus="true"
```

```bash
# Query labels
docker inspect myimage --format='{{json .Config.Labels}}' | jq

# Filter by label
docker images --filter "label=com.enterprise.team=platform"
```

## Practice 10: Optimize for Production

### Mô tả

Production images cần optimizations khác với development images - smaller size, better security, proper logging.

```dockerfile
# Development Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install  # Development deps + devDependencies
COPY . .
CMD ["npm", "run", "dev"]

# Production Dockerfile
FROM node:18-alpine AS production
WORKDIR /app

# Production-only dependencies
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Build artifacts
COPY tsconfig.json ./
COPY src/ ./src/
RUN npm run build

# Copy source (not needed in final if built)
COPY . .

# Non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S appuser -u 1001
USER appuser

# Production settings
ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  api:
    build:
      context: .
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=info
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
```

## Practice 11: Implement Health Checks for All Services

### Mô tả

Tất cả services cần health checks để enable proper orchestration và self-healing.

```yaml
version: '3.8'
services:
  # API with custom health endpoint
  api:
    image: myapi:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
  
  # Database with built-in check
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  # Redis health check
  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    volumes:
      - redis_data:/data
  
  # Nginx as reverse proxy
  nginx:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      api:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
```

## Practice 12: Use BuildKit for Better Performance

### Mô tả

Enable Docker BuildKit để được improved build performance, better caching, và advanced features.

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Or use inline syntax
docker buildx build .
```

```dockerfile
# syntax=docker/dockerfile:1
# Enable BuildKit-specific features

# Cache mounts for package managers
FROM python:3.11-slim
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# SSH agent forwarding for private repos
RUN --mount=type=ssh \
    git clone git@github.com:org/private-repo.git

# Better layer caching
RUN --mount=type=cache,target=/tmp/cache \
    npm ci
```

```yaml
# docker-compose.yml với BuildKit
version: '3.8'
services:
  api:
    build:
      context: .
      builder: default
      args:
        - BUILD_VERSION=1.0.0
      labels:
        - "org.opencontainers.image.version=${BUILD_VERSION}"
```

## Related Documents

- [Docker Glossary](../glossary.md)
- [Docker Architecture](../architecture.md)
- [Docker Anti-Patterns](../anti-pattern.md)
- [Docker Checklist](../checklist.md)
- [Docker FAQ](../faq.md)
- [Docker Decision Tree](../decision-tree.md)
