---
title: "AWS Lambda Serverless Computing"
description: "Hướng dẫn toàn diện về Lambda functions, layers, extensions, Power Tuning, EventBridge integration và SAM template"
tags: ["aws", "lambda", "serverless", "functions", "layers", "eventbridge", "sam", "power-tuning"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# AWS Lambda Serverless Computing

## Tổng Quan (Overview)

AWS Lambda là serverless compute service cho phép chạy code mà không cần provisioning hoặc managing servers. Lambda tự động scales your application bằng cách running code in response to events, và bạn chỉ trả tiền cho compute time khi code đang chạy.

Tài liệu này bao gồm comprehensive coverage của Lambda features và best practices, bao gồm function development và deployment, Lambda Layers cho code reuse, Extensions cho monitoring và security tooling integration, Lambda Power Tuning cho cost optimization, EventBridge integration cho event-driven architectures, và AWS SAM (Serverless Application Model) cho infrastructure as code. Các patterns cho error handling, cold starts, và production deployments cũng được covered.

Lambda là nền tảng cốt lõi cho serverless architectures trên AWS, cung cấp highly available, scalable compute với pay-per-use pricing model, lý tưởng cho event-driven workloads, microservices, và data processing pipelines.

## Mục Đích (Purpose)

Mục đích chính của tài liệu này bao gồm:

1. **Function Development**: Best practices cho writing và deploying Lambda functions
2. **Performance Optimization**: Configure memory, timeout, và Power Tuning
3. **Code Organization**: Use Layers và Extensions hiệu quả
4. **Event-Driven Architecture**: Integrate với EventBridge và other services
5. **Infrastructure as Code**: Use SAM cho repeatable deployments
6. **Security**: Apply least privilege, VPC configuration, và secrets management

## Các Khái Niệm Chính (Key Concepts)

### 1. Lambda Function Configuration

```yaml
# CloudFormation for Lambda Function
Resources:
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: lambda-policy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: '*'
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource: '*'
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                Resource: '*'

  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: production-api-handler
      Handler: index.handler
      Runtime: python3.11
      Role: !GetAtt LambdaExecutionRole.Arn
      Code:
        S3Bucket: !Ref LambdaCodeBucket
        S3Key: functions/production-api-v2.zip
        S3ObjectVersion: !GetAtt LambdaCode.ObjectVersion
      MemorySize: 512
      Timeout: 30
      ReservedConcurrentExecutions: 100
      EphemeralStorage:
        Size: 10240
      FileSystemConfigs:
        - Arn: !Ref EfsAccessPointArn
          LocalMountPath: /mnt/efs
      Environment:
        Variables:
          NODE_ENV: production
          LOG_LEVEL: info
          CACHE_TTL: "3600"
      VpcConfig:
        SubnetIds:
          - !Ref PrivateSubnet1
          - !Ref PrivateSubnet2
        SecurityGroupIds:
          - !Ref LambdaSecurityGroup
      Layers:
        - !Ref CommonDependenciesLayer
        - !Ref PowertoolsLayer
      TracingConfig:
        Mode: Active
      DeadLetterQueue:
        TargetArn: !GetAtt DeadLetterQueue.Arn
        Type: SQS
      Tags:
        - Key: Environment
          Value: Production
        - Key: Application
          Value: API

  LambdaVersion:
    Type: AWS::Lambda::Version
    Properties:
      FunctionName: !Ref LambdaFunction
      ProvisionedConcurrencyConfig:
        ProvisionedConcurrentExecutions: 5

  Alias:
    Type: AWS::Lambda::Alias
    Properties:
      FunctionName: !Ref LambdaFunction
      FunctionVersion: !GetAtt LambdaVersion.Version
      Name: production
      RoutingConfig:
        AdditionalVersionWeights:
          - FunctionVersion: "2"
            FunctionWeight: 0.1
```

### 2. Lambda Layers

Lambda Layers cho phép share common code giữa multiple functions.

```yaml
# Layer configuration
Resources:
  CommonDependenciesLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: common-dependencies
      Description: Common Python dependencies
      Content:
        S3Bucket: !Ref LayerBucket
        S3Key: layers/common-dependencies.zip
      CompatibleRuntimes:
        - python3.11
        - python3.10
        - python3.9
      LicenseInfo: MIT

  PowertoolsLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: aws-powertools
      Description: AWS Lambda Powertools for Python
      Content:
        S3Bucket: !Ref LayerBucket
        S3Key: layers/powertools.zip
      CompatibleRuntimes:
        - python3.11
        - python3.10
        - python3.9

  XRaySDKLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: xray-sdk
      Description: AWS X-Ray SDK
      Content:
        S3Bucket: !Ref LayerBucket
        S3Key: layers/xray-sdk.zip
      CompatibleRuntimes:
        - python3.11
        - python3.10
```

```bash
# Create layer from existing pip packages
mkdir -p python/lib/python3.11/site-packages
pip install -r requirements.txt -t python/lib/python3.11/site-packages
cd python && zip -r ../layer.zip .
aws lambda publish-layer-version \
  --layer-name common-dependencies \
  --description "Common Python dependencies" \
  --content S3Bucket=my-bucket,S3Key=layers/common-dependencies.zip \
  --compatible-runtimes python3.11 \
  --license-info MIT

# Layer structure
# my-layer.zip
# ├── python/
# │   ├── lib/
# │   │   └── python3.11/
# │   │       └── site-packages/
# │   │           ├── requests/
# │   │           └── pandas/
# └── layer.json (optional metadata)

# List available layers
aws lambda list-layers \
  --compatible-runtime python3.11 \
  --query 'Layers[*].[LayerName,LatestMatchingVersion.Version,LatestMatchingVersion.CreatedDate]'

# Check layer permissions
aws lambda get-layer-version-policy \
  --layer-name common-dependencies \
  --version-number 1
```

### 3. Lambda Extensions

Extensions integrate external tooling với Lambda runtime.

```yaml
# Lambda Extension Layer
Resources:
  DatadogExtensionLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: datadog-extension
      Content:
        S3Bucket: !Ref DatadogBucket
        S3Key: extensions/datadog-extension.zip
      CompatibleArchitectures:
        - x86_64
        - arm64
      CompatibleRuntimes:
        - python3.11
        - python3.10

  SecurityExtensionLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: security-toolkit
      Content:
        S3Bucket: !Ref LayerBucket
        S3Key: layers/security-extension.zip
      CompatibleRuntimes:
        - python3.11
```

```bash
# Extensions configuration via environment variables
# Datadog extension
LAMBDA_EXTENSION_ENABLED: "true"
DD_API_KEY_SECRET_ARN: "arn:aws:secretsmanager:us-east-1:123456789012:secret:datadog-api-key"
DD_SITE: "datadoghq.com"
DD_LOG_LEVEL: "info"
DD_EXTENSION_SOCKET_PATH: "/tmp/datadog/extensions/v0.4"

# AWS Distro for OpenTelemetry
OPENTELEMETRY_EXTENSION_ENABLED: "true"
OTEL_EXPORTER_OTLP_ENDPOINT: "http://collector.observability:4317"
OTEL_SERVICE_NAME: "production-api"
OTEL_PROPAGATORS: "tracecontext,baggage,awsxray"
```

### 4. Lambda Power Tuning

Power Tuning giúp optimize function performance và cost.

```yaml
# Power Tuning State Machine
Resources:
  PowerTuningRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: states.amazonaws.com
            Action: sts:AssumeRole

  PowerTuningStateMachine:
    Type: AWS::Serverless::StateMachine
    Properties:
      Name: lambda-power-tuning
      DefinitionUri: s3://aws-serverless-app-state/power-tuner/statmach.asl.json
      Policies:
        - LambdaInvokePolicy:
            FunctionName: "*"
        - CloudWatchLogsPolicy:
            LogGroupArn: !Sub 'arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:/aws/lambda/*'
      Type: EXPRESS
```

```bash
# Run power tuning via AWS CLI
aws lambda power-tuning invoke \
  --function-name production-api-handler \
  --power-values [128,256,512,768,1024,1536,2048,3008] \
  --strategy cost

# Power tuning configuration in function
aws lambda put-function-event-invoke-config \
  --function-name production-api-handler \
  --qualifier v2 \
  --maximum-event-age 3600 \
  --maximum-retry-attempts 2

# Custom power tuning script
#!/bin/bash
# power-tuning.sh

FUNCTION_NAME=$1
REGION=${2:-us-east-1}

for memory in 128 256 512 1024 2048 3008; do
  echo "Testing memory: $memory MB"
  
  # Update function memory
  aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --memory-size $memory \
    --region $REGION
  
  # Wait for update
  aws lambda wait function-updated \
    --function-name $FUNCTION_NAME \
    --region $REGION
  
  # Run test
  START=$(date +%s)
  aws lambda invoke \
    --function-name $FUNCTION_NAME \
    --payload '{"test": true}' \
    --log-type Tail \
    --region $REGION \
    response.json
  
  END=$(date +%s)
  DURATION=$((END - START))
  
  # Extract metrics from log
  BILLED_DURATION=$(cat response.json | jq -r '.LogResult' | base64 -d | grep "BILLED_DURATION" | awk '{print $2}')
  
  echo "Memory: $memory MB, Duration: $BILLED_DURATION ms"
  
  # Clean up
  rm response.json
done
```

### 5. EventBridge Integration

```yaml
# EventBridge Rule for Lambda
Resources:
  EventBridgeRule:
    Type: AWS::Events::Rule
    Properties:
      Name: production-event-rule
      Description: Route S3 events to Lambda
      EventBusName: default
      EventPattern:
        source:
          - aws.s3
        detail-type:
          - AWS API Call via CloudTrail
        detail:
          eventSource:
            - s3.amazonaws.com
          eventName:
            - PutObject
            - CompleteMultipartUpload
          requestParameters:
            bucketName:
              - production-data-bucket
      Targets:
        - Id: LambdaTarget
          Arn: !GetAtt LambdaFunction.Arn
          DeadLetterConfig:
            Arn: !GetAtt DeadLetterQueue.Arn
          RetryPolicy:
            MaximumRetryAttempts: 3
            MaximumEventAge: 3600

  EventBridgePermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref LambdaFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt EventBridgeRule.Arn

  # Scheduled Event
  ScheduledRule:
    Type: AWS::Events::Rule
    Properties:
      Name: nightly-maintenance
      Description: Run nightly maintenance tasks
      ScheduleExpression: cron(0 2 * * ? *)
      Targets:
        - Id: MaintenanceLambda
          Arn: !GetAtt MaintenanceFunction.Arn
          Input: '{"maintenance_type": "cleanup"}'
```

```python
# EventBridge event processing
import json
from datetime import datetime

def handler(event, context):
    """Process EventBridge events"""
    
    # Parse EventBridge event
    detail = event.get('detail', {})
    event_type = event.get('detail-type', '')
    source = event.get('source', '')
    
    print(f"Received event: {event_type} from {source}")
    
    if source == 'aws.s3':
        return handle_s3_event(detail)
    elif source == 'aws.dynamodb':
        return handle_dynamodb_event(detail)
    elif source == 'aws.ec2':
        return handle_ec2_event(detail)
    else:
        return process_generic_event(event)

def handle_s3_event(detail):
    """Process S3 CloudTrail events"""
    bucket = detail.get('requestParameters', {}).get('bucketName')
    key = detail.get('requestParameters', {}).get('key')
    event_name = detail.get('eventName')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'bucket': bucket,
            'key': key,
            'event': event_name
        })
    }

def handle_dynamodb_event(detail):
    """Process DynamoDB Streams events"""
    table_name = detail.get('tableName')
    event_name = detail.get('eventName')
    
    # NewImage and OldImage contain item data
    new_image = detail.get('dynamodb', {}).get('NewImage', {})
    old_image = detail.get('dynamodb', {}).get('OldImage', {})
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'table': table_name,
            'event': event_name,
            'new': new_image,
            'old': old_image
        })
    }
```

### 6. SAM Template

```yaml
# SAM Template for Serverless Application
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Globals:
  Function:
    Timeout: 30
    MemorySize: 512
    Runtime: python3.11
    Tracing: Active
    Architectures:
      - x86_64
    Environment:
      Variables:
        LOG_LEVEL: info
    VpcConfig:
      SecurityGroupIds:
        - !Ref LambdaSecurityGroup
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
  Api:
    Auth:
      Authorizers:
        CognitoAuthorizer:
          UserPoolArn: !GetAtt UserPool.Arn
          AppIdClientId: !Ref UserPoolClient
    MethodSettings:
      - ResourcePath: /*
        MetricsEnabled: true
        LoggingLevel: INFO
        DataTraceEnabled: true

Resources:
  # DynamoDB Table
  UsersTable:
    Type: AWS::Serverless::SimpleTable
    Properties:
      TableName: users
      PrimaryKey:
        Name: user_id
        Type: String
      ProvisionedThroughput:
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      SSESpecification:
        SSEEnabled: true
        SSEType: KMS
        KMSMasterKeyId: !Ref TableKMSKey

  # S3 Bucket
  DataBucket:
    Type: AWS::Serverless::S3
    Properties:
      BucketName: !Sub '${AWS::StackName}-data-bucket'
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: s3:ObjectCreated:*
            Function: !GetAtt S3EventHandler.Arn
          - Event: s3:ObjectRemoved:*
            Function: !GetAtt S3EventHandler.Arn
      NotificationConfiguration:
        QueueConfigurations:
          - Event: s3:ObjectCreated:*
            Queue: !GetAtt EventQueue.Arn
      CorsConfiguration:
        CorsRules:
          - AllowedOrigins:
              - https://example.com
            AllowedMethods:
              - GET
              - PUT
              - POST
            AllowedHeaders:
              - '*'
            MaxAge: 3600
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: ArchiveOldData
            Status: Enabled
            Prefix: temp/
            ExpirationInDays: 7
          - Id: TransitionToGlacier
            Status: Enabled
            Prefix: archive/
            Transitions:
              - TransitionInDays: 30
                StorageClass: GLACIER
      VersioningConfiguration:
        Status: Enabled

  # Main API Function
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-api'
      Handler: src/api.handler
      CodeUri: src/
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
        - S3CrudPolicy:
            BucketName: !Ref DataBucket
        - SecretsManagerReadWrite:
            SecretArn: !Ref UserCredentialsSecret
        - Statement:
            - Sid: SSMParameterAccess
              Effect: Allow
              Action:
                - ssm:GetParameter
                - ssm:GetParameters
              Resource:
                - !Sub 'arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter/${AWS::StackName}/*'
      Events:
        ApiRoot:
          Type: Api
          Properties:
            Path: /
            Method: GET
        ApiUsers:
          Type: Api
          Properties:
            Path: /users
            Method: ANY
        ApiUserById:
          Type: Api
          Properties:
            Path: /users/{user_id}
            Method: ANY
        ApiBatch:
          Type: Api
          Properties:
            Path: /batch
            Method: POST
        S3EventTrigger:
          Type: S3
          Properties:
            Bucket: !Ref DataBucket
            Events:
              - s3:ObjectCreated:*
              - s3:ObjectRemoved:*
        DynamoDBStreamEvent:
          Type: DynamoDB
          Properties:
            Stream:
              !GetAtt UsersTable.StreamArn
            StartingPosition: TRIM_HORIZON
            BatchSize: 100
            MaximumBatchingWindowInSeconds: 60
      ProvisionedConcurrency: 5
      AutoPublishAlias: production

  # S3 Event Handler
  S3EventHandler:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-s3-handler'
      Handler: src.s3_handler.handle
      CodeUri: src/
      MemorySize: 256
      Timeout: 60
      Policies:
        - S3ReadPolicy:
            BucketName: !Ref DataBucket
        - Statement:
            - Sid: RekognitionAccess
              Effect: Allow
              Action:
                - rekognition:DetectLabels
                - rekognition:ModerateImage
              Resource: '*'

  # Scheduled Function
  MaintenanceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-maintenance'
      Handler: src.maintenance.run
      CodeUri: src/
      MemorySize: 1024
      Timeout: 900  # 15 minutes
      Events:
        Schedule:
          Type: Schedule
          Properties:
            Schedule: rate(1 day)
      Environment:
        Variables:
          RETENTION_DAYS: "30"

  # Step Functions State Machine
  ProcessingStateMachine:
    Type: AWS::Serverless::StateMachine
    Properties:
      Name: !Sub '${AWS::StackName}-processing'
      DefinitionUri: statemachine/processing.asl.json
      DefinitionSubstitutions:
        ProcessFunction: !GetAtt ProcessingFunction.Arn
        NotifyFunction: !GetAtt NotifyFunction.Arn
        FailedTopicArn: !Ref FailedTopic.Arn
      Policies:
        - LambdaInvokePolicy:
            FunctionName: !Ref ProcessingFunction
        - LambdaInvokePolicy:
            FunctionName: !Ref NotifyFunction
        - SNSPublishMessagePolicy:
            TopicArn: !Ref FailedTopic.Arn

  # Output
Outputs:
  ApiEndpoint:
    Description: API Gateway endpoint URL
    Value: !Sub 'https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/'
    Export:
      Name: !Sub '${AWS::StackName}-api-endpoint'

  UsersTableName:
    Description: Users table name
    Value: !Ref UsersTable
    Export:
      Name: !Sub '${AWS::StackName}-users-table'

  DataBucketName:
    Description: Data bucket name
    Value: !Ref DataBucket
    Export:
      Name: !Sub '${AWS::StackName}-data-bucket'
```

## Best Practices

### 1. Security Best Practices

```yaml
# Security-focused Lambda configuration
Resources:
  SecureLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: secure-api-handler
      Handler: index.handler
      Runtime: python3.11
      Role: !GetAtt SecureLambdaRole.Arn
      Code:
        S3Bucket: !Ref SecureCodeBucket
        S3Key: functions/secure-handler.zip
      MemorySize: 256
      Timeout: 10
      VpcConfig:
        SubnetIds:
          - !Ref PrivateSubnet1
          - !Ref PrivateSubnet2
        SecurityGroupIds:
          - !Ref SecureLambdaSecurityGroup
      Environment:
        Variables:
          SECURE_MODE: "true"
      TracingConfig:
        Mode: Active
      FileSystemConfigs:
        - Arn: !Ref SecureEFSArn
          LocalMountPath: /secure-data
      Layers:
        - !Ref SecurityLayer

  SecureLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
      Policies:
        - PolicyName: least-privilege-policy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                Resource:
                  - !Sub '${DataBucket.Arn}/*'
                Condition:
                  StringEquals:
                    s3:x-amz-server-side-encryption: AES256
              - Effect: Allow
                Action:
                  - dynamodb:Query
                  - dynamodb:GetItem
                Resource:
                  - !GetAtt SecureTable.Arn
                  - !Sub '${SecureTable.Arn}/index/*'
              - Effect: Allow
                Action:
                  - secretsmanager:GetSecretValue
                Resource: !Ref SecureSecretArn
              - Effect: Deny
                Action:
                  - "*"
                Resource: "*"
                Condition:
                  Bool:
                    aws:SecureTransport: false

  # Resource-based policy for cross-account access
  LambdaPermissionCrossAccount:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref SecureLambdaFunction
      Action: lambda:InvokeFunction
      Principal: "123456789012.amazonaws.com"
      SourceAccount: "123456789012"
      SourceArn: !Sub 'arn:aws:lambda:${AWS::Region}:123456789012:function:*'
```

### 2. Error Handling và Dead Letter Queue

```python
# Robust error handling with retries and DLQ
import json
import boto3
import traceback
from functools import wraps
from typing import Callable, Any

sqs = boto3.client('sqs')
sns = boto3.client('sns')

def with_retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for automatic retry with exponential backoff"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except RetryableException as e:
                    last_exception = e
                    if attempt < max_attempts:
                        time.sleep(current_delay)
                        current_delay *= backoff
                        continue
                except NonRetryableException as e:
                    raise
                except Exception as e:
                    last_exception = e
                    if is_retryable_error(e):
                        if attempt < max_attempts:
                            time.sleep(current_delay)
                            current_delay *= backoff
                            continue
                    raise
            
            raise last_exception
        return wrapper
    return decorator

class RetryableException(Exception):
    """Exception that should trigger retry"""
    pass

class NonRetryableException(Exception):
    """Exception that should not trigger retry"""
    pass

def is_retryable_error(error: Exception) -> bool:
    """Check if error is retryable"""
    retryable_codes = [
        'ThrottlingException',
        'ProvisionedThroughputExceededException',
        'ServiceUnavailable',
        'InternalServerError'
    ]
    
    error_type = type(error).__name__
    error_message = str(error)
    
    return error_type in retryable_codes or any(
        code in error_message for code in retryable_codes
    )

def send_to_dlq(message: dict, error: Exception, context: Any = None):
    """Send failed message to Dead Letter Queue"""
    dlq_message = {
        'original_message': message,
        'error': {
            'type': type(error).__name__,
            'message': str(error),
            'traceback': traceback.format_exc()
        },
        'context': {
            'function_name': context.function_name if context else None,
            'request_id': context.aws_request_id if context else None,
            'invoked_function_arn': context.invoked_function_arn if context else None
        },
        'timestamp': datetime.utcnow().isoformat()
    }
    
    sqs.send_message(
        QueueUrl=os.environ['DLQ_URL'],
        MessageBody=json.dumps(dlq_message),
        MessageAttributes={
            'error_type': {
                'DataType': 'String',
                'StringValue': type(error).__name__
            },
            'retry_count': {
                'DataType': 'Number',
                'StringValue': '0'
            }
        }
    )

def send_alert(error: Exception, context: Any):
    """Send alert for critical errors"""
    if should_alert(error):
        sns.publish(
            TopicArn=os.environ['ALERT_TOPIC_ARN'],
            Subject=f"Lambda Error: {context.function_name}",
            Message=json.dumps({
                'function': context.function_name,
                'error': str(error),
                'request_id': context.aws_request_id
            })
        )

def should_alert(error: Exception) -> bool:
    """Determine if error should trigger alert"""
    critical_errors = ['DataLossException', 'LimitExceededException']
    return type(error).__name__ in critical_errors

@with_retry(max_attempts=3)
def process_order(order_data: dict) -> dict:
    """Example function with retry logic"""
    # Simulated processing
    result = save_to_database(order_data)
    return result

def handler(event, context):
    """Main Lambda handler with error handling"""
    try:
        for record in event.get('Records', []):
            order_data = json.loads(record['body'])
            result = process_order(order_data)
            
        return {
            'statusCode': 200,
            'body': json.dumps({'processed': len(event.get('Records', []))})
        }
        
    except Exception as e:
        print(f"Error processing message: {e}")
        send_to_dlq(event, e, context)
        send_alert(e, context)
        raise
```

### 3. Cold Start Optimization

```python
# Minimize cold starts with lazy loading và connection pooling
import json
import os
import boto3
from functools import lru_cache
from contextlib import contextmanager

# Global connection pools
_db_pool = None
_s3_client = None
_secrets_client = None

def get_db_pool():
    """Lazy initialize database connection pool"""
    global _db_pool
    if _db_pool is None:
        import psycopg2
        from psycopg2 import pool
        _db_pool = pool.ThreadedConnectionPool(
            minconn=int(os.environ.get('DB_POOL_MIN', 2)),
            maxconn=int(os.environ.get('DB_POOL_MAX', 10)),
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            port=int(os.environ.get('DB_PORT', 5432))
        )
    return _db_pool

@lru_cache(maxsize=1)
def get_secrets():
    """Cache secrets to avoid repeated API calls"""
    import json
    secrets_client = get_secrets_client()
    response = secrets_client.get_secret_value(
        SecretId=os.environ['SECRET_ARN']
    )
    return json.loads(response['SecretString'])

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    pool = get_db_pool()
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)

def get_s3_client():
    """Lazy initialize S3 client"""
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client('s3')
    return _s3_client

def get_secrets_client():
    """Lazy initialize Secrets Manager client"""
    global _secrets_client
    if _secrets_client is None:
        _secrets_client = boto3.client('secretsmanager')
    return _secrets_client

@lru_cache(maxsize=100)
def get_cached_data(key: str) -> dict:
    """Cache frequently accessed data"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM cache WHERE key = %s", (key,))
        result = cursor.fetchone()
        return json.loads(result[0]) if result else None

def handler(event, context):
    """Optimized Lambda handler"""
    # Pre-warm connections
    _ = get_secrets()  # Load secrets during warm start
    
    # Process event
    result = process_event(event)
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

## Common Patterns

### Pattern 1: Lambda Destinations

```yaml
# Lambda Destinations configuration
Resources:
  MainFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: main-processor
      Handler: index.handler
      Runtime: python3.11
      Code:
        S3Bucket: !Ref CodeBucket
        S3Key: functions/main.zip
      EventInvokeConfig:
        DestinationConfig:
          OnSuccess:
            Destination: !GetAtt SuccessQueue.Arn
            Type: SQS
          OnFailure:
            Destination: !GetAtt FailureQueue.Arn
            Type: SQS
        MaximumEventAge: 3600
        MaximumRetryAttempts: 2
      ReservedConcurrentExecutions: 50

  SuccessQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: success-queue
      VisibilityTimeout: 300
      MessageRetentionPeriod: 86400
      RedrivePolicy:
        maxReceiveCount: 3
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn

  FailureQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: failure-queue
      VisibilityTimeout: 300
      MessageRetentionPeriod: 1209600  # 14 days

  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: dlq
      MessageRetentionPeriod: 1209600
```

### Pattern 2: Lambda Concurrency Controls

```yaml
# Concurrency control
Resources:
  # Standard function
  StandardFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: standard-processor
      Handler: index.handler
      Runtime: python3.11
      ReservedConcurrentExecutions: 100
      ProvisionedConcurrencyConfig:
        ProvisionedConcurrentExecutions: 10

  # Burstable function with reserved concurrency
  BurstableFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: burstable-processor
      Handler: index.handler
      Runtime: python3.11
      ReservedConcurrentExecutions: 5

  # Account-level concurrency settings
  AccountLevelConcurrency:
    Type: AWS::Lambda::Concurrency
    Properties:
      Resource: !GetAtt StandardFunction.Arn
      ProvisionedConcurrency:
        ProvisionedConcurrentExecutions: 20

  # Version và Alias for traffic shifting
  FunctionVersion:
    Type: AWS::Lambda::Version
    Properties:
      FunctionName: !Ref StandardFunction

  ProductionAlias:
    Type: AWS::Lambda::Alias
    Properties:
      FunctionName: !Ref StandardFunction
      FunctionVersion: !GetAtt FunctionVersion.Version
      Name: production
      RoutingConfig:
        AdditionalVersionWeights:
          - FunctionVersion: "3"
            FunctionWeight: 0.05  # 5% traffic to v3
```

### Pattern 3: Lambda Layers với Custom Runtime

```bash
# Create custom runtime layer
# bootstrap script
#!/bin/sh
# Custom runtime bootstrap

# Load dependencies
export LD_LIBRARY_PATH=/opt/lib:$LD_LIBRARY_PATH

# Stream handler
while true
do
  HEADERS="$(mktemp)"
  EVENT_DATA=$(mktemp)
  
  # Read event from Lambda Runtime API
  curl -sS -X GET "http://${AWS_LAMBDA_RUNTIME_API}/2018-06-01/runtime/invocation/next" \
    -D $HEADERS > $EVENT_DATA
  
  REQUEST_ID=$(grep -i Lambda-Runtime-Aws-Request-Id $HEADERS | cut -d: -f2 | tr -d ' \r')
  
  # Execute handler
  RESPONSE=$(/opt/bin/custom-handler < $EVENT_DATA)
  
  # Send response
  curl -sS -X POST "http://${AWS_LAMBDA_RUNTIME_API}/2018-06-01/runtime/invocation/${REQUEST_ID}/response" \
    -d "$RESPONSE"
  
  # Cleanup
  rm $HEADERS $EVENT_DATA
done

# Create layer package
mkdir -p custom-runtime/bootstrap
cp bootstrap custom-runtime/bootstrap/
cp -r bin/ custom-runtime/
cp -r lib/ custom-runtime/

zip -r custom-runtime.zip custom-runtime/

aws lambda publish-layer-version \
  --layer-name custom-runtime \
  --description "Custom runtime with dependencies" \
  --content S3Bucket=my-bucket,S3Key=layers/custom-runtime.zip \
  --compatible-runtimes provided.al2023
```

## Troubleshooting

### Common Issues và Solutions

**1. Timeout Errors**

```bash
# Check function configuration
aws lambda get-function-configuration \
  --function-name my-function

# View CloudWatch logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "Task timed out" \
  --start-time 1705939200000

# Increase timeout
aws lambda update-function-configuration \
  --function-name my-function \
  --timeout 300

# Common causes:
# - Cold start taking too long
# - External API slow to respond
# - Database connection timeout
# - Large payload processing

# Solutions:
# 1. Increase memory for faster cold starts
# 2. Use VPC endpoint for internal services
# 3. Optimize code (lazy loading, caching)
# 4. Async processing for long operations
```

**2. Memory Exhaustion**

```bash
# Check memory usage
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "REPORT" \
  --start-time 1705939200000

# View memory metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name MemoryUtilization \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time 1705939200 \
  --end-time 1706025600 \
  --period 60 \
  --statistics Average,Maximum

# Check for memory errors in logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "fatal" \
  --start-time 1705939200000

# Increase memory
aws lambda update-function-configuration \
  --function-name my-function \
  --memory-size 1024
```

**3. Concurrent Execution Limits**

```bash
# Check current usage
aws lambda get-account-settings \
  --query 'AccountLimit.[UnreservedConcurrentExecutions,ReservedConcurrentExecutions]'

# Check function concurrency
aws lambda get-function-concurrency \
  --function-name my-function

# Remove reserved concurrency if needed
aws lambda delete-function-concurrency \
  --function-name my-function

# Request limit increase
aws service-quotas request-service-quota-increase \
  --service-code lambda \
  --quota-code L-B99A9384 \
  --desired-value 1000

# Monitor concurrent executions
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name ConcurrentExecutions \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time 1705939200 \
  --end-time 1706025600 \
  --period 300 \
  --statistics Maximum
```

**4. IAM Permission Issues**

```bash
# Check function policies
aws lambda get-policy \
  --function-name my-function

# Check execution role
aws iam get-role \
  --role-name my-function-role

# Simulate policy
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/my-function-role \
  --action-names lambda:InvokeFunction \
  --resource-arns arn:aws:lambda:us-east-1:123456789012:function:my-function

# Check CloudWatch logs for access denied
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "AccessDenied" \
  --start-time 1705939200000
```

## Examples

### Example 1: Complete SAM Application

```yaml
# template.yaml - Complete SAM template
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Production Serverless Application

Globals:
  Function:
    Timeout: 30
    MemorySize: 512
    Runtime: python3.11
    Tracing: Active
    PackageType: Zip
    DeadLetterQueue:
      Type: SQS
      TargetArn: !GetAtt DeadLetterQueue.Arn
    Environment:
      Variables:
        LOG_LEVEL: info
        ENVIRONMENT: production
    VpcConfig:
      SecurityGroupIds:
        - !Ref LambdaSecurityGroup
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2

Resources:
  # DynamoDB Table
  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: users
      BillingMode: PAY_PER_REQUEST
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      AttributeDefinitions:
        - AttributeName: user_id
          AttributeType: S
        - AttributeName: email
          AttributeType: S
        - AttributeName: created_at
          AttributeType: S
      KeySchema:
        - AttributeName: user_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: email-index
          KeySchema:
            - AttributeName: email
              KeyType: HASH
          Projection:
            ProjectionType: ALL
        - IndexName: created-at-index
          KeySchema:
            - AttributeName: created_at
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      SSESpecification:
        SSEEnabled: true
        SSEType: KMS
        KMSMasterKeyId: !GetAtt TableKMSKey.Arn

  # S3 Bucket
  AssetsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::StackName}-assets'
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: AbortIncompleteUploads
            Status: Enabled
            AbortIncompleteMultipartUploadDays: 7
          - Id: TransitionToGlacier
            Status: Enabled
            NoncurrentVersionTransitions:
              - NoncurrentDays: 30
                StorageClass: GLACIER
      CorsConfiguration:
        CorsRules:
          - AllowedOrigins:
              - https://example.com
            AllowedMethods:
              - GET
              - PUT
              - POST
            AllowedHeaders:
              - '*'
            MaxAge: 3600

  # KMS Key
  TableKMSKey:
    Type: AWS::KMS::Key
    Properties:
      Description: KMS key for DynamoDB encryption
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: kms:*
            Resource: '*'
          - Sid: Allow Lambda to use key
            Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action:
              - kms:Encrypt
              - kms:Decrypt
            Resource: '*'

  # SNS Topic
  NotificationTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub '${AWS::StackName}-notifications'
      DisplayName: Production Notifications

  # Dead Letter Queue
  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub '${AWS::StackName}-dlq'
      MessageRetentionPeriod: 1209600
      VisibilityTimeout: 3600

  # User Management Function
  UserManagementFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-user-management'
      Handler: src.users.handler
      CodeUri: src/
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
        - SNSPublishMessagePolicy:
            TopicArn: !Ref NotificationTopic
        - Statement:
            - Sid: SecretsManagerAccess
              Effect: Allow
              Action:
                - secretsmanager:GetSecretValue
              Resource: '*'
      Environment:
        Variables:
          SNS_TOPIC_ARN: !Ref NotificationTopic
      Events:
        ApiUserCreate:
          Type: Api
          Properties:
            Path: /users
            Method: POST
        ApiUserGet:
          Type: Api
          Properties:
            Path: /users/{user_id}
            Method: GET
        ApiUserUpdate:
          Type: Api
          Properties:
            Path: /users/{user_id}
            Method: PATCH
        ApiUserDelete:
          Type: Api
          Properties:
            Path: /users/{user_id}
            Method: DELETE
        ApiUserList:
          Type: Api
          Properties:
            Path: /users
            Method: GET
      ProvisionedConcurrency: 5
      AutoPublishAlias: production

  # File Processing Function
  FileProcessingFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-file-processing'
      Handler: src.processing.handler
      MemorySize: 1024
      Timeout: 300
      CodeUri: src/
      Policies:
        - S3ReadPolicy:
            BucketName: !Ref AssetsBucket
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
      Events:
        S3Upload:
          Type: S3
          Properties:
            Bucket: !Ref AssetsBucket
            Events:
              - s3:ObjectCreated:*
        S3Delete:
          Type: S3
          Properties:
            Bucket: !Ref AssetsBucket
            Events:
              - s3:ObjectRemoved:*
      ReservedConcurrentExecutions: 10

  # Scheduled Maintenance Function
  MaintenanceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub '${AWS::StackName}-maintenance'
      Handler: src.maintenance.handler
      MemorySize: 512
      Timeout: 900
      CodeUri: src/
      Environment:
        Variables:
          RETENTION_DAYS: "90"
      Events:
        DailySchedule:
          Type: Schedule
          Properties:
            Schedule: cron(0 3 * * ? *)
        WeeklyCleanup:
          Type: Schedule
          Properties:
            Schedule: cron(0 4 ? * SUN *)

  # API Gateway
  ApiGateway:
    Type: AWS::Serverless::Api
    Properties:
      Name: !Sub '${AWS::StackName}-api'
      StageName: prod
      Auth:
        Authorizers:
          CognitoAuthorizer:
            UserPoolArn: !GetAtt UserPool.Arn
        DefaultAuthorizer: CognitoAuthorizer
      MethodSettings:
        - ResourcePath: /users
          HttpMethod: POST
          MetricsEnabled: true
          LoggingLevel: INFO
          DataTraceEnabled: true
      DefinitionBody:
        swagger: "2.0"
        info:
          title: !Ref AWS::StackName
        paths:
          /users:
            get:
              x-amazon-apigateway-integration:
                uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${UserManagementFunction.Arn}/invocations'
                httpMethod: POST
                type: aws_proxy
            post:
              x-amazon-apigateway-integration:
                uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${UserManagementFunction.Arn}/invocations'
                httpMethod: POST
                type: aws_proxy
          /users/{user_id}:
            get:
              x-amazon-apigateway-integration:
                uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${UserManagementFunction.Arn}/invocations'
                httpMethod: POST
                type: aws_proxy
            patch:
              x-amazon-apigateway-integration:
                uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${UserManagementFunction.Arn}/invocations'
                httpMethod: POST
                type: aws_proxy
            delete:
              x-amazon-apigateway-integration:
                uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${UserManagementFunction.Arn}/invocations'
                httpMethod: POST
                type: aws_proxy

