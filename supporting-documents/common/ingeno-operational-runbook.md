# Ingeno AWS Operational Runbook

## Purpose

This operational runbook provides standardized procedures for routine activities, issue resolution, and troubleshooting scenarios for AWS ECS-based workloads. The runbook specifically addresses the workload health KPIs defined in the Ingeno Monitoring and Observability Framework and establishes consistent operational practices across all customer environments.

## Scope

This runbook covers operational procedures for:
- ECS service monitoring and troubleshooting
- Database performance management
- Application performance optimization
- Alert response and escalation procedures
- Incident resolution workflows
- Routine maintenance activities

## Prerequisites

- Access to AWS Management Console with appropriate IAM permissions
- CloudWatch dashboard access for the target environment
- SNS alert notifications configured
- AWS CLI configured with appropriate profiles
- On-call rotation schedule established

---

## Health check routine

**Objective:** Verify system health and identify any issues requiring attention.

**Procedure:**
1. **Review CloudWatch Dashboard**
   - Access technical dashboard: `{customer}-{environment}-technical-dashboard`
   - Verify all widgets display current data (no "No data available" messages)
   - Check last 12-hour trends for all critical metrics

2. **Alert Status Review**
   - Review CloudWatch Alarms console for any active alarms
   - Check SNS notification history for overnight alerts
   - Verify resolution of any previously active incidents

3. **Resource Utilization Assessment**
   - **ECS Services:** Verify running task counts match desired capacity
   - **Database:** Check connection count trends and query performance
   - **Load Balancer:** Review request distribution and response times

4. **Log Analysis**
   - Execute CloudWatch Logs Insights queries for error patterns:
     ```
     fields @timestamp, @message, @requestId
     | filter @level = "ERROR"
     | stats count() by @service
     | sort count desc
     ```

**Escalation:** Report any anomalies to development team via Slack project channel.

### Capacity Planning Review

**Objective:** Analyze resource utilization trends and plan capacity adjustments.

**Procedure:**
1. **Trend Analysis (7-day period)**
   - ECS CPU/Memory utilization patterns
   - Database connection and storage growth
   - Application response time trends
   - Load balancer request volume patterns

2. **Capacity Recommendations**
   - Identify services approaching 70% sustained utilization
   - Evaluate auto-scaling configurations
   - Plan infrastructure adjustments for upcoming releases

3. **Cost Optimization Review**
   - Identify underutilized resources
   - Review Reserved Instance coverage
   - Assess spot instance opportunities for non-critical workloads

---

## Alert Response Procedures

### Critical Alert Response (Immediate - 0-5 minutes)

**Trigger Conditions:**
- ECS CPU utilization >85%
- ECS Memory utilization >90%
- Application 5XX error rate >5%
- Service health check failures
- Database connection exhaustion

**Response Procedure:**

1. **Initial Assessment (0-2 minutes)**
   - Acknowledge alert in monitoring system
   - Access CloudWatch dashboard for affected service
   - Determine scope: single service vs. multiple services affected

2. **Immediate Actions (2-5 minutes)**
   - **ECS High Utilization:**
     - Check ECS service auto-scaling status
     - Manually increase desired task count if auto-scaling disabled
     - Verify load balancer health check status
   
   - **Application Errors:**
     - Execute log query to identify error patterns:
       ```
       fields @timestamp, @message, @requestId, @level
       | filter @level = "ERROR" and @timestamp > "2024-01-01T00:00:00"
       | sort @timestamp desc
       | limit 20
       ```
     - Check recent deployment history for correlation
   
   - **Database Issues:**
     - Review active connections and blocking queries
     - Check RDS performance insights for slow queries
     - Verify read replica availability

3. **Communication (Within 5 minutes)**
   - Post incident status in #alerts Slack channel
   - Notify customer if external impact confirmed
   - Update incident tracking system

**Escalation:** If not resolved within 15 minutes, escalate to senior engineer and customer success manager.

### Warning Alert Response

**Trigger Conditions:**
- ECS CPU utilization >70%
- Database query latency >200ms
- Application 4XX error rate >10%
- DynamoDB throttling events

