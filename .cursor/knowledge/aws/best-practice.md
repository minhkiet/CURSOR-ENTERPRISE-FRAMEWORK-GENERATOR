# AWS Knowledge Base - Best Practices

## Tổng quan

Document này cung cấp 10+ best practices cho việc sử dụng AWS trong Cursor Enterprise Framework, kèm theo code examples cụ thể cho từng practice.

## Practice 1: Use IAM Roles Thay vì Access Keys

### Mô tả

Sử dụng IAM roles thay vì access keys cho EC2 instances và Lambda functions để tránh hardcoded credentials và improve security.

```bash
# Create IAM role for EC2
aws iam create-role \
  --role-name ec2-s3-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policy
aws iam attach-role-policy \
  --role-name ec2-s3-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create instance profile
aws iam create-instance-profile \
  --instance-profile-name ec2-s3-profile

aws iam add-role-to-instance-profile \
  --role-name ec2-s3-role \
  --instance-profile-name ec2-s3-profile

# Launch instance with role
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --iam-instance-profile Name=ec2-s3-profile
```

```typescript
// Lambda function using IAM role (no credentials needed)
import { S3Client, ListBucketsCommand } from "@aws-sdk/client-s3";

export const handler = async (): Promise<void> => {
  // IAM role provides credentials automatically
  const client = new S3Client({});
  const command = new ListBucketsCommand({});
  const response = await client.send(command);
  
  console.log("Buckets:", response.Buckets);
};
```

## Practice 2: Implement VPC Security Best Practices

### Mô tả

Sử dụng security groups, NACLs, và private subnets để secure network infrastructure.

```bash
# Create VPC
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=my-vpc}]'

# Create private subnets
aws ec2 create-subnet \
  --vpc-id vpc-0123456789abcdef0 \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a \
  --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=private-subnet-1}]'

# Create security group
aws ec2 create-security-group \
  --group-name my-security-group \
  --description "My security group" \
  --vpc-id vpc-0123456789abcdef0

# Add rules (restrictive)
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 443 \
  --cidr 10.0.0.0/16

aws ec2 authorize-security-group-egress \
  --group-id sg-0123456789abcdef0 \
  --protocol all \
  --cidr 0.0.0.0/0
```

```bash
# Create NAT Gateway for private subnet internet access
aws ec2 create-nat-gateway \
  --subnet-id subnet-0123456789abcdef0 \
  --allocation-id eip-0123456789abcdef0

# Update route table for private subnet
aws ec2 create-route \
  --route-table-id rtb-0123456789abcdef0 \
  --destination-cidr-block 0.0.0.0/0 \
  --nat-gateway-id nat-0123456789abcdef0
```

## Practice 3: Use S3 Best Practices

### Mô tả

Configure S3 với appropriate bucket policies, encryption, và lifecycle rules.

```bash
# Create S3 bucket with versioning and encryption
aws s3api create-bucket \
  --bucket my-unique-bucket-name \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-unique-bucket-name \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket my-unique-bucket-name \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Create bucket policy (restrict access)
aws s3api put-bucket-policy \
  --bucket my-unique-bucket-name \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Sid": "RestrictAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::my-unique-bucket-name/*"],
      "Condition": {
        "Bool": {"aws:SecureTransport": false}
      }
    }]
  }'

# Configure lifecycle rule
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-unique-bucket-name \
  --lifecycle-configuration '{
    "Rules": [{
      "ID": "archive-old-objects",
      "Status": "Enabled",
      "Filter": {"Prefix": "logs/"},
      "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 365}
    }]
  }'
```

## Practice 4: Use Auto Scaling

### Mô tả

Implement Auto Scaling groups để maintain availability và reduce costs.

