# Kubernetes Knowledge Base - Best Practices

## Tổng quan

Document này cung cấp 10+ best practices cho việc sử dụng Kubernetes trong Cursor Enterprise Framework, kèm theo code examples cụ thể cho từng practice.

## Practice 1: Always Set Resource Requests và Limits

### Mô tả

Luôn luôn set resource requests và limits cho containers để đảm bảo scheduling chính xác và ngăn chặn resource starvation.

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
          
          # Resource management - CRITICAL
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          
          # Proactive liveness check
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
            failureThreshold: 3
          
          # Ensure traffic only goes to ready pods
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3
            successThreshold: 1
```

### Tại sao quan trọng

- **Scheduling**: Kubernetes scheduler dựa vào requests để assign pods to nodes
- **QoS Classes**: Limits và requests xác định QoS class (Guaranteed, Burstable, BestEffort)
- **Resource protection**: Limits ngăn containers consume tất cả resources
- **Cost control**: Resource limits giúp predict costs

## Practice 2: Use Namespaces cho Logic Isolation

### Mô tả

Sử dụng namespaces để phân tách environments, teams, và applications. Namespaces cung cấp scope cho names, resource quotas, và network policies.

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: platform
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
    team: platform
---
apiVersion: v1
kind: Namespace
metadata:
  name: development
  labels:
    environment: development
    team: platform
```

```yaml
# Apply namespace to resources
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production  # Specify namespace
  labels:
    app: myapp
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

```bash
# Switch context to namespace
kubectl config set-context --current --namespace=production

# List resources in namespace
kubectl get pods -n production

# Get resources across all namespaces
kubectl get pods --all-namespaces
```

## Practice 3: Implement Health Checks Properly

### Mô tả

Health checks (liveness, readiness, startup probes) là critical cho self-healing và proper traffic routing.

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: api
          image: myapi:1.0.0
          
          # Startup probe - for slow starting apps
          startupProbe:
            httpGet:
              path: /startup
              port: 8080
            failureThreshold: 30  # 30 * 10s = 5 minutes max
            periodSeconds: 10
          
          # Liveness probe - is container alive?
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
            timeoutSeconds: 5
            failureThreshold: 3
          
          # Readiness probe - can receive traffic?
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 3
            failureThreshold: 3
            successThreshold: 1
```

```yaml
# For databases and services without HTTP
- name: postgres
  image: postgres:15-alpine
  readinessProbe:
    exec:
      command:
        - pg_isready
        - -U
        - postgres
        - -d
        - myapp
    initialDelaySeconds: 10
    periodSeconds: 10
  
  livenessProbe:
    exec:
      command:
        - pg_isready
        - -U
        - postgres
    initialDelaySeconds: 30
    periodSeconds: 20
```

## Practice 4: Use Labels và Selectors Effectively

### Mô tả

Labels và selectors là cách chính để group và select Kubernetes objects. Sử dụng consistent labeling scheme.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-api
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
      app.kubernetes.io/component: api
      app.kubernetes.io/version: "1.0.0"
      app.kubernetes.io/part-of: myapp-suite
      app.kubernetes.io/managed-by: flux
  template:
    metadata:
      labels:
        app.kubernetes.io/name: myapp
        app.kubernetes.io/component: api
        app.kubernetes.io/version: "1.0.0"
        app.kubernetes.io/part-of: myapp-suite
        app.kubernetes.io/managed-by: flux
    spec:
      containers:
        - name: api
          image: myapi:1.0.0
```

```yaml
# Service selector
apiVersion: v1
kind: Service
metadata:
  name: myapp-api
spec:
  selector:
    app.kubernetes.io/name: myapp
    app.kubernetes.io/component: api
  ports:
    - port: 80
      targetPort: 8080
```

```yaml
# PodDisruptionBudget using labels
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-api-pdb
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
      app.kubernetes.io/component: api
  minAvailable: 2
```

## Practice 5: Implement Pod Disruption Budgets

### Mô tả

PodDisruptionBudgets đảm bảo minimum number of pods available during voluntary disruptions (node drains, cluster upgrades).

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  # Option 1: Minimum number of pods available
  minAvailable: 2
  
  # Option 2: Maximum pods unavailable
  # maxUnavailable: 1
  
  selector:
    matchLabels:
      app: myapp
      tier: backend
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5
  selector:
    matchLabels:
      app: myapp
      tier: backend
  template:
    metadata:
      labels:
        app: myapp
        tier: backend
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
```

```bash
# Check if disruption is allowed
kubectl get pdb myapp-pdb

# Drain a node safely
kubectl drain node worker-node-1 --ignore-daemonsets --delete-emptydir-data

# See PDB status
kubectl describe pdb myapp-pdb
```

## Practice 6: Use Topology Spread Constraints for HA

### Mô tả

Topology spread constraints phân phối pods across failure domains (regions, zones, nodes) để đảm bảo high availability.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 6
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      topologySpreadConstraints:
        # Spread across zones
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: myapp
        
        # Spread across nodes
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: myapp
      
      containers:
        - name: myapp
          image: myapp:1.0.0
