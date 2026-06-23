# Kubernetes Knowledge Base - Decision Tree

## Tổng quan

Document này cung cấp cây quyết định chi tiết để hướng dẫn việc lựa chọn các Kubernetes resources và configurations phù hợp trong Cursor Enterprise Framework.

## 1. Workload Type Selection Tree

```
Bạn cần chọn workload type nào?
│
├── Ứng dụng stateless?
│   ├── Cần rolling updates? → Deployment
│   │   └── → RollingUpdate strategy với maxUnavailable: 0
│   │
│   ├── Cần one-time job? → Job
│   │   └── → Batch processing, migrations
│   │
│   └── Cần scheduled job? → CronJob
│       └── → Reports, backups, periodic tasks
│
├── Ứng dụng stateful?
│   ├── Cần stable identity? → StatefulSet
│   │   ├── Database replication
│   │   ├── Message queues
│   │   └── Leader election required
│   │
│   ├── Cần chạy trên mọi node? → DaemonSet
│   │   ├── Logging agents
│   │   ├── Monitoring agents
│   │   └── Network plugins
│   │
│   └── Cần one-time stateful job? → Job (với PVC)
│
└── Infrastructure workload?
    ├── Cluster autoscaler → Cluster Autoscaler
    ├── DNS → CoreDNS (DaemonSet)
    └── Ingress → Ingress Controller (Deployment)

WORKLOAD SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Stateless + Replicas    → Deployment                        │
│ Stateful + Stable IDs   → StatefulSet                       │
│ Every Node              → DaemonSet                         │
│ Batch/Cron              → Job/CronJob                       │
└─────────────────────────────────────────────────────────────┘
```

## 2. Service Type Selection Tree

```
Bạn cần expose service như thế nào?
│
├── Chỉ internal access (cluster-wide)?
│   └── → ClusterIP (default)
│       ├── Same namespace: http://service-name
│       └── Cross namespace: http://service-name.namespace.svc
│
├── Cần access từ bên ngoài cluster?
│   ├── Development/Local → NodePort
│   │   └── → NodeIP:NodePort (30000-32767)
│   │
│   ├── Production (Cloud)?
│   │   ├── AWS → LoadBalancer (NLB/ALB)
│   │   ├── GCP → LoadBalancer (Cloud L7)
│   │   └── Azure → LoadBalancer (L4)
│   │
│   └── HTTP/HTTPS routing?
│       └── → Ingress (với Ingress Controller)
│           ├── Multiple services
│           ├── TLS termination
│           └── Path-based routing
│
└── External service integration?
    └── → ExternalName (CNAME)

SERVICE TYPE SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Internal only          → ClusterIP                          │
│ External (dev)         → NodePort                           │
│ External (prod cloud)   → LoadBalancer                       │
│ HTTP routing           → Ingress + ClusterIP                 │
│ External DNS            → ExternalName                       │
└─────────────────────────────────────────────────────────────┘
```

## 3. Storage Selection Tree

```
Bạn cần chọn storage type nào?
│
├── Data có cần persist không?
│   ├── Không → emptyDir
│   │   ├── Temporary files
│   │   ├── Cache
│   │   └── Ephemeral data
│   │
│   └── Có → PersistentVolumeClaim
│       │
│       ├── Cloud storage?
│       │   ├── AWS → EBS (gp3), EFS (shared)
│       │   ├── GCP → Persistent Disk
│       │   └── Azure → Managed Disks
│       │
│       ├── On-prem?
│       │   ├── NFS → NFS volume
│       │   ├── iSCSI → iSCSI
│       │   └── Local storage → Local Persistent Volume
│       │
│       └── Database?
│           └── → Block storage (RWO)
│               └── StatefulSet với volumeClaimTemplates
│
├── Data có sensitive?
│   ├── Có → tmpfs (memory-backed)
│   │   └── → Data lost on pod restart!
│   │
│   └── Không → Regular volume
│
└── Cần share giữa pods?
    ├── Có → Shared storage (NFS, EFS, HostPath)
    │   └── → Access mode: ReadWriteMany
    │
    └── Không → Pod-specific (EBS, GCE PD)
        └── → Access mode: ReadWriteOnce

STORAGE SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Ephemeral/Temp        → emptyDir                           │
│ Persistent (single pod) → PVC + Block storage (RWO)          │
│ Persistent (multi-pod) → PVC + NFS/EFS (RWX)               │
│ Sensitive data         → tmpfs                              │
│ Database              → PVC + Block storage                 │
└─────────────────────────────────────────────────────────────┘
```

