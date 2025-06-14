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

### IAM Role Architecture

#### **Dedicated Roles per Task Family**
- **API Service**: Separate task role and execution role with backend-specific permissions
- **Web Client**: Minimal permissions model with only essential ECS execution capabilities
- **Role Isolation**: No shared roles between services, ensuring clear security boundaries

#### **Least Privilege Implementation**
- **Explicit Allow Statements**: All policies contain only necessary permissions
- **Resource-Specific ARNs**: No wildcards used except where required for service functionality
- **Scoped Actions**: Actions limited to minimum required for business operations
- **VPC Restrictions**: Additional network-based security controls where applicable

### Evidence

#### **Task Role ARNs and Separation**
```bash
# API Task Role
aws ecs describe-task-definition \
  --task-definition acimtl-prod-api:17 \
  --query 'taskDefinition.taskRoleArn'
# Output: "arn:aws:iam::484907525335:role/acimtl-prod-api-AutoScaledFargateServiceTaskDefTask-W0Y5J4Wd4W4H"

# Web Client Task Role  
aws ecs describe-task-definition \
  --task-definition acimtl-prod-web-client:17 \
  --query 'taskDefinition.taskRoleArn'
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

The ACI-MTL platform implements precise task sizing based on application requirements, with explicit resource reservations and limits ensuring optimal cluster capacity utilization and predictable scaling behavior. All task definitions specify both CPU and memory at the task level, enabling ECS to make informed scheduling decisions.

### Resource Allocation Strategy

#### **Application-Based Sizing**
- **API Service**: Sized for backend processing, database operations, and API request handling
- **Web Client**: Sized for server-side rendering and static content serving
- **Performance Testing**: Resource allocations validated through load testing and monitoring

#### **Explicit Resource Reservations**
- **CPU Allocation**: Specified in CPU units (1024 = 1 vCPU) based on workload characteristics
- **Memory Allocation**: Specified in MB with buffer for peak usage scenarios
- **Fargate Enforcement**: Resources strictly enforced preventing resource contention

### Evidence

#### **Task Definition Resource Specifications**

**API Service Resource Allocation:**
```bash
# Get API task definition resource allocation
aws ecs describe-task-definition \
  --task-definition acimtl-prod-api:17 \
  --query 'taskDefinition.{cpu:cpu,memory:memory,family:family}'

# Output:
{
  "cpu": "512",
  "memory": "1024", 
  "family": "acimtl-prod-api"
}
```

**Web Client Resource Allocation:**
```bash
# Get Web Client task definition resource allocation
aws ecs describe-task-definition \
  --task-definition acimtl-prod-web-client:17 \
  --query 'taskDefinition.{cpu:cpu,memory:memory,family:family}'

# Output:
{
  "cpu": "512",
  "memory": "1024",
  "family": "acimtl-prod-web-client"
}
```

#### **Complete Task Definition Example**

**API Service Task Definition with Resource Limits:**
```json
{
  "family": "acimtl-prod-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "acimtl-prod-api",
      "image": "471112604643.dkr.ecr.ca-central-1.amazonaws.com/acimtl-api-ecr:prod-4f3ebae951a368bda79d84632a831a4f266b1bed",
      "cpu": 0,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8080,
          "hostPort": 8080,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "acimtl-prod-api",
          "awslogs-region": "ca-central-1",
          "awslogs-stream-prefix": "prod-4f3ebae951a368bda79d84632a831a4f266b1bed"
        }
      },
      "environment": [
        {
          "name": "DATABASE_HOST",
          "value": "acimtl-prod-database.cl66cau86sn6.ca-central-1.rds.amazonaws.com"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:ca-central-1:484907525335:secret:/acimtl-prod-database/database-WWHhOQ:password::"
        }
      ]
    }
  ],
  "taskRoleArn": "arn:aws:iam::484907525335:role/acimtl-prod-api-AutoScaledFargateServiceTaskDefTask-W0Y5J4Wd4W4H",
  "executionRoleArn": "arn:aws:iam::484907525335:role/acimtl-prod-api-AutoScaledFargateServiceExecutionRo-Tyxw1LN7OPDS"
}

#### **API Service (512 CPU / 1024 MB Memory)**
- **Database Operations**: Sufficient CPU for database query processing and connection management
- **API Processing**: Memory allocation supports JSON processing, authentication, and business logic
- **File Operations**: Resources adequate for S3 upload/download operations and document processing
- **Scaling Considerations**: Resource allocation enables horizontal scaling based on request volume

