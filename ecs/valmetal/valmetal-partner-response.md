# Valmetal - Partner Response

## Valmetal Partner Response

## Description

Valmetal is an IoT-enabled web platform to help manage farming equipment. It is deployed on Amazon ECS Fargate with IoT integration for real-time equipment monitoring.

The system consists of containerized services including an API backend for user authentication via Cognito and secure file management through S3, alongside web client interfaces. The platform integrates with farming equipment through AWS IoT Core for real-time data collection and processing.

The platform demonstrates production-grade container orchestration with automated CI/CD deployment, comprehensive IAM security controls, IoT data processing pipelines, and scalable infrastructure management.

## ECS-001: Amazon ECS Represents Majority of the Workload

### Response

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

### Response

**Tagging Strategy:** One-to-one mapping between Git commit SHA, container image tag, and task definition revision ensures version traceability.

**Tag Dimensions:** Environment, Application, Component, Version accurately represent task launches within ECS clusters.

### Evidence

```bash
# Task definition tags
aws ecs describe-task-definition --task-definition valmetal-prod-backend-api:37 --include TAGS --query 'tags'
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

### Response

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

### Response

The Valmetal platform implements precise task sizing based on application requirements, with explicit resource reservations and limits ensuring optimal cluster capacity utilization and predictable scaling behavior. All task definitions specify both CPU and memory at the task level, enabling ECS to make informed scheduling decisions.

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

#### **Resource Reservation and Limits**

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

#### **Complete Task Definition Example**

**API Service Task Definition with Resource Limits:**
```json
{
  "family": "valmetal-prod-backend-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "valmetal-prod-backend-api",
      "image": "497409020770.dkr.ecr.us-east-1.amazonaws.com/valmetal-api-ecr:prod-ede8f4c9a8fba49e904614fc80efd8936c9e41cc",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "valmetal-prod-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "taskRoleArn": "arn:aws:iam::628892762446:role/valmetal-prod-backend-api-AutoScaledFargateServiceT-sIV3LgyVICHP",
  "executionRoleArn": "arn:aws:iam::628892762446:role/valmetal-prod-backend-api-AutoScaledFargateServiceExecutionRo-B7A8C9D4E5F6"
}
```

#### **Resource Sizing Rationale**

**API Service (512 CPU / 1024 MB Memory)**
- **IoT Data Processing**: Sufficient CPU for real-time sensor data ingestion and processing
- **Database Operations**: Memory allocation supports database query processing and connection management
- **Equipment Monitoring**: Resources sized for continuous farming equipment monitoring and alerting

**Web Client (512 CPU / 1024 MB Memory)** 
- **Multi-Interface Serving**: CPU allocation supports NextJS SSR for Admin, Client, and PWA interfaces
- **Static Content**: Memory allocation handles web application assets and rendering requirements
- **User Sessions**: Resource allocation supports concurrent farming equipment management sessions

## ECS-007: Cluster Capacity Management and ECS Capacity Providers

### Response

The Valmetal platform leverages **AWS Fargate Capacity Provider** exclusively for automatic cluster capacity management, eliminating manual scaling operations and ensuring optimal resource allocation. All ECS services are configured with Fargate capacity providers to handle scaling events seamlessly based on task demand.

### Capacity Provider Strategy

#### **Fargate Capacity Provider Implementation**
- **Launch Type**: AWS Fargate exclusively for both API and Web Client services
- **Automatic Scaling**: ECS automatically provisions and scales underlying compute capacity
- **No Manual Intervention**: Zero manual cluster capacity management required
- **Resource Optimization**: Fargate manages capacity allocation based on task resource requirements

### Evidence

#### **Capacity Provider Configuration**

```bash
# Verify Fargate capacity provider configuration
aws ecs describe-clusters \
  --clusters valmetal-prod-backend-api \
  --include CAPACITY_PROVIDERS

# Output:
clusterName: valmetal-prod-backend-api
capacityProviders:
- FARGATE
defaultCapacityProviderStrategy:
- capacityProvider: FARGATE
  weight: 1
  base: 0
```

#### **Auto-Scaling Integration**

```bash
# Verify ECS service auto-scaling configuration
aws ecs describe-services \
  --cluster valmetal-prod-backend-api \
  --services valmetal-prod-backend-api \
  --query 'services[0].{desiredCount:desiredCount,runningCount:runningCount,pendingCount:pendingCount}'

