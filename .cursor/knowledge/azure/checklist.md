# Azure Knowledge Base - Checklist

## Tổng quan

Document này cung cấp checklist toàn diện cho việc đánh giá và kiểm tra Azure deployments trong Cursor Enterprise Framework.

## 1. Security Checklist

### 1.1 Identity và Access

- [ ] Azure AD tenant configured
- [ ] Conditional Access policies defined
- [ ] MFA enabled for all users
- [ ] Privileged Identity Management (PIM) enabled
- [ ] Service principals use managed identities
- [ ] No hardcoded credentials in code
- [ ] RBAC roles properly assigned
- [ ] Access reviews scheduled

### 1.2 Network Security

- [ ] Virtual Network created with proper address space
- [ ] Subnets properly segmented
- [ ] Network Security Groups (NSGs) configured
- [ ] Private Endpoints enabled for sensitive services
- [ ] Azure Firewall or NVAs deployed for perimeter
- [ ] DDoS Protection enabled
- [ ] VPN/ExpressRoute configured for hybrid

### 1.3 Data Security

- [ ] Encryption at rest enabled
- [ ] Encryption in transit (TLS) enforced
- [ ] Azure Key Vault used for secrets
- [ ] Key rotation policy defined
- [ ] Firewall rules on databases and storage
- [ ] Soft delete enabled for blobs

### 1.4 Application Security

- [ ] WAF enabled on Application Gateway
- [ ] SSL/TLS certificates properly managed
- [ ] Application Insights configured
- [ ] Security scanning in CI/CD pipeline
- [ ] Dependency scanning enabled
- [ ] Secrets not in source control

## 2. Networking Checklist

### 2.1 Virtual Network

- [ ] Address space properly sized
- [ ] Subnets created with appropriate sizes
- [ ] Service Endpoints configured
- [ ] Private Endpoints configured
- [ ] DNS configuration correct
- [ ] Peering configured if needed

### 2.2 Load Balancing

- [ ] Load Balancer type appropriate (Standard/SKU)
- [ ] Health probes configured
- [ ] Backend pools properly configured
- [ ] SSL termination configured
- [ ] Session persistence set correctly
- [ ] Availability Zones used

### 2.3 Application Delivery

- [ ] Application Gateway deployed
- [ ] WAF policy configured
- [ ] SSL certificates valid
- [ ] Rewrite rules tested
- [ ] Autoscaling configured
- [ ] CDN used for static assets

## 3. Compute Checklist

### 3.1 Virtual Machines

- [ ] Appropriate VM size selected
- [ ] Managed disks used
- [ ] Disk redundancy appropriate (LRS/GRS/ZRS)
- [ ] Availability Zones configured
- [ ] VM extensions properly configured
- [ ] Just-in-Time access enabled
- [ ] VM backup configured

### 3.2 App Service

- [ ] App Service Plan sized correctly
- [ ] Deployment slots created
- [ ] Auto-swap enabled (if appropriate)
- [ ] Connection strings in Key Vault
- [ ] HTTPS only enforced
- [ ] ARR affinity reviewed
- [ ] Health check endpoint configured

### 3.3 Kubernetes (AKS)

- [ ] RBAC enabled
- [ ] Azure AD integration configured
- [ ] Network policy enabled
- [ ] Container monitoring enabled
- [ ] Pod security policies/admission controller configured
- [ ] Horizontal Pod Autoscaler configured
- [ ] Cluster autoscaler enabled

## 4. Storage Checklist

### 4.1 Storage Accounts

- [ ] Appropriate performance tier (Standard/Premium)
- [ ] Redundancy level appropriate (LRS/GRS/ZRS/GZRS)
- [ ] Public access disabled
- [ ] Hierarchical namespace enabled (if needed)
- [ ] Soft delete enabled
- [ ] Lifecycle policies configured
- [ ] Network rules configured

### 4.2 Blob Storage

- [ ] Access tier appropriate (Hot/Cool/Archive)
- [ ] CDN integrated for static content
- [ ] Immutability configured (if needed)
- [ ] Versioning enabled
- [ ] Change feed configured (if needed)

### 4.3 Files

- [ ] File shares sized appropriately
- [ ] Backup configured
- [ ] SMB 3.0 encryption enforced
- [ ] Large file shares enabled (if needed)

## 5. Database Checklist

### 5.1 Azure SQL

- [ ] Appropriate service tier selected
- [ ] Connection strings in Key Vault
- [ ] Firewall rules configured
- [ ] Geo-replication configured
- [ ] Point-in-time restore enabled
- [ ] Threat detection enabled
- [ ] Auditing enabled
- [ ] Auto-tuning configured

### 5.2 Cosmos DB

- [ ] Appropriate API selected
- [ ] Consistency level appropriate
- [ ] Multi-region writes enabled (if needed)
- [ ] Partition key optimized
- [ ] Request units properly sized
- [ ] Backup policy configured

### 5.3 Redis Cache

