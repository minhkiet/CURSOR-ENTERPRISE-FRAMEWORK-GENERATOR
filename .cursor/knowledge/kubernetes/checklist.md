# Kubernetes Knowledge Base - Checklist

## Tổng quan

Document này cung cấp checklist toàn diện cho việc đánh giá và kiểm tra Kubernetes deployments trong Cursor Enterprise Framework.

## 1. Deployment Checklist

### 1.1 Basic Configuration

- [ ] Deployment uses appropriate replicas count for HA
- [ ] Deployment selector correctly matches pod labels
- [ ] Rolling update strategy configured appropriately
- [ ] minReadySeconds set for stability verification
- [ ] revisionHistoryLimit configured for rollback capability

### 1.2 Resource Management

- [ ] Resource requests and limits set for all containers
- [ ] Requests are reasonable for scheduling
- [ ] Limits prevent resource monopolization
- [ ] QoS class is appropriate (Guaranteed, Burstable, BestEffort)
- [ ] LimitRange exists in namespace for defaults

### 1.3 Container Configuration

- [ ] Image tag is specific (not :latest)
- [ ] imagePullPolicy is explicitly set
- [ ] Container port is correctly configured
- [ ] Environment variables are properly set
- [ ] Non-root user is used
- [ ] readOnlyRootFilesystem is true when possible

### 1.4 Health Checks

- [ ] startupProbe configured for slow-starting applications
- [ ] livenessProbe configured to detect failures
- [ ] readinessProbe configured to control traffic routing
- [ ] Probe paths/commands are correct
- [ ] Probe timing (initialDelaySeconds, periodSeconds) is appropriate
- [ ] Probe failure thresholds are reasonable

## 2. Service Checklist

### 2.1 Service Configuration

- [ ] Service selector correctly targets pods
- [ ] Service type is appropriate (ClusterIP, NodePort, LoadBalancer)
- [ ] Port mappings are correct
- [ ] Service name follows naming conventions
- [ ] Service has appropriate labels

### 2.2 Service Discovery

- [ ] Services use DNS names for internal communication
- [ ] Headless service created for StatefulSet when needed
- [ ] ExternalName service configured correctly if used
- [ ] Ingress configured for external HTTP/HTTPS access

### 2.3 Load Balancing

- [ ] LoadBalancer service configured for cloud integration
- [ ] External traffic policy is appropriate
- [ ] Session affinity configured if needed

## 3. Networking Checklist

### 3.1 Network Policies

- [ ] Default deny-all policy exists
- [ ] Required allow rules are defined
- [ ] Namespace isolation is enforced
- [ ] Ingress/egress rules are specific

### 3.2 DNS Configuration

- [ ] Cluster DNS is functional
- [ ] Services are reachable by DNS name
- [ ] Headless services work correctly
- [ ] External name resolution works

### 3.3 Ingress Configuration

- [ ] Ingress controller is deployed
- [ ] Ingress class is specified
- [ ] TLS is configured
- [ ] Host rules are correct
- [ ] Path routing is configured properly

## 4. Security Checklist

### 4.1 Pod Security

- [ ] PodSecurityPolicy/PodSecurityStandard applied
- [ ] Security context is configured appropriately
- [ ] Non-root user is enforced
- [ ] Privilege escalation is disabled
- [ ] Capabilities are dropped
- [ ] Root filesystem is read-only when possible

### 4.2 Secrets Management

- [ ] Secrets used instead of ConfigMaps for sensitive data
- [ ] External secrets management integrated (Vault, AWS, GCP)
- [ ] Secrets are not in environment variables (use volume mounts)
- [ ] RBAC controls secrets access

### 4.3 Network Security

- [ ] Network policies restrict traffic
- [ ] Pod-to-pod communication is controlled
- [ ] External access is restricted
- [ ] TLS is used for sensitive communications

### 4.4 RBAC

- [ ] ServiceAccounts are used for workloads
- [ ] Roles/RoleBindings are scoped to minimal permissions
- [ ] ClusterRoles/ClusterRoleBindings are justified
- [ ] No overly permissive bindings

## 5. Storage Checklist

### 5.1 Persistent Storage

- [ ] PersistentVolumeClaim is configured correctly
- [ ] StorageClass is appropriate
- [ ] Access modes are correct
- [ ] Storage is backed up

### 5.2 Volume Configuration

- [ ] emptyDir volumes have appropriate size limits
- [ ] tmpfs used for sensitive data
- [ ] hostPath is not used inappropriately
- [ ] Volume mounts are read-only when possible

### 5.3 Data Management

- [ ] StatefulSets use stable network IDs
- [ ] Data is replicated for HA
- [ ] Backup strategy is in place
- [ ] Volume expansion is configured

## 6. High Availability Checklist

### 6.1 Pod Distribution

- [ ] PodAntiAffinity prevents co-location
- [ ] TopologySpreadConstraints configured
- [ ] Pods spread across availability zones
- [ ] Multiple replicas configured

### 6.2 Disruption Protection

- [ ] PodDisruptionBudget is configured
- [ ] PDB allows required availability
- [ ] Node drains respect PDBs

### 6.3 Application HA

- [ ] Application handles graceful shutdown
- [ ] Database connections are pooled
- [ ] Caching prevents thundering herd
- [ ] Health checks prevent traffic to failed pods

## 7. Monitoring Checklist