# Output:
{
  "desiredCount": 2,
  "runningCount": 2, 
  "pendingCount": 0
}
```

**Scaling Strategy:**
- **Target Tracking**: CPU and memory utilization targets for automatic scaling
- **IoT Load Balancing**: Scaling triggers based on farming equipment data processing load
- **Cost Efficiency**: Pay only for resources consumed by running tasks

This Fargate-based capacity provider strategy ensures that cluster capacity management is fully automated, cost-effective, and aligned with AWS best practices for serverless container deployments.

## ECS-008: EC2 Spot and Fargate Spot Strategy

### Response

**Status**: Not Applicable - The Valmetal platform does not utilize EC2 Spot Instances or Fargate Spot capacity.

The Valmetal platform exclusively uses **standard AWS Fargate** launch type for all ECS services to ensure consistent availability and predictable performance for the farming equipment management platform. Spot capacity is not utilized due to the mission-critical nature of IoT data processing and real-time equipment monitoring.

### Evidence

#### **Standard Fargate Only - No Spot Usage**
```bash
# Verify no spot capacity in use across both services
aws ecs describe-services \
  --cluster valmetal-prod-backend-api \
  --services valmetal-prod-backend-api \
  --query 'services[0].{launchType:launchType,capacityProviderStrategy:capacityProviderStrategy}'

# Output confirms standard Fargate:
capacityProviderStrategy: null
launchType: FARGATE
```

```bash
# Verify no spot fleet requests in use
aws ec2 describe-spot-fleet-requests

# Output
SpotFleetRequestConfigs: []
```

The current Valmetal platform architecture prioritizes **reliability over cost optimization** for its core farming equipment management and IoT processing functions, making standard Fargate the appropriate choice.

## ECS-009: Multi-Cluster Management

### Response

The Valmetal platform uses **AWS CDK (TypeScript)** for multi-cluster management with consistent configuration across environments.

### Evidence

#### **Infrastructure as Code Tool for Multi-Cluster Deployment**

**AWS CDK (TypeScript)** is used to define and deploy all Amazon ECS clusters with consistent configuration. The same stacks with appropriate parameters are used for all environments (development, staging, production).

#### **Multi-Cluster Management Tool**

**CDK-Based Multi-Cluster Management:** AWS CDK manages multiple ECS clusters with consistent configuration across environments.

#### **Multi-Account Environment Mapping**

**Account Structure:**

- **Development Account**: `410308623475` - Isolated development and testing clusters
- **Staging Account**: `475448362599` - Pre-production validation with production-like configuration (replica of production)  
- **Production Account**: `628892762446` - Live farming equipment management clusters
- **Shared Account**: `497409020770` - ECR repositories
- **Cross-Account Access**: CDK deployment roles is granted to Github CI/CD pipeline based on which environment is being deployed to.

## ECS-010: Container Image Scanning and Security

### Response

The Valmetal platform uses **Amazon ECR** as the image repository with **scan-on-push vulnerability scanning** enabled. All container images undergo security scanning before deployment to ECS clusters.

### Evidence

#### **Image Repository**

**Amazon ECR Repository Configuration:**
```bash
# Verify ECR repository with scan-on-push configuration
aws ecr describe-repositories --repository-names valmetal-api-ecr --query 'repositories[0].{repositoryName:repositoryName,scanOnPush:imageScanningConfiguration.scanOnPush,tagMutability:imageTagMutability}'

# Output:
{
  "repositoryName": "valmetal-api-ecr",
  "scanOnPush": true,
  "tagMutability": "IMMUTABLE"
}
```

#### **ECR Repository Policies and Image Version Consistency**

**ECR Repository Policies Allow ECS Task Pull:**
- ECS task execution roles have `ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`, and `ecr:BatchCheckLayerAvailability` permissions
- Repository policies restrict access to authorized ECS task execution roles only

**Image Versions Match Task Definitions:**
- **API Task Definition**: `497409020770.dkr.ecr.us-east-1.amazonaws.com/valmetal-api-ecr:prod-ede8f4c9a8fba49e904614fc80efd8936c9e41cc`
- **Web Client Task Definition**: `497409020770.dkr.ecr.us-east-1.amazonaws.com/valmetal-web-client-ecr:prod-ede8f4c9a8fba49e904614fc80efd8936c9e41cc`
- Git commit SHA tags ensure one-to-one mapping between code versions and container images

#### **ECR Monitoring and Observability**

**CloudWatch Integration:**
- ECR image pulls logged to CloudWatch for monitoring
- Vulnerability scan results integrated with alerting for HIGH/CRITICAL findings
- ECR repository usage monitored to ensure expected container images are stored and pulled

#### **Image Version Consistency Verification**
```bash
# Verify current task definition uses specific versioned image (not :latest)
aws ecs describe-task-definition --task-definition valmetal-prod-backend-api:37 --query 'taskDefinition.containerDefinitions[0].image'

