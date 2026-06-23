# Docker Architecture - Kiến Trúc Docker

## Tổng quan

Docker là containerization platform cho phép đóng gói và chạy applications trong isolated containers.

## Kiến trúc chi tiết

### 1. Docker Architecture

- **Docker Daemon**: Background service
- **Docker Client**: CLI interface
- **Docker Registry**: Image storage

### 2. Dockerfile Best Practices

```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Kết luận

Docker architecture enables consistent deployments.
