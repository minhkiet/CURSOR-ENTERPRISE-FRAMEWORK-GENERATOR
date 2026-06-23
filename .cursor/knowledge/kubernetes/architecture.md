# Kubernetes Knowledge Base - Architecture

## Tổng quan

Document này mô tả chi tiết kiến trúc hệ thống Kubernetes trong Cursor Enterprise Framework, bao gồm các components, interactions, và design patterns cho production-ready deployments.

## 1. Kubernetes Architecture Overview

### 1.1 Control Plane Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Control Plane (Master)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                     kube-apiserver                          │ │
│  │  - REST API for all operations                              │ │
│  │  - Authentication & Authorization                           │ │
│  │  - Validates and configures data                            │ │
│  │  - Only component that talks to etcd                        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                           │                                       │
│  ┌──────────────┐  ┌──────┴──────┐  ┌──────────────┐           │
│  │ kube-        │  │   etcd      │  │ kube-        │           │
│  │ scheduler    │  │             │  │ controller   │           │
│  │              │  │ - Stores    │  │ manager      │           │
│  │ - Assigns    │  │   cluster   │  │              │           │
│  │   Pods to    │  │   state     │  │ - Node       │           │
│  │   Nodes      │  │ - Config    │  │   controller │           │
│  │ - Resource   │  │             │  │ - Replica    │           │
│  │   constraints│  │             │  │   controller │           │
│  │ - Affinity   │  │             │  │ - Endpoint   │           │
│  │   rules      │  │             │  │   controller │           │
│  └──────────────┘  └────────────┘  └──────────────┘           │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Node Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         Worker Node                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                        kubelet                              │ │
│  │  - Agent on each node                                       │ │
│  │  - Ensures containers are running                            │ │
│  │  - Mounts volumes, secrets                                  │ │
│  │  - Reports node/pod status                                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                      kube-proxy                             │ │
│  │  - Network proxy on each node                               │ │
│  │  - Maintains network rules                                 │ │
│  │  - Enables Service communication                            │ │
│  │  - Handles packet forwarding                                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                   Container Runtime                         │ │
│  │  - docker, containerd, CRI-O                               │ │
│  │  - Pulls images                                            │ │
│  │  - Creates containers                                      │ │
│  │  - Manages container lifecycle                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │   Pod   │  │   Pod   │  │   Pod   │  │   Pod   │           │
│  │    A    │  │    B    │  │    C    │  │    D    │           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## 2. Workload Architecture

### 2.1 Deployment Strategy

```yaml
# Rolling Update Strategy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Allow 1 extra pod during update
      maxUnavailable: 0   # Keep all pods available
  minReadySeconds: 30    # Wait 30s before pod is ready
  progressDeadlineSeconds: 600
```

```
Rolling Update Flow:
┌─────────────────────────────────────────────────────────────────┐
│                                                                     │
│  Initial:  [A-1.0] [A-1.0] [A-1.0] [A-1.0]                       │
│                  │                                                  │
│                  ▼                                                  │
│  Step 1:  [A-1.0] [A-1.0] [A-1.0] [A-1.0] [A-NEW] (maxSurge)    │
│                  │                                                  │
│                  ▼                                                  │
│  Step 2:  [A-1.0] [A-1.0] [A-1.0] [A-NEW] [A-NEW]                │
│                  │                                                  │
│                  ▼                                                  │
│  Step 3:  [A-1.0] [A-1.0] [A-NEW] [A-NEW] [A-NEW]                │
│                  │                                                  │
│                  ▼                                                  │
│  Final:   [A-NEW] [A-NEW] [A-NEW] [A-NEW]                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 ReplicaSet Controller

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-replicaset
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: v1
  template:
    # Pod template...
```

### 2.3 StatefulSet Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   StatefulSet Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Service: postgres-headless                                       │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │  pod-suffix-0  pod-suffix-1  pod-suffix-2               │     │
│  │  [postgres-0]  [postgres-1]  [postgres-2]              │     │
│  │       │             │             │                        │     │
│  │       └─────────────┴─────────────┘                        │     │
│  │                      │                                     │     │
│  │              stable network identity                       │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                     │
│  Volume Claims:                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │ data-pvc-0 │  │ data-pvc-1 │  │ data-pvc-2 │               │
│  │ (10Gi SSD) │  │ (10Gi SSD) │  │ (10Gi SSD) │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
│                                                                     │
│  Properties:                                                       │
│  - Stable, unique network identifiers                             │
│  - Stable, persistent storage                                       │
│  - Ordered deployment/scaling                                      │
│  - Ordered, graceful deletion                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Service Architecture