# Output: 
"497409020770.dkr.ecr.us-east-1.amazonaws.com/valmetal-api-ecr:prod-ede8f4c9a8fba49e904614fc80efd8936c9e41cc"

# Verify web client image consistency  
aws ecs describe-task-definition --task-definition valmetal-prod-web-client:20 --query 'taskDefinition.containerDefinitions[0].image'

# Output:
"497409020770.dkr.ecr.us-east-1.amazonaws.com/valmetal-web-client-ecr:prod-ede8f4c9a8fba49e904614fc80efd8936c9e41cc"
```

## ECS-011: Runtime Security Tools for Containerized Workloads

### Response

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
aws ecs describe-services \
  --cluster valmetal-prod-backend-api \
  --services valmetal-prod-backend-api \
  --query 'services[0].{launchType:launchType,platformVersion:platformVersion}'

# Output:
launchType: FARGATE
platformVersion: 1.4.0
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

The Valmetal platform uses **AWS Fargate** exclusively, which provides **AWS-managed, ECS-optimized operating systems** without requiring customer management of underlying AMIs or infrastructure.

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
  --cluster valmetal-prod-backend-api \
  --services valmetal-prod-backend-api \
  --query 'services[0].{launchType:launchType,platformVersion:platformVersion}'

# Output:
launchType: FARGATE
platformVersion: 1.4.0
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

**Not Applicable** - The Valmetal platform does not require adherence to specific regulatory compliance standards (SOC, PCI, FedRAMP, HIPAA, etc.).

## ECS-014: ECS-Anywhere for On-Premises and Edge Deployments

### Response

**Not Applicable** - The Valmetal platform uses **AWS Fargate exclusively**, and does not deploy on-premises or at edge locations using ECS-Anywhere (ECS-A).

## ECS-015: Ingress Control and Network Traffic Configuration

### Response

The Valmetal platform uses **Application Load Balancer (ALB)** for ingress control with TLS-secured layer 7 traffic.

### Evidence

#### **Ingress Controller and Infrastructure**

**Ingress Controller**: AWS Application Load Balancer (ALB) with HTTPS/TLS termination

```bash
# Verify VPC configuration for ECS services
aws ecs describe-services \
  --cluster valmetal-prod-backend-api \
  --services valmetal-prod-backend-api \
  --query 'services[0].networkConfiguration.awsvpcConfiguration.{subnets:subnets,assignPublicIp:assignPublicIp}'

# Output shows private subnet deployment:
assignPublicIp: DISABLED
subnets:
- subnet-0891bef2c77a8e234
- subnet-0d9367f4e5cf291ab
```

**Infrastructure**: Private subnets for ECS tasks, ALB in public subnets, NAT Gateways for outbound access

#### **Network Modes and Load Balancing Configuration**

```bash
# Verify awsvpc network mode for Fargate
aws ecs describe-task-definition --task-definition valmetal-prod-backend-api:37 --query 'taskDefinition.{networkMode:networkMode,requiresCompatibilities:requiresCompatibilities}'

# Output confirms Fargate networking:
{
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"]
}

# Verify service network configuration
aws ecs describe-services --cluster valmetal-prod-web-client --services valmetal-prod-web-client --query 'services[0].networkConfiguration.awsvpcConfiguration'

