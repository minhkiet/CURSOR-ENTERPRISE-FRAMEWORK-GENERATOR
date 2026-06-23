---
title: "AWS ECS Fargate Container Orchestration"
description: "Hướng dẫn toàn diện về Amazon ECS clusters, Fargate tasks, service definitions, task definitions, service connect và secrets management"
tags: ["aws", "ecs", "fargate", "containers", "docker", "task-definition", "service-connect"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# AWS ECS Fargate Container Orchestration

## Tổng Quan (Overview)

Amazon Elastic Container Service (ECS) là một container orchestration service quản lý Docker containers trên AWS, hoạt động mà không cần quản lý underlying infrastructure khi sử dụng Fargate launch type. Fargate là serverless compute engine cho containers, cho phép focus vào application development thay vì infrastructure management.

Tài liệu này cung cấp hướng dẫn chi tiết về việc thiết lập ECS clusters với Fargate, cách define tasks và services, implement service discovery với Service Connect, manage secrets một cách secure, và các best practices cho production deployments. ECS Fargate là lựa chọn phổ biến cho microservices architectures, batch processing, và các application workloads cần containerization mà không muốn quản lý EC2 instances.

ECS được thiết kế để scale với high availability, hỗ trợ deep integration với các AWS services như Application Load Balancer, CloudWatch, IAM, VPC, và Secrets Manager, making it ideal for enterprise-grade container deployments.

## Mục Đích (Purpose)

Mục đích chính của tài liệu này bao gồm:

1. **Infrastructure Abstraction**: Hiểu cách Fargate loại bỏ need cho EC2 management
2. **Task Definition**: Thiết lập task definitions với proper resource allocation và container configs
3. **Service Management**: Deploy và manage services với auto-scaling và health checks
4. **Security**: Implement secrets management, IAM roles, và network isolation
5. **Observability**: Setup logging, monitoring, và tracing cho containerized applications
6. **Networking**: Configure VPC networking, service discovery, và Service Connect

## Các Khái Niệm Chính (Key Concepts)

### 1. ECS Architecture Components

**Cluster**: Logical grouping of tasks/services. Clusters có thể contain both Fargate và EC2 launch types.

**Task Definition**: Blueprint cho containers, tương tự như Dockerfile nhưng cho Docker compose. Defines CPU, memory, port mappings, environment variables, và logging configuration.

**Task**: Running instance của task definition, có thể be standalone hoặc part of a service.

**Service**: Maintains desired task count, automatically replaces failed tasks, và supports load balancing.

```json
{
  "family": "web-application",
  "cpu": "256",
  "memory": "512",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "containerDefinitions": [
    {
      "name": "web",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/web:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:db-credentials:DATABASE_URL::"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/web-application",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "web"
        }
      }
    }
  ]
}
```

### 2. Fargate Resource Allocation

Fargate yêu cầu specify CPU và memory với specific combinations:

| CPU | Memory Options |
|-----|---------------|
| 256 (.25 vCPU) | 512 MB, 1 GB, 2 GB |
| 512 (.5 vCPU) | 1 GB, 2 GB, 3 GB, 4 GB |
| 1024 (1 vCPU) | 2 GB, 3 GB, 4 GB, 5 GB, 6 GB, 7 GB, 8 GB |
| 2048 (2 vCPU) | 4 GB to 16 GB (1 GB increments) |
| 4096 (4 vCPU) | 8 GB to 30 GB (1 GB increments) |

```bash
# Valid Fargate task definitions
aws ecs register-task-definition \
  --family web-app \
  --cpu 1024 \
  --memory 2048 \
  --network-mode awsvpc \
  --requires-compatibilities FARGATE \
  --container-definitions '[{"name":"web","image":"nginx:latest","essential":true}]'
```

### 3. Task Definition Examples

**Web Application với Multiple Containers:**

```json
{
  "family": "api-gateway",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "nginx",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/nginx:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }
      ],
      "dependsOn": [
        {
          "containerName": "app",
          "condition": "HEALTHY"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/api-gateway",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "nginx"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:80/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 10
      }
    },
    {
      "name": "app",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest",
      "essential": true,
      "environment": [
        {"name": "NODE_ENV", "value": "production"},
        {"name": "LOG_LEVEL", "value": "info"}
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:database-url:DATABASE_URL::"
        },
        {
          "name": "API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:api-key:API_KEY::"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/api-gateway",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "app"
        }
      },
      "workingDirectory": "/app",
      "command": ["node", "server.js"]
    },
    {
      "name": "sidecar",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/datadog-agent:latest",
      "essential": false,
      "environment": [
        {"name": "DD_API_KEY", "value": "secretsmanager:datadog-api-key:value"},
        {"name": "DD_SITE", "value": "datadoghq.com"},
        {"name": "ECS_FARGATE", "value": "true"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/api-gateway",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "datadog"
        }
      }
    }
  ]
}
```

**Sidecar Pattern cho Logging/Monitoring:**

```json
{
  "family": "worker-service",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "worker",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/worker:latest",
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/worker",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "worker"
        }
      }
    },
    {
      "name": "log-aggregator",
      "image": "fluent/fluent-bit:latest",
      "essential": false,
      "firelensConfiguration": {
        "type": "fluentbit",
        "options": {
          "config-file-type": "file",
          "config-file-value": "/fluent-bit/etc/fluent-bit.conf"
        }
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/fluentbit",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "fluentbit"
        }
      },
      "storage": {
        "fsxWindowsFileServerVolumeConfiguration": []
      }
    }
  ]
}
```

### 4. Service Definitions

```yaml
# CloudFormation cho ECS Service
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: production-cluster
      ClusterSettings:
        - Name: containerInsights
          Value: enabled
      ServiceConnectDefaults:
        Namespace: production.local

  TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: web-service
      NetworkMode: awsvpc
      RequiresCompatibilities:
        - FARGATE
      Cpu: 1024
      Memory: 2048
      ExecutionRoleArn: !GetAtt ExecutionRole.Arn
      TaskRoleArn: !GetAtt TaskRole.Arn
      ContainerDefinitions:
        - Name: web
          Image: !Sub '${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/web:latest'
          Essential: true
          PortMappings:
            - ContainerPort: 8080
              AppProtocol: http
          EnvironmentFiles:
            - Value: arn:aws:s3:::my-bucket/env/production.env
              Type: s3
          Environment:
            - Name: LOG_LEVEL
              Value: info
          Secrets:
            - Name: DATABASE_URL
              ValueFrom: !Sub '${SecretManagerSecret.Arn}:DATABASE_URL::'
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: /ecs/web-service
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: web
          HealthCheck:
            Command:
              - CMD-SHELL
              - curl -f http://localhost:8080/health || exit 1
            Interval: 30
            Timeout: 5
            Retries: 3
            StartPeriod: 10

  ExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
      Policies:
        - PolicyName: ecr-pull-policy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ecr:GetAuthorizationToken
                Resource: '*'
              - Effect: Allow
                Action:
                  - ecr:BatchCheckLayerAvailability
                  - ecr:GetDownloadUrlForLayer
                  - ecr:BatchGetImage
                Resource: '*'
        - PolicyName: secrets-policy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                Resource: !Sub '${SecretManagerSecret.Arn}'

  TaskRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ecs-tasks.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: s3-access-policy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource: !Sub '${DataBucket.Arn}/*'
              - Effect: Allow
                Action:
                  - s3:ListBucket
                Resource: !GetAtt DataBucket.Arn

  SecretManagerSecret:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: /ecs/web-service/production
      SecretString: '{"DATABASE_URL":"postgres://user:pass@host:5432/db"}'

  SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: ECS Service Security Group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          SourceSecurityGroupId: !Ref ALBSecurityGroup
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          DestinationSecurityGroupId: !Ref RDSSecurityGroup

  Service:
    Type: AWS::ECS::Service
    Properties:
      ServiceName: web-service
      Cluster: !Ref ECSCluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 3
      LaunchType: FARGATE
      DeploymentConfiguration:
        MinimumHealthyPercent: 100
        MaximumPercent: 200
      DeploymentController:
        Type: CODE_DEPLOY
      HealthCheckGracePeriodSeconds: 30
      NetworkConfiguration:
        AwsvpcConfiguration:
          Subnets:
            - !Ref PrivateSubnet1
            - !Ref PrivateSubnet2
          SecurityGroups:
            - !Ref SecurityGroup
          AssignPublicIp: DISABLED
      LoadBalancers:
        - ContainerName: web
          ContainerPort: 8080
          TargetGroupArn: !Ref TargetGroup
      ServiceConnectConfiguration:
        Enabled: true
        Namespace: production.local
        Services:
          - DiscoveryName: web-service
            Port: 8080
            IngressPortOverride: 0
      PropagateTags: TASK_DEFINITION
      EnableExecuteCommand: true
```

### 5. Service Connect

Service Connect cung cấp built-in service discovery và traffic management cho ECS services.

```yaml
# Service Connect configuration
Service:
  Type: AWS::ECS::Service
  Properties:
    ServiceName: web-service
    Cluster: !Ref ECSCluster
    TaskDefinition: !Ref TaskDefinition
    DesiredCount: 3
    LaunchType: FARGATE
    NetworkConfiguration:
      AwsvpcConfiguration:
        Subnets:
          - !Ref PrivateSubnet1
          - !Ref PrivateSubnet2
        SecurityGroups:
          - !Ref SecurityGroup
    ServiceConnectConfiguration:
      Enabled: true
      Namespace: production.local
      LogConfiguration:
        LogDriver: awslogs
        Options:
          awslogs-group: /ecs/service-connect
          awslogs-region: !Ref AWS::Region
      Services:
        - DiscoveryName: web-service
          Port: 8080
          IngressPortOverride: 0
          ClientAliases:
            - Port: 8080
              DnsName: web-service.internal
        - DiscoveryName: api-service
          Port: 8080
          # Client can use this alias to connect
          ClientAliases:
            - Port: 8080
              DnsName: api.internal
```

```python
# Python example: Service discovery với boto3
import boto3

ecs_client = boto3.client('ecs')

def register_service_with_discovery(cluster, service_name, task_definition):
    """
    Register service với Service Connect discovery
    """
    response = ecs_client.create_service(
        cluster=cluster,
        serviceName=service_name,
        taskDefinition=task_definition,
        desiredCount=3,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-abc123', 'subnet-def456'],
                'securityGroups': ['sg-0123456789abcdef0']
            }
        },
        serviceConnectConfiguration={
            'enabled': True,
            'namespace': 'production.local',
            'services': [
                {
                    'discoveryName': service_name,
                    'port': 8080,
                    'ingressPortOverride': 0
                }
            ]
        }
    )
    return response

def discover_service(service_name, namespace='production.local'):
    """
    Query Service Connect để discover service endpoints
    """
    ecs_client = boto3.client('ecs')
    
    # List services in namespace
    response = ecs_client.list_services(
        cluster='production-cluster',
        launchType='FARGATE'
    )
    
    # Use Cloud Map for service discovery
    servicediscovery = boto3.client('servicediscovery')
    
    response = servicediscovery.discover_instances(
        NamespaceName=namespace,
        ServiceName=service_name,
        MaxResults=10,
        HealthStatus='HEALTHY'
    )
    
    return response['Instances']
```

### 6. Secrets Management

```bash
# Store secrets in Secrets Manager
aws secretsmanager create-secret \
  --name /ecs/my-app/production \
  --secret-string '{"DB_PASSWORD":"secret123","API_KEY":"apikey456"}'

# Store secret in Parameter Store (Systems Manager)
aws ssm put-parameter \
  --name /ecs/my-app/db-password \
  --value "secret123" \
  --type SecureString \
  --key-id alias/aws/ssm

# Grant ECS task execution role access to secrets
aws iam put-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-name ecs-secrets-access \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "secretsmanager:GetSecretValue"
        ],
        "Resource": [
          "arn:aws:secretsmanager:us-east-1:123456789012:secret:/ecs/my-app/*"
        ]
      },
      {
        "Effect": "Allow",
        "Action": [
          "ssm:GetParameters"
        ],
        "Resource": [
          "arn:aws:ssm:us-east-1:123456789012:parameter/ecs/my-app/*"
        ]
      }
    ]
  }'
```

## Best Practices

### 1. Security Best Practices

**IAM Roles Configuration:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRPull",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    },
    {
      "Sid": "SecretsManager",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:us-east-1:123456789012:secret:*"
      ],
      "Condition": {
        "ForAnyValue:StringEquals": {
          "aws:CalledVia": ["ecs-tasks.amazonaws.com"]
        }
      }
    },
    {
      "Sid": "ParameterStore",
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameters"
      ],
      "Resource": [
        "arn:aws:ssm:us-east-1:123456789012:parameter/*"
      ]
    }
  ]
}
```

**Network Security:**

```bash
# Create security groups for ECS tasks
aws ec2 create-security-group \
  --group-name ecs-tasks-sg \
  --description "Security group for ECS tasks" \
  --vpc-id vpc-abc123