```bash
# Create launch template
aws ec2 create-launch-template \
  --launch-template-name my-template \
  --version-description "Version 1" \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.micro \
  --key-name my-key-pair \
  --security-group-ids sg-0123456789abcdef0 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-instance}]'

# Create Auto Scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name my-asg \
  --launch-template LaunchTemplateName=my-template,Version=1 \
  --min-size 2 \
  --max-size 10 \
  --desired-capacity 3 \
  --vpc-zone-identifier "subnet-0123456789abcdef0,subnet-0abcdef1234567890" \
  --health-check-type EC2 \
  --health-check-period 300 \
  --new-instances-protected-from-scale-in

# Create scaling policies
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name my-asg \
  --policy-name scale-out \
  --scaling-adjustment 2 \
  --adjustment-type ChangeInCapacity

aws autoscaling put-scaling-policy \
  --auto-scaling-group-name my-asg \
  --policy-name scale-in \
  --scaling-adjustment -1 \
  --adjustment-type ChangeInCapacity

# Create CloudWatch alarm for scale out
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
```

## Practice 5: Use AWS Secrets Manager

### Mô tả

Store sensitive information như database credentials và API keys trong Secrets Manager.

```bash
# Create secret
aws secretsmanager create-secret \
  --name my-database-password \
  --description "Production database password" \
  --secret-string '{"username":"dbadmin","password":"mypassword123"}'

# Create secret with automatic rotation
aws secretsmanager create-secret \
  --name my-api-key \
  --secret-string '{"apiKey":"myapikey123"}'

# Enable automatic rotation (Lambda required)
aws lambda create-function \
  --function-name rotate-secret \
  --runtime python3.9 \
  --role arn:aws:iam::123456789012:role/lambda-secret-rotation \
  --handler rotate.handler \
  --zip-file fileb://rotation-function.zip

aws secretsmanager rotate-secret \
  --secret-id my-api-key \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:rotate-secret
```

```typescript
// Retrieve secret in Lambda
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";

const client = new SecretsManagerClient({});

export const handler = async (): Promise<void> => {
  const command = new GetSecretValueCommand({
    SecretId: "my-database-password"
  });
  
  const response = await client.send(command);
  const secret = JSON.parse(response.SecretString!);
  
  // Use secret.username and secret.password
  console.log("Username:", secret.username);
};
```

## Practice 6: Implement Multi-Factor Authentication (MFA)

### Mô tả

Enable MFA cho all IAM users để improve account security.

```bash
# Enable MFA for IAM user
aws iam create-virtual-mfa-device \
  --virtual-mfa-device-name my-mfa-device \
  --outfile ./mfacode.png \
  --bootstrap-method QRCodePNG

# Associate MFA with user
aws iam enable-mfa-device \
  --user-name my-user \
  --serial-number arn:aws:iam::123456789012:mfa/my-mfa-device \
  --authentication-code1 123456 \
  --authentication-code2 789012

# Enforce MFA policy
aws iam create-policy \
  --policy-name enforce-mfa \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "AllowViewAccountInfo",
        "Effect": "Allow",
        "Action": "iam:ListUsers",
        "Resource": "*"
      },
      {
        "Sid": "RequireMFA",
        "Effect": "Allow",
        "Action": "ec2:*",
        "Resource": "*",
        "Condition": {
          "Bool": {"aws:MultiFactorAuthPresent": true}
        }
      }
    ]
  }'
```

## Practice 7: Use CloudWatch for Monitoring

### Mô tả

Implement comprehensive monitoring với CloudWatch metrics, logs, và alarms.

```bash
# Create CloudWatch dashboard
aws cloudwatch put-dashboard \
  --dashboard-name my-dashboard \
  --dashboard-body '{
    "widgets": [{
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/EC2", "CPUUtilization", {"stat": "Average"}],
          [".", "NetworkIn", {"stat": "Sum"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "EC2 Metrics"
      }
    }]
  }'

# Create log group
aws logs create-log-group \
  --log-group-name /aws/lambda/my-function

# Create metric filter
aws logs put-metric-filter \
  --log-group-name /aws/lambda/my-function \
  --filter-name error-count \
  --metric-transformations '[
    {"metricName": "ErrorCount", "metricNamespace": "MyApp", "metricValue": "1"}
  ]' \
  --filter-pattern "ERROR"

# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name lambda-errors \
  --alarm-description "Lambda function has errors" \
  --metric-name ErrorCount \
  --namespace MyApp \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:my-topic
```

## Practice 8: Use AWS CloudTrail for Audit

### Mô tả

Enable CloudTrail để track user activity và API usage.

