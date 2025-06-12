# Valmetal

## Description

Valmetal project is a IoT / web-based platform to help manage farming equipments. It uses Amazon ECS Fargate to run containerized services.

The system consists of containerized services including an API backend for user authentication via Cognito and secure file management through S3, alongside a web client interface.

The platform demonstrates production-grade container orchestration with automated CI/CD deployment, comprehensive IAM security controls, and scalable infrastructure management.

Diagram: @valmetal-diagram.mmd

## AWS Account access

### AWS Profiles

Use these profiles to access the AWS accounts with the AWS CLI. Make sure you are authentified before making requests. If not, useh `aws sso login` to authenticate.

- `valmetal.prod` : production account
- `valmetal.shared` : shared infra account (this is where ECR images are stored)

Use us-east-1 region for all requests.

## Notes

### ECS Tasks

```bash
# List clusters
> aws ecs list-clusters

clusterArns:
- arn:aws:ecs:us-east-1:628892762446:cluster/valmetal-prod-web-client
- arn:aws:ecs:us-east-1:628892762446:cluster/valmetal-prod-backend-api

# List tasks for web client
> aws ecs list-tasks --cluster valmetal-prod-web-client

taskArns:
- arn:aws:ecs:us-east-1:628892762446:task/valmetal-prod-web-client/4822ca6be77f49429c091d1430a89f41

# List tasks for backend api
> aws ecs list-tasks --cluster valmetal-prod-backend-api

taskArns:
- arn:aws:ecs:us-east-1:628892762446:task/valmetal-prod-backend-api/9c9fbdab99cd4d6fa5327283f51ab38f


# List task definitions
> aws ecs list-task-definitions

taskDefinitionArns:
- arn:aws:ecs:us-east-1:628892762446:task-definition/valmetal-prod-backend-api:37
- arn:aws:ecs:us-east-1:628892762446:task-definition/valmetal-prod-web-client:20


# List task definition roles

> aws ecs describe-task-definition \ 
      --task-definition valmetal-prod-backend-api:37 \
      --query 'taskDefinition.taskRoleArn' && \
    aws ecs describe-task-definition \ 
      --task-definition valmetal-prod-web-client:20 \
      --query 'taskDefinition.taskRoleArn'

"arn:aws:iam::628892762446:role/valmetal-prod-backend-api-AutoScaledFargateServiceT-sIV3LgyVICHP"
"arn:aws:iam::628892762446:role/valmetal-prod-web-client-AutoScaledFargateServiceTa-MkTSyCuPPpEs"

# List backend role policies
> aws iam list-attached-role-policies --role-name valmetal-prod-backend-api-AutoScaledFargateServiceT-sIV3LgyVICHP && \
  aws iam list-role-policies --role-name valmetal-prod-backend-api-AutoScaledFargateServiceT-sIV3LgyVICHP

AttachedPolicies:
- PolicyArn: arn:aws:iam::628892762446:policy/BackendPolicy
  PolicyName: BackendPolicy
PolicyNames: []

# Get backend policy

> aws iam get-policy-version --policy-arn arn:aws:iam::628892762446:policy/BackendPolicy --version-id v10

PolicyVersion:
  CreateDate: '2025-04-24T14:53:33+00:00'
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
      Resource: arn:aws:cognito-idp:us-east-1:628892762446:userpool/us-east-1_W0zPMIedZ
    - Action:
      - logs:CreateLogStream
      - logs:DescribeLogStreams
      - logs:PutLogEvents
      Effect: Allow
      Resource: arn:aws:logs:us-east-1:628892762446:log-group:valmetal-prod-backend-api:*
    - Action: iot:SearchIndex
      Effect: Allow
      Resource: arn:aws:iot:us-east-1:628892762446:index/AWS_Things
    - Action: iot:UpdateThingShadow
      Effect: Allow
      Resource: arn:aws:iot:us-east-1:628892762446:thing/*
    - Action:
      - sns:Subscribe
      - sns:Unsubscribe
      Effect: Allow
      Resource: arn:aws:sns:us-east-1:628892762446:valmetal-prod-equipment-alarms
    - Action: states:StartExecution
      Effect: Allow
      Resource: arn:aws:states:us-east-1:628892762446:stateMachine:AlarmStepFunctionsprod3C8F8A3E-ccLB3dOLNPNr
    - Action:
      - states:DescribeExecution
      - states:StopExecution
      Effect: Allow
      Resource: arn:aws:states:us-east-1:628892762446:execution:AlarmStepFunctionsprod3C8F8A3E-ccLB3dOLNPNr:*
    - Action:
      - sqs:DeleteMessage
      - sqs:ReceiveMessage
      Effect: Allow
      Resource:
      - arn:aws:sqs:us-east-1:628892762446:AlarmQueue-prod
      - arn:aws:sqs:us-east-1:628892762446:ThingEventsQueue-prod
    - Action: dynamodb:Query
      Effect: Allow
      Resource: arn:aws:dynamodb:us-east-1:628892762446:table/EntityHierarchy/index/EntityAlarmIndicatorIndex
    - Action:
      - appconfig:GetConfiguration
      - appconfig:GetLatestConfiguration
      - appconfig:StartConfigurationSession
      - timestream:DescribeEndpoints
      Effect: Allow
      Resource: '*'
    - Action: timestream:Select
      Effect: Allow
      Resource: arn:aws:timestream:us-east-1:628892762446:database/valmetal-autorationx/table/feed_sequence
    Version: '2012-10-17'
  IsDefaultVersion: true
  VersionId: v10

# List frontend role policies
> aws iam list-attached-role-policies --role-name valmetal-prod-web-client-AutoScaledFargateServiceTa-MkTSyCuPPpEs && \
  aws iam list-role-policies --role-name valmetal-prod-web-client-AutoScaledFargateServiceTa-MkTSyCuPPpEs

AttachedPolicies: []
PolicyNames: []
```

