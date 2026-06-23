---
title: "AWS S3 Storage Best Practices"
description: "Hướng dẫn toàn diện về Amazon S3 buckets, lifecycle policies, replication, presigned URLs, multipart upload và Glacier archive"
tags: ["aws", "s3", "storage", "glacier", "lifecycle", "replication", "presigned-urls"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# AWS S3 Storage Best Practices

## Tổng Quan (Overview)

Amazon Simple Storage Service (S3) là object storage service cung cấp industry-leading scalability, data availability, security, và performance. S3 được sử dụng rộng rãi trong enterprise environments cho nhiều use cases từ data lakes, backup và restore, disaster recovery, cho đến static website hosting và application data storage.

Tài liệu này bao gồm các best practices và implementation patterns cho việc sử dụng S3 trong môi trường enterprise, bao gồm bucket configuration, lifecycle policies, cross-region replication, security mechanisms như presigned URLs và bucket policies, cũng như chiến lược tối ưu chi phí với S3 Intelligent-Tiering và Glacier.

S3 là một trong những dịch vụ foundation của AWS, với 11 9's durability (99.999999999%) và 99.99% availability SLA. Việc nắm vững các tính năng và best practices của S3 là điều kiện tiên quyết cho bất kỳ enterprise architecture nào trên AWS.

## Mục Đích (Purpose)

Mục đích chính của tài liệu này bao gồm:

1. **Data Protection**: Thiết lập appropriate access controls, encryption và replication để bảo vệ dữ liệu
2. **Cost Optimization**: Sử dụng lifecycle policies và storage classes hiệu quả để giảm chi phí
3. **Performance**: Tối ưu hóa performance với multipart uploads, transfer acceleration và prefixes
4. **Compliance**: Hỗ trợ các compliance requirements như GDPR, HIPAA, SEC
5. **Data Governance**: Implement data retention policies và audit trails

## Các Khái Niệm Chính (Key Concepts)

### 1. S3 Storage Classes

AWS cung cấp nhiều storage classes để tối ưu chi phí theo access patterns:

| Storage Class | Use Case | Durability | Min Storage Duration | Price Considerations |
|---------------|----------|------------|---------------------|---------------------|
| S3 Standard | Frequently accessed data | 11 9's | None | Higher storage, lower access |
| S3 Intelligent-Tiering | Unknown/variable access | 11 9's | 30 days | Monitoring + storage fees |
| S3 Standard-IA | Infrequent access (>30 days) | 11 9's | 30 days | Lower storage, retrieval fees |
| S3 Glacier Instant Retrieval | Archive with ms retrieval | 11 9's | 90 days | Lower storage, retrieval fees |
| S3 Glacier Flexible Retrieval | Long-term archive | 11 9's | 90 days | Very low storage, retrieval in minutes to hours |
| S3 Glacier Deep Archive | Compliance archive | 11 9's | 180 days | Lowest storage cost |
| S3 Outposts | On-premises object storage | Configurable | None | Highest cost, local access |

**Chọn Storage Class:**
```bash
# Upload với specific storage class
aws s3 cp local-file.txt s3://my-bucket/data/ \
  --storage-class STANDARD

# Upload với Intelligent-Tiering
aws s3 cp local-file.txt s3://my-bucket/data/ \
  --storage-class INTELLIGENT_TIERING

# Upload với Glacier Instant Retrieval
aws s3 cp archive.zip s3://my-bucket/archive/ \
  --storage-class GLACIER
```

### 2. Bucket Configuration

```yaml
# CloudFormation cho S3 Bucket với comprehensive configuration
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  DataLakeBucket:
    Type: AWS::S3::Bucket
    DeletionPolicy: Retain
    Properties:
      BucketName: !Sub '${AWS::StackName}-datalake-${AWS::AccountId}'
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
            BucketKeyEnabled: true
      VersioningConfiguration:
        Status: Enabled
      ObjectLockConfiguration:
        ObjectLockEnabled: Enabled
        Rule:
          DefaultRetention:
            Mode: GOVERNANCE
            Years: 1
      LifecycleConfiguration:
        Rules:
          - Id: ArchiveOldData
            Status: Enabled
            Prefix: logs/
            Transitions:
              - TransitionInDays: 30
                StorageClass: STANDARD_IA
              - TransitionInDays: 90
                StorageClass: GLACIER
              - TransitionInDays: 365
                StorageClass: DEEP_ARCHIVE
            ExpirationInDays: 2555
          - Id: DeleteIncompleteUploads
            Status: Enabled
            AbortIncompleteMultipartUploadDays: 7
      Tags:
        - Key: Environment
          Value: Production
        - Key: DataClassification
          Value: Confidential

  DataLakeBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref DataLakeBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: EnforceTLS
            Effect: Deny
            Principal:
              AWS: '*'
            Action:
              - s3:*"
            Resource:
              - !Sub '${DataLakeBucket.Arn}'
              - !Sub '${DataLakeBucket.Arn}/*'
            Condition:
              Bool:
                aws:SecureTransport: false
          - Sid: RestrictAccess
            Effect: Deny
            Principal:
              AWS: '*'
            Action:
              - s3:GetObject
            Resource:
              - !Sub '${DataLakeBucket.Arn}/*'
            Condition:
              IpAddress:
                aws:SourceIp:
                  - "10.0.0.0/8"
                  - "172.16.0.0/12"
              Bool:
                aws:ViaAWSService: false
```

### 3. S3 Lifecycle Policies

Lifecycle policies là cách hiệu quả để tự động hóa việc chuyển đổi objects giữa các storage classes.

```json
{
  "Rules": [
    {
      "ID": "LogArchivalPolicy",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "application-logs/"
      },
      "Transitions": [
        {
          "Days": 7,
          "StorageClass": "INTELLIGENT_TIERING"
        },
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        },
        {
          "Days": 365,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ],
      "NoncurrentVersionTransitions": [
        {
          "NoncurrentDays": 7,
          "StorageClass": "GLACIER"
        }
      ],
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 365
      },
      "AbortIncompleteMultipartUpload": {
        "DaysAfterInitiation": 7
      }
    },
    {
      "ID": "TemporaryFilesPolicy",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "temp/"
      },
      "Expiration": {
        "Days": 7
      }
    },
    {
      "ID": "FinancialDataPolicy",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "financial/"
      },
      "Transitions": [
        {
          "Days": 1,
          "StorageClass": "GLACIER"
        }
      ],
      "NoncurrentVersionTransitions": [
        {
          "NoncurrentDays": 1,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ]
    }
  ]
}
```

```bash
# Apply lifecycle configuration
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle-policy.json

# View current lifecycle configuration
aws s3api get-bucket-lifecycle-configuration \
  --bucket my-bucket
```

### 4. Cross-Region Replication (CRR)

CRR tự động replicate objects đến một bucket ở region khác, hữu ích cho disaster recovery, latency reduction, và compliance.

```yaml
# S3 Replication Configuration
Resources:
  ReplicationBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::StackName}-replica-${AWS::Region}'
      Region: us-west-2

  ReplicatedBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref ReplicationBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: AllowReplication
            Effect: Allow
            Principal:
              Service: s3.amazonaws.com
            Action:
              - s3:ReplicateObject
              - s3:ReplicateDelete
              - s3:ObjectOwnerOverrideToBucketOwner
            Resource:
              - !Sub '${ReplicationBucket.Arn}/*'

  ReplicationRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: s3.amazonaws.com
            Action: sts:AssumeRole

  ReplicationPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: replication-policy
      Roles:
        - !Ref ReplicationRole
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - s3:GetObjectVersionForReplication
              - s3:GetObjectVersionAcl
              - s3:GetObjectVersionTagging
            Resource:
              - !Sub '${PrimaryBucket.Arn}/*'
          - Effect: Allow
            Action:
              - s3:ListObjects
              - s3:GetBucketVersioning
              - s3:GetBucketLocation
            Resource: !Sub '${PrimaryBucket.Arn}'
          - Effect: Allow
            Action:
              - s3:ReplicateObject
              - s3:ReplicateDelete
              - s3:ObjectOwnerOverrideToBucketOwner
              - s3:ReplicateTags
            Resource:
              - !Sub '${ReplicationBucket.Arn}/*'

  PrimaryBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::StackName}-primary'
      ReplicationConfiguration:
        Role: !GetAtt ReplicationRole.Arn
        Rules:
          - ID: replicate-all
            Status: Enabled
            Priority: 1
            DeleteMarkerReplication:
              Status: Enabled
            Filter:
              Prefix: ""
            Destination:
              Bucket: !GetAtt ReplicationBucket.Arn
              StorageClass: GLACIER
              EncryptionConfiguration:
                ReplicaKmsKeyID: !Ref ReplicationKMSKey
              Metrics:
                Status: Enabled
                EventThreshold:
                  Minutes: 15
              ReplicationTime:
                Status: Enabled
                Time:
                  Minutes: 15
```

### 5. Presigned URLs

Presigned URLs cho phép temporary access đến objects mà không cần public access.

```python
# Python script để generate presigned URLs
import boto3
import argparse
from datetime import datetime, timedelta

def generate_presigned_url(bucket_name, object_key, expiration_minutes=60, http_method='GET'):
    """
    Generate presigned URL cho S3 object access
    
    Args:
        bucket_name: S3 bucket name
        object_key: Object key trong bucket
        expiration_minutes: Thời gian URL có hiệu lực (phút)
        http_method: HTTP method (GET, PUT, DELETE, etc.)
    
    Returns:
        Presigned URL string
    """
    s3_client = boto3.client('s3')
    
    try:
        if http_method == 'GET':
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_key},
                ExpiresIn=expiration_minutes * 60
            )
        elif http_method == 'PUT':
            url = s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': bucket_name, 'Key': object_key},
                ExpiresIn=expiration_minutes * 60
            )
        elif http_method == 'POST':
            url = s3_client.generate_presigned_post(
                Bucket=bucket_name,
                Key=object_key,
                Conditions=[
                    ['content-length-range', 1, 104857600],  # Max 100MB
                    {'Content-Type': 'application/octet-stream'}
                ],
                ExpiresIn=expiration_minutes * 60
            )
        else:
            url = s3_client.generate_presigned_url(
                http_method.lower() + '_object',
                Params={'Bucket': bucket_name, 'Key': object_key},
                ExpiresIn=expiration_minutes * 60
            )
        
        return url
    
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None

def generate_multipart_upload_urls(bucket_name, object_key, num_parts=10, expiration_minutes=60):
    """
    Generate presigned URLs cho multipart upload
    """
    s3_client = boto3.client('s3')
    
    try:
        # Initiate multipart upload
        response = s3_client.create_multipart_upload(
            Bucket=bucket_name,
            Key=object_key
        )
        
        upload_id = response['UploadId']
        
        # Generate presigned URLs for each part
        part_urls = []
        for part_number in range(1, num_parts + 1):
            url = s3_client.generate_presigned_url(
                'upload_part',
                Params={
                    'Bucket': bucket_name,
                    'Key': object_key,
                    'UploadId': upload_id,
                    'PartNumber': part_number
                },
                ExpiresIn=expiration_minutes * 60
            )
            part_urls.append({
                'part_number': part_number,
                'url': url
            })
        
        return {
            'upload_id': upload_id,
            'bucket': bucket_name,
            'key': object_key,
            'part_urls': part_urls
        }
    
    except ClientError as e:
        print(f"Error initiating multipart upload: {e}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate S3 presigned URLs')
    parser.add_argument('action', choices=['get', 'put', 'upload'], 
                        help='Action: get (download), put (upload), upload (multipart)')
    parser.add_argument('--bucket', required=True, help='S3 bucket name')
    parser.add_argument('--key', required=True, help='Object key')
    parser.add_argument('--expiration', type=int, default=60, 
                        help='Expiration time in minutes')
    
    args = parser.parse_args()
    
    if args.action == 'get':
        url = generate_presigned_url(args.bucket, args.key, args.expiration, 'GET')
        print(f"Download URL:\n{url}")
    elif args.action == 'put':
        url = generate_presigned_url(args.bucket, args.key, args.expiration, 'PUT')
        print(f"Upload URL:\n{url}")
    elif args.action == 'upload':
        result = generate_multipart_upload_urls(args.bucket, args.key, 10, args.expiration)
        print(f"Upload ID: {result['upload_id']}")
        print(f"Part URLs:")
        for part in result['part_urls']:
            print(f"  Part {part['part_number']}: {part['url']}")
```

```bash
# AWS CLI commands cho presigned URLs
# Generate presigned URL for download (1 hour expiration)
aws s3 presign s3://my-bucket/documents/report.pdf \
  --expires-in 3600

# Generate presigned URL for upload
aws s3 presign s3://my-bucket/uploads/file.zip \
  --expires-in 1800 \
  --region us-east-1

# Generate presigned URL với custom response headers
aws s3 presign s3://my-bucket/private/document.pdf \
  --expires-in 3600 \
  --response-content-disposition "attachment; filename=\"custom-name.pdf\"" \
  --response-cache-control "no-cache"
```

### 6. Multipart Upload

Multipart upload cho phép upload large files (up to 5TB) thành multiple parts.

```python
# Python script cho optimized multipart upload
import boto3
import os
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class S3MultipartUploader:
    def __init__(self, bucket, key, file_path, part_size_mb=8, num_threads=10):
        self.s3_client = boto3.client('s3')
        self.bucket = bucket
        self.key = key
        self.file_path = file_path
        self.part_size = part_size_mb * 1024 * 1024  # Convert to bytes
        self.num_threads = num_threads
        self.upload_id = None
        self.parts = []
        self.etags_lock = threading.Lock()
    
    def calculate_part_size(self):
        """Calculate optimal part size based on file size"""
        file_size = os.path.getsize(self.file_path)
        
        # S3 limits: min 5MB, max 5GB per part
        # Default 8MB is good for most cases
        if file_size <= 100 * 1024 * 1024:  # < 100MB
            return 5 * 1024 * 1024  # 5MB minimum
        elif file_size <= 5 * 1024 * 1024 * 1024:  # < 5GB
            return self.part_size
        else:
            # Ensure we don't exceed 10,000 parts limit
            num_parts = (file_size // (5 * 1024 * 1024 * 1024)) + 1
            return max(5 * 1024 * 1024, file_size // min(num_parts, 10000))
    
    def upload_part(self, part_number, start_byte, end_byte):
        """Upload a single part"""
        part_size = end_byte - start_byte
        
        with open(self.file_path, 'rb') as f:
            f.seek(start_byte)
            data = f.read(part_size)
        
        # Calculate MD5 for this part
        md5_hash = hashlib.md5(data).hexdigest()
        
        try:
            response = self.s3_client.upload_part(
                Bucket=self.bucket,
                Key=self.key,
                Body=data,
                PartNumber=part_number,
                UploadId=self.upload_id,
                ContentMD5=md5_hash
            )
            
            etag = response['ETag']
            
            with self.etags_lock:
                self.parts.append({
                    'PartNumber': part_number,
                    'ETag': etag
                })
            
            print(f"Part {part_number} uploaded successfully")
            return part_number, etag
            
        except Exception as e:
            print(f"Error uploading part {part_number}: {e}")
            raise
    
    def upload(self):
        """Execute multipart upload"""
        file_size = os.path.getsize(self.file_path)
        part_size = self.calculate_part_size()
        
        print(f"Starting multipart upload for {file_size / (1024*1024):.2f} MB file")
        print(f"Part size: {part_size / (1024*1024):.2f} MB")
        
        # Initiate multipart upload
        try:
            response = self.s3_client.create_multipart_upload(
                Bucket=self.bucket,
                Key=self.key,
                ContentType='application/octet-stream'
            )
            self.upload_id = response['UploadId']
            print(f"Upload ID: {self.upload_id}")
        except Exception as e:
            print(f"Error initiating multipart upload: {e}")
            raise
        
        # Calculate parts
        parts = []
        start_byte = 0
        part_number = 1
        while start_byte < file_size:
            end_byte = min(start_byte + part_size, file_size)
            parts.append((part_number, start_byte, end_byte))
            start_byte = end_byte
            part_number += 1
        
        # Upload parts in parallel
        print(f"Uploading {len(parts)} parts using {self.num_threads} threads...")
        
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = {
                executor.submit(self.upload_part, part[0], part[1], part[2]): part[0]
                for part in parts
            }
            
            for future in as_completed(futures):
                part_number = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Part {part_number} failed: {e}")
                    self.abort()
                    raise
        
        # Complete multipart upload
        self.parts.sort(key=lambda x: x['PartNumber'])
        
        try:
            response = self.s3_client.complete_multipart_upload(
                Bucket=self.bucket,
                Key=self.key,
                UploadId=self.upload_id,
                MultipartUpload={
                    'Parts': self.parts
                }
            )
            print(f"Upload completed: {response['Location']}")
            return response
        except Exception as e:
            print(f"Error completing multipart upload: {e}")
            raise
    
    def abort(self):
        """Abort the multipart upload"""
        if self.upload_id:
            try:
                self.s3_client.abort_multipart_upload(
                    Bucket=self.bucket,
                    Key=self.key,
                    UploadId=self.upload_id
                )
                print("Multipart upload aborted")
            except Exception as e:
                print(f"Error aborting upload: {e}")

# Usage
if __name__ == '__main__':
    uploader = S3MultipartUploader(
        bucket='my-bucket',
        key='uploads/large-file.zip',
        file_path='./large-file.zip',
        part_size_mb=10,
        num_threads=8
    )
    uploader.upload()
```

## Best Practices

### 1. Security Best Practices

```yaml
# Comprehensive bucket policy với multiple security controls
BucketPolicy:
  Type: AWS::S3::BucketPolicy
  Properties:
    Bucket: !Ref DataBucket
    PolicyDocument:
      Version: '2012-10-17'
      Statement:
        # Enforce SSL/TLS
        - Sid: EnforceSSLTLS
          Effect: Deny
          Principal:
            AWS: '*'
          Action:
            - s3:*"
          Resource:
            - !Sub '${DataBucket.Arn}'
            - !Sub '${DataBucket.Arn}/*'
          Condition:
            Bool:
              aws:SecureTransport: false
        
        # Require specific headers
        - Sid: RequireServerSideEncryption
          Effect: Deny
          Principal:
            AWS: '*'
          Action:
            - s3:PutObject
          Resource:
            - !Sub '${DataBucket.Arn}/*'
          Condition:
            StringNotEquals:
              s3:x-amz-server-side-encryption: AES256
        
        # Restrict by VPC Endpoint
        - Sid: RestrictVPCAccess
          Effect: Deny
          Principal:
            AWS: '*'
          Action:
            - s3:GetObject
          Resource:
            - !Sub '${DataBucket.Arn}/*'
          Condition:
            StringNotEquals:
              aws:SourceVpce: !Ref VPCEndpoint
        
        # Require MFA for delete
        - Sid: RequireMFADelete
          Effect: Deny
          Principal:
            AWS: '*'
          Action:
            - s3:DeleteBucket
            - s3:DeleteObject
            - s3:DeleteObjectVersion
          Resource:
            - !Sub '${DataBucket.Arn}'
            - !Sub '${DataBucket.Arn}/*'
          Condition:
            NumericNotEquals:
              s3:x-amz-mfa: "required"
        
        # Audit logging
        - Sid: AllowS3ServerAccessLogsDelivery
          Effect: Allow
          Principal:
            Service: logging.s3.amazonaws.com
          Action:
            - s3:PutObject
          Resource:
            - !Sub '${DataBucket.Arn}/*'
          Condition:
            StringEquals:
              aws:SourceAccount: !Ref AWS::AccountId
              s3:x-amz-acl: bucket-owner-full-control
```

### 2. Cost Optimization Strategies

```bash
# Analyze storage costs với S3 Storage Lens
aws s3control put-storage-lens-configuration \
  --account-id 123456789012 \
  --storage-lens-configuration-id default-config \
  --storage-lens-configuration '{
    "enabled": true,
    "awsOrg": {
      "arn": "arn:aws:organizations::123456789012:organization/o-abc123"
    },
    "tagsAndPrefixesCount": 20,
    "additionalMetadataConfigurations": {},
    "metricsConfigurations": [
      {
        "id": "source-buckets",
        "selectionCriteria": {
          "bucketIncludes": ["*"],
          "prefixIncludes": ["logs/", "data/"]
        }
      }
    ]
  }'

# Check S3 Inventory for analysis
aws s3api put-bucket-inventory-configuration \
  --bucket my-bucket \
  --inventory-configuration '{
    "Destination": {
      "S3BucketDestination": {
        "Format": "Parquet",
        "AccountId": "123456789012",
        "Arn": "arn:aws:s3:::inventory-destination-bucket",
        "Prefix": "reports/my-bucket/inventory"
      }
    },
    "IsEnabled": true,
    "Filter": {
      "Prefix": "logs/"
    },
    "IncludedObjectVersions": "All",
    "OptionalFields": ["Size","LastModified","StorageClass","EncryptionStatus"],
    "Schedule": {
      "Frequency": "Daily"
    }
  }'
```

### 3. Performance Optimization

```bash
# Upload with transfer acceleration
aws s3 cp large-file.zip s3://my-bucket/ \
  --region us-east-1 \
  --storage-class STANDARD \
  --expected-size 1073741824

# Use S3 Transfer Acceleration with CloudFront
# CloudFront distribution fronting S3
aws cloudfront create-distribution \
  --origin-domain-name my-bucket.s3.us-east-1.amazonaws.com \
  --default-root-object index.html

# Parallel downloads
aws s3 cp s3://my-bucket/large-prefix/ ./local-dir/ \
  --recursive \
  --parallel-level 10
```

### 4. Data Protection với Object Lock

```yaml
# Enable Object Lock với COMPLIANCE mode
DataBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: !Sub '${AWS::StackName}-compliant'
    ObjectLockEnabled: true
    ObjectLockConfiguration:
      ObjectLockEnabled: Enabled
      Rule:
        DefaultRetention:
          Mode: COMPLIANCE
          Years: 7
```

```bash
# Apply Object Lock manually
aws s3api put-object \
  --bucket compliant-bucket \
  --key documents/contract.pdf \
  --body contract.pdf \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date "2031-06-23T00:00:00Z"

# Legal Hold (không có expiration)
aws s3api put-object-legal-hold \
  --bucket compliant-bucket \
  --key documents/contract.pdf \
  --legal-hold Status=ON
```

## Common Patterns

### Pattern 1: Data Lake Architecture

```yaml
# S3 Data Lake với multiple zones
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # Raw Zone
  RawZoneBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::StackName}-raw-zone'
      LifecycleConfiguration:
        Rules:
          - Id: MoveToGlacier
            Status: Enabled
            Prefix: "raw/"
            Transitions:
              - TransitionInDays: 90
                StorageClass: GLACIER
      Tags:
        - Key: Zone
          Value: raw

  # Curated Zone
  CuratedZoneBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::StackName}-curated-zone'
      LifecycleConfiguration:
        Rules:
          - Id: IntelligentTiering
            Status: Enabled
            Prefix: "curated/"
            Transitions:
              - TransitionInDays: 30
                StorageClass: INTELLIGENT_TIERING
      Tags:
        - Key: Zone
          Value: curated

  # Analytics Zone
  AnalyticsZoneBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${AWS::StackName}-analytics-zone'
      Tags:
        - Key: Zone
          Value: analytics

  # Glue Database
  GlueDataCatalog:
    Type: AWS::Glue::Database
    Properties:
      CatalogId: !Ref AWS::AccountId
      DatabaseInput:
        Name: !Sub '${AWS::StackName}_datalake'
        Description: Data Lake Glue Catalog
        LocationUri: !Sub 's3://${RawZoneBucket}/'
        Parameters:
          classification: delta
```

### Pattern 2: Static Website Hosting

```yaml
# Static website với CloudFront và Route 53
StaticWebsiteBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: example.com
    WebsiteConfiguration:
      IndexDocument: index.html
      ErrorDocument: error.html
    OwnershipControls:
      Rules:
        - ObjectOwnership: BucketOwnerPreferred

StaticWebsitePolicy:
  Type: AWS::S3::BucketPolicy
  Properties:
    Bucket: !Ref StaticWebsiteBucket
    PolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Sid: CloudFrontReadAccess
          Effect: Allow
          Principal:
            Service: cloudfront.amazonaws.com
          Action:
            - s3:GetObject
          Resource:
            - !Sub '${StaticWebsiteBucket.Arn}/*'
          Condition:
            StringEquals:
              aws:SourceArn: !Sub 'arn:aws:cloudfront::${AWS::AccountId}:distribution/${CloudFrontDistribution}'

CloudFrontDistribution:
  Type: AWS::CloudFront::Distribution
  Properties:
    DistributionConfig:
      Enabled: true
      HttpVersion: http2and3
      DefaultRootObject: index.html
      Aliases:
        - example.com
      ViewerCertificate:
        AcmCertificateArn: !Ref SSLCertificate
        MinimumProtocolVersion: TLSv1.2_2021
        SslSupportMethod: sni-only
      Origins:
        - DomainName: !GetAtt StaticWebsiteBucket.DomainName
          Id: S3Origin
          S3OriginConfig:
            OriginAccessIdentity: !Ref CloudFrontOriginAccessIdentity
      DefaultCacheBehavior:
        TargetOriginId: S3Origin
        ViewerProtocolPolicy: redirect-to-https
        Compress: true
        CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6
        OriginRequestPolicyId: 88a5eaf4-2fd4-4709-b370-b4c650ea3fcf
      CustomErrorResponses:
        - ErrorCode: 404
          ResponseCode: 404
          ResponsePagePath: /error.html
        - ErrorCode: 403
          ResponseCode: 403
          ResponsePagePath: /error.html

CloudFrontOriginAccessIdentity:
  Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
  Properties:
    CloudFrontOriginAccessIdentityConfig:
      Comment: !Sub 'Access identity for ${StaticWebsiteBucket}'
```

## Troubleshooting

### Common Issues và Solutions

**1. Access Denied Errors**

```bash
# Check bucket policy
aws s3api get-bucket-policy --bucket my-bucket --query Policy --output text | jq .

# Check bucket ACL
aws s3api get-bucket-acl --bucket my-bucket

# Check object ACL
aws s3api get-object-acl --bucket my-bucket --key path/to/object

# Check IAM policy
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/myuser \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::my-bucket/path/to/object

# Check VPC endpoint policy
aws ec2 describe-vpc-endpoints --vpc-endpoint-ids vpce-xxx
```

**2. Slow Upload/Download Performance**

```bash
# Enable S3 Transfer Acceleration
aws s3api put-bucket-accelerate-configuration \
  --bucket my-bucket \
  --accelerate-configuration Status=Enabled

# Check current performance metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name 4xxErrors \
  --dimensions Name=BucketName,Value=my-bucket \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T12:00:00Z \
  --period 3600 \
  --statistics Sum

# Use multipart upload for large files
aws s3 cp large-file.zip s3://my-bucket/ \
  --multipart-chunk-size-mb 50
```

**3. Lifecycle Policy Not Working**

```bash
# Verify lifecycle rules
aws s3api get-bucket-lifecycle-configuration --bucket my-bucket

# Check if objects match filter
aws s3api list-objects-v2 --bucket my-bucket --prefix logs/

# Verify versioning is enabled (required for NoncurrentVersion transitions)
aws s3api get-bucket-versioning --bucket my-bucket

# Check CloudTrail for lifecycle events
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=PutBucketLifecycleConfiguration
```

**4. Cross-Region Replication Issues**

```bash
# Check replication status
aws s3api get-bucket-replication --bucket source-bucket

# Check replication metrics
aws s3api get-bucket-replication-metrics --bucket source-bucket

# Verify IAM role permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/s3-replication-role \
  --action-names s3:GetObject,s3:ReplicateObject \
  --resource-arns arn:aws:s3:::source-bucket/*

# Check if objects are encrypted with KMS
# KMS-encrypted objects require additional permissions
aws s3api get-object --bucket source-bucket --key path/to/object | jq '.ServerSideEncryption'
```

## Examples

### Example 1: Automated Backup Solution

```python
#!/usr/bin/env python3
"""
S3 Backup Solution với versioning và cross-region replication
"""
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict

class S3BackupManager:
    def __init__(self, source_bucket: str, dest_bucket: str, dest_region: str):
        self.source_client = boto3.client('s3')
        self.dest_client = boto3.client('s3', region_name=dest_region)
        self.source_bucket = source_bucket
        self.dest_bucket = dest_bucket
        self.dest_region = dest_region
    
    def create_backup_tag(self) -> str:
        """Create timestamp tag for backup"""
        return datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    def list_objects_for_backup(self, prefix: str = '') -> List[Dict]:
        """List all objects in source bucket"""
        objects = []
        paginator = self.source_client.get_paginator('list_objects_v2')
        
        for page in paginator.paginate(Bucket=self.source_bucket, Prefix=prefix):
            if 'Contents' in page:
                for obj in page['Contents']:
                    objects.append({
                        'Key': obj['Key'],
                        'Size': obj['Size'],
                        'LastModified': obj['LastModified'].isoformat(),
                        'ETag': obj['ETag']
                    })
        
        return objects
    
    def copy_object(self, source_key: str, tags: Dict[str, str] = None) -> bool:
        """Copy single object to destination bucket"""
        try:
            copy_source = {
                'Bucket': self.source_bucket,
                'Key': source_key
            }
            
            tag_string = ''
            if tags:
                tag_string = '&'.join([f'{k}={v}' for k, v in tags.items()])
            
            self.dest_client.copy(
                CopySource=copy_source,
                Bucket=self.dest_bucket,
                Key=source_key,
                ExtraArgs={
                    'Tagging': tag_string,
                    'ServerSideEncryption': 'AES256'
                } if tags else {'ServerSideEncryption': 'AES256'}
            )
            
            return True
        except Exception as e:
            logging.error(f"Error copying {source_key}: {e}")
            return False
    
    def incremental_backup(self, prefix: str = '', retention_days: int = 30) -> Dict:
        """Perform incremental backup of objects modified since last backup"""
        objects = self.list_objects_for_backup(prefix)
        backup_tag = self.create_backup_tag()
        
        results = {
            'total': len(objects),
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
        
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        for obj in objects:
            try:
                # Check if object is already backed up
                try:
                    self.dest_client.head_object(
                        Bucket=self.dest_bucket,
                        Key=obj['Key']
                    )
                    results['skipped'] += 1
                    continue
                except self.dest_client.exceptions.ClientError:
                    pass
                
                # Copy new or modified objects
                tags = {
                    'BackupDate': backup_tag,
                    'OriginalETag': obj['ETag'].strip('"')
                }
                
                if self.copy_object(obj['Key'], tags):
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'key': obj['Key'],
                    'error': str(e)
                })
        
        return results
    
    def cleanup_old_backups(self, prefix: str = '', retention_days: int = 90) -> int:
        """Delete backups older than retention period"""
        deleted_count = 0
        paginator = self.dest_client.get_paginator('list_objects_v2')
        
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        for page in paginator.paginate(Bucket=self.dest_bucket, Prefix=prefix):
            if 'Contents' in page:
                for obj in page['Contents']:
                    try:
                        response = self.dest_client.get_object_tagging(
                            Bucket=self.dest_bucket,
                            Key=obj['Key']
                        )
                        
                        for tag in response['TagSet']:
                            if tag['Key'] == 'BackupDate':
                                backup_date = datetime.strptime(
                                    tag['Value'], '%Y%m%d_%H%M%S'
                                )
                                if backup_date < cutoff_date:
                                    self.dest_client.delete_object(
                                        Bucket=self.dest_bucket,
                                        Key=obj['Key']
                                    )
                                    deleted_count += 1
                                    break
                                
                    except Exception as e:
                        logging.error(f"Error processing {obj['Key']}: {e}")
        
        return deleted_count

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Initialize backup manager
    backup_manager = S3BackupManager(
        source_bucket='production-data',
        dest_bucket='production-backup',
        dest_region='us-west-2'
    )
    
    # Perform incremental backup
    logging.info("Starting incremental backup...")
    results = backup_manager.incremental_backup(prefix='data/', retention_days=30)
    logging.info(f"Backup complete: {results}")
    
    # Cleanup old backups
    logging.info("Cleaning up old backups...")
    deleted = backup_manager.cleanup_old_backups(prefix='data/', retention_days=90)
    logging.info(f"Deleted {deleted} old backup objects")
```

### Example 2: S3 Inventory Report Analysis

```sql
-- Query S3 Inventory data với Athena
-- Create table for inventory data
CREATE EXTERNAL TABLE s3_inventory(
  bucket string,
  key string,
  version_id string,
  is_latest boolean,
  is_delete_marker boolean,
  size bigint,
  last_modified_date timestamp,
  e_tag string,
  storage_class string,
  is_multipart_upload boolean,
  replication_status string,
  encryption_status string
)
PARTITIONED BY (year string, month string, day string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.S3OutputFormat'
LOCATION 's3://inventory-destination-bucket/reports/my-bucket/';

-- Add partitions
ALTER TABLE s3_inventory ADD PARTITION (year='2024', month='01', day='01')
LOCATION 's3://inventory-destination-bucket/reports/my-bucket/year=2024/month=01/day=01/';

-- Analyze storage by storage class
SELECT 
  storage_class,
  COUNT(*) as object_count,
  SUM(size) / 1024 / 1024 as size_mb,
  AVG(size) / 1024 as avg_size_kb
FROM s3_inventory
WHERE year = '2024'
GROUP BY storage_class
ORDER BY SUM(size) DESC;

-- Find large objects
SELECT 
  key,
  size / 1024 / 1024 as size_mb,
  storage_class,
  last_modified_date
FROM s3_inventory
WHERE year = '2024' AND size > 104857600  -- > 100MB
ORDER BY size DESC
LIMIT 20;

-- Find objects not accessed recently
SELECT 
  key,
  size,
  storage_class,
  last_modified_date,
  datediff(current_date, last_modified_date) as days_old
FROM s3_inventory
WHERE year = '2024' 
  AND is_latest = true 
  AND is_delete_marker = false
  AND datediff(current_date, last_modified_date) > 90
ORDER BY days_old DESC
LIMIT 50;
```

## References

### Official Documentation
- [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/)
- [S3 Storage Classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)
- [S3 Lifecycle Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [S3 Replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

### Tools
- [S3 Storage Lens](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-lens.html)
- [S3 Inventory](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-inventory.html)
- [S3 Batch Operations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/batch-ops.html)
- [S3 Object Lambda](https://docs.aws.amazon.com/AmazonS3/latest/userguide/transforming-objects.html)

### Cost Optimization
- [S3 Pricing](https://aws.amazon.com/s3/pricing/)
- [Cost Optimization for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-storage.html)
- [S3 Intelligent-Tiering](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html#s3-intelligent-tiering)
