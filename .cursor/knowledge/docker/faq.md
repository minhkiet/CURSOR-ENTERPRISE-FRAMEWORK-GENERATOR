# Docker Knowledge Base - FAQ

## Tổng quan

Document này cung cấp 10 câu hỏi thường gặp và câu trả lời chi tiết về Docker trong Cursor Enterprise Framework.

## Câu hỏi 1: Làm thế nào để giảm kích thước Docker image?

### Câu trả lời

Có nhiều strategies để giảm Docker image size, từ việc chọn base image đến multi-stage builds:

```dockerfile
# Strategy 1: Use Alpine-based images
# Ubuntu: ~80MB, Alpine: ~5MB
FROM node:18-alpine  # ~180MB vs ~950MB for node:18

# Strategy 2: Use slim variants
FROM python:3.11-slim-bookworm  # Smaller than full Python

# Strategy 3: Multi-stage builds
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (no build tools)
FROM node:18-alpine AS production
WORKDIR /app

# Only copy built artifacts and production deps
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001
USER nodeuser

CMD ["node", "dist/main.js"]

# Strategy 4: Distroless images (smallest)
FROM gcr.io/distroless/nodejs18-debian11
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["dist/main.js"]

# Strategy 5: Scratch (smallest possible, no OS)
FROM golang:1.21-alpine AS builder
WORKDIR /build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp

FROM scratch
COPY --from=builder /build/myapp /myapp
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
CMD ["/myapp"]
```

### Best practices

1. **Chỉ cài đặt những gì cần thiết**: `pip install --no-cache-dir` thay vì `pip install`
2. **Clean up trong cùng một layer**: Kết hợp install và cleanup
3. **Sử dụng BuildKit cache mounts**: Giảm image size mà không mất caching benefits
4. **Font subsetting và image optimization**: Giảm assets size

## Câu hỏi 2: Sự khác biệt giữa CMD và ENTRYPOINT là gì?

### Câu trả lời

CMD và ENTRYPOINT đều define command được execute khi container start, nhưng có subtle differences:

```dockerfile
# CMD: Default command (có thể override từ CLI)
# Shell form
CMD echo "Hello"

# Exec form (recommended)
CMD ["echo", "Hello"]

# ENTRYPOINT: Configure container như executable
ENTRYPOINT ["python", "app.py"]
# Container chạy như: python app.py [args]

# Kết hợp ENTRYPOINT và CMD
ENTRYPOINT ["python", "app.py"]
CMD ["--default", "arg"]
# Container chạy như: python app.py --default arg
# Override CMD: docker run myapp --custom arg
# Container chạy: python app.py --custom arg
```

### Use cases

| Directive | Use Case |
|-----------|----------|
| CMD | Default arguments, có thể override |
| ENTRYPOINT | Container như executable, arguments appended |
| CMD [] | Làm gì cả khi không có command nào được truyền |
| ENTRYPOINT + CMD | Best practice cho flexible images |

```dockerfile
# Ví dụ: Python CLI tool
FROM python:3.11-alpine
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "-m", "mytool"]
CMD ["--help"]

# Usage:
# docker run mytool              # Runs: python -m mytool --help
# docker run mytool --version    # Runs: python -m mytool --version
# docker run mytool subcommand    # Runs: python -m mytool subcommand
```

## Câu hỏi 3: Làm thế nào để handle graceful shutdown trong Docker?

### Câu trả lời

Graceful shutdown đảm bảo container stop một cách clean, không mất data hoặc break in-progress requests.

```typescript
// Node.js: Proper signal handling
const server = app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});

let isShuttingDown = false;

const gracefulShutdown = async (signal) => {
  if (isShuttingDown) return;
  isShuttingDown = true;
  
  console.log(`\nReceived ${signal}. Starting graceful shutdown...`);
  
  // 1. Stop accepting new connections
  server.close(async () => {
    console.log('HTTP server closed');
    
    try {
      // 2. Close database connections
      await db.end();
      console.log('Database connections closed');
      
      // 3. Close Redis connections
      await redis.quit();
      console.log('Redis connections closed');
      
      // 4. Flush pending logs
      await logger.flush();
      console.log('Logs flushed');
      
      console.log('Graceful shutdown completed');
      process.exit(0);
    } catch (error) {
      console.error('Error during shutdown:', error);
      process.exit(1);
    }
  });
  
  // 5. Force exit after timeout
  setTimeout(() => {
    console.error('Could not close connections in time, forcefully shutting down');
    process.exit(1);
  }, 30000); // 30 second grace period
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

```dockerfile
# Dockerfile: Use exec form for proper signal handling
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Use exec form - signals go directly to process
CMD ["node", "server.js"]
# NOT: CMD node server.js (shell form)
```

```yaml
# docker-compose.yml: Configure stop signal
services:
  api:
    image: myapi:latest
    stop_signal: SIGTERM
    # Or custom signal
    # stop_signal: SIGUSR1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      timeout: 10s
      retries: 3
