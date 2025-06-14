# ACI-MTL - Partner Response

## ACI-MTL Partner Response

## Description

ACI-MTL is a web-based platform to help manage shelters for homeless people. It is deployed on Amazon ECS Fargate.

The system consists of containerized services including an API backend for user authentication via Cognito and secure file management through S3, alongside a web client interface.

The platform demonstrates production-grade container orchestration with automated CI/CD deployment, comprehensive IAM security controls, and scalable infrastructure management.

## ECS-001: Amazon ECS Represents Majority of the Workload

### Response

The complete ACI-MTL application is containerized and deployed on Amazon ECS.

**Components deployed to Amazon ECS:**
1. **Frontend (web app)** - SSR frontend running on containers
2. **Backend API** - Core business logic and API for web application frontend

### Evidence

```bash
# List tasks for web client
> aws ecs list-tasks --cluster acimtl-prod-web-client

taskArns:
- arn:aws:ecs:ca-central-1:484907525335:task/acimtl-prod-web-client/acec54f623894240804eae1ec13867b9

# List tasks for backend api
> aws ecs list-tasks --cluster acimtl-prod-api       

taskArns:
- arn:aws:ecs:ca-central-1:484907525335:task/acimtl-prod-api/09d11cc6e2454d5e8b16ee472ea5eaaf
```

## ECS-002: Changes to Infrastructure and Workloads are Deployed in an Automated Way

### Response

**Infrastructure as Code Tooling:** AWS CDK (TypeScript) for infrastructure provisioning and ECS service management

**Automated Deployment Tools:** 
- GitHub Actions for CI/CD pipeline orchestration
- Docker for containerized application builds
- Amazon ECR for container image storage and versioning

**Deployment Process:** 
Pull requests trigger code review and automated testing pipeline (linting, unit tests, component tests, end-to-end tests). Merged code in main branch triggers GitHub Actions workflow that builds container images tagged with Git commit SHA, pushes to ECR, deploys to staging environment via CDK with automated health checks for validation, and upon staging validation, deploys to production with ECS service updates.

**Rollback Procedures:** 
Automatic rollback triggered by health check failures and CloudWatch alarms during deployment. Previous task definition versions remain available for rollback procedures.

**Source Repository:** 
GitHub repository with branch protection policies requiring code reviews. Infrastructure code, ECS task definitions, and application configuration stored under version control.

**Version Control System:** 
Git with container image tags corresponding to Git commit SHAs, ensuring traceability from code commit to deployed infrastructure.

**CI/CD Tooling:** 
GitHub Actions workflows integrate with AWS services to automate ECS task definition updates and service deployments. All production changes flow through the version-controlled deployment pipeline with zero manual changes permitted.

## ECS-003: Task Definition Families for Singular Business Purpose

### Response

**Task Definitions and Business Functions:**

1. **`acimtl-prod-api`** - Backend API Services
   - Core API services and business logic layer for shelter management operations

2. **`acimtl-prod-web-client`** - Frontend Web Application  
   - User interface and web application serving for shelter management platform

### Evidence

```bash
# List task definition families
aws ecs list-task-definition-families

families:
- acimtl-prod-api
- acimtl-prod-web-client
```

## ECS-004: Tagging Strategy and Amazon ECS Managed Tags and Tag Propagation

### Response

**Tagging Strategy:** One-to-one mapping between Git commit SHA, container image tag, and task definition revision ensures version traceability.

**Tag Dimensions:** Environment, Application, Component, Version accurately represent task launches within ECS clusters.

### Evidence

```bash
# Task definition tags
aws ecs describe-task-definition --task-definition acimtl-prod-api:17 --include TAGS --query 'tags'
# Output: 
[
  {"key": "Environment", "value": "production"},
  {"key": "Application", "value": "acimtl"},
  {"key": "Component", "value": "api"},
  {"key": "Version", "value": "4f3ebae951a368bda79d84632a831a4f266b1bed"}
]

# ECS managed tags and tag propagation enabled
aws ecs describe-services --cluster acimtl-prod-api --services acimtl-prod-api --query 'services[0].{propagateTags:propagateTags,enableECSManagedTags:enableECSManagedTags}'
# Output: 
{
  "propagateTags": "TASK_DEFINITION", 
  "enableECSManagedTags": true
}
```