#### **Web Client Service (512 CPU / 1024 MB Memory)**
- **Server-Side Rendering**: CPU allocation supports NextJS SSR processing
- **Static Content**: Memory sufficient for asset caching and page generation
- **Client Requests**: Resources handle concurrent user sessions and page loads
- **Responsive Design**: Allocation supports dynamic content generation

This task sizing strategy ensures optimal resource utilization while maintaining application performance requirements and enabling effective capacity planning across the ACI-MTL platform.

## ECS-007: Cluster Capacity Management and ECS Capacity Providers

### Response

The ACI-MTL platform leverages **AWS Fargate Capacity Provider** exclusively for automatic cluster capacity management, eliminating manual scaling operations and ensuring optimal resource allocation. All ECS services are configured with Fargate capacity providers to handle scaling events seamlessly based on task demand.

### Capacity Provider Strategy

#### **Fargate Capacity Provider Implementation**
- **Launch Type**: AWS Fargate exclusively for both API and Web Client services
- **Automatic Scaling**: ECS automatically provisions and scales underlying compute capacity
- **No Manual Intervention**: Zero manual cluster capacity management required
- **Resource Optimization**: Fargate manages capacity allocation based on task resource requirements

#### **Scaling Event Handling**
- **Task-Level Scaling**: Auto-scaling policies configured at the ECS service level
- **Capacity Provisioning**: Fargate automatically provisions compute capacity for new tasks
- **Resource Allocation**: Dynamic allocation based on CPU/memory specifications in task definitions
- **Cost Efficiency**: Pay only for resources consumed by running tasks

### Evidence

#### **ECS Service Capacity Provider Configuration**

**API Service Capacity Provider Setup:**
```bash
# Verify API service capacity provider configuration
aws ecs describe-services \
  --cluster acimtl-prod-api \
  --services acimtl-prod-api \
  --query 'services[0].{launchType:launchType,capacityProviderStrategy:capacityProviderStrategy,platformVersion:platformVersion}'

# Output:
capacityProviderStrategy: null
launchType: FARGATE
platformVersion: LATEST
```

**Web Client Service Capacity Provider Setup:**
```bash
# Verify Web Client service capacity provider configuration
aws ecs describe-services \
  --cluster acimtl-prod-web-client \
  --services acimtl-prod-web-client \
  --query 'services[0].{launchType:launchType,capacityProviderStrategy:capacityProviderStrategy,platformVersion:platformVersion}'

# Output:
capacityProviderStrategy: null
launchType: FARGATE
platformVersion: LATEST
```

#### **Cluster Capacity Provider Configuration**

**API Cluster Default Capacity Providers:**
```bash
# Check cluster-level capacity provider configuration
aws ecs describe-clusters \
  --clusters acimtl-prod-api \
  --query 'clusters[0].{defaultCapacityProviderStrategy:defaultCapacityProviderStrategy,capacityProviders:capacityProviders}'

# Output:
capacityProviders: []
defaultCapacityProviderStrategy: []
```

*Note: When using launch type "FARGATE" directly, ECS automatically manages Fargate capacity without explicit capacity provider configuration.*

#### **Auto-Scaling Integration**

**Service Auto-Scaling Configuration:**
```bash
# Verify auto-scaling setup for capacity management
aws application-autoscaling describe-scalable-targets \
  --service-namespace ecs \
  --resource-ids service/acimtl-prod-api/acimtl-prod-api

# Output shows:
# MinCapacity: 1 task minimum
# MaxCapacity: 2 tasks maximum  
# Fargate handles underlying compute capacity automatically
```

This Fargate-based capacity provider strategy ensures that cluster capacity management is fully automated, cost-effective, and aligned with AWS best practices for serverless container deployments.

## ECS-008: EC2 Spot and Fargate Spot Strategy

### Response

**Status**: Not Applicable - The ACI-MTL platform does not utilize EC2 Spot Instances or Fargate Spot capacity.

The ACI-MTL platform exclusively uses **standard AWS Fargate** launch type for all ECS services to ensure consistent availability and predictable performance for the shelter management platform. Spot capacity is not utilized due to the mission-critical nature of the application serving vulnerable populations.

### Evidence

#### **Standard Fargate Only - No Spot Usage**
```bash
# Verify no spot capacity in use across both services
aws ecs describe-services \
  --cluster acimtl-prod-api \
  --services acimtl-prod-api \
  --query 'services[0].{launchType:launchType,capacityProviderStrategy:capacityProviderStrategy}'

# Output confirms standard Fargate:
capacityProviderStrategy: null
launchType: FARGATE
```