```bash
# Create CloudTrail
aws cloudtrail create-trail \
  --name my-trail \
  --s3-bucket-name my-cloudtrail-bucket \
  --is-multi-region-trail \
  --enable-log-file-validation \
  --include-global-service-events

# Start logging
aws cloudtrail start-logging \
  --name my-trail

# Create SNS topic for notifications
aws sns create-topic \
  --name my-cloudtrail-alerts

# Add CloudWatch Logs integration
aws cloudtrail update-trail \
  --name my-trail \
  --cloud-watch-logs-log-group-arn arn:aws:logs:us-east-1:123456789012:log-group:my-cloudtrail-logs:* \
  --cloud-watch-logs-role-arn arn:aws:iam::123456789012:role/CloudTrail_CloudWatchLogs_Role
```

## Practice 9: Use Parameter Store for Configuration

### Mô tả

Store configuration data như database connection strings và feature flags trong Parameter Store.

```bash
# Create parameter (String)
aws ssm put-parameter \
  --name /my-app/database/host \
  --value "mydb.xyz.us-east-1.rds.amazonaws.com" \
  --type String

# Create parameter (SecureString)
aws ssm put-parameter \
  --name /my-app/database/password \
  --value "mypassword123" \
  --type SecureString

# Create parameter with KMS key
aws ssm put-parameter \
  --name /my-app/api-key \
  --value "myapikey123" \
  --type SecureString \
  --key-id alias/my-kms-key

# Get parameter
aws ssm get-parameter \
  --name /my-app/database/host

# Get parameter with decryption
aws ssm get-parameter \
  --name /my-app/database/password \
  --with-decryption
```

```typescript
// Get parameters in Lambda
import { SSMClient, GetParametersCommand } from "@aws-sdk/client-ssm";

const client = new SSMClient({});

export const handler = async (): Promise<void> => {
  const command = new GetParametersCommand({
    Names: [
      "/my-app/database/host",
      "/my-app/database/password"
    ],
    WithDecryption: true
  });
  
  const response = await client.send(command);
  
  const params: Record<string, string> = {};
  for (const param of response.Parameters!) {
    params[param.Name!] = param.Value!;
  }
  
  console.log("DB Host:", params["/my-app/database/host"]);
};
```

## Practice 10: Implement Cost Optimization

### Mô tả

Use cost optimization strategies để reduce AWS spending.

```bash
# Create budget
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "monthly-cost",
    "BudgetLimit": {"Amount": "1000", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "ComparisonOperator": "GREATER_THAN",
      "NotificationType": "ACTUAL",
      "Threshold": 80,
      "ThresholdType": "ABSOLUTE_VALUE"
    },
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "billing@example.com"}]
  }]'

# Create Cost Anomaly Detection
aws cost-management create-anomaly-detector \
  --anomaly-subscription-arn arn:aws:cost-optimization:...

# Enable S3 Intelligent-Tiering
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket my-unique-bucket-name \
  --id my-config \
  --intelligent-tiering-configuration '{
    "Id": "my-config",
    "Status": "Enabled",
    "Tierings": [
      {"Days": 0, "AccessTier": "FREQUENT_ACCESS"},
      {"Days": 30, "AccessTier": "STANDARD_ACCESS"},
      {"Days": 60, "AccessTier": "INFREQUENT_ACCESS"},
      {"Days": 90, "AccessTier": "ARCHIVE_ACCESS"},
      {"Days": 180, "AccessTier": "DEEP_ARCHIVE_ACCESS"}
    ]
  }'

# Schedule auto-stop for development instances
aws events put-rule \
  --name stop-dev-instances \
  --schedule-expression "cron(0 18 ? * MON-FRI *)" \
  --state ENABLED

aws events put-targets \
  --rule stop-dev-instances \
  --targets '[{"Id": "1", "Arn": "arn:aws:lambda:us-east-1:123456789012:function:stop-instances"}]'
```

## Related Documents

- [AWS Glossary](../glossary.md)
- [AWS Architecture](../architecture.md)
- [AWS Anti-Patterns](../anti-pattern.md)
- [AWS Checklist](../checklist.md)
- [AWS FAQ](../faq.md)
- [AWS Decision Tree](../decision-tree.md)
