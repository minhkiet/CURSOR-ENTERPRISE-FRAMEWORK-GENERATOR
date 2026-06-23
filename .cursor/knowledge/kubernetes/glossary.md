---
title: "Kubernetes Glossary"
description: "Từ điển thuật ngữ Kubernetes toàn diện - các khái niệm, resources, components và terminology"
tags: ["kubernetes", "k8s", "glossary", "terminology", "vocabulary", "concepts"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Kubernetes Glossary

## Tổng quan (Overview)

Tài liệu này cung cấp một từ điển toàn diện về các thuật ngữ chuyên ngành Kubernetes, được thiết kế để giúp developers, DevOps engineers, và system architects hiểu rõ các khái niệm và terminology được sử dụng trong Kubernetes ecosystem. Mỗi entry bao gồm định nghĩa chi tiết, context sử dụng, và các ví dụ minh họa để đảm bảo comprehension sâu sắc.

Kubernetes là một container orchestration platform phức tạp với rất nhiều khái niệm và terminology riêng. Việc nắm vững các thuật ngữ này là essential cho việc effectively deploy, manage, và troubleshoot các applications trên Kubernetes. Từ điển này được tổ chức theo categories để dễ dàng reference và học tập.

## A

### Admission Controller

Admission Controller là một plugin intercepts requests tới Kubernetes API server sau khi authentication và authorization đã được thực hiện, nhưng trước khi objects được persisted vào etcd. Admission controllers được sử dụng để enforce custom policies, mutate objects với default values, hoặc validate complex constraints mà không thể handled bởi standard RBAC.

Có hai loại admission controllers: mutating controllers có thể modify objects trước khi chúng được persisted, trong khi validating controllers chỉ có thể accept hoặc reject requests. Các admission controllers phổ biến bao gồm NamespaceLifecycle, LimitRanger, ResourceQuota, ServiceAccount, PersistentVolumeLabel, và DefaultStorageClass. Admission controllers được enable/disable thông qua kube-apiserver flags.

### Affinity

Affinity là mechanism cho controlling pod placement behavior, bao gồm node affinity (chọn nodes dựa trên node labels), pod affinity (yêu cầu pods được placed gần nhau), và pod anti-affinity (yêu cầu pods được placed xa nhau). Affinity rules được express sử dụng label selectors với các operators như In, NotIn, Exists, và DoesNotExist.

```yaml
# Pod anti-affinity example
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: redis
              topologyKey: kubernetes.io/hostname
```

### Annotations

Annotations cung cấp một cách để attach arbitrary non-identifying metadata tới Kubernetes objects. Không giống như labels, annotations không được used for querying hoặc selecting objects, mà thay vào đó được sử dụng để store metadata như build information, contact information, hoặc configuration pointers.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  annotations:
    kubernetes.io/change-cause: "kubectl set image deployment/myapp app=myapp:v2"
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    contact: "team@example.com"
spec:
  containers:
    - name: app
      image: myapp:v1
```

### API Group

API Group là một tập hợp các related Kubernetes API resources. API groups giúp organize resources theo chức năng, ví dụ như "apps" group chứa các resources liên quan đến application management như Deployment, StatefulSet, và DaemonSet. API groups được identify bởi a group name và optional version.

## B

### Bloat

Bloat là tình trạng khi một container hoặc pod sử dụng nhiều disk space hơn cần thiết, thường do logging không được managed đúng cách, temporary files không được cleaned up, hoặc container image quá lớn. Bloat có thể dẫn đến disk pressure và node instability.

### Bucket

Trong context của Horizontal Pod Autoscaler (HPA), bucket được sử dụng trong metrics systems như Prometheus để aggregate và histogram data. Bucket boundaries define các ranges của values được counted trong histogram metric.

## C

### Capacity

Capacity refers to the total resources available on a node or cluster, bao gồm CPU cores, memory, và storage. Capacity được reported bởi kubelet và used by the scheduler để make placement decisions.

### Cert-manager

cert-manager là một Kubernetes operator tự động hóa việc provisioning và management của TLS certificates từ various sources bao gồm Let's Encrypt, HashiCorp Vault, và Venafi. Nó replaces manual certificate management với declarative configuration.

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
```

### Chaos Engineering

Chaos Engineering involves intentionally introducing failures vào production systems để test their resilience và identify weaknesses trước khi chúng gây ra outages. Tools như Chaos Mesh và Litmus cho phép practitioners define và execute chaos experiments trong Kubernetes.

### CIDR

Classless Inter-Domain Routing (CIDR) notation được sử dụng trong Kubernetes để define IP address ranges cho various purposes như pod networks (thường là 10.244.0.0/16), service cluster IP ranges (thường là 10.96.0.0/12), và node addresses. CIDR allows for efficient IP allocation và summarization.

### CKAD

Certified Kubernetes Application Developer (CKAD) là một certification program từ CNCF kiểm tra practical skills trong designing, building, và configuring cloud-native applications for Kubernetes. CKAD exam focuses on topics như core concepts, configuration, workloads, services, và observability.

### CKA

Certified Kubernetes Administrator (CKA) là một certification program từ CNCF validates skills trong bootstrapping, configuring, managing, và operating Kubernetes clusters. CKA exam covers cluster architecture, workload scheduling, services, storage, security, và troubleshooting.

### CNCF

Cloud Native Computing Foundation (CNCF) là một sub-foundation của Linux Foundation host các major open-source projects bao gồm Kubernetes, Prometheus, Grafana, Envoy, và hundreds of other cloud-native technologies. CNCF provides governance, marketing, và technical support cho its projects.

### CNI

Container Network Interface (CNI) là một specification và library standardizing network connectivity cho Linux containers. CNI plugins implement the specification để provide networking capabilities như IP address assignment và network isolation. Popular CNI implementations bao gồm Calico, Flannel, Cilium, và Weave.

### Container

Container là một lightweight, standalone, executable package chứa everything needed to run a piece of software, bao gồm code, runtime, system tools, libraries, và settings. Containers được isolated từ host system và other containers, cung cấp consistency across development, testing, và production environments.

### Container Runtime

Container Runtime là software responsible cho running containers trên a host system. Kubernetes supports multiple container runtimes through the Container Runtime Interface (CRI), bao gồm containerd, CRI-O, và Docker (through dockershim, deprecated in Kubernetes 1.24+).

### CRI

Container Runtime Interface (CRI) là một plugin interface cho phép kubelet sử dụng various container runtimes without hardcoding implementation details. CRI defines gRPC services cho managing containers và container images.

### CronJob

CronJob creates Jobs on a repeating schedule, tương tự như crontab trên Unix/Linux systems. CronJobs được sử dụng cho periodic tasks như backups, report generation, và cleanup operations.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
spec:
  schedule: "0 2 * * *"  # Run at 2 AM daily
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: backup-tool:v1
              command: ["/bin/sh", "-c", "./backup.sh"]
              env:
                - name: DB_HOST
                  value: "postgres.database.svc"
          restartPolicy: OnFailure
```

### CSI

Container Storage Interface (CSI) là một standard interface cho exposing block và file storage systems tới containerized workloads. CSI allows storage vendors to develop plugins once và deploy them across multiple container orchestration systems.

### Custom Controller

Custom Controller là một reconciliation loop watches one or more custom resources và takes actions để ensure desired state matches actual state. Controllers are the pattern used by Kubernetes itself và by many operators và add-ons.

### Custom Resource Definition (CRD)

CRD là một mechanism cho extending Kubernetes API bằng cách define new resource types. CRDs cho phép users tạo custom resources mà không cần adding another API server, enabling declarative management của custom application-specific logic.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.example.com
spec:
  group: example.com
  names:
    kind: Database
    plural: databases
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
```

## D

### DaemonSet

DaemonSet đảm bảo rằng một copy của một specific Pod chạy trên every node (hoặc subset of nodes selected by node selector). DaemonSets được sử dụng cho system daemons như node exporters, log collectors, và network plugins.

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
          image: fluentd:v1.16
          volumeMounts:
            - name: varlog
              mountPath: /var/log
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          effect: NoSchedule
```

### Dashboard

Kubernetes Dashboard là một web-based UI cho Kubernetes clusters, cho phép users manage và troubleshoot cluster resources, deploy applications, và monitor resource usage. Dashboard được deploy như một web application trong the cluster.

### Data Plane

Data plane là layer responsible cho forwarding network traffic giữa containers và services. Trong Kubernetes networking context, data plane được implemented by CNI plugins và kube-proxy.

### Deployment

Deployment là một high-level resource quản lý declarative updates cho application pods. Deployments provide capabilities cho updating, rolling back, và scaling Pods với zero downtime through rolling update strategies.

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
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
        - name: webapp
          image: myapp:v2.1.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
```

### Disruption

Disruption refers to voluntary interruption of pod workloads, bao gồm node drains cho maintenance, cluster upgrades, và pod evictions. PodDisruptionBudgets (PDBs) help manage disruption impacts.

### DNS

Kubernetes includes a DNS server (CoreDNS) that provides name resolution for services và pods. DNS records được automatically created when services are defined, allowing applications to locate other services using names instead of IP addresses.

Service DNS format: `my-svc.my-namespace.svc.cluster.local`
Pod DNS format: `pod-ip.namespace.pod.cluster.local` (với dots thay vì dashes trong IP)

### Downward API

Downward API cho phép containers consume information about themselves và about the cluster without accessing Kubernetes API directly. Information được exposed through environment variables hoặc mounted files.

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      image: myapp:v1
      env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
```

## E

### ectd

etcd là một distributed, consistent, key-value store được sử dụng as the backing store cho all Kubernetes cluster data. etcd uses Raft consensus algorithm để ensure strong consistency và high availability. In production, etcd clusters should have odd number of members (3, 5, 7) để achieve quorum.

### egress

Egress refers to outbound network traffic leaving the cluster hoặc a specific namespace. Network policies có thể được configured để control egress traffic, và egress gateways có thể be used để manage external connections.

### Endpoint

Endpoints (often plural) represents the actual IP addresses và ports của pods backing a service. Kubernetes automatically creates và maintains EndpointSlice objects containing these addresses, và services reference these endpoints for traffic routing.

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: my-service
subsets:
  - addresses:
      - ip: 10.244.1.5
        targetRef:
          kind: Pod
          name: myapp-pod-abc123
          namespace: default
    ports:
      - port: 8080
        protocol: TCP
```

### EndpointSlice

EndpointSlice là một API resource cung cấp a more scalable way để track network endpoints cho a service. EndpointSlices group endpoints together và are designed to scale as services have more pods.

### Eviction

Eviction là process của terminating one or more pods. Evictions có thể be initiated manually by users hoặc automatically by kubelet when resources are constrained (thresholds exceeded). Graceful eviction respects terminationGracePeriodSeconds.

### External Metric

External metrics come from systems outside of Kubernetes cluster, như Prometheus queries hoặc cloud provider metrics. HPA có thể scale based on external metrics using the custom metrics API.

## F

### Failover

Failover là process của switching workloads từ a failed component tới a healthy standby. In Kubernetes, failover có thể happen automatically through controllers và schedulers hoặc manually through operators.

### Finalizer

Finalizers are keys on resources that tell Kubernetes to wait until specific conditions are met before fully deleting the resource. Finalizers được sử dụng để implement cleanup logic và ensure proper resource deletion ordering.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
  finalizers:
    - example.com/cleanup-hook
```

### Floating IP

Floating IP là một IP address có thể be dynamically moved between nodes hoặc pods. In cloud environments, floating IPs được used với load balancers để provide stable external addresses.

### Foreground Cascading Deletion

Foreground cascading deletion là một deletion propagation policy trong đó owner object không được deleted cho đến khi all dependent objects được deleted first. This ensures proper cleanup ordering.

### Front-end

Front-end thường refers to the user-facing layer of an application architecture, như web servers hoặc API gateways. In Kubernetes context, front-ends are often exposed through Ingress controllers hoặc LoadBalancer services.

## G

### Garbage Collection

Garbage collection là process của cleaning up unused resources như completed pods, failed jobs, và orphaned resources. Kubernetes garbage collector sử dụng owner references để determine which resources to clean up.

### Gauge

Gauge là một Prometheus metric type represents a numerical value that can arbitrarily go up and down. Gauges được sử dụng cho metrics như current memory usage hoặc number of running pods.

### gitops

GitOps là một operational framework sử dụng Git as the single source of truth cho declarative infrastructure và applications. Changes được made through Git commits và automatically synchronized to the cluster through tools như ArgoCD hoặc Flux.

## H

### Hard Affinity

Hard affinity (requiredDuringSchedulingIgnoredDuringExecution) means that the scheduling constraint must be met for a pod to be scheduled. If no suitable node is found, the pod remains unscheduled.

### HPA

Horizontal Pod Autoscaler (HPA) automatically scales the number of pods in a Deployment, ReplicaSet, hoặc StatefulSet based on observed CPU utilization, memory usage, hoặc custom metrics.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### Helm

Helm là package manager cho Kubernetes, sử dụng charts để define, install, và upgrade complex Kubernetes applications. Helm templates allow for configurable deployments và versioned releases.

```bash
# Install a chart
helm install my-release bitnami/nginx

# Upgrade a release
helm upgrade my-release bitnami/nginx --set image.tag=v2.0

# List releases
helm list
```

### High Availability (HA)

High Availability refers to system design that ensures continued operation even when components fail. In Kubernetes, HA achieved through multiple control plane nodes, replicated etcd, multiple replicas of workloads, và anti-affinity rules.

### Horizontal Scaling

Horizontal scaling means adding more instances of a resource (like pods) rather than making individual instances larger. Kubernetes excels at horizontal scaling through Deployments và HPA.

### HostPath

HostPath volume mounts a file or directory from the host node's filesystem into the pod. HostPaths are commonly used for system daemons và should be used cautiously due to security implications.

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      image: myapp:v1
      volumeMounts:
        - name: host-time
          mountPath: /etc/localtime
          readOnly: true
  volumes:
    - name: host-time
      hostPath:
        path: /etc/localtime
        type: File
```

### Humanoid Controllers

Humanoid controllers là informal term cho controllers that require human input hoặc approval before taking actions, như controllers that wait for confirmation before performing destructive operations.

## I

### Image

Container image là một immutable, layered file system chứa all necessary files for a container to run. Images được specified in pod specs và pulled from container registries.

### ImagePullBackOff

ImagePullBackOff là một Kubernetes pod status indicating that the kubelet failed to pull the container image và is backing off before retrying. Common causes include invalid image names, authentication failures, và network issues.

### ImagePullPolicy

ImagePullPolicy determines when kubelet should pull container images. Options include Always (luôn luôn pull), IfNotPresent (chỉ pull nếu không có local image), và Never (không bao giờ pull).

### Ingress

Ingress manages external HTTP/HTTPS access to services in a cluster, providing load balancing, SSL termination, và name-based virtual hosting.

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
  tls:
    - hosts:
        - myapp.example.com
      secretName: myapp-tls
```

### Init Container

Init containers are specialized containers that run before app containers in a pod. They are commonly used for setup tasks như waiting for dependencies, database migrations, và configuration loading.

```yaml
apiVersion: v1
kind: Pod
spec:
  initContainers:
    - name: wait-for-db
      image: busybox:1.36
      command: ['sh', '-c', 'until nc -z postgres:5432; do sleep 1; done']
    - name: migrate-db
      image: myapp-migrations:v1
      command: ['node', 'migrate.js']
  containers:
    - name: app
      image: myapp:v1
```

### In-Tree

In-tree refers to code that is part of the core Kubernetes repository. In-tree plugins và providers are built directly into Kubernetes binaries, trong khi out-of-tree alternatives được deployed as separate components.

## J

### Job

Job creates one or more pods và ensures a specified number of them successfully terminate. Jobs are suitable for batch processing và one-time tasks.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-processor
spec:
  parallelism: 2
  completions: 5
  backoffLimit: 3
  template:
    spec:
      containers:
        - name: processor
          image: data-processor:v1
          command: ['./process.sh']
          env:
            - name: BATCH_ID
              valueFrom:
                fieldRef:
                  fieldPath: metadata.labels['batch-id']
      restartPolicy: OnFailure
```

## K

### kube-apiserver

kube-apiserver là front-end cho Kubernetes control plane, exposing the Kubernetes API và processing all operations. It validates và configures data for API objects và is the central management point for the cluster.

### kube-controller-manager

kube-controller-manager runs controller processes, each implementing a reconciliation loop that regulates the state of the cluster. Controllers include Node, Replication, Endpoint, Service Account, và Resource Quota controllers.

### kube-proxy

kube-proxy runs on each node, maintaining network rules that enable communication to pods from inside or outside the cluster. It translates Service VIP requests to backend pod IPs using iptables hoặc IPVS.

### kube-scheduler

kube-scheduler is the default scheduler, responsible for assigning newly created pods to nodes based on resource requirements, constraints, affinity rules, và other policies.

### kubelet

kubelet is an agent running on each node that registers the node with the cluster và ensures containers are running and healthy as specified in pod specifications.

### kubectl

kubectl is the command-line tool for interacting with Kubernetes clusters. It reads configuration from kubeconfig files và provides commands for creating, updating, deleting, và inspecting resources.

```bash
# Common kubectl commands
kubectl get pods -n production
kubectl describe pod myapp-abc123
kubectl logs myapp-abc123
kubectl exec -it myapp-abc123 -- /bin/sh
kubectl apply -f deployment.yaml
kubectl scale deployment myapp --replicas=5
```

### kubeconfig

kubeconfig is a file containing cluster credentials và configuration used by kubectl to authenticate và communicate with clusters. Multiple contexts allow switching between clusters.

## L

### Label

Labels are key/value pairs attached to objects for identifying and organizing resources. Unlike annotations, labels are intended for selection và grouping và are included in API queries và selectors.

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: webapp
    tier: frontend
    environment: production
    version: v2.1.0
spec:
  containers:
    - name: webapp
      image: myapp:v2.1.0
```

### Label Selector

Label selectors are used to filter objects based on their labels. Kubernetes supports two types: equality-based selectors (app=frontend) và set-based selectors (app in (frontend, api)).

```yaml
# Service selector
apiVersion: v1
kind: Service
spec:
  selector:
    app: webapp
    tier: frontend
---
# PodDisruptionBudget selector
apiVersion: policy/v1
kind: PodDisruptionBudget
spec:
  selector:
    matchLabels:
      app: webapp
```

### LimitRange

LimitRange sets default và maximum resource limits for containers in a namespace, preventing individual containers from consuming excessive resources.

```yaml
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
        memory: 64Mi
      max:
        cpu: "2"
        memory: 1Gi
      min:
        cpu: 50m
        memory: 32Mi
```

### LoadBalancer

LoadBalancer service creates an external load balancer in supported environments (cloud providers), providing a stable external IP for accessing the service.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
```

## M

### Manifest

Manifest là một YAML hoặc JSON file chứa Kubernetes resource specifications. Manifests được used with kubectl apply để deploy resources declarative.

### Metadata

Metadata provides identifying information about Kubernetes objects, bao gồm name, UID, namespace, labels, annotations, và creation timestamp. Metadata helps identify và manage resources.

### Metrics Server

Metrics Server là một cluster-wide aggregator of resource usage data, collecting metrics from kubelet và exposing them through Kubernetes API for use by HPA và kubectl top.

### Minikube

Minikube là một tool để run a single-node Kubernetes cluster locally for development và testing. It creates a VM running Kubernetes components và is useful for local development workflows.

### Multi-tenancy

Multi-tenancy refers to architecture where multiple tenants (users, teams, or organizations) share a single Kubernetes cluster while maintaining isolation. Kubernetes supports soft multi-tenancy through namespaces và RBAC, và hard multi-tenancy through dedicated clusters.

## N

### Name

Name is a client-provided string identifying a resource object within a namespace. Names must be unique within a namespace at any given time.

### Namespace

Namespace provides a mechanism for partitioning resources within a cluster. Namespaces enable resource isolation, access control, và resource quotas for different teams or projects.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    team: platform
```

### Network Policy

Network Policy là một specification defining how groups of pods are allowed to communicate with each other và other network endpoints. Default deny-all policies ensure least-privilege networking.

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

### Node

Node là một worker machine in Kubernetes, có thể be virtual hoặc physical. Each node contains services necessary to run pods, including kubelet, container runtime, và kube-proxy.

### NodePort

NodePort service exposes the service on each node's IP at a static port (30000-32767). This makes the service accessible from outside the cluster using `<NodeIP>:<NodePort>`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-nodeport
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080
```

### NodeSelector

NodeSelector là simplest way to constrain pods to nodes with specific labels. Pods are only scheduled on nodes whose labels match the selector.

```yaml
apiVersion: v1
kind: Pod
spec:
  nodeSelector:
    disktype: ssd
    region: us-west-2
  containers:
    - name: app
      image: myapp:v1
```

## O

### Operator

Operator là một pattern sử dụng custom controllers để encode domain-specific operational knowledge into Kubernetes. Operators automate complex operational tasks như backups, upgrades, và configuration management for stateful applications.

### OOMKilled

OOMKilled là pod status indicating that a container was terminated because it exceeded its memory limit (Out of Memory). Kubernetes attempts to restart OOMKilled containers based on restart policy.

### Out-of-Tree

Out-of-tree refers to plugins hoặc providers that exist outside the core Kubernetes repository. CNI, CSI, và device plugins are commonly implemented out-of-tree.

## P

### Pausing a Pod

Pausing a pod (setting replicas to 0) stops all containers while preserving the pod specification và resources. This is useful for debugging và troubleshooting.

### PDB

PodDisruptionBudget (PDB) specifies the minimum number or percentage of pods that must remain available during voluntary disruptions like node drains.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

### PersistentVolume (PV)

PersistentVolume là một piece of storage in the cluster that has been provisioned by an administrator hoặc dynamically provisioned using StorageClass. PVs have a lifecycle independent of any individual pod.

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
  nfs:
    server: nfs.example.com
    path: /exports/data
```

### PersistentVolumeClaim (PVC)

PersistentVolumeClaim là một request for storage by a user. PVCs consume PV resources và can request specific size, access modes, và storage class.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast
```

### Pod

Pod là smallest deployable unit in Kubernetes, representing a single instance of a running process. A pod may contain one or more containers that share network namespace và storage.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  containers:
    - name: app
      image: myapp:v1
      ports:
        - containerPort: 8080
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 256Mi
      readinessProbe:
        httpGet:
          path: /health/ready
          port: 8080
      livenessProbe:
        httpGet:
          path: /health/live
          port: 8080
```

### Pod Identity

Pod Identity refers to the way pods authenticate to other services và APIs. This includes service account tokens, projected volumes, và workload identity solutions for cloud providers.

### Pod Lifecycle

Pod lifecycle includes the stages a pod goes through: Pending, Running, Succeeded, Failed, và Unknown. Containers within pods have their own lifecycle with states: Waiting, Running, và Terminated.

### Pod Priority

Pod priority indicates the relative importance of a pod compared to other pods. Higher priority pods are scheduled before lower priority pods và can preempt lower priority pods when resources are constrained.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: critical-app
spec:
  priorityClassName: high-priority
  containers:
    - name: app
      image: critical:v1
```

### PodSecurityContext

PodSecurityContext defines pod-level security settings, including running as non-root user, configuring supplemental groups, và setting seccomp profiles.

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
```

### PriorityClass

PriorityClass defines a mapping from priority class name to integer value. Higher values indicate higher priority. System priority classes include system-cluster-critical và system-node-critical.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 100000
globalDefault: false
description: "High priority for critical production workloads"
```

### Probe

Probe là một periodic check performed by kubelet on a container to determine its health. Types include livenessProbe (is the container alive?), readinessProbe (can the container receive traffic?), và startupProbe (has the container started?).

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 20
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3
  successThreshold: 1

startupProbe:
  httpGet:
    path: /startup
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

### Projected Volume

Projected volume projects multiple volume sources into the same directory. Common projections include secrets, downwardAPI, configMap, và serviceAccountToken.

### Proportional Scaling

Proportional scaling is a feature of HPA that scales replicas proportionally based on pod rankings for workloads with multiple replicas receiving traffic.

### pull-through cache

Pull-through cache là một registry mirror that caches container images locally. This reduces image pull times và bandwidth usage, especially in multi-cluster environments.

## Q

### QoS Class

Quality of Service (QoS) class determines scheduling và eviction priority when resources are constrained. Classes include Guaranteed (highest), Burstable (medium), và BestEffort (lowest).

```yaml
# Guaranteed QoS - both requests and limits specified and equal
containers:
  - name: app
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "128Mi"
        cpu: "100m"

# Burstable QoS - requests less than limits
containers:
  - name: app
    resources:
      requests:
        memory: "64Mi"
        cpu: "50m"
      limits:
        memory: "256Mi"
        cpu: "500m"
```

### Quota

Resource quota defines aggregate resource constraints per namespace, limiting total CPU, memory, storage, và object counts.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
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

## R

### RBAC

Role-Based Access Control (RBAC) regulates access based on the roles of individual users within the enterprise. Kubernetes RBAC uses Role/ClusterRole và RoleBinding/ClusterRoleBinding objects.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
subjects:
  - kind: User
    name: jane
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### Reconciliation

Reconciliation là pattern used by Kubernetes controllers, where the controller continuously compares desired state (from the API) with actual state (in the cluster) và takes actions to reconcile differences.

### ReplicaSet

ReplicaSet ensures a specified number of pod replicas are running at any given time. While often managed by Deployments, ReplicaSets can also be used independently for simple use cases.

### ReplicationController

ReplicationController là legacy resource (replaced by ReplicaSet in apps/v1) that ensures a specified number of pod replicas are running. It is functionally similar to ReplicaSet but with less flexibility in selector syntax.

### Resource Manager

Resource Manager refers to the collection of components that manage cluster resources, including the scheduler, node controller, và resource quota controllers.

### Rolling Update

Rolling update là một deployment strategy that updates pods gradually with zero downtime by incrementally replacing old pods with new ones while maintaining availability.

### Root filesystem

Root filesystem refers to the container's root filesystem. readOnlyRootFilesystem security option prevents containers from writing to the root filesystem, improving security by enforcing immutable infrastructure.

## S

### Scheduler

Scheduler là component responsible for placing pods onto nodes based on resource requirements, constraints, affinity/anti-affinity rules, và other policies.

### Scope

Scope defines the validity boundary of a resource. Namespaced resources exist within a specific namespace, while cluster-scoped resources exist across all namespaces or no namespace at all.

### Seccomp

Secure Computing Mode (seccomp) is a Linux kernel feature that restricts the system calls available to a process. In Kubernetes, seccomp profiles can be applied to pods to limit container capabilities.

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    seccompProfile:
      type: RuntimeDefault  # Use container runtime's default profile
```

### Secret

Secret stores sensitive information like passwords, OAuth tokens, và SSH keys. Secrets are similar to ConfigMaps but designed to hold confidential data.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DB_PASSWORD: "supersecret"
  API_KEY: "key-12345"
```

### Security Context

Security context defines privilege và access control settings for a pod or container, including user ID, group ID, capabilities, và filesystem permissions.

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
  containers:
    - name: app
      image: myapp:v1
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
          add:
            - NET_BIND_SERVICE
```

### Selector

Selector is used to filter a set of objects based on their labels. Services use selectors to identify backing pods, và Deployments use selectors to identify managed pods.

### Semi-replicated

Semi-replicated refers to workloads where some components are replicated while others are not. This pattern is common in databases with primary-replica architectures.

### Service

Service là một abstract way to expose an application running on a set of pods as a network service. Services provide stable IP addresses và DNS names for accessing the pods.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
      name: http
```

### ServiceAccount

ServiceAccount provides an identity for processes running in a pod, allowing them to authenticate to the Kubernetes API server.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: production
automountServiceAccountToken: true
imagePullSecrets:
  - name: my-registry-secret
```

### Soft Affinity

Soft affinity (preferredDuringSchedulingIgnoredDuringExecution) indicates that the scheduler tries to satisfy the rule but may not guarantee it if other constraints prevent.

### Static Pod

Static Pods are managed directly by kubelet on a specific node, without the API server observing them. They are useful for running control plane components.

### StatefulSet

StatefulSet manages stateful applications, providing guarantees about ordering và uniqueness of pod deployment, scaling, và deletion.

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
      terminationGracePeriodSeconds: 30
      containers:
        - name: postgres
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: "fast"
        resources:
          requests:
            storage: 50Gi
```

### StorageClass

StorageClass provides a way for administrators to describe the "classes" of storage they offer, such as performance levels or backup policies.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

### Supplemental Groups

Supplemental groups are additional group IDs added to the container's primary group, useful for granting access to shared resources.

### System Metadata

System metadata refers to fields set by Kubernetes system components, such as UIDs, timestamps, resource versions, và generated labels/annotations.

## T

### Taint

Taint là một property of a node that repels pods from being scheduled onto it unless the pod has a matching toleration. Taints work together with tolerations to control pod placement.

```yaml
apiVersion: v1
kind: Node
metadata:
  name: gpu-node
spec:
  taints:
    - key: "nvidia.com/gpu"
      value: "present"
      effect: NoSchedule
```

### Toleration

Toleration allows a pod to be scheduled on nodes with matching taints, enabling specialized nodes to only accept workloads that explicitly request them.

```yaml
apiVersion: v1
kind: Pod
spec:
  tolerations:
    - key: "nvidia.com/gpu"
      operator: "Exists"
      effect: "NoSchedule"
  containers:
    - name: ml-workload
      image: ml-training:v1
```

### Topology Key

Topology key là một label key used to spread pods across failure domains like regions, zones, or nodes. topologyKey in pod affinity/anti-affinity và topology spread constraints determines how pods are distributed.

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 6
  template:
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: webapp
```

### Topology Manager

Topology Manager is a kubelet component (alpha in 1.16, beta in 1.18) that coordinates resource alignment for NUMA nodes, optimizing for performance-sensitive workloads.

### UID

UID is a unique identifier assigned by Kubernetes to every object, unique across the entire cluster lifetime. Unlike names, UIDs persist through updates.

### Update Strategy

Update strategy determines how deployments perform updates. RollingUpdate replaces pods gradually, while Recreate terminates all pods before creating new ones.

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

## V

### Version

Version refers to the API version of a resource type, following the pattern group/version (like apps/v1 hoặc networking.k8s.io/v1). Multiple versions may be served simultaneously, with the storage version being the authoritative version.

### Vertical Pod Autoscaler (VPA)

VPA automatically adjusts container resource requests based on actual usage patterns, recommending or automatically applying right-sized resource configurations.

```yaml
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
    updateMode: "Auto"
```

### Volume

Volume là một directory, possibly with data in it, accessible to containers in a pod. Kubernetes supports many volume types including emptyDir, hostPath, persistentVolumeClaim, configMap, secret, và more.

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      image: myapp:v1
      volumeMounts:
        - name: config
          mountPath: /app/config
  volumes:
    - name: config
      configMap:
        name: app-config
```

### Volume Snapshot

Volume snapshot allows creating a point-in-time copy of a persistent volume, useful for backups và disaster recovery.

## W

### WaitForFirstConsumer

WaitForFirstConsumer is a volume binding mode where PersistentVolumeClaim binding is deferred until a pod using the PVC is scheduled, ensuring optimal node selection for volume placement.

### Webhook

Webhook là một HTTP callback mechanism, used in Kubernetes for admission webhooks (custom validation/mutation) và external logging/monitoring integrations.

### Weighted Pod Affinity

Weighted pod affinity allows specifying preference weights for affinity rules, enabling the scheduler to make trade-offs between multiple affinity requirements.

### Workload

Workload is an application running on Kubernetes, typically managed by workload resources like Deployment, StatefulSet, hoặc DaemonSet.

### Workload Identity

Workload identity refers to the approach of granting cloud provider IAM roles directly to Kubernetes service accounts, enabling secure authentication without managing secrets.

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/concepts/)
- [Kubernetes Glossary](https://kubernetes.io/docs/reference/glossary/)
- [CNCF Cloud Native Glossary](https://glossary.cncf.io/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/)