**Response Procedure:**

1. **Analysis Phase (0-5 minutes)**
   - Review alert context and recent trends
   - Check for correlation with other metrics
   - Identify potential root causes

2. **Investigation Actions (5-15 minutes)**
   - **Performance Degradation:**
     - Analyze CloudWatch Logs for application bottlenecks
     - Review database query performance
     - Check external service dependencies
   
   - **Resource Constraints:**
     - Evaluate current vs. historical resource usage
     - Check auto-scaling configuration and recent scaling events
     - Review application deployment logs

3. **Preventive Actions**
   - Implement temporary scaling adjustments if warranted
   - Schedule follow-up capacity planning review
   - Document findings for trend analysis

### Performance Alert Response

**Trigger Conditions:**
- Application response time >500ms
- Database read/write latency >100ms
- Load balancer target response time >1000ms

**Response Procedure:**

1. **Trend Analysis**
   - Review 24-hour performance patterns
   - Compare with previous week's baseline
   - Identify performance regression patterns

2. **Optimization Assessment**
   - Database query optimization opportunities
   - Application code performance review scheduling
   - Infrastructure rightsizing recommendations

---

## Troubleshooting Scenarios

### Scenario 1: ECS Service Startup Failures

**Symptoms:**
- ECS tasks failing to start or immediately stopping
- Service showing "PENDING" tasks that don't reach "RUNNING" state

**Diagnostic Steps:**
1. **Task Definition Review**
   - Check task definition for resource allocation errors
   - Verify container image availability and tags
   - Review environment variable configuration

2. **Service Event Analysis**
   - Access ECS console → Service → Events tab
   - Look for placement constraint failures
   - Check for insufficient resources in cluster

3. **CloudWatch Logs Investigation**
   - Review task logs for application startup errors
   - Check for dependency connection failures (database, external APIs)

**Resolution Actions:**
- Update task definition resource requirements if insufficient
- Verify security group and network ACL configurations
- Check application configuration and dependencies
- Scale cluster capacity if resource constraints identified

### Scenario 2: Database Performance Degradation

**Symptoms:**
- Query latency exceeding normal baselines
- Connection pool exhaustion alerts
- Application timeout errors

**Diagnostic Steps:**
1. **Performance Insights Analysis**
   - Access RDS Performance Insights dashboard
   - Identify top SQL statements by execution time
   - Review wait events and resource utilization

2. **Connection Analysis**
   - Monitor active vs. maximum connections
   - Check for connection leaks in application logs
   - Review connection pooling configuration

3. **Resource Utilization Review**
   - CPU utilization patterns and spikes
   - Storage I/O performance metrics
   - Memory utilization and buffer cache efficiency

**Resolution Actions:**
- Optimize slow queries identified in Performance Insights
- Adjust connection pool settings in application configuration
- Scale database instance if resource constrained
- Implement read replica for read-heavy workloads

### Scenario 3: Application Load Balancer Issues

**Symptoms:**
- High response times from load balancer
- Uneven traffic distribution across targets
- Target health check failures

**Diagnostic Steps:**
1. **Target Health Assessment**
   - Review target group health in ALB console
   - Check health check configuration and response codes
   - Verify target registration and deregistration patterns

2. **Traffic Pattern Analysis**
   - Review request count distribution across targets
   - Check for sticky session configuration issues
   - Analyze response code distribution (2xx, 4xx, 5xx)

3. **Load Balancer Configuration Review**
   - Verify listener rules and target group routing
   - Check security group configurations
   - Review SSL certificate status and configuration

**Resolution Actions:**
- Adjust health check parameters if too aggressive
- Update target group configuration for better distribution
- Scale target capacity if traffic exceeds current capacity
- Review and optimize application health check endpoint

### Scenario 4: DynamoDB Performance Issues

**Symptoms:**
- Throttling events on DynamoDB tables
- Increased application latency for database operations
- UserErrors or SystemErrors in DynamoDB metrics

**Diagnostic Steps:**
1. **Capacity Analysis**
   - Review consumed vs. provisioned read/write capacity
   - Check for hot partition issues using CloudWatch Contributor Insights
   - Analyze access patterns and key distribution

