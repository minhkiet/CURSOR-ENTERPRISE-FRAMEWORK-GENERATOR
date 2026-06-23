# AWS Knowledge Base - Decision Tree

## Tổng quan

Document này cung cấp cây quyết định chi tiết để hướng dẫn việc lựa chọn các AWS services và configurations phù hợp trong Cursor Enterprise Framework.

## 1. Compute Service Selection Tree

```
Bạn cần chọn compute service nào?
│
├── Cần full control over OS?
│   └── EC2 Virtual Machines
│       ├── Windows hoặc Linux
│       ├── Auto Scaling
│       └── Bare metal (EC2 Bare Metal)
│
├── Cần serverless, event-driven?
│   └── AWS Lambda
│       ├── HTTP via API Gateway
│       ├── Triggered by events (S3, DynamoDB, SQS)
│       └── Max 15 minutes execution
│
├── Cần Docker containers?
│   ├── Cần Kubernetes API? → Amazon EKS
│   │   └── Full Kubernetes control
│   │
│   ├── AWS-managed containers? → Amazon ECS
│   │   ├── On EC2 (self-managed)
│   │   └── On Fargate (serverless)
│   │
│   └── Simple containers? → Amazon Lightsail
│       └── Simple VPS
│
└── Cần batch processing?
    └── AWS Batch
        ├── Managed compute environments
        └── Job scheduling

COMPUTE SELECTION:
┌─────────────────────────────────────────────────────────────┐
│ Full control + OS     → EC2                                   │
│ Serverless functions   → Lambda                                │
│ Containers + K8s      → EKS                                  │
│ Containers (managed)  → ECS Fargate                           │
│ Simple containers      → Lightsail                             │
│ Batch jobs            → AWS Batch                              │
└─────────────────────────────────────────────────────────────┘
```

## 2. Storage Service Selection Tree

```
Bạn cần storage service nào?
│
├── Object storage (files, images, videos)?
│   └── Amazon S3
│       ├── Static website hosting
│       ├── Data lake
│       ├── Backup/Archive (Glacier)
│       └── Intelligent-Tiering
│
├── File storage (NFS/SMB)?
│   └── Amazon EFS/FSx
│       ├── EFS: Linux NFS, scalable
│       └── FSx: Windows (SMB) hoặc Lustre
│
├── Block storage (for VMs)?
│   └── Amazon EBS
│       ├── gp3: General purpose SSD
│       ├── io2: Provisioned IOPS SSD
│       └── st1: Throughput optimized HDD
│
├── Archive storage?
│   └── Amazon S3 Glacier
│       ├── Glacier: 3-12 hours retrieval
│       └── Deep Archive: 12+ hours retrieval
│
└── Hybrid cloud storage?
    └── AWS Storage Gateway
        ├── File Gateway: S3 as NFS
        └── Tape Gateway: S3 as tape
```

## 3. Database Service Selection Tree

```
Bạn cần database service nào?
│
├── Relational (SQL)?
│   ├── Traditional apps? → Amazon RDS
│   │   ├── MySQL, PostgreSQL, MariaDB
│   │   ├── Oracle, SQL Server
│   │   └── Aurora: AWS-native MySQL/PostgreSQL
│   │
│   └── Lift-and-shift SQL Server?
│       └── RDS Custom
│
├── NoSQL (document, key-value)?
│   ├── Massive scale, serverless? → Amazon DynamoDB
│   │   ├── Key-value
│   │   ├── Document (JSON)
│   │   └── Global tables
│   │
│   └── MongoDB-compatible? → Amazon DocumentDB
│
├── In-memory cache?
│   └── Amazon ElastiCache
│       ├── Redis: Complex data structures
│       └── Memcached: Simple key-value
│
├── Graph database?
│   └── Amazon Neptune
│
└── Time-series data?
    └── Amazon Timestream
```

## 4. Networking Service Selection Tree

```
Bạn cần networking service nào?
│
├── Load balancing?
│   ├── HTTP/HTTPS? → Application Load Balancer
│   │   ├── Layer 7 routing
│   │   ├── Path-based routing
│   │   └── SSL termination
│   │
│   ├── TCP/UDP? → Network Load Balancer
│   │   ├── Layer 4
│   │   └── Millions of requests/second
│   │
│   └── Legacy? → Classic Load Balancer
│
├── DNS management?
│   └── Amazon Route 53
│       ├── A, AAAA, CNAME, MX records
│       ├── Health checks
│       └── Routing policies: Simple, Weighted, Latency, Geo
│
├── CDN/Edge?
│   └── Amazon CloudFront
│       ├── Global content delivery
│       ├── Edge functions (Lambda@Edge)
│       └── WAF integration
│
├── VPN/Private connection?
│   ├── Site-to-Site VPN
│   ├── Client VPN
│   └── Direct Connect (private line)
│
└── API Management?
    └── Amazon API Gateway
        ├── REST APIs
        └── WebSocket APIs
```

## 5. Security Service Selection Tree

