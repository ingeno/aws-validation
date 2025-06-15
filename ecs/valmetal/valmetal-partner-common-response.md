## DOC-001: Architecture Diagram with Scalability and High Availability

The Valmetal platform architecture is designed with scalability and high availability using AWS Fargate, Application Load Balancer, and multi-AZ deployment across multiple AWS services.

### Evidence

**Architecture Diagram:** See included diagram - Complete farm-to-cloud architecture showing edge computing (PLC with Node-RED, Agent), IoT data ingestion (IoT Core, Device Shadow), processing pipeline (ECS Fargate, Lambda, Step Functions), and storage services (RDS multi-AZ, DynamoDB, Timestream, S3).

**Failure Recovery:** Major solution elements maintain availability through multi-AZ RDS deployment with automated backups, ECS service auto-restart for failed tasks, IoT Core device shadow for edge resilience, and S3 cross-region replication for critical data.

**Automatic Scaling:** ECS Fargate services scale automatically based on CPU/memory utilization, DynamoDB scales on-demand for IoT device states, Timestream provides automatic scaling for sensor data, and Application Load Balancer distributes traffic across multiple availability zones as demand changes.

## ACCT-001: Secure AWS Account Governance Best Practice

Ingeno implements comprehensive secure AWS account governance through documented procedures that address all four AWS Service Delivery Program requirements: strict root account usage policies, mandatory MFA implementation, corporate contact information management, and comprehensive CloudTrail logging with dedicated log protection.

### Evidence

**1. Security Engagement SOP Documentation:**
- **Primary Document:** `ingeno-root-account-security-summary.md` - Comprehensive root account security controls covering:
  - Root account usage policy (emergency access only, maximum 3 designated personnel)
  - MFA implementation (Google Authenticator with 1Password integration)
  - Corporate contact information standards (role-based emails, corporate phone numbers)
  - CloudTrail configuration with multi-region coverage and log protection
  - **Supporting Documentation:** Ingeno - AWS Landing Zone Provisioning.pdf - Complete SOP with step-by-step implementation procedures

**3. Compliance Verification:**
- Root account access restricted to emergency use with maximum 3 designated administrators
- MFA enabled on all accounts using Google Authenticator with secure 1Password storage
- Corporate contact information configured with security contact `aws.valmetal.audit@ingeno.ca`
- CloudTrail enabled across all Control Tower regions with centralized log protection and KMS encryption

## ACCT-002: Define Identity Security Best Practice on How to Access Customer Environment by Leveraging IAM

Ingeno implements comprehensive identity security best practices for accessing customer AWS environments through standardized IAM approaches that eliminate permanent credentials, enforce least privilege access, and integrate with enterprise identity systems. Our approach covers both AWS Management Console access and programmatic access using temporary credentials exclusively.

### Evidence

**1. Security Engagement SOP Documentation:**
- **Primary Document:** `aws-account-access-summary.md` - Comprehensive access management procedures covering:
  - Standard approach to customer AWS account access (Console via SAML federation, Programmatic via temporary credentials)
  - Temporary credential usage through IAM roles and AWS STS
  - Enterprise identity integration with Google Workspace and customer identity providers
  - IAM best practices implementation (least privilege, wildcard avoidance, individual accountability)
