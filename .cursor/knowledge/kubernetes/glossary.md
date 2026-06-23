# Kubernetes Knowledge Base - Glossary

## Tổng quan

Document này cung cấp danh sách các thuật ngữ chuyên ngành liên quan đến Kubernetes trong Cursor Enterprise Framework. Các thuật ngữ được phân loại theo từng nhóm để dễ tra cứu.

## Nhóm 1: Core Kubernetes Concepts

### 1. Kubernetes (K8s)

Nền tảng container orchestration mã nguồn mở giúp automate việc deploy, scale, và manage containerized applications. Kubernetes cung cấp cơ chế để define desired state cho applications và tự động reconcile actual state với desired state.

```yaml
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
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          ports:
            - containerPort: 8080
```

Kubernetes hoạt động như một container orchestration layer, abstracting underlying infrastructure và cung cấp unified API cho container management.

### 2. Pod

Đơn vị nhỏ nhất trong Kubernetes, đại diện cho một hoặc nhiều containers được deploy cùng nhau trên cùng một node. Pods share network namespace và có thể share volumes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
    - name: myapp
      image: myapp:1.0.0
      ports:
        - containerPort: 8080
      resources:
        requests:
          memory: "128Mi"
          cpu: "250m"
        limits:
          memory: "256Mi"
          cpu: "500m"
```

Pods có ephemeral lifecycle - chúng có thể be created, destroyed, và recreated. Đối với production, thường sử dụng Deployments để manage Pods.

### 3. Node

Worker machine trong Kubernetes cluster, có thể là physical server hoặc virtual machine. Mỗi node chứa Kubelet, container runtime (Docker/containerd), và Kube-proxy.

```bash
# Get node information
kubectl get nodes
kubectl describe node worker-node-1
kubectl top node worker-node-1
```

Node status bao gồm: Addresses, Conditions, Capacity, Info. Kubernetes automatically schedules Pods onto nodes dựa trên resource availability và constraints.

### 4. Cluster

Tập hợp các nodes được quản lý bởi Kubernetes control plane. Cluster bao gồm control plane components và worker nodes.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                    Control Plane                          │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │    │
│  │  │ kube-   │  │ kube-  │  │ kube-  │  │ etcd   │   │    │
│  │  │ apiserver│ │ sched- │  │ ctrl-  │  │         │   │    │
│  │  │         │  │ uler   │  │ mgr    │  │         │   │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                      Worker Nodes                          │    │
│  │  ┌───────────┐    ┌───────────┐    ┌───────────┐       │    │
│  │  │  Node 1   │    │  Node 2   │    │  Node 3   │       │    │
│  │  │ ┌───────┐│    │ ┌───────┐│    │ ┌───────┐│       │    │
│  │  │ │ Pod A ││    │ │ Pod B ││    │ │ Pod C ││       │    │
│  │  │ └───────┘│    │ └───────┘│    │ └───────┘│       │    │
│  │  └───────────┘    └───────────┘    └───────────┘       │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## Nhóm 2: Workload Resources

### 5. Deployment

Kubernetes resource quản lý ReplicaSets và cung cấp declarative updates cho Pods. Deployments enable rolling updates, rollbacks, và scaling.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
```

### 6. ReplicaSet

Đảm bảo một số lượng cố định của Pod replicas đang chạy tại bất kỳ thời điểm nào. Thông thường được quản lý bởi Deployment.

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
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
```

### 7. StatefulSet

Quản lý stateful applications với persistent storage và unique network identifiers. StatefulSets đảm bảo ordering và uniqueness.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: "postgres"
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:15-alpine
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

### 8. DaemonSet

Đảm bảo Pod chạy trên tất cả (hoặc một số) nodes trong cluster. Thường dùng cho logging agents, monitoring agents, và network plugins.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector
spec:
  selector:
    matchLabels:
      app: log-collector
  template:
    metadata:
      labels:
        app: log-collector
    spec:
      containers:
        - name: fluentd
          image: fluent/fluentd:v1.16
          resources:
            limits:
              memory: 200Mi
              cpu: 100m
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
```

### 9. Job và CronJob

Job tạo một hoặc nhiều Pods và đảm bảo chúng hoàn thành thành công. CronJob schedule Jobs theo cron expression.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-import
spec:
  backoffLimit: 4
  template:
    spec:
      containers:
        - name: importer
          image: myapp:1.0.0
          command: ["node", "import.js"]
      restartPolicy: OnFailure
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-report
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: reporter
              image: myapp:1.0.0
              command: ["node", "report.js"]
              env:
                - name: REPORT_DATE
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.labels['date']
          restartPolicy: OnFailure
