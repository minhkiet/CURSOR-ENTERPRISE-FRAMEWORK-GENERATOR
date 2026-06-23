# Kubernetes Glossary - Từ Điển Thuật Ngữ Kubernetes

## Giới thiệu

Tài liệu này cung cấp các thuật ngữ chuyên ngành Kubernetes container orchestration.

## Các thuật ngữ cơ bản

### 1. Pod

Pod là smallest deployable unit. Contains one or more containers. Shared network, storage.

### 2. Node

Node là worker machine in cluster. Virtual or physical. Contains Kubelet, container runtime.

### 3. Cluster

Cluster là set of nodes. Control plane manages nodes. High availability.

### 4. Deployment

Deployment manages Pod replicas. Declarative updates. Rollback support.

### 5. Service

Service là abstract way to expose application. Load balancing. ClusterIP, NodePort, LoadBalancer.

### 6. ReplicaSet

ReplicaSet ensures specified number of pods running. Used by Deployments.

### 7. Ingress

Ingress manages external access to services. HTTP/HTTPS routing. TLS termination.

### 8. ConfigMap

ConfigMap stores non-sensitive configuration. Environment variables, files.

### 9. Secret

Secret stores sensitive data. Encoded, base64. TLS certificates, passwords.

### 10. PersistentVolume

PersistentVolume provides durable storage. Survives pod restarts. NFS, cloud storage.

### 11. Namespace

Namespace provides resource isolation. Virtual cluster. Default, kube-system.

### 12. Helm

Helm là package manager for Kubernetes. Charts, templates, releases.

### 13. kubectl

kubectl là command-line tool for Kubernetes. Cluster management, deployments.

## Kết luận

Kubernetes Glossary cung cấp nền tảng về container orchestration.
