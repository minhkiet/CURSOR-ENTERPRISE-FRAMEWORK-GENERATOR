---
title: "AWS CloudWatch Observability Platform"
description: "Hướng dẫn toàn diện về CloudWatch Logs, Metrics, Dashboards, Alarms, Insights queries và Embedded Metrics Format"
tags: ["aws", "cloudwatch", "observability", "monitoring", "logging", "metrics", "alarms", "dashboards"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# AWS CloudWatch Observability Platform

## Tổng Quan (Overview)

CloudWatch là unified observability service của AWS, cung cấp monitoring và observability cho applications, infrastructure, và services. CloudWatch thu thập monitoring và operational data dạng logs, metrics, và events, enabling teams to gain visibility across their entire AWS environment và on-premises resources.

Tài liệu này bao gồm comprehensive coverage của CloudWatch components: Logs cho centralized logging, Metrics cho numerical time-series data, Dashboards cho visualization, Alarms cho proactive alerting, CloudWatch Logs Insights cho advanced log analysis, và Embedded Metrics Format cho custom metrics ingestion. Các best practices cho cost optimization, data retention, và integration với third-party tools cũng được covered.

CloudWatch là foundation cho AWS-native observability, cung cấp a single pane of glass cho monitoring infrastructure health, application performance, và operational issues across your entire AWS environment.

## Mục Đích (Purpose)

Mục đích chính của tài liệu này bao gồm:

1. **Metrics Collection**: Collect và analyze numerical data từ AWS services và custom applications
2. **Log Management**: Centralized logging với structured data và efficient querying
3. **Alerting**: Proactive notification khi thresholds are exceeded
4. **Visualization**: Create dashboards cho real-time visibility
5. **Troubleshooting**: Use Logs Insights và traces để diagnose issues
6. **Cost Optimization**: Implement strategies để reduce monitoring costs

## Các Khái Niệm Chính (Key Concepts)

### 1. CloudWatch Metrics

Metrics là fundamental building blocks của CloudWatch. Mỗi metric có:
- **Namespace**: Container for metrics (e.g., AWS/EC2, custom namespace)
- **MetricName**: Name của metric
- **Dimensions**: Attributes cho filtering (e.g., InstanceId, InstanceType)
- **Timestamp**: When the data point was collected
- **Value**: Numerical value
- **Unit**: Unit of measurement (Seconds, Bytes, Percent, etc.)

```bash
# List available metrics for a service
aws cloudwatch list-metrics \
  --namespace AWS/EC2 \
  --query 'Metrics[*].[MetricName,Dimensions]' \
  --output table

# Get specific metric statistics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T12:00:00Z \
  --period 300 \
  --statistics Average,Maximum,Minimum,SampleCount,Sum \
  --output json

# Get metric data points
aws cloudwatch get-metric-data \
  --metric-data-queries '[
    {
      "Id": "cpu",
      "MetricStat": {
        "Metric": {
          "Namespace": "AWS/EC2",
          "MetricName": "CPUUtilization",
          "Dimensions": [{"Name": "InstanceId", "Value": "i-1234567890abcdef0"}]
        },
        "Period": 300,
        "Stat": "Average"
      }
    },
    {
      "Id": "network",
      "MetricStat": {
        "Metric": {
          "Namespace": "AWS/EC2",
          "MetricName": "NetworkIn",
          "Dimensions": [{"Name": "InstanceId", "Value": "i-1234567890abcdef0"}]
        },
        "Period": 300,
        "Stat": "Sum"
      }
    }
  ]' \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T12:00:00Z
```

### 2. CloudWatch Logs

CloudWatch Logs cung cấp centralized logging với features cho ingestion, storage, và querying.

```bash
# Create log group
aws logs create-log-group \
  --log-group-name /aws/ecs/production-web \
  --kms-key-id arn:aws:kms:us-east-1:123456789012:key/1234abcd-1234-1234-1234-123456789012 \
  --retention-in-days 30 \
  --tags Key=Environment,Value=Production Key=Application,Value=WebAPI

# Create log stream
aws logs create-log-stream \
  --log-group-name /aws/ecs/production-web \
  --log-stream-name instance-12345

# Put log events
aws logs put-log-events \
  --log-group-name /aws/ecs/production-web \
  --log-stream-name instance-12345 \
  --log-events '[{"timestamp":1705939200000,"message":"Application started successfully"},{"timestamp":1705939201000,"message":"Connected to database"}]'

# Get log events
aws logs filter-log-events \
  --log-group-name /aws/ecs/production-web \
  --start-time 1705939200000 \
  --filter-pattern "ERROR"

# Describe log groups
aws logs describe-log-groups \
  --log-group-name-prefix /aws/ecs \
  --query 'logGroups[*].[logGroupName,retentionInDays,storedBytes,metricFilterCount]'

# Create metric filter
aws logs put-metric-filter \
  --log-group-name /aws/ecs/production-web \
  --filter-name error-count \
  --filter-pattern '"ERROR"' \
  --metric-transformations '[{"metricName":"ErrorCount","metricNamespace":"MyApplication","metricValue":"1"}]'
```

```json
// CloudWatch Logs subscription filter (for real-time processing)
{
  "destinationArn": "arn:aws:lambda:us-east-1:123456789012:function:log-processor",
  "filterName": "to-lambda",
  "filterPattern": "",
  "logGroupName": "/aws/ecs/production-web",
  "distribution": "Random"
}
```

```bash
# Create subscription filter to Kinesis Data Firehose
aws logs put-subscription-filter \
  --log-group-name /aws/ecs/production-web \
  --filter-name to-firehose \
  --filter-pattern "" \
  --destination-arn arn:aws:firehose:us-east-1:123456789012:deliverystream/centralized-logs \
  --distribution Random

# Create subscription filter to OpenSearch
aws logs put-subscription-filter \
  --log-group-name /aws/ecs/production-web \
  --filter-name to-opensearch \
  --filter-pattern "[timestamp, request_id, level, message]" \
  --destination-arn arn:aws:es:us-east-1:123456789012:domain/logs-domain
```

### 3. CloudWatch Dashboards

```json
{
  "widgets": [
    {
      "type": "metric",
      "x": 0,
      "y": 0,
      "width": 12,
      "height": 6,
      "properties": {
        "title": "EC2 CPU Utilization",
        "annotations": {
          "alarms": ["arn:aws:cloudwatch:us-east-1:123456789012:alarm:HighCPU"]
        },
        "region": "us-east-1",
        "metrics": [
          ["AWS/EC2", "CPUUtilization", {"stat": "Average", "period": 300}],
          [".", "NetworkIn"],
          [".", "NetworkOut"]
        ],
        "period": 300,
        "stat": "Average",
        "statistic": "Average",
        "yAxis": {
          "left": {
            "min": 0,
            "max": 100
          }
        },
        "liveData": true
      }
    },
    {
      "type": "log",
      "x": 12,
      "y": 0,
      "width": 12,
      "height": 6,
      "properties": {
        "title": "Application Errors",
        "region": "us-east-1",
        "query": "fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20",
        "width": 600,
        "height": 400
      }
    },
    {
      "type": "text",
      "x": 0,
      "y": 6,
      "width": 3,
      "height": 3,
      "properties": {
        "markdown": "# Production Environment\n\n- **Region**: us-east-1\n- **Status**: Healthy\n- **Last Update**: " + now() + ""
      }
    }
  ]
}
```

```bash
# Create dashboard
aws cloudwatch put-dashboard \
  --dashboard-name production-overview \
  --dashboard-body file://dashboard.json

# Get dashboard
aws cloudwatch get-dashboard \
  --dashboard-name production-overview

# List dashboards
aws cloudwatch list-dashboards \
  --dashboard-name-prefix production

# Delete dashboard
aws cloudwatch delete-dashboards \
  --dashboard-names production-overview
```

### 4. CloudWatch Alarms

```yaml
# CloudFormation for CloudWatch Alarms
Resources:
  # CPU Alarm
  HighCPUAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: HighCPU
      AlarmDescription: "Alarm when CPU exceeds 80%"
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      DatapointsToAlarm: 2
      Threshold: 80
      ComparisonOperator: GreaterThanThreshold
      TreatMissingData: notBreaching
      Dimensions:
        - Name: InstanceId
          Value: !Ref EC2Instance
      AlarmActions:
        - !Ref SNSTopic
      InsufficientDataActions:
        - !Ref SNSTopic
      OKActions:
        - !Ref SNSTopic

  # Composite Alarm
  ServiceHealthCompositeAlarm:
    Type: AWS::CloudWatch::CompositeAlarm
    Properties:
      AlarmName: ServiceHealth
      AlarmRule: "(HighCPU AND HighMemory) OR DatabaseUnavailable"
      ActionsEnabled: true
      AlarmActions:
        - !Ref SNSTopic
      InsufficientDataActions:
        - !Ref SNSTopic
      OKActions:
        - !Ref SNSTopic

  # Anomaly Detection Alarm
  AnomalyDetectionAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: TrafficAnomaly
      AlarmDescription: "Alarm when traffic deviates from normal pattern"
      Metrics:
        - Id: totalRequests
          MetricStat:
            Metric:
              Namespace: MyApplication
              MetricName: RequestCount
              Dimensions:
                - Name: Service
                  Value: API
            Period: 300
            Stat: Sum
          ReturnData: false
        - Id: anomalyBand
          Expression: "ANOMALY_DETECTION_BAND(totalRequests, 2)"
          ReturnData: false
        - Id: isAnomaly
          Expression: "IF(totalRequests > anomalyBand.UpperBound OR totalRequests < anomalyBand.LowerBound, 1, 0)"
          ReturnData: true
      ThresholdMetricId: isAnomaly
      EvaluationPeriods: 2
      EvaluationRange: "0, 1"
```

```bash
# Create alarm
aws cloudwatch put-metric-alarm \
  --alarm-name high-cpu-alarm \
  --alarm-description "Alarm when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --datapoints-to-alarm 2 \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:alerts \
  --ok-actions arn:aws:sns:us-east-1:123456789012:alerts \
  --treat-missing-data notBreaching

# Set alarm state
aws cloudwatch set-alarm-state \
  --alarm-name high-cpu-alarm \
  --state-value ALARM \
  --state-reason "Testing alarm state"

# Describe alarms
aws cloudwatch describe-alarms \
  --alarm-names high-cpu-alarm memory-alarm disk-alarm

# Get alarm history
aws cloudwatch describe-alarm-history \
  --alarm-name high-cpu-alarm \
  --history-item-type StateUpdate \
  --start-date 2024-01-01T00:00:00Z \
  --end-date 2024-01-31T23:59:59Z
```

### 5. CloudWatch Logs Insights

```sql
-- Basic query patterns

-- Error analysis
fields @timestamp, @message, @level, @logger
| filter @message like /ERROR/
| sort @timestamp desc
| limit 50

-- Performance metrics extraction
fields @timestamp, latency_ms, status_code, request_path
| filter status_code >= 500
| stats count() as error_count, avg(latency_ms) as avg_latency by request_path
| sort error_count desc

-- Request rate by endpoint
fields @timestamp, request_path, request_method
| parse request_path as @path
| stats count() as request_count by bin(5m), request_path
| sort request_count desc

-- User activity tracking
fields user_id, action, @timestamp
| filter user_id is not null
| stats count() as actions by user_id, action
| sort actions desc
| limit 20

-- Database query analysis
fields @timestamp, query, duration_ms
| filter query like /SELECT/
| stats avg(duration_ms) as avg_duration, max(duration_ms) as max_duration, count() as query_count
| sort avg_duration desc

-- Security analysis
fields @timestamp, source_ip, request_path, user_agent
| filter request_path like /admin/
| stats count() as attempts by source_ip
| filter attempts > 10
| sort attempts desc

-- API latency percentiles
fields @timestamp, latency_ms
| stats percentile(latency_ms, 50) as p50,
        percentile(latency_ms, 90) as p90,
        percentile(latency_ms, 99) as p99
| sort @timestamp desc

-- Complex pattern matching
fields @timestamp, @message
| filter @message like /timeout/i or @message like /connection refused/i
| parse @message as /(?<error_type>\w+):\s*(?<error_msg>.*)/
| stats count() by error_type, error_msg
| sort count() desc

-- Time series with aggregation
fields @timestamp, metric_value
| bin auto
| stats avg(metric_value) as avg_value, sum(metric_value) as total_value
| sort @timestamp asc
```

```bash
# Run Insights query
aws logs start-query \
  --log-group-name /aws/ecs/production-web \
  --start-time 1705939200 \
  --end-time 1706025600 \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20'

# Get query results
aws logs get-query-results \
  --query-id abcdef12-3456-7890-abcd-ef1234567890

# Run query with multiple log groups
aws logs start-query \
  --log-group-name /aws/ecs/production-web \
  --log-group-name /aws/lambda/production-function \
  --start-time 1705939200 \
  --end-time 1706025600 \
  --query-string 'fields @log, @message | filter @message like /exception/i'
```

### 6. Embedded Metrics Format

EMF cho phép embed metrics directly in log events, simplifying custom metrics collection.

```python
# Python example with EMF
import json
import logging
from datetime import datetime

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """Example Lambda function with embedded metrics"""
    
    # Process the event
    start_time = datetime.now()
    result = process_data(event)
    duration = (datetime.now() - start_time).total_seconds() * 1000
    
    # Create embedded metrics
    logger.info(
        json.dumps({
            "_aws": {
                "Timestamp": int(datetime.now().timestamp() * 1000),
                "CloudWatchMetrics": [
                    {
                        "Namespace": "MyApplication",
                        "Dimensions": [["Service", "Environment"]],
                        "Metrics": [
                            {"Name": "RequestCount", "Unit": "Count"},
                            {"Name": "SuccessCount", "Unit": "Count"},
                            {"Name": "ErrorCount", "Unit": "Count"},
                            {"Name": "Duration", "Unit": "Milliseconds"},
                            {"Name": "MemoryUsed", "Unit": "Megabytes"}
                        ]
                    }
                ]
            },
            "Service": "OrderProcessor",
            "Environment": "production",
            "RequestCount": 1,
            "SuccessCount": 1 if result["status"] == "success" else 0,
            "ErrorCount": 1 if result["status"] == "error" else 0,
            "Duration": duration,
            "MemoryUsed": int(context.memory_limit_in_mb * 0.6),  # Example
            "OrderId": result.get("order_id"),
            "UserId": result.get("user_id"),
            "Message": f"Processed order {result.get('order_id')}"
        })
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }

def process_data(event):
    """Process order data"""
    try:
        # Simulated processing
        return {
            "status": "success",
            "order_id": event.get("order_id", "ORD-001"),
            "user_id": event.get("user_id", "USR-001")
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
```

```javascript
// Node.js example with EMF
const { Logger } = require('@aws-lambda-powertools/logger');
const { MetricsUnit, Metrics } = require('@aws-lambda-powertools/metrics');

const logger = new Logger();
const metrics = new Metrics();

exports.handler = async (event) => {
    const startTime = Date.now();
    
    try {
        // Add metrics
        metrics.addMetric('RequestCount', MetricsUnit.Count, 1);
        metrics.addDimension('Service', 'OrderProcessor');
        metrics.addDimension('Environment', process.env.ENVIRONMENT || 'production');
        
        // Process order
        const result = await processOrder(event);
        
        // Add success metrics
        metrics.addMetric('SuccessCount', MetricsUnit.Count, 1);
        metrics.addMetric('Duration', MetricsUnit.Milliseconds, Date.now() - startTime);
        
        // Log with embedded metrics
        logger.info('Order processed successfully', {
            orderId: result.orderId,
            userId: result.userId
        });
        
        // Flush metrics to CloudWatch
        metrics.publishStoredMetrics();
        
        return {
            statusCode: 200,
            body: JSON.stringify(result)
        };
    } catch (error) {
        // Add error metrics
        metrics.addMetric('ErrorCount', MetricsUnit.Count, 1);
        metrics.addMetric('Duration', MetricsUnit.Milliseconds, Date.now() - startTime);
        
        logger.error('Order processing failed', {
            error: error.message
        });
        
        metrics.publishStoredMetrics();
        
        throw error;
    }
};
```

## Best Practices

### 1. Cost Optimization

```yaml
# CloudWatch cost optimization policies
Resources:
  # High-resolution metric alarm (1-minute granularity - higher cost)
  OneMinuteAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: urgent-alarm
      MetricName: ErrorRate
      Namespace: MyApplication
      Statistic: Average
      Period: 60  # 1-minute resolution
      Threshold: 5
      ComparisonOperator: GreaterThanThreshold
      EvaluationPeriods: 1

  # Standard resolution alarm (5-minute granularity - lower cost)
  StandardAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: standard-alarm
      MetricName: ErrorRate
      Namespace: MyApplication
      Statistic: Average
      Period: 300  # 5-minute resolution
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      EvaluationPeriods: 2

  # Retention policies for log groups
  ApplicationLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/ecs/production-app
      RetentionInDays: 14  # Reduced from 30
      MetricFilterCount: 1
      KmsKeyId: !Ref LogsKmsKey

  HighVolumeLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/ecs/debug-logs
      RetentionInDays: 3  # Short retention for debug logs
      KmsKeyId: !Ref LogsKmsKey
```

```bash
# Estimate costs with Cost Explorer API
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics "BlendedCost" "UnblendedCost" "UsageQuantity" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{"Dimensions": {"Key": "SERVICE", "Values": ["Amazon CloudWatch"]}}'

# List log groups with storage
aws logs describe-log-groups \
  --log-group-name-prefix /aws \
  --query 'logGroups[*].{Name:logGroupName,Retention:retentionInDays,Storage:storedBytes,Metrics:metricFilterCount}'

# Estimate log storage cost
# Example: 100GB stored at $0.03/GB = $3/month for storage alone
```

### 2. Unified CloudWatch Agent Configuration

```json
{
  "agent": {
    "omem_stats": 0,
    "debug": false,
    "file_path_config": "/etc/awslogs/etc/awslogs-agent.conf"
  },
  "logs": {
    "force_flush_interval": 5,
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/nginx/access.log",
            "log_group_name": "/ec2/nginx/access",
            "log_stream_name": "{instance_id}/nginx/access",
            "timestamp_format": "%Y-%m-%dT%H:%M:%S%z",
            "encoding": "utf-8",
            "multi_line_start_pattern": "{timestamp_format}",
            "filters": [
              {
                "filter_type": "regex",
                "expression": "^(?<status_code>\\d{3}) (?<latency>\\d+) (?<size>\\d+)$"
              }
            ]
          },
          {
            "file_path": "/var/log/nginx/error.log",
            "log_group_name": "/ec2/nginx/error",
            "log_stream_name": "{instance_id}/nginx/error",
            "timestamp_format": "%Y-%m-%d %H:%M:%S",
            "encoding": "utf-8",
            "filter_rules": [
              {
                "type": "select",
                "expression": "error|ERROR|Error"
              }
            ]
          },
          {
            "file_path": "/var/log/application.log",
            "log_group_name": "/ec2/application",
            "log_stream_name": "{instance_id}/application",
            "timestamp_format": "%Y-%m-%d %H:%M:%S.%f",
            "encoding": "utf-8",
            "line_pattern": "^\\d{4}-\\d{2}-\\d{2}",
            "datetime_format": "%Y-%m-%d %H:%M:%S.%f"
          }
        ]
      },
      "windows_events": {
        "collect_list": [
          {
            "event_name": "System",
            "log_group_name": "/windows/eventlog/System",
            "event_level": "INFORMATION,WARNING,ERROR",
            "log_stream_name": "{hostname}/System",
            "filter_rules": [
              {
                "type": "select",
                "event_ids": "1000,1001,1002,6005,6006"
              }
            ]
          },
          {
            "event_name": "Security",
            "log_group_name": "/windows/eventlog/Security",
            "event_level": "INFORMATION,AUDIT_SUCCESS,AUDIT_FAILURE",
            "log_stream_name": "{hostname}/Security"
          }
        ]
      }
    }
  },
  "metrics": {
    "metrics_collected": {
      "cpu": {
        "measurement": [
          "cpu_usage_idle",
          "cpu_usage_user",
          "cpu_usage_system"
        ],
        "metrics_collection_interval": 60,
        "resources": ["*"],
        "drop_metrics": ["cpu_usage_guest", "cpu_usage_guest_nice"]
      },
      "disk": {
        "measurement": [
          "disk_used",
          "disk_free",
          "inodes_free"
        ],
        "metrics_collection_interval": 60,
        "resources": ["*"],
        "drop_metrics": ["disk_inodes_free"]
      },
      "mem": {
        "measurement": [
          "mem_used",
          "mem_available",
          "mem_total"
        ],
        "metrics_collection_interval": 60
      },
      "netstat": {
        "measurement": [
          "netstat_tcp_established",
          "netstat_tcp_time_wait"
        ],
        "metrics_collection_interval": 60
      },
      "processes": {
        "measurement": [
          "processes_running",
          "processes_sleeping",
          "process_total"
        ],
        "metrics_collection_interval": 60
      }
    },
    "append_dimensions": {
      "ImageId": "${aws:ImageId}",
      "InstanceId": "${aws:InstanceId}",
      "InstanceType": "${aws:InstanceType}",
      "AutoScalingGroupName": "${aws:AutoScalingGroupName}"
    },
    "aggregation_dimensions": [
      [{"AutoScalingGroupName": "RollupAutoScalingGroupName"}],
      [{"InstanceId": "RollupInstanceId"}],
      []
    ]
  }
}
```

```bash
# Install CloudWatch agent
# For Amazon Linux 2 / RHEL / CentOS
sudo yum install -y amazon-cloudwatch-agent

# For Ubuntu / Debian
sudo apt-get install -y amazon-cloudwatch-agent

# Start agent with configuration file
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json \
  -s

# Check agent status
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -m ec2 \
  -a status

# Validate configuration
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-validate-config \
  -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json \
  -o /var/log/amazon-cloudwatch-agent-validate.log
```

### 3. Contributor Insights

```yaml
# Contributor Insights for DNS analysis
Resources:
  DNSAccessPatterns:
    Type: AWS::CloudWatch::InsightRule
    Properties:
      InsightRuleName: dns-access-patterns
      InsightRuleState: ENABLED
      InsightRuleDefinition:
        Schema: >-
          {
            "aggregateBy": {
              "logGroup": false
            },
            "Contribution": {
              "datapoints": 10,
              "filters": [
                {
                  "match": "*.amazonaws.com",
                  "inReverse": false,
                  "property": "request_path"
                }
              ],
              "keys": [
                "request_path",
                "source_ip"
              ]
            },
            "Limit": 20,
            "LogGroupNames": [
              "/aws/eks/production"
            ],
            "LogFormat": "JSON",
            "Query": "fields @timestamp, request_path, source_ip | sort @timestamp desc"
```

## Common Patterns

### Pattern 1: Container Monitoring với Container Insights

```yaml
# CloudFormation for Container Insights
Resources:
  ContainerInsightsLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/containerinsights/production/performance
      RetentionInDays: 7
      KmsKeyId: !Ref LogsKmsKey

  ContainerInsightsConfig:
    Type: AWS::EKS::Cluster
    Properties:
      Name: production-cluster
      # Container Insights is enabled via cluster configuration
      Logging:
        ClusterLogging:
          EnabledTypes:
            - EKS - API Server
            - EKS - Audit
```

```bash
# Enable Container Insights on EKS cluster
aws eks update-cluster-config \
  --name production-cluster \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'

# Install Container Insights add-on
aws eks create-addon \
  --cluster-name production-cluster \
  --addon-name amazon-cloudwatch-observability \
  --addon-version v1.4.0 \
  --configuration-values '{"enableContainerInsights":true}'

# Or via kubectl
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/main/k8s-deployment-manifest.yaml

# Query Container Insights metrics
aws cloudwatch get-metric-data \
  --metric-data-queries '[
    {
      "Id": "cpu",
      "MetricStat": {
        "Metric": {
          "Namespace": "ContainerInsights",
          "MetricName": "pod_cpu_utilization",
          "Dimensions": [{"Name": "ClusterName", "Value": "production-cluster"}, {"Name": "NodeName", "Value": "*"}]
        },
        "Period": 60,
        "Stat": "Average"
      }
    },
    {
      "Id": "memory",
      "MetricStat": {
        "Metric": {
          "Namespace": "ContainerInsights",
          "MetricName": "pod_memory_working_set",
          "Dimensions": [{"Name": "ClusterName", "Value": "production-cluster"}]
        },
        "Period": 60,
        "Stat": "Average"
      }
    }
  ]' \
  --start-time 1705939200 \
  --end-time 1706025600
```

### Pattern 2: Distributed Tracing với X-Ray Integration

```yaml
# CloudFormation for X-Ray integration
Resources:
  XRayRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole

  XRayPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: xray-policy
      Roles:
        - !Ref XRayRole
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - xray:PutTraceSegments
              - xray:PutTelemetryRecords
              - xray:GetSamplingRules
              - xray:GetSamplingTargets
              - xray:GetSamplingStatisticSummaries
            Resource: "*"

  # Lambda with X-Ray
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: production-api
      Runtime: python3.11
      Handler: lambda_function.handler
      Role: !GetAtt LambdaExecutionRole.Arn
      TracingConfig:
        Mode: Active
      Environment:
        Variables:
          AWS_XRAY_SDK_ENABLED: "true"
```

```python
# Python Lambda with X-Ray tracing
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask import XRayMiddleware
from aws_xray_sdk.ext.boto3 import patch

# Patch boto3 for automatic subsegment creation
patch(['boto3', 'botocore'])

# Add custom annotations and metadata
@xray_recorder.capture('process_order')
def process_order(order_data):
    with xray_recorder.capture('validate_order') as validate_segment:
        validate_order(order_data)
        validate_segment.put_annotation('customer_id', order_data['customer_id'])
    
    with xray_recorder.capture('persist_order') as persist_segment:
        result = save_to_database(order_data)
        persist_segment.put_metadata('order_id', result['id'])
    
    return result

# Custom subsegment for business logic timing
def get_recommendations(customer_id):
    with xray_recorder.in_subsegment('recommendations'):
        recommendations = fetch_recommendations(customer_id)
        return recommendations
```

## Troubleshooting

### Common Issues và Solutions

**1. Missing Metrics**

```bash
# Check if CloudWatch agent is running
systemctl status amazon-cloudwatch-agent
ps aux | grep amazon-cloudwatch-agent

# Check agent logs
tail -f /var/log/amazon-cloudwatch-agent/amazon-cloudwatch-agent.log

# Verify configuration
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a status -m ec2

# Check metrics namespace
aws cloudwatch list-metrics \
  --namespace CWAgent \
  --query 'Metrics[*].[MetricName,Dimensions]'

# Verify permissions
aws lambda invoke \
  --function-name amazon-cloudwatch-observability \
  --payload '{}' \
  response.json
```

**2. Log Ingestion Issues**

```bash
# Check for ingestion throttling
aws logs describe-log-groups \
  --log-group-name-prefix /aws \
  --query 'logGroups[*].{Name:logGroupName,StoredBytes:storedBytes,BytesAccepted:bytesAccepted}'

# Verify subscription filter
aws logs describe-subscription-filters \
  --log-group-name /aws/ecs/production-web

# Check for permission issues
aws logs test-metric-filter \
  --log-group-name /aws/ecs/production-web \
  --filter-pattern "ERROR"

# Check log events for errors
aws logs filter-log-events \
  --log-group-name /aws/ecs/production-web \
  --filter-pattern "ERROR" \
  --start-time 1705939200000 \
  --end-time 1706025600000
```

**3. Alarm Not Triggering**

```bash
# Check alarm state
aws cloudwatch describe-alarms \
  --alarm-names high-cpu-alarm \
  --query 'MetricAlarms[0].[AlarmName,StateValue,StateReason,MetricName,Threshold,Period,EvaluationPeriods]'

# Check if data is being published
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 1705939200 \
  --end-time 1706025600 \
  --period 300 \
  --statistics Average

# Check alarm history
aws cloudwatch describe-alarm-history \
  --alarm-name high-cpu-alarm \
  --history-item-type StateUpdate

# Verify SNS permissions
aws sns get-topic-attributes \
  --topic-arn arn:aws:sns:us-east-1:123456789012:alerts
```

**4. High Cost Investigation**

```bash
# Get detailed cost breakdown
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity DAILY \
  --metrics "BlendedCost" "UsageQuantity" \
  --group-by Type=DIMENSION,Key=OPERATION \
  --filter '{"Dimensions": {"Key": "SERVICE", "Values": ["Amazon CloudWatch"]}}'

# Get usage by log group
aws logs describe-log-groups \
  --log-group-name-prefix /aws \
  --query 'logGroups[*].{Name:logGroupName,StoredBytes:storedBytes,Retention:retentionInDays,Metrics:metricFilterCount}'

# Analyze metric frequency
aws cloudwatch list-metrics \
  --namespace MyApplication \
  --query 'length(Metrics[])'

# Check for custom metrics with high cardinality
aws cloudwatch list-metrics \
  --namespace MyApplication \
  --dimensions '[]'
```

## Examples

### Example 1: Production Monitoring Setup

```yaml
# Complete CloudWatch monitoring infrastructure
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  # KMS Key for log encryption
  LogsKmsKey:
    Type: AWS::KMS::Key
    Properties:
      Description: KMS key for CloudWatch Logs encryption
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: kms:*
            Resource: '*'
          - Sid: Allow CloudWatch to use key
            Effect: Allow
            Principal:
              Service: logs.amazonaws.com
            Action:
              - kms:Encrypt
              - kms:Decrypt
              - kms:GenerateDataKey
              - kms:DescribeKey
            Resource: '*'

  # SNS Topic for alarms
  AlarmSNSTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: production-alarms
      DisplayName: Production Alarms
      KmsMasterKeyId: !Ref LogsKmsKey

  # Email subscription
  AlarmEmailSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      TopicArn: !Ref AlarmSNSTopic
      Endpoint: ops-team@example.com
      Protocol: email

  # Log groups
  ApplicationLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/production/application
      RetentionInDays: 30
      KmsKeyId: !Ref LogsKmsKey
      Tags:
        - Key: Environment
          Value: Production
        - Key: Application
          Value: ProductionAPI

  LambdaLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/lambda/${AWS::StackName}'
      RetentionInDays: 14
      KmsKeyId: !Ref LogsKmsKey

  # Dashboard
  MonitoringDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: !Sub '${AWS::StackName}-dashboard'
      DashboardBody: !Sub |
        {
          "widgets": [
            {
              "type": "metric",
              "x": 0,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "title": "API Latency",
                "annotations": {
                  "alarms": ["${HighLatencyAlarm.Arn}"]
                },
                "region": "${AWS::Region}",
                "metrics": [
                  ["MyApplication", "Latency", {"stat": "p50"}],
                  [".", "Latency", {"stat": "p90"}],
                  [".", "Latency", {"stat": "p99"}]
                ],
                "period": 60,
                "stat": "Average"
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "title": "Error Rate",
                "annotations": {
                  "alarms": ["${HighErrorRateAlarm.Arn}"]
                },
                "region": "${AWS::Region}",
                "metrics": [
                  ["MyApplication", "ErrorRate", {"stat": "Average"}]
                ],
                "period": 60,
                "stat": "Average"
              }
            },
            {
              "type": "log",
              "x": 0,
              "y": 6,
              "width": 24,
              "height": 6,
              "properties": {
                "title": "Recent Errors",
                "region": "${AWS::Region}",
                "query": "fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20"
              }
            }
          ]
        }

  # Alarms
  HighCPUAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${AWS::StackName}-high-cpu'
      AlarmDescription: Alarm when CPU exceeds 80%
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 80
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: InstanceId
          Value: !Ref EC2Instance
      AlarmActions:
        - !Ref AlarmSNSTopic
      OKActions:
        - !Ref AlarmSNSTopic

  HighLatencyAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${AWS::StackName}-high-latency'
      AlarmDescription: Alarm when p99 latency exceeds 500ms
      MetricName: Latency
      Namespace: MyApplication
      Statistic: Percentile
      ExtendedStatistic: p99
      Period: 60
      EvaluationPeriods: 3
      Threshold: 500
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref AlarmSNSTopic
      OKActions:
        - !Ref AlarmSNSTopic

  HighErrorRateAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${AWS::StackName}-high-error-rate'
      AlarmDescription: Alarm when error rate exceeds 1%
      MetricName: ErrorRate
      Namespace: MyApplication
      Statistic: Average
      Period: 60
      EvaluationPeriods: 3
      Threshold: 1
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref AlarmSNSTopic
      OKActions:
        - !Ref AlarmSNSTopic

  # Composite alarm
  ServiceHealthAlarm:
    Type: AWS::CloudWatch::CompositeAlarm
    Properties:
      AlarmName: !Sub '${AWS::StackName}-service-health'
      AlarmDescription: Combined service health alarm
      AlarmRule: "(NOT ${HighLatencyAlarm.Arn}) AND (NOT ${HighErrorRateAlarm.Arn})"
      ActionsEnabled: true
      AlarmActions:
        - !Ref AlarmSNSTopic
      OKActions:
        - !Ref AlarmSNSTopic
```

## References

### Official Documentation
- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [CloudWatch Logs Documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/)
- [CloudWatch Metrics Documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/)
- [CloudWatch Dashboards](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html)
- [CloudWatch Embedded Metrics Format](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html)
- [CloudWatch Agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)

### Tools và Integrations
- [CloudWatch Observability Access Manager](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/query-with-OAM.html)
- [CloudWatch Contributor Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContributorInsights.html)
- [CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Signals.html)
- [CloudWatch Lambda Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights.html)
- [Container Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html)

### Best Practices
- [CloudWatch Best Practices](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_best_practices.html)
- [Monitoring Best Practices](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-metrics-insights-best-practices.html)
- [Logs Insights Query Best Practices](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/cloudwatch-insights-best-practices.html)
