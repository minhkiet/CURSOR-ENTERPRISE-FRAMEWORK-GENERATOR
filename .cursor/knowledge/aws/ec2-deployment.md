---
title: "AWS EC2 Deployment Best Practices"
description: "Hướng dẫn toàn diện về triển khai EC2 với Auto Scaling, Load Balancing, Launch Templates và Spot Instances cho enterprise workloads"
tags: ["aws", "ec2", "auto-scaling", "load-balancing", "alb", "nlb", "spot-instances", "launch-templates"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# AWS EC2 Deployment Best Practices

## Tổng Quan (Overview)

Amazon Elastic Compute Cloud (EC2) là nền tảng cốt lõi của AWS, cung cấp khả năng compute linh hoạt và có thể mở rộng trong cloud. Trong môi trường enterprise, việc triển khai EC2 đòi hỏi các best practices về high availability, scalability, cost optimization và security. Tài liệu này sẽ hướng dẫn chi tiết về cách thiết lập Auto Scaling Groups (ASG), Application Load Balancer (ALB), Network Load Balancer (NLB), Launch Templates, và tận dụng Spot Instances để tối ưu chi phí.

EC2 là dịch vụ foundation cho hầu hết các architecture patterns trên AWS, từ simple web applications đến complex distributed systems. Việc nắm vững các khái niệm và best practices liên quan đến EC2 là điều kiện tiên quyết để xây dựng hệ thống enterprise-grade.

## Mục Đích (Purpose)

Mục đích của tài liệu này bao gồm:

1. **High Availability**: Thiết lập multi-AZ deployment để đảm bảo uptime và fault tolerance
2. **Scalability**: Tự động scale resources theo demand sử dụng Auto Scaling
3. **Cost Optimization**: Sử dụng Spot Instances và Reserved Instances hiệu quả
4. **Security**: Áp dụng security best practices từ network đến instance level
5. **Operational Excellence**: Thiết lập monitoring, logging và incident response

Việc kết hợp các thành phần này một cách hợp lý sẽ tạo ra một hệ thống có khả năng chịu lỗi cao, có thể mở rộng theo nhu cầu, và tối ưu về chi phí vận hành.

## Các Khái Niệm Chính (Key Concepts)

### 1. Instance Types và Families

AWS cung cấp nhiều instance families cho các use cases khác nhau:

| Family | Use Case | Ví Dụ |
|--------|----------|-------|
| General Purpose (T, M) | Web servers, dev environments | t3.medium, m5.large |
| Compute Optimized (C) | Batch processing, gaming | c5.xlarge, c6i.2xlarge |
| Memory Optimized (R, X) | Databases, caching | r6i.xlarge, x2gd.2xlarge |
| Storage Optimized (I, D) | Data warehousing, NoSQL | i3en.3xlarge, d3.xlarge |
| Accelerated Computing (P, G) | ML/AI, graphics | p4d.24xlarge, g4dn.xlarge |

Khi chọn instance type, cần cân nhắc các yếu tố:
- **vCPU**: Số lượng virtual CPUs
- **Memory**: Dung lượng RAM (GB)
- **Network Performance**: Bandwidth capability (Low, Moderate, High, 10Gbps, 100Gbps)
- **Storage**: Loại và dung lượng local storage

### 2. Auto Scaling Groups (ASG)

ASG là thành phần core cho elasticity trong EC2 deployments. ASG duy trì số lượng instances trong một specified range và tự động thêm hoặc bớt instances dựa trên scaling policies.

**Các Scaling Policies chính:**

```yaml
# CloudFormation snippet cho Auto Scaling Group
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  MyAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      LaunchTemplate:
        LaunchTemplateId: !Ref MyLaunchTemplate
        Version: !GetAtt MyLaunchTemplate.LatestVersionNumber
      HealthCheckType: ELB
      HealthCheckGracePeriod: 300
      Tags:
        - Key: Name
          Value: !Sub '${AWS::StackName}-instance'
          PropagateAtLaunch: true
```

**Target Tracking Scaling Policy:**
```yaml
MyTargetTrackingPolicy:
  Type: AWS::AutoScaling::ScalingPolicy
  Properties:
    AutoScalingGroupName: !Ref MyAutoScalingGroup
    PolicyType: TargetTrackingScaling
    TargetTrackingConfiguration:
      PredefinedMetricSpecification:
        PredefinedMetricType: ASGAverageCPUUtilization
      TargetValue: 70
      DisableScaleIn: false
```

### 3. Application Load Balancer (ALB)

ALB hoạt động ở Layer 7 (Application layer) và hỗ trợ content-based routing, perfect cho microservices architectures.

```yaml
# ALB với Target Groups
Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: my-alb
      Scheme: internet-facing
      SecurityGroups:
        - !Ref ALBSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      LoadBalancerAttributes:
        - Key: idle_timeout.timeout_seconds
          Value: '60'

  WebTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: web-tg
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VPC
      Matcher:
        HttpCode: '200-299'
      HealthCheckIntervalSeconds: 30
      HealthCheckPath: /health
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3

  Listener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 443
      Protocol: HTTPS
      Certificates:
        - CertificateArn: !Ref Certificate
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref WebTargetGroup
```

### 4. Network Load Balancer (NLB)

NLB hoạt động ở Layer 4, cung cấp ultra-low latency và support cho TCP/UDP traffic, lý tưởng cho high-performance workloads.

```yaml
# NLB cho high-performance applications
NetworkLoadBalancer:
  Type: AWS::ElasticLoadBalancingV2::LoadBalancer
  Properties:
    Name: my-nlb
    Scheme: internet-facing
    Type: network
    Subnets:
      - !Ref PublicSubnet1
      - !Ref PublicSubnet2
    Tags:
      - Key: Environment
        Value: Production
```

### 5. Launch Templates

Launch Templates thay thế Launch Configurations với nhiều tính năng ưu việt hơn như versioning, parameter references, và nested stacks.

```yaml
# Launch Template đầy đủ
Resources:
  MyLaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: !Sub '${AWS::StackName}-lt'
      LaunchTemplateData:
        ImageId: ami-0c55b159cbfafe1f0
        InstanceType: t3.medium
        KeyName: !Ref KeyPair
        SecurityGroupIds:
          - !Ref InstanceSecurityGroup
        UserData:
          Fn::Base64: |
            #!/bin/bash
            yum update -y
            yum install -y httpd
            systemctl start httpd
            systemctl enable httpd
            echo "Hello from EC2" > /var/www/html/index.html
        IamInstanceProfile:
          Arn: !GetAtt InstanceProfile.Arn
        Monitoring:
          Enabled: true
        MetadataOptions:
          HttpTokens: required
          HttpPutResponseHopLimit: 1
          HttpEndpoint: enabled
        EnclaveOptions:
          Enabled: true
      TagSpecifications:
        - ResourceType: instance
          Tags:
            - Key: Environment
              Value: !Ref Environment
            - Key: Application
              Value: !Ref Application
```

### 6. Spot Instances

Spot Instances cung cấp discount lên đến 90% so với On-Demand nhưng có thể bị interrupted bất cứ lúc nào khi EC2 cần lại capacity.

```yaml
# Spot Instance với Spot Fleet
SpotFleet:
  Type: AWS::EC2::SpotFleet
  Properties:
    SpotFleetRequestConfigData:
      IAMFleetRole: !GetAtt SpotFleetRole.Arn
      TargetCapacity: 10
      AllocationStrategy: lowestPrice
      InstancePoolsToUsePublic: 1
      LaunchSpecifications:
        - InstanceType: m5.large
          ImageId: ami-0c55b159cbfafe1f0
          SubnetId: !Ref PrivateSubnet1
          WeightedCapacity: 1
          SpotPrice: 0.05
        - InstanceType: m5.xlarge
          ImageId: ami-0c55b159cbfafe1f0
          SubnetId: !Ref PrivateSubnet2
          WeightedCapacity: 2
          SpotPrice: 0.10
      TerminateInstancesWithExpiration: true
      ValidFrom: !Ref ValidFrom
      ValidUntil: !Ref ValidUntil
```

## Best Practices

### 1. Thiết kế cho High Availability

**Multi-AZ Deployment:**
```bash
# Tạo Auto Scaling Group spread across 3 AZs
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name production-asg \
  --launch-template "launch-template-id=lt-0123456789abcdef" \
  --min-size 3 \
  --max-size 9 \
  --desired-capacity 3 \
  --vpc-zone-identifier "subnet-abc123,subnet-def456,subnet-ghi789" \
  --health-check-type ELB \
  --health-check-grace-period 300 \
  --default-cooldown 300 \
  --termination-policies "OldestInstance" \
  --new-instances-protected-from-scale-in
```

**Placement Groups:**
```bash
# Tạo Spread Placement Group cho critical instances
aws ec2 create-placement-group \
  --group-name production-spread \
  --strategy spread

# Launch instances trong Spread Placement Group
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type c5.xlarge \
  --placement "GroupName=production-spread" \
  --key-name my-keypair
```

### 2. Security Best Practices

**Instance Profile và IAM Roles:**
```bash
# Tạo IAM Role cho EC2
aws iam create-role \
  --role-name ec2-s3-access-role \
  --assume-role-policy-document file://trust-policy.json

# Trust policy (trust-policy.json)
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Tạo Instance Profile
aws iam create-instance-profile \
  --instance-profile-name s3-access-profile

aws iam add-role-to-instance-profile \
  --role-name ec2-s3-access-role \
  --instance-profile-name s3-access-profile
```

**Security Groups với Principle of Least Privilege:**
```yaml
# restrictive security groups
WebServerSG:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Security group for web servers
    VpcId: !Ref VPC
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        CidrIp: 0.0.0.0/0
        Description: HTTPS from anywhere
      - IpProtocol: tcp
        FromPort: 80
        ToPort: 80
        CidrIp: 0.0.0.0/0
        Description: HTTP from ALB only
        SourceSecurityGroupId: !Ref ALBSecurityGroup
```

### 3. Cost Optimization

**Reserved Instances và Savings Plans:**
```bash
# Mua Reserved Instance (1 year, No Upfront)
aws ec2 purchase-reserved-instances-offering \
  --reserved-instances-offering-id offering-id \
  --instance-count 5

# Convertible Reserved Instance
aws ec2 purchase-reserved-instances-offering \
  --reserved-instances-offering-id offering-id \
  --instance-count 3 \
  --instance-match-criteria open

# Kiểm tra Reserved Instance coverage
aws ec2 describe-reserved-instances-coverage \
  --query 'ReservedInstancesCoverages[?CoveragePercentage<`100`].[InstanceType,AvailabilityZone,CoveragePercentage]'
```

**Spot Instance Strategies:**
```python
# Python script để handle Spot interruption
import subprocess
import signal
import sys

def signal_handler(signum, frame):
    """Handle Spot interruption gracefully"""
    print("Received termination signal, gracefully shutting down...")
    # Stop application
    subprocess.run(["systemctl", "stop", "myapp"])
    # Upload logs to S3
    subprocess.run(["aws", "s3", "sync", "/var/log/myapp", "s3://my-bucket/logs/"])
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
```

### 4. Performance Optimization

**Enhanced Networking:**
```bash
# Enable ENA cho high-throughput networking
aws ec2 modify-instance-attribute \
  --instance-id i-1234567890abcdef0 \
  --ena-support

# Enable Elastic Fabric Adapter
aws ec2 modify-instance-attribute \
  --instance-id i-1234567890abcdef0 \
  --efa
```

**Storage Optimization:**
```bash
# Attach NVMe SSD với instance store
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type i3en.2xlarge \
  --block-device-mappings \
    DeviceName=/dev/sda1,Ebs="{VolumeSize=100,VolumeType=gp3,DeleteOnTermination=true,Iops=3000,Throughput=125}"
```

## Common Patterns

### Pattern 1: Blue-Green Deployment với ASG

```yaml
# Blue-Green deployment sử dụng ASG và ELB
Resources:
  BlueASG:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      VPCZoneIdentifier: !Ref PrivateSubnets
      MinSize: 2
      MaxSize: 4
      DesiredCapacity: 2
      LaunchTemplate:
        LaunchTemplateId: !Ref BlueLaunchTemplate
        Version: !GetAtt BlueLaunchTemplate.LatestVersionNumber
      HealthCheckType: ELB
      TargetGroupARNs:
        - !Ref BlueTargetGroup

  GreenASG:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      VPCZoneIdentifier: !Ref PrivateSubnets
      MinSize: 0
      MaxSize: 4
      DesiredCapacity: 0
      LaunchTemplate:
        LaunchTemplateId: !Ref GreenLaunchTemplate
        Version: !GetAtt GreenLaunchTemplate.LatestVersionNumber
      HealthCheckType: ELB
      TargetGroupARNs:
        - !Ref GreenTargetGroup

  TrafficSwitch:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      ListenerArn: !Ref HTTPSListener
      Priority: 100
      Conditions:
        - Field: path-pattern
          Values: ['/api/*']
      Actions:
        - Type: forward
          TargetGroupArn: !Ref GreenTargetGroup
```

### Pattern 2: Spot Fleet với On-Demand Fallback

```yaml
# Mixed instances policy với Spot và On-Demand
Resources:
  MixedASG:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      VPCZoneIdentifier: !Ref PrivateSubnets
      MinSize: 2
      MaxSize: 20
      DesiredCapacity: 6
      MixedInstancesPolicy:
        LaunchTemplate:
          LaunchTemplateId: !Ref LaunchTemplate
          Override:
            - InstanceType: m5.large
              WeightedCapacity: 1
            - InstanceType: m5.xlarge
              WeightedCapacity: 2
            - InstanceType: m5.2xlarge
              WeightedCapacity: 4
        InstancesDistribution:
          OnDemandPercentageAboveBaseCapacity: 30
          SpotAllocationStrategy: lowest-price
          SpotInstancePoolsToUsePublic: 2
          SpotMaxPrice: ""
      HealthCheckType: ELB
```

### Pattern 3: Bastion Host với Systems Manager Session Manager

```yaml
# Thay thế Bastion Host bằng Systems Manager
Resources:
  SSMIAMRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
        - arn:aws:iam::aws:policy/AmazonSSMDirectoryServiceAccess
        - arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy

  InstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Path: /
      Roles:
        - !Ref SSMIAMRole
```

```bash
# Kết nối đến instance qua Session Manager
aws ssm start-session --target i-1234567890abcdef0

# Start session với port forwarding
aws ssm start-session \
  --target i-1234567890abcdef0 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["database.internal"],"portNumber":["5432"],"localPortNumber":["5432"]}'
```

## Troubleshooting

### Common Issues và Solutions

**1. Instance không pass Health Check**

```bash
# Kiểm tra health check status
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:region:123456789012:targetgroup/my-tg/abc123

# Debug với detailed health check
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:region:123456789012:targetgroup/my-tg/abc123 \
  --targets Id=i-1234567890abcdef0

# Common causes và fixes:
# - Security group không cho phép health check: Thêm rule cho ELB SG
# - Application không listen trên correct port: Kiểm tra app config
# - Health check path không đúng: Update health check configuration
# - Instance out of capacity: Check CloudWatch metrics
```

**2. Auto Scaling không scale**

```bash
# Check scaling activities
aws autoscaling describe-scaling-activities \
  --auto-scaling-group-name production-asg \
  --max-records 10

# Kiểm tra metric data
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=AutoScalingGroupName,Value=production-asg \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T12:00:00Z \
  --period 300 \
  --statistics Average

# Check if scaling is blocked
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names production-asg \
  --query 'AutoScalingGroups[0].SuspendedProcesses'
```

**3. Spot Instance Interruption**

```bash
# Xem Spot instance request status
aws ec2 describe-spot-instance-requests \
  --filters "Name=state,Values=active"

# Check for interruption warnings in logs
# Spot instances nhận notification 2 phút trước khi bị interrupt
# Instance metadata cung cấp:
# - instance-action: action sẽ được thực hiện (stop/terminate)
# - spot-instance-action: tương tự

# Kiểm tra interruption warning
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/spot/instance-action

# Enable Spot instance interruption handling
#!/bin/bash
while true; do
  ACTION=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
    http://169.254.169.254/latest/meta-data/spot/instance-action)
  if [ "$ACTION" != "" ]; then
    logger "Spot interruption: $ACTION"
    # Gracefully shutdown application
    /opt/myapp/shutdown.sh
    # Upload state to S3
    aws s3 sync /data s3://my-bucket/state/
    break
  fi
  sleep 5
done
```

**4. High Latency từ Load Balancer**

```bash
# Kiểm tra ALB metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name TargetResponseTime \
  --dimensions Name=LoadBalancer,Value=app/my-alb/1234567890abcdef \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T12:00:00Z \
  --period 60 \
  --statistics Average,Maximum,p95

# Check NLB metrics cho throughput
aws cloudwatch get-metric-statistics \
  --namespace AWS/NetworkELB \
  --metric-name ActiveFlowCount \
  --dimensions Name=LoadBalancer,Value=net/my-nlb/1234567890abcdef \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T12:00:00Z \
  --period 60 \
  --statistics Average,Maximum
```

## Examples

### Example 1: Complete VPC Infrastructure với EC2

```terraform
# Terraform code cho complete infrastructure
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
    Name = "production-vpc"
  }
}

# Subnets
resource "aws_subnet" "private_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = false

  tags = {
    Name = "private-subnet-1a"
    Tier = "private"
  }
}

resource "aws_subnet" "private_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = false

  tags = {
    Name = "private-subnet-1b"
    Tier = "private"
  }
}

resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.101.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-1a"
    Tier = "public"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

# NAT Gateway
resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_1.id

  tags = {
    Name = "main-nat"
  }
}

# Route Tables
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name = "private-rt"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}

# Security Group
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS"
  }

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    cidr_blocks     = ["0.0.0.0/0"]
    description     = "HTTP"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web-security-group"
  }
}

# ALB
resource "aws_lb" "main" {
  name               = "main-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = [aws_subnet.public_1.id, aws_subnet.public_2.id]

  enable_deletion_protection = false

  tags = {
    Name = "main-alb"
  }
}

resource "aws_lb_target_group" "web" {
  name     = "web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# IAM Role cho EC2
resource "aws_iam_role" "ec2_role" {
  name = "ec2-s3-role"

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

resource "aws_iam_role_policy_attachment" "s3_access" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# Launch Template
resource "aws_launch_template" "web" {
  name                   = "web-launch-template"
  image_id               = var.ami_id
  instance_type          = "t3.medium"
  key_name               = var.key_name
  iam_instance_associate = aws_iam_instance_profile.ec2_profile.name

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
  }))

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  monitoring {
    enabled = true
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "web-instance"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  name                = "web-asg"
  vpc_zone_identifier = [aws_subnet.private_1.id, aws_subnet.private_2.id]
  min_size            = 2
  max_size            = 10
  desired_capacity    = 2
  health_check_type   = "ELB"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "web-asg-instance"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "web-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 70
  alarm_description   = "Scale up when CPU > 70%"

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }

  alarm_actions = [aws_autoscaling_policy.scale_up.arn]
}

# User data script
# user_data.sh
#!/bin/bash
yum update -y
yum install -y httpd php mysql
systemctl start httpd
systemctl enable httpd
echo "<?php phpinfo(); ?>" > /var/www/html/info.php
aws s3 cp s3://my-bucket/config /etc/myapp/config --recursive
```

### Example 2: Spot Fleet với Cost Optimization

```bash
#!/bin/bash
# Script để request Spot Fleet với optimal allocation

# Define instance types và weights
INSTANCE_TYPES='{
  "m5.large": {"Zone": "us-east-1a", "Weight": 1},
  "m5.xlarge": {"Zone": "us-east-1b", "Weight": 2},
  "c5.xlarge": {"Zone": "us-east-1a", "Weight": 2}
}'

# Calculate total capacity needed
DESIRED_CAPACITY=20
MIN_SPOT_PERCENTAGE=70

# Get current Spot prices
for instance_type in m5.large m5.xlarge c5.xlarge; do
  price=$(aws ec2 describe-spot-price-history \
    --instance-types $instance_type \
    --product-descriptions "Linux/UNIX" \
    --availability-zone us-east-1a \
    --start-time $(date +%Y-%m-%dT%H:%M:%S) \
    --max-results 1 \
    --query 'SpotPriceHistory[0].SpotPrice' \
    --output text)
  echo "$instance_type: $price"
done

# Create Spot Fleet request
aws ec2 request-spot-fleet \
  --spot-fleet-request-config file://spot-fleet-config.json

# spot-fleet-config.json
cat > spot-fleet-config.json << 'EOF'
{
  "SpotFleetRequestConfig": {
    "IAMFleetRole": "arn:aws:iam::123456789012:role/aws-ec2-spot-fleet-role",
    "TargetCapacity": 20,
    "SpotMaintenanceStrategies": {
      "CapacityRebalance": {
        "ReplacementStrategy": "launch"
      }
    },
    "AllocationStrategy": "lowestPrice",
    "InstancePoolsToUseCount": 3,
    "LaunchSpecifications": [
      {
        "InstanceType": "m5.large",
        "ImageId": "ami-0c55b159cbfafe1f0",
        "SubnetId": "subnet-abc123",
        "WeightedCapacity": 1,
        "SpotPrice": "0.04",
        "SecurityGroups": [
          {
            "GroupId": "sg-0123456789abcdef0"
          }
        ]
      },
      {
        "InstanceType": "m5.xlarge",
        "ImageId": "ami-0c55b159cbfafe1f0",
        "SubnetId": "subnet-def456",
        "WeightedCapacity": 2,
        "SpotPrice": "0.08"
      },
      {
        "InstanceType": "c5.xlarge",
        "ImageId": "ami-0c55b159cbfafe1f0",
        "SubnetId": "subnet-ghi789",
        "WeightedCapacity": 2,
        "SpotPrice": "0.06"
      }
    ],
    "TerminateInstancesWithExpiration": true
  }
}
EOF
```

## References

### Official Documentation
- [Amazon EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Auto Scaling Developer Guide](https://docs.aws.amazon.com/autoscaling/ec2/userguide/)
- [Elastic Load Balancing Documentation](https://docs.aws.amazon.com/elasticloadbalancing/)
- [EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
- [Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/)

### Tools và Resources
- [AWS EC2 Instance Selector](https://github.com/aws/amazon-ec2-instance-selector)
- [AWS Instance Scheduler](https://aws.amazon.com/solutions/implementations/instance-scheduler/)
- [EC2 Rescue for Linux](https://github.com/awslabs/aws-ec2rescue-linux)
- [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)

### Cost Calculators
- [AWS Pricing Calculator](https://calculator.aws/)
- [Savings Plans Recommendations](https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html)
- [Reserved Instance Coverage Report](https://docs.aws.amazon.com/cost-management/aws-cost-explorer/user-guide RI coverage report)

### Well-Architected Framework
- [AWS Well-Architected Framework - Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [AWS Well-Architected Framework - Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)