# Output shows private subnet placement:
{
  "assignPublicIp": "DISABLED",
  "securityGroups": ["sg-0a343e12863986b6a"],
  "subnets": ["subnet-06fc4817ddefe2868", "subnet-088d8ad6d6d617c95"]
}
```

**Configuration**: awsvpc network mode with IP-based ALB target groups for direct task communication

## ECS-016: IP Exhaustion Management

### Response

**Not Applicable** - The Valmetal platform uses **AWS Fargate exclusively**, and IP exhaustion concerns do not apply to Fargate use cases per validation requirements.

## ECS-017: Service Communication and Connectivity

### Response

The Valmetal platform uses **direct VPC networking** for service communication with AWS services, and **Application Load Balancer** for external connectivity.

### Evidence

#### **Service Communication Architecture**

**AWS Services Integration:**
- **RDS Database**: Direct VPC connectivity through private subnets
- **DynamoDB**: VPC endpoints for secure NoSQL database access
- **Timestream**: Direct AWS service integration for time-series data
- **S3**: VPC endpoints for secure object storage access
- **AWS IoT Core**: Direct service integration for device communication
- **Cognito**: Direct AWS service integration for authentication

**External Connectivity:**
- **Application Load Balancer**: TLS-secured ingress for web applications
- **API Gateway**: Not used - direct ALB integration preferred for simplicity
- **Internal Communication**: No service mesh required due to stateless architecture

#### **Network Configuration**

```bash
# Verify VPC networking configuration
aws ecs describe-services \
  --cluster valmetal-prod-backend-api \
  --services valmetal-prod-backend-api \
  --query 'services[0].networkConfiguration.awsvpcConfiguration.{subnets:subnets,assignPublicIp:assignPublicIp}'

# Output shows private networking:
assignPublicIp: DISABLED
subnets:
- subnet-0891bef2c77a8e234
- subnet-0d9367f4e5cf291ab
```

**Communication Patterns:**
- **Service-to-Service**: Direct VPC networking within private subnets
- **Service-to-AWS**: VPC endpoints and direct service integration
- **External-to-Service**: ALB with TLS termination and target groups
- **IoT Devices**: AWS IoT Core with device certificates and policies

#### **IoT Integration and Farming Equipment Connectivity**

**IoT Device Communication:**
- **Device Certificates**: X.509 certificates for secure device authentication
- **Device Policies**: Custom policies for device authorization and access control
- **Device Shadows**: Virtual device representations for efficient data processing
- **MQTT Protocol**: Message Queue Telemetry Transport for low-bandwidth device communication

**Farming Equipment Connectivity:**
- **Real-Time Data Processing**: Timestream database for efficient sensor data processing
- **Equipment Monitoring**: Real-time monitoring and alerting for equipment performance
- **Predictive Maintenance**: Machine learning models for predictive maintenance scheduling
- **Automated Workflows**: Automated workflows for equipment management and maintenance

## ECS-018: Observability Mechanisms

### Response

The Valmetal platform uses **Amazon CloudWatch** for comprehensive observability with logging, metrics, and monitoring across all environments.

### Evidence

#### **Observability Mechanism**

**CloudWatch Observability:**
- **Application/Container Metrics**: CloudWatch Container Insights for task-level metrics
- **Infrastructure Metrics**: ECS cluster and service metrics via CloudWatch
- **Scaling Events**: Auto-scaling metrics and logs captured during scaling operations  
- **Multi-Environment**: CloudWatch monitoring across dev, staging, and prod accounts
- **IoT Monitoring**: CloudWatch metrics for AWS IoT Core device connectivity and data processing
- **Distributed Tracing**: Not implemented - given the streamlined nature of the system, X-Ray distributed tracing is not used. CloudWatch logs provide sufficient debugging capabilities.

#### **ECS Service CloudWatch Logs**
```bash
# Verify CloudWatch log groups for ECS services
aws logs describe-log-groups --query 'logGroups[?contains(logGroupName, `valmetal-prod`)].logGroupName'

# ECS Service Log Groups:
- valmetal-prod-backend-api
- valmetal-prod-web-client
```

#### **IoT-Specific Monitoring and Observability**

TODO: Is IoT monitoring required in this document?

**AWS IoT Core Monitoring:**
```bash
# Monitor IoT device connectivity and message processing
aws iot describe-thing-group --thing-group-name valmetal-farming-equipment

# Output shows device group status:
thingGroupName: valmetal-farming-equipment
thingGroupProperties:
  description: Farming equipment IoT devices for Valmetal platform
  attributePayload:
    attributes:
      deviceType: farming-equipment
      environment: production
