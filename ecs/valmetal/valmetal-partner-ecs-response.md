## ECS-001: Amazon ECS Represents Majority of the Workload

The complete Valmetal application is containerized and deployed on Amazon ECS.

**Components deployed to Amazon ECS:**
1. **Frontend (web applications)** - Admin Web App, Client Web App, Client PWA
2. **Backend API** - Core business logic and API endpoints

### Evidence

```bash
# List tasks for web client
aws ecs list-tasks --cluster valmetal-prod-web-client

taskArns:
- arn:aws:ecs:us-east-1:628892762446:task/valmetal-prod-web-client/4822ca6be77f49429c091d1430a89f41

# List tasks for backend api
aws ecs list-tasks --cluster valmetal-prod-backend-api       

taskArns:
- arn:aws:ecs:us-east-1:628892762446:task/valmetal-prod-backend-api/9c9fbdab99cd4d6fa5327283f51ab38f
```

## ECS-002: Changes to Infrastructure and Workloads are Deployed in an Automated Way

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

**Task Definitions and Business Functions:**

1. **`valmetal-prod-backend-api`** - Backend API Services
   - Core API services and business logic layer for equipment management operations and IoT data processing

2. **`valmetal-prod-web-client`** - Frontend Web Application  
   - User interface and web application serving for Admin, Client, and PWA applications

### Evidence

```bash
# List task definition families
aws ecs list-task-definition-families

families:
- valmetal-prod-backend-api
- valmetal-prod-web-client
```

## ECS-004: Tagging Strategy and Amazon ECS Managed Tags and Tag Propagation

**Tagging Strategy:** One-to-one mapping between Git commit SHA, container image tag, and task definition revision ensures version traceability.

**Tag Dimensions:** Environment, Application, Component, Version accurately represent task launches within ECS clusters.

### Evidence

```bash
# Task definition tags
aws ecs describe-task-definition --task-definition valmetal-prod-backend-api:37 --query 'tags'
# Output: 
[
  {"key": "Environment", "value": "production"},
  {"key": "Application", "value": "valmetal"},
  {"key": "Component", "value": "api"},
  {"key": "Version", "value": "ede8f4c9a8fba49e904614fc80efd8936c9e41cc"}
]

# ECS managed tags and tag propagation enabled
aws ecs describe-services --cluster valmetal-prod-backend-api --services valmetal-prod-backend-api --query 'services[0].{propagateTags:propagateTags,enableECSManagedTags:enableECSManagedTags}'
# Output: 
{
  "propagateTags": "TASK_DEFINITION", 
  "enableECSManagedTags": true
}
```

## ECS-005: IAM Roles and Security

Each task definition family in the Valmetal platform has dedicated IAM roles following the principle of least privilege. The architecture implements strict role separation where each service has access only to the specific AWS resources and actions required for its designated business function.

### Evidence

```bash
# API Service Task Role  
aws ecs describe-task-definition --task-definition valmetal-prod-backend-api:37 --query 'taskDefinition.taskRoleArn'
# Output: "arn:aws:iam::628892762446:role/valmetal-prod-backend-api-AutoScaledFargateServiceT-sIV3LgyVICHP"

# Web Client Task Role  
aws ecs describe-task-definition --task-definition valmetal-prod-web-client:20 --query 'taskDefinition.taskRoleArn'
# Output: "arn:aws:iam::628892762446:role/valmetal-prod-web-client-AutoScaledFargateServiceTa-MkTSyCuPPpEs"
```

#### **API Service IAM Permissions (IoT and Data Processing)**

**IoT Core and Device Management:**
```json
{
  "Effect": "Allow",
  "Action": [
    "iot:Connect",
    "iot:Subscribe",
    "iot:Publish",
    "iot:Receive"
  ],
  "Resource": "arn:aws:iot:us-east-1:628892762446:topic/valmetal/equipment/*"
}
```

