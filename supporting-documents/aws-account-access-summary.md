# AWS Account Access Management Summary
*Based on AWS Landing Zone Provisioning Guide*

## Standard Approach to Customer AWS Account Access

### AWS Management Console Access
**Identity Provider Integration:**
- **Primary Method:** SAML federation through Google Workspace SSO
- **AWS Integration:** AWS IAM Identity Center (formerly AWS SSO)
- **Portal Configuration:** Custom portal URLs (`<account-name>.awsapps.com/start`)
- **Session Management:** 8-hour maximum session duration with automatic timeout

**Access Flow:**
1. Users authenticate through Google Workspace with MFA
2. SAML assertion provides temporary credentials via IAM Identity Center
3. Role-based access to appropriate AWS accounts based on group membership
4. All console access uses temporary, session-based credentials

### Programmatic Access (CLI/API)
**Credential Method:**
- **No Permanent Access Keys:** All programmatic access uses temporary credentials
- **AWS CLI Integration:** Assume role capabilities through federated identity
- **MFA Protection:** Required for all credential generation
- **Session Duration:** Configurable based on security requirements

**Implementation:**
- Users configure AWS CLI with assume role profiles
- Temporary credentials generated via AWS STS
- Integration with corporate identity provider for authentication
- No long-term access keys stored or distributed

### Temporary Credentials and IAM Roles

**Mandatory Temporary Credential Usage:**
- **Root Account Access:** Emergency use only with MFA protection
- **Federated Access:** All normal operations use temporary credentials via IAM roles
- **CI/CD Pipelines:** GitHub OIDC integration with minimal permission roles
- **No Standing Privileges:** Just-in-time access provisioning

**IAM Role Strategy:**
```
Management Account → IAM Identity Center → Permission Sets → Cross-Account Roles
```

### Enterprise Identity Integration

**Customer Identity Provider Support:**
- **Flexible Integration:** Support for customer's existing SAML/OIDC providers
- **Hybrid Scenarios:** Ability to integrate with customer's Active Directory or identity systems
- **Trust Relationships:** Established between customer identity providers and AWS
- **Access Delegation:** Customers maintain control over user lifecycle and permissions

**When Customer Manages Identity:**
- Customer configures their identity provider as trusted source
- Customer maps their groups to AWS permission sets
- Customer maintains user provisioning and access reviews
- Ingeno operates within customer-defined permission boundaries

## IAM Best Practices Implementation

### Principle of Least Privilege

**Permission Set Design:**
- **Role-Based Access:** Developers, Architects, ProdOps, BillingAdmins groups
- **Account Scope Restrictions:** Environment-specific access (dev, staging, prod)
- **Service-Specific Permissions:** Granular permissions based on job function
- **Regular Access Reviews:** Quarterly certification of all access

**Wildcard Avoidance:**
```json
{
  "Effect": "Deny",
  "Action": [
    "iam:CreateUser",
    "iam:CreateGroup", 
    "iam:CreateRole"
  ],
  "Resource": "*"
}
```
*Example: Specific denial actions rather than broad wildcards*

### Individual Accountability

**Dedicated Credentials Policy:**
- **No Shared Accounts:** Every individual has unique identity
- **Traceability:** All actions logged to specific user identities
- **Google Workspace Integration:** Individual @ingeno.ca accounts
- **MFA Enforcement:** Required for all users without exception

**Service Control Policies:**
- **Prevent IAM User Creation:** SCP blocks local IAM user/group creation
- **Enforce Identity Center:** All access must go through centralized identity
- **Audit Trail:** CloudTrail logging across all regions and accounts

### Access Control Architecture

**Organizational Structure:**
```
Root Organization
├── Core OU (Management, Audit, Log Archive)
├── Shared OU (Shared Infrastructure)
├── Workloads_Test OU (Dev, Staging)
└── Workloads_Prod OU (Production)
```

**Permission Set Mapping:**
| Role | Development | Staging | Production | Shared | Audit/Logs |
|------|------------|---------|------------|--------|------------|
| Developers | Admin | Admin | ReadOnly | ReadOnly | ReadOnly |
| Architects | Admin | Admin | Admin | Admin | ReadOnly |
| ProdOps | ReadOnly | Admin | Admin | Admin | ReadOnly |
| BillingAdmins | N/A | N/A | N/A | N/A | Billing Only |

## Security Controls and Monitoring

### Root Account Protection
- **MFA Required:** Google Authenticator integration
- **Credential Storage:** Secure 1Password vault (maximum 3 administrators)
- **Usage Monitoring:** All root account access logged and alerted
- **Password Policy:** 14+ characters, 90-day rotation

### Multi-Factor Authentication
- **Universal Requirement:** MFA mandatory for all access types
- **Integration Method:** Google Workspace SAML with Google Authenticator
- **No Bypass:** Technical controls prevent MFA circumvention
- **Device Management:** Individual authenticator devices per user

### Audit and Compliance
- **CloudTrail Logging:** Multi-region trails with KMS encryption
- **Centralized Logging:** Dedicated Log Archive account
- **Security Hub Integration:** Continuous compliance monitoring
- **GuardDuty Protection:** Threat detection across all accounts

## Contact Information and Governance

### Corporate Contact Standards
- **Security Contact:** `aws.<project>.audit@ingeno.ca`
- **Corporate Phone:** 1 844 446-4366
- **Billing Contact:** `bills@ingeno.ca` (when applicable)
- **Contact Verification:** Quarterly validation process

### Access Request Process
**Standard Workflow:**
1. **Role-Based Assignment:** Users added to appropriate Google Workspace groups
2. **Automatic Provisioning:** IAM Identity Center group assignments trigger access
3. **Access Verification:** Test console and programmatic access
4. **Documentation:** Record access granted in project documentation

**Privilege Escalation:**
- **Approval Required:** Written justification to super administrators
- **Time-Limited:** Defined expiration for elevated access
- **Enhanced Monitoring:** Additional logging during escalated periods
- **Post-Access Review:** Mandatory documentation of escalated activities

## Evidence Documents

The complete "Ingeno - AWS Landing Zone Provisioning.pdf" serves as the comprehensive Standard Operating Procedure that includes:

- **Identity Federation Setup:** Detailed SAML configuration with Google Workspace
- **IAM Role Configuration:** Step-by-step permission set creation
- **Security Control Implementation:** MFA, CloudTrail, and monitoring setup
- **Access Management Procedures:** User provisioning and group assignment processes
- **Compliance Requirements:** CIS Benchmark and AWS Security Best Practices implementation