### 7.1 Metrics

- [ ] Prometheus metrics endpoint exposed
- [ ] Custom metrics are defined
- [ ] Application metrics are informative
- [ ] Resource metrics are collected

### 7.2 Logging

- [ ] Logs are written to stdout/stderr
- [ ] Logs are structured (JSON preferred)
- [ ] Log level is configurable
- [ ] Logs include relevant metadata
- [ ] Log aggregation is configured

### 7.3 Tracing

- [ ] Distributed tracing is integrated
- [ ] Trace context is propagated
- [ ] Span IDs are included in logs

### 7.4 Alerting

- [ ] Critical alerts are configured
- [ ] Alert thresholds are appropriate
- [ ] Alert routing is configured
- [ ] Alert notifications are sent

## 8. Configuration Management Checklist

### 8.1 ConfigMaps

- [ ] Configuration is externalized
- [ ] ConfigMaps are properly namespaced
- [ ] ConfigMaps are version controlled
- [ ] ConfigMaps are updated atomically

### 8.2 Environment Variables

- [ ] Environment variables are validated
- [ ] Defaults are set appropriately
- [ ] Environment-specific configs exist
- [ ] No hardcoded sensitive values

### 8.3 Application Configuration

- [ ] Hot reload is supported when needed
- [ ] Configuration changes are graceful
- [ ] Old config is cleaned up

## 9. Lifecycle Management Checklist

### 9.1 Updates and Rollbacks

- [ ] Rolling update strategy is configured
- [ ] maxSurge and maxUnavailable are appropriate
- [ ] Rollback procedure is documented
- [ ] revisionHistoryLimit is set
- [ ] Updates are tested before production

### 9.2 Scaling

- [ ] HPA is configured when appropriate
- [ ] VPA is considered for resource optimization
- [ ] CA is configured for node scaling
- [ ] Scaling thresholds are appropriate

### 9.3 Cleanup

- [ ] Old replicasets are cleaned up
- [ ] Failed pods are investigated
- [ ] Orphaned resources are removed
- [ ] Image garbage collection is configured

## 10. CI/CD Checklist

### 10.1 Build Process

- [ ] Images are built from Dockerfile
- [ ] Multi-stage builds are used
- [ ] Images are scanned for vulnerabilities
- [ ] Images are tagged with version/commit

### 10.2 Deployment Process

- [ ] Deployment is automated
- [ ] Deployment includes validation
- [ ] Rollback capability exists
- [ ] Canary deployments are considered

### 10.3 GitOps

- [ ] Manifests are in Git
- [ ] ArgoCD/Flux is configured
- [ ] Sync policies are appropriate
- [ ] Drift detection is enabled

## 11. Disaster Recovery Checklist

### 11.1 Backup

- [ ] etcd is backed up regularly
- [ ] PV snapshots are configured
- [ ] Application data is backed up
- [ ] Backups are tested

### 11.2 Recovery

- [ ] Recovery procedures are documented
- [ ] Recovery time objectives are defined
- [ ] Recovery point objectives are acceptable
- [ ] DR drills are conducted

### 11.3 Multi-Region

- [ ] Multi-region deployment is considered
- [ ] Data replication is configured
- [ ] Failover procedures exist

## 12. Cost Optimization Checklist

### 12.1 Resource Efficiency

- [ ] Right-sized resources are used
- [ ] VPA recommendations are implemented
- [ ] Spot/preemptible instances are used where appropriate
- [ ] Resource quotas prevent waste

### 12.2 Storage Efficiency

- [ ] Appropriate storage classes are used
- [ ] Storage is reclaimed when not needed
- [ ] Volume snapshotting is optimized

### 12.3 Networking

- [ ] Service type is appropriate
- [ ] Ingress is used instead of LoadBalancer when possible
- [ ] NAT gateways are optimized

## 13. Compliance Checklist

### 13.1 Security Compliance

- [ ] CIS Kubernetes Benchmark is followed
- [ ] Pod Security Standards are enforced
- [ ] Network policies are restrictive
- [ ] Audit logging is enabled

### 13.2 Data Compliance

- [ ] Data residency requirements are met
- [ ] Encryption at rest is configured
- [ ] Encryption in transit is enforced
- [ ] Data retention policies are implemented

### 13.3 Access Control

- [ ] RBAC is properly configured
- [ ] Audit logs are reviewed
- [ ] Service accounts are minimized
- [ ] Default service account is not used

## 14. Operations Checklist

### 14.1 Documentation

- [ ] Architecture is documented
- [ ] Runbooks exist for common operations
- [ ] Deployment procedures are documented
- [ ] Troubleshooting guide exists

### 14.2 Access

- [ ] kubectl access is controlled
- [ ] kubeconfig is managed securely
- [ ] Jump hosts are used appropriately
- [ ] VPN access is configured

### 14.3 Maintenance

- [ ] Kubernetes version is current
- [ ] Node OS is updated
- [ ] Maintenance windows are scheduled
- [ ] Change management is followed

## Related Documents

- [Kubernetes Glossary](../glossary.md)
- [Kubernetes Architecture](../architecture.md)
- [Kubernetes Best Practices](../best-practice.md)
- [Kubernetes Anti-Patterns](../anti-pattern.md)
- [Kubernetes FAQ](../faq.md)
- [Kubernetes Decision Tree](../decision-tree.md)
