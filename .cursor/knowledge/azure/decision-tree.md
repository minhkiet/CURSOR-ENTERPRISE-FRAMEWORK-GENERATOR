# Azure Knowledge Base - Decision Tree

## Tổng quan

Document này cung cấp cây quyết định chi tiết để hướng dẫn việc lựa chọn các Azure services và configurations phù hợp trong Cursor Enterprise Framework.

## 1. Compute Service Selection Tree

```
Bạn cần chọn compute service nào?
│
├── Cần full control over OS và infrastructure?
│   └── Azure Virtual Machines
│       ├── Windows hoặc Linux
│       ├── Custom configurations
│       └── Managed disks, availability sets/zones
│
├── Cần host web applications, APIs, hoặc background jobs?
│   └── Azure App Service
│       ├── .NET, Java, Node.js, Python, PHP
│       ├── Web Apps, API Apps, Mobile Apps
│       └── Auto-scaling, deployment slots
│
├── Cần serverless, event-driven functions?
│   └── Azure Functions
│       ├── HTTP triggers, Timer triggers
│       ├── Event Grid, Service Bus triggers
│       └── Consumption or Premium plan
│
├── Cần container orchestration?
│   └── Azure Kubernetes Service (AKS)
│       ├── Managed Kubernetes
│       ├── Windows hoặc Linux containers
│       └── Auto-scaling, upgrades
│
└── Cần simple container hosting?
    └── Azure Container Instances
        ├── Quick deployment
        ├── No orchestration needed
        └── Short-lived workloads

COMPUTE SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Full control     → Virtual Machines                        │
│ Web apps         → App Service                             │
│ Serverless       → Azure Functions                        │
│ Containers + Scale→ AKS                                    │
│ Simple containers → Container Instances                     │
└─────────────────────────────────────────────────────────────┘
```

## 2. Storage Service Selection Tree

```
Bạn cần storage service nào?
│
├── Lưu trữ files (documents, images, videos)?
│   ├── Static website → Azure Blob Storage + Static Website
│   ├── File shares → Azure Files
│   └── Object storage → Azure Blob Storage
│
├── Lưu trữ NoSQL data?
│   └── Azure Cosmos DB
│       ├── SQL, MongoDB, Cassandra APIs
│       ├── Global distribution
│       └── Multi-region writes
│
├── Lưu trữ relational data?
│   ├── Full SQL Server features → Azure SQL Managed Instance
│   ├── Single database → Azure SQL Database
│   └── PostgreSQL/MySQL → Azure Database for PostgreSQL/MySQL
│
├── Message queue?
│   └── Azure Queue Storage hoặc Service Bus
│
└── Cần data warehouse?
    └── Azure Synapse Analytics

STORAGE SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Files/blobs        → Blob Storage / Azure Files          │
│ NoSQL              → Cosmos DB                            │
│ Relational         → Azure SQL / Managed Instance          │
│ Messages           → Queue Storage / Service Bus           │
│ Analytics          → Synapse Analytics                    │
└─────────────────────────────────────────────────────────────┘
```

## 3. Networking Service Selection Tree

```
Bạn cần networking service nào?
│
├── Load balancing (Layer 4)?
│   └── Azure Load Balancer
│       ├── Public or Internal
│       ├── Health probes
│       └── Backend pools
│
├── Load balancing với WAF (Layer 7)?
│   └── Azure Application Gateway
│       ├── URL-based routing
│       ├── SSL termination
│       ├── Web Application Firewall
│       └── Rewrite rules
│
├── Global traffic management?
│   └── Azure Front Door
│       ├── Global load balancing
│       ├── CDN
│       └── WAF
│
├── DNS management?
│   └── Azure DNS
│       ├── Public DNS zones
│       └── Private DNS zones
│
├── VPN to on-premises?
│   └── Azure VPN Gateway
│       ├── Site-to-Site
│       ├── Point-to-Site
│       └── ExpressRoute (private)
│
└── Network security?
    ├── Perimeter → Azure Firewall
    ├── NSGs → Network Security Groups
    └── Bastion → Azure Bastion (no public IPs)
```

## 4. Database Service Selection Tree