# Allow traffic from ALB only
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 8080 \
  --source-group sg-alb-sg

# Allow outbound to RDS
aws ec2 authorize-security-group-egress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 5432 \
  --destination-group-id sg-rds-sg
```

### 2. Auto Scaling Configuration

```yaml
# CloudFormation Auto Scaling cho ECS Service
ServiceAutoScalingTarget:
  Type: AWS::ApplicationAutoScaling::ScalableTarget
  Properties:
    MaxCapacity: 10
    MinCapacity: 2
    ResourceId: !Sub 'service/${ECSCluster}/${Service}'
    RoleARN: !GetAtt AutoScalingRole.Arn
    ScalableDimension: ecs:service:DesiredCount
    ScheduledActionsCapacityProviderStrategy:
      - CapacityProvider: FARGATE
        Base: 2
        Weight: 1

ServiceScalingPolicyCPU:
  Type: AWS::ApplicationAutoScaling::ScalingPolicy
  Properties:
    PolicyName: cpu-scaling-policy
    PolicyType: TargetTrackingScaling
    ResourceId: !Sub 'service/${ECSCluster}/${Service}'
    ScalableDimension: ecs:service:DesiredCount
    TargetTrackingScalingPolicyConfiguration:
      TargetValue: 70
      ScaleInCooldown: 60
      ScaleOutCooldown: 60
      PredefinedMetricSpecification:
        PredefinedMetricType: ECSServiceAverageCPUUtilization

