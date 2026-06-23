# Docker Glossary - Từ Điển Thuật Ngữ Docker

## Giới thiệu

Tài liệu này cung cấp các thuật ngữ chuyên ngành Docker containerization.

## Các thuật ngữ cơ bản

### 1. Container

Container là lightweight, standalone executable package chứa everything needed to run software. Isolated from other containers và host system.

### 2. Image

Image là read-only template để create containers. Built from Dockerfile. Layers-based.

### 3. Dockerfile

Dockerfile là script chứa instructions để build image. FROM, RUN, COPY, EXPOSE, CMD commands.

### 4. Docker Hub

Docker Hub là cloud-based registry cho Docker images. Public và private repositories.

### 5. Docker Compose

Docker Compose là tool định nghĩa và run multi-container applications. YAML configuration.

### 6. Volume

Volume là persistent data storage. Survives container restarts. Mount host directories.

### 7. Network

Docker networking cho phép containers communicate. Bridge, host, overlay networks.

### 8. Registry

Registry là storage và distribution system cho images. Docker Hub, ECR, GCR, private registries.

### 9. Layer

Layer là intermediate image state. Cached for faster builds. Shared between images.

### 10. Multi-stage Build

Multi-stage builds sử dụng multiple FROM statements. Reduce final image size.

### 11. Port Mapping

Port mapping exposes container ports to host. -p flag: host:container.

### 12. Environment Variables

ENV instructions set environment variables. -e flag for runtime. Secrets management.

## Kết luận

Docker Glossary cung cấp nền tảng về containerization.