2. **Query Pattern Review**
   - Identify inefficient scan operations vs. queries
   - Review Global Secondary Index (GSI) usage patterns
   - Check for missing or suboptimal indexes

**Resolution Actions:**
- Increase provisioned capacity or enable auto-scaling
- Optimize query patterns to avoid hot partitions
- Implement exponential backoff for throttled requests
- Consider table design changes for better key distribution

---

## Incident Resolution Workflow

### Incident Classification

**Severity 1 (Critical):** Complete service outage affecting all users
- Response time: Immediate (0-5 minutes)
- Resolution target: 1 hour
- Communication: Real-time updates every 15 minutes

**Severity 2 (High):** Partial service degradation affecting subset of users
- Response time: 15 minutes
- Resolution target: 4 hours
- Communication: Updates every 30 minutes

**Severity 3 (Medium):** Performance issues with workaround available
- Response time: 1 hour
- Resolution target: 24 hours
- Communication: Initial response and resolution summary

### Incident Response Process

1. **Detection and Acknowledgment**
   - Alert received via CloudWatch/SNS
   - Incident acknowledged in alerting system (depends on each customer - e.g. PagerDuty)
   - Initial assessment and severity classification

2. **Investigation and Diagnosis**
   - Execute relevant troubleshooting procedures
   - Gather diagnostic information using CloudWatch tools
   - Identify root cause or implement temporary mitigation

3. **Resolution and Recovery**
   - Apply fix or implement workaround
   - Verify system recovery using monitoring dashboards
   - Confirm resolution with stakeholders

4. **Post-Incident Activities**
   - Document incident details and resolution steps
   - Conduct post-mortem review for Severity 1 and 2 incidents
   - Implement preventive measures to avoid recurrence

### Communication Templates

**Initial Incident Notification:**
```
🚨 INCIDENT ALERT - Severity {X}
Service: {Service Name}
Impact: {Description of impact}
Status: Investigating
ETA for Update: {Time}
```

**Resolution Notification:**
```
✅ INCIDENT RESOLVED - Severity {X}
Service: {Service Name}
Duration: {Start time - End time}
Root Cause: {Brief description}
Prevention: {Actions taken to prevent recurrence}
```

---

## Routine Maintenance Procedures

**Procedure:**
1. **Pre-maintenance Verification**
   - Verify backup completion for all databases
   - Check system health status using dashboards
   - Notify stakeholders of maintenance window

2. **Patching Process**
   - Apply security patches to ECS container images
   - Update task definitions with new image versions
   - Perform rolling deployment to minimize downtime

3. **Post-maintenance Validation**
   - Verify all services return to healthy state
   - Execute health check validation procedures
   - Monitor for 30 minutes post-deployment

### Disaster Recovery Testing

**Procedure:**
1. **Database Backup Restoration Testing**
   - Restore RDS snapshots to test environment
   - Verify data integrity and application connectivity
   - Document restoration time and process

2. **Recovery Documentation Update**
   - Update disaster recovery procedures based on test results
   - Review and update emergency contact information
   - Validate backup retention and recovery objectives

---

## Escalation Procedures

### Internal Escalation Path

**Level 1:** Project Team Leader
- Initial response and basic troubleshooting
- Escalation trigger: Unable to resolve within defined SLA

**Level 2:** COO - Denis Brochu
- Advanced troubleshooting and system analysis
- Architecture and infrastructure modifications
- Escalation trigger: Complex technical issues or extended outage

### Customer Communication

**Proactive Communication Triggers:**
- Any Severity 1 incident
- Planned maintenance extending beyond scheduled window

**Communication Channels:**
- Alerting system (e.g. PagerDuty): Primary incident notifications
- Slack: Real-time updates and internal coordination
- Phone: Emergency escalation for critical incidents

### Knowledge Management

**Incident Documentation:**
- All incidents must be documented in incident tracking system
- Post-mortem reports required for Severity 1 and 2 incidents
- Knowledge base articles created for recurring issues
