# Kubernetes Knowledge Base - Anti-Patterns

## Tổng quan

Document nôi liệt kê các anti-patterns phổ biến khi sử dụng Kubernetes và đề xuất giải pháp thay thế. Mỗi anti-pattern được mô tả chi tiết với ví dụ về cách phát hiện và khắc phục.

## Anti-Pattern 1: Not Setting Resource Limits

### Mô tả

Không set resource limits khiến containers có thể consume tất cả available resources, gây ảnh hưởng đến other pods và có thể crash nodes.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No resource limits
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          ports:
            - containerPort: 8080
          # No resources specified - pod gets BestEffort QoS
```

```bash
# Check current resource usage
kubectl top pods

# Pods without limits might get OOMKilled or throttle
```

### Giải pháp

```yaml
# ✅ SOLUTION: Set both requests and limits
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
```

```yaml
# ✅ BETTER: Use LimitRange for defaults
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
spec:
  limits:
    - type: Container
      default:
        cpu: 500m
        memory: 256Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      max:
        cpu: "4"
        memory: 2Gi
```

## Anti-Pattern 2: Not Using Health Checks

### Mô tả

Pod không có health checks sẽ không được restart khi fail và có thể nhận traffic khi not ready.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No health checks
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          # No livenessProbe - won't restart if stuck
          # No readinessProbe - will receive traffic immediately
```

### Giải pháp

```yaml
# ✅ SOLUTION: Comprehensive health checks
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          
          # Startup probe for slow starting apps
          startupProbe:
            httpGet:
              path: /startup
              port: 8080
            failureThreshold: 30
            periodSeconds: 10
          
          # Liveness probe - is container alive?
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
            failureThreshold: 3
          
          # Readiness probe - can receive traffic?
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3
```

## Anti-Pattern 3: Using Latest Tag

### Mô tả

Sử dụng `:latest` tag không deterministic - image được pull mỗi lần có thể khác nhau, gây khó khăn cho debugging và reproducibility.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Using latest tag
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myregistry.io/myapp:latest
          # Could be different image each deploy!
```

### Giải pháp

```yaml
# ✅ SOLUTION: Use specific tags or digests
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          # Specific version tag
          image: myregistry.io/myapp:1.2.3
          
          # Or use image digest (immutable)
          # image: myregistry.io/myapp@sha256:a1b2c3...
```

```yaml
# ✅ BETTER: Use imagePullPolicy
spec:
  containers:
    - name: myapp
      image: myregistry.io/myapp:1.2.3
      imagePullPolicy: IfNotPresent
      # Or Always for :latest tags
```

## Anti-Pattern 4: Running as Root

### Mô tả

Container chạy với root user là security risk nghiêm trọng. Nếu container escape, attacker có root access trên host.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Running as root
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      securityContext:
        runAsUser: 0  # Root!
      containers:
        - name: myapp
          image: myapp:1.0.0
          # Container runs as root
```

### Giải pháp

```yaml
# ✅ SOLUTION: Run as non-root with security context
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
      
      containers:
        - name: myapp
          image: myapp:1.0.0
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
```

```dockerfile
# Create non-root user in Dockerfile
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -D appuser
USER appuser
```

## Anti-Pattern 5: Hardcoding Secrets in Config

### Mô tả

Lưu trữ secrets trực tiếp trong configuration files hoặc environment variables không mã hóa.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Secrets in plain text
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  # base64 encoded but not encrypted!
  DB_PASSWORD: c3VwZXJzZWNyZXQ=
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          env:
            - name: DB_PASSWORD
              value: "super_secret_password"  # In plain text!
```

### Giải pháp

```yaml
# ✅ SOLUTION: Use Kubernetes Secrets properly
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DB_PASSWORD: "super_secret_password"
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: DB_PASSWORD
```

```yaml
# ✅ BETTER: Use external secrets management
# HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: app-secrets
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: secret/myapp/db-password
```

## Anti-Pattern 6: No Pod Disruption Budget

### Mô tả

Không có PDB khi performing node drains hoặc updates có thể gây downtime nếu too many pods bị terminate cùng lúc.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No PDB for critical deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 2  # Only 2 pods, could lose both during drain!
```

### Giải pháp

```yaml
# ✅ SOLUTION: Add PodDisruptionBudget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 1  # At least 1 pod must be available
  selector:
    matchLabels:
      app: myapp
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3  # 3 replicas, PDB ensures at least 1 available
```

## Anti-Pattern 7: Not Using Namespaces

### Mô tả

Deploying all resources vào default namespace gây khó khăn cho management, quotas, và isolation.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: Everything in default namespace
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend  # Mixed with other apps
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend   # Mixed with other apps
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database  # Mixed with other apps
```

### Giải pháp

```yaml
# ✅ SOLUTION: Use namespaces for isolation
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
---
# Resources now organized
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: production
```

```yaml
# ✅ BETTER: Add quotas per namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "20"
    requests.memory: "40Gi"
    pods: "50"