### 3.1 Service Types

```
┌─────────────────────────────────────────────────────────────────┐
│                     Service Types                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ClusterIP (default): Internal cluster access                     │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │  Pod A ──┐                                               │      │
│  │  Pod B ──┼──► [Service:10.96.x.x] ◄── Service IP       │      │
│  │  Pod C ──┘          │                                    │      │
│  │                 [Target Pods]                             │      │
│  └─────────────────────────────────────────────────────────┘      │
│                                                                     │
│  NodePort: Expose service on each node's IP                        │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │  Node:30000 ◄── External Traffic                         │      │
│  │      │                                                  │      │
│  │      └──► [Service] ──► [Target Pods]                  │      │
│  └─────────────────────────────────────────────────────────┘      │
│                                                                     │
│  LoadBalancer: Cloud provider load balancer                        │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │  [Cloud LB] ──► [Service] ──► [Target Pods]            │      │
│  └─────────────────────────────────────────────────────────┘      │
│                                                                     │
│  ExternalName: CNAME mapping                                       │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │  Service: myapp ◄── myapp.example.com (CNAME)           │      │
│  └─────────────────────────────────────────────────────────┘      │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Ingress Architecture

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-service-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls-secret
    - hosts:
        - app.example.com
      secretName: app-tls-secret
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: api-v1
                port:
                  number: 8080
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: api-v2
                port:
                  number: 8080
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80
```

## 4. Network Architecture

### 4.1 Pod Networking Model

```
┌─────────────────────────────────────────────────────────────────┐
│                   Pod Network Model                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Node 1 (10.0.1.x)                                               │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Pod A (10.1.1.10)                                        │     │
│  │  ┌─────────────┐                                           │     │
│  │  │ eth0 ◄─────┼──────► eth0 (Node)                         │     │
│  │  └─────────────┘        │                                  │     │
│  │                    veth pair                               │     │
│  │                         │                                  │     │
│  │  ┌─────────────┐        │                                  │     │
│  │  │ container   │◄───────┘                                  │     │
│  │  │ networking  │                                           │     │
│  │  └─────────────┘                                           │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                     │
│  Pod-to-Pod Communication:                                        │
│  - Same Node: veth pair → bridge → veth pair                      │
│  - Cross Node: veth → bridge → CNI → Node NIC → Network           │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Network Policy Example

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
      tier: backend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: production
          podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
    - from:
        - podSelector:
            matchLabels:
              app: monitoring
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: cache
      ports:
        - protocol: TCP
          port: 6379
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: TCP
          port: 53
        - protocol: UDP
          port: 53
```

## 5. Storage Architecture

### 5.1 Volume Types

```
┌─────────────────────────────────────────────────────────────────┐
│                   Volume Architecture                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  emptyDir   │  │  hostPath   │  │  persistent │              │
│  │             │  │             │  │   Volume    │              │
│  │ Ephemeral   │  │ Host FS     │  │   Claim     │              │
│  │ Pod lifetime│  │ Node-level  │  │  Cluster    │              │
│  │             │  │             │  │   storage   │              │
│  │ [Pod A]     │  │ /data/      │  │             │              │
│  │ [Pod B]     │  │ [Node FS]   │  │ [PVC]       │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  configMap  │  │   secret    │  │  downwardAPI │              │
│  │             │  │             │  │             │              │
│  │ Config data │  │ Sensitive   │  │ Pod metadata│              │
│  │ as files    │  │ data        │  │ as files    │              │
│  │             │  │             │  │             │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 PersistentVolume Provisioning

```yaml
# Static Provisioning
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-fast
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: fast
  gcePersistentDisk:
    pdName: my-disk
    fsType: ext4
---
# Dynamic Provisioning
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: regional-pd
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Retain
---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast
  resources:
    requests:
      storage: 20Gi
