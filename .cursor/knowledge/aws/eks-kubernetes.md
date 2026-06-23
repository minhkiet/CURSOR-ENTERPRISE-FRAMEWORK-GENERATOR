---
title: "AWS EKS Kubernetes Orchestration"
description: "Hướng dẫn toàn diện về Amazon EKS clusters, node groups, managed node groups, Fargate profiles, cluster autoscaler và Helm deployment"
tags: ["aws", "eks", "kubernetes", "k8s", "node-groups", "fargate", "helm", "cluster-autoscaler"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# AWS EKS Kubernetes Orchestration

## Tổng Quan (Overview)

Amazon Elastic Kubernetes Service (EKS) là managed Kubernetes service giúp deploy, manage, và scale containerized applications trên AWS infrastructure một cách dễ dàng. EKS tự động handles Kubernetes control plane provisioning, scaling, và management, cho phép focus vào application workloads thay vì infrastructure.

Tài liệu này bao gồm comprehensive coverage của EKS architecture và operations, bao gồm cluster creation và configuration, managed node groups cho EC2-based workloads, Fargate profiles cho serverless containers, cluster autoscaler configuration, persistent storage với EBS và EFS, networking với VPC CNI, và Helm-based application deployment. Các best practices cho security, monitoring, và disaster recovery cũng được covered in detail.

EKS là lựa chọn phổ biến cho enterprises cần Kubernetes-native experience với AWS integration, hỗ trợ hybrid deployments, và compliance requirements. Với EKS, bạn có full control over Kubernetes configuration trong khi AWS manages the control plane với 99.95% availability SLA.

## Mục Đích (Purpose)

Mục đích chính của tài liệu này bao gồm:

1. **Cluster Architecture**: Hiểu EKS architecture và design patterns cho production
2. **Node Management**: Configure managed node groups, self-managed nodes, và Fargate profiles
3. **Networking**: Setup VPC CNI, ingress controllers, và service mesh
4. **Storage**: Implement persistent storage với EBS và EFS drivers
5. **Scaling**: Configure cluster autoscaler và HPA/VPA for application scaling
6. **Security**: Apply security best practices từ network policies đến pod security
7. **CI/CD**: Integrate EKS với CI/CD pipelines cho automated deployments

## Các Khái Niệm Chính (Key Concepts)

### 1. EKS Architecture

**Control Plane**: Managed by AWS, includes:
- API Server (kube-apiserver)
- etcd cluster
- Scheduler
- Controller Manager

**Data Plane**: Worker nodes where pods run:
- Managed Node Groups (EC2)
- Self-managed nodes
- Fargate

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   EKS Control Plane                  │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │    │
│  │  │API Server│ │  etcd  │ │Scheduler│ │Controller│  │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    VPC (10.0.0.0/16)                 │    │
│  │                                                       │    │
│  │  ┌─────────────┐    ┌─────────────┐                 │    │
│  │  │ Private Subnet│    │Private Subnet│                │    │
│  │  │  (10.0.1.0/24)│    │ (10.0.2.0/24)│                │    │
│  │  │              │    │              │                 │    │
│  │  │ ┌──────────┐│    │ ┌──────────┐│                 │    │
│  │  │ │ Node 1   ││    │ │ Node 2   ││                 │    │
│  │  │ │ (Managed) ││    │ │(Managed) ││                 │    │
│  │  │ └──────────┘│    │ └──────────┘│                 │    │
│  │  │ ┌──────────┐│    │ ┌──────────┐│                 │    │
│  │  │ │ Pod       ││    │ │ Pod       ││                 │    │
│  │  │ │ ┌──────┐  ││    │ │ ┌──────┐  ││                 │    │
│  │  │ │ │nginx │  ││    │ │ │app   │  ││                 │    │
│  │  │ │ └──────┘  ││    │ │ └──────┘  ││                 │    │
│  │  │ └──────────┘│    │ └──────────┘│                 │    │
│  │  └─────────────┘    └─────────────┘                 │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2. Managed Node Groups

Managed Node Groups tự động provision và manages EC2 instances cho EKS nodes.

```yaml
# CloudFormation for EKS Cluster
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  EKSCluster:
    Type: AWS::EKS::Cluster
    Properties:
      Name: production-cluster
      Version: "1.29"
      RoleArn: !GetAtt EKSRole.Arn
      ResourcesVpcConfig:
        SubnetIds:
          - !Ref PrivateSubnet1
          - !Ref PrivateSubnet2
          - !Ref PrivateSubnet3
        EndpointPrivateAccess: true
        EndpointPublicAccess: true
        PublicAccessCidrs:
          - "0.0.0.0/0"
      Logging:
        ClusterLogging:
          EnabledTypes:
            - EKS - API Server
            - EKS - Audit
            - EKS - Authenticator
            - EKS - ControllerManager
            - EKS - Scheduler
      EncryptionConfig:
        - Resources:
            - secrets
          Provider:
            KeyArn: !GetAtt KMSKey.Arn

  EKSRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: eks-cluster-role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: eks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
        - arn:aws:iam::aws:policy/AmazonEKSVPCResourceController

  KMSKey:
    Type: AWS::KMS::Key
    Properties:
      Description: EKS secrets encryption key
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: kms:*
            Resource: '*'
          - Sid: Allow EKS to use key
            Effect: Allow
            Principal:
              Service: eks.amazonaws.com
            Action:
              - kms:Encrypt
              - kms:Decrypt
              - kms:CreateGrant
            Resource: '*'
            Condition:
              StringEquals:
                kms:ViaService: !Sub 'eks.${AWS::Region}.amazonaws.com'

  ManagedNodeGroup:
    Type: AWS::EKS::Nodegroup
    Properties:
      ClusterName: !Ref EKSCluster
      NodegroupName: production-nodes
      scalingConfig:
        minSize: 2
        maxSize: 10
        desiredSize: 3
      amiType: BOTTLEROCKET_x86_64
      capacityType: ON_DEMAND
      instanceTypes:
        - m5.xlarge
      subnets:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
        - !Ref PrivateSubnet3
      nodeRole: !GetAtt NodeInstanceRole.Arn
      labels:
        workload-type: general
        environment: production
      taints:
        - key: dedicated
          value: gpu
          effect: NO_SCHEDULE
      updateConfig:
        maxUnavailable: 1
      diskSize: 100
      remoteAccess:
        ec2SshKey: !Ref SSHSecurityGroup
        sourceSecurityGroups:
          - !Ref WorkerNodeSecurityGroup

  NodeInstanceRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: eks-node-role
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
        - arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy

  NodeInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      InstanceProfileName: eks-node-profile
      Roles:
        - !Ref NodeInstanceRole

  WorkerNodeSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for worker nodes
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 1025
          ToPort: 65535
          SourceSecurityGroupId: !Ref EKSClusterSecurityGroup
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          SourceSecurityGroupId: !Ref EKSClusterSecurityGroup
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0

  EKSClusterSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security group for EKS cluster
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
```

### 3. Fargate Profiles

Fargate Profiles cho phép run Kubernetes pods on Fargate without managing EC2 instances.

```yaml
# Fargate Profile for application workloads
FargateProfile:
  Type: AWS::EKS::FargateProfile
  Properties:
    FargateProfileName: production-app-profile
    ClusterName: !Ref EKSCluster
    PodExecutionRoleArn: !GetAtt FargatePodExecutionRole.Arn
    Subnets:
      - !Ref PrivateSubnet1
      - !Ref PrivateSubnet2
      - !Ref PrivateSubnet3
    Selectors:
      - Namespace: production
        Labels:
          workload-type: application
      - Namespace: staging
        Labels:
          environment: staging
      - Namespace: kube-system
        Labels:
          k8s-app: kube-dns

FargatePodExecutionRole:
  Type: AWS::IAM::Role
  Properties:
    RoleName: eks-fargate-pod-execution-role
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: eks-fargate-pods.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy
```

```bash
# Create Fargate profile via AWS CLI
aws eks create-fargate-profile \
  --cluster-name production-cluster \
  --fargate-profile-name web-app-profile \
  --pod-execution-role-arn arn:aws:iam::123456789012:role/eks-fargate-pod-execution-role \
  --selectors '[{"namespace": "web-app", "labels": {"environment": "production"}}]' \
  --subnets subnet-abc123 subnet-def456 subnet-ghi789

# List Fargate profiles
aws eks list-fargate-profiles --cluster-name production-cluster

# Delete Fargate profile
aws eks delete-fargate-profile \
  --cluster-name production-cluster \
  --fargate-profile-name web-app-profile
```

### 4. Cluster Autoscaler

```yaml
# Cluster Autoscaler deployment
apiVersion: v1
kind: ServiceAccount
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/cluster-autoscaler-role
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-autoscaler
rules:
  - apiGroups: [""]
    resources: ["events", "endpoints"]
    verbs: ["create", "patch"]
  - apiGroups: [""]
    resources: ["pods/eviction"]
    verbs: ["create"]
  - apiGroups: [""]
    resources: ["pods/status"]
    verbs: ["update"]
  - apiGroups: [""]
    resources: ["events"]
    verbs: ["list", "watch"]
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list", "watch", "update", "patch"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["services"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["extensions"]
    resources: ["replicasets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["replicasets", "deployments"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-autoscaler
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-autoscaler
subjects:
  - kind: ServiceAccount
    name: cluster-autoscaler
    namespace: kube-system
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-autoscaler
  namespace: kube-system
data:
  AWS_REGION: "us-east-1"
  AUTO_SCALER_VERSION: "1.29.0"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    app: cluster-autoscaler
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
      annotations:
        prometheus.io/scrape: "true"
    spec:
      serviceAccountName: cluster-autoscaler
      containers:
        - image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.29.0
          name: cluster-autoscaler
          resources:
            limits:
              cpu: 100m
              memory: 512Mi
            requests:
              cpu: 100m
              memory: 512Mi
          command:
            - /cluster-autoscaler
          args:
            - --cloud-provider=aws
            - --cluster-name=production-cluster
            - --namespace=kube-system
            - --scale-down-delay-after-add=3m
            - --scale-down-unneeded-time=5m
            - --scale-down-utilization-threshold=0.5
            - --scan-interval=30s
            - --skip-nodes-with-local-storage=false
            - --skip-nodes-with-system-pods=false
            - --expander=price
            - --balance-similar-node-groups
          env:
            - name: AWS_REGION
              value: us-east-1
          volumeMounts:
            - name: ssl-certs
              mountPath: /etc/ssl/certs/ca-certificates.crt
              readOnly: true
      volumes:
        - name: ssl-certs
          hostPath:
            path: /etc/ssl/certs/ca-certificates.crt
```

### 5. VPC CNI Configuration

```yaml
# VPC CNI addon configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-node
  namespace: kube-system
data:
  ENABLE_WARM_IP_TARGET: "true"
  WARM_IP_TARGET: "5"
  MINIMUM_IP_TARGET: "3"
  AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CIDR: "192.168.0.0/16"
  AWS_VPC_K8S_CNI_EXTERNAL_SNAT: "false"
  AWS_VPC_K8S_CNI_LOGLEVEL: "DEBUG"
  AWS_VPC_K8S_CNI_VETHPROXY: "false"
---
# Enable prefix delegation for higher pod density
apiVersion: v1
kind: ConfigMap
metadata:
  name: amazon-vpc-cni
  namespace: kube-system
data:
  enable-windows-ipam: "false"
  enable-network-policy-controller: "false"
  enable-big-pod-termination: "true"
  warm-prefix-target: "1"
  minimum-ip-target: "3"
  warm-ip-target: "3"
  ENABLE_IPv6: "false"
```

```bash
# Enable prefix delegation on existing node group
aws eks update-nodegroup-version \
  --cluster-name production-cluster \
  --nodegroup-name production-nodes \
  --resolve-aliases

# Configure node group with prefix delegation
aws eks create-nodegroup \
  --cluster-name production-cluster \
  --nodegroup-name optimized-nodes \
  --subnets subnet-abc123 subnet-def456 \
  --instance-types t3.medium \
  --node-role arn:aws:iam::123456789012:role/eks-node-role \
  --ami-type AL2_x86_64 \
  --scaling-config minSize=2,maxSize=10,desiredSize=3 \
  --remote-access ec2SshKey=my-key \
  --kubernetes-labels '{"eks.amazonaws.com/nodegroup-version":"v1"}'
```

## Best Practices

### 1. Security Best Practices

**Pod Security Standards:**

```yaml
# Pod Security Standards via Pod Security Policy / admission
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted-psp
  annotations:
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: 'runtime/default'
    apparmor.security.beta.kubernetes.io/allowedProfileNames: 'runtime/default'
    seccomp.security.alpha.kubernetes.io/defaultProfileName:  'runtime/default'
    apparmor.security.beta.kubernetes.io/defaultProfileName:  'runtime/default'
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: true
```

**Network Policies:**

```yaml
# Default deny all traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
# Allow only necessary traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
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
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: database
      ports:
        - protocol: TCP
          port: 5432
```

**IRSA (IAM Role for Service Accounts):**

```bash
# Create IAM role for service account
aws iam create-role \
  --role-name eks-app-service-account \
  --assume-role-policy-document file://trust-policy.json

# Trust policy for IRSA
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53DE1B716D3041E:sub": "system:serviceaccount:production:app-service-account"
        }
      }
    }
  ]
}
EOF

# Create service account with IRSA annotation
kubectl create serviceaccount app-service-account \
  --namespace production \
  --annotation iam.amazonaws.com/role=arn:aws:iam::123456789012:role/eks-app-service-account
```

```yaml
# Service account with IRSA
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/eks-app-service-account
```

### 2. Persistent Storage với EBS CSI

```yaml
# EBS CSI Driver installation
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ebs-csi-controller-sa
  namespace: kube-system
  labels:
    app: ebs-csi-controller
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ebs-csi-node-sa
  namespace: kube-system
  labels:
    app: ebs-csi-node
---
# StorageClass for GP3
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  csi.storage.k8s.io/pv/name: ${pvc.name}
  csi.storage.k8s.io/pvc/namespace: ${pvc.namespace}
  encrypted: "true"
  kmsKey: arn:aws:kms:us-east-1:123456789012:key/mrk-1234abcd5678efgh9012
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Retain
---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
  namespace: production
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: gp3
  resources:
    requests:
      storage: 50Gi
---
# Pod using PVC
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
  namespace: production
spec:
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - name: app-storage
          mountPath: /data
  volumes:
    - name: app-storage
      persistentVolumeClaim:
        claimName: app-storage
```

### 3. Horizontal Pod Autoscaler

```yaml
# HPA với custom metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 20
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
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
        - type: Pods
          value: 2
          periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

## Common Patterns

### Pattern 1: GitOps với ArgoCD

```yaml
# ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-web-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: production
  source:
    repoURL: https://github.com/org/k8s-manifests.git
    targetRevision: main
    path: production/web-app
    kustomize:
      images:
        - nginx=123456789.dkr.ecr.us-east-1.amazonaws.com/web:v1.2.3
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```

### Pattern 2: Helm Deployment

```bash
# Add Helm repos
helm repo add stable https://charts.helm.sh/stable
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add prometheus https://prometheus-community.github.io/helm-charts
helm repo update

# Install ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --values ingress-nginx-values.yaml

# ingress-nginx-values.yaml
cat > ingress-nginx-values.yaml << 'EOF'
controller:
  replicaCount: 3
  service:
    type: ClusterIP
    annotations:
      service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
      service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
  resources:
    requests:
      cpu: 100m
      memory: 90Mi
    limits:
      cpu: 500m
      memory: 256Mi
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
  config:
    use-forwarded-headers: "true"
    compute-full-forwarded-for: "true"
    use-proxy-protocol: "false"
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "10254"
    prometheus.io/path: /metrics
  podLabels:
    app: ingress-nginx
EOF

# Install Prometheus Stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --values prometheus-values.yaml

# prometheus-values.yaml
cat > prometheus-values.yaml << 'EOF'
prometheus:
  prometheusSpec:
    replicas: 2
    retention: 15d
    retentionSize: 50GiB
    resources:
      requests:
        cpu: 500m
        memory: 2Gi
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3
          resources:
            requests:
              storage: 100Gi
    ruleSelector: true
    ruleNamespaceSelector: {}
    serviceMonitorSelector: {}
    podMonitorSelector: {}
  ingress:
    enabled: true
    annotations:
      kubernetes.io/ingress.class: nginx
    hosts:
      - prometheus.example.com
    tls:
      - hosts:
          - prometheus.example.com

alertmanager:
  alertmanagerSpec:
    replicas: 3
    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3
          resources:
            requests:
              storage: 10Gi
EOF
```

### Pattern 3: Multi-Cluster Management

```bash
# Create EKS cluster using eksctl
cat > cluster-config.yaml << 'EOF'
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: production-cluster
  region: us-east-1
  version: "1.29"
  tags:
    environment: production
    team: platform

iam:
  withOIDC: true
  serviceAccounts:
    - metadata:
        name: cluster-autoscaler
        namespace: kube-system
      wellKnownPolicies:
        clusterAutoscaler: true
    - metadata:
        name: external-dns
        namespace: kube-system
      wellKnownPolicies:
        externalDNS: true
    - metadata:
        name: metrics-server
        namespace: kube-system
      wellKnownPolicies:
        metricsServer: true

vpc:
  cidr: 10.0.0.0/16
  nat:
    gateway: HighlyAvailable
  clusterEndpoints:
    publicAccess: true
    privateAccess: true
  sharedNodeSecurityGroupRules: true

managedNodeGroups:
  - name: general
    instanceType: m5.xlarge
    desiredCapacity: 3
    minSize: 2
    maxSize: 10
    volumeSize: 100
    volumeType: gp3
    privateNetworking: true
    labels:
      workload-type: general
    tags:
      environment: production
    iam:
      withAddonPolicies:
        imageBuilder: true
        cloudWatch: true
        ebs: true
        fsx: true
        efs: true
        certManager: true
        autoScaler: true

  - name: memory-optimized
    instanceType: r5.xlarge
    desiredCapacity: 2
    minSize: 1
    maxSize: 5
    privateNetworking: true
    labels:
      workload-type: memory-intensive
    taints:
      - key: workload-type
        value: memory-intensive
        effect: NoSchedule
    iam:
      withAddonPolicies:
        cloudWatch: true
        ebs: true

fargateProfiles:
  - name: production-app
    selectors:
      - namespace: production
        labels:
          workload-type: application
      - namespace: staging
        labels:
          environment: staging
    subnets:
      - subnet-abc123
      - subnet-def456

addons:
  - name: vpc-cni
    version: latest
    configurationValues: |-
      enableNetworkPolicyController: "true"
  - name: coredns
    version: latest
  - name: kube-proxy
    version: latest
  - name: aws-ebs-csi-driver
    version: latest
    serviceAccountRoleARN: arn:aws:iam::123456789012:role/ebs-csi-driver-role
  - name: aws-load-balancer-controller
    version: latest
    serviceAccountRoleARN: arn:aws:iam::123456789012:role/alb-ingress-controller
EOF

# Create cluster
eksctl create cluster -f cluster-config.yaml

# Update cluster
eksctl upgrade cluster -f cluster-config.yaml --approve

# Delete cluster
eksctl delete cluster -f cluster-config.yaml
```

## Troubleshooting

### Common Issues và Solutions

**1. Node Not Joining Cluster**

```bash
# Check node status
kubectl get nodes -o wide

# Describe node for details
kubectl describe node <node-name>

# Check system pods in kube-system
kubectl get pods -n kube-system -o wide

# View kubelet logs
kubectl logs -n kube-system <kubelet-pod-name>

# SSH to node and check
# On the node:
journalctl -u kubelet -f
cat /var/log/cloud-init-output.log
aws ssm start-session --target <instance-id>

# Common issues:
# - Security group rules missing
# - Node role IAM permissions incorrect
# - kubelet not starting due to configuration error
```

**2. Pods Pending Due to Resource Constraints**

```bash
# Check pod status
kubectl get pods -o wide -A | grep Pending

# Check resource requests vs available
kubectl describe node | grep -A 5 "Allocated resources"

# Check ResourceQuotas
kubectl get resourcequota -A

# Check LimitRanges
kubectl get limitrange -A

# Debug with events
kubectl get events --sort-by='.lastTimestamp' | tail -50

# Increase node group size
aws eks update-nodegroup-config \
  --cluster-name production-cluster \
  --nodegroup-name production-nodes \
  --scaling-config minSize=3,maxSize=15,desiredSize=5
```

**3. Storage Volume Issues**

```bash
# Check PVC status
kubectl get pvc -A

# Describe PVC for details
kubectl describe pvc <pvc-name> -n <namespace>

# Check EBS volume status
aws ec2 describe-volumes \
  --filters "Name=tag:KubernetesCluster,Values=production-cluster"

# Check CSI driver pods
kubectl get pods -n kube-system | grep csi

# Describe CSI driver logs
kubectl logs -n kube-system ebs-csi-controller-0 -c csi-provisioner

# Common EBS issues:
# - Volume stuck in attaching/detaching
# - Wrong availability zone
# - Insufficient permissions
# - Encryption key access denied
```

**4. Networking Issues**

```bash
# Check CoreDNS status
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Test DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default

# Check VPC CNI logs
kubectl logs -n kube-system -l k8s-app=aws-node --tail=100

# Check security group rules
kubectl describe node <node-name> | grep -A 10 "Security Groups"

# Test pod-to-pod connectivity
kubectl exec -it <source-pod> -n <namespace> -- wget -qO- http://<target-pod-ip>

# Check network policies
kubectl get networkpolicies -A
```

## Examples

### Example 1: Production EKS Setup với Terraform

```terraform
# Terraform configuration for EKS
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "eks-vpc"
  }
}

