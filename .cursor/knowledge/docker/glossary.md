# Docker Knowledge Base - Glossary

## Tổng quan

Document này cung cấp danh sách các thuật ngữ chuyên ngành liên quan đến Docker trong Cursor Enterprise Framework. Các thuật ngữ được phân loại theo từng nhóm để dễ tra cứu.

## Nhóm 1: Core Docker Concepts

### 1. Docker

Nền tảng containerization cho phép đóng gói ứng dụng và các dependencies vào một đơn vị standalone gọi là container. Docker cung cấp công cụ để build, run, và manage containers trên các môi trường khác nhau.

```dockerfile
# Example: Simple Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Docker sử dụng client-server architecture với Docker daemon (server) và Docker client (CLI) giao tiếp qua REST API. Containers cung cấp isolation nhưng chia sẻ OS kernel, làm cho chúng nhẹ hơn VMs.

### 2. Container

Đơn vị runtime của Docker, chứa tất cả những gì cần thiết để chạy một ứng dụng: code, runtime, system tools, libraries, và settings. Container được tạo từ Docker images và có thể start, stop, move, và delete.

```bash
# Create and run a container
docker run -d --name my-app -p 8080:80 nginx:alpine

# List running containers
docker ps

# Stop a container
docker stop my-app

# Remove a container
docker rm my-app
```

Containers tồn tại trong filesystem layer và có writable layer cho phép thay đổi trong runtime mà không ảnh hưởng đến image gốc.

### 3. Docker Image

Template read-only chứa tất cả instructions để tạo container. Image được build từ Dockerfile và có thể được share qua registries như Docker Hub, Google Container Registry, hoặc private registries.

```bash
# Build an image
docker build -t myapp:1.0.0 .

# Tag an image
docker tag myapp:1.0.0 registry.example.com/myapp:1.0.0

# Push to registry
docker push registry.example.com/myapp:1.0.0

# Pull from registry
docker pull nginx:1.25-alpine
```

Images sử dụng layered architecture cho phép caching và reuse. Mỗi instruction trong Dockerfile tạo ra một layer mới.

### 4. Dockerfile

Text file chứa instructions để build Docker image. Dockerfile syntax bao gồm các instructions như FROM, RUN, COPY, CMD, ENV, và nhiều others.

```dockerfile
# Multi-stage Dockerfile example
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS production
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

## Nhóm 2: Image Management

### 5. Docker Registry

Service lưu trữ và phân phối Docker images. Public registries như Docker Hub chứa hàng ngàn pre-built images. Private registries được sử dụng cho internal images.

```bash
# Login to registry
docker login registry.example.com

# Pull image
docker pull myregistry.azurecr.io/myapp:v1

# Push image
docker push myregistry.azurecr.io/myapp:v1

# Logout
docker logout registry.example.com
```

Common registry options bao gồm Docker Hub, Amazon ECR, Google GCR, Azure Container Registry, và self-hosted registries như Harbor hoặc GitLab Container Registry.

### 6. Docker Tag

Identifier gắn với image để version và track builds. Tags không unique - nhiều images có thể có cùng tag.

```bash
# Tag for version
docker tag myapp:latest myapp:1.0.0
docker tag myapp:latest myapp:1.0
docker tag myapp:latest myapp:stable

# Tag for environment
docker tag myapp:latest myapp:production
docker tag myapp:latest myapp:staging
```

Best practice: Luôn sử dụng specific tags (version numbers) thay vì `latest` trong production để đảm bảo reproducibility.

### 7. Multi-stage Build

Docker feature cho phép sử dụng nhiều FROM statements để optimize image size. Chỉ artifacts cần thiết được copy vào final image.

```dockerfile
# Build stage with full tooling
FROM golang:1.21 AS builder
WORKDIR /build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp

# Runtime stage - minimal base
FROM alpine:3.18
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /build/myapp .
CMD ["./myapp"]
```

Multi-stage builds giảm image size đáng kể bằng cách loại bỏ build dependencies và unnecessary files từ production image.

## Nhóm 3: Container Operations

### 8. Docker Volume

Mechanism để persist data giữa container restarts và share data giữa containers. Volumes được quản lý bởi Docker và tách biệt khỏi container's filesystem.

```bash
# Create volume
docker volume create mydata

# Run container with volume
docker run -d -v mydata:/app/data myapp:latest

# Run with bind mount
docker run -d -v /host/path:/container/path myapp:latest

# Inspect volume
docker volume inspect mydata

# Remove volume
docker volume rm mydata
```

Volume types bao gồm: named volumes (managed by Docker), bind mounts (host filesystem), và tmpfs mounts (memory-based).

### 9. Docker Network

Cơ chế cho containers communicate với nhau và với external world. Docker cung cấp several network drivers.

```bash
# Create network
docker network create mynetwork

# Run container in network
docker run -d --network mynetwork --name app myapp:latest

# Connect container to network
docker network connect mynetwork database

# List networks
docker network ls

# Inspect network
docker network inspect bridge
```

Network drivers: bridge (default cho standalone containers), host (removes network isolation), overlay (swarm mode), macvlan (assign MAC address), và none (disable networking).

### 10. Port Mapping