ServiceScalingPolicyMemory:
  Type: AWS::ApplicationAutoScaling::ScalingPolicy
  Properties:
    PolicyName: memory-scaling-policy
    PolicyType: TargetTrackingScaling
    ResourceId: !Sub 'service/${ECSCluster}/${Service}'
    ScalableDimension: ecs:service:DesiredCount
    TargetTrackingScalingPolicyConfiguration:
      TargetValue: 80
      ScaleInCooldown: 60
      ScaleOutCooldown: 60
      PredefinedMetricSpecification:
        PredefinedMetricType: ECSServiceAverageMemoryUtilization

ServiceScalingPolicyALB:
  Type: AWS::ApplicationAutoScaling::ScalingPolicy
  Properties:
    PolicyName: alb-request-count-policy
    PolicyType: TargetTrackingScaling
    ResourceId: !Sub 'service/${ECSCluster}/${Service}'
    ScalableDimension: ecs:service:DesiredCount
    TargetTrackingScalingPolicyConfiguration:
      TargetValue: 1000
      ScaleInCooldown: 60
      ScaleOutCooldown: 30
      PredefinedMetricSpecification:
        PredefinedMetricType: ALBRequestCountPerTarget
        ResourceLabel: !Sub 'app/${ALB}/${TargetGroupName}/ecs/${ECSCluster}/${Service}'
