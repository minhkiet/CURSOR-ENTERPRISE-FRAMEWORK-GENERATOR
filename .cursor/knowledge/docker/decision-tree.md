# Docker Knowledge Base - Decision Tree

## Tổng quan

Document này cung cấp cây quyết định chi tiết để hướng dẫn việc lựa chọn các best practices và configurations phù hợp trong Cursor Enterprise Framework.

## 1. Image Selection Decision Tree

```
Bạn cần chọn base image như thế nào?
│
├── Language/Framework nào?
│   ├── Node.js → node:18-alpine
│   ├── Python → python:3.11-slim
│   ├── Go → golang:1.21-alpine
│   ├── Java → eclipse-temurin:21-jre-alpine
│   ├── .NET → mcr.microsoft.com/dotnet/aspnet:8.0
│   └── Ruby → ruby:3.2-alpine
│
├── Production hay Development?
│   ├── Production → Alpine/slim variants
│   │   └── Cần tối ưu size?
│   │       ├── Có → Distroless hoặc Scratch
│   │       └── Không → Alpine đã đủ nhẹ
│   │
│   └── Development → Full images có dev tools
│
└── Có cần full Linux utilities không?
    ├── Có → Ubuntu/Debian
    └── Không → Alpine (musl libc, smaller)

QUYẾT ĐỊNH CUỐI CÙNG:
┌─────────────────────────────────────────────────────────────┐
│ Production + Size-critical    → Alpine/slim                 │
│ Production + Security-critical → Distroless                 │
│ Development                   → Full image với dev tools     │
│ Static language (Go, Rust)   → Scratch hoặc Distroless      │
└─────────────────────────────────────────────────────────────┘
```

## 2. Dockerfile Instruction Decision Tree

```
Bạn cần thêm instruction nào vào Dockerfile?
│
├── Cần copy files?
│   ├── Code → COPY
│   ├── Secrets → Use Docker secrets, không COPY
│   └── Build artifacts → COPY --from=builder
│
├── Cần install dependencies?
│   ├── npm → npm ci --only=production
│   ├── pip → pip install --no-cache-dir
│   ├── apt → apt-get install --no-install-recommends
│   └── apt clean trong cùng layer!
│
├── Cần set working directory?
│   └── WORKDIR (tự động tạo directory)
│
├── Cần expose port?
│   ├── HTTP → EXPOSE 80 hoặc 8080
│   ├── HTTPS → EXPOSE 443
│   └── Custom → Port của ứng dụng
│
└── Cần CMD hay ENTRYPOINT?
    ├── Application executable → ENTRYPOINT ["executable"]
    ├── Default arguments → CMD ["default", "args"]
    └── Script/both → ENTRYPOINT + CMD
```

## 3. Multi-Stage Build Decision Tree

```
Bạn có nên dùng multi-stage build không?
│
├── Language có compilation step?
│   ├── Có (Go, Rust, C++, Java) → YES, multi-stage
│   │   ├── Build stage với compiler
│   │   └── Production stage với runtime only
│   │
│   └── Không (Node.js, Python, Ruby) → MAYBE
│       ├── Image size > 500MB? → YES, multi-stage
│       ├── Production deps khác dev deps? → YES
│       └── Cần separate build/test stages? → YES
│
└── Benefits của multi-stage:
    - Smaller image size
    - Better security (no build tools in prod)
    - Separation of concerns
    - Cache optimization
```

## 4. Network Configuration Decision Tree

```
Bạn cần cấu hình networking như thế nào?
│
├── Container cần access internet?
│   ├── Có → Bridge network (default được)
│   └── Không → Internal network
│
├── Multi-container trên cùng host?
│   ├── Cần communicate → User-defined bridge network
│   └── Production → Docker Compose network
│
├── Multi-host communication?
│   ├── Docker Swarm → Overlay network
│   ├── Kubernetes → Pod network
│   └── External services → Host network hoặc Port exposure
│
└── Cần expose port ra ngoài?
    ├── Local development → ports: - "8080:80"
    ├── Production → Reverse proxy, limited ports
    └── Database → Không expose, internal network only

NETWORK SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Single host, simple      → Default bridge                    │
│ Single host, multi-container → User-defined bridge           │
│ Swarm/Kubernetes        → Overlay network                   │
│ Performance critical     → Host network                       │
│ No networking needed     → None network                      │
└─────────────────────────────────────────────────────────────┘
```