```

## Practice 7: Configure Security Context Appropriately

### Mô tả

Security contexts define privilege và access control settings cho pods và containers.

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      # Pod security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      
      containers:
        - name: myapp
          image: myapp:1.0.0
          
          # Container security context
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
          
          # Read-only root filesystem
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/cache
      
      # Use tmpfs for temporary data
      volumes:
        - name: tmp
          emptyDir:
            medium: Memory
            sizeLimit: 64Mi
        - name: cache
          emptyDir:
            medium: Memory
            sizeLimit: 128Mi
```

## Practice 8: Implement Resource Quotas và LimitRanges

### Mô tả

ResourceQuotas giới hạn total resource consumption trong một namespace, trong khi LimitRanges set default và maximum limits cho containers.

```yaml
# LimitRange - Set default limits for containers
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
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
        cpu: "2"
        memory: 1Gi
      min:
        cpu: 50m
        memory: 32Mi
      maxLimitRequestRatio:
        cpu: "4"
        memory: "4"
---
# ResourceQuota - Total namespace limits
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: production
spec:
  hard:
    requests.cpu: "20"
    requests.memory: "40Gi"
    limits.cpu: "40"
    limits.memory: "80Gi"
    pods: "50"
    services: "10"
    persistentvolumeclaims: "20"
```

## Practice 9: Use Services thay vì Pod IPs

### Mô tả

Pod IPs are ephemeral và thay đổi khi pods được recreate. Luôn sử dụng Services để reference other pods/services.

```yaml
# ❌ BAD: Hardcoded Pod IP
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: frontend
      env:
        - name: API_URL
          value: "http://10.244.1.5:8080"  # Will break!

# ✅ GOOD: Use Service DNS name
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: frontend
      env:
        - name: API_URL
          value: "http://api.default.svc.cluster.local:8080"
        # Or shorter:
        # value: "http://api:8080"
```

```yaml
# Service definition
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: default
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 8080
---
# Headless service for StatefulSet
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  clusterIP: None  # Headless
  selector:
    app: postgres
  ports:
    - port: 5432
```

## Practice 10: Implement Graceful Shutdown

### Mô tả

Applications cần handle SIGTERM gracefully để đảm bảo clean shutdown khi pods are terminated.

```typescript
// Node.js graceful shutdown example
const server = app.listen(PORT);

const gracefulShutdown = async (signal) => {
  console.log(`Received ${signal}, starting graceful shutdown...`);
  
  // Stop accepting new connections
  server.close(async () => {
    console.log('HTTP server closed');
    
    // Close database connections
    await db.end();
    
    // Close Redis
    await redis.quit();
    
    // Flush logs
    logger.flush();
    
    console.log('Graceful shutdown completed');
    process.exit(0);
  });
  
  // Force exit after timeout
  setTimeout(() => {
    console.error('Graceful shutdown timeout, forcing exit');
    process.exit(1);
  }, 30000);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

```yaml
# Pre-stop hook for slow shutdowns
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: myapp
      lifecycle:
        preStop:
          exec:
            command:
              - /bin/sh
              - -c
              - "sleep 10 && nginx -s quit"
      terminationGracePeriodSeconds: 60
```

## Practice 11: Use Init Containers Appropriately

### Mô tả

Init containers chạy trước main containers và thường được dùng cho setup tasks như waiting for dependencies, configuring, hoặc seeding data.

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      initContainers:
        # Wait for database to be ready
        - name: wait-for-db
          image: busybox:1.36
          command:
            - sh
            - -c
            - |
              echo "Waiting for database..."
              until nc -z postgres.database.svc.cluster.local 5432; do
                echo "Database not ready, waiting..."
                sleep 2
              done
              echo "Database is ready!"
        
        # Migrate database schema
        - name: db-migrate
          image: myapp:1.0.0
          command: ["node", "migrate.js"]
          env:
            - name: DATABASE_URL
              valueFrom:
                configMapKeyRef:
                  name: db-config
                  key: connection-string
        
        # Fetch configuration from remote
        - name: fetch-config
          image: curlimages/curl:latest
          command:
            - sh
            - -c
            - |
              curl -s http://config-server/api/config > /config/app.json
          volumeMounts:
            - name: config
              mountPath: /config
      
      containers:
        - name: myapp
          image: myapp:1.0.0
          volumeMounts:
            - name: config
              mountPath: /app/config
      
      volumes:
        - name: config
          emptyDir: {}
```

## Practice 12: Implement Proper Logging và Monitoring

### Mô tả

Structured logging và proper monitoring là essential cho debugging và maintaining production systems.

```yaml
# Pod with logging configuration
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:1.0.0
          
          # Log to stdout (not files)
          # Application should log to stdout/stderr
          
          env:
            # Structured logging
            - name: LOG_LEVEL
              value: "info"
            - name: LOG_FORMAT
              value: "json"
            
            # Add metadata to logs
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
```

```yaml
# Prometheus scrape configuration
apiVersion: v1
kind: Service
metadata:
  name: myapp-metrics
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: myapp
  ports:
    - name: http
      port: 8080
    - name: metrics
      port: 9090
```

## Related Documents

- [Kubernetes Glossary](../glossary.md)
- [Kubernetes Architecture](../architecture.md)
- [Kubernetes Anti-Patterns](../anti-pattern.md)
- [Kubernetes Checklist](../checklist.md)
- [Kubernetes FAQ](../faq.md)
- [Kubernetes Decision Tree](../decision-tree.md)
