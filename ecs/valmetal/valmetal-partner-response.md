# Valmetal - Partner Response

## Valmetal Partner Response

## Description

Valmetal is an IoT-enabled web platform to help manage farming equipment. It is deployed on Amazon ECS Fargate with IoT integration for real-time equipment monitoring.

The system consists of containerized services including an API backend for user authentication via Cognito and secure file management through S3, alongside web client interfaces. The platform integrates with farming equipment through AWS IoT Core for real-time data collection and processing.

The platform demonstrates production-grade container orchestration with automated CI/CD deployment, comprehensive IAM security controls, IoT data processing pipelines, and scalable infrastructure management.

## ECS-001: Amazon ECS Represents Majority of the Workload

### Response

The complete Valmetal application is containerized and deployed on Amazon ECS.

There are 2 components on ECS:

1. **Frontend (web applications)**
   - **Admin Web App**: Administrative interface for farming equipment management
   - **Client Web App**: Primary client interface for equipment monitoring
   - **Client PWA**: Progressive web application for mobile access

2. **Backend API**
   - Core business logic and API endpoints
   - IoT data processing and equipment management
   - Integration with farming equipment via AWS IoT Core
   - Data pipeline orchestration for real-time monitoring

The backend service runs on Amazon ECS and handles all core business logic including IoT data ingestion, processing, and storage. The service processes requests to serve multiple UI applications and integrates with AWS services including RDS, DynamoDB, Timestream for data storage, and S3 for file management. The platform connects to farming equipment through AWS IoT Core for real-time equipment monitoring and control.

## ECS-002

Infrastructure as code tooling: AWS CDK (TypeScript)
Description of the tools used for automated deployment:

AWS CDK for infrastructure provisioning and ECS service management
GitHub Actions for CI/CD pipeline orchestration
Docker for containerized application builds
Amazon ECR for container image storage and versioning

Description of deployment process and rollback procedures:

Developer commits code changes to feature branch in GitHub (Pull Request)
  - Pull request triggers code review and automated testing pipeline

Upon merge to main branch, GitHub Actions workflow initiates:
  - Automated linting, unit tests, component tests, and end-to-end tests
  - Container images built and tagged with Git commit SHA
  - Images pushed to Amazon ECR
  - CDK deploys infrastructure changes to staging environment (replica of production)
  - Automated health checks validate staging deployment functionality
  - If staging validation passes, production deployment begins with ECS service updates
  - Post-deployment health monitoring with CloudWatch alarms
  - Automatic rollback triggered if health checks fail or monitoring indicates issues

Rollback procedures:

- Automated health checks post-deployment assess service health metrics
- Automatic rollback triggered if health checks fail within monitoring window
- CloudWatch alarms monitored during deployment to detect anomalies
- Previous task definition versions remain available for rollback
- Manual rollback procedures available for emergency situations

Description of source repository that stores infrastructure and task definition files:
- GitHub repository with branch protection policies requiring code reviews. All infrastructure code, ECS task definitions, and application configuration stored under version control.

Version control system used to manage technical artifacts:
- Git with container image tags corresponding to Git commit SHAs, ensuring traceability from code commit to deployed infrastructure.

Description of CI/CD tooling to automate updates to underlying workloads:
- GitHub Actions workflows orchestrate the deployment pipeline, integrating with AWS services to automate ECS task definition updates and service deployments. Zero manual changes permitted in production environment - all modifications flow through the version-controlled Infrastructure deployment pipeline.

## ECS-003: Task Definition Families for Singular Business Purpose

### Response

Each task definition family in the Valmetal architecture serves a distinct, singular business purpose without mixing application logic. This separation ensures clear boundaries between services and facilitates independent scaling, deployment, and management.

### Task Definition Families and Their Singular Business Functions

#### 1. `valmetal-prod-backend-api` - Backend API Services
**Business Purpose**: Core API services and business logic layer
- **Specific Function**: RESTful API endpoints for equipment management operations and IoT data processing
- **Business Logic**: User authentication, data validation, business rules enforcement, IoT data pipeline orchestration
- **External Integrations**: AWS Cognito (user management), S3 (file operations), RDS (equipment records), DynamoDB (IoT device states), Timestream (sensor data), AWS IoT Core (equipment monitoring)
- **No Mixed Logic**: Contains only backend API functionality - no frontend rendering or web serving capabilities

#### 2. `valmetal-prod-web-client` - Frontend Web Application
**Business Purpose**: User interface and web application serving
- **Specific Function**: Server-side rendered web applications using NextJS
- **Business Logic**: UI rendering, client-side interactions, frontend routing for multiple interfaces
- **User Interface**: Complete web interfaces for Admin, Client, and PWA applications for equipment management platform
- **No Mixed Logic**: Contains only frontend presentation logic - no direct database access or business rule processing