```

## Anti-Pattern 8: Not Implementing Graceful Shutdown

### Mô tả

Application không handle SIGTERM, dẫn đến interrupted requests và potential data loss khi pods bị terminate.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No graceful shutdown handling
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          # SIGTERM received but not handled
          # In-flight requests interrupted
          # Database connections not closed
```

### Giải pháp

```typescript
// ✅ SOLUTION: Handle SIGTERM in application
// Node.js example
const server = app.listen(PORT);

process.on('SIGTERM', async () => {
  console.log('SIGTERM received, starting graceful shutdown');
  
  server.close(async () => {
    // Close connections
    await db.end();
    await redis.quit();
    await closeFileHandles();
    
    console.log('Graceful shutdown completed');
    process.exit(0);
  });
  
  // Force exit after timeout
  setTimeout(() => {
    console.error('Shutdown timeout, forcing exit');
    process.exit(1);
  }, 30000);
});
```

```yaml
# ✅ SOLUTION: Configure terminationGracePeriodSeconds
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: myapp
          image: myapp:1.0.0
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 10"]
```

## Anti-Pattern 9: Using hostPath Without Restrictions

### Mô tả

hostPath volumes cho phép containers access filesystem của host, có thể là security risk nếu không được restrict đúng.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: hostPath without restrictions
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          volumeMounts:
            - name: hostfs
              mountPath: /host
      volumes:
        - name: hostfs
          hostPath:
            path: /  # Access entire host filesystem!
            type: Directory
```

### Giải pháp

```yaml
# ✅ SOLUTION: Use cluster storage instead of hostPath
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          volumeMounts:
            - name: data
              mountPath: /data
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: myapp-data

# ✅ IF hostPath is necessary, restrict carefully
apiVersion: apps/v1
kind: Pod
spec:
  containers:
    - name: myapp
      volumeMounts:
        - name: logs
          mountPath: /var/log/myapp
  volumes:
    - name: logs
      hostPath:
        path: /var/log/myapp  # Specific, restricted path
        type: DirectoryOrCreate
```

## Anti-Pattern 10: Not Setting Image Pull Policy

### Mô tả

Không set imagePullPolicy có thể dẫn đến unexpected behavior với image caching và updates.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No imagePullPolicy
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          # Default: Always pull if tag is :latest
          # Default: IfNotPresent for other tags
          # May not pull new image when expected
```

### Giải phól

```yaml
# ✅ SOLUTION: Explicit imagePullPolicy
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          imagePullPolicy: Always  # Always pull, good for :latest
          
        - name: stable-service
          image: myservice:1.2.3
          imagePullPolicy: IfNotPresent  # Only pull if not cached
          
        - name: immutable-service
          image: myservice@sha256:abc123
          imagePullPolicy: Never  # Never pull, must exist locally
```

## Anti-Pattern 11: No LimitRange, Unlimited Namespaces

### Mô tả

Namespace không có LimitRange cho phép containers consume unlimited resources, có thể affect other workloads.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No resource constraints
# Namespace with no LimitRange or ResourceQuota
apiVersion: v1
kind: Namespace
metadata:
  name: production
# Someone could deploy a pod requesting 100 CPUs!
```

### Giải pháp

```yaml
# ✅ SOLUTION: LimitRange for container defaults
apiVersion: v1
kind: LimitRange
metadata:
  name: compute-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:
        cpu: 500m
        memory: 256Mi
      defaultRequest:
        cpu: 100m
        memory: 64Mi
      max:
        cpu: "8"
        memory: 8Gi
      min:
        cpu: 50m
        memory: 32Mi
---
# ✅ SOLUTION: ResourceQuota for namespace totals
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "40"
    requests.memory: "80Gi"
    limits.cpu: "80"
    limits.memory: "160Gi"
    pods: "100"
```

## Anti-Pattern 12: Not Using PodAntiAffinity

### Mô tả

Multiple replicas của same application có thể be scheduled on same node, gây downtime khi node fails.

### Ví dụ xấu

```yaml
# ❌ ANTI-PATTERN: No anti-affinity, replicas might cluster
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3  # All 3 could be on same node!
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
```

### Giải pháp

```yaml
# ✅ SOLUTION: PodAntiAffinity for HA
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    spec:
      affinity:
        podAntiAffinity:
          # Prefer not to co-locate pods
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: myapp
                topologyKey: kubernetes.io/hostname
        
        # OR require distribution (hard constraint)
        # requiredDuringSchedulingIgnoredDuringExecution:
        #   - labelSelector:
        #       matchLabels:
        #         app: myapp
        #     topologyKey: kubernetes.io/hostname
      
      containers:
        - name: myapp
          image: myapp:1.0.0
```

## Related Documents

- [Kubernetes Glossary](../glossary.md)
- [Kubernetes Architecture](../architecture.md)
- [Kubernetes Best Practices](../best-practice.md)
- [Kubernetes Checklist](../checklist.md)
- [Kubernetes FAQ](../faq.md)
- [Kubernetes Decision Tree](../decision-tree.md)