```

### 3. CI/CD Pipeline với ECS

```yaml
# CodePipeline cho ECS deployment
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  CodePipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      Name: ecs-deployment-pipeline
      RoleArn: !GetAtt CodePipelineRole.Arn
      ArtifactStore:
        Type: S3
        Location: !Ref PipelineArtifactBucket
      Stages:
        - Name: Source
          Actions:
            - Name: SourceAction
              ActionTypeId:
                Category: Source
                Owner: AWS
                Provider: CodeCommit
                Version: '1'
              Configuration:
                RepositoryName: !Ref CodeCommitRepo
                BranchName: main
                PollForSourceChanges: false
              OutputArtifacts:
                - Name: SourceOutput
              RunOrder: 1
        - Name: Build
          Actions:
            - Name: BuildAction
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: '1'
              Configuration:
                ProjectName: !Ref CodeBuildProject
                PrimarySource: SourceOutput
              InputArtifacts:
                - Name: SourceOutput
              OutputArtifacts:
                - Name: BuildOutput
              RunOrder: 1
        - Name: Deploy
          Actions:
            - Name: DeployAction
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: ECS
                Version: '1'
              Configuration:
                ClusterName: !Ref ECSCluster
                ServiceName: !Ref ECSService
                DeploymentTimeout: "60"
                FileName: taskdef.json
              InputArtifacts:
                - Name: BuildOutput
              RunOrder: 1

  CodeBuildProject:
    Type: AWS::CodeBuild::Project
    Properties:
      Name: ecs-build-project
      ServiceRole: !GetAtt CodeBuildRole.Arn
      Artifacts:
        Type: CODEPIPELINE
      Environment:
        Type: LINUX_CONTAINER
        Image: aws/codebuild/standard:7.0
        ComputeType: BUILD_GENERAL1_SMALL
        EnvironmentVariables:
          - Name: AWS_ACCOUNT_ID
            Value: !Ref AWS::AccountId
          - Name: IMAGE_REPO_NAME
            Value: !Ref ECRRepository
          - Name: IMAGE_TAG
            Value: latest
      Source:
        Type: CODEPIPELINE
        BuildSpec: |
          version: 0.2
          phases:
            pre_build:
              commands:
                - echo Logging in to Amazon ECR...
                - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
            build:
              commands:
                - echo Build started on `date`
                - echo Building the Docker image...
                - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
                - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
            post_build:
              commands:
                - echo Pushing the Docker image...
                - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
                - echo Writing task definition...
                - printf '[{"name":"web","image":"%s.dkr.ecr.%s.amazonaws.com/%s:%s"}]' $AWS_ACCOUNT_ID $AWS_DEFAULT_REGION $IMAGE_REPO_NAME $IMAGE_TAG > taskdef.json
          artifacts:
            files:
              - taskdef.json

  ECRRepository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: web-application
      ImageScanningConfiguration:
        scanOnPush: true
      EncryptionConfiguration:
        EncryptionType: AES256