## ECS-004: Tagging Strategy and Amazon ECS Managed Tags and Tag Propagation

### Response

The Valmetal platform implements a comprehensive version tracking strategy that maintains strict one-to-one mapping between application code, container images, and task definition revisions. The core versioning strategy is in place, and the current implementation meets AWS Service Delivery tagging requirements.

### Current Tagging Implementation

#### **One-to-One Version Mapping (✅ Implemented)**
Our deployment pipeline ensures complete traceability from source code to running containers:

- **Git Commit SHA ↔ Container Image Tag**: Each deployment uses specific Git commit SHAs embedded in container image tags
- **Container Image ↔ Task Definition**: Task definitions reference specific versioned images from ECR
- **Complete Traceability**: Every running task can be traced back to exact source code version

## ECS-005: IAM Roles and Security

### Response

Each task definition family in the Valmetal platform has dedicated IAM roles following the principle of least privilege. The architecture implements strict role separation where each service has access only to the specific AWS resources and actions required for its designated business function.

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

## ECS-007: Cluster Capacity Management and ECS Capacity Providers

### Response

The Valmetal platform leverages **AWS Fargate Capacity Provider** exclusively for automatic cluster capacity management, eliminating manual scaling operations and ensuring optimal resource allocation. All ECS services are configured with Fargate capacity providers to handle scaling events seamlessly based on task demand.

### Capacity Provider Strategy

#### **Fargate Capacity Provider Implementation**
- **Launch Type**: AWS Fargate exclusively for both API and Web Client services
- **Automatic Scaling**: ECS automatically provisions and scales underlying compute capacity
- **No Manual Intervention**: Zero manual cluster capacity management required
- **Resource Optimization**: Fargate manages capacity allocation based on task resource requirements

## ECS-008: EC2 Spot and Fargate Spot Strategy

### Response

**Status**: Not Applicable - The Valmetal platform does not utilize EC2 Spot Instances or Fargate Spot capacity.

## ECS-009: Multi-Cluster Management

### Response

The Valmetal platform implements a **multi-cluster architecture** with separate ECS clusters for API and Web Client services, providing resource isolation and independent deployment pipelines. All clusters are uniformly provisioned and managed using AWS CDK (TypeScript) for consistent infrastructure-as-code deployment across environments and accounts.

### Multi-Cluster Strategy

#### **Cluster Separation Rationale**
- **Resource Isolation**: Separate clusters prevent resource contention between API backend and web frontend
- **Independent Scaling**: Each cluster can scale independently based on workload characteristics
- **Deployment Independence**: API and Web Client can be deployed separately without affecting each other
- **Security Boundaries**: Isolated clusters provide additional security segmentation

## ECS-010: Container Image Scanning and Security

### Response

The Valmetal platform uses **Amazon ECR** as the image repository with **scan-on-push vulnerability scanning** enabled. All container images undergo security scanning before deployment to ECS clusters.

## ECS-011: Runtime Security Tools for Containerized Workloads

### Response

The Valmetal platform uses **AWS Fargate's built-in runtime security** to protect running containers from malicious syscalls to the underlying host operating system.

## ECS-012: Operating Systems Optimized for Containerized Workloads

### Response

The Valmetal platform uses **AWS Fargate** exclusively, which provides **AWS-managed, ECS-optimized operating systems** without requiring customer management of underlying AMIs or infrastructure.

## ECS-013: Compliance Standards and Frameworks

### Response

**Not Applicable** - The Valmetal platform does not require adherence to specific regulatory compliance standards (SOC, PCI, FedRAMP, HIPAA, etc.).

## ECS-014: ECS-Anywhere for On-Premises and Edge Deployments

### Response

**Not Applicable** - The Valmetal platform uses **AWS Fargate exclusively** and does not deploy on-premises or at edge locations using ECS-Anywhere (ECS-A).

## ECS-015: Ingress Control and Network Traffic Configuration

### Response

The Valmetal platform uses **Application Load Balancer (ALB)** for ingress control with TLS-secured layer 7 traffic.

## ECS-016: IP Exhaustion Management

### Response

**Not Applicable** - The Valmetal platform uses **AWS Fargate exclusively**, and IP exhaustion concerns do not apply to Fargate use cases per validation requirements.

## ECS-017: Service Communication and Connectivity

### Response

The Valmetal platform uses **direct VPC networking** for service communication with AWS services, and **Application Load Balancer** for external connectivity.

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