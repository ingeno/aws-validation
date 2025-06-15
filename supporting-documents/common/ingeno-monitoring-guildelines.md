# Ingeno Monitoring and Observability Guidelines

## Purpose

This document establishes standardized procedures for implementing workload health KPIs, alerting systems across all customer environments to ensure optimal system performance and rapid issue detection.

## Workload Health KPI Implementation

### Customer Implementation Example: ACI-MTL Production

Our monitoring framework is demonstrated through the ACI-MTL production environment, showing comprehensive CloudWatch dashboard and alerting implementation.

### Infrastructure Health Metrics

**ECS Services**
• CPU utilization monitoring (alert threshold: >75% for 2 datapoints)
• Memory consumption tracking (alert threshold: >80% for 3 datapoints)
• Running vs. desired task counts for availability
• Container health check status and deployment tracking

**Database Performance**
• CPU utilization patterns with 75% alert threshold
• Database connection counts and I/O operations monitoring
• Read/Write IOPS tracking (alert threshold: >80 for 2 datapoints)
• Free storage space monitoring (alert at ≤10GB remaining)

**Load Balancer Monitoring**
• Request count and distribution patterns
• Target response times (0.315 seconds average shown)
• HTTP status code distributions (2XX, 4XX, 5XX error tracking)
• 5XX error alerts (threshold: ≥1 error for 2 datapoints within 10 minutes)

**Application Performance**
• Request processing duration and error tracking
• Service-specific performance metrics per container
• Real-time error log analysis through CloudWatch Logs Insights

## Alert Configuration Standards

### Implemented Alert Thresholds (ACI-MTL Example)

**Critical Alerts**
• API ELB HTTP 5XX errors: ≥1 for 2 datapoints within 10 minutes
• Database storage depletion: FreeStorageSpace ≤10GB
• Service unavailability through health check failures

**Warning Alerts**
• ECS CPU utilization: ≥75% for 2 datapoints within 10 minutes
• ECS Memory utilization: >80% for 3 datapoints within 3 minutes
• Database CPU utilization: ≥75% for 2 datapoints within 10 minutes
• Database I/O operations: ReadIOPS/WriteIOPS ≥80 for 2 datapoints

**Performance Monitoring**
• Application response time trending
• Resource utilization pattern analysis
• Capacity planning threshold monitoring

### Alert Evaluation Standards
• Critical/Warning alerts: 2-3 datapoints within 10 minutes
• All alerts configured with SNS integration
• Actions enabled for automated response

## Dashboard Implementation

### Standardized Dashboard Architecture

**Production Dashboard: "ops-monitoring-dashboard"**
The implemented dashboard demonstrates our standardized approach with:

**ECS Service Metrics Widget**
• Task count tracking (Deployment, Running, Task Set, Pending counts)
• CPU utilization by service (acimtl-prod-api, acimtl-prod-web-client)
• Memory utilization monitoring across all containers
• Real-time service health visualization

**Database Performance Widget**
• CPU utilization trending (6.44% current utilization shown)
• Freeable memory monitoring (1.166-1.086 GB range)
• Read/Write latency tracking (6e-3 to 6e-5 second range)
• Database connections and I/O operations
• Free storage space trending (2.656GB current)

**Load Balancer Metrics Widget**
• Request count distribution
• HTTP response code analysis (2XX, 4XX, 5XX)
• Target response time monitoring (0.315 seconds)
• Error rate tracking and alerting integration

**Application Error Tracking Widget**
• Recent application errors analysis
• CloudWatch Logs Insights integration
• Real-time error pattern detection
• "No data found" indicates healthy application state