```

## Common Patterns

### Pattern 1: Blue-Green Deployment với CodeDeploy

```yaml
# Task Definition for CodeDeploy blue-green
TaskDefinition:
  Type: AWS::ECS::TaskDefinition
  Properties:
    Family: web-service
    NetworkMode: awsvpc
    RequiresCompatibilities:
      - FARGATE
    Cpu: 1024
    Memory: 2048
    ContainerDefinitions:
      - Name: web
        Image: !Sub '${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/web:${CODEDEPLOY_LATEST_REVISION}'
        Essential: true
        PortMappings:
          - ContainerPort: 8080
        LogConfiguration:
          LogDriver: awslogs
          Options:
            awslogs-group: /ecs/web-service
            awslogs-region: !Ref AWS::Region
            awslogs-stream-prefix: web

# CodeDeploy Deployment Group
DeploymentGroup:
  Type: AWS::CodeDeploy::DeploymentGroup
  Properties:
    ApplicationName: !Ref ECSApplication
    DeploymentConfigName: CodeDeployDefault.ECSLinear10PercentEvery1Minutes
    DeploymentStyle:
      DeploymentType: BLUE_GREEN
      OptionSpecification:
        Instant: false
    ECSCluster: !Ref ECSCluster
    ServiceRoleArn: !GetAtt CodeDeployRole.Arn
    TargetResourceType: ecs:cluster
    BlueGreenDeploymentConfiguration:
      TerminateBlueInstancesOnDeployment:
        Behavior: TERMINATE
        TerminationWaitTimeInMinutes: 5
      DeploymentReadyOption:
        ActionOnTimeout: CONTINUE_DEPLOYMENT
        WaitTimeInMinutes: 5
    LoadBalancerInfo:
      ContainerName: web
      ContainerPort: 8080
      TargetGroupPairInfo:
        TargetGroups:
          - Name: !Ref BlueTargetGroup
          - Name: !Ref GreenTargetGroup
