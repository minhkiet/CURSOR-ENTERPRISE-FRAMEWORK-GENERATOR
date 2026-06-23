# AWS Knowledge Base - Anti-Patterns

## Tổng quan

Document này liệt kê các anti-patterns phổ biến khi sử dụng AWS và đề xuất giải pháp thay thế. Mỗi anti-pattern được mô tả chi tiết với ví dụ về cách phát hiện và khắc phục.

## Anti-Pattern 1: Hardcoding AWS Credentials

### Mô tả

Lưu trữ AWS access keys trực tiếp trong code là security risk nghiêm trọng. Credentials có thể bị exposed qua source control và logs.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: Hardcoded credentials
import { S3Client } from "@aws-sdk/client-s3";

const client = new S3Client({
  region: "us-east-1",
  credentials: {
    accessKeyId: "AKIAIOSFODNN7EXAMPLE",
    secretAccessKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  }
});
```

### Giải pháp

```typescript
// ✅ SOLUTION: Use IAM roles
import { S3Client } from "@aws-sdk/client-s3";

// Credentials automatically provided by IAM role
const client = new S3Client({});

export const handler = async (): Promise<void> => {
  // Use client without explicit credentials
};
```

```bash
# ✅ SOLUTION: Use environment variables with proper IAM
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)

# Or use AWS_PROFILE
export AWS_PROFILE=my-profile

# Or use EC2 Instance Profile
# (No credentials needed, handled by metadata service)
```

## Anti-Pattern 2: Using Default VPC

### Mô tả

Default VPC có security settings quá permissive và không phù hợp cho production workloads.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Deploying to default VPC
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --subnet-id subnet-12345678 # Default VPC subnet
```

### Giải pháp

```bash
# ✅ SOLUTION: Create dedicated VPC
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=production-vpc}]'

# Create private subnets
aws ec2 create-subnet \
  --vpc-id vpc-0123456789abcdef0 \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

aws ec2 create-subnet \
  --vpc-id vpc-0123456789abcdef0 \
  --cidr-block 10.0.2.0/24 \
  --availability-zone us-east-1b

# Enable VPC Flow Logs
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-0123456789abcdef0 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flow-logs
```

## Anti-Pattern 3: Not Using Auto Scaling

### Mô tả

Static instance counts không handle variable traffic và có thể lead to downtime hoặc over-provisioning.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Fixed instance count
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --min-size 5 \
  --max-size 5 \
  --desired-capacity 5  # Always 5, regardless of load
```

### Giải pháp

```bash
# ✅ SOLUTION: Configure auto scaling
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name my-asg \
  --policy-name scale-out \
  --adjustment-type PercentChangeInCapacity \
  --scaling-adjustment 25 \
  --cooldown 300

# Scale based on CPU
aws cloudwatch put-metric-alarm \
  --alarm-name cpu-high \
  --alarm-actions arn:aws:autoscaling:us-east-1:123456789012:scalingPolicy:my-asg:policy-name:scale-out \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 70 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2

# Scale based on memory (custom metric)
aws cloudwatch put-metric-alarm \
  --alarm-name memory-high \
  --alarm-actions arn:aws:autoscaling:us-east-1:123456789012:scalingPolicy:my-asg:policy-name:scale-out \
  --metric-name CWAgent/memorial_percent_used \
  --namespace CWAgent \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

## Anti-Pattern 4: Not Configuring RDS Backups

### Mô tả

Databases without backup configuration có risk of data loss.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: No backup configuration
aws rds create-db-instance \
  --db-instance-identifier my-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --allocated-storage 20
# Uses default backup: 1 day retention
```

### Giải pháp

```bash
# ✅ SOLUTION: Configure comprehensive backups
aws rds create-db-instance \
  --db-instance-identifier my-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --allocated-storage 100 \
  --backup-retention-period 30 \
  --backup-window 03:00-04:00 \
  --maintenance-window mon:04:00-mon:05:00 \
  --multi-az \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 31

# Enable auto minor version upgrade
aws rds modify-db-instance \
  --db-instance-identifier my-db \
  --auto-minor-version-upgrade \
  --allow-major-version-upgrade
```

## Anti-Pattern 5: Using Public S3 Buckets Without Restrictions

### Mô tả

Public S3 buckets có thể lead to data breaches và unexpected charges.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Bucket without restrictions
aws s3api create-bucket --bucket my-public-bucket

# Public access block disabled by default
# Anyone can upload/download files
```

### Giải pháp

```bash
# ✅ SOLUTION: Block public access and use bucket policies
aws s3api put-public-access-block \
  --bucket my-private-bucket \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Create restrictive bucket policy
aws s3api put-bucket-policy \
  --bucket my-private-bucket \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Sid": "RestrictAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-private-bucket/*"
      ],
      "Condition": {
        "Bool": {"aws:SecureTransport": false}
      }
    }]
  }'

# Use presigned URLs for temporary access
aws s3 presign s3://my-private-bucket/my-file.txt --expires-in 3600
```

## Anti-Pattern 6: Not Implementing Security Groups Least Privilege

### Mô tả

Security groups với wide-open rules như 0.0.0.0/0 cho all traffic.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Overly permissive security group
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol all \
  --cidr 0.0.0.0/0
```

### Giải pháp

```bash
# ✅ SOLUTION: Least privilege security groups
# Web server security group
aws ec2 create-security-group \
  --group-name web-sg \
  --description "Security group for web servers"

