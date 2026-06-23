# Kubernetes Knowledge Base - FAQ

## Tổng quan

Document này cung cấp 10 câu hỏi thường gặp và câu trả lời chi tiết về Kubernetes trong Cursor Enterprise Framework.

## Câu hỏi 1: Làm thế nào để handle graceful shutdown trong Kubernetes?

### Câu trả lời

Graceful shutdown trong Kubernetes đòi hỏi coordination giữa Kubernetes lifecycle và application code:

```yaml
# 1. Configure terminationGracePeriodSeconds
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60  # Give app time to shutdown
      
      containers:
        - name: myapp
          image: myapp:1.0.0
          
          # 2. PreStop hook for external setup
          lifecycle:
            preStop:
              exec:
                command:
                  - /bin/sh
                  - -c
                  - "sleep 5 && nginx -s quit"  # Let LB update
      
          # 3. Handle SIGTERM in application
```

```typescript
// Application graceful shutdown (Node.js example)
const server = app.listen(PORT);

async function gracefulShutdown(signal) {
  console.log(`${signal} received, starting graceful shutdown`);
  
  // 1. Stop accepting new connections
  server.close(async () => {
    console.log('HTTP server closed');
    
    // 2. Complete in-flight requests (with timeout)
    await waitForRequestsToComplete(25000);
    
    // 3. Close database connections
    await db.end();
    console.log('Database connections closed');
    
    // 4. Close Redis connections
    await redis.quit();
    console.log('Redis connections closed');
    
    // 5. Flush logs
    await logger.flush();
    
    console.log('Graceful shutdown completed');
    process.exit(0);
  });
  
  // 6. Force exit after grace period
  setTimeout(() => {
    console.error('Graceful shutdown timeout, forcing exit');
    process.exit(1);
  }, 55000);  // Less than terminationGracePeriodSeconds
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
```

```yaml
# Service with rolling update to minimize disruption
apiVersion: apps/v1
kind: Deployment
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # No downtime
  minReadySeconds: 30
```

## Câu hỏi 2: Sự khác biệt giữa liveness, readiness, và startup probes là gì?

### Câu trả lời

```yaml
# Startup Probe - For slow starting applications
# Disables liveness and readiness checks until it succeeds
startupProbe:
  httpGet:
    path: /startup
    port: 8080
  failureThreshold: 30      # 30 * 10s = 5 minutes max startup
  periodSeconds: 10
  successThreshold: 1

# Liveness Probe - Is the container alive?
# If this fails, kubelet kills and restarts the container
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 15   # Wait for app to initialize
  periodSeconds: 20          # Check every 20 seconds
  timeoutSeconds: 5          # Timeout after 5 seconds
  failureThreshold: 3        # 3 failures = restart

# Readiness Probe - Can the container receive traffic?
# If this fails, remove from Service endpoints
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3
  successThreshold: 1         # Only 1 success to be ready
```

| Probe Type | Purpose | Failure Action | When to Use |
|------------|---------|----------------|-------------|
| startupProbe | Wait for app to start | None (delays other probes) | Slow starting apps, DB migrations |
| livenessProbe | Detect hung/dead processes | Restart container | Apps that can crash safely |
| readinessProbe | Detect not ready to serve | Remove from Service | Apps that need warming, dependencies |

## Câu hỏi 3: Làm thế nào để configure high availability với multiple replicas?

### Câu trả lời

```yaml
# Deployment với HA configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5  # More replicas = higher availability
  
  selector:
    matchLabels:
      app: myapp
  
  # Anti-affinity to spread across nodes
  template:
    spec:
      affinity:
        # Prefer to spread across nodes
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: myapp
                topologyKey: kubernetes.io/hostname
        
        # Spread across zones (required)
        topologySpreadConstraints:
          - maxSkew: 1
            topologyKey: topology.kubernetes.io/zone
            whenUnsatisfiable: DoNotSchedule
            labelSelector:
              matchLabels:
                app: myapp
      
      containers:
        - name: myapp
          image: myapp:1.0.0
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080

# PodDisruptionBudget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 3  # At least 3 must be available during updates
  selector:
    matchLabels:
      app: myapp
```

## Câu hỏi 4: Làm thế nào để manage secrets một cách an toàn?

### Câu trả lời

```yaml
# Option 1: Kubernetes Secrets (basic)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DB_PASSWORD: "supersecret"
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
# Option 2: External Secrets (recommended for production)
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
    creationPolicy: Owner
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: secret/data/myapp
        property: password
    - secretKey: API_KEY
      remoteRef:
        key: secret/data/myapp
        property: api_key
```

```yaml
# Vault SecretStore configuration
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: kubernetes
          role: "myapp-role"
```

```bash
# Encrypt secrets at rest in etcd
# kube-apiserver configuration:
--encryption-provider-config=/etc/kubernetes/encryption-config.yaml
--encryption-provider-config-automatic-lookup

# encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <base64-encoded-key>
      - identity: {}
```

## Câu hỏi 5: Resource requests và limits hoạt động như thế nào?

### Câu trả lời

```yaml
# Resource configuration
resources:
  requests:
    memory: "128Mi"    # Guaranteed allocation
    cpu: "100m"        # 0.1 CPU cores
  limits:
    memory: "256Mi"   # Maximum allowed
    cpu: "500m"        # Maximum 0.5 cores
```

| QoS Class | Condition | Behavior |
|-----------|-----------|----------|
| Guaranteed | requests == limits for all containers | Last to be evicted |
| Burstable | requests < limits OR some resources not set | Evicted before Guaranteed |
| BestEffort | No requests or limits | First to be evicted |