```

### Pattern 2: Scheduled Tasks cho Batch Processing

```yaml
# Scheduled Task Definition
ScheduledTask:
  Type: AWS::Events::Rule
  Properties:
    Name: daily-batch-job
    ScheduleExpression: cron(0 2 * * ? *)
    Targets:
      - Id: ecs-target
        Arn: !GetAtt ECSCluster.Arn
        RoleArn: !GetAtt EventRuleRole.Arn
        EcsParameters:
          TaskDefinitionArn: !Ref BatchTaskDefinition
          TaskCount: 1
          LaunchType: FARGATE
          PlatformVersion: LATEST
          NetworkConfiguration:
            AwsvpcConfiguration:
              Subnets:
                - !Ref PrivateSubnet1
              SecurityGroups:
                - !Ref BatchSecurityGroup
              AssignPublicIp: DISABLED

BatchTaskDefinition:
  Type: AWS::ECS::TaskDefinition
  Properties:
    Family: batch-processor
    NetworkMode: awsvpc
    RequiresCompatibilities:
      - FARGATE
    Cpu: 2048
    Memory: 4096
    ContainerDefinitions:
      - Name: batch
        Image: !Sub '${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/batch-processor:latest'
        Essential: true
        Environment:
          - Name: BATCH_SIZE
            Value: "1000"
        LogConfiguration:
          LogDriver: awslogs
          Options:
            awslogs-group: /ecs/batch
            awslogs-region: !Ref AWS::Region
            awslogs-stream-prefix: batch
        Command:
          - node
          - process-batch.js
```

### Pattern 3: Worker Queue Pattern

```yaml
# Worker Service với SQS integration
WorkerTaskDefinition:
  Type: AWS::ECS::TaskDefinition
  Properties:
    Family: worker-service
    NetworkMode: awsvpc
    RequiresCompatibilities:
      - FARGATE
    Cpu: 512
    Memory: 1024
    ContainerDefinitions:
      - Name: worker
        Image: !Sub '${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/worker:latest'
        Essential: true
        Environment:
          - Name: SQS_QUEUE_URL
            Value: !Ref JobQueueUrl
        EnvironmentFiles:
          - Value: arn:aws:s3:::my-bucket/env/worker.env
            Type: s3
        Secrets:
          - Name: AWS_ACCESS_KEY_ID
            ValueFrom: arn:aws:ssm:us-east-1:123456789012:parameter/worker/access-key
          - Name: AWS_SECRET_ACCESS_KEY
            ValueFrom: arn:aws:ssm:us-east-1:123456789012:parameter/worker/secret-key:SecureString::
        LogConfiguration:
          LogDriver: awslogs
          Options:
            awslogs-group: /ecs/worker
            awslogs-region: !Ref AWS::Region
            awslogs-stream-prefix: worker

