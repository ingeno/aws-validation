# Ingeno Monitoring and Observability Framework

## Executive Summary

This document establishes standardized procedures for implementing comprehensive monitoring, alerting, and logging across all Ingeno cloud workloads using an infrastructure-as-code approach with AWS CDK. It provides cloud developers with clear guidelines for creating CloudWatch dashboards, defining key performance metrics, configuring operational alerts, and implementing structured application logging to ensure optimal system performance and rapid issue detection.

## Monitoring Dashboard Standards

### Dashboard Architecture

All production workloads must implement a standardized dashboard architecture consisting of:

**Purpose:** Comprehensive technical monitoring for operations teams  
**Components Required:**
- **ECS Service Metrics:** CPU utilization, memory usage, running/pending task counts
- **Database Performance:** RDS/DynamoDB metrics including connections, latency, and throughput
- **Load Balancer Health:** Request counts, response times, HTTP status distributions
- **Application Logs:** Error tracking and performance logging via CloudWatch Logs Insights
- **Service-Specific Metrics:** Lambda functions, Timestream, IoT services as applicable

### Dashboard Naming Convention

Use the following standardized naming pattern:
```
{customer}-{environment}-{dashboard-type}
Examples:
- acimtl-prod-technical-dashboard
- valmetal-prod-executive-dashboard
```

### Widget Configuration Standards

#### Metric Widget Standards
- **Time Range:** Default to 1-hour view with 5-minute granularity
- **Period:** 300 seconds (5 minutes) for standard metrics
- **Statistics:** Use appropriate statistics (Average, Sum, Maximum) based on metric type
- **Region Specification:** Always specify region parameter in metric definitions

#### Log Widget Standards
- **Query Optimization:** Limit results to 50-100 entries for performance
- **Time Window:** Default to last 1 hour for error logs
- **Structured Queries:** Use CloudWatch Logs Insights syntax for complex filtering

## Key Performance Metrics Framework

### Core Infrastructure Metrics

#### ECS Services (Required for all ECS workloads)
```json
{
  "metrics": [
    ["AWS/ECS", "CPUUtilization", "ServiceName", "{service-name}", "ClusterName", "{cluster-name}"],
    [".", "MemoryUtilization", ".", ".", ".", "."],
    [".", "RunningTaskCount", ".", ".", ".", "."],
    [".", "PendingTaskCount", ".", ".", ".", "."]
  ],
  "period": 300,
  "stat": "Average"
}
```

#### RDS Database Monitoring (Required for all RDS instances)
```json
{
  "metrics": [
    ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", "{db-instance-name}"],
    [".", "DatabaseConnections", ".", "."],
    [".", "FreeableMemory", ".", "."],
    [".", "ReadLatency", ".", "."],
    [".", "WriteLatency", ".", "."]
  ],
  "period": 300,
  "stat": "Average"
}
```

#### Application Load Balancer (Required for all ALB configurations)
```json
{
  "metrics": [
    ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", "{load-balancer-arn}", {"stat": "Sum"}],
    [".", "TargetResponseTime", ".", "."],
    [".", "HTTPCode_Target_2XX_Count", ".", ".", {"stat": "Sum"}],
    [".", "HTTPCode_Target_4XX_Count", ".", ".", {"stat": "Sum"}],
    [".", "HTTPCode_Target_5XX_Count", ".", ".", {"stat": "Sum"}]
  ],
  "period": 300
}
```

### Service-Specific Metrics

#### DynamoDB Monitoring (For DynamoDB workloads)
```json
{
  "metrics": [
    ["AWS/DynamoDB", "ConsumedReadCapacityUnits", "TableName", "{table-name}"],
    [".", "ConsumedWriteCapacityUnits", ".", "."],
    [".", "SuccessfulRequestLatency", ".", ".", "Operation", "GetItem"],
    [".", "ThrottledRequests", ".", "."]
  ],
  "period": 300,
  "stat": "Average"
}
```

#### Lambda Function Monitoring (For serverless workloads)
```json
{
  "metrics": [
    ["AWS/Lambda", "Invocations", "FunctionName", "{function-name}"],
    [".", "Duration", ".", "."],
    [".", "Errors", ".", "."],
    [".", "Throttles", ".", "."]
  ],
  "period": 300,
  "stat": "Average"
}
```

