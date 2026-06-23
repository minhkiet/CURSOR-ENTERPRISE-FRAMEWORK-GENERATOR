# AWS Knowledge Base - FAQ

## Tổng quan

Document này cung cấp 10 câu hỏi thường gặp và câu trả lời chi tiết về AWS trong Cursor Enterprise Framework.

## Câu hỏi 1: Làm thế nào để bắt đầu với AWS?

### Câu trả lời

```bash
# 1. Đăng ký AWS account
# Truy cập https://aws.amazon.com/free

# 2. Cài đặt AWS CLI
# Windows: winget install Amazon.AWSCLI
# macOS: brew install awscli
# Linux: curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# 3. Cấu hình AWS CLI
aws configure
# AWS Access Key ID: [your-key]
# AWS Secret Access Key: [your-secret]
# Default region name: us-east-1
# Default output format: json

# 4. Verify configuration
aws sts get-caller-identity

# 5. Tạo resources đầu tiên
# Tạo S3 bucket
aws s3 mb s3://my-unique-bucket-name

# Tạo EC2 instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-key-pair \
  --security-group-ids sg-0123456789abcdef0

# Tạo Lambda function
aws lambda create-function \
  --function-name my-function \
  --runtime python3.9 \
  --role arn:aws:iam::123456789012:role/lambda-execution-role \
  --handler app.handler \
  --zip-file fileb://function.zip
```

## Câu hỏi 2: Sự khác biệt giữa EC2, ECS, EKS, và Lambda là gì?

### Câu trả lời

| Service | Type | Use Case | Management |
|---------|------|---------|------------|
| EC2 | IaaS | Full control over OS | Manual |
| ECS | Container | Docker containers on EC2/Fargate | Managed |
| EKS | Kubernetes | Full K8s API | Managed K8s |
| Lambda | Serverless | Event-driven functions | Fully managed |

```bash
# EC2 - Full control
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-key

# ECS with Fargate - Serverless containers
aws ecs create-cluster --cluster-name my-cluster --capacity-providers FARGATE

# EKS - Managed Kubernetes
aws eks create-cluster --name my-cluster --role-arn arn:aws:iam::123456789012:role/eks-cluster-role

# Lambda - Serverless functions
aws lambda create-function \
  --function-name my-function \
  --runtime python3.9 \
  --handler app.handler \
  --zip-file fileb://function.zip
```

## Câu hỏi 3: Làm thế nào để secure AWS resources?

### Câu trả lời

```bash
# 1. IAM - Quản lý identity và access
aws iam create-user --user-name my-user
aws iam attach-user-policy \
  --user-name my-user \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# 2. MFA - Bật MFA cho tất cả users
aws iam create-virtual-mfa-device \
  --virtual-mfa-device-name my-mfa

# 3. Security Groups - Firewall cho instances
aws ec2 create-security-group \
  --group-name my-sg \
  --description "My security group"

aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# 4. KMS - Mã hóa
aws kms create-key --description "My encryption key"

# 5. Secrets Manager - Quản lý secrets
aws secretsmanager create-secret \
  --name my-secret \
  --secret-string '{"password":"mypassword"}'

# 6. WAF - Web Application Firewall
aws wafv2 create-web-acl \
  --name my-web-acl \
  --scope CLOUDFRONT
```

## Câu hỏi 4: RDS vs DynamoDB vs ElastiCache - Khi nào nên dùng?

### Câu trả lời

| Database | Best For | Scalability | Use Case |
|----------|----------|------------|----------|
| RDS | Relational data, complex queries | Vertical (can add read replicas) | Traditional apps, transactions |
| DynamoDB | NoSQL, massive scale | Automatic horizontal | Serverless, high-traffic apps |
| ElastiCache | Caching, real-time | In-memory | Sessions, leaderboards |

```bash
# RDS - MySQL/PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier my-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --allocated-storage 20 \
  --master-username admin \
  --master-user-password password

# DynamoDB - NoSQL
aws dynamodb create-table \
  --table-name my-table \
  --attribute-definitions AttributeName=PK,AttributeType=S \
  --key-schema AttributeName=PK,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# ElastiCache - Redis
aws elasticache create-cache-cluster \
  --cache-cluster-id my-cluster \
  --engine redis \
  --cache-node-type cache.t3.micro \
  --num-cache-nodes 1
```

## Câu hỏi 5: Làm thế nào để reduce AWS costs?

### Câu trả lời

```bash
# 1. Right-sizing instances
aws ec2 describe-instance-types \
  --query 'InstanceTypes[?MemoryInfo.SizeInMiB>=2048].[InstanceType,MemoryInfo.SizeInMiB,VCpuInfo.DefaultVCpus]'

# Resize instance
aws ec2 stop-instances --instance-ids i-0123456789abcdef0
aws ec2 modify-instance-type \
  --instance-id i-0123456789abcdef0 \
  --instance-type t3.small

# 2. Use Spot instances for non-critical workloads
aws ec2 request-spot-instances \
  --instance-count 5 \
  --spot-price "0.05" \
  --launch-specification file://spot-spec.json

# 3. Reserved instances for steady-state
aws ec2 purchase-reserved-instances-offering \
  --reserved-instances-offering-id offering-id \
  --instance-count 3

# 4. S3 Intelligent-Tiering
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket my-bucket \
  --id my-config \
  --intelligent-tiering-configuration '{
    "Id": "my-config",
    "Status": "Enabled",
    "Tierings": [
      {"Days": 30, "AccessTier": "STANDARD_IA"},
      {"Days": 90, "AccessTier": "GLACIER"}
    ]
  }'

# 5. Auto-stop development resources
aws events put-rule \
  --name stop-dev-instances \
  --schedule-expression "cron(0 18 ? * MON-FRI *)"

# 6. Set up budgets
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "monthly-cost",
    "BudgetLimit": {"Amount": "500", "Unit": "USD"},
    "TimeUnit": "MONTHLY"
  }'
```