```
Bạn cần database service nào?
│
├── SQL-like relational database?
│   ├── Single database, elastic pool → Azure SQL Database
│   │   └── Serverless for intermittent usage
│   │
│   ├── Full SQL Server, miễn phí nào? → Azure SQL Managed Instance
│   │   └── Lift-and-shift SQL Server
│   │
│   └── Open-source databases?
│       ├── PostgreSQL → Azure Database for PostgreSQL
│       ├── MySQL → Azure Database for MySQL
│       └── MariaDB → Azure Database for MariaDB
│
├── NoSQL, globally distributed?
│   └── Azure Cosmos DB
│       ├── Multiple APIs (SQL, MongoDB, Cassandra)
│       ├── Tunable consistency
│       └── Multi-region replication
│
├── In-memory cache?
│   └── Azure Cache for Redis
│       ├── Basic (single node)
│       ├── Standard (replicated)
│       └── Premium (clustered)
│
└── Big data / Analytics?
    ├── Data warehouse → Azure Synapse Analytics
    ├── Big data clusters → Azure HDInsight
    └── Data lakes → Azure Data Lake Storage
```

## 5. Security Service Selection Tree

```
Bạn cần security service nào?
│
├── Identity và Access Management?
│   └── Azure Active Directory
│       ├── User authentication
│       ├── SSO
│       ├── Conditional Access
│       └── Privileged Identity Management (PIM)
│
├── Secrets Management?
│   └── Azure Key Vault
│       ├── Keys
│       ├── Secrets
│       └── Certificates
│
├── Protect against DDoS?
│   └── Azure DDoS Protection
│       ├── Basic (automatic)
│       └── Standard (additional protection)
│
├── Web Application Firewall?
│   └── Azure Application Gateway WAF
│       └── OWASP rules
│
├── Network Security?
│   ├── Perimeter → Azure Firewall
│   ├── Subnet → Network Security Groups (NSGs)
│   └── Private access → Private Endpoints
│
└── Security monitoring?
    └── Azure Security Center / Microsoft Defender
        ├── Posture management
        └── Threat protection
```

## 6. Monitoring Service Selection Tree

```
Bạn cần monitoring service nào?
│
├── Centralized logging?
│   └── Azure Monitor - Log Analytics
│       ├── Azure Activity logs
│       ├── Resource logs
│       └── Custom logs
│
├── Application Performance Monitoring?
│   └── Application Insights
│       ├── Live metrics
│       ├── Distributed tracing
│       └── Smart detection
│
├── Infrastructure monitoring?
│   └── Azure Monitor for VMs / Containers
│       ├── Performance
│       ├── Health
│       └── Dependencies
│
├── Metrics và alerts?
│   └── Azure Monitor Alerts
│       ├── Metric alerts
│       ├── Log query alerts
│       └── Activity log alerts
│
└── Dashboarding?
    └── Azure Dashboards / Grafana
        ├── Custom visualizations
        └── Sharing
```

## 7. DevOps Service Selection Tree

```
Bạn cần DevOps service nào?
│
├── Source control?
│   └── Azure Repos (Git)
│       └── Pull requests, policies
│
├── CI/CD?
│   ├── Pipeline-based → Azure Pipelines
│   └── GitOps → Azure Arc / GitHub Actions
│
├── Container registry?
│   └── Azure Container Registry
│       ├── Basic (dev)
│       ├── Standard (prod)
│       └── Premium (geo-replication)
│
├── Infrastructure as Code?
│   ├── Declarative → ARM templates / Bicep
│   └── Terraform → HashiCorp Terraform provider
│
├── Security scanning?
│   ├── Containers → Microsoft Defender for Containers
│   └── Code → GitHub Advanced Security
│
└── Project management?
    └── Azure Boards
        ├── Kanban boards
        └── Sprint planning
```

## 8. Disaster Recovery Selection Tree

