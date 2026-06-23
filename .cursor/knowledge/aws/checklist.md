# AWS Knowledge Base - Checklist

## Tổng quan

Document này cung cấp checklist toàn diện cho việc đánh giá và kiểm tra AWS deployments trong Cursor Enterprise Framework.

## 1. Security Checklist

### 1.1 Identity and Access Management

- [ ] IAM users created with appropriate permissions
- [ ] MFA enabled for all IAM users
- [ ] Access keys rotated regularly
- [ ] IAM roles used instead of access keys for services
- [ ] Password policy enforced
- [ ] Service Control Policies (SCPs) configured
- [ ] Permissions boundaries used where appropriate

### 1.2 Network Security

- [ ] VPC created with proper CIDR ranges
- [ ] Private subnets for application tiers
- [ ] Security groups with least privilege
- [ ] NACLs configured appropriately
- [ ] VPC Flow Logs enabled
- [ ] NAT Gateways for private subnet internet access
- [ ] VPN or Direct Connect for hybrid connectivity

### 1.3 Data Security

- [ ] Encryption at rest enabled for all storage
- [ ] Encryption in transit enforced
- [ ] KMS keys created and rotated
- [ ] Secrets Manager used for sensitive data
- [ ] S3 bucket policies restrictive
- [ ] S3 public access blocked
- [ ] EBS encryption enabled by default

### 1.4 Monitoring and Logging

- [ ] CloudTrail enabled for all regions
- [ ] CloudWatch Logs configured
- [ ] GuardDuty enabled
- [ ] Security Hub enabled
- [ ] Config rules configured
- [ ] VPC Flow Logs enabled
- [ ] AWS WAF/Shield enabled

## 2. Compute Checklist

### 2.1 EC2

- [ ] Appropriate instance types selected
- [ ] Auto Scaling Group configured
- [ ] Health checks configured
- [ ] Termination protection enabled
- [ ] Instance metadata service v2 (IMDSv2) enforced
- [ ] Detailed monitoring enabled
- [ ] Root volume encrypted

### 2.2 Lambda

- [ ] IAM execution roles properly scoped
- [ ] Environment variables encrypted
- [ ] VPC config if needed
- [ ] Dead letter queues configured
- [ ] Concurrency limits set
- [ ] Provisioned concurrency for critical functions

### 2.3 ECS/EKS

- [ ] Task definitions properly configured
- [ ] IAM roles for tasks
- [ ] Network mode appropriate
- [ ] Autoscaling configured
- [ ] Secrets injected securely
- [ ] Container security hardening

## 3. Storage Checklist

### 3.1 S3

- [ ] Bucket policies restrictive
- [ ] Public access blocked
- [ ] Versioning enabled
- [ ] Lifecycle policies configured
- [ ] Encryption enabled
- [ ] Intelligent-Tiering for cost optimization
- [ ] Cross-region replication for DR

### 3.2 EBS

- [ ] Encrypted volumes
- [ ] Appropriate volume types
- [ ] Snapshots configured
- [ ] Regular backups
- [ ] Cleanup policies

### 3.3 EFS/FSx

- [ ] Encryption enabled
- [ ] Backup configured
- [ ] Performance mode appropriate

## 4. Database Checklist

### 4.1 RDS

- [ ] Multi-AZ enabled for production
- [ ] Read replicas for read scaling
- [ ] Encryption enabled
- [ ] Backup retention configured
- [ ] Point-in-time recovery enabled
- [ ] Performance Insights enabled
- [ ] Auto minor version upgrades enabled

### 4.2 DynamoDB

- [ ] On-demand or provisioned capacity appropriate
- [ ] Encryption enabled
- [ ] TTL configured where appropriate
- [ ] Global tables for multi-region
- [ ] DAX for caching
- [ ] Streams enabled for triggers

### 4.3 ElastiCache

- [ ] Encryption in transit
- [ ] Encryption at rest
- [ ] Memcached or Redis appropriate
- [ ] Cluster mode if needed
- [ ] Replicas for Redis

## 5. Networking Checklist

### 5.1 VPC

- [ ] Proper CIDR allocation
- [ ] Subnets properly distributed across AZs
- [ ] Route tables configured
- [ ] Internet Gateway attached
- [ ] NAT Gateways for private subnets
- [ ] Transit Gateway for multi-VPC

### 5.2 Load Balancers

- [ ] Application/Network/Classic appropriate
- [ ] Health checks configured
- [ ] SSL certificates valid
- [ ] Access logs enabled
- [ ] Cross-zone load balancing
- [ ] Desync mitigation mode

### 5.3 Route 53

- [ ] Hosted zones configured
- [ ] Health checks for failover
- [ ] Routing policies appropriate
- [ ] DNSSEC enabled
- [ ] Alias records for AWS resources

## 6. DevOps Checklist

### 6.1 CI/CD

- [ ] CodePipeline/CodeBuild configured
- [ ] Buildspec properly configured
- [ ] Artifact storage encrypted
- [ ] Deployment strategies defined
- [ ] Rollback mechanisms in place
- [ ] Testing automated

### 6.2 Infrastructure as Code

- [ ] CloudFormation/Terraform used
- [ ] Templates version controlled
- [ ] Environments properly segregated
- [ ] Drift detection enabled
- [ ] StackSets for multi-account

## 7. Monitoring Checklist

### 7.1 CloudWatch

- [ ] Dashboards created
- [ ] Alarms configured
- [ ] Log groups configured
- [ ] Metrics collected
- [ ] Anomaly detection enabled

### 7.2 Cost Management

- [ ] Budgets created
- [ ] Cost allocation tags enabled
- [ ] Cost Explorer analyzed
- [ ] Savings Plans/Reserved Instances
- [ ] Unused resources cleaned up

## 8. Disaster Recovery Checklist

### 8.1 Backup

- [ ] Regular backups configured
- [ ] Backup verification tested
- [ ] Cross-region backup
- [ ] Backup retention appropriate

### 8.2 High Availability

- [ ] Multi-AZ deployments
- [ ] Auto Scaling configured
- [ ] Load balancing with health checks
- [ ] Failover mechanisms tested

### 8.3 DR Strategy

- [ ] RTO/RPO defined
- [ ] DR site configured
- [ ] Failover procedures documented
- [ ] DR drills conducted

## 9. Compliance Checklist

### 9.1 Data Protection

- [ ] PII identified and protected
- [ ] Encryption standards met
- [ ] Data residency requirements met
- [ ] Retention policies defined

### 9.2 Audit

- [ ] CloudTrail enabled
- [ ] Access logging enabled
- [ ] Audit reports generated
- [ ] Compliance framework aligned

## 10. Operations Checklist

### 10.1 Change Management

- [ ] Change approval process
- [ ] Deployment procedures documented
- [ ] Rollback procedures tested

### 10.2 Incident Response

- [ ] Runbooks created
- [ ] Escalation procedures defined
- [ ] On-call rotation established
- [ ] Post-incident reviews

### 10.3 Support

- [ ] Support plan appropriate
- [ ] AWS Trusted Advisor access
- [ ] AWS Support API integrated

## Related Documents

- [AWS Glossary](../glossary.md)
- [AWS Architecture](../architecture.md)
- [AWS Best Practices](../best-practice.md)
- [AWS Anti-Patterns](../anti-pattern.md)
- [AWS FAQ](../faq.md)
- [AWS Decision Tree](../decision-tree.md)
