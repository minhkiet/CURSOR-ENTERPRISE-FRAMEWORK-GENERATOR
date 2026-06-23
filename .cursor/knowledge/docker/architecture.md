# Docker Knowledge Base - Architecture

## Tổng quan

Document này mô tả chi tiết kiến trúc hệ thống Docker trong Cursor Enterprise Framework, bao gồm các components, interactions, và design patterns cho production-ready deployments.

## 1. Docker Architecture Overview

### 1.1 Client-Server Model

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Host                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Containers  │    │   Containers │    │   Containers │      │
│  │    App A     │    │    App B     │    │    App C     │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                    │                    │              │
│  ┌──────┴────────────────────┴────────────────────┴───────┐     │
│  │                    Docker Daemon (dockerd)              │     │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │     │
│  │  │ Volume  │  │ Network │  │ Image   │  │ Container│   │     │
│  │  │ Manager │  │ Manager │  │ Manager │  │ Manager │   │     │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │     │
│  └──────────────────────────┬──────────────────────────────┘     │
│                             │                                     │
│  ┌──────────────────────────┴──────────────────────────────┐     │
│  │                    Container Runtime                      │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │     │
│  │  │ runc        │  │ containerd  │  │ shim        │     │     │
│  │  │ (low-level) │  │ (high-level)│  │ (detach)    │     │     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
                               ▲
                               │ REST API (Unix Socket)
                               │
┌──────────────────────────────┴────────────────────────────────────┐
│                        Docker Client                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │    CLI       │  │  SDK/API     │  │ Compose CLI  │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└───────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Responsibilities

#### Docker Daemon (dockerd)
- Lắng nghe Docker API requests
- Quản lý Docker objects (images, containers, networks, volumes)
- Build images từ Dockerfiles
- Handle container lifecycle
- Expose REST API qua Unix socket hoặc TCP

#### Container Runtime
- **runc**: Low-level runtime tạo và run containers theo OCI specification
- **containerd**: High-level runtime quản lý container lifecycle (start, stop, pause)
- **containerd-shim**: Cho phép containers run independently sau khi containerd exits

#### Docker Client
- CLI tool (docker) giao tiếp với daemon
- SDKs cho multiple languages (Go, Python, JavaScript, etc.)
- Docker Compose CLI cho multi-container applications

## 2. Image Architecture

### 2.1 Layered Filesystem

```
┌─────────────────────────────────────────────────────────────────┐
│                     Container Layer (R/W)                       │
│  Writable layer created when container starts                   │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                     Image Layer 5 (CMD)                          │
│  CMD ["python", "app.py"]                                        │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                     Image Layer 4 (COPY)                         │
│  Application code                                                │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                     Image Layer 3 (RUN)                          │
│  pip install -r requirements.txt                                 │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                     Image Layer 2 (COPY)                         │
│  requirements.txt                                               │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                     Image Layer 1 (RUN)                          │
│  apt-get update && apt-get install -y python3 python3-pip        │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                     Base Image Layer (OS)                        │
│  FROM ubuntu:22.04                                              │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Storage Drivers

```bash
# Check current storage driver
docker info | grep "Storage Driver"