Outputs:
  ApiEndpoint:
    Description: API Gateway endpoint URL
    Value: !Sub 'https://${ApiGateway}.execute-api.${AWS::Region}.amazonaws.com/prod/'
    Export:
      Name: !Sub '${AWS::StackName}-api-endpoint'

  UsersTableName:
    Description: Users DynamoDB table name
    Value: !Ref UsersTable
    Export:
      Name: !Sub '${AWS::StackName}-users-table'

  UserManagementFunction:
    Description: User management Lambda function ARN
    Value: !GetAtt UserManagementFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-user-management-function'
```

```python
# src/users.py - User management handler
import json
import os
import boto3
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Main handler for user management API"""
    
    http_method = event.get('httpMethod')
    path = event.get('path', '')
    
    try:
        if http_method == 'GET' and '/users/' in path:
            user_id = path.split('/')[-1]
            return get_user(user_id)
        elif http_method == 'GET':
            return list_users(event.get('queryStringParameters', {}))
        elif http_method == 'POST' and path == '/users':
            return create_user(json.loads(event.get('body', '{}')))
        elif http_method == 'PATCH' and '/users/' in path:
            user_id = path.split('/')[-1]
            return update_user(user_id, json.loads(event.get('body', '{}')))
        elif http_method == 'DELETE' and '/users/' in path:
            user_id = path.split('/')[-1]
            return delete_user(user_id)
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_user(user_id: str) -> Dict[str, Any]:
    """Get user by ID"""
    table = dynamodb.Table(os.environ.get('USERS_TABLE', 'users'))
    response = table.get_item(Key={'user_id': user_id})
    
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Item'])
    }

def list_users(params: Dict[str, Any]) -> Dict[str, Any]:
    """List users with pagination"""
    table = dynamodb.Table(os.environ.get('USERS_TABLE', 'users'))
    
    scan_kwargs = {}
    if params:
        limit = int(params.get('limit', 20))
        scan_kwargs['Limit'] = limit
        
        if params.get('last_key'):
            scan_kwargs['ExclusiveStartKey'] = {'user_id': params['last_key']}
    
    response = table.scan(**scan_kwargs)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'items': response.get('Items', []),
            'count': response.get('Count', 0),
            'last_key': response.get('LastEvaluatedKey', {}).get('user_id')
        })
    }

def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create new user"""
    table = dynamodb.Table(os.environ.get('USERS_TABLE', 'users'))
    
    user_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    user = {
        'user_id': user_id,
        'email': data['email'],
        'name': data.get('name', ''),
        'created_at': timestamp,
        'updated_at': timestamp,
        'status': 'active'
    }
    
    table.put_item(Item=user)
    
    # Publish notification
    sns.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Subject='New User Created',
        Message=json.dumps(user)
    )
    
    return {
        'statusCode': 201,
        'body': json.dumps(user)
    }