#### Timestream Monitoring (For IoT/time-series workloads)
```json
{
  "metrics": [
    ["AWS/Timestream", "IngestedRecords", "DatabaseName", "{database-name}", "TableName", "{table-name}"],
    [".", "ActiveMagneticStorePartitions", ".", ".", ".", "."],
    [".", "MagneticStoreRejectedRecords", ".", ".", ".", "."],
    [".", "MemoryStoreRejectedRecords", ".", ".", ".", "."]
  ],
  "period": 300,
  "stat": "Sum"
}
```

## Alert Configuration Guidelines

### Alert Threshold Standards

#### Critical Alerts (Immediate Response)
- **ECS CPU Utilization:** >85%
- **ECS Memory Utilization:** >90%
- **RDS CPU Utilization:** >85%
- **Application 5XX Error Rate:** >5%
- **Database Connection Exhaustion:** >80% of max connections
- **Service Health Check Failures:** Any failure

#### Warning Alerts (15-minute Response)
- **ECS CPU Utilization:** >70%
- **ECS Memory Utilization:** >75%
- **RDS CPU Utilization:** >70%
- **Application 4XX Error Rate:** >10%
- **Database Query Latency:** >200ms average
- **Lambda Error Rate:** >5%

#### Performance Alerts (Hourly Review)
- **Application Response Time:** >500ms
- **Database Read/Write Latency:** >100ms
- **DynamoDB Throttling Events:** Any occurrence
- **Timestream Ingestion Failures:** Any failure

### Alert Configuration Procedures

#### 1. Infrastructure as Code Requirement
All CloudWatch alarms must be defined as code using AWS CDK to ensure consistency, version control, and reproducible deployments across environments.

#### 2. Required Alert Categories

**Critical Alerts (Immediate Response Required)**
- **ECS CPU Utilization:** Threshold >85% for 2 evaluation periods
- **ECS Memory Utilization:** Threshold >90% for 2 evaluation periods  
- **RDS CPU Utilization:** Threshold >85% for 2 evaluation periods
- **Application 5XX Error Rate:** Threshold >5% for 2 evaluation periods
- **Database Connection Exhaustion:** Threshold >80% of maximum connections
- **Service Health Check Failures:** Any failure triggers immediate alert
- **Lambda Function Errors:** Threshold >5% error rate for 2 evaluation periods

**Warning Alerts (15-minute Response Window)**
- **ECS CPU Utilization:** Threshold >70% for 3 evaluation periods
- **ECS Memory Utilization:** Threshold >75% for 3 evaluation periods
- **RDS CPU Utilization:** Threshold >70% for 3 evaluation periods
- **Application 4XX Error Rate:** Threshold >10% for 3 evaluation periods
- **Database Query Latency:** Threshold >200ms average for 3 evaluation periods
- **DynamoDB Throttling Events:** Any throttling occurrence
- **Lambda Function Duration:** Threshold >80% of timeout limit

**Performance Alerts (Hourly Review)**
- **Application Response Time:** Threshold >500ms average for 5 evaluation periods
- **Database Read/Write Latency:** Threshold >100ms average for 5 evaluation periods
- **Timestream Ingestion Failures:** Any ingestion failure
- **Load Balancer Target Response Time:** Threshold >1000ms for 5 evaluation periods

#### 3. Alert Configuration Requirements

**SNS Integration**
- Configure separate SNS topics for each alert severity level (Critical, Warning, Performance)
- Implement appropriate notification channels (email, Slack, PagerDuty) based on severity
- Establish escalation procedures for unacknowledged critical alerts

**Alert Metadata**
- All alarms must include descriptive names following pattern: `{service}-{metric}-{severity}`
- Include comprehensive alarm descriptions explaining the condition and required response
- Configure appropriate evaluation periods and comparison operators based on alert type
- Implement proper alarm actions for each severity level

## CloudWatch Logs Implementation

### Logging Architecture Standards

#### 1. Log Group Naming Convention
```
/aws/{service}/{environment}/{application}
Examples:
/aws/ecs/prod/acimtl-api
/aws/lambda/prod/valmetal-iot-processor
```

#### 2. Structured Logging Requirements

All applications must implement structured JSON logging with the following mandatory fields:

```json
{
  "@timestamp": "2024-01-01T12:00:00.000Z",
  "@level": "INFO|WARN|ERROR|DEBUG",
  "@message": "Human readable message",
  "@requestId": "unique-request-identifier",
  "@service": "service-name",
  "@version": "application-version",
  "additionalFields": {}
}
```

