# Kubernetes Architecture - Kiến Trúc Kubernetes

## Tổng quan

Kubernetes là container orchestration platform cho phép deploy, scale, manage containerized applications.

## Kiến trúc chi tiết

### 1. Components

- **Control Plane**: API Server, etcd, Controller Manager, Scheduler
- **Worker Nodes**: Kubelet, Container Runtime, Kube Proxy

### 2. Resources

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: myapp:latest
        ports:
        - containerPort: 80
```

## Kết luận

Kubernetes architecture enables scalable, reliable deployments.