WorkerService:
  Type: AWS::ECS::Service
  Properties:
    ServiceName: worker-service
    Cluster: !Ref ECSCluster
    TaskDefinition: !Ref WorkerTaskDefinition
    DesiredCount: 2
    LaunchType: FARGATE
    DeploymentConfiguration:
      MinimumHealthyPercent: 50
      MaximumPercent: 200
    NetworkConfiguration:
      AwsvpcConfiguration:
        Subnets:
          - !Ref PrivateSubnet1
          - !Ref PrivateSubnet2
        SecurityGroups:
          - !Ref WorkerSecurityGroup
    PropagateTags: TASK_DEFINITION
```

## Troubleshooting

### Common Issues và Solutions

**1. Tasks Not Starting**

```bash
# Check service events
aws ecs describe-services \
  --cluster production-cluster \
  --services web-service \
  --query 'services[0].events[:5]'

# Check task definition status
aws ecs describe-task-definition \
  --task-definition web-service \
  --query 'taskDefinition.status'

# Check for capacity issues
aws ecs describe-tasks \
  --cluster production-cluster \
  --tasks <task-arn> \
  --query 'tasks[0].stoppedReason'

# Common reasons for task not starting:
# - Not enough memory/CPU in cluster
# - Security group doesn't allow traffic
# - Subnet doesn't have internet access
# - Image doesn't exist or isn't accessible
# - IAM role doesn't have required permissions

# Debug network issues
aws ecs execute-command \
  --cluster production-cluster \
  --task <task-arn> \
  --container web \
  --command "/bin/sh" \
  --interactive
```

**2. Health Check Failures**

```bash
# Check container health status
aws ecs describe-tasks \
  --cluster production-cluster \
  --tasks <task-arn> \
  --query 'tasks[0].containers[*].healthStatus'

# Check CloudWatch logs
aws logs tail /ecs/web-service --follow --aws-region us-east-1

# Verify health check configuration
aws ecs describe-task-definition \
  --task-definition web-service \
  --query 'taskDefinition.containerDefinitions[0].healthCheck'

# Common health check issues:
# - Health check command is incorrect
# - Application takes too long to start (increase startPeriod)
# - Health endpoint returns wrong status code
# - Security group doesn't allow health checks from ALB
```

**3. Secret Not Found Errors**

```bash
# Verify secret exists
aws secretsmanager describe-secret \
  --secret-id /ecs/my-app/production

# Check secret value
aws secretsmanager get-secret-value \
  --secret-id /ecs/my-app/production

# Verify IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/ecsTaskExecutionRole \
  --action-names secretsmanager:GetSecretValue \
  --resource-arns arn:aws:secretsmanager:us-east-1:123456789012:secret:/ecs/my-app/production

# Check CloudWatch for errors
aws logs filter-log-events \
  --log-group-name /ecs/web-service \
  --filter-pattern "Error"
```

**4. Service Connect Issues**

```bash
# Check Service Connect configuration
aws ecs describe-services \
  --cluster production-cluster \
  --services web-service \
  --query 'services[0].serviceConnectConfiguration'

# Verify Cloud Map service registration
aws servicediscovery list-services \
  --query 'Services[?Name==`web-service`]'

# Check if tasks are registered
aws ecs describe-tasks \
  --cluster production-cluster \
  --tasks <task-arn> \
  --query 'tasks[0].containers[*].networkInterfaces'

# Test connectivity between services
aws ecs execute-command \
  --cluster production-cluster \
  --task <task-arn> \
  --container web \
  --command "curl http://api-service.internal:8080/health"
```

## Examples

### Example 1: Complete ECS Fargate Setup với Terraform

```terraform
# Terraform configuration cho ECS Fargate
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
    Name = "ecs-vpc"
  }
}

# Subnets
resource "aws_subnet" "private" {
  count = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "ecs-private-subnet-${count.index + 1}"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "ecs-igw"
  }
}

# NAT Gateway
resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id
}

# Route Tables
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name = "ecs-private-rt"
  }
}