## ECS-005: IAM Roles and Security

### Response

Each task definition family in the ACI-MTL platform has dedicated IAM roles following the principle of least privilege. The architecture implements strict role separation where each service has access only to the specific AWS resources and actions required for its designated business function.

### Evidence

```bash
# API Task Role
aws ecs describe-task-definition --task-definition acimtl-prod-api:17 --query 'taskDefinition.taskRoleArn'
# Output: "arn:aws:iam::484907525335:role/acimtl-prod-api-AutoScaledFargateServiceTaskDefTask-W0Y5J4Wd4W4H"

# Web Client Task Role  
aws ecs describe-task-definition --task-definition acimtl-prod-web-client:17 --query 'taskDefinition.taskRoleArn'
# Output: "arn:aws:iam::484907525335:role/acimtl-prod-web-client-AutoScaledFargateServiceTask-2PQCxZE72dbm"
```

#### **API Service Role Permissions (Backend Policy)**
The API service role demonstrates precise resource scoping:

**Cognito Identity Provider Permissions:**
```json
{
  "Effect": "Allow",
  "Action": [
    "cognito-idp:AdminCreateUser",
    "cognito-idp:AdminDeleteUser", 
    "cognito-idp:AdminDisableUser",
    "cognito-idp:AdminEnableUser",
    "cognito-idp:AdminGetUser",
    "cognito-idp:AdminUpdateUserAttributes"
  ],
  "Resource": "arn:aws:cognito-idp:ca-central-1:484907525335:userpool/ca-central-1_J0PRtqr7r"
}
```

**CloudWatch Logs Permissions:**
```json
{
  "Effect": "Allow",
  "Action": [
    "logs:CreateLogStream",
    "logs:DescribeLogStreams", 
    "logs:PutLogEvents"
  ],
  "Resource": "arn:aws:logs:ca-central-1:484907525335:log-group:acimtl-prod-api:*"
}
```

**S3 Permissions with VPC Restriction:**
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:DeleteObject",
    "s3:GetObject",
    "s3:ListBucket",
    "s3:PutObject"
  ],
  "Resource": [
    "arn:aws:s3:::acimtl-prod-bucket-clientsfiles6bf6a7b3-ahcxoubzmxqq/*",
    "arn:aws:s3:::acimtl-prod-bucket-clientsfiles6bf6a7b3-ahcxoubzmxqq"
  ],
  "Condition": {
    "StringEqualsIfExists": {
      "aws:SourceVpc": "acimtl-prod"
    }
  }
}

```

#### **Web Client Role Permissions**
```bash
# Check Web Client role policies
aws iam list-attached-role-policies \
  --role-name acimtl-prod-web-client-AutoScaledFargateServiceTask-2PQCxZE72dbm
# Output: AttachedPolicies: []

aws iam list-role-policies \
  --role-name acimtl-prod-web-client-AutoScaledFargateServiceTask-2PQCxZE72dbm
# Output: PolicyNames: []
```
## ECS-006: Task Sizing and Resource Limits

### Response

Task definitions specify explicit CPU and memory resource reservations based on application requirements. Resource limits were determined through empirical testing under production load scenarios to ensure optimal performance and cost efficiency.

### Evidence

```bash
# API Service Resource Configuration
aws ecs describe-task-definition --task-definition acimtl-prod-api:17 --query 'taskDefinition.{cpu:cpu,memory:memory,family:family}'
# Output:
{
  "cpu": "512",
  "memory": "1024", 
  "family": "acimtl-prod-api"
}