## 5. Storage Decision Tree

```
Bạn cần chọn loại storage nào?
│
├── Data cần persist không?
│   ├── Có → Named volume
│   │   ├── Database data → Named volume
│   │   ├── User uploads → Named volume
│   │   └── Config files → Config file hoặc ConfigMap
│   │
│   └── Không → tmpfs hoặc không mount
│
├── Data cần share giữa containers?
│   ├── Có → Named volume
│   └── Không → Container-specific volume
│
├── Data sensitive?
│   ├── Có → tmpfs (memory-based)
│   └── Không → Regular volume
│
└── Cần access từ host?
    ├── Có → Bind mount
    └── Không → Named volume

STORAGE TYPE SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Database files         → Named volume                        │
│ User uploads           → Named volume + backup              │
│ Application logs       → Bind mount (host) hoặc logging driver │
│ Sensitive temp data    → tmpfs                              │
│ Config files           → Config file hoặc env vars           │
│ Source code (dev)      → Bind mount                          │
└─────────────────────────────────────────────────────────────┘
```

## 6. Security Configuration Decision Tree

```
Bạn cần apply security measures nào?
│
├── User permissions?
│   ├── Production → Non-root user (REQUIRED)
│   │   ├── addgroup/adduser
│   │   └── USER directive
│   │
│   └── Development → Root acceptable với warning
│
├── Capabilities?
│   ├── Default (NET_BIND_SERVICE) → Acceptable
│   ├── Need more → Add với cap_add
│   └── Don't need default → Drop ALL
│
├── Container capabilities best practice:
    cap_add:
      - NET_BIND_SERVICE
    cap_drop:
      - ALL
│
├── Filesystem?
│   ├── Production → Read-only rootfs
│   │   └── read_only: true
│   └── Dev → Writable (để develop)
│
└── Privileged mode?
    ├── NEVER in production!
    └── Development only if absolutely necessary
```

## 7. Resource Limits Decision Tree

```
Bạn nên set resource limits như thế nào?
│
├── Service type?
│   │
│   ├── API/Backend
│   │   ├── Limits: 1-2 CPU, 512MB-2GB RAM
│   │   └── CPU-bound hoặc Memory-bound?
│   │
│   ├── Database
│   │   ├── Limits: 2-4 CPU, 1GB-8GB RAM
│   │   └── Postgres: shared_buffers = 25% RAM
│   │
│   ├── Cache (Redis)
│   │   ├── Limits: 0.5-2 CPU, 256MB-1GB RAM
│   │   └── maxmemory based on container limit
│   │
│   ├── Worker
│   │   ├── Limits: 0.5-2 CPU, 256MB-1GB RAM
│   │   └── Scale horizontally, not vertically
│   │
│   └── nginx/proxy
│       ├── Limits: 0.25-1 CPU, 128-256MB RAM
│       └── CPU-bound
│
└── Memory swap?
    ├── Production → --memory-swap=-1 (unlimited swap)
    └── Memory-sensitive → --memory-swap=2x --memory
```

## 8. Health Check Decision Tree

```
Bạn nên implement health check như thế nào?
│
├── Application có HTTP endpoint?
│   ├── Có → HTTP health check
│   │   └── curl -f http://localhost:PORT/health
│   │
│   └── Không → Command-based check
│       ├── Database → pg_isready, mysqladmin ping
│       ├── Redis → redis-cli ping
│       └── Custom → Custom script
│
└── Health check best practices:
    - interval: 30s (not too frequent)
    - timeout: 10s (long enough to respond)
    - retries: 3 (allow some failures)
    - start_period: 30s (time to start up)

HEALTH CHECK TEMPLATE:
services:
  api:
    healthcheck:
      test: ["CMD", "command"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

## 9. Logging Configuration Decision Tree

```
Bạn nên configure logging như thế nào?
│
├── Log driver nào?
│   │
│   ├── Local development → json-file (default)
│   ├── Centralized logging → syslog, fluentd, gelf
│   ├── CloudWatch (AWS) → awslogs
│   ├── Splunk → splunk
│   └── Production → json-file với rotation
│
└── Log rotation configuration:
    - max-size: 100m
    - max-file: 3-5