resource "aws_subnet" "public" {
  count = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 10)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "ecs-public-subnet-${count.index + 1}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "ecs-public-rt"
  }
}

# Security Group
resource "aws_security_group" "ecs_tasks" {
  name        = "ecs-tasks-sg"
  description = "Security group for ECS tasks"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ecs-tasks-sg"
  }
}

# ALB Security Group
resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  tags = {
    Name = "alb-sg"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "production-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "production-ecs-cluster"
  }
}

# ECR Repository
resource "aws_ecr_repository" "app" {
  name = "web-application"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}

# IAM Roles
resource "aws_iam_role" "ecs_execution_role" {
  name = "ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "secrets_access" {
  name = "secrets-access"
  role = aws_iam_role.ecs_execution_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "*"
      }
    ]
  })
}

# Secrets
resource "aws_secretsmanager_secret" "app_secrets" {
  name = "/ecs/web-app/production"
}

resource "aws_secretsmanager_secret_version" "app_secrets" {
  secret_id = aws_secretsmanager_secret.app_secrets.id
  secret_string = jsonencode({
    DATABASE_URL = "postgres://user:pass@rds.amazonaws.com:5432/mydb"
    API_KEY = "secret-api-key"
  })
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/web-app"
  retention_in_days = 30

  tags = {
    Name = "ecs-log-group"
  }
}

# ALB
resource "aws_lb" "main" {
  name               = "ecs-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = false

  tags = {
    Name = "ecs-alb"
  }
}

resource "aws_lb_target_group" "app" {
  name     = "ecs-tg"
  port     = 8080
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
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "web-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name      = "web"
      image     = "${aws_ecr_repository.app.repository_url}:latest"
      essential = true
      portMappings = [
        {
          containerPort = 8080
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "NODE_ENV"
          value = "production"
        }
      ]
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = "${aws_secretsmanager_secret.app_secrets.arn}:DATABASE_URL::"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "web"
        }
      }
      healthCheck = {
        command  = ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"]
        interval = 30
        timeout  = 5
        retries  = 3
      }
    }
  ])
}

# ECS Service
resource "aws_ecs_service" "app" {
  name            = "web-app-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3
  launch_type     = "FARGATE"

  deployment_controller {
    type = "ECS"
  }

  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100
  health_check_grace_period_seconds  = 30

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "web"
    container_port   = 8080
  }

  depends_on = [aws_lb_listener.https]
}

# Auto Scaling
resource "aws_appautoscaling_target" "app" {
  max_capacity       = 10
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  role_arn           = aws_iam_role.appautoscaling.arn
}

resource "aws_appautoscaling_policy" "app" {
  name               = "app-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.app.resource_id
  scalable_dimension = aws_appautoscaling_target.app.scalable_dimension
  target_tracking_scaling_policy_configuration {
    target_value       = 70
    scale_in_cooldown  = 60
    scale_out_cooldown = 60
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
  }
}
```

## References

### Official Documentation
- [Amazon ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS Fargate Documentation](https://docs.aws.amazon.com/AmazonECS/latest/userguide/what-is-fargate.html)
- [ECS Task Definitions](https://docs.aws.amazon.com/AmazonECS/latest/userguide/task_definitions.html)
- [ECS Services](https://docs.aws.amazon.com/AmazonECS/latest/userguide/ecs_services.html)
- [Service Connect](https://docs.aws.amazon.com/AmazonECS/latest/userguide/service-connect.html)

### Best Practices
- [ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpractices.html)
- [ECS Security Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/userguide/security-best-practices.html)
- [Fargate Spot](https://docs.aws.amazon.com/AmazonECS/latest/userguide/fargate-task-placement.html)
- [ECS Service Auto Scaling](https://docs.aws.amazon.com/AmazonECS/latest/userguide/service-autoscaling.html)

### Tools
- [ECS CLI](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI.html)
- [ECS CDK](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-ecs-readme.html)
- [ECS Copilot](https://aws.github.io/copilot-cli/)