```

```bash
# Test graceful shutdown
docker stop --time=30 my_container

# Watch the shutdown process
docker logs -f my_container
```

## Câu hỏi 4: Multi-stage builds hoạt động như thế nào?

### Câu trả lời

Multi-stage builds cho phép sử dụng nhiều FROM statements để optimize image size:

```dockerfile
# ============================================
# Stage 1: Dependency installation
# ============================================
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# ============================================
# Stage 2: Build
# ============================================
FROM node:18-alpine AS builder
WORKDIR /app

# Copy dependencies from first stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build the application
RUN npm run build

# ============================================
# Stage 3: Test (optional)
# ============================================
FROM builder AS test
WORKDIR /app
RUN npm run test

# ============================================
# Stage 4: Production
# ============================================
FROM node:18-alpine AS production
WORKDIR /app

# Copy only built artifacts
COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY package*.json ./

# Create user and set environment
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001
USER nodeuser

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "dist/main.js"]
```

```bash
# Build specific stage
docker build --target production -t myapp:latest .

# Build all stages
docker build -t myapp:latest .

# Size comparison
docker images | grep myapp
# REPOSITORY   TAG       SIZE
# myapp        builder   1.2GB
# myapp        latest    180MB
```

## Câu hỏi 5: Làm thế nào để debug Docker containers?

### Câu trả lời

```bash
# 1. Kiểm tra container logs
docker logs my_container
docker logs -f my_container  # Follow logs
docker logs --tail 100 my_container  # Last 100 lines

# 2. Exec vào container
docker exec -it my_container /bin/sh
docker exec -it my_container /bin/bash
docker exec -it my_container env  # View environment variables

# 3. Inspect container
docker inspect my_container
docker inspect --format='{{.State.Status}}' my_container
docker inspect --format='{{.NetworkSettings.IPAddress}}' my_container

# 4. Check resource usage
docker stats my_container
docker stats --no-stream my_container

# 5. Network debugging
docker exec -it my_container nslookup google.com
docker exec -it my_container curl -v http://api:3000/health

# 6. Process list
docker exec -it my_container ps aux

# 7. File system inspection
docker exec -it my_container ls -la /app
docker cp my_container:/app/logs ./local_logs

# 8. Network connectivity
docker exec -it my_container ping api
docker exec -it my_container telnet db 5432
```

```yaml
# Add debug utilities in development
services:
  api:
    image: myapi:latest
    profiles:
      - debug
    build:
      context: .
      target: debug  # Development target with tools
  
  debug:
    image: curlimages/curl:latest
    profiles:
      - debug
    network_mode: "service:api"
```

## Câu hỏi 6: Docker networking hoạt động như thế nào?

### Câu trả lời

```yaml
version: '3.8'
services:
  # Bridge network (default)
  web:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "8080:80"
  
  # Connects to backend network
  api:
    image: myapi:latest
    networks:
      - frontend
      - backend
    environment:
      - DB_HOST=database
      - REDIS_HOST=redis
    depends_on:
      db:
        condition: service_healthy
  
  # Database on backend network only
  database:
    image: postgres:15-alpine
    networks:
      - backend
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  redis:
    image: redis:7-alpine
    networks:
      - backend
    volumes:
      - redis_data:/data

networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  backend:
    driver: bridge
    internal: true  # No external access

volumes:
  db_data:
  redis_data:
```

### Network types

| Driver | Use Case | Features |
|--------|----------|----------|
| bridge | Single host, default | Isolated network |
| host | Performance-critical | No isolation |
| overlay | Multi-host (Swarm) | Distributed networking |
| macvlan | Direct L2 attach | Physical network access |
| none | No networking | Completely isolated |

## Câu hỏi 7: Làm thế nào để manage secrets trong Docker?

### Câu trả lời

```yaml
# Docker Compose với external secrets
version: '3.8'
services:
  api:
    image: myapi:latest
    secrets:
      - db_password
      - api_key
    env_file:
      - ./config.env  # Non-sensitive config
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - API_KEY_FILE=/run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Managed externally (Vault, AWS Secrets Manager)