## 4. Security Configuration Tree

```
Bạn cần configure security như thế nào?
│
├── Pod Security?
│   ├── Enforce baseline? → PodSecurityPolicy (deprecated)
│   │   └── → Pod Security Standards: baseline
│   │
│   ├── Strictest? → Pod Security Standards: restricted
│   │   ├── Non-root required
│   │   ├── Read-only rootfs
│   │   └── Dropped capabilities
│   │
│   └── Disabled (testing only)? → privileged namespace
│
└── Container Security?
    │
    ├── Run as non-root?
    │   ├── Production → runAsNonRoot: true
    │   └── Dev → acceptable to run as root
    │
    ├── Prevent privilege escalation?
    │   └── → allowPrivilegeEscalation: false
    │
    ├── Drop capabilities?
    │   └── → capabilities.drop: ["ALL"]
    │
    └── Read-only filesystem?
        ├── Production → readOnlyRootFilesystem: true
        │   └── → Use volumes for writable paths
        │
        └── Dev → acceptable to have writable
```

## 5. Health Check Selection Tree

```
Bạn cần configure probe nào?
│
├── App có startup time dài (>30s)?
│   ├── Có → startupProbe REQUIRED
│   │   ├── failureThreshold: 30
│   │   ├── periodSeconds: 10
│   │   └── → Startup probe passes → enable liveness/readiness
│   │
│   └── Không → startupProbe optional
│
├── App có thể "hung" nhưng không crash?
│   ├── Có → livenessProbe
│   │   └── → Detect deadlocks, infinite loops
│   │       ├── httpGet: /healthz
│   │       ├── exec: custom command
│   │       └── tcpSocket: port check
│   │
│   └── Không → livenessProbe có thể optional
│
├── App cần warm-up time trước khi nhận traffic?
│   ├── Có → readinessProbe
│   │   ├── Check dependencies: DB, cache
│   │   ├── Check initialization complete
│   │   └── → Pod removed from Service endpoints
│   │
│   └── Không → readinessProbe optional

PROBE SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Slow startup          → startupProbe                        │
│ Detect hung process    → livenessProbe                       │
│ Delay traffic          → readinessProbe                     │
│ All three combined     → Best for production                 │
└─────────────────────────────────────────────────────────────┘
```

## 6. Resource Configuration Tree

```
Bạn nên set resource limits như thế nào?
│
├── Resource type?
│   │
│   ├── Memory-intensive (DB, cache)?
│   │   ├── requests.memory: 1-4Gi
│   │   ├── limits.memory: 2x requests
│   │   └── → Monitor OOM kills
│   │
│   ├── CPU-intensive (compute)?
│   │   ├── requests.cpu: 1-2 cores
│   │   ├── limits.cpu: 2-4 cores
│   │   └── → CPU throttling acceptable
│   │
│   └── Web API (balanced)?
│       ├── requests.cpu: 100-500m
│       ├── requests.memory: 128-512Mi
│       └── → Balanced limits
│
├── QoS class nào?
│   ├── Guaranteed (critical) → requests == limits
│   │   └── → Highest priority, last evicted
│   │
│   ├── Burstable (normal) → requests < limits
│   │   └── → Most workloads
│   │
│   └── BestEffort (batch) → no requests/limits
│       └── → Lowest priority, first evicted
│
└── Namespace có limits không?
    ├── Có LimitRange → Container defaults applied
    └── Không → Set explicit resources

RESOURCE RECOMMENDATIONS:
┌─────────────────────────────────────────────────────────────┐
│ Database (Postgres)    → 1-4Gi RAM, 1-2 CPU                │
│ Cache (Redis)          → 256Mi-2Gi RAM, 250m-1 CPU         │
│ Web API                → 128-512Mi RAM, 100-500m CPU        │
│ Worker                 → 512Mi-1Gi RAM, 500m-2 CPU         │
│ CronJob                → 64-256Mi RAM, 50-250m CPU          │
└─────────────────────────────────────────────────────────────┘
```

## 7. Network Policy Selection Tree