#### 3. Log Retention Policies
- **Production Logs:** 30 days retention minimum
- **Development Logs:** 7 days retention
- **Security Logs:** 90 days retention
- **Audit Logs:** 1 year retention

### Application Logging Best Practices

#### 1. Error Logging Standards
```json
{
  "@timestamp": "2024-01-01T12:00:00.000Z",
  "@level": "ERROR",
  "@message": "Database connection failed",
  "@requestId": "req-123456",
  "@service": "api-service",
  "@error": {
    "type": "DatabaseConnectionError",
    "message": "Connection timeout after 30s",
    "stack": "...",
    "code": "DB_TIMEOUT"
  },
  "@context": {
    "userId": "user-123",
    "endpoint": "/api/users",
    "method": "GET"
  }
}
```

#### 2. Performance Logging Standards
```json
{
  "@timestamp": "2024-01-01T12:00:00.000Z",
  "@level": "INFO",
  "@message": "Request completed",
  "@requestId": "req-123456",
  "@service": "api-service",
  "@performance": {
    "duration": 150,
    "endpoint": "/api/users",
    "method": "GET",
    "statusCode": 200,
    "responseSize": 1024
  }
}
```

#### 3. Security Event Logging
```json
{
  "@timestamp": "2024-01-01T12:00:00.000Z",
  "@level": "WARN",
  "@message": "Authentication failed",
  "@requestId": "req-123456",
  "@service": "auth-service",
  "@security": {
    "event": "authentication_failed",
    "userId": "user-123",
    "ipAddress": "192.168.1.1",
    "userAgent": "...",
    "reason": "invalid_credentials"
  }
}
```

### CloudWatch Logs Insights Queries

#### Standard Error Query
```sql
SOURCE '{loggroupname}'
| fields @timestamp, @message, @requestId
| filter @level = "ERROR"
| sort @timestamp desc
| limit 100
```

#### Performance Analysis Query
```sql
SOURCE '{loggroupname}'
| fields @timestamp, @performance.duration, @performance.endpoint
| filter @performance.duration > 1000
| stats avg(@performance.duration) by @performance.endpoint
| sort avg desc
```

#### Security Events Query
```sql
SOURCE '{loggroupname}'
| fields @timestamp, @security.event, @security.userId, @security.ipAddress
| filter @security.event = "authentication_failed"
| stats count() by @security.ipAddress
| sort count desc
```

## Implementation Procedures

### Infrastructure as Code Requirements

**All monitoring components must be defined as code using AWS CDK to ensure consistency, reproducibility, and proper version control.**

### 1. Dashboard Implementation

#### Dashboard Definition Requirements
- All dashboards must be defined using CDK Dashboard constructs
- Follow standardized naming conventions: `{customer}-{environment}-technical-dashboard`
- Include all required widget types: ECS metrics, database performance, application logs, service-specific metrics
- Configure appropriate time ranges and granularity (5-minute periods for standard metrics)
- Integrate log widgets using CloudWatch Logs Insights queries for error tracking

#### Dashboard Deployment
- Deploy dashboards as part of CDK stack deployment process
- Ensure dashboards are versioned with application code
- Include dashboard definitions in CI/CD pipeline deployment

### 2. Alert Implementation

#### Alert Definition Requirements
- Define all CloudWatch alarms using CDK constructs
- Implement the three-tier alert system (Critical, Warning, Performance) as specified
- Configure SNS topics for each alert severity level
- Set appropriate evaluation periods and thresholds per alert category requirements
- Include proper alarm metadata and descriptions

#### Alert Integration
- Configure notification channels (email, Slack, PagerDuty) based on alert severity
- Implement escalation procedures for unacknowledged critical alerts
- Ensure alerts are deployed consistently across all environments

### 3. Application Logging Implementation

#### Log Group Configuration
- Define log groups using CDK with standardized naming: `/aws/{service}/{environment}/{application}`
- Configure appropriate retention policies based on environment type
- Integrate log groups with ECS task definitions for automatic log streaming

#### Structured Logging Requirements
- Implement structured JSON logging with mandatory fields (@timestamp, @level, @message, @requestId, @service)
- Configure log-based metrics for error tracking and performance monitoring
- Create log-based alarms for critical error patterns using CDK constructs

#### Log Monitoring Integration
- Define metric filters for error tracking using CDK
- Configure log-based alarms with appropriate thresholds
- Integrate log monitoring with overall alerting strategy