- [ ] Appropriate tier selected
- [ ] Redis version current
- [ ] SSL required
- [ ] Cluster mode enabled (if needed)
- [ ] Data persistence configured
- [ ] Firewall rules configured

## 6. Monitoring Checklist

### 6.1 Azure Monitor

- [ ] Log Analytics workspace created
- [ ] Diagnostic settings configured
- [ ] Metrics collected
- [ ] Alerts configured
- [ ] Action groups defined
- [ ] Service Health alerts enabled

### 6.2 Application Insights

- [ ] SDK integrated
- [ ] Sampling configured
- [ ] Availability tests created
- [ ] Smart Detection enabled
- [ ] Dashboard configured

### 6.3 Container Monitoring

- [ ] Container Insights enabled
- [ ] Log Analytics connected
- [ ] Prometheus metrics collected
- [ ] Alerts configured for pods

## 7. Cost Management Checklist

### 7.1 Budget

- [ ] Budget created and alerts configured
- [ ] Cost alerts enabled
- [ ] Spending tracked by tag

### 7.2 Optimization

- [ ] Right-sized resources
- [ ] Unused resources identified
- [ ] Reserved instances considered
- [ ] Auto-shutdown for dev resources
- [ ] Spot VMs for batch workloads

### 7.3 Review

- [ ] Cost analysis reviewed regularly
- [ ] Anomalies investigated
- [ ] Cost recommendations reviewed

## 8. Governance Checklist

### 8.1 Policy

- [ ] Azure Policy definitions created
- [ ] Policies assigned at appropriate scope
- [ ] Compliance monitored
- [ ] Non-compliant resources remediated

### 8.2 Resource Organization

- [ ] Management groups configured
- [ ] Resource groups properly organized
- [ ] Tags standardized
- [ ] Naming convention defined

### 8.3 Blueprints

- [ ] Blueprints defined for compliance
- [ ] Blueprints assigned
- [ ] Blueprints updated as needed

## 9. Disaster Recovery Checklist

### 9.1 Backup

- [ ] Azure Backup configured for VMs
- [ ] SQL Managed Instance backup configured
- [ ] Storage account backup configured (if needed)
- [ ] Backup policies defined
- [ ] Backup retention appropriate

### 9.2 Replication

- [ ] Geo-replication enabled
- [ ] Failover tested
- [ ] Recovery procedures documented

### 9.3 Site Recovery

- [ ] Site Recovery configured for critical VMs
- [ ] Failover tested
- [ ] Recovery time objectives (RTO) met
- [ ] Recovery point objectives (RPO) met

## 10. Operations Checklist

### 10.1 Deployment

- [ ] ARM templates/Bicep used
- [ ] Terraform used (if applicable)
- [ ] Deployment pipeline configured
- [ ] Secrets in Key Vault
- [ ] Deployment validated

### 10.2 Maintenance

- [ ] Update management configured
- [ ] Patching scheduled
- [ ] Maintenance windows defined
- [ ] Dependencies managed

### 10.3 Support

- [ ] Support plan appropriate
- [ ] Support contacts configured
- [ ] Incident procedures documented

## 11. Compliance Checklist

### 11.1 Regulatory

- [ ] GDPR requirements addressed
- [ ] Industry-specific compliance (HIPAA, PCI, etc.)
- [ ] Data residency requirements met
- [ ] Retention policies defined

### 11.2 Audit

- [ ] Audit logging enabled
- [ ] Logs retained appropriately
- [ ] Compliance reports generated
- [ ] Access audits conducted

## 12. Networking Advanced Checklist

### 12.1 Hybrid Connectivity

- [ ] ExpressRoute configured (if needed)
- [ ] VPN Gateway configured
- [ ] Virtual WAN configured (if needed)
- [ ] Routing properly configured

### 12.2 Application Delivery

- [ ] Traffic Manager configured (if needed)
- [ ] Azure Front Door configured (if needed)
- [ ] SSL offloading configured
- [ ] Custom domains configured

### 12.3 Security

- [ ] Azure Firewall deployed
- [ ] Web Application Firewall policies configured
- [ ] NSG flow logs enabled
- [ ] DDoS Protection Standard configured

## 13. Developer Checklist

### 13.1 CI/CD

- [ ] Build pipeline configured
- [ ] Release pipeline configured
- [ ] Infrastructure as Code in pipeline
- [ ] Automated testing in pipeline
- [ ] Deployment approval process defined

### 13.2 DevOps

- [ ] Git repository configured
- [ ] Branching strategy defined
- [ ] Code review process in place
- [ ] Automated testing coverage adequate

### 13.3 Security

- [ ] Secrets scanning in pipeline
- [ ] Dependency scanning configured
- [ ] SAST/DAST in pipeline
- [ ] Container scanning enabled

## Related Documents

- [Azure Glossary](../glossary.md)
- [Azure Architecture](../architecture.md)
- [Azure Best Practices](../best-practice.md)
- [Azure Anti-Patterns](../anti-pattern.md)
- [Azure FAQ](../faq.md)
- [Azure Decision Tree](../decision-tree.md)