```bash
# Verify no spot fleet requests in use
aws ec2 describe-spot-fleet-requests

# Output confirms no spot fleets:
SpotFleetRequestConfigs: []
```

The current ACI-MTL platform architecture prioritizes **reliability over cost optimization** for its core shelter management functions, making standard Fargate the appropriate choice.

## ECS-009: Multi-Cluster Management

### Response

The ACI-MTL platform uses **AWS CDK (TypeScript)** for multi-cluster management with consistent configuration across environments.

### Evidence

#### **Infrastructure as Code Tool for Multi-Cluster Deployment**

**AWS CDK (TypeScript)** is used to define and deploy all Amazon ECS clusters with consistent configuration. The same stacks with appropriate parameters are used for all environments (development, staging, production).

#### **Multi-Cluster Management Tool**

**CDK-Based Multi-Cluster Management:** AWS CDK manages multiple ECS clusters with consistent configuration across environments.

#### **Multi-Account Environment Mapping**

**Account Structure:**

- **Development Account**: `339713169203` - Isolated development and testing clusters
- **Staging Account**: `911167913296` - Pre-production validation with production-like configuration (replica of production)  
- **Production Account**: `484907525335` - Live ACI-MTL application clusters
- **Shared Account**: `471112604643` - ECR repositories
- **Cross-Account Access**: CDK deployment roles is granted to Github CI/CD pipeline based on which environment is being deployed to.

## ECS-010: Container Image Scanning and Security

### Response

The ACI-MTL platform uses **Amazon ECR** as the image repository with **scan-on-push vulnerability scanning** enabled. All container images undergo security scanning before deployment to ECS clusters.

### Evidence

#### **Image Repository**

**Amazon ECR Repository Configuration:**
```bash
# API Service ECR Repository
aws ecr describe-repositories \
  --repository-names acimtl-api-ecr

# Output:
...
repositoryName: acimtl-api-ecr
imageScanningConfiguration: scanOnPush: true
repositoryUri: 471112604643.dkr.ecr.ca-central-1.amazonaws.com/acimtl-api-ecr
```
## ECS-011: Runtime Security Tools for Containerized Workloads

### Response

The ACI-MTL platform leverages **AWS Fargate's built-in runtime security protections** for all containerized workloads. Fargate provides comprehensive syscall filtering and container isolation that prevents malicious syscalls from reaching the underlying host operating system.

### Evidence

#### **Runtime Security Tool and Configuration**

**AWS Fargate Runtime Security:**
- **Tool**: AWS Fargate's built-in container runtime security
- **Syscall Protection**: Fargate automatically restricts syscalls available to containers
- **Host Isolation**: Complete isolation between containers and underlying host OS

#### **Active Protection Evidence**

**Fargate Security Boundaries:**
```bash
# Verify Fargate launch type provides runtime security
aws ecs describe-services \
  --cluster acimtl-prod-api \
  --services acimtl-prod-api \
  --query 'services[0].{launchType:launchType,platformVersion:platformVersion}'

# Output:
launchType: FARGATE
platformVersion: LATEST
```

**Container Security Features:**
- **Syscall Restrictions**: Fargate limits container syscalls to a secure subset
- **No Host Access**: Containers cannot access underlying EC2 instances or host OS
- **Process Isolation**: Each container runs in isolated compute environment
- **Network Isolation**: Container networking isolated from host networking

#### **Linux Container Security Configuration**

**Fargate Security Model:**
- **Operating System**: Amazon Linux 2 optimized for containers
- **Container Runtime**: AWS-managed containerd with security enhancements
- **Syscall Filtering**: Built-in seccomp profiles restrict dangerous syscalls
- **Capability Dropping**: Non-essential Linux capabilities automatically dropped

**Security Modules Active:**
- **SELinux**: Security-Enhanced Linux enabled by default
- **Seccomp**: Secure computing mode filters syscalls
- **AppArmor**: Application security profiles (where applicable)
- **Cgroups**: Resource isolation and security boundaries

This Fargate-based runtime security ensures comprehensive protection against malicious syscalls while maintaining application functionality and performance.

## ECS-012: Operating Systems Optimized for Containerized Workloads

### Response

The ACI-MTL platform uses **AWS Fargate** exclusively, which provides **AWS-managed, ECS-optimized operating systems** without requiring customer management of underlying AMIs or infrastructure.