```

## 6. Security Architecture

### 6.1 RBAC Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       RBAC Architecture                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Subject (Who)           Role (What)         Resource (Where)    │
│  ─────────────────────────────────────────────────────────────  │
│  User: admin            ClusterRole          pods, services       │
│  Group: developers      Role                 pods, configmaps     │
│  ServiceAccount: app    ClusterRoleBinding   cluster-wide        │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Role/ClusterRole                                          │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │ rules:                                               │  │  │
│  │  │   - apiGroups: [""]                                  │  │  │
│  │  │     resources: ["pods", "services"]                  │  │  │
│  │  │     verbs: ["get", "list", "watch"]                  │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                           │                                       │
│                           ▼                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  RoleBinding/ClusterRoleBinding                            │  │
│  │  subjects:                                                │  │
│  │    - kind: User                                           │  │
│  │      name: john@example.com                               │  │
│  │  roleRef:                                                 │  │
│  │    kind: Role                                             │  │
│  │    name: pod-reader                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Pod Security Standards

```yaml
# Privileged Policy (ClusterAdmin)
apiVersion: v1
kind: Namespace
metadata:
  name: privileged
  labels:
    pod-security.kubernetes.io/enforce: privileged

# Baseline Policy (Default)
apiVersion: v1
kind: Namespace
metadata:
  name: baseline
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/enforce-version: latest

# Restricted Policy (Hardened)
apiVersion: v1
kind: Namespace
metadata:
  name: restricted
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: latest
```

## 7. Observability Architecture

### 7.1 Monitoring Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                   Monitoring Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │              Metrics Collection Layer                     │      │
│  │                                                         │      │
│  │  [Prometheus] ◄── [node-exporter]                      │      │
│  │       │             [kube-state-metrics]                │      │
│  │       │             [cAdvisor]                         │      │
│  │       │             [Custom Metrics]                   │      │
│  └───────┼─────────────────────────────────────────────────┘      │
│          │                                                      │
│          ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                    Storage Layer                          │     │
│  │                                                         │     │
│  │  [Thanos/S3] ◄── [Prometheus TSDB]                     │     │
│  │                       │                                 │     │
│  └───────────────────────┼─────────────────────────────────┘     │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                   Visualization Layer                      │     │
│  │                                                         │     │
│  │  [Grafana] ◄── Metrics Dashboard                        │     │
│  │                                                         │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Logging Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Logging Architecture                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Application Logs                                                 │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  [Pod A]  ──► stdout/stderr ──► Container Runtime      │     │
│  │  [Pod B]  ──► stdout/stderr ──► Container Runtime      │     │
│  └─────────────────────────────────────────────────────────┘     │
│                           │                                       │
│                           ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │              Log Collection Layer                         │     │
│  │                                                         │     │
│  │  [Fluent Bit] ◄── Node logs                            │     │
│  │       │            [Pod logs]                           │     │
│  │       │            [Audit logs]                        │     │
│  └───────┼─────────────────────────────────────────────────┘     │
│          │                                                       │
│          ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                    Storage Layer                         │     │
│  │                                                         │     │
│  │  [Elasticsearch / OpenSearch] ◄── Indexed logs         │     │
│  │                    │                                     │     │
│  │  [Loki / S3] ◄─────┴────── Raw logs                    │     │
│  └─────────────────────────────────────────────────────────┘     │
│                           │                                       │
│                           ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                  Visualization Layer                     │     │
│  │                                                         │     │
│  │  [Kibana / Grafana] ◄── Query & Visualize              │     │
│  │                                                         │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 8. High Availability Architecture

### 8.1 Multi-Region Deployment

```yaml
# Federation-style deployment across regions
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    topology.kubernetes.io/region: eastus
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/region
      whenUnsatisfiable: DoNotSchedule
      labelSelector:
        matchLabels:
          app: myapp
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: ScheduleAnyway
      labelSelector:
        matchLabels:
          app: myapp
```

### 8.2 Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2  # At least 2 pods must be available
  # OR
  # maxUnavailable: 1  # At most 1 pod can be unavailable
  selector:
    matchLabels:
      app: myapp
```

## Related Documents

- [Kubernetes Glossary](../glossary.md)
- [Kubernetes Best Practices](../best-practice.md)
- [Kubernetes Anti-Patterns](../anti-pattern.md)
- [Kubernetes Checklist](../checklist.md)
- [Kubernetes FAQ](../faq.md)
- [Kubernetes Decision Tree](../decision-tree.md)