```
Bạn nên configure network policy như thế nào?
│
├── Default policy?
│   ├── Deny all ingress → Default deny Ingress
│   │   └── apiVersion: networking.k8s.io/v1 (policyTypes: [Ingress])
│   │
│   └── Deny all egress → Default deny Egress
│       └── policyTypes: [Egress]
│
├── Allow traffic pattern?
│   │
│   ├── Frontend → API?
│   │   └── → Egress rule: API namespace/label
│   │
│   ├── API → Database?
│   │   └── → Egress rule: Database namespace/label, port 5432
│   │
│   ├── API → Cache?
│   │   └── → Egress rule: Redis label, port 6379
│   │
│   └── API → External APIs?
│       ├── Allow DNS (port 53)
│       └── Allow specific external IPs
│
└── Namespace isolation?
    ├── Same namespace only → podSelector: {}
    ├── Same team/label → podSelector: {matchLabels: {...}}
    └── Different namespace → namespaceSelector: {matchLabels: {...}}

NETWORK POLICY TEMPLATE:
┌─────────────────────────────────────────────────────────────┐
│ 1. Default deny-all ingress                                │
│ 2. Default deny-all egress                                │
│ 3. Allow DNS (TCP/UDP port 53)                            │
│ 4. Allow from ingress controller                           │
│ 5. Allow app-to-app based on labels                       │
│ 6. Allow to external dependencies                         │
└─────────────────────────────────────────────────────────────┘
```

## 8. Scaling Decision Tree

```
Bạn cần scaling strategy nào?
│
├── Manual scaling?
│   └── kubectl scale deployment --replicas=N
│       └── → Temporary/lab environments
│
├── Horizontal Pod Autoscaling?
│   ├── Metric-based (CPU, memory) → HPA với resource metrics
│   │   └── → General purpose, most workloads
│   │
│   ├── Custom metrics → HPA với custom metrics adapter
│   │   └── → Queue depth, request rate
│   │
│   └── Multi-dimensional → HPA với multiple metrics
│       └── → Complex scaling requirements
│
├── Vertical Pod Autoscaling?
│   ├── Recommendations only → VPA Off
│   │   └── → Analyze without changes
│   │
│   └── Auto-apply → VPA Auto/Recreate
│       └── → Not recommended for production (pod restarts)
│
└── Cluster Autoscaling?
    └── → Add/remove nodes based on resource pressure
        ├── Cloud: Managed (EKS, GKE, AKS)
        └── On-prem: Cluster Autoscaler/KEDA

SCALING COMBINATION:
┌─────────────────────────────────────────────────────────────┐
│ Standard web app   → HPA (CPU/Memory)                       │
│ Queue processor    → HPA (Custom: queue depth)             │
│ Database           → Manual/Scheduled (VPA recommendations)│
│ Worker jobs        → KEDA (event-driven scaling)           │
│ All                → Cluster Autoscaler for nodes          │
└─────────────────────────────────────────────────────────────┘
```

## 9. High Availability Decision Tree

```
Bạn cần HA configuration nào?
│
├── Replicas count?
│   ├── Minimum HA → 2 replicas
│   │   └── → One node failure OK
│   │
│   ├── Standard HA → 3 replicas
│   │   └── → One AZ failure OK
│   │
│   └── Maximum HA → 5+ replicas
│       └── → Multiple failures OK, higher cost
│
├── Pod distribution?
│   │
│   ├── Spread across nodes? → PodAntiAffinity
│   │   ├── preferredDuringSchedulingIgnoredDuringExecution
│   │   └── requiredDuringSchedulingIgnoredDuringExecution
│   │
│   └── Spread across zones? → TopologySpreadConstraints
│       ├── maxSkew: 1
│       └── topologyKey: topology.kubernetes.io/zone
│
└── Disruption protection?
    │
    ├── PodDisruptionBudget
    │   ├── minAvailable: N (number of pods)
    │   └── maxUnavailable: N (percentage)
    │
    └── → Always create PDB for production deployments

HA CONFIGURATION:
┌─────────────────────────────────────────────────────────────┐
│ Replicas          → 3+ for production                      │
│ Anti-affinity     → required (kubernetes.io/hostname)       │
│ Zone spread       → maxSkew: 1, DoNotSchedule              │
│ PDB               → minAvailable: 2 (for 3 replicas)       │
│ Readiness gate    → Ensure healthy before receiving traffic │
└─────────────────────────────────────────────────────────────┘
```