# Allow only HTTPS from anywhere
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# Allow HTTP from ALB only
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 80 \
  --source-group sg-11111111 # ALB security group

# Database security group
aws ec2 create-security-group \
  --group-name db-sg \
  --description "Security group for database"

# Allow only from web servers
aws ec2 authorize-security-group-ingress \
  --group-id sg-22222222 \
  --protocol tcp \
  --port 3306 \
  --source-group sg-0123456789abcdef0 # Web servers only!
```

## Anti-Pattern 7: Not Using CloudWatch Logs

### Mô tả

Applications without logging make debugging và monitoring impossible.

### Ví dụ xấu

```typescript
// ❌ ANTI-PATTERN: No logging
export const handler = async (event) => {
  processOrder(event);
  // No logs, no visibility into what happened
  return { statusCode: 200 };
};
```

### Giải pháp

```typescript
// ✅ SOLUTION: Comprehensive logging
import { Logger } from "@aws-lambda-powertools/logger";
import { Metrics } from "@aws-lambda-powertools/metrics";
import { Tracer } from "@aws-lambda-powertools/tracer";

const logger = new Logger();
const metrics = new Metrics();
const tracer = new Tracer();

export const handler = tracer.captureLambdaHandler(async (event) => {
  const orderId = event.orderId;
  
  logger.info("Processing order", { orderId });
  metrics.addMetric("OrderProcessed", "Count", 1);
  
  try {
    tracer.putAnnotation("OrderId", orderId);
    
    const result = await processOrder(event);
    
    logger.info("Order processed successfully", {
      orderId,
      result
    });
    
    metrics.addMetric("OrderSuccess", "Count", 1);
    
    return { statusCode: 200, body: JSON.stringify(result) };
    
  } catch (error) {
    logger.error("Order processing failed", {
      orderId,
      error: error.message
    });
    
    metrics.addMetric("OrderFailure", "Count", 1);
    
    throw error;
  }
});
```

## Anti-Pattern 8: Not Using AWS Organizations for Multi-Account

### Mô tả

All resources in single account leads to security, billing, và operational challenges.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Everything in one account
# Production workloads, dev experiments, personal projects all mixed
# - Security risks
# - Cost tracking difficult
# - Permission management complex
```

### Giải pháp

```bash
# ✅ SOLUTION: Use AWS Organizations
# Create organization
aws organizations create-organization \
  --feature-set ALL

# Create organizational units (OUs)
aws organizations create-organizational-unit \
  --parent-id r-xxxxx \
  --name Production

aws organizations create-organizational-unit \
  --parent-id r-xxxxx \
  --name Development

# Create accounts
aws organizations create-account \
  --email prod@example.com \
  --account-name "Production Account" \
  --parent-id ou-xxxxx-12345678

# Enable SCPs at OU level
aws organizations put-scp-entitlement \
  --policy-id p-xxxxx \
  --target-id ou-xxxxx-12345678 \
  --permission-type FULL
```

## Anti-Pattern 9: Not Using Cost Allocation Tags

### Mô tả

Without tags, tracking costs by team, project, hoặc environment is impossible.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: No tags on resources
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro
# Resources created without cost tracking
```

### Giải pháp

```bash
# ✅ SOLUTION: Use cost allocation tags
# Enable tags at account level
aws organizations enable-policy-type \
  --root-id r-xxxxx \
  --policy-type TAG_POLICY

# Create tag policy
aws organizations create-policy \
  --content '{
    "tags": {
      "CostCenter": {
        "tag_key": "CostCenter",
        "enforced_for": ["ec2:instance", "s3:bucket"]
      },
      "Environment": {
        "tag_key": "Environment",
        "enforced_for": ["ec2:instance"]
      }
    }
  }' \
  --description "Require cost tracking tags" \
  --name tag-policy

# Attach tag policy to root
aws organizations attach-policy \
  --policy-id p-xxxxx \
  --target-id r-xxxxx

# Tag resources at creation
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=CostCenter,Value=CC-1234},{Key=Environment,Value=Production},{Key=Project,Value=MyApp}]'
```

## Anti-Pattern 10: Not Implementing Encryption at Rest

### Mô tả

Unencrypted data at rest có risk of unauthorized access if storage is compromised.

### Ví dụ xấu

```bash
# ❌ ANTI-PATTERN: Unencrypted storage
aws s3api create-bucket \
  --bucket my-unencrypted-bucket

aws rds create-db-instance \
  --storage-encrypted false
```

### Giải pháp

```bash
# ✅ SOLUTION: Enable encryption everywhere
# S3 encryption
aws s3api put-bucket-encryption \
  --bucket my-encrypted-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# RDS encryption
aws rds create-db-instance \
  --storage-encrypted \
  --kms-key-id alias/my-kms-key

# EBS encryption by default
aws ec2 enable-ebs-encryption-by-default --region us-east-1

# Lambda environment encryption
aws lambda create-function \
  --kms-key-arn arn:aws:kms:us-east-1:123456789012:key/my-key
```

## Related Documents

- [AWS Glossary](../glossary.md)
- [AWS Architecture](../architecture.md)
- [AWS Best Practices](../best-practice.md)
- [AWS Checklist](../checklist.md)
- [AWS FAQ](../faq.md)
- [AWS Decision Tree](../decision-tree.md)