```

**CloudWatch Metrics for IoT Integration:**
- **Device Connectivity**: Connection status and device heartbeat monitoring
- **Message Throughput**: MQTT message rates and processing latency
- **Data Processing**: Timestream ingestion rates and query performance
- **Error Rates**: Failed device connections and message processing errors
- **Equipment Status**: Real-time farming equipment operational status

#### **Multi-Environment and Scaling Monitoring**

**Container-Level Observability:**

TODO: Is this required in this document? Does it validate the requirements?```bash
# Verify CloudWatch Container Insights configuration
aws ecs describe-clusters \
  --clusters valmetal-prod-backend-api \
  --include INSIGHTS

# Output shows Container Insights enabled:
clusterName: valmetal-prod-backend-api
settings:
- name: containerInsights
  value: enabled
```

**Environmental Monitoring:**
- **Development Environment**: CloudWatch logs and metrics for testing IoT scenarios
- **Staging Environment**: Full production-like monitoring for validation
- **Production Environment**: Complete observability with real farming equipment data
- **Cross-Account Visibility**: Centralized monitoring dashboard across all environments

**Scaling Event Monitoring:**
- **ECS Service Scaling**: Auto-scaling triggers and capacity changes logged
- **Resource Utilization**: CPU, memory, and network metrics for scaling decisions
- **IoT Load Balancing**: Device connection distribution and processing load monitoring
- **Performance Optimization**: Response time and throughput optimization tracking

## ECS-019: Storage Options Selection

### Response

The Valmetal platform uses **external database services** and **object storage** to meet application storage requirements without persistent container storage.

### Evidence

#### **Workload and Storage Selection**

**Farming Equipment Management Application Workload:**
- **Database Operations**: Equipment records, maintenance schedules, IoT device states, reporting queries
- **Time-Series Data**: Real-time equipment sensor data, performance metrics, operational analytics
- **Document Storage**: Equipment manuals, maintenance reports, configuration files
- **Web Application**: Stateless application serving and API processing for multiple interfaces

**Storage Solutions:**
- **Amazon RDS**: PostgreSQL database for relational data and equipment records
- **Amazon DynamoDB**: NoSQL database for IoT device states and real-time data processing
- **Amazon Timestream**: Time-series database for sensor data and equipment performance metrics
- **Amazon S3**: Object storage for file uploads, documents, and data archival
- **No Container Storage**: Fargate containers remain stateless without persistent volumes

**Performance Requirements and Reasoning:**
- **RDS**: Sub-second query response for equipment records, automated scaling and backup
- **DynamoDB**: Millisecond latency for IoT device state management, automatic scaling
- **Timestream**: Optimized for time-series data ingestion and analytics queries
- **S3**: Standard access latency acceptable for file storage, cost-effective for long-term retention
- **Stateless Design**: No container-level storage needed, simplifies deployment and scaling

## ECS-020: EFS Mount Targets in Availability Zones

### Response

**Not Applicable** - The Valmetal platform does not use Amazon Elastic File System (EFS) for persistent storage.

## ECS-021: Secure Access to Persistent Storage

### Response

The Valmetal platform secures access to persistent storage (RDS, DynamoDB, Timestream, and S3) through **IAM roles and VPC security controls** limiting access to only applications that require it.

### Evidence

#### **Access Requirements Evaluation**

**Storage Access Analysis:**
- **RDS Database**: Only API service requires database access for equipment records and relational data
- **DynamoDB**: Only API service requires NoSQL access for IoT device states and real-time processing
- **Timestream**: Only API service requires time-series database access for sensor data analytics
- **S3 File Storage**: Only API service requires file upload/download capabilities for documents and archival
- **Web Applications**: No direct storage access required (Admin, Client, PWA apps)

#### **Security Method**

**IAM Role-Based Access Control:**
- **API Service**: IAM task role with RDS, DynamoDB, Timestream, and S3 permissions
- **Web Applications**: No storage permissions in IAM task roles
- **VPC Security**: RDS database in private subnets, accessible only via VPC
- **Service Isolation**: Each storage service accessed through dedicated IAM policies with least privilege

## ECS-022: EBS Task Placement Constraints

### Response

**Not Applicable** - The Valmetal platform uses **AWS Fargate exclusively**, and EBS volumes are not supported with Fargate launch type.

## ECS-023: Multi-Tenant Workloads

### Response

**Not Applicable** - The Valmetal platform is designed as a **single-tenant application**. There is only one production deployment that manages multiple farming equipment. There is application-level logic to allow Farmers use the platform to manage their own equipment.