# ACI-MTL

## Description

ACI-MTL is a web-based platform to help manage shelters for homeless people. It is deployed on Amazon ECS Fargate.

The system consists of containerized services including an API backend for user authentication via Cognito and secure file management through S3, alongside a web client interface.

The platform demonstrates production-grade container orchestration with automated CI/CD deployment, comprehensive IAM security controls, and scalable infrastructure management.

## AWS Account access

### AWS Profiles

Use these profiles to access the AWS accounts with the AWS CLI. Make sure you are authentified before making requests. If not, useh `aws sso login` to authenticate.

- `acimtl.prod` : production account
- `acimtl.shared` : shared infra account (this is where ECR images are stored)

Use ca-central-1 region for all requests.

## Notes

### ECS Tasks

```bash
# List clusters
> aws ecs list-clusters

clusterArns:
- arn:aws:ecs:ca-central-1:484907525335:cluster/acimtl-prod-web-client
- arn:aws:ecs:ca-central-1:484907525335:cluster/acimtl-prod-api

# List tasks for web client
> aws ecs list-tasks --cluster acimtl-prod-web-client

taskArns:
- arn:aws:ecs:ca-central-1:484907525335:task/acimtl-prod-web-client/acec54f623894240804eae1ec13867b9

# List tasks for backend api
> aws ecs list-tasks --cluster acimtl-prod-api       

taskArns:
- arn:aws:ecs:ca-central-1:484907525335:task/acimtl-prod-api/09d11cc6e2454d5e8b16ee472ea5eaaf


### List task definitions

> aws ecs list-task-definitions

taskDefinitionArns:
- arn:aws:ecs:ca-central-1:484907525335:task-definition/acimtl-prod-api:17
- arn:aws:ecs:ca-central-1:484907525335:task-definition/acimtl-prod-web-client:17


### List task definition roles

> aws ecs describe-task-definition --task-definition acimtl-prod-api:17 --query 'taskDefinition.taskRoleArn' && aws ecs describe-task-definition --task-definition acimtl-prod-web-client:17 --query 'taskDefinition.taskRoleArn'

"arn:aws:iam::484907525335:role/acimtl-prod-api-AutoScaledFargateServiceTaskDefTask-W0Y5J4Wd4W4H"
"arn:aws:iam::484907525335:role/acimtl-prod-web-client-AutoScaledFargateServiceTask-2PQCxZE72dbm"

### List backend role policies
> aws iam list-attached-role-policies --role-name acimtl-prod-api-AutoScaledFargateServiceTaskDefTask-W0Y5J4Wd4W4H && \
  aws iam list-role-policies --role-name acimtl-prod-api-AutoScaledFargateServiceTaskDefTask-W0Y5J4Wd4W4H

AttachedPolicies:
- PolicyArn: arn:aws:iam::484907525335:policy/BackendPolicy
  PolicyName: BackendPolicy
PolicyNames: []

### Get backend policy

> aws iam get-policy-version --policy-arn arn:aws:iam::484907525335:policy/BackendPolicy

PolicyVersion:
  CreateDate: '2024-12-04T18:31:41+00:00'
  Document:
    Statement:
    - Action:
      - cognito-idp:AdminCreateUser
      - cognito-idp:AdminDeleteUser
      - cognito-idp:AdminDisableUser
      - cognito-idp:AdminEnableUser
      - cognito-idp:AdminGetUser
      - cognito-idp:AdminUpdateUserAttributes
      Effect: Allow
      Resource: arn:aws:cognito-idp:ca-central-1:484907525335:userpool/ca-central-1_J0PRtqr7r
    - Action:
      - logs:CreateLogStream
      - logs:DescribeLogStreams
      - logs:PutLogEvents
      Effect: Allow
      Resource: arn:aws:logs:ca-central-1:484907525335:log-group:acimtl-prod-api:*
    - Action:
      - s3:DeleteObject
      - s3:GetObject
      - s3:ListBucket
      - s3:PutObject
      Condition:
        StringEqualsIfExists:
          aws:SourceVpc: acimtl-prod
      Effect: Allow
      Resource:
      - arn:aws:s3:::acimtl-prod-bucket-clientsfiles6bf6a7b3-ahcxoubzmxqq/*
      - arn:aws:s3:::acimtl-prod-bucket-clientsfiles6bf6a7b3-ahcxoubzmxqq
    Version: '2012-10-17'
  IsDefaultVersion: true
  VersionId: v2

### List frontend role policies

> aws iam list-attached-role-policies --role-name acimtl-prod-web-client-AutoScaledFargateServiceTask-2PQCxZE72dbm && \
  aws iam list-role-policies --role-name acimtl-prod-web-client-AutoScaledFargateServiceTask-2PQCxZE72dbm

AttachedPolicies: []
PolicyNames: []
```