## Câu hỏi 6: AWS Lambda hoạt động như thế nào?

### Câu trả lời

```typescript
// Lambda function handler
export const handler = async (event: any): Promise<any> => {
  // Event sources trigger the function
  // - API Gateway (HTTP requests)
  // - S3 (file uploads)
  // - DynamoDB (stream events)
  // - SQS (queue messages)
  
  console.log("Event:", JSON.stringify(event));
  
  // Your business logic
  const result = await processEvent(event);
  
  return {
    statusCode: 200,
    body: JSON.stringify({ success: true, result })
  };
};

// With dependencies (bundled)
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({});

export const processImage = async (event: any) => {
  const bucket = event.Records[0].s3.bucket.name;
  const key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
  
  await s3.send(new PutObjectCommand({
    Bucket: bucket,
    Key: `processed/${key}`,
    Body: processImage(key)
  }));
};
```

```bash
# Deploy Lambda function
aws lambda create-function \
  --function-name my-function \
  --runtime nodejs18.x \
  --handler index.handler \
  --zip-file fileb://function.zip \
  --role execution-role-arn

# Invoke Lambda
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  response.json
```

## Câu hỏi 7: Làm thế nào để monitor AWS resources?

### Câu trả lời

```bash
# 1. CloudWatch Metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average

# 2. CloudWatch Alarms
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu \
  --alarm-description "CPU alarm" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --period 300 \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:my-topic

# 3. CloudWatch Dashboards
aws cloudwatch put-dashboard \
  --dashboard-name my-dashboard \
  --dashboard-body '{
    "widgets": [{
      "type": "metric",
      "properties": {
        "metrics": [["AWS/EC2", "CPUUtilization"]],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1"
      }
    }]
  }'

# 4. CloudWatch Logs
aws logs create-log-group --log-group-name /aws/lambda/my-function
aws logs describe-log-groups --log-group-name-prefix /aws/lambda
```

## Câu hỏi 8: VPC là gì và tại sao cần nó?

### Câu trả lời

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create subnets (public và private)
aws ec2 create-subnet \
  --vpc-id vpc-0123456789abcdef0 \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

aws ec2 create-subnet \
  --vpc-id vpc-0123456789abcdef0 \
  --cidr-block 10.0.2.0/24 \
  --availability-zone us-east-1a

# Create Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway \
  --vpc-id vpc-0123456789abcdef0 \
  --internet-gateway-id igw-0123456789abcdef0

# Create route table
aws ec2 create-route-table --vpc-id vpc-0123456789abcdef0

# Add route for public subnet
aws ec2 create-route \
  --route-table-id rtb-0123456789abcdef0 \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id igw-0123456789abcdef0
```

## Câu hỏi 9: S3 có các storage classes nào?

### Câu trả lời

| Storage Class | Use Case | Cost | Retrieval |
|---------------|---------|------|-----------|
| Standard | Frequently accessed | Highest | Free |
| Intelligent-Tiering | Unknown access patterns | Varies | Free |
| Standard-IA | Infrequent access | Lower | Fees |
| Glacier | Archival | Lowest | Fees + retrieval time |
| Glacier Deep Archive | Long-term archive | Lowest | Fees + 12+ hours |

```bash
# Upload với storage class
aws s3 cp myfile.txt s3://my-bucket/ \
  --storage-class STANDARD_IA

# Configure lifecycle rule
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "ArchiveRule",
      "Status": "Enabled",
      "Prefix": "logs/",
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"},
        {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}
      ]
    }]
  }'
```

## Câu hỏi 10: Best practices cho production AWS architecture?

### Câu trả lời

```bash
# 1. Multi-AZ deployment
aws rds create-db-instance \
  --db-instance-identifier my-db \
  --multi-az \
  --db-instance-class db.t3.micro \
  --engine postgres

# 2. Auto Scaling
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 3 \
  --vpc-zone-identifier "subnet-1a,subnet-1b,subnet-1c"

# 3. Load Balancer
aws elbv2 create-load-balancer \
  --name my-lb \
  --subnets subnet-1a subnet-1b subnet-1c \
  --security-groups sg-0123456789abcdef0

# 4. Health checks và failover
aws elbv2 create-target-group \
  --name my-targets \
  --protocol HTTP \
  --port 80 \
  --vpc-id vpc-0123456789abcdef0 \
  --health-check-path /health

# 5. Encryption everywhere
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
  }'

# 6. Backup và DR
aws rds create-db-instance-read-replica \
  --db-instance-identifier my-db-replica \
  --source-db-instance-identifier my-db

# 7. Monitoring
aws cloudwatch put-metric-alarm \
  --alarm-name service-health \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:my-topic \
  --metric-name HealthyHostCount \
  --namespace AWS/ApplicationELB
```

## Related Documents

- [AWS Glossary](../glossary.md)
- [AWS Architecture](../architecture.md)
- [AWS Best Practices](../best-practice.md)
- [AWS Anti-Patterns](../anti-pattern.md)
- [AWS Checklist](../checklist.md)
- [AWS Decision Tree](../decision-tree.md)