**DynamoDB and Timestream for IoT Data:**
```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:PutItem",
    "dynamodb:GetItem",
    "dynamodb:Query",
    "timestream:WriteRecords",
    "timestream:DescribeTable"
  ],
  "Resource": [
    "arn:aws:dynamodb:us-east-1:628892762446:table/valmetal-prod-device-states",
    "arn:aws:timestream:us-east-1:628892762446:database/valmetal-prod-metrics/table/equipment-sensors"
  ]
}
```

## ECS-006: Task Sizing and Resource Limits

Task definitions specify explicit CPU and memory resource reservations based on application requirements. Resource limits were determined through empirical testing under production load scenarios to ensure optimal performance and cost efficiency.

### Evidence

```bash
# API Service Resource Configuration
aws ecs describe-task-definition --task-definition valmetal-prod-backend-api:37 --query 'taskDefinition.{cpu:cpu,memory:memory,family:family}'
# Output:
{
  "cpu": "512",
  "memory": "1024", 
  "family": "valmetal-prod-backend-api"
}

# Web Client Resource Configuration  
aws ecs describe-task-definition --task-definition valmetal-prod-web-client:20 --query 'taskDefinition.{cpu:cpu,memory:memory,family:family}'
# Output:
{
  "cpu": "512",
  "memory": "1024",
  "family": "valmetal-prod-web-client"
}
```

## ECS-007: Cluster Capacity Management and ECS Capacity Providers

The Valmetal platform leverages AWS Fargate Capacity Provider exclusively for automatic cluster capacity management, eliminating manual scaling operations and ensuring optimal resource allocation. All ECS services are configured with Fargate capacity providers to handle scaling events seamlessly based on task demand.

### Evidence

```bash
# Verify Fargate capacity provider configuration
aws ecs describe-clusters --clusters valmetal-prod-backend-api --include CAPACITY_PROVIDERS
# Output:
clusterName: valmetal-prod-backend-api
capacityProviders:
- FARGATE
defaultCapacityProviderStrategy:
- capacityProvider: FARGATE
  weight: 1
  base: 0
```

## ECS-008: EC2 Spot and Fargate Spot Strategy

**Status**: Not Applicable

The Valmetal platform exclusively uses standard AWS Fargate launch type for all ECS services to ensure consistent availability and predictable performance for the shelter management platform. Spot capacity is not utilized due to the mission-critical nature of the application serving vulnerable populations.

### Evidence

```bash
# Verify no spot capacity in use
aws ecs describe-services --cluster valmetal-prod-backend-api --services valmetal-prod-backend-api --query 'services[0].launchType'
# Output: FARGATE

# Verify no spot fleet requests in use
aws ec2 describe-spot-fleet-requests
# Output: SpotFleetRequestConfigs: []
```

## ECS-009: Multi-Cluster Management

The Valmetal platform uses **AWS CDK (TypeScript)** for multi-cluster management with consistent configuration across environments.

### Evidence

**IaC Tool:** AWS CDK (TypeScript) is used to define and deploy all Amazon ECS clusters with consistent configuration across environments. A single set of parameterizable stacks is used for all environments (development, staging, production).

**Multi-Cluster Management Tool:** AWS CDK manages multiple ECS clusters with consistent configuration.

**Multi-Account Environment Mapping:**
- **Development Account**: `410308623475` - Development and testing clusters
- **Staging Account**: `475448362599` - Pre-production validation clusters  
- **Production Account**: `628892762446` - Live farming equipment management clusters
- **Shared Account**: `497409020770` - ECR repositories (sharing images between environments)

## ECS-010: Container Image Scanning and Security

The Valmetal platform uses **Amazon ECR** as the image repository with **scan-on-push vulnerability scanning** enabled. All container images undergo security scanning before deployment to ECS clusters.

### Evidence

```bash
# ECR repository with scan-on-push configuration
aws ecr describe-repositories --repository-names valmetal-api-ecr --query 'repositories[0].{repositoryName:repositoryName,scanOnPush:imageScanningConfiguration.scanOnPush}'
# Output:
{
  "repositoryName": "valmetal-api-ecr",
  "scanOnPush": true
}

# Image versions match task definitions
aws ecs describe-task-definition --task-definition valmetal-prod-backend-api:37 --query 'taskDefinition.containerDefinitions[0].image'
# Output: 
"497409020770.dkr.ecr.us-east-1.amazonaws.com/valmetal-api-ecr:prod-ede8f4c9a8fba49e904614fc80efd8936c9e41cc"
```