# Or use environment variables for non-sensitive config
```

```bash
# Create secrets at runtime
echo "mysecretpassword" | docker secret create db_password -
docker secret ls
docker secret inspect db_password
```

```yaml
# Kubernetes-style (works with Docker Compose v2.4+)
services:
  api:
    image: myapi:latest
    environment:
      DB_PASSWORD:
        file: /run/secrets/db_password
    configs:
      - source: app_config
        target: /app/config.yaml

configs:
  app_config:
    file: ./config.yaml

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Câu hỏi 8: Resource limits nên set như thế nào?

### Câu trả lời

```yaml
version: '3.8'
services:
  # High-memory service
  api:
    image: myapi:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'           # Max 2 CPU cores
          memory: 2G            # Max 2GB RAM
          pids: 1000            # Max 1000 processes
        reservations:
          cpus: '0.5'           # Guaranteed minimum
          memory: 512M          # Guaranteed minimum
  
  # CPU-intensive worker
  worker:
    image: myworker:latest
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 1G
  
  # Lightweight service
  redis:
    image: redis:7-alpine
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

### Memory swap configuration

```bash
# --memory-swap: Total memory + swap
# --memory: Physical memory limit

# Scenario 1: No swap allowed
docker run --memory=1g --memory-swap=1g myapp
# Container can use 1GB RAM, NO swap

# Scenario 2: Swap enabled (2x RAM)
docker run --memory=1g --memory-swap=2g myapp
# Container can use 1GB RAM + 1GB swap

# Scenario 3: Unlimited swap
docker run --memory=1g --memory-swap=-1 myapp
# Container can use 1GB RAM + unlimited swap
```

## Câu hỏi 9: Health checks nên implement như thế nào?

### Câu trả lời

```dockerfile
# HTTP health check
FROM node:18-alpine
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Database health check
FROM postgres:15-alpine
ENV POSTGRES_DB=myapp
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD pg_isready -U postgres -d ${POSTGRES_DB} || exit 1

# Custom script health check
FROM myapp:latest
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD ["/app/healthcheck.sh"]

CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml với comprehensive health checks
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
      redis:
        condition: service_healthy
  
  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
  
  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 3
```

```typescript
// Express: Health check endpoint
app.get('/health', async (req, res) => {
  try {
    // Check database
    await db.query('SELECT 1');
    
    // Check Redis
    await redis.ping();
    
    // Check external services
    const paymentService = await paymentClient.healthCheck();
    
    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: 'up',
        redis: 'up',
        payment: paymentService.status
      }
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message
    });
  }
});
```

## Câu hỏi 10: CI/CD pipeline với Docker nên thiết kế như thế nào?

### Câu trả lời

```yaml
# .gitlab-ci.yml hoặc GitHub Actions workflow
stages:
  - build
  - test
  - scan
  - push
  - deploy

variables:
  DOCKER_REGISTRY: registry.example.com
  IMAGE_NAME: myapp

build:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  script:
    - docker build --target builder -t ${IMAGE_NAME}:build .
    - docker save ${IMAGE_NAME}:build | gzip > /tmp/build.tar.gz
  artifacts:
    paths:
      - /tmp/build.tar.gz
    expire_in: 1 hour

test:integration:
  stage: test
  image: ${DOCKER_REGISTRY}/${IMAGE_NAME}:build
  services:
    - postgres:15-alpine
    - redis:7-alpine
  script:
    - npm run test:integration
  needs:
    - build

scan:
  stage: scan
  image: docker:24-dind
  script:
    - docker load < /tmp/build.tar.gz
    - trivy image --exit-code 1 --severity HIGH,CRITICAL ${IMAGE_NAME}:build
  allow_failure: false

push:
  stage: push
  image: docker:24-dind
  script:
    - docker load < /tmp/build.tar.gz
    - docker tag ${IMAGE_NAME}:build ${DOCKER_REGISTRY}/${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}
    - docker tag ${IMAGE_NAME}:build ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
    - echo ${DOCKER_REGISTRY_TOKEN} | docker login ${DOCKER_REGISTRY} -u ci --password-stdin
    - docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}
    - docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
  only:
    - main
  needs:
    - scan

deploy:staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp api=${DOCKER_REGISTRY}/${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}
    - kubectl rollout status deployment/myapp
  environment:
    name: staging
  only:
    - main
```

## Related Documents

- [Docker Glossary](../glossary.md)
- [Docker Architecture](../architecture.md)
- [Docker Best Practices](../best-practice.md)
- [Docker Anti-Patterns](../anti-pattern.md)
- [Docker Checklist](../checklist.md)
- [Docker Decision Tree](../decision-tree.md)
