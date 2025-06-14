# Valmetal - Implementation TODO for AWS Service Delivery Compliance

## ECS-004: Tagging Strategy and Tag Propagation Implementation

### Required Changes (Missing Components)

#### 1. Task Definition Tagging (CDK Implementation)

**Location**: AWS CDK TypeScript code for ECS task definitions

**Add these formal tags to expose existing version tracking:**
```typescript
// For valmetal-prod-backend-api task definition
const apiTaskDefinition = new ecs.FargateTaskDefinition(this, 'ApiTaskDef', {
  // ... existing configuration
  tags: {
    'Environment': 'production',
    'Application': 'valmetal',
    'Component': 'backend-api',
    'Version': process.env.GIT_COMMIT_SHA || 'unknown'
  }
});

// For valmetal-prod-web-client task definition
const webClientTaskDefinition = new ecs.FargateTaskDefinition(this, 'WebClientTaskDef', {
  // ... existing configuration
  tags: {
    'Environment': 'production',
    'Application': 'valmetal',
    'Component': 'web-client',
    'Version': process.env.GIT_COMMIT_SHA || 'unknown'
  }
});
```

**Implementation Notes:**
- Use the same Git commit SHA your CI/CD pipeline already generates for container images
- The `GIT_COMMIT_SHA` environment variable should match what's used in image tagging

#### 2. Service Tag Propagation Configuration

**Location**: AWS CDK TypeScript code for ECS services

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

## ECS-018: Container Insights Implementation

### Required Changes (Observability Enhancement)

#### 1. ECS Cluster Container Insights Configuration

**Location**: AWS CDK TypeScript code for ECS cluster definitions

**Add Container Insights to existing clusters:**
```typescript
// For backend API cluster
const backendApiCluster = new ecs.Cluster(this, 'BackendApiCluster', {
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