## 10. Update Strategy Selection Tree

```
Bạn nên chọn update strategy nào?
│
├── Rolling Update (default)?
│   ├── maxUnavailable: 0 → Zero downtime, slower
│   │   └── → maxSurge: 1 (temporary extra pod)
│   │
│   ├── maxUnavailable: 1 → Faster, brief partial capacity
│   │   └── → 4 replicas: 3 always available
│   │
│   └── maxUnavailable: 25% → Fastest, significant capacity drop
│       └── → Only for non-critical workloads
│
├── Recreate?
│   └── → Kills all pods, creates new
│       ├── Database migrations requiring exclusive access
│       └── State applications where rolling doesn't work
│
└── Canary Deployment?
    ├── Manual canary → 2 deployments, adjust traffic
    │   └── → Direct traffic shift
    │
    ├── Progressive canary → Argo Rollouts/Flagger
    │   ├── Step-based progression
    │   ├── Automated rollback on failure
    │   └── → Advanced deployment strategies
    │
    └── Blue/Green → 2 identical environments
        └── → Instant switch, higher resource cost

UPDATE STRATEGY:
┌─────────────────────────────────────────────────────────────┐
│ Zero downtime (critical) → RollingUpdate, maxUnavailable: 0│
│ Fast deployment          → RollingUpdate, maxUnavailable: 1│
│ Database migrations     → Recreate strategy                 │
│ Risky changes           → Canary (manual or automated)      │
│ Instant switch          → Blue/Green deployment             │
└─────────────────────────────────────────────────────────────┘
```

## 11. Quick Reference Decision Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUICK DECISION GUIDE                            │
├────────────────────────────────┬───────────────────────────────────────┤
│ SITUATION                      │ DECISION                               │
├────────────────────────────────┼───────────────────────────────────────┤
│ Stateless app                  │ Deployment                             │
│ Database/Stateful              │ StatefulSet                           │
│ Per-node agent                 │ DaemonSet                             │
│ Batch job                      │ Job                                   │
│ Scheduled task                 │ CronJob                               │
├────────────────────────────────┼───────────────────────────────────────┤
│ Internal communication         │ ClusterIP Service                     │
│ External HTTP access           │ Ingress + ClusterIP                   │
│ External TCP/UDP               │ LoadBalancer Service                  │
│ Development testing            │ NodePort Service                      │
├────────────────────────────────┼───────────────────────────────────────┤
│ Temporary data                 │ emptyDir                              │
│ Persistent data (single pod)   │ PVC + ReadWriteOnce                   │
│ Persistent data (multi-pod)   │ PVC + ReadWriteMany                   │
│ Sensitive temporary data       │ tmpfs                                 │
├────────────────────────────────┼───────────────────────────────────────┤
│ Non-root container             │ securityContext.runAsNonRoot: true    │
│ Prevent privilege escalation   │ allowPrivilegeEscalation: false       │
│ Drop all capabilities          │ capabilities.drop: ["ALL"]            │
│ Read-only filesystem           │ readOnlyRootFilesystem: true          │
├────────────────────────────────┼───────────────────────────────────────┤
│ Slow starting app              │ startupProbe                          │
│ Detect hung process            │ livenessProbe                         │
│ Delay traffic                  │ readinessProbe                        │
├────────────────────────────────┼───────────────────────────────────────┤
│ Guaranteed resources           │ requests == limits (Guaranteed QoS)  │
│ Variable resources             │ requests < limits (Burstable QoS)     │
│ Batch processing               │ No limits (BestEffort QoS)            │
├────────────────────────────────┼───────────────────────────────────────┤
│ Critical deployment            │ 3 replicas + PDB + Anti-affinity     │
│ Fast deployment                │ RollingUpdate, maxUnavailable: 1      │
│ Zero downtime                  │ RollingUpdate, maxUnavailable: 0      │
│ Risky changes                  │ Canary/Blue-Green                     │
└────────────────────────────────┴───────────────────────────────────────┘
```

## Related Documents

- [Kubernetes Glossary](../glossary.md)
- [Kubernetes Architecture](../architecture.md)
- [Kubernetes Best Practices](../best-practice.md)
- [Kubernetes Anti-Patterns](../anti-pattern.md)
- [Kubernetes Checklist](../checklist.md)
- [Kubernetes FAQ](../faq.md)