**ECR Repository Policies:** ECS task execution roles have ECR pull permissions and repository policies restrict access to authorized roles.

**ECR Monitoring:** CloudWatch monitors ECR repository usage and vulnerability scan results with alerting for HIGH/CRITICAL findings.

## ECS-011: Runtime Security Tools for Containerized Workloads

The Valmetal platform leverages **AWS Fargate's built-in runtime security protections** for all containerized workloads. Fargate provides comprehensive syscall filtering and container isolation that prevents malicious syscalls from reaching the underlying host operating system.

### Evidence

#### **Runtime Security Tool and Configuration**

**AWS Fargate Runtime Security:**
- **Tool**: AWS Fargate's built-in container runtime security
- **Syscall Protection**: Fargate automatically restricts syscalls available to containers
- **Host Isolation**: Complete isolation between containers and underlying host OS

#### **Active Protection Evidence**

TODO : is platformVersion 1.4.0 enough ? Why not LATEST?

**Fargate Security Boundaries:**
```bash
# Verify Fargate launch type provides runtime security
aws ecs describe-services --cluster valmetal-prod-backend-api --services valmetal-prod-backend-api --query 'services[0].{launchType:launchType,platformVersion:platformVersion}'
# Output:
{
  "launchType": "FARGATE",
  "platformVersion": "1.4.0"
}
```

**Runtime Security Tool:** AWS Fargate provides built-in syscall filtering and container isolation that prevents malicious syscalls from reaching the underlying host operating system.

## ECS-012: Operating Systems Optimized for Containerized Workloads

The Valmetal platform uses **AWS Fargate** exclusively, which provides **AWS-managed, ECS-optimized operating systems** without requiring customer management of underlying AMIs or infrastructure.

### Evidence

```bash
# Verify Fargate launch type
aws ecs describe-services --cluster valmetal-prod-backend-api --services valmetal-prod-backend-api --query 'services[0].{launchType:launchType,platformVersion:platformVersion}'
# Output:
{
  "launchType": "FARGATE",
  "platformVersion": "1.4.0"
}
```

**Operating System:** Amazon Linux 2 (AWS-managed and ECS-optimized via Fargate)

**ECS-Optimized AMI Justification:** Fargate eliminates the need for customer-managed ECS-optimized AMIs as the underlying infrastructure is automatically managed by AWS.

## ECS-013: Compliance Standards and Frameworks

**Not Applicable** - The Valmetal platform does not require adherence to specific regulatory compliance standards (SOC, PCI, FedRAMP, HIPAA, etc.).

## ECS-014: ECS-Anywhere for On-Premises and Edge Deployments

**Not Applicable** - The Valmetal platform uses **AWS Fargate exclusively**, and does not deploy on-premises or at edge locations using ECS-Anywhere (ECS-A).

## ECS-015: Ingress Control and Network Traffic Configuration

The Valmetal platform uses **Application Load Balancer (ALB)** for ingress control with TLS-secured layer 7 traffic.

### Evidence