# Web Client Resource Configuration
aws ecs describe-task-definition --task-definition acimtl-prod-web-client:17 --query 'taskDefinition.{cpu:cpu,memory:memory,family:family}'
# Output:
{
  "cpu": "512",
  "memory": "1024",
  "family": "acimtl-prod-web-client"
}
```

## ECS-007: Cluster Capacity Management and ECS Capacity Providers

### Response

The ACI-MTL platform leverages AWS Fargate Capacity Provider exclusively for automatic cluster capacity management, eliminating manual scaling operations and ensuring optimal resource allocation. All ECS services are configured with Fargate capacity providers to handle scaling events seamlessly based on task demand.

### Evidence

```bash
# Verify Fargate capacity provider configuration
aws ecs describe-clusters --clusters acimtl-prod-api --include CAPACITY_PROVIDERS
# Output:
clusterName: acimtl-prod-api
capacityProviders:
- FARGATE
defaultCapacityProviderStrategy:
- capacityProvider: FARGATE
  weight: 1
  base: 0
```

## ECS-008: EC2 Spot and Fargate Spot Strategy

### Response

**Status**: Not Applicable

The ACI-MTL platform exclusively uses standard AWS Fargate launch type for all ECS services to ensure consistent availability and predictable performance for the shelter management platform. Spot capacity is not utilized due to the mission-critical nature of the application serving vulnerable populations.

### Evidence

```bash
# Verify no spot capacity in use
aws ecs describe-services --cluster acimtl-prod-api --services acimtl-prod-api --query 'services[0].launchType'
# Output: FARGATE

# Verify no spot fleet requests in use
aws ec2 describe-spot-fleet-requests
# Output: SpotFleetRequestConfigs: []
```

## ECS-009: Multi-Cluster Management

### Response

The ACI-MTL platform uses **AWS CDK (TypeScript)** for multi-cluster management with consistent configuration across environments.

### Evidence

**IaC Tool:** AWS CDK (TypeScript) is used to define and deploy all Amazon ECS clusters with consistent configuration across environments. A single set of parameterizable stacks is used for all environments (development, staging, production).

**Multi-Cluster Management Tool:** AWS CDK manages multiple ECS clusters with consistent configuration.

**Multi-Account Environment Mapping:**
- **Development Account**: `339713169203` - Development and testing clusters
- **Staging Account**: `911167913296` - Pre-production validation clusters  
- **Production Account**: `484907525335` - Live ACI-MTL application clusters
- **Shared Account**: `471112604643` - ECR repositories (sharing images between environments)

## ECS-010: Container Image Scanning and Security

### Response

The ACI-MTL platform uses **Amazon ECR** as the image repository with **scan-on-push vulnerability scanning** enabled. All container images undergo security scanning before deployment to ECS clusters.

### Evidence

```bash
# ECR repository with scan-on-push configuration
aws ecr describe-repositories --repository-names acimtl-api-ecr --query 'repositories[0].{repositoryName:repositoryName,scanOnPush:imageScanningConfiguration.scanOnPush}'
# Output:
{
  "repositoryName": "acimtl-api-ecr",
  "scanOnPush": true
}