# Subnets
resource "aws_subnet" "private" {
  count = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 4, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "eks-private-subnet-${count.index + 1}"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

resource "aws_subnet" "public" {
  count = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 4, count.index + 3)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "eks-public-subnet-${count.index + 1}"
    "kubernetes.io/role/elb" = "1"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "eks-igw"
  }
}

# NAT Gateways
resource "aws_eip" "nat" {
  count = 3
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  count = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
}

# Route Tables
resource "aws_route_table" "private" {
  count = 3
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = {
    Name = "eks-private-rt-${count.index + 1}"
  }
}

resource "aws_route_table_association" "private" {
  count = 3
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# EKS Cluster
resource "aws_eks_cluster" "main" {
  name     = "production-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.29"

  vpc_config {
    subnet_ids              = concat(aws_subnet.private[*].id, aws_subnet.public[*].id)
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }

  encryption_config {
    provider {
      key_arn = aws_kms_key.eks.arn
    }
    resources = ["secrets"]
  }

  kubernetes_network_config {
    service_ipv6_cidr = false
    ip_family         = "ipv4"
  }

  logging {
    cluster_logging {
      enabled_types = [
        "api",
        "audit",
        "authenticator",
        "controllerManager",
        "scheduler"
      ]
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
    aws_iam_role_policy_attachment.eks_vpc_resource_controller
  ]
}

# KMS Key for secrets encryption
resource "aws_kms_key" "eks" {
  description = "EKS Cluster Secrets Encryption Key"
  deletion_window_in_days = 10
  enable_key_rotation = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "Enable IAM User Permissions"
        Effect = Allow
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = "kms:*"
        Resource = "*"
      },
      {
        Sid = "Allow EKS to use key"
        Effect = Allow
        Principal = {
          Service = "eks.amazonaws.com"
        }
        Action = ["kms:Encrypt", "kms:Decrypt", "kms:CreateGrant"]
        Resource = "*"
        Condition = {
          StringEquals = {
            "kms:ViaService" = "eks.${data.aws_region.current.name}.amazonaws.com"
          }
        }
      }
    ]
  })
}