LOGGING SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Local dev         → json-file (default)                    │
│ Docker Swarm      → json-file hoặc journald                │
│ Kubernetes        → json-file (để stdout)                  │
│ Centralized ELK   → json-file → Filebeat/Fluentd          │
│ Cloud-native      → CloudWatch/GCP Logging/Splunk          │
└─────────────────────────────────────────────────────────────┘
```

## 10. Compose File Structure Decision Tree

```
Bạn nên tổ chức docker-compose.yml như thế nào?
│
├── Cần environment nào?
│   ├── Development → docker-compose.override.yml
│   ├── Staging → docker-compose.staging.yml
│   └── Production → docker-compose.prod.yml
│
├── Base structure:
    version: '3.8'  # Hoặc version mới nhất supported
    
    services:
      app:
        build: .  # Development
        # image: registry/app:tag  # Production
    
    networks:
      default:
    
    volumes:
      data:
│
├── Production add:
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
```

## 11. Service Dependency Decision Tree

```
Làm thế nào để handle service dependencies?
│
├── depends_on đủ không?
│   ├── Development → Có, acceptable
│   └── Production → Cần thêm health checks
│
└── Production dependencies:
    version: '3.8'
    services:
      api:
        depends_on:
          db:
            condition: service_healthy
          redis:
            condition: service_healthy
        # Wait for services to be healthy, not just started
      
      db:
        healthcheck:
          test: ["CMD-SHELL", "pg_isready"]
          interval: 10s
          timeout: 5s
          retries: 5
          start_period: 30s
      
      redis:
        healthcheck:
          test: ["CMD", "redis-cli", "ping"]
```

## 12. Deployment Strategy Decision Tree

```
Bạn nên chọn deployment strategy nào?
│
├── Docker Compose (single host)?
│   ├── Development → docker-compose up -d
│   └── Simple staging → docker-compose pull && docker-compose up -d
│
├── Docker Swarm (multi-host)?
│   ├── docker stack deploy
│   ├── Rolling update: parallelism=1, delay=10s
│   └── Blue-green: service update với new version first
│
├── Kubernetes?
│   ├── RollingUpdate (default)
│   ├── Blue-Green: deployment với selector
│   └── Canary: multiple deployments, gradual traffic shift
│
└── Deployment validation:
    - Health checks pass?
    - Logs show no errors?
    - Smoke tests pass?
    - Rollback plan ready?
```

## 13. Quick Reference Decision Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUICK DECISION GUIDE                            │
├─────────────────────────────────┬──────────────────────────────────────┤
│ SITUATION                       │ DECISION                              │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Base image for API             │ node:18-alpine, python:3.11-slim      │
│ Base image for Go binary       │ scratch hoặc distroless               │
├─────────────────────────────────┼──────────────────────────────────────┤
│ User in container               │ Non-root user ALWAYS                  │
│ Capabilities                    │ cap_drop: ALL, cap_add: specific      │
│ Root filesystem                 │ read_only: true (production)          │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Network driver (single host)    │ bridge với user-defined network       │
│ Network driver (multi-host)     │ overlay (Swarm)                      │
│ Database access                 │ Internal network, no port exposure    │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Persistent data                 │ Named volume                          │
│ Development code                │ Bind mount                            │
│ Sensitive temp data             │ tmpfs                                 │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Health check (HTTP app)         │ curl -f http://localhost:PORT/health  │
│ Health check (database)         │ pg_isready, mysqladmin ping          │
│ Health check (redis)            │ redis-cli ping                       │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Secrets in compose              │ Docker secrets hoặc external store   │
│ Secrets in CI/CD                │ Environment variables từ vault       │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Image size critical?           │ Multi-stage build + alpine            │
│ Security critical?              │ Distroless + non-root + read-only    │
│ Development?                    │ Full image + bind mounts + hot reload │
└─────────────────────────────────┴──────────────────────────────────────┘
```

## Related Documents

- [Docker Glossary](../glossary.md)
- [Docker Architecture](../architecture.md)
- [Docker Best Practices](../best-practice.md)
- [Docker Anti-Patterns](../anti-pattern.md)
- [Docker Checklist](../checklist.md)
- [Docker FAQ](../faq.md)
