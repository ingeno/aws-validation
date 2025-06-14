# ACI-MTL - Implementation TODO for AWS Service Delivery Compliance

## ECS-004: Tagging Strategy and Tag Propagation Implementation

### Overview
This document outlines the specific changes needed to complete AWS Service Delivery ECS-004 validation compliance.

### Required Changes (Missing Components)

#### 1. Task Definition Tagging (CDK Implementation)

**Location**: AWS CDK TypeScript code for ECS task definitions

**Add these formal tags to expose existing version tracking:**
```typescript
// For acimtl-prod-api task definition
const apiTaskDefinition = new ecs.FargateTaskDefinition(this, 'ApiTaskDef', {
  // ... existing configuration
  tags: {
    'Environment': 'production',
    'Application': 'acimtl',
    'Component': 'api',
    'Version': process.env.GIT_COMMIT_SHA || 'unknown'
  }
});

// For acimtl-prod-web-client task definition
const webClientTaskDefinition = new ecs.FargateTaskDefinition(this, 'WebClientTaskDef', {
  // ... existing configuration
  tags: {
    'Environment': 'production',
    'Application': 'acimtl',
    'Component': 'web-client',
    'Version': process.env.GIT_COMMIT_SHA || 'unknown'
  }
});
```

**Implementation Notes:**
- Use the same Git commit SHA your CI/CD pipeline already generates for container images
- The `GIT_COMMIT_SHA` environment variable should match what's used in image tagging

#### 2. Service Tag Propagation Configuration

**Location**: AWS CDK ECS Service definitions

**Add tag propagation to existing services:**
```typescript
// For API service
const apiService = new ecs.FargateService(this, 'ApiService', {
  // ... existing configuration
  propagateTags: ecs.PropagatedTagSource.TASK_DEFINITION,
  enableECSManagedTags: true
});

// For Web Client service
const webClientService = new ecs.FargateService(this, 'WebClientService', {
  // ... existing configuration
  propagateTags: ecs.PropagatedTagSource.TASK_DEFINITION,
  enableECSManagedTags: true
});
```

### Implementation Steps

#### Step 1: Update CDK Code
1. **Locate your ECS task definition and service definitions** in your CDK TypeScript code
2. **Add the tags object** to both task definitions (as shown above)
3. **Add propagateTags and enableECSManagedTags** to both services (as shown above)
4. **Ensure your deployment pipeline** passes the Git commit SHA as an environment variable to CDK

#### Step 2: Deploy Changes
```bash
# Deploy the updated CDK stack
cdk deploy --profile acimtl.prod

# This will:
# - Create new task definition revisions with tags
# - Update services with tag propagation enabled
# - Apply changes without downtime
```

### Verification Commands

#### Check Task Definition Tags (After Implementation)
```bash
# Verify API task definition tags
aws ecs describe-task-definition \
  --task-definition acimtl-prod-api:latest \
  --region ca-central-1 \
  --include TAGS \
  --query 'tags' \
  --profile acimtl.prod

# Expected output - 4 required tags:
[
  {"key": "Environment", "value": "production"},
  {"key": "Application", "value": "acimtl"},
  {"key": "Component", "value": "api"},
  {"key": "Version", "value": "4f3ebae951a368bda79d84632a831a4f266b1bed"}
]
```

#### Check Service Tag Propagation
```bash
# Verify services have tag propagation enabled
aws ecs describe-services \
  --cluster acimtl-prod-api \
  --services acimtl-prod-api \
  --region ca-central-1 \
  --query 'services[0].{propagateTags:propagateTags,enableECSManagedTags:enableECSManagedTags}' \
  --profile acimtl.prod

# Expected output:
{
  "propagateTags": "TASK_DEFINITION",
  "enableECSManagedTags": true
}
```

### Implementation Checklist

**Task Definition Tags:**
- [ ] Add 4 required tags to API task definition in CDK
- [ ] Add 4 required tags to Web Client task definition in CDK
- [ ] Deploy updated CDK stack
- [ ] Verify tags present on new task definition revisions

**Service Tag Propagation:**
- [ ] Enable tag propagation in CDK service definitions
- [ ] Verify `propagateTags: TASK_DEFINITION` is set
- [ ] Verify `enableECSManagedTags: true` is set
- [ ] Confirm tags propagate to newly launched tasks

### Compliance Impact

Once these two changes are implemented:
- **One-to-one mapping**: Already satisfied via existing Git SHA in image tags + new formal Version tag
- **Tag dimensions**: Environment, Application, Component will enable proper organization
- **Business process mapping**: Component tag will map to singular functions per ECS-003
- **Tag propagation**: Tasks and associated resources will receive proper tags
- **Managed tags**: ECS-managed tags will be enabled for AWS resource tracking

## ECS-018: Container Insights Implementation

### Required Changes (Observability Enhancement)

#### 1. ECS Cluster Container Insights Configuration

**Location**: AWS CDK TypeScript code for ECS cluster definitions

**Add Container Insights to existing clusters:**
```typescript
// For API cluster
const apiCluster = new ecs.Cluster(this, 'ApiCluster', {
  // ... existing configuration
  containerInsights: true
});

// For any other ECS clusters
const otherCluster = new ecs.Cluster(this, 'OtherCluster', {
  // ... existing configuration
  containerInsights: true
});
```

**Implementation Notes:**
- Container Insights has been manually enabled via CLI for immediate compliance
- Adding this to CDK ensures future deployments maintain Container Insights configuration
- Provides individual app/container level metrics required for ECS-018 compliance
- Enables detailed CloudWatch metrics and logs for task-level observability

### Summary

This is a lightweight addition to your existing, well-implemented version tracking system. You already have the hard part (Git SHA traceability) working perfectly - you just need to expose it through formal AWS tags and enable propagation for full compliance.