# Image versions match task definitions
aws ecs describe-task-definition --task-definition acimtl-prod-api:17 --query 'taskDefinition.containerDefinitions[0].image'
# Output: 
"471112604643.dkr.ecr.ca-central-1.amazonaws.com/acimtl-api-ecr:prod-4f3ebae951a368bda79d84632a831a4f266b1bed"
```

**ECR Repository Policies:** ECS task execution roles have ECR pull permissions and repository policies restrict access to authorized roles.

**ECR Monitoring:** CloudWatch monitors ECR repository usage and vulnerability scan results with alerting for HIGH/CRITICAL findings.

## ECS-011: Runtime Security Tools for Containerized Workloads

### Response

The ACI-MTL platform leverages **AWS Fargate's built-in runtime security protections** for all containerized workloads. Fargate provides comprehensive syscall filtering and container isolation that prevents malicious syscalls from reaching the underlying host operating system.

### Evidence

```bash
# Verify Fargate launch type provides runtime security
aws ecs describe-services --cluster acimtl-prod-api --services acimtl-prod-api --query 'services[0].{launchType:launchType,platformVersion:platformVersion}'
# Output:
{
  "launchType": "FARGATE",
  "platformVersion": "LATEST"
}
```

**Runtime Security Tool:** AWS Fargate provides built-in syscall filtering and container isolation that prevents malicious syscalls from reaching the underlying host operating system.

## ECS-012: Operating Systems Optimized for Containerized Workloads

### Response

The ACI-MTL platform uses **AWS Fargate** exclusively, which provides **AWS-managed, ECS-optimized operating systems** without requiring customer management of underlying AMIs or infrastructure.

### Evidence

```bash
# Verify Fargate launch type
aws ecs describe-services --cluster acimtl-prod-api --services acimtl-prod-api --query 'services[0].{launchType:launchType,platformVersion:platformVersion}'
# Output:
{
  "launchType": "FARGATE",
  "platformVersion": "LATEST"
}
```

**Operating System:** Amazon Linux 2 (AWS-managed and ECS-optimized via Fargate)

**ECS-Optimized AMI Justification:** Fargate eliminates the need for customer-managed ECS-optimized AMIs as the underlying infrastructure is automatically managed by AWS.

## ECS-013: Compliance Standards and Frameworks

### Response

**Not Applicable** - The ACI-MTL platform does not require adherence to specific regulatory compliance standards (SOC, PCI, FedRAMP, HIPAA, etc.).

## ECS-014: ECS-Anywhere for On-Premises and Edge Deployments

### Response

**Not Applicable** - The ACI-MTL platform uses **AWS Fargate exclusively**, and does not deploy on-premises or at edge locations using ECS-Anywhere (ECS-A).

## ECS-015: Ingress Control and Network Traffic Configuration

### Response

The ACI-MTL platform uses **Application Load Balancer (ALB)** for ingress control with TLS-secured layer 7 traffic.

### Evidence

```bash
# Verify network configuration and ingress setup
aws ecs describe-services --cluster acimtl-prod-api --services acimtl-prod-api --query 'services[0].networkConfiguration.awsvpcConfiguration.{subnets:subnets,securityGroups:securityGroups}'
# Output:
{
  "securityGroups": ["sg-07e5a5aa26e76e167"],
  "subnets": ["subnet-0372dfef1f99d4299", "subnet-0c8258e3ec5bf068f"]
}

# Verify awsvpc network mode for Fargate
aws ecs describe-task-definition --task-definition acimtl-prod-api:17 --query 'taskDefinition.{networkMode:networkMode,requiresCompatibilities:requiresCompatibilities}'
# Output:
{
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"]
}
```

**Ingress Controller:** AWS Application Load Balancer (ALB) with HTTPS/TLS termination

**Infrastructure:** Private subnets for ECS tasks, ALB in public subnets, NAT Gateways for outbound access

**Network Mode:** awsvpc network mode with IP-based ALB target groups for direct task communication

## ECS-016: IP Exhaustion Management

### Response

**Not Applicable** - The ACI-MTL platform uses **AWS Fargate exclusively**, and IP exhaustion concerns do not apply to Fargate use cases per validation requirements.

## ECS-017: Service Communication and Connectivity

### Response

The ACI-MTL platform uses **direct VPC networking** for service communication with AWS services, and **Application Load Balancer** for external connectivity.

### Evidence

```bash
# Verify VPC networking configuration
aws ecs describe-services --cluster acimtl-prod-api --services acimtl-prod-api --query 'services[0].networkConfiguration.awsvpcConfiguration.{subnets:subnets,securityGroups:securityGroups}'
# Output:
{
  "securityGroups": ["sg-07e5a5aa26e76e167"],
  "subnets": ["subnet-0372dfef1f99d4299", "subnet-0c8258e3ec5bf068f"]
}
```

**AWS Services Integration:** Direct VPC connectivity through private subnets for RDS, S3 via VPC endpoints, and direct service integration for Cognito authentication.

**External Connectivity:** Application Load Balancer with TLS termination for secure external access.

**Internal Communication:** Direct VPC networking within private subnets without service mesh due to stateless architecture.

## ECS-018: Observability Mechanisms

### Response

The ACI-MTL platform uses **Amazon CloudWatch** for comprehensive observability with logging, metrics, and monitoring across all environments.

### Evidence

```bash
# Verify CloudWatch log groups for ECS services
aws logs describe-log-groups --query 'logGroups[?contains(logGroupName, `acimtl-prod`)].logGroupName'
# Output:
[
  "acimtl-prod-api",
  "acimtl-prod-web-client"
]