```
Bạn cần DR solution nào?
│
├── VMs?
│   ├── Site Recovery
│   │   └── Azure Site Recovery vault
│   │
│   └── Azure Backup
│       └── For non-critical VMs
│
├── Databases?
│   ├── Azure SQL → Geo-replication / Auto-failover groups
│   ├── Cosmos DB → Multi-region configuration
│   └── Redis → Geo-replication
│
├── Storage?
│   └── Geo-redundant Storage (GRS/GZRS)
│
├── Application tier?
│   ├── Traffic Manager → DNS failover
│   ├── Front Door → Global load balancing
│   └── App Service → Traffic Manager / Front Door
│
└── DRaaS comparison:
    ┌─────────────────────────────────────────────────────────┐
    │ Service Level    │ RTO        │ RPO        │ Cost     │
    ├──────────────────┼────────────┼────────────┼──────────┤
    │ Site Recovery    │ Minutes    │ Minutes    │ Medium   │
    │ Geo-replication  │ Minutes    │ Near-zero  │ High     │
    │ Backup + Restore │ Hours      │ Last backup│ Low      │
    └──────────────────┴────────────┴────────────┴──────────┘
```

## 9. Cost Optimization Selection Tree

```
Bạn muốn optimize costs như thế nào?
│
├── Compute?
│   ├── Right-size VMs → Check metrics, resize
│   ├── Spot VMs → For batch workloads
│   ├── Reserved Instances → 1 or 3 year commitment
│   └── Auto-scale → Scale down during off-hours
│
├── Storage?
│   ├── Use appropriate tiers → Hot/Cool/Archive
│   ├── Lifecycle policies → Auto-tier to cooler
│   └── Delete unused → Azure Orphaned Resources
│
├── Database?
│   ├── Serverless → For intermittent usage
│   ├── DTU vs vCore → Match to workload
│   └── Reserved capacity → For production
│
├── Networking?
│   ├── Private Endpoints → Avoid data transfer charges
│   └── ExpressRoute → For high-volume connectivity
│
└── Monitoring?
    ├── Set budgets → Cost Management budgets
    ├── Alerts → Spending alerts
    └── Policies → Enforce cost controls
```

## 10. Quick Reference Decision Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUICK DECISION GUIDE                            │
├─────────────────────────────────┬──────────────────────────────────────┤
│ NEED                             │ SERVICE                             │
├─────────────────────────────────┼──────────────────────────────────────┤
│ IaaS VMs                         │ Virtual Machines                    │
│ PaaS Web Apps                   │ App Service                        │
│ Serverless Functions             │ Azure Functions                    │
│ Container Orchestration         │ AKS                                 │
│ Simple Containers               │ Container Instances                  │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Object Storage                  │ Blob Storage                        │
│ File Shares                     │ Azure Files                        │
│ NoSQL Database                 │ Cosmos DB                          │
│ Relational Database             │ Azure SQL Database                  │
│ In-Memory Cache                │ Azure Cache for Redis               │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Layer 4 Load Balancer           │ Load Balancer                       │
│ Layer 7 Load Balancer + WAF     │ Application Gateway                 │
│ Global CDN + Load Balancer      │ Front Door                         │
│ Web Application Firewall        │ App Gateway WAF                    │
│ DNS Management                  │ Azure DNS                          │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Secrets Management              │ Key Vault                           │
│ Identity & Access              │ Azure AD                            │
│ DDoS Protection                 │ DDoS Protection                    │
│ Network Security               │ Azure Firewall + NSGs              │
│ Security Monitoring            │ Security Center / Defender          │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Centralized Logging             │ Log Analytics                       │
│ APM                            │ Application Insights                │
│ Infrastructure Monitoring       │ Azure Monitor                       │
│ Dashboards                     │ Azure Dashboards / Grafana          │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Infrastructure as Code          │ ARM Templates / Bicep / Terraform   │
│ CI/CD                          │ Azure Pipelines / GitHub Actions    │
│ Container Registry             │ Container Registry                   │
│ Source Control                 │ Azure Repos / GitHub                │
├─────────────────────────────────┼──────────────────────────────────────┤
│ VM Backup                      │ Azure Backup / Site Recovery        │
│ Database Backup                │ Built-in + Geo-replication          │
│ Disaster Recovery              │ Site Recovery                       │
└─────────────────────────────────┴──────────────────────────────────────┘
```

## Related Documents

- [Azure Glossary](../glossary.md)
- [Azure Architecture](../architecture.md)
- [Azure Best Practices](../best-practice.md)
- [Azure Anti-Patterns](../anti-pattern.md)
- [Azure Checklist](../checklist.md)
- [Azure FAQ](../faq.md)