Expose container's port(s) đến host machine qua `-p` flag. Format: `host_port:container_port`.

```bash
# Map single port
docker run -d -p 8080:80 nginx

# Map multiple ports
docker run -d -p 3000:3000 -p 5000:5000 myapp

# Map UDP port
docker run -d -p 8080:80/udp myapp

# Map random host port
docker run -d -P nginx  # Maps to random available ports
```

## Nhóm 4: Container Lifecycle

### 11. Docker Compose

Tool định nghĩa và chạy multi-container applications. Sử dụng YAML file để configure services, networks, và volumes.

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
      - redis
    networks:
      - app-network
  
  db:
    image: postgres:15-alpine
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    networks:
      - app-network

volumes:
  db-data:

networks:
  app-network:
    driver: bridge
```

### 12. Docker Swarm

Native clustering và scheduling cho Docker. Cho phép quản lý cluster của Docker engines như một virtual system.

```bash
# Initialize swarm
docker swarm init

# Join worker
docker swarm join --token <token> <manager-ip>:2377

# Deploy stack
docker stack deploy -c docker-compose.yml myapp

# List services
docker service ls

# Scale service
docker service scale myapp_web=5

# Leave swarm
docker swarm leave --force
```

Swarm features bao gồm: load balancing, rolling updates, rollback, service discovery, và distributed secret management.

## Nhóm 5: Security

### 13. Docker Security

Các best practices và features để secure containers: user namespaces, seccomp, SELinux, AppArmor, và capability dropping.

```dockerfile
# Run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Drop all capabilities
USER nobody --group=nobody
# Or use explicit capabilities
USER appuser --cap-drop=ALL --cap-add=NET_BIND_SERVICE
```

Security considerations bao gồm: image scanning, minimal base images, read-only root filesystems, non-root users, và resource limits.

### 14. Docker Secrets

Secure way để manage sensitive data như passwords, tokens, và SSH keys trong Swarm mode.

```bash
# Create secret
echo "mypassword" | docker secret create db_password -

# Create secret from file
docker secret create mycert /path/to/cert.pem

# Use in service
docker service create \
  --name api \
  --secret db_password \
  myapp:latest
```

Secrets được encrypted at rest và in transit, chỉ available cho services that explicitly request them.

## Nhóm 6: Orchestration & Production

### 15. Container Orchestration

Quản lý container lifecycles trong production: scheduling, scaling, networking, load balancing, và high availability.

Modern orchestration platforms bao gồm Kubernetes (most popular), Docker Swarm, Amazon ECS, Apache Mesos, và Nomad. Each cung cấp features cho deployment strategies, service discovery, và resource management.

### 16. Health Check

Docker feature để determine whether container is healthy. Used by Docker và orchestrators để make decisions về traffic routing và restarts.

```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Command-based health check
HEALTHCHECK --interval=1m --timeout=3s --retries=3 \
  CMD ["mysqladmin", "ping", "-h", "localhost"]
```

Health checks được Docker daemon execute và container status changed based on exit code.

### 17. Resource Limits

Container configuration để giới hạn CPU, memory, và other resources.

```bash
# Memory limit
docker run -m 512m myapp:latest

# CPU limit
docker run --cpus="1.5" myapp:latest
docker run --cpuset-cpus="0,1" myapp:latest

# Combined limits
docker run \
  --memory=1g \
  --memory-swap=2g \
  --cpus=2 \
  --cpuset-cpus=0,1 \
  myapp:latest
```

Setting resource limits prevents containers từ consuming excessive resources và affecting other containers.

## Nhóm 7: Development & CI/CD

### 18. Docker BuildKit

Next-generation build backend với improved performance, caching, và features. Enabled by default in Docker 23.0+.

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with BuildKit
docker build -t myapp:latest .

# Use cache mount for faster builds
docker build --mount=type=cache,target=/root/.cache/pip \
  -t myapp:latest .
```

BuildKit features bao gồm: parallel build execution, improved caching, secret mounting, và inline cache from registry.

### 19. Docker Layer Caching

Mechanism để reuse layers giữa builds. Effective caching depends on instruction order và file modification patterns.

```dockerfile
# Good caching: dependencies first
COPY package*.json ./
RUN npm ci

# Bad: full source first
COPY . .  # Invalidates cache for all above
RUN npm ci

# Better: source after dependencies
COPY package*.json ./
RUN npm ci
COPY . .
```

Caching strategy quan trọng cho CI/CD performance. Small changes nên không invalidate expensive build steps.

### 20. .dockerignore

File similar to .gitignore để exclude files và directories từ build context, giảm image size và build time.

```
# Comments
.git
.gitignore
*.md
node_modules
dist
build
.env
.env.*
!env.example
.vscode
tests
__pycache__
*.pyc
```

Excluding unnecessary files từ build context giảm thời gian upload context đến Docker daemon và giảm image size.

## Related Documents

- [Docker Architecture](../architecture.md)
- [Docker Best Practices](../best-practice.md)
- [Docker Anti-Patterns](../anti-pattern.md)
- [Docker Checklist](../checklist.md)
- [Docker FAQ](../faq.md)
- [Docker Decision Tree](../decision-tree.md)