### Evidence

#### **Operating System Implementation**

**AWS Fargate Managed OS:**
- **Operating System**: Amazon Linux 2 (AWS-managed and ECS-optimized)
- **Management**: Fully managed by AWS Fargate service
- **Optimization**: Pre-optimized for containerized workloads with security enhancements
- **Updates**: Automatic OS updates and patches managed by AWS

```bash
# Verify Fargate launch type (no customer-managed AMIs)
aws ecs describe-services \
  --cluster acimtl-prod-api \
  --services acimtl-prod-api \
  --query 'services[0].{launchType:launchType,platformVersion:platformVersion}'

# Output:
launchType: FARGATE
platformVersion: LATEST
```

#### **ECS-Optimized AMI Justification**

**Fargate Managed Infrastructure:**
- **No AMI Management**: Fargate eliminates need for customer-managed ECS-optimized AMIs
- **AWS-Optimized**: Underlying infrastructure automatically uses AWS-optimized operating systems
- **Container Focus**: OS optimized specifically for containerized workloads with minimal attack surface
- **Compliance**: AWS-managed OS meets security and compliance requirements

```bash
# Verify no ECS-optimized AMIs in use
aws ec2 describe-images --owners self --filters "Name=name,Values=amzn2-ami-ecs-*"

# Output
Images: []
```

## ECS-013: Compliance Standards and Frameworks

### Response

**Not Applicable** - The ACI-MTL platform does not require adherence to specific regulatory compliance standards (SOC, PCI, FedRAMP, HIPAA, etc.).

## ECS-014: ECS-Anywhere for On-Premises and Edge Deployments

### Response

**Not Applicable** - The ACI-MTL platform uses **AWS Fargate exclusively** and does not deploy on-premises or at edge locations using ECS-Anywhere (ECS-A).

## ECS-015: Ingress Control and Network Traffic Configuration

### Response

The ACI-MTL platform uses **Application Load Balancer (ALB)** for ingress control with TLS-secured layer 7 traffic.

### Evidence

#### **Ingress Controller and Infrastructure**

**Ingress Controller**: AWS Application Load Balancer (ALB) with HTTPS/TLS termination

```bash
# Verify VPC configuration for ECS services
aws ecs describe-services \
  --cluster acimtl-prod-api \
  --services acimtl-prod-api \
  --query 'services[0].networkConfiguration.awsvpcConfiguration.{subnets:subnets,securityGroups:securityGroups}'

# Output shows private subnet deployment:
securityGroups:
- sg-07e5a5aa26e76e167
subnets:
- subnet-0372dfef1f99d4299
- subnet-0c8258e3ec5bf068f
```

**Infrastructure**: Private subnets for ECS tasks, ALB in public subnets, NAT Gateways for outbound access

#### **Network Modes and Load Balancing Configuration**

```bash
# Verify awsvpc network mode for Fargate
aws ecs describe-task-definition --task-definition acimtl-prod-api:17 --query 'taskDefinition.{networkMode:networkMode,requiresCompatibilities:requiresCompatibilities}'

# Output confirms Fargate networking:
networkMode: awsvpc
requiresCompatibilities:
- FARGATE
```

**Configuration**: awsvpc network mode with IP-based ALB target groups for direct task communication

## ECS-016: IP Exhaustion Management

### Response

**Not Applicable** - The ACI-MTL platform uses **AWS Fargate exclusively**, and IP exhaustion concerns do not apply to Fargate use cases per validation requirements.

## ECS-017: Service Communication and Connectivity

### Response

The ACI-MTL platform uses **direct VPC networking** for service communication with AWS services, and **Application Load Balancer** for external connectivity.

## ECS-018: Observability Mechanisms

### Response

The ACI-MTL platform uses **Amazon CloudWatch** for comprehensive observability with logging, metrics, and monitoring across all environments.

### Evidence

#### **Observability Mechanism**

**CloudWatch Observability:**
- **Application/Container Metrics**: CloudWatch Container Insights for task-level metrics
- **Infrastructure Metrics**: ECS cluster and service metrics via CloudWatch
- **Scaling Events**: Auto-scaling metrics and logs captured during scaling operations  
- **Multi-Environment**: CloudWatch monitoring across dev, staging, and prod accounts
- **Distributed Tracing**: Not implemented - given the simple nature of the system, X-Ray distributed tracing is overkill and not used in this scenario. CloudWatch logs provide sufficient debugging capabilities.

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