```
Bạn cần security service nào?
│
├── Identity & Access?
│   └── AWS IAM
│       ├── Users, Groups, Roles
│       ├── Policies
│       └── Federation (SSO)
│
├── Secrets Management?
│   └── AWS Secrets Manager
│       ├── Database credentials
│       ├── API keys
│       └── Automatic rotation
│
├── Encryption Keys?
│   └── AWS KMS
│       ├── Symmetric keys (AES-256)
│       ├── Asymmetric keys (RSA, ECC)
│       └── CloudHSM for FIPS 140-2
│
├── DDoS Protection?
│   ├── Layer 3/4 → AWS Shield
│   │   ├── Shield Standard: Free
│   │   └── Shield Advanced: Paid
│   │
│   └── Layer 7 → AWS WAF
│       ├── OWASP rules
│       └── Custom rules
│
└── Security Monitoring?
    ├── GuardDuty: Threat detection
    ├── Security Hub: Centralized view
    └── Inspector: Vulnerability scanning
```

## 6. Analytics Service Selection Tree

```
Bạn cần analytics service nào?
│
├── Data warehousing?
│   └── Amazon Redshift
│       ├── Petabyte scale
│       └── RA3 nodes for scaling
│
├── Real-time analytics?
│   ├── Streaming data? → Amazon Kinesis
│   │   ├── Kinesis Data Streams
│   │   ├── Kinesis Data Firehose
│   │   └── Kinesis Data Analytics
│   │
│   └── OpenSearch (Elasticsearch)?
│
├── Big data processing?
│   └── Amazon EMR
│       ├── Hadoop, Spark
│       ├── Hive, Presto
│       └── Serverless option
│
├── Data visualization?
│   └── Amazon QuickSight
│       ├── Dashboards
│       └── ML-powered insights
│
└── SQL queries on S3?
    └── Amazon Athena
        ├── Serverless
        └── Pay per query
```

## 7. Machine Learning Service Selection Tree

```
Bạn cần ML service nào?
│
├── No ML experience?
│   ├── Predictions? → Amazon Forecast, Personalize
│   ├── Chatbots? → Amazon Lex
│   ├── Text analysis? → Amazon Comprehend
│   └── Image recognition? → Amazon Rekognition
│
├── Data scientists?
│   └── Amazon SageMaker
│       ├── Ground Truth: Labeling
│       ├── Canvas: No-code ML
│       ├── Studio: Full IDE
│       └── Autopilot: AutoML
│
├── Deep learning?
│   ├── Custom models → SageMaker Training
│   ├── Inference → SageMaker Endpoints
│   └── GPU instances → EC2 P3/P4/G4
│
└── AI Services (Pre-built)?
    ├── Text-to-speech → Polly
    ├── Translation → Translate
    ├── Speech-to-text → Transcribe
    └── Language → Bedrock (LLMs)
```

## 8. Deployment Service Selection Tree

```
Bạn cần deployment service nào?
│
├── Code deployment?
│   ├── Full CI/CD → AWS CodePipeline
│   ├── Build only → AWS CodeBuild
│   └── Deploy only → AWS CodeDeploy
│
├── Infrastructure as Code?
│   ├── AWS-native → CloudFormation
│   │   ├── JSON/YAML
│   │   └── CDK (TypeScript, Python, etc.)
│   │
│   └── Terraform → HashiCorp Terraform on AWS
│
├── Container deployment?
│   ├── ECS/EKS → ECS Deploy, Flagger
│   └── Helm charts
│
└── Lambda deployment?
    ├── SAM (Serverless Application Model)
    └── Serverless Framework
```

## 9. Quick Reference Decision Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUICK DECISION GUIDE                            │
├─────────────────────────────────┬──────────────────────────────────────┤
│ NEED                             │ SERVICE                               │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Virtual machines                 │ EC2                                    │
│ Serverless functions            │ Lambda                                 │
│ Containers                      │ ECS/EKS                               │
│ Object storage                  │ S3                                     │
│ File storage                    │ EFS/FSx                               │
│ Block storage                   │ EBS                                    │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Relational database            │ RDS (Aurora)                           │
│ NoSQL database                 │ DynamoDB                               │
│ In-memory cache                │ ElastiCache                            │
│ Graph database                 │ Neptune                               │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Load balancer (HTTP)           │ Application Load Balancer              │
│ Load balancer (TCP)            │ Network Load Balancer                  │
│ CDN                            │ CloudFront                            │
│ DNS                            │ Route 53                              │
│ API Gateway                    │ API Gateway                           │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Identity & Access              │ IAM                                    │
│ Secrets                        │ Secrets Manager                        │
│ Encryption keys                │ KMS                                    │
│ DDoS protection                │ Shield + WAF                          │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Data warehouse                 │ Redshift                              │
│ Real-time streaming            │ Kinesis                               │
│ SQL on S3                      │ Athena                                │
│ Visualization                  │ QuickSight                            │
├─────────────────────────────────┼──────────────────────────────────────┤
│ CI/CD pipeline                 │ CodePipeline                          │
│ Infrastructure as Code         │ CloudFormation / CDK                   │
│ Containers                     │ ECS/EKS                               │
│ Serverless                    │ Lambda + SAM                           │
├─────────────────────────────────┼──────────────────────────────────────┤
│ Monitoring & Logs              │ CloudWatch                            │
│ Distributed tracing            │ X-Ray                                 │
│ Metrics & Alarms               │ CloudWatch                            │
│ Log analysis                   │ CloudWatch Logs                        │
└─────────────────────────────────┴──────────────────────────────────────┘
```

## Related Documents

- [AWS Glossary](../glossary.md)
- [AWS Architecture](../architecture.md)
- [AWS Best Practices](../best-practice.md)
- [AWS Anti-Patterns](../anti-pattern.md)
- [AWS Checklist](../checklist.md)
- [AWS FAQ](../faq.md)