```

## Nhóm 3: Networking

### 10. Service

Abstraction định nghĩa logical set of Pods và policy để truy cập chúng. Services enable load balancing và service discovery.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
# LoadBalancer service for external access
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

Service types: ClusterIP, NodePort, LoadBalancer, ExternalName, ExternalLB.

### 11. Ingress

Quản lý external access đến services trong cluster, thường cung cấp HTTP/HTTPS routing và load balancing.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8080
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

### 12. NetworkPolicy

Xác định rules cho phép hoặc từ chối traffic giữa pods và/hoặc namespaces.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
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
```

## Nhóm 4: Configuration và Secrets

### 13. ConfigMap

Kubernetes object lưu trữ non-sensitive configuration data dưới dạng key-value pairs. ConfigMaps có thể be consumed by pods as environment variables, command-line arguments, hoặc config files.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "postgres.database.svc.cluster.local"
  LOG_LEVEL: "info"
  config.json: |
    {
      "feature_flags": {
        "new_ui": true,
        "beta_api": false
      }
    }
```

### 14. Secret

Kubernetes object lưu trữ sensitive data như passwords, OAuth tokens, và SSH keys. Secrets có thể be consumed by pods similarly to ConfigMaps.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DATABASE_PASSWORD: "supersecretpassword"
  API_KEY: "sk_live_abc123"
---
# Using TLS secret
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: base64-encoded-cert
  tls.key: base64-encoded-key
```

## Nhóm 5: Storage

### 15. PersistentVolume (PV)

Piece of storage trong cluster đã được provisioned hoặc claimed. PVs có lifecycle độc lập với individual pods.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-fast
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: fast
  hostPath:
    path: /data/pv-fast
---
# AWS EBS PersistentVolume
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-aws
spec:
  capacity:
    storage: 50Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: ebs-sc
  awsElasticBlockStore:
    volumeID: vol-0a1b2c3d4e5f
    fsType: ext4
```

### 16. PersistentVolumeClaim (PVC)

Yêu cầu storage từ user. PVCs consume PV resources giống như pods consume node resources.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast
  selector:
    matchLabels:
      type: fast-storage
```

### 17. StorageClass

Cung cấp cách describe "classes" của storage. StorageClasses enable dynamic provisioning của PersistentVolumes.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: regional-pd
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

## Nhóm 6: Security

### 18. RBAC (Role-Based Access Control)

Cơ chế kiểm soát quyền truy cập vào Kubernetes resources dựa trên roles và role bindings.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "watch", "list"]
  - apiGroups: [""]
    resources: ["pods/log"]
    verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: default
subjects:
  - kind: ServiceAccount
    name: default
    namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### 19. ServiceAccount

Identity cho processes running in pods để authenticate với Kubernetes API server.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: production
automountServiceAccountToken: false
---
# Pod using specific ServiceAccount
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: myapp-sa
  containers:
    - name: myapp
      image: myapp:1.0.0
```

### 20. PodSecurityPolicy (Deprecated)

Deprecated mechanism để control security-sensitive aspects of pod specification. Đã được thay thế bởi Pod Security Standards (PSS) và OPA/Gatekeeper.

## Nhóm 7: Observability

### 21. Liveness Probe

Kiểm tra xem container còn alive không. Nếu probe fails, kubelet sẽ kill container và restart.

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 15
  timeoutSeconds: 5
  failureThreshold: 3
```

### 22. Readiness Probe

Kiểm tra xem container có ready để accept traffic không. Container chỉ nhận traffic khi readiness probe succeeds.

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  successThreshold: 1
  failureThreshold: 3
```

### 23. ResourceQuota

Giới hạn tổng resource consumption trong một namespace.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "20"
```

### 24. LimitRange

Đặt default, min, và max resource limits cho containers trong một namespace.

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: compute-limits
spec:
  limits:
    - type: Container
      max:
        cpu: "2"
        memory: 1Gi
      min:
        cpu: 100m
        memory: 64Mi
      default:
        cpu: 500m
        memory: 256Mi
      defaultRequest:
        cpu: 200m
        memory: 128Mi
```

## Related Documents

- [Kubernetes Architecture](../architecture.md)
- [Kubernetes Best Practices](../best-practice.md)
- [Kubernetes Anti-Patterns](../anti-pattern.md)
- [Kubernetes Checklist](../checklist.md)
- [Kubernetes FAQ](../faq.md)
- [Kubernetes Decision Tree](../decision-tree.md)