```yaml
# Guaranteed QoS
containers:
  - name: app
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "128Mi"
        cpu: "100m"

# Burstable QoS
containers:
  - name: app
    resources:
      requests:
        memory: "64Mi"
        cpu: "50m"
      limits:
        memory: "256Mi"
        cpu: "500m"

# BestEffort QoS
containers:
  - name: app
    resources: {}  # No requests or limits
```

```bash
# Check pod QoS class
kubectl get pods -o custom-columns=NAME:.metadata.name,QOS:.status.qosClass

# Check node allocatable
kubectl describe node <node-name> | grep -A5 "Allocatable"
```

## Câu hỏi 6: Làm thế nào để scale applications?

### Câu trả lời

```yaml
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  
  minReplicas: 3
  maxReplicas: 10
  
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
```

```bash
# Manual scaling
kubectl scale deployment myapp --replicas=5

# Check HPA status
kubectl get hpa myapp
kubectl describe hpa myapp

# View HPA recommendations
kubectl get hpa myapp -o yaml | grep -A10 "metrics:"
```

```yaml
# Vertical Pod Autoscaler for right-sizing
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto"  # Or "Off" for recommendations only
  resourcePolicy:
    containerPolicies:
      - containerName: myapp
        minAllowed:
          cpu: 50m
          memory: 64Mi
        maxAllowed:
          cpu: 4
          memory: 8Gi
```

## Câu hỏi 7: Network policies hoạt động như thế nào?

### Câu trả lời

```yaml
# Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
    - Ingress

# Default deny all egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
spec:
  podSelector: {}
  policyTypes:
    - Egress
```

```yaml
# Allow frontend to communicate with API
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-from-frontend
spec:
  podSelector:
    matchLabels:
      app: api
      tier: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
              tier: frontend
      ports:
        - protocol: TCP
          port: 8080
```

```yaml
# Allow API to access database
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-allow-from-api
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api
      ports:
        - protocol: TCP
          port: 5432

# Allow API to access external DNS
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-dns
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector: {}  # All namespaces
      ports:
        - protocol: TCP
          port: 53
        - protocol: UDP
          port: 53
```

## Câu hỏi 8: StatefulSets hoạt động như thế nào và khi nào nên sử dụng?

### Câu trả lời

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: "postgres"  # Headless service name
  replicas: 3
  
  selector:
    matchLabels:
      app: postgres
  
  template:
    metadata:
      labels:
        app: postgres
    spec:
      terminationGracePeriodSeconds: 30
      
      containers:
        - name: postgres
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
              name: postgres
          
          env:
            - name: POSTGRES_REPLICATION_MODE
              value: "master"
            - name: POSTGRES_USERNAME
              value: "repl_user"
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secrets
                  key: replication-password
          
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
      
      # Anti-affinity for HA
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: postgres
              topologyKey: kubernetes.io/hostname
  
  # Persistent storage
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: "fast-ssd"
        resources:
          requests:
            storage: 50Gi
```

```yaml
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
      name: postgres
```

**Use StatefulSets when:**
- Stable, unique network identifiers needed
- Stable, persistent storage needed
- Ordered deployment and scaling
- Ordered, graceful deletion
- Ordered rolling updates

**Examples:** Databases (Postgres, MySQL, MongoDB), message queues (Kafka, RabbitMQ), any stateful distributed system.

## Câu hỏi 9: Làm thế nào để debug issues trong Kubernetes?

### Câu trả lời

```bash
# 1. Check pod status
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>

# 2. Check pod logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous  # Previous container
kubectl logs <pod-name> -n <namespace> -f  # Follow logs

# 3. Execute into container
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# 4. Check resource usage
kubectl top pod <pod-name> -n <namespace>
kubectl top node

# 5. Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
kubectl describe <resource-type> <name> -n <namespace>

# 6. Check service endpoints
kubectl get endpoints <service-name> -n <namespace>

# 7. Port forward for debugging
kubectl port-forward <pod-name> 8080:8080 -n <namespace>

# 8. Network debugging
kubectl exec -it <pod-name> -n <namespace> -- nc -zv <service> <port>
kubectl exec -it <pod-name> -n <namespace> -- curl -v http://<service>:<port>
```

```yaml
# Debug container for troubleshooting
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod
spec:
  restartPolicy: Never
  containers:
    - name: debug
      image: busybox:1.36
      command: ["sleep", "3600"]
      resources:
        limits:
          memory: 64Mi
          cpu: 100m
```

## Câu hỏi 10: Rolling updates và rollbacks hoạt động như thế nào?

### Câu trả lời

```yaml
# Deployment với rolling update strategy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Can have 5 pods during update (4+1)
      maxUnavailable: 0   # Always have 4 pods available
  minReadySeconds: 30     # Wait 30s before marking ready
  
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
# Check rollout status
kubectl rollout status deployment/myapp -n <namespace>

# View rollout history
kubectl rollout history deployment/myapp -n <namespace>

# Rollback to previous version
kubectl rollout undo deployment/myapp -n <namespace>

# Rollback to specific revision
kubectl rollout undo deployment/myapp -n <namespace> --to-revision=2

# Pause/resume rollout
kubectl rollout pause deployment/myapp -n <namespace>
kubectl rollout resume deployment/myapp -n <namespace>
```

```yaml
# Canary deployment with multiple deployments
---
# Stable version (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      track: stable
---
# Canary version (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      track: canary
---
# Service selects both
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
```

## Related Documents

- [Kubernetes Glossary](../glossary.md)
- [Kubernetes Architecture](../architecture.md)
- [Kubernetes Best Practices](../best-practice.md)
- [Kubernetes Anti-Patterns](../anti-pattern.md)
- [Kubernetes Checklist](../checklist.md)
- [Kubernetes Decision Tree](../decision-tree.md)