# Verify Container Insights enabled for application/container metrics
aws ecs describe-clusters --clusters acimtl-prod-api --include SETTINGS --query 'clusters[0].settings'
# Output:
[
  {
    "name": "containerInsights",
    "value": "enabled"
  }
]

# Verify ECS service metrics for infrastructure layer monitoring
aws cloudwatch list-metrics --namespace AWS/ECS --query 'Metrics[?contains(MetricName, `CPUUtilization`)].{MetricName:MetricName,Dimensions:Dimensions[0]}'
# Output:
[
  {
    "MetricName": "CPUUtilization",
    "Dimensions": {
      "Name": "ServiceName",
      "Value": "acimtl-prod-api"
    }
  },
  {
    "MetricName": "CPUUtilization",
    "Dimensions": {
      "Name": "ServiceName", 
      "Value": "acimtl-prod-web-client"
    }
  }
]
```

**Application/Container Metrics:** CloudWatch Container Insights enabled for individual task and container-level metrics collection and filtering.

**Infrastructure Metrics:** ECS cluster and service metrics captured via CloudWatch for infrastructure layer monitoring.

**Scaling Events:** Auto-scaling metrics and logs captured during scaling operations across all services.

**Multi-Environment:** CloudWatch monitoring deployed across development, staging, and production accounts.

**Distributed Tracing:** CloudWatch logs provide application debugging capabilities for the stateless architecture.

## ECS-019: Storage Options Selection

### Response

The ACI-MTL platform uses **external database services** and **object storage** to meet application storage requirements without persistent container storage.

### Evidence

#### **Workload and Storage Selection**

**Shelter Management Application Workload:**
- **Database Operations**: Client records, case management, reporting queries
- **File Management**: Document uploads, reports, administrative files
- **Web Application**: Stateless application serving and API processing

**Storage Solutions:**
- **Amazon RDS**: PostgreSQL database for transactional data with automated backups
- **Amazon S3**: Object storage for file uploads and document management
- **No Container Storage**: Fargate containers remain stateless without persistent volumes

**Performance Requirements and Reasoning:**
- **RDS**: Sub-second query response for database operations, automated scaling and backup
- **S3**: Standard access latency acceptable for file storage, cost-effective for document retention
- **Stateless Design**: No container-level storage needed, simplifies deployment and scaling

## ECS-020: EFS Mount Targets in Availability Zones

### Response

**Not Applicable** - The ACI-MTL platform does not use Amazon Elastic File System (EFS) for persistent storage.

## ECS-021: Secure Access to Persistent Storage

### Response

The ACI-MTL platform secures access to persistent storage (RDS and S3) through **IAM roles and VPC security controls** limiting access to only applications that require it.

### Evidence

#### **Access Requirements Evaluation**

**Storage Access Analysis:**
- **RDS Database**: Only API service requires database access for application data
- **S3 File Storage**: Only API service requires file upload/download capabilities
- **Web Client**: No direct storage access required

#### **Security Method**

**IAM Role-Based Access Control:**
- **API Service**: IAM task role with RDS and S3 permissions
- **Web Client**: No storage permissions in IAM task role
- **VPC Security**: Database in private subnets, accessible only via VPC

## ECS-022: EBS Task Placement Constraints

### Response

**Not Applicable** - The ACI-MTL platform uses **AWS Fargate exclusively**, and EBS volumes are not supported with Fargate launch type.

## ECS-023: Multi-Tenant Workloads

### Response

**Not Applicable** - The ACI-MTL platform is designed as a **single-tenant application**. There is only one production deployment that manages multiple shelters.