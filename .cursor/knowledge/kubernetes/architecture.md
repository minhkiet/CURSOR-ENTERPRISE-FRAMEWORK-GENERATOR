---
title: "Kubernetes Architecture"
description: "Chi tiết kiến trúc Kubernetes - Control Plane, Worker Nodes, Network, Storage và các components cốt lõi"
tags: ["kubernetes", "k8s", "architecture", "control-plane", "worker-node", "etcd", "networking"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Kubernetes Architecture

## Tổng quan (Overview)

Kubernetes (thường gọi tắt là K8s) là một container orchestration platform mã nguồn mở được phát triển bởi Google, cho phép deploy, scale, và manage các containerized applications một cách tự động. Kiến trúc Kubernetes được thiết kế theo mô hình master-worker, trong đó Control Plane chịu trách nhiệm quản lý và điều phối toàn bộ cluster, còn Worker Nodes thực hiện công việc chạy các workloads.

Mục đích chính của tài liệu này là cung cấp kiến thức toàn diện về kiến trúc Kubernetes trong Cursor Enterprise Framework, bao gồm các thành phần cốt lõi, cách chúng tương tác với nhau, và các best practices để thiết kế một production-ready Kubernetes cluster. Tài liệu này phù hợp cho các developers, DevOps engineers, và system architects đang làm việc với Kubernetes trong môi trường enterprise.

## Kiến trúc tổng quan (High-Level Architecture)

### Mô hình Master-Worker

Kubernetes cluster bao gồm hai phần chính: Control Plane (hay còn gọi là Master node) và Worker Nodes. Control Plane chịu trách nhiệm quản lý trạng thái của toàn bộ cluster, bao gồm scheduling, scaling, và maintaining desired state. Worker Nodes là các machines (physical hoặc virtual) chạy các containers và thực hiện công việc được giao bởi Control Plane.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KUBERNETES CLUSTER                                │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         CONTROL PLANE                                  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │ kube-      │  │   etcd      │  │  kube-      │  │  kube-      │  │  │
│  │  │ apiserver  │◄─┤  (state     │  │  scheduler  │  │  controller │  │  │
│  │  │            │  │   store)     │  │            │  │  manager    │  │  │
│  │  └──────┬──────┘  └─────────────┘  └──────┬──────┘  └──────┬──────┘  │  │
│  └─────────┼───────────────────────────────────┼───────────────┼─────────┘  │
│            │                                   │               │            │
│            └───────────────────────────────────┴───────────────┘            │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         WORKER NODES                                  │  │
│  │                                                                       │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │  │
│  │  │   Node 1        │  │   Node 2        │  │   Node 3        │      │  │
│  │  │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │      │  │
│  │  │  │ kubelet   │  │  │  │ kubelet   │  │  │  │ kubelet   │  │      │  │
│  │  │  │ kube-proxy│  │  │  │ kube-proxy│  │  │  │ kube-proxy│  │      │  │
│  │  │  │ Container │  │  │  │ Container │  │  │  │ Container │  │      │  │
│  │  │  │ Runtime   │  │  │  │ Runtime   │  │  │  │ Runtime   │  │      │  │
│  │  │  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │      │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### High Availability Architecture

Trong production environments, Control Plane thường được deploy với multiple instances để đảm bảo high availability. Các best practices cho HA bao gồm việc deploy at least three instances của mỗi Control Plane component, sử dụng stacked etcd hoặc external etcd cluster, và đảm bảo nodes được phân bố across different availability zones.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HIGH AVAILABILITY CONTROL PLANE                           │
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                       │
│  │   Node 1    │    │   Node 2    │    │   Node 3    │                       │
│  │ ┌─────────┐ │    │ ┌─────────┐ │    │ ┌─────────┐ │                       │
│  │ │apiserver│ │    │ │apiserver│ │    │ │apiserver│ │                       │
│  │ │scheduler│ │    │ │scheduler│ │    │ │scheduler│ │                       │
│  │ │controller│ │   │ │controller│ │   │ │controller│ │                      │
│  │ └────┬────┘ │    │ └────┬────┘ │    │ └────┬────┘ │                       │
│  │      │      │    │      │      │    │      │      │                       │
│  │      └──────┼────┴──────┼──────┴──────┼──────┘                       │
│  │             │           │              │                                │
│  │             └───────────┼──────────────┘                                │
│  │                         ▼                                              │
│  │                  ┌─────────────┐                                        │
│  │                  │   etcd     │ (stacked or external cluster)          │
│  │                  │  Cluster   │                                        │
│  │                  └─────────────┘                                        │
│  └─────────────────────────────────────────────────────────────────────────┘
```

## Control Plane Components

### kube-apiserver

API Server là component trung tâm của Kubernetes, cung cấp RESTful API để tất cả các interactions với cluster đều thông qua nó. Đây là front-end cho Kubernetes control plane, xử lý tất cả các requests từ users, kubectl, và các internal components. API Server validate và configure data cho các API objects như Pods, Services, Deployments, và các resources khác.

API Server sử dụng etcd như backing store cho tất cả cluster data, nhưng không bao giờ directly access etcd từ kubelets hoặc other components - tất cả đều phải thông qua API Server. Điều này đảm bảo rằng cluster state được centralized và validated tại một điểm duy nhất.

```yaml
# Example API Server configuration in kube-apiserver manifest
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
    - name: kube-apiserver
      image: registry.k8s.io/kube-apiserver:v1.28.0
      command:
        - kube-apiserver
        - --etcd-servers=https://127.0.0.1:2379
        - --service-cluster-ip-range=10.96.0.0/12
        - --bind-address=0.0.0.0
        - --secure-port=6443
        - --tls-cert-file=/var/lib/kubernetes/pki/apiserver.crt
        - --tls-private-key-file=/var/lib/kubernetes/pki/apiserver.key
        - --client-ca-file=/var/lib/kubernetes/pki/ca.crt
        - --service-account-key-file=/var/lib/kubernetes/pki/sa.pub
        - --service-account-issuer=https://kubernetes.default.svc
      ports:
        - containerPort: 6443
          protocol: TCP
      volumeMounts:
        - name: pki
          mountPath: /var/lib/kubernetes/pki
          readOnly: true
```

API Server hỗ trợ multiple authentication mechanisms bao gồm client certificates, bearer tokens, Bootstrap tokens, và OIDC. Authorization được thực hiện thông qua RBAC (Role-Based Access Control) hoặc other authorization modes như ABAC, Node, hay Webhook. Admission controllers cung cấp một layer cuối để mutate hoặc validate objects trước khi chúng được persisted vào etcd.

### etcd

etcd là một distributed, reliable key-value store được sử dụng để store tất cả cluster data bao gồm pod specifications, service definitions, configmaps, secrets, và cluster state. etcd sử dụng Raft consensus algorithm để đảm bảo strong consistency và high availability trong trường hợp một số nodes fail.

Trong một production Kubernetes cluster, etcd cluster nên có ít nhất 3 hoặc 5 nodes để đảm bảo quorum và fault tolerance. etcd data nên được backed up regularly sử dụng tools như etcdctl snapshot save để phục vụ disaster recovery.

```bash
# Backup etcd data
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /backup/etcd-snapshot.db

# Restore etcd from backup
ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd-snapshot.db \
  --data-dir=/var/lib/etcd/restore
```

etcd's consistent data model với hierarchical keys làm cho nó phù hợp cho storing complex nested structures như Kubernetes objects. Tuy nhiên, điều quan trọng cần lưu ý là etcd performance phụ thuộc heavily vào disk I/O, do đó production clusters nên sử dụng SSDs cho etcd storage.

### kube-scheduler

Scheduler là component chịu trách nhiệm assigning Pods tới Nodes dựa trên resource requirements, constraints, affinity/anti-affinity rules, và other policies. Khi một Pod mới được create nhưng chưa được assign tới any node, Scheduler chọn một node phù hợp nhất từ pool của available nodes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KUBERNETES SCHEDULER                                │
│                                                                              │
│  1. Filtering        2. Scoring           3. Binding                        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                     │
│  │ Filter      │    │ Score       │    │ Bind        │                     │
│  │ Nodes       │───▶│ Nodes       │───▶│ Pod to      │                     │
│  │ (Predicate) │    │ (Priority)  │    │ Node        │                     │
│  └─────────────┘    └─────────────┘    └─────────────┘                       │
│                                                                              │
│  Scoring Plugins:                                                           │
│  - ImageLocality: Prefer nodes with cached images                            │
│  - InterPodAffinity: Honor pod affinity rules                               │
│  - LeastRequested: Balance resource usage                                   │
│  - NodeAffinity: Honor node selector/affinity                              │
│  - NodeResources: Consider CPU/memory availability                          │
│  - PodTopologySpread: Distribute pods across topology                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

Scheduler hoạt động theo hai giai đoạn chính: filtering và scoring. Trong giai đoạn filtering, scheduler loại bỏ các nodes không đáp ứng được pod's requirements như resource requests, node selectors, taints, và affinity rules. Trong giai đoạn scoring, scheduler rank các eligible nodes và chọn node có score cao nhất.

```yaml
# Pod with specific scheduling requirements
apiVersion: v1
kind: Pod
metadata:
  name: scheduled-pod
spec:
  containers:
    - name: app
      image: myapp:1.0.0
      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1000m"
  
  # Node selector for specific node characteristics
  nodeSelector:
    disktype: ssd
    region: us-west-2
  
  # Tolerations to allow scheduling on tainted nodes
  tolerations:
    - key: "node-type"
      operator: "Equal"
      value: "compute-optimized"
      effect: "NoSchedule"
  
  # Affinity rules for pod placement
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          preference:
            matchExpressions:
              - key: "gpu"
                operator: In
                values: ["available"]
```

### kube-controller-manager

Controller Manager là component chạy các controller processes, điều khiển various reconciliation loops that regulate the state of the cluster. Mỗi controller là một separate process, nhưng để simplify complexity, chúng đều được compile thành một single binary và chạy trong một single process.

Các controllers quan trọng bao gồm Node Controller (theo dõi nodes và respond khi nodes become unavailable), Replication Controller (duy trì correct number of pods cho replicated applications), Endpoints Controller (populates endpoints for services), Service Account Controller (tạo default accounts cho new namespaces), và Resource quota Controller (đảm bảo namespace-level resource quotas được enforced).

```go
// Conceptual representation of controller reconciliation loop
type Controller interface {
    // Reconcile compares desired state with actual state
    // and takes actions to reconcile them
    Reconcile(ctx context.Context, key string) error
    
    // Name returns the controller's name for logging
    Name() string
}

// Example: Node Controller handles node failures
type NodeController struct {
    nodeInformer coreinformers.NodeInformer
    kubeClient   clientset.Interface
    // ... other dependencies
}

func (nc *NodeController) Reconcile(ctx context.Context, req reconcile.Request) (reconcile.Result, error) {
    node, err := nc.nodeInformer.Lister().Get(req.Name)
    if errors.IsNotFound(err) {
        // Node deleted - cleanup
        return reconcile.Result{}, nil
    }
    
    // Check node condition and handle accordingly
    // - Ready, NotReady, MemoryPressure, DiskPressure, PIDPressure, NetworkUnavailable
    return reconcile.Result{}, nil
}
```

## Worker Node Components

### kubelet

kubelet là một agent chạy trên mỗi node trong cluster, chịu trách nhiệm maintaining the state of all containers in its node. kubelet nhận Pod specifications từ API Server và đảm bảo rằng containers described in those specs are running and healthy. Nó also reports node and pod status back to the API Server.

kubelet không quản lý containers được create bởi Kubernetes không phải là Docker hoặc containerd. Nó tương tác với container runtime thông qua Container Runtime Interface (CRI), cho phép nó làm việc với bất kỳ container runtime nào implement interface này.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              KUBELET                                        │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         kubelet Process                              │   │
│  │                                                                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │ Pod         │  │ Image       │  │ Container   │  │ Node        │  │   │
│  │  │ Lifecycle   │  │ Manager     │  │ Logger      │  │ Lease       │  │   │
│  │  │ Manager     │  │             │  │             │  │ Manager     │  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │   │
│  │         │                │                │                │         │   │
│  │         └────────────────┼────────────────┴────────────────┘         │   │
│  │                          │                                           │   │
│  │                    ┌─────▼─────┐                                     │   │
│  │                    │   CRI     │ (Container Runtime Interface)        │   │
│  │                    │   Shim    │                                     │   │
│  │                    └─────┬─────┘                                     │   │
│  │                          │                                           │   │
│  │  ┌───────────────────────┼───────────────────────────────────────┐  │   │
│  │  │                       ▼                                        │  │   │
│  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐                  │  │   │
│  │  │  │ containerd│  │  Docker   │  │  CRI-O    │ (Any CRI impl)   │  │   │
│  │  │  └───────────┘  └───────────┘  └───────────┘                  │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

kubelet also responsible cho managing volumes và secrets, mount volumes vào containers, và reporting pod và node status. Nó sử dụng a cgroup driver để quản lý resource isolation và ensure containers don't exceed their resource limits.

```yaml
# kubelet configuration example (kubeadm config)
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
address: 0.0.0.0
anonymousAuth: false
authentication:
  webhook:
    enabled: true
    cacheTTL: 2m0s
authorization:
  mode: Webhook
  webhook:
    cacheAuthorizedTTL: 5m0s
    cacheUnauthorizedTTL: 30s

cgroupDriver: systemd
cgroupRoot: /
clusterDNS:
  - 10.96.0.10
clusterDomain: cluster.local
cpuManagerReconcilePeriod: 10s
evictionHard:
  memory.available: 100Mi
  nodefs.available: 10%
  imagefs.available: 15%
  imagefs.inodesFree: 5%
evictionPressureTransitionPeriod: 5m0s
failSwapOn: true
fileCheckFrequency: 20s
healthzBindAddress: 127.0.0.1
healthzPort: 10248
httpCheckFrequency: 20s
imageMinimumGCAge: 2m0s
logging:
  verbosity: 2
maxOpenFiles: 1000000
maxPods: 110
nodeLeaseDurationSeconds: 40
nodeStatusReportFrequency: 10s
nodeStatusUpdateFrequency: 10s
resolvConf: /run/systemd/resolve/resolv.conf
runtimeRequestTimeout: 2m0s
serializeImagePulls: true
staticPodPath: /etc/kubernetes/manifests
streamingConnectionIdleTimeout: 4h0m0s
syncFrequency: 1m0s
volumeStatsAggPeriod: 1m0s
```

### kube-proxy

kube-proxy là network proxy chạy trên mỗi node, duy trì network rules trên local node để cho phép communication tới Pods từ inside hoặc outside cluster. kube-proxy translates Service VIP (Virtual IP) requests tới backend Pod IPs sử dụng iptables hoặc IPVS rules.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            KUBE-PROXY                                       │
│                                                                              │
│  Service VIP: 10.96.45.123:80                                               │
│                     │                                                        │
│                     ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      iptables / IPVS Rules                          │   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │ KUBE-SERVICES                                                 │   │   │
│  │  │   └─▶ KUBE-SVC-XXXXXXXX (Service)                            │   │   │
│  │  │         ├─▶ KUBE-SEP-XXXXX1 (Pod 1) ──▶ 10.244.1.15:8080     │   │   │
│  │  │         ├─▶ KUBE-SEP-XXXXX2 (Pod 2) ──▶ 10.244.2.23:8080     │   │   │
│  │  │         └─▶ KUBE-SEP-XXXXX3 (Pod 3) ──▶ 10.244.1.8:8080      │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

kube-proxy hỗ trợ ba operating modes: iptables (default), IPVS, và userspace. Mode iptables sử dụng kernel's iptables rules để forward traffic, trong khi IPVS cung cấp better performance với larger number of Services thông qua in-kernel load balancing. Userspace mode, deprecated trong newer versions, handles traffic routing in userspace process.

```yaml
# kube-proxy configuration with IPVS mode
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
ipvs:
  scheduler: "rr"  # Round Robin
  excludeCIDRs:
    - "10.0.0.0/8"
  minSyncPeriod: 0s
  syncPeriod: 30s
  strict ARP: true

# iptables configuration (default)
# mode: "iptables"
# iptables:
#   masqueradeAll: false
#   masqueradeBit: 14
#   minSyncPeriod: 0s
#   syncPeriod: 30s
```

### Container Runtime Interface (CRI)

Container Runtime Interface là một plugin interface cho phép kubelet sử dụng various container runtimes mà không cần biết implementation details. CRI defines the protocol buffers và gRPC services cho managing containers và container images.

Các container runtimes phổ biến được support bao gồm containerd (production standard), Docker (through dockershim, deprecated in K8s 1.24+), CRI-O (lightweight, OCI-compliant), và Mirantis Container Runtime. Việc chọn container runtime phụ thuộc vào specific requirements như security, performance, và compliance.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONTAINER RUNTIME INTERFACE                              │
│                                                                              │
│                         ┌──────────────────┐                               │
│                         │     kubelet      │                               │
│                         └────────┬─────────┘                               │
│                                  │                                         │
│                    CRI API (gRPC over Unix Socket)                          │
│                                  │                                         │
│                         ┌────────▼─────────┐                               │
│                         │    CRI Shims     │                               │
│                         │                  │                               │
│  ┌──────────────────────┼──────────────────┼──────────────────────────┐  │
│  │                      │                  │                              │  │
│  │    ┌───────────┐     │   ┌─────────┐   │    ┌───────────┐           │  │
│  │    │containerd │     │   │ CRI-O   │   │    │  Docker   │           │  │
│  │    │  (cri)    │     │   │         │   │    │(dockershim)          │  │
│  │    └─────┬─────┘     │   └────┬────┘   │    │ (deprecated)        │  │
│  │          │            │        │        │    └───────────┘           │  │
│  │          │            │        │        │                              │  │
│  │    ┌─────▼─────┐     │  ┌─────▼─────┐  │                              │  │
│  │    │   runc    │     │  │  runc     │  │                              │  │
│  │    │           │     │  │           │  │                              │  │
│  │    └───────────┘     │  └───────────┘  │                              │  │
│  └───────────────────────┴──────────────────┴──────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Networking Architecture

### Container Network Interface (CNI)

CNI (Container Network Interface) là một specification và library cho configuring network connectivity trong containers. Kubernetes sử dụng CNI plugins để assign IP addresses cho Pods và connect containers tới networks.

Các CNI plugins phổ biến bao gồm Calico (policy-based networking, supports BGP), Flannel (simple overlay networking), Cilium (eBPF-based networking with security), Weave Net (simple, resilient networking), và Amazon VPC CNI (native AWS networking).

```json
{
  "cniVersion": "1.0.0",
  "name": "kubernetes-network",
  "type": "calico",
  "ipam": {
    "type": "host-local",
    "subnet": "usePodCidr"
  },
  "policy": {
    "type": "k8s"
  },
  "kubernetes": {
    "kubeconfig": "/etc/cni/net.d/calico.kubeconfig"
  }
}
```

### Pod Networking Model

Mỗi Pod trong Kubernetes nhận một unique IP address trong cluster, và tất cả containers trong một Pod chia sẻ network namespace. Điều này có nghĩa là containers trong cùng Pod có thể communicate với nhau qua localhost.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         POD NETWORK NAMESPACE                               │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Network Namespace (netns)                       │   │
│  │                                                                      │   │
│  │    eth0 ────────────────────────── Network (Overlay/VLAN)           │   │
│  │      │                                                                   │   │
│  │  ┌───┴───┐                                                             │   │
│  │  │       │                                                             │   │
│  │  │   ┌───┴───┐    localhost:8080                                    │   │
│  │  │   │init   │    (shared between containers)                        │   │
│  │  │   │container│                                                       │   │
│  │  │   └───────┘                                                        │   │
│  │  │                                                                     │   │
│  │  │   ┌─────────┐    ┌─────────┐    ┌─────────┐                        │   │
│  │  │   │Container│    │Container│    │Container│                        │   │
│  │  │   │    A    │    │    B    │    │    C    │                        │   │
│  │  │   │ port:80 │    │ port:90 │    │port:8080│                       │   │
│  │  │   └─────────┘    └─────────┘    └─────────┘                        │   │
│  │  │                                                                     │   │
│  └──┼─────────────────────────────────────────────────────────────────────┘   │
│     │                                                                       │
│     └───────────▶ eth0 (Pod IP: 10.244.1.15)                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

Kubernetes không specified một particular networking implementation, nhưng yêu cầu all containers có thể communicate với all other containers without NAT, và all nodes có thể communicate với all containers without NAT. Điều này được gọi là "pod-to-pod" networking model.

### Service Networking

Services cung cấp một stable IP address (ClusterIP) và DNS name cho một set of Pods, cho phép loose coupling giữa frontend và backend applications. Kube-proxy handles traffic routing từ Service IP tới backend Pods.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SERVICE DISCOVERY                                    │
│                                                                              │
│  ┌─────────────┐                                                            │
│  │   Ingress   │ ───▶ Frontend Service (10.96.45.100:80)                   │
│  │  Controller │                            │                                │
│  └─────────────┘                            ▼                                │
│                                     ┌─────────────┐                         │
│                                     │  Frontend   │                         │
│                                     │  Pods (3)   │                         │
│                                     └──────┬──────┘                         │
│                                            │                                 │
│                                     Backend Service (10.96.45.123:8080)      │
│                                            │                                │
│                                            ▼                                │
│                                     ┌─────────────┐                         │
│                                     │   Backend   │                         │
│                                     │   Pods (3)  │                         │
│                                     └──────┬──────┘                         │
│                                            │                                 │
│                                       Database Service (10.96.45.200:5432)  │
│                                            │                                │
│                                            ▼                                │
│                                     ┌─────────────┐                         │
│                                     │  PostgreSQL │                         │
│                                     │  StatefulSet │                         │
│                                     └─────────────┘                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Storage Architecture

### Persistent Storage

Kubernetes cung cấp PersistentVolume (PV) và PersistentVolumeClaim (PVC) để manage persistent storage. PV là một piece of storage trong cluster đã được provisioned bởi administrator hoặc dynamically provisioned using StorageClass. PVC là request for storage by a user.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PERSISTENT STORAGE                                   │
│                                                                              │
│  PersistentVolume (Provisioned)                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  spec:                                                              │   │
│  │    capacity: { storage: 100Gi }                                    │   │
│  │    accessModes: [ReadWriteOnce]                                    │   │
│  │    persistentVolumeReclaimPolicy: Retain                           │   │
│  │    storageClassName: fast-ssd                                     │   │
│  │    nfs:                                                             │   │
│  │      path: /exports/data                                            │   │
│  │      server: nfs.example.com                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ▲                                        │
│                              Bound by               ┌──────────────────┐   │
│                                    │                │ PersistentVolume │   │
│                                    │                │ Claim (PVC)      │   │
│                                    └──────────┐      │                  │   │
│  ┌──────────────────────────────────────────────┐  └──────────────────┘   │
│  │                    Pod                        │                         │
│  │  ┌────────────────────────────────────────┐  │                         │
│  │  │ spec:                                   │  │                         │
│  │  │   volumes:                             │  │                         │
│  │  │     - name: data                      │  │                         │
│  │  │       persistentVolumeClaim:          │  │                         │
│  │  │         claimName: app-data            │  │                         │
│  │  │   containers:                          │  │                         │
│  │  │     - name: app                        │  │                         │
│  │  │       volumeMounts:                    │  │                         │
│  │  │         - name: data                   │  │                         │
│  │  │           mountPath: /var/lib/app      │  │                         │
│  │  └────────────────────────────────────────┘  │                         │
│  └────────────────────────────────────────────────┘                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Storage Classes

StorageClass cung cấp một cách để administrators describe các "types" of storage they offer. Different classes có thể map tới different quality-of-service levels, backup policies, hoặc arbitrary policies được determined by cluster administrators.

```yaml
# StorageClass for fast SSD storage
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: pd.csi.storage.gke.io  # GKE Persistent Disk
parameters:
  type: pd-ssd
  replication-type: regional-pd
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Retain

---
# StorageClass for NFS
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-storage
provisioner: nfs.storage.k8s.io
parameters:
  server: nfs.example.com
  path: /exports/shared
volumeBindingMode: Immediate
reclaimPolicy: Delete
```

### Container Storage Interface (CSI)

CSI là một standard cho exposing arbitrary block và file storage systems tới containerized workloads trên Container Orchestration Systems như Kubernetes. CSI plugins được deploy như containerized workloads, cho phép vendors implement their own storage plugins without modifying Kubernetes core code.

## Admission Controllers và API Extensions

### Admission Controllers

Admission controllers là plugins that intercept requests to the Kubernetes API server after authentication and authorization, but before objects are persisted. Chúng được sử dụng để enforce custom policies, mutate objects with default values, hoặc validate complex constraints.

```yaml
# Example: MutatingWebhookConfiguration for adding default labels
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  name: default-labels-webhook
webhooks:
  - name: add-default-labels.example.com
    clientConfig:
      service:
        name: webhook-service
        namespace: default
        path: "/mutate"
      caBundle: <base64-encoded-ca-cert>
    rules:
      - operations: ["CREATE", "UPDATE"]
        apiGroups: [""]
        apiVersions: ["v1"]
        resources: ["pods", "deployments"]
    namespaceSelector:
      matchLabels:
        webhook-enabled: "true"
    admissionReviewVersions: ["v1", "v1beta1"]
    sideEffects: None
```

Các admission controllers phổ biến bao gồm NamespaceLifecycle (prevent creation in non-existent namespaces), LimitRanger (enforce resource limits), ResourceQuota (enforce resource quotas), ServiceAccount (automount API credentials for ServiceAccounts), và DefaultStorageClass (assign default StorageClass to PVCs without one).

### Custom Resource Definitions (CRDs)

CRDs cho phép users tạo new resource types mà không cần adding another API server. Đây là cách phổ biến để extend Kubernetes API với custom resources, được sử dụng rộng rãi bởi operators và add-ons như Prometheus Operator, cert-manager, và Argo CD.

```yaml
# Example CRD for a custom backup resource
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: backups.example.com
  labels:
    app.kubernetes.io/name: backup-operator
spec:
  group: example.com
  names:
    kind: Backup
    listKind: BackupList
    plural: backups
    singular: backup
    shortNames:
      - bk
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                schedule:
                  type: string
                retention:
                  type: integer
                destination:
                  type: string
            status:
              type: object
              properties:
                lastRun:
                  type: string
                  format: date-time
                completed:
                  type: boolean
```

## Common Patterns

### Declarative Configuration

Kubernetes encourages declarative configuration, trong đó users define desired state thay vì imperatively commanding what to do. Configuration files (manifests) define the desired state of resources, và Kubernetes controllers work continuously để achieve và maintain that state.

```yaml
# Declarative deployment - user defines desired state
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: production
spec:
  replicas: 3  # Desired: 3 replicas always running
  selector:
    matchLabels:
      app: webapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: webapp
        version: v2.1.0
    spec:
      containers:
        - name: webapp
          image: myapp:2.1.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
```

### Operators và Custom Controllers

Operators là pattern trong đó custom controllers encode operational knowledge vào Kubernetes, cho phép automated management của complex stateful applications. Operators use CRDs để define custom resources và watch for changes to automatically manage the underlying system.

## Troubleshooting

### Kiểm tra Control Plane Health

```bash
# Check control plane pods status
kubectl get pods -n kube-system

# Get detailed information about API server
kubectl get componentstatuses  # deprecated in newer versions
kubectl get --raw='/healthz'

# Check etcd cluster health
kubectl exec -n kube-system etcd-<node-name> -- etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health

# View API server logs
kubectl logs -n kube-system kube-apiserver-<node-name>
```

### Kiểm tra Node Status

```bash
# List all nodes with status
kubectl get nodes -o wide

# Describe specific node for details
kubectl describe node <node-name>

# Check kubelet certificate expiration
openssl x509 -in /var/lib/kubelet/pki/kubelet.crt -noout -dates

# View kubelet logs
journalctl -u kubelet -n 100 --no-pager
```

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [CNCF Kubernetes Documentation](https://www.cncf.io/kubernetes/)
- [Kubernetes Production Patterns](https://learnkubernetes.io/)