## ECS Task Sizing & Resource Limits Compliance

Our ECS task definitions are sized based on application requirements, with explicit resource reservations and limits, ensuring tasks can scale properly and cluster capacity is managed effectively.

1. **Resource Reservation and Limits:**
   - All ECS task definitions in our Valmetal production clusters (e.g., `valmetal-prod-web-client`) explicitly specify both `cpu` and `memory` at the task level.
   - For example, the `valmetal-prod-web-client` task definition reserves 0.5 vCPU (`"cpu": "512"`) and 1 GB memory (`"memory": "1024"`) per task. This ensures that ECS only schedules tasks when sufficient resources are available, supporting predictable scaling and robust capacity planning.
   - On Fargate, these limits are strictly enforced, preventing resource contention and guaranteeing that each task receives the resources it requires.

2. **Evidence – Example Task Definition:**
   - Below is a real snippet from our `valmetal-prod-web-client` ECS task definition, demonstrating proper resource reservation and limits:

```json
{
  "family": "valmetal-prod-web-client",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "valmetal-prod-web-client",
      "image": "497409020770.dkr.ecr.us-east-1.amazonaws.com/valmetal-web-client-ecr:prod-...",
      "cpu": 0,
      "essential": true,
      "portMappings": [
        { "containerPort": 3000, "hostPort": 3000, "protocol": "tcp" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "valmetal-prod-web-client",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "prod-...",
          "mode": "blocking"
        }
      }
    }
  ]
}
```

## ECS Cluster Capacity Management & Scaling

All ECS services in the Valmetal environment are deployed using AWS Fargate. Fargate automatically provisions and scales compute resources for tasks, eliminating the need for manual cluster scaling or EC2 instance management. This approach fully meets AWS recommendations for ECS cluster capacity management.

### How We Meet the Requirement

- **Fargate-Only:** All ECS services use the Fargate launch type, so AWS manages all scaling events and cluster capacity automatically.
- **No Manual Scaling:** No EC2 or Fargate Spot capacity providers are configured; there is no manual intervention required for scaling.

### Evidence

- **Cluster Capacity Providers:**

  ```bash
  aws ecs describe-clusters --clusters valmetal-prod-web-client --include CONFIGURATIONS
  # Output: capacityProviders: []
  ```

- **Service Launch Type:**

  ```bash
  aws ecs describe-services --cluster valmetal-prod-web-client --services valmetal-prod-web-client
  # Output: launchType: FARGATE
  ```

This configuration ensures that all scaling and capacity management is handled by AWS, in line with best practices and compliance requirements.