# IAM Role for EKS Cluster
resource "aws_iam_role" "eks_cluster" {
  name = "eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

resource "aws_iam_role_policy_attachment" "eks_vpc_resource_controller" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.eks_cluster.name
}

# IAM Role for EKS Node Group
resource "aws_iam_role" "eks_nodes" {
  name = "eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_worker_node" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_cni" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks_nodes.name
}

resource "aws_iam_role_policy_attachment" "eks_container_registry" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks_nodes.name
}

# EKS Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "production-nodes"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = aws_subnet.private[*].id
  instance_types  = ["m5.xlarge"]

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 2
  }

  disk_size = 100

  update_config {
    max_unavailable = 1
  }

  label = {
    "environment" = "production"
    "workload-type" = "general"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node,
    aws_iam_role_policy_attachment.eks_cni,
    aws_iam_role_policy_attachment.eks_container_registry
  ]
}

# Security Groups
resource "aws_security_group" "eks_cluster" {
  name        = "eks-cluster-sg"
  description = "Security group for EKS cluster"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Worker nodes to API server"
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "eks-cluster-sg"
  }
}

resource "aws_security_group" "eks_nodes" {
  name        = "eks-nodes-sg"
  description = "Security group for EKS nodes"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Cluster to nodes"
    protocol    = "tcp"
    from_port   = 1025
    to_port     = 65535
    cidr_blocks = ["10.0.0.0/16"]
  }

  ingress {
    description = "API server to nodes"
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "eks-nodes-sg"
  }
}

# OIDC Provider for IRSA
resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

data "tls_certificate" "eks" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

# Update kubeconfig
resource "null_resource" "update_kubeconfig" {
  provisioner "local-exec" {
    command = "aws eks update-kubeconfig --name ${aws_eks_cluster.main.name} --region us-east-1"
  }

  depends_on = [aws_eks_cluster.main]
}
```

## References

### Official Documentation
- [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/)
- [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [eksctl Documentation](https://eksctl.io/)
- [AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)
- [VPC CNI Documentation](https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html)

### Tools
- [eksctl](https://eksctl.io/)
- [kubectl](https://kubernetes.io/docs/reference/kubectl/)
- [Helm](https://helm.sh/)
- [Kustomize](https://kustomize.io/)
- [ArgoCD](https://argoproj.github.io/cd/)
- [Flux](https://fluxcd.io/)

### Kubernetes Documentation
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.29/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
