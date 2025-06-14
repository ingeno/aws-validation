# Root Account Security Controls Summary

## Purpose

This document summarizes the security controls and procedures implemented for AWS root account management across all customer environments. These controls ensure proper governance, security, and compliance for root account usage in accordance with AWS security best practices.

## Root Account Usage Policy

### When Root Account Access is Permitted

Root account access is **strictly limited** to the following scenarios:

**Emergency Access Only:**
- System-wide service outages affecting IAM Identity Center
- Critical security incidents requiring immediate administrative intervention
- AWS Support escalations requiring root account verification
- Recovery from Control Tower or organizational-level failures

**Prohibited Uses:**
- Daily operational activities
- Regular workload deployment and management
- Standard administrative tasks
- Development or testing activities

**Access Control:**
- Maximum of 3 designated personnel have root account access
- All root account usage requires incident documentation
- Security team notification mandatory within 15 minutes of access
- Post-incident review required for all root account activities

## Multi-Factor Authentication Implementation

### Root Account MFA Configuration

**MFA Requirements:**
- MFA is **mandatory** for all root accounts across all customer environments
- Google Authenticator used as the MFA mechanism
- Integration with 1Password for secure credential storage
- Unique MFA device for each account (no shared authenticators)

**Implementation Process:**
1. **Management Account Setup:**
   - Root account MFA configured during initial account creation
   - 1Password used as Virtual Authenticator app
   - QR code scanning integrated with 1Password workflow
   - Account ID and Secret Key documented in secure vault

2. **Sub-Account Configuration:**
   - MFA enabled for every sub-account root user
   - Password reset process initiated for dormant root accounts
   - Unique passwords and MFA tokens for each environment
   - Systematic documentation in customer-specific 1Password vaults

**Security Controls:**
- MFA tokens stored in encrypted 1Password vaults
- Regular MFA device verification and rotation
- Backup recovery codes securely documented
- MFA bypass prevention through organizational policies

## Contact Information Management

### Corporate Contact Configuration

**Primary Contact Information:**
- **Full Name:** `<Customer Name> management account`
- **Contact Details:** Customer-specific information as provided
- **Email Format:** Corporate email addresses only (no personal emails)
- **Phone Number:** Corporate contact numbers with proper verification

**Security Contact Configuration:**
- **Full Name:** Security
- **Title:** Security
- **Email Address:** `aws.<project>.audit@ingeno.ca`
- **Phone Number:** 1 844 446-4366 (Corporate Security Line)

**Billing Contact Configuration (When Applicable):**
- **Full Name:** Finance
- **Title:** Finance  
- **Email Address:** `bills@ingeno.ca`
- **Phone Number:** 1 844 446-4366 (Corporate Finance Line)

**Contact Management Process:**
1. Contact information set during account provisioning
2. Regular verification of contact details (quarterly)
3. Immediate updates for any organizational changes
4. Consistent format across all customer environments

## CloudTrail Logging Configuration

### Multi-Region CloudTrail Implementation

**CloudTrail Setup:**
- **Configuration Method:** Automated through AWS Control Tower
- **Coverage:** All regions enabled in Control Tower governance
- **Trail Type:** Multi-region trail with global service events
- **Management Events:** All management events logged
- **Data Events:** IAM roles and SSO activities tracked

**Regional Coverage:**
- **Home Region:** Primary region (ca-central-1 for Canadian customers, us-east-2 for US customers)
- **Secondary Regions:** Disaster recovery regions (us-west-2 for additional coverage)
- **Governance:** All enabled regions governed by Control Tower stacksets
- **Compliance:** Region-level compliance monitoring through AWS Config

**Logging Configuration:**
```json
{
  "TrailName": "aws-controltower-cloudtrail",
  "S3BucketName": "aws-controltower-logs-<account-id>-<region>",
  "IncludeGlobalServiceEvents": true,
  "IsMultiRegionTrail": true,
  "EnableLogFileValidation": true,
  "KMSEncryption": "Enabled"
}
```

## CloudTrail Log Protection

### Centralized Log Architecture

**Log Archive Account:**
- **Purpose:** Dedicated account for secure log storage
- **Access Control:** Restricted access through IAM Identity Center
- **Isolation:** Separate from workload accounts for security
- **Retention:** Long-term retention with compliance-based policies

**S3 Bucket Protection:**
```json
{
  "BucketName": "aws-controltower-logs-<account-id>-<region>",
  "Encryption": "AES256-KMS",
  "VersioningStatus": "Enabled",
  "PublicAccessBlock": "All public access blocked",
  "BucketPolicy": "CloudTrail service permissions only"
}
```

**Protection Mechanisms:**

1. **KMS Encryption:**
   - Custom KMS key: "ControlTower"
   - Key policy restricts access to CloudTrail and Config services
   - Encryption in transit and at rest
   - Key rotation enabled

2. **Access Controls:**
   - Service Control Policies prevent unauthorized deletion
   - Bucket policies restrict access to AWS services only
   - Cross-account access through designated roles only
   - MFA required for any administrative actions

3. **Monitoring and Alerting:**
   - CloudWatch monitoring for bucket access
   - SNS notifications for unauthorized access attempts
   - AWS Config rules for bucket policy compliance
   - Security Hub integration for centralized monitoring

**Backup and Recovery:**
- Cross-region replication for disaster recovery
- Versioning enabled for accidental deletion protection
- Lifecycle policies for cost-effective long-term storage
- Regular backup verification and restoration testing

## Implementation Compliance

### Verification Checklist

**Root Account Security:**
- Root account access limited to emergency use only
- Maximum 3 designated administrators
- MFA enabled on all root accounts
- Credentials securely stored in 1Password
- Usage logging and incident documentation

**Contact Information:**
- Corporate contact details configured
- Security contact: `aws.<project>.audit@ingeno.ca`
- Corporate phone number: 1 844 446-4366
- Regular contact verification process

**CloudTrail Configuration:**
- Multi-region CloudTrail enabled
- All Control Tower regions covered
- Global service events included
- Log file validation enabled
- KMS encryption configured

**Log Protection:**
- Dedicated Log Archive account
- KMS encryption with custom key
- Service Control Policies implemented
- Cross-region backup and replication
- Access monitoring and alerting