def update_user(user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update existing user"""
    table = dynamodb.Table(os.environ.get('USERS_TABLE', 'users'))
    
    # Build update expression
    update_expr = 'SET updated_at = :updated_at'
    expr_values = {':updated_at': datetime.utcnow().isoformat()}
    expr_names = {}
    
    for key, value in data.items():
        if key != 'user_id' and key != 'created_at':
            update_expr += f', #{key} = :{key}'
            expr_values[f':{key}'] = value
            expr_names[f'#{key}'] = key
    
    try:
        response = table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ReturnValues='ALL_NEW'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Attributes', {}))
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }

def delete_user(user_id: str) -> Dict[str, Any]:
    """Delete user"""
    table = dynamodb.Table(os.environ.get('USERS_TABLE', 'users'))
    
    try:
        response = table.delete_item(
            Key={'user_id': user_id},
            ReturnValues='ALL_OLD'
        )
        
        if 'Attributes' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Attributes', {}))
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

## References

### Official Documentation
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- [Lambda Extensions](https://docs.aws.amazon.com/lambda/latest/dg/lambda-extensions.html)
- [Lambda Power Tuning](https://docs.aws.amazon.com/lambda/latest/dg/services-power-tuning.html)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)

### Tools
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/)
- [AWS Serverless Application Repository](https://serverlessrepo.aws.amazon.com/)
- [Chalice (Python Serverless)](https://aws.github.io/chalice/)

### Best Practices
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Lambda Performance Optimization](https://docs.aws.amazon.com/lambda/latest/dg/performance.html)
- [Lambda Security Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/security-best-practices.html)
- [Serverless Land Patterns](https://serverlessland.com/patterns)