# Available storage drivers
- overlay2 (recommended for most cases)
- devicemapper (legacy)
- btrfs (for specific use cases)
- zfs (for specific use cases)
- vfs (testing only)
```

```yaml
# /etc/docker/daemon.json
{
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
```

## 3. Network Architecture

### 3.1 Network Drivers

```
┌─────────────────────────────────────────────────────────────────┐
│                      Network Types                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Bridge    │  │    Host     │  │   Overlay   │              │
│  │             │  │             │  │             │              │
│  │  Default    │  │  No iso-    │  │  Swarm      │              │
│  │  for single │  │  lation     │  │  multi-host │              │
│  │  host       │  │             │  │             │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Macvlan   │  │   IPvlan    │  │   None      │              │
│  │             │  │             │  │             │              │
│  │  Direct     │  │  Direct     │  │  No network │              │
│  │  L2 attach  │  │  L3 attach  │  │             │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Bridge Network Configuration

```bash
# Create custom bridge network
docker network create \
  --driver bridge \
  --subnet=172.20.0.0/16 \
  --ip-range=172.20.5.0/24 \
  --gateway=172.20.0.1 \
  my-network

# Run container in custom network
docker run -d --network my-network --name app myapp:latest

# Connect existing container to network
docker network connect my-network database

# Inspect network
docker network inspect my-network
```

### 3.3 DNS and Service Discovery

```yaml
# docker-compose.yml với DNS service discovery
version: '3.8'
services:
  web:
    build: .
    container_name: web
    networks:
      - frontend
      - backend
  
  api:
    build: ./api
    container_name: api
    networks:
      - backend
  
  database:
    image: postgres:15-alpine
    container_name: database
    networks:
      - backend
  
  nginx:
    image: nginx:alpine
    container_name: nginx
    networks:
      - frontend
    ports:
      - "80:80"

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

Trong user-defined bridge network, containers có thể communicate bằng container name như hostname.

## 4. Volume Architecture

### 4.1 Volume Types

```
┌─────────────────────────────────────────────────────────────────┐
│                    Volume Types                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │     Named Volume     │  │    Bind Mount        │              │
│  │                      │  │                      │              │
│  │  Managed by Docker  │  │  Host filesystem     │              │
│  │  Persistent         │  │  Live changes        │              │
│  │  Portable            │  │  Host-dependent      │              │
│  │                      │  │                      │              │
│  │  docker volume create│  │  -v /host:/container  │              │
│  │  -v myvol:/data      │  │                      │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                   │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │     tmpfs Mount     │  │    Named Pipe       │              │
│  │                      │  │                      │              │
│  │  Memory-based       │  │  For IPC            │              │
│  │  Non-persistent     │  │  Host-dependent     │              │
│  │  Secure             │  │                      │              │
│  │                      │  │  --volumes-from     │              │
│  │  --tmpfs /data      │  │                      │              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Volume Driver Architecture

```bash
# List volume drivers
docker plugin ls | grep volume

# Common volume plugins
- local (default)
- azure-file (Azure)
- gce-docker (Google Cloud)
- rexray (AWS, Azure, GCP)
- convoy (multi-driver)
```

```yaml
# Using cloud-specific volume
services:
  app:
    image: myapp:latest
    volumes:
      - mystorage:/data

volumes:
  mystorage:
    driver: azure_file
    driver_opts:
      share_name: myfileshare
      storage_account_name: mystorageaccount
```

## 5. Multi-Stage Build Architecture

### 5.1 Build Strategy

```dockerfile
# ============================================
# STAGE 1: Dependencies
# ============================================
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# ============================================
# STAGE 2: Build
# ============================================
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# ============================================
# STAGE 3: Test
# ============================================
FROM builder AS test
RUN npm run test

# ============================================
# STAGE 4: Production
# ============================================
FROM node:18-alpine AS production
WORKDIR /app

# Security: create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001

# Copy built artifacts
COPY --from=builder --chown=nodeuser:nodejs /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules

# Set environment
ENV NODE_ENV=production
ENV PORT=3000

# Switch to non-root user
USER nodeuser

EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### 5.2 Build Cache Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                 Build Cache Optimization                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  CACHE HIT (fast)          CACHE MISS (slow)                    │
│  ───────────────           ─────────────────                    │
│                                                                   │
│  FROM node:18-alpine       FROM node:18-alpine                  │
│         │                         │                              │
│  COPY package*.json       COPY package*.json                    │
│         │                         │                              │
│  RUN npm ci ← cached      RUN npm ci ← rebuild                  │
│         │                         │                              │
│  COPY . . ← invalidates cache                                 │
│         │                         │                              │
│  RUN npm run build                                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 6. Security Architecture

### 6.1 Container Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                  Container Security Layers                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Layer 1: Image Security                                         │
│  - Scan for vulnerabilities                                      │
│  - Use trusted base images                                        │
│  - Sign and verify images                                         │
│                                                                   │
│  Layer 2: Container Hardening                                     │
│  - Drop capabilities                                             │
│  - No privileged mode                                             │
│  - Read-only root filesystem                                       │
│  - No SUID binaries                                               │
│                                                                   │
│  Layer 3: Runtime Security                                        │
│  - Seccomp profiles                                              │
│  - AppArmor/SELinux profiles                                      │
│  - Resource limits                                                │
│  - Network policies                                               │
│                                                                   │
│  Layer 4: Secrets Management                                       │
│  - Docker Secrets (Swarm)                                         │
│  - External secret stores                                         │
│  - Environment variables (with care)                              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Security Configuration Example

```yaml
# docker-compose.yml với security configurations
version: '3.8'
services:
  api:
    image: myapi:latest
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp
      - /run
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
      nproc:
        soft: 4096
        hard: 4096
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 7. Logging Architecture

### 7.1 Logging Drivers

```bash
# Configure logging driver
docker daemon --log-driver=json-file --log-opt max-size=10m --log-opt max-file=3

# Or in daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Available drivers: json-file (default), syslog, journald, gelf, fluentd, awslogs, splunk, etwlogs, gcplogs.

### 7.2 Centralized Logging

```yaml
# docker-compose.yml với centralized logging
version: '3.8'
services:
  app:
    image: myapp:latest
    logging:
      driver: "fluentd"
      options:
        fluentd-address: fluentd:24224
        tag: "myapp.{{.Name}}"
  
  fluentd:
    image: fluent/fluentd:v1.16-1
    ports:
      - "24224:24224"
      - "24224:24224/udp"
    volumes:
      - ./fluentd/etc:/fluentd/etc
    environment:
      FLUENTD_CONF: fluent.conf
```

## 8. Resource Management Architecture

### 8.1 Memory and CPU Limits

```yaml
# docker-compose.yml với resource limits
version: '3.8'
services:
  api:
    image: myapi:latest
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
  
  worker:
    image: myworker:latest
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### 8.2 OOM Handling

```
┌─────────────────────────────────────────────────────────────────┐
│               Memory Pressure Response                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Container A                  Container B                        │
│  Memory: 500MB                Memory: 500MB                       │
│  Limit: 1GB                  Limit: 1GB                         │
│       │                            │                            │
│       ▼                            ▼                            │
│  ┌─────────────────────────┐  ┌─────────────────────────┐      │
│  │  OOM Killer Triggered   │  │  OOM Killer Triggered   │      │
│  │  when memory usage      │  │  when memory usage      │      │
│  │  exceeds limit          │  │  exceeds limit          │      │
│  └─────────────────────────┘  └─────────────────────────┘      │
│           │                            │                         │
│           ▼                            ▼                         │
│  Container STOPS/                 Container STOPS/               │
│  RESTARTS (if restart policy)    RESTARTS (if restart policy)  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 9. High Availability Architecture

### 9.1 Swarm Mode Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Docker Swarm Cluster                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                    ┌─────────────────┐                          │
│                    │  Manager Node   │                          │
│                    │  (Leader)       │                          │
│                    │  - Orchestrates │                          │
│                    │  - API endpoint │                          │
│                    │  - State store  │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│              ┌──────────────┼──────────────┐                    │
│              │              │              │                    │
│     ┌────────▼────────┐    │    ┌────────▼────────┐           │
│     │  Manager Node    │    │    │  Manager Node    │           │
│     │  (Follower)      │    │    │  (Follower)      │           │
│     └────────┬────────┘    │    └────────┬────────┘           │
│              │              │              │                    │
│              └──────────────┼──────────────┘                    │
│                             │                                   │
│     ┌───────────────────────┼───────────────────────┐          │
│     │                       │                       │          │
│ ┌───▼───┐ ┌───────────┐ ┌───▼───┐ ┌───────────┐ ┌───▼───┐      │
│ │ Worker│ │  Worker   │ │ Worker│ │  Worker   │ │ Worker│      │
│ │ Node  │ │  Node     │ │ Node  │ │  Node     │ │ Node  │      │
│ └───────┘ └───────────┘ └───────┘ └───────────┘ └───────┘      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Service Distribution

```yaml
# docker-compose.yml for Swarm deployment
version: '3.8'
services:
  api:
    image: myapi:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
        monitor: 5s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
      placement:
        constraints:
          - "node.role==worker"
          - "engine.labels.zone==public"
        preferences:
          - spread: engine.labels.rack
```

## Related Documents

- [Docker Glossary](../glossary.md)
- [Docker Best Practices](../best-practice.md)
- [Docker Anti-Patterns](../anti-pattern.md)
- [Docker Checklist](../checklist.md)
- [Docker FAQ](../faq.md)
- [Docker Decision Tree](../decision-tree.md)