### ECS Task Sizing & Resource Limits Compliance

Our ECS task definitions are sized based on application requirements, with explicit resource reservations and limits, ensuring tasks can scale properly and cluster capacity is managed effectively.

1. **Resource Reservation and Limits:**
   - All ECS task definitions in our production clusters (e.g., `acimtl-prod-api`, `acimtl-prod-web-client`) explicitly specify both `cpu` and `memory` at the task level.
   - For example, the `acimtl-prod-api` task definition reserves 0.5 vCPU (`"cpu": "512"`) and 1 GB memory (`"memory": "1024"`) per task. This ensures that ECS only schedules tasks when sufficient resources are available, supporting predictable scaling and robust capacity planning.
   - On Fargate, these limits are strictly enforced, preventing resource contention and guaranteeing that each task receives the resources it requires.

2. **Evidence – Example Task Definition:**
   - Below is a real snippet from our `acimtl-prod-api` ECS task definition, demonstrating proper resource reservation and limits:

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
      "image": "471112604643.dkr.ecr.ca-central-1.amazonaws.com/acimtl-api-ecr:prod-...",
      "cpu": 0,
      "essential": true,
      "portMappings": [
        { "containerPort": 8080, "hostPort": 8080, "protocol": "tcp" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "acimtl-prod-api",
          "awslogs-region": "ca-central-1",
          "awslogs-stream-prefix": "prod-..."
        }
      }
    }
  ]
}
```

**Summary:**  
Our ECS task definitions are sized based on application requirements, with explicit resource reservations and limits, ensuring tasks can scale properly and cluster capacity is managed effectively.

### ECS Cluster Capacity Management & Scaling

All ECS services in the ACI-MTL environment are deployed using AWS Fargate. Fargate automatically provisions and scales compute resources for tasks, eliminating the need for manual cluster scaling or EC2 instance management. This approach fully meets AWS recommendations for ECS cluster capacity management.

### How We Meet the Requirement

- **Fargate-Only:** All ECS services use the Fargate launch type, so AWS manages all scaling events and cluster capacity automatically.
- **No Manual Scaling:** No EC2 or Fargate Spot capacity providers are configured; there is no manual intervention required for scaling.

### Evidence

- **Cluster Capacity Providers:**

  ```bash
  aws ecs describe-clusters --clusters acimtl-prod-web-client --region ca-central-1 --include CONFIGURATIONS
  # Output: capacityProviders: []
  aws ecs describe-clusters --clusters acimtl-prod-api --region ca-central-1 --include CONFIGURATIONS
  # Output: capacityProviders: []
  ```

- **Service Launch Type:**

  ```bash
  aws ecs describe-services --cluster acimtl-prod-web-client --services acimtl-prod-web-client --region ca-central-1
  # Output: launchType: FARGATE
  aws ecs describe-services --cluster acimtl-prod-api --services acimtl-prod-api --region ca-central-1
  # Output: launchType: FARGATE
  ```

This configuration ensures that all scaling and capacity management is handled by AWS, in line with best practices and compliance requirements.