- **Supporting Documentation:** [AWS Landing Zone Provisioning Guide](https://docs.google.com/document/d/1zXsGmOj8kVbkEh-kJNkz5WJsaoq_5SmgHeNPCf-d_5M/edit) - Complete SOP with step-by-step implementation procedures

**2. Customer Implementation - Standard Architecture:**

**Console Access Implementation:**
- SAML federation through Google Workspace with AWS IAM Identity Center integration
- Custom portal URLs for secure access with 8-hour maximum session duration
- Mandatory MFA enforcement using Google Authenticator for all users
- Role-based access to appropriate AWS accounts based on group membership

**Programmatic Access Implementation:**
- Exclusive use of temporary credentials through AWS CLI assume role profiles
- No permanent access keys distributed or stored anywhere in the system
- MFA protection required for all credential generation via AWS STS
- Integration with corporate identity provider for seamless authentication

**Temporary Credential Usage:**
- Root account access limited to emergency use only with MFA protection
- All normal operations conducted through federated access via IAM roles
- CI/CD pipelines use GitHub OIDC integration with minimal permission roles
- Just-in-time access provisioning with no standing privileges maintained

**Enterprise Identity Integration:**
- Flexible support for customer SAML/OIDC identity providers
- Customer maintains control over user lifecycle and permission management
- Established trust relationships between customer identity providers and AWS
- Hybrid integration capabilities with customer Active Directory systems

**3. IAM Best Practices Implementation:**
- **Least Privilege Principle:** Role-based access with environment-specific restrictions across Development, Staging, and Production scopes
- **Wildcard Avoidance:** Specific denial policies prevent broad permission grants and enforce granular access controls
- **Individual Accountability:** Every team member uses dedicated credentials through Google Workspace integration with unique @ingeno.ca accounts
- **Service Control Policies:** Organizational controls prevent local IAM user creation and enforce centralized identity management
- **Access Architecture:** Standardized permission set mapping across organizational units with quarterly access reviews

**4. Compliance Controls:**
- No permanent access keys distributed or stored across any customer environments
- Universal MFA enforcement with Google Authenticator integration and no bypass capabilities
- CloudTrail logging across all regions providing complete audit trail for all access activities
- Centralized identity management through AWS IAM Identity Center eliminating local account creation
- Regular access certification and privilege reviews conducted quarterly with documented remediation

## OPE-001: Define, Monitor and Analyze Customer Workload Health KPIs

Ingeno implements comprehensive workload health monitoring through standardized CloudWatch dashboards, automated alerting systems, and structured application logging to ensure optimal system performance and rapid issue detection across all IoT platform components.

Our monitoring strategy follows the **Ingeno Monitoring and Observability Framework** (documented in `ingeno-monitoring-summary.md`) which establishes standardized procedures for workload health KPIs, three-tier alerting systems, and infrastructure-as-code monitoring deployment using AWS CDK.

### Evidence

**1. Standardized Workload Health KPI Framework:**

*Reference: See `ingeno-monitoring-summary.md` for complete framework documentation.*

## OPE-002: Define a Customer Runbook/Playbook to Guide Operational Tasks

Ingeno has developed a comprehensive operational runbook that documents routine activities and provides systematic issue resolution procedures directly addressing the workload health KPIs defined in OPE-001. The runbook establishes standardized operational practices for monitoring, troubleshooting, and maintaining IoT platform workloads across ECS, DynamoDB, Timestream, and Lambda services.

### Evidence

**Standardized Operational Runbook:**

*Reference: See `ingeno-operational-runbook.md` for complete runbook documentation.*

The operational runbook covers:
- **Health Check Routines:** Systematic verification procedures for CloudWatch dashboards and IoT-specific metrics monitoring
- **Alert Response Procedures:** Structured response workflows for Critical, Warning, and Performance alerts based on OPE-001 KPIs
- **Troubleshooting Scenarios:** Detailed diagnostic and resolution steps for ECS service failures, database performance issues, DynamoDB throttling, and Timestream ingestion problems
- **Incident Resolution Workflow:** Classification procedures, escalation paths, and communication templates for IoT platform incidents
- **Routine Maintenance Procedures:** Security patching and disaster recovery testing protocols for multi-service IoT architecture

## OPE-003: Use Consistent Processes to Assess Deployment Readiness

Ingeno employs a fully automated CI/CD pipeline that ensures deployment readiness through comprehensive testing and validation processes. Rather than manual checklists, our approach leverages an automated checklist with automated testing, peer review, and staged deployment processes to guarantee code quality and system reliability before production deployment across the IoT platform's multi-service architecture.

### Evidence

**Automated CI/CD Pipeline Process:**

Our deployment readiness assessment includes:
- **Automated Code Quality:** Linting, security scanning, and code quality checks executed on every commit
- **Comprehensive Testing:** Unit tests, integration tests, and IoT-specific end-to-end testing automatically executed in CI pipeline
- **Peer Review Process:** All code changes require GitHub pull request approval from senior developers before merge
- **Staged Deployment:** Code deployed first to testing environment (production replica) for validation across ECS, Lambda, DynamoDB, and Timestream services
- **Zero-Downtime Production Deployment:** ECS rolling deployments with health checks ensure seamless production updates without IoT data ingestion interruption
- **Automated Rollback:** Pipeline automatically reverts deployments if health checks or monitoring thresholds indicate issues with any IoT platform component

This automated approach eliminates manual checklist errors while ensuring consistent, reliable deployments across all customer IoT environments.

## NETSEC-001: Define Security Best Practices for Virtual Private Cloud and Network Security

Ingeno implements comprehensive VPC network security using standardized AWS CDK infrastructure that enforces defense-in-depth architecture with multi-tier network segmentation, granular security group controls, and AWS native security services integration.

### Evidence

Ingeno has developed reusable CDK constructs to implement network security best practices in a reliable and repeatable way. 

### VPC Construct

A two-tier VPC construct implements a two-tier architecture with the following key features:

- Network Configuration:
  - Creates public subnets for internet-facing resources
  - Creates private subnets with egress (for resources that need outbound internet but no inbound)
  - Spans exactly multiple availability zones for high availability
  - NAT Gateway Strategy:
    - Production mode (prod: true): Creates one NAT gateway per AZ (2 total) for high availability
    - Non-production mode: Creates only 1 NAT gateway to save costs
  - VPC Flow Logs:
    - Automatically configures VPC flow logs to capture rejected traffic
    - Creates a dedicated CloudWatch log group with infinite retention
    - Sets up proper IAM roles and policies for flow log delivery
  - Network ACLs: Using default NACL configuration (allows all traffic) - security controls implemented primarily through security group rules

This construct is designed to provide a cost-effective, secure, and highly available network foundation that can be easily reused across different AWS stacks and environments.

### Security Groups Constructs

Security groups are used to control traffic flow between subnets and to the internet and between relevant AWS resources. We have reusable constructs to implement security groups for the interoperability between ECS services and database resources:

- Database is deployed in private subnets
- ECS services are deployed in private subnets
- ECS services can access database using security group rules
- Database can not be accessed from the internet
- ECS services can access the internet using NAT gateway
- A bastion host is deployed in public subnets to access private subnets 
  - Developers can connect to the bastion host using session manager to access private subnets
  - SSH tunneling is used between the bastion and database to troubleshoot database issues or to perform database maintenance

## NETSEC-002: Define Data Encryption Policy for Data at Rest and in Transit

Ingeno enforces comprehensive data encryption for all customer environments using AWS native encryption services and industry-standard protocols. Our standardized encryption policy ensures all data is protected both at rest and in transit with centralized key management through AWS KMS.

### Evidence

**Internet-Facing Endpoints Encryption:** 
- Public endpoints (Load balancers for UI and API) use HTTPS
- AWS Certificate Manager provides SSL/TLS certificates for HTTPS listeners
- Automatic redirection ensures all traffic uses encrypted connections

**External API Communication Encryption:**
- All external API calls use HTTPS/TLS (mainly to invoke other AWS services)
- AWS SDK Encryption: All AWS service communications automatically encrypted in transit
- Certificate Validation: Enforced certificate validation for all outbound connections

**Data at Rest Encryption:**
- RDS Database: PostgreSQL database encrypted at rest using customer-managed KMS key (e.g. for production : `arn:aws:kms:us-east-1:628892762446:key/95c863e4-8572-4e22-a4eb-0a559f25db34`) 
- DynamoDB Tables: All IoT data tables encrypted using AWS managed keys with AES-256 encryption
- Timestream Database: Time-series data automatically encrypted at rest using AWS managed keys
- CloudWatch Logs: Application logs and VPC flow logs encrypted using KMS keys
- ECS Fargate: Container runtime and ephemeral storage encrypted using AWS Fargate platform encryption

**Key Management Implementation:**
- AWS KMS Integration: Centralized key management with customer-managed keys for production databases
- Key Rotation: Automatic annual rotation for AWS managed keys, scheduled rotation for customer-managed keys
- Access Control: KMS key policies restrict access to authorized IAM roles and services only
- Audit Logging: All key usage tracked through CloudTrail for security compliance

## REL-001: Automate Deployment and Leverage Infrastructure-as-Code Tools

Ingeno implements fully automated deployment using GitHub Actions CI/CD pipelines with AWS CDK (Cloud Development Kit) for infrastructure-as-code. All production infrastructure is deployed programmatically without manual AWS Management Console operations.

### Evidence

**1. Automated Deployment Infrastructure:**

All Valmetal production resources are deployed using automated CI/CD with the following CloudFormation stacks:

- valmetal-prod-cloudwatch-alarms
- valmetal-prod-feed-sequence
- valmetal-prod-feature-flags
- valmetal-prod-web-client
- valmetal-prod-billing
- valmetal-prod-alarm
- valmetal-prod-web-admin
- valmetal-prod-backend-api
- valmetal-prod-common-http
- valmetal-prod-bastion
- valmetal-prod-database
- valmetal-prod-auth
- valmetal-prod-logging
- valmetal-prod-common-infrastructure
- valmetal-prod-metrics
- valmetal-prod-iot
- valmetal-prod-provisioning
- valmetal-prod-agent-provider
- valmetal-prod-iot-prerequisites
- valmetal-prod-api
- valmetal-prod-plc-logger
- valmetal-prod-github

**2. Infrastructure-as-Code Example Template:**

*Reference: See `valmetal-prod-api-cloudformation-template.yaml` for complete CDK-generated CloudFormation template.*

**3. GitHub Actions CI/CD Pipeline:**

- **Automated Testing:** All code changes trigger automated linting, unit tests, and integration tests
- **CDK Synthesis:** CloudFormation templates automatically generated from CDK TypeScript code
- **Staged Deployment:** Changes deployed to testing environments before production
- **Zero-Touch Production:** Production deployments triggered only after successful testing and peer review

**4. No Manual Console Operations:**

Manual infrastructure changes are prohibited via AWS Management Console or AWS CLI. Production deployments exclusively use:
- GitHub Actions runners with Github OIDC with minimal permissions
- CDK CLI for CloudFormation stack deployment and updates

## REL-002: Plan for Disaster Recovery and Recommend Recovery Time Objective (RTO) and Recovery Point Objective (RPO)

Customer did not allocate budget for fully automated disaster recovery mechanisms but we implement foundational resilience capabilities and provide clear recovery processes.

### Evidence

**1. Workload Resilience Guidance:**

**RTO & RPO Targets:**
- **Recommended RTO:** ~8 hours for complete workload recovery in alternate region
- **Recommended RPO:** ~15 minutes for database recovery using automated backups
- **Customer Communication:** RTO/RPO targets discussed during architecture review sessions

**Recovery Process for Core Components:**
- **Database Recovery:** Automated RDS backups with point-in-time recovery enable restoration to any point within the backup retention period
- **Application Recovery:** Containerized ECS services can be redeployed in any AWS region using existing CDK infrastructure definitions
- **Data Recovery:** S3 Cross-Region Replication ensures critical application data is automatically replicated to secondary regions
- **Infrastructure Recovery:** Complete infrastructure can be recreated in alternate regions by modifying CDK deployment parameters (region, VPC CIDR ranges)

**2. Valmetal IoT Platform Resilience Implementation:**

**Automated Backup Mechanisms:**
- **RDS Database:** Automated daily backups with 35-day retention period and continuous transaction log backups for point-in-time recovery
- **DynamoDB Tables:** Point-in-time recovery enabled for all IoT data tables providing restore capability for the last 35 days
- **Application Code:** Source code versioned in GitHub with automated CI/CD pipeline enabling rapid redeployment

## COST-001: Develop Total Cost of Ownership Analysis or Cost Modeling

Ingeno conducts comprehensive TCO analysis using AWS Pricing Calculator and right-sizing methodology to provide customers with accurate cost projections and business value quantification.

### Evidence

**1. Cost Analysis Methodology:**

**Cost Estimation Inputs:**
- Current resource utilization metrics (CPU, memory, storage, network)
- Historical usage patterns and growth projections
- Service pricing models (on-demand, reserved instances, pay-per-use)

**2. Cost Model Implementation:**

**Current Architecture Costs:**
- ECS Fargate: Right-sized to minimal load (~$XX/month)
- RDS Database: Small instance with automated backups (~$XX/month)  
- Supporting Services: DynamoDB pay-per-request, CloudWatch, S3 (~$XX/month)
- **Total Monthly Cost:** ~$XXX for current minimal load

**Business Value Analysis:**
- Auto-scaling ensures costs scale with actual usage (no over-provisioning)
- Managed services eliminate server maintenance and security patching costs

*Reference: AWS Pricing Calculator estimate provided as supporting documentation.*