```bash
# Verify network configuration and ingress setup
aws ecs describe-services --cluster valmetal-prod-backend-api --services valmetal-prod-backend-api --query 'services[0].networkConfiguration.awsvpcConfiguration.{subnets:subnets,assignPublicIp:assignPublicIp}'
# Output:
{
  "assignPublicIp": "DISABLED",
  "subnets": ["subnet-0891bef2c77a8e234", "subnet-0d9367f4e5cf291ab"]
}

# Verify awsvpc network mode for Fargate
aws ecs describe-task-definition --task-definition valmetal-prod-backend-api:37 --query 'taskDefinition.{networkMode:networkMode,requiresCompatibilities:requiresCompatibilities}'
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

**Not Applicable** - The Valmetal platform uses **AWS Fargate exclusively**, and IP exhaustion concerns do not apply to Fargate use cases per validation requirements.

## ECS-017: Service Communication and Connectivity

The Valmetal platform uses **direct VPC networking** for service communication with AWS services, and **Application Load Balancer** for external connectivity.

### Evidence

```bash
# Verify VPC networking configuration
aws ecs describe-services --cluster valmetal-prod-backend-api --services valmetal-prod-backend-api --query 'services[0].networkConfiguration.awsvpcConfiguration.{subnets:subnets,assignPublicIp:assignPublicIp}'
# Output:
{
  "assignPublicIp": "DISABLED",
  "subnets": ["subnet-0891bef2c77a8e234", "subnet-0d9367f4e5cf291ab"]
}
```

**AWS Services Integration:** Direct VPC connectivity through private subnets for RDS, DynamoDB via VPC endpoints, S3 via VPC endpoints, and direct service integration for IoT Core and Cognito.

**External Connectivity:** Application Load Balancer with TLS termination for secure external access.

**Internal Communication:** Direct VPC networking within private subnets without service mesh due to stateless architecture.

## ECS-018: Observability Mechanisms

The Valmetal platform uses **Amazon CloudWatch** for comprehensive observability with logging, metrics, and monitoring across all environments.

### Evidence

```bash
# Verify CloudWatch log groups for ECS services
aws logs describe-log-groups --query 'logGroups[?contains(logGroupName, `valmetal-prod`)].logGroupName'
# Output:
[
  "valmetal-prod-backend-api",
  "valmetal-prod-web-client"
]

# Verify Container Insights enabled for application/container metrics
aws ecs describe-clusters --clusters valmetal-prod-backend-api --include SETTINGS --query 'clusters[0].settings'
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
      "Value": "valmetal-prod-backend-api"
    }
  },
  {
    "MetricName": "CPUUtilization", 
    "Dimensions": {
      "Name": "ServiceName",
      "Value": "valmetal-prod-web-client"
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

The Valmetal platform uses **external database services** and **object storage** to meet application storage requirements without persistent container storage.

### Evidence

**Workload:** Farming equipment management application with database operations, time-series data processing, document storage, and stateless web application serving.

**Storage Selection:**
- **Amazon RDS**: PostgreSQL database for relational data
- **Amazon DynamoDB**: NoSQL database for IoT device states  
- **Amazon Timestream**: Time-series database for sensor data
- **Amazon S3**: Object storage for file uploads and documents

**Performance Requirements and Reasoning:**
- **RDS**: Sub-second query response required for equipment records; chosen for automated scaling and backup
- **DynamoDB**: Millisecond latency required for IoT device state management; chosen for automatic scaling
- **Timestream**: Optimized time-series data ingestion required; chosen for analytics query performance  
- **S3**: Standard access latency acceptable for file storage; chosen for cost-effective long-term retention
- **No Container Storage**: Fargate containers remain stateless to simplify deployment and scaling

## ECS-020: EFS Mount Targets in Availability Zones

**Not Applicable** - The Valmetal platform does not use Amazon Elastic File System (EFS) for persistent storage.

## ECS-021: Secure Access to Persistent Storage

The Valmetal platform secures access to persistent storage (RDS, DynamoDB, Timestream, and S3) through **IAM roles and VPC security controls** limiting access to only applications that require it.

### Evidence

**Access Requirements Evaluation:** Only the API service requires direct storage access for database operations, file management, and data processing. Web applications have no direct storage access requirements.

**Security Method:** IAM role-based access control with least privilege principle - API service has IAM task role with storage permissions, while web applications have no storage permissions in their IAM task roles.

**Access Control Configuration:** RDS database deployed in private subnets accessible only via VPC, with dedicated IAM policies for each storage service ensuring service isolation.

## ECS-022: EBS Task Placement Constraints

**Not Applicable** - The Valmetal platform uses **AWS Fargate exclusively**, and EBS volumes are not supported with Fargate launch type.

## ECS-023: Multi-Tenant Workloads

**Not Applicable** - The Valmetal platform is designed as a **single-tenant application**.
