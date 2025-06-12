# **Amazon ECS**

## Service Delivery Validation Checklist

### **Validity Period: February 2025-August 2025**

*This version of the checklist was released on February 14th, 2025\. The next version of this checklist is expected to be released in August 2025\. AWS Partners may continue to use this version of the checklist until November 2025\. Please review the change log for a list of changes (if any) since the previous version.*

## **Introduction**

AWS Specialization Program recognizes AWS Partner Network (APN) Partners who demonstrate successful customer delivery and expertise in specific AWS services. This AWS Service Delivery Validation Checklist outlines the criteria necessary to achieve the Amazon ECS designation under the AWS Service Delivery Program.

## **Expectations of Parties**

It is expected that AWS Partners will review this document in detail before submitting an AWS Service Delivery Program application, even if AWS Partners believe that all pre-requisites are met. If items in this document are unclear AWS Partners should contact their Partner Development Representative (PDR) or Partner Development Manager (PDM). AWS reserves the right to make changes to this document at any time.

When ready to submit a program application, AWS Partners must complete the self-assessment spreadsheet available for download at the top of this page. Upon completion of the self-assessment spreadsheet, AWS Partners must submit an application in AWS Partner Central. For more information on how to submit an application, view the [Program Guide](https://partnercentral.awspartner.com/ContentFolderPartner?id=0698a00000BpB2yAAF) or contact your PDR or PDM.

Once an AWS Partner’s application has been submitted through the AWS Partner Central, AWS will review for completeness and for compliance with the requirements. AWS will review and aim to respond back with any questions within five business days. Incomplete applications will not be considered until all requirements are met. If complete, AWS will send the application to in-house experts to complete a Technical Validation.

The Technical Validation will be completed offline. AWS Partners should prepare for the Technical Validation by reading the Checklist, completing and submitting a self-assessment for each Case Study, and submitting all relevant objective evidence with the application, including architecture diagrams.

Upon completion of the Technical Validation, AWS Partners will receive a final status for the submitted application either confirming or denying acceptance into the AWS Service Delivery Program. AWS Partners may attain one or more AWS Service Delivery designations. Please note that attaining one AWS Service Delivery designation does not guarantee approval into additional AWS Service Delivery designations. If the AWS Partner is denied acceptance for the desired AWS Service Delivery designation, the AWS Partner may re-apply via AWS Partner Central after the AWS Partner has remediated all outstanding action items.

AWS may revoke an AWS Partner’s AWS Service Delivery designation if, at any time, AWS determines in its sole discretion that such AWS Partner does not meet its AWS Service Delivery Program requirements. If an AWS Partner’s AWS Service Delivery designation is revoked, such AWS Partner will (i) no longer receive benefits associated with its designation, (ii) immediately cease use of all materials provided to it in connection with the applicable AWS Service Delivery designation and (iii) immediately cease to identify or hold itself out as a Partner of such AWS Service Delivery.

## **AWS Service Delivery Program Prerequisites**

The following items will be validated by the AWS Service Delivery Program Manager; missing or incomplete information must be addressed prior to scheduling of the Technical Validation.

* **1.0APN Program Requirements**  
  * **1.1Program Guidelines**  
    The AWS Partner must read the Program guidelines and Definitions before submitting the application. [Click here for Program details](https://partnercentral.awspartner.com/ContentFolderPartner?id=0698a00000BpB2yAAF).  
  * **1.2Services Path Membership**  
    Partner must be at the Validated or Differentiated stage within the [Services Path](https://aws.amazon.com/partners/paths). Partners should talk to their PDR/PDM about how to join the Services Path.  
* **2.0AWS Customer Case Studies**  
  * **2.1Production AWS Customer Case Studies**  
    AWS Partner must privately share with AWS details about two (2) unique examples of Amazon ECS projects executed for two (2) unique AWS customers. Each case study must demonstrate how the Partner used the unique capabilities of the AWS service to address the customer's problem.  
    In addition to the required case study details provided in AWS Partner Central, the partner must also provide architecture diagrams of the specific customer deployment and information listed in the technical requirements sections of this validation checklist.  
    The information provided for these case studies will be used by AWS for validation purposes only. AWS Partner is not required to publish these details publicly.  
    AWS Partner can reuse the same case study across different AWS Specialization designations as long as the case study and implementation scope are relevant to those designations. The partner should make sure the existing case study clearly explains the relevance to each designation they are applying for.  
    In cases where a case study is used across multiple AWS Partner Specialization applications, the partner must attach a completed self-assessment spreadsheet for each Specialization with all service-specific details provided.  
    AWS will accept one case study per customer. Each customer must be a separate legal entity to qualify. The partner may use an example for an internal or affiliate company of the partner if the offering is available to outside customers.  
    All case studies must describe deployments that have been performed within the past 18 months and must be for projects that are in production with customers, rather than in a ‘pilot’ or proof of concept stage.  
    All case studies provided will be examined in the Documentation Review of the Technical Validation. The partner offering will be removed from consideration if the partner cannot provide the documentation necessary to assess all case studies against each relevant validation checklist item, or if any of the validation checklist items are not met.  
    Note: Public-facing case studies are encouraged over private case studies, as they may be used by AWS for marketing purposes and will be featured in [Partner Solution Finder](https://partners.amazonaws.com/). Evidence of a publicly referenceable case study must be provided in the form of a case study, white paper, blog post, or equivalent. In cases where the partner cannot publicly name customers due to the sensitive nature of the customer engagements, the partner may choose to anonymize the public case study. Anonymized public case study details will be published by AWS, but the customer name will remain private. For best practices on how to write an accepted public case study see the [Public Case Study Guide](https://partnercentral.awspartner.com/partnercentral2/s/resources?Id=0698W00000wgPO9QAM).  
  * **2.2Architecture Diagrams**  
    Submitted case studies must include architecture diagrams.  
    * Architecture diagrams must detail how the solution interacts with the AWS Cloud; specifically, what AWS tools and services are used in the solution  
    * Diagrams must also include evidence of AWS best practices for architecture and security  
  * **Note:** [Click here for best practices on how to build an acceptable Architecture Diagram.](https://s3-us-west-2.amazonaws.com/competency.awspartner.com/Templates/Partner+Guides/How-to+Guide+-+APN+-+Architecture+Diagram.pdf)  
* **3.0AWS Partner Self-Assessment**  
  * **3.1Program Validation Checklist Self-Assessment**  
    AWS Partner must conduct a self-assessment of their compliance to the requirements of the Amazon ECS Service Delivery using the Self-Assessment Spreadsheet linked at the top of this page. All sections of the Self-Assessment Spreadsheet must be completed for each case study and spreadsheet must be attached to the associated application in AWS Partner Central.  
    It is recommended that AWS Partners have their Solutions Architect, PDR, or PDM review the completed self-assessment before submitting to AWS. The purpose of this is to ensure the AWS Partner’s AWS team is engaged and working to provide recommendations prior to the technical validation and to help ensure a positive technical validation experience.

## **Amazon ECS Customer Reference Requirements**

The following requirements relate to how Amazon ECS was used in each provided customer reference.

### **Amazon ECS Expertise**

The following requirements relate to the AWS Partner's ability to demonstrate deep expertise with Amazon ECS in the context of the provided customer references.

* **ECS-001 \- Amazon ECS represents majority of the workload**  
  Amazon ECS is used to manage majority of all workloads and core data flows for the system. Amazon Elastic Compute Cloud instances (EC2 or Fargate) should be used to manage the underlying infrastructure of the Amazon ECS cluster.  
  Please provide the following as evidence:  
  * List of workloads/components that are being deployed to Amazon ECS  
  * The output of running the following command: aws ecs list-tasks  
* **ECS-002 \- Changes to infrastructure and workloads are deployed and updated in an automated and reliable way**  
  Changes to the infrastructure and workloads are automated using infrastructure as code tooling such as AWS CloudFormation, AWS CDK, or other third-party infrastructure as code tooling. These technical artifacts (both infrastructure and workload) must be version controlled and stored in a source repository such as GitHub. The tool being used must have rollback procedures in place in case of failure. \*Changes to production clusters/environment cannot be managed/conducted through the AWS management console.  
  Please provide the following as evidence:  
  * Infrastructure as code tooling used to manage infrastructure  
  * Description of the tools used for automated deployment  
  * Description of deployment process and rollback procedures  
  * Description of source repository that stores infrastructure and task definition files in source control  
  * Version control system used to manage technical artifacts  
  * Description of CI/CD tooling to automate updates to underlying workloads  
* **ECS-003 \- Amazon ECS task definition families are used for a singular business purpose**  
  In the context of Amazon Elastic Container Service (ECS), a singular business purpose task is a task that runs a single application process in a container image. This approach is considered best practice when deploying containers on ECS because it ensures that each container image is focused on a single, well-defined function. Having a single purpose for each container makes it easier to manage and maintain the containers, as well as to scale and update individual components. It also improves security by reducing the attack surface and making it easier to apply security patches to specific components.  
  Please provide the following as evidence:  
  * Provide a list of created task definitions and description of their business functions.  
* **ECS-004 \- Tagging strategy and Amazon ECS Managed Tags and Tag Propagation is implemented**  
  To ensure that application versions are tagged appropriately and Amazon ECS Managed Tags and Tag Propagation are enabled, the following practices should be followed:  
  * There should be a one-to-one mapping between a version of application code, a container image tag, and a task definition revision. As part of the release process, a git commit should be turned into a container image that has its own associated git commit SHA. That container image tag should then get its own Amazon ECS task definition update.  
  * Amazon ECS Managed Tags and Tag Propagation should be enabled to attach and propagate tags on the tasks that the service launches. This is useful for usage and billing reports and can provide insight into resource usage.  
  * The tag dimensions should accurately represent how tasks are launched within an Amazon ECS cluster. Example dimensions can include environment=production or application=storefront.  
* Please provide the following as evidence:  
  * Description of tagging strategy used by the partner to ensure application versions are tagged appropriately based on running task definitions  
  * Description of tag dimensions that accurately represent how tasks are launched within an Amazon ECS cluster  
  * Example of tag dimensions being used within and/or across Amazon ECS clusters that demonstrate that tasks are being mapped to singular business processes.  
* **ECS-005 \- Task definition families have their own associated IAM roles**  
  Task definition families should have their own associated IAM roles to limit how much access each service has to resources within a partners AWS accounts  
  Please provide the following as evidence:  
  * ARN of task definition files from the case studies provided that shows that the IAM role attached are scoped down by the principles of least privilege  
* **ECS-006 \- Partner has mechanism in place for appropriately determining Amazon ECS task sizes**  
  Task definitions need to be appropriately sized based on application requirements for tasks running in an Amazon ECS cluster to be able to scale properly and for capacity planning purposes.  
  Please provide the following as evidence:  
  * Description of resource reservation and limits for running tasks within partners Amazon ECS cluster  
  * Example task definition file that demonstrates proper usage of resource reservations and limits  
* **ECS-007 \- Partner has defined strategy for addressing cluster capacity for Amazon ECS clusters**  
  Amazon ECS Capacity Providers allow for Amazon ECS clusters to scale your clusters up and down for you. The three different capacity providers available include the at least one of the following: 1\) Amazon EC2, 2\) Fargate, and 3\) Fargate Spot. The recommended approach for scaling clusters is to leverage capacity providers and to not scale clusters manually.  
  Please provide the following as evidence:  
  * Description of how the partner has configured Amazon ECS capacity providers to address scaling events within their Amazon ECS clusters  
* **ECS-008 \- Partner has defined strategy for leveraging Amazon EC2 Spot and FARGATE\_SPOT. Note that this is only applicable for partners leveraging spot capacity with their Amazon ECS clusters.**  
  Spot capacity is appropriate for batch processing, machine-learning workloads, and dev/staging environments where temporary downtime is acceptable. During high demand, the unavailability of Spot capacity can cause delays in Fargate Spot tasks and EC2 Spot instance launches. However, ECS services and EC2 Auto Scaling groups will retry launches until the required capacity is available. Spot capacity will not be replaced with on-demand capacity. When overall demand increases, instances and tasks may be terminated with a two-minute warning, and tasks should start an orderly shutdown to minimize errors. To minimize Spot shortages, partners should utilize capacity across multiple regions and availability zones, leverage multiple EC2 instance types in autoscaling groups, and use a capacity-optimized Spot allocation strategy  
  Please provide the following as evidence: *Note : Please note that the AWS CLI command below should be run prior to completing the self-assessment*  
  * Description of the strategy used to minimize Spot capacity shortages when utilizing EC2 Spot Instances and Fargate Spot.  
  * Output of "aws ecs describe-capacity-providers —region $region".  
  * Output of "aws ec2 describe-spot-fleet-requests —region $region".  
* **ECS-009 \- Partner has mechanism for managing multiple Amazon ECS clusters**  
  Partners that spread their workloads across multiple Amazon ECS clusters must have a uniform and consistent method for provisioning of container-related infrastructure, and management of workloads across multiple clusters. Use cases for having multiple Amazon ECS clusters include the following as examples:  
  * Resource isolation: You might want to create separate Amazon ECS clusters for different applications or environments, to isolate their resources and prevent potential interference between them.  
  * Different deployment pipelines: If you have multiple applications with different deployment pipelines, you can create separate Amazon ECS clusters for each application to manage their deployments independently.  
  * Different scaling requirements: If you have different applications with varying resource utilization patterns, you can create separate Amazon ECS clusters for each application to optimize their scaling and cost.  
  * Different security requirements: If you have different applications with different security requirements, you can create separate Amazon ECS clusters for each application to manage their security independently.  
  * Different network requirements: If you have different applications with different network requirements, you can create separate Amazon ECS clusters for each application to manage their network resources independently.  
* Please provide the following as evidence for multi-cluster workloads:  
  * Description of IaC tool being used to define and deploy Amazon ECS clusters. Partners may also provide sample templates that cover how container related infrastructure is being deployed and managed.  
  * Description of the tool being used for multi-cluster management.  
  * If Amazon ECS clusters and their respective workloads are being deployed on-prem using ECS-A, hybrid scenarios, please provide justification for doing so.  
  * If multiple AWS accounts are being used, please provide description that details how AWS accounts are mapped per cluster/workload and the purpose for each cluster being defined. Example would be a scenario in which an AWS account is being used as the “management” or “control” plane that is then used to deploy Amazon ECS clusters to target AWS accounts.  
* **ECS-010 \- Partner uses an image scanning tool that runs a security scan before any image is used within the cluster**  
  Any image that is being used within the cluster must be stored in an image repository such as Amazon ECR and must go through a security scan to ensure that there are no security vulnerabilities. The partner should also have a process in place where images are regularly scanned for vulnerabilities.  
  Please provide the following as evidence:  
  * Description of image repository being used for submitted case studies  
  * Description of the tool and configuration used to protect running containers within the cluster. If ECR is being used, task definitions should demonstrate the proper configurations:  
    * Amazon ECR repository policies allow Amazon ECS tasks to pull container images  
    * Image versions in ECR should match versions specified in task definition files  
  * Partner should have monitoring/observability mechanism/tooling to monitor usage of ECR repository to ensure that expected container images are being pulled and stored in Amazon ECR  
* **ECS-011 \- Partner uses a runtime security tool for all containerized workloads**  
  The workloads running inside a cluster must have active protection for any containerized workload that is actively running inside the cluster that includes preventing malicious syscalls being made to the underlying host operating system. Restricting what syscalls can be made from inside the container can help aid in reducing the applications attack surface. Note that runtime security configurations is different between Windows and Linux Containers  
  Please provide the following as evidence:  
  * Amazon ECS cluster has a tool or configuration in place to protect running containers from malicious syscalls being made to the underlying host operating system.  
  * The specific tool or configuration used for protection provides evidence that it is actively protecting running containers  
  * If open-source tooling/third party tooling is being used, provide description of the specific tool and security modules/configurations added  
  * If Windows containers are being used, the robust security boundary within the Windows environment and the tool used to assess running Windows containers  
* **ECS-012 \- Use of operating systems optimized for running containerized workloads on Amazon ECS**  
  Partner should be leveraging Amazon ECS optimized AMI’s that are optimized for containerized workloads to ensure that customer workloads are protected. At least one of the customer example workloads is implemented on one of the operating systems listed below. Other operating systems may be considered given that the partner provides justification for using such operating system with their Amazon ECS cluster.  
  * Amazon Linux  
  * Ubuntu Linux  
  * Bottlerocket OS  
  * Windows  
* Please provide the following as evidence:  
  * Operating system being used as part of the implementation. If a different operating system was implemented outside of the ones listed above, please provide the name of the distribution being used along with the use case  
  * If partner is not using Amazon ECS optimized AMIs, please provide justification as to why  
* **ECS-013 \- Partner has mechanism for addressing compliance standards and frameworks for workloads that must adhere to regulatory compliance standards i.e SOC, PCI, FedRAMP, HIPAA, etc. A comprehensive list of AWS service that in scope by compliance program can be found \[here\](http://aws.amazon.com/compliance/services-in-scope/)**  
  Partners that are working with customers in which the underlying workloads must adhere to compliance standards and frameworks carry the compliance responsibility of ensuring that the sensitivity of customer data, customers compliance objectives, and applicable laws and regulations are addressed based on the specific compliance standard the customer needs to adhere to. *Note that if the customer references do not require to adhere to regulatory or compliance standards, the partner may answer with N/A.*  
  Please provide the following as evidence:  
  * Description of internal processes and tooling used to address customer workloads that must adhere to regulatory compliance standards  
  * Description of operational run books that is passed off to the customer after the workload has been implemented that outlines the regulatory compliance guidelines needed to address third-party audits  
* **ECS-014 \- Amazon ECS capacity deployed on-prem or at different edge locations must follow the best practices for leveraging ECS-A. Applies to Partners deploying solutions that leverage ECS-A. Note that this control is not mandatory for case studies submitted that do not cover on-prem/edge deployments leveraging ECS-A.**  
  Amazon ECS capacity being deployed on-prem or at different edge locations must follow the best practices for leveraging ECS-A which can be found here (https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-anywhere.html).  
  Partners that are leveraging ECS-A for deploying capacity on-prem or at various edge locations must provide the following as evidence  
  * Description and/or guidance given to customers that demonstrates the ability to deploy ECS-Anywhere capacity across different environments outside of AWS.  
  * Description and/or guidance given to customers that demonstrates the ability to provision ECS-A capacity at different edge locations. AWS Outposts is considered a valid edge location.  
* **ECS-015 \- Partner has a defined mechanism for ingress to control and configure network traffic into the ECS cluster.**  
  Partner should have a strategy around how to control network traffic that is going into the tasks to securely allow traffic into the tasks. This includes specifying the ingress controller of choice and specifying a set of rules to configure ingress traffic. *All layer 7 traffic must be secured with TLS or mTLS.*  
  Please provide the following as evidence:  
  * Description of the ingress controller and infrastructure like: VPCs, NAT Gateways, Subnets, and ENIs and their configurations. Partners may also provide screenshot or pseudo-code that describes how the ingress method of choice is configured to securely allow traffic into the tasks.  
  * Description of network modes and load balancing systems and their associated configurations; along with elaborations on why certain strategies were used.  
* **ECS-016 \- Partner has a defined mechanism to address IP Exhaustion when deploying many tasks**  
  Partners deploying Tasks to Amazon ECS need to adhere to the potential networking concerns around IP exhaustion within the VPC that the tasks are being deployed to. There are a variety of mechanisms to address IP exhaustion with various systems available within Amazon ECS. Note that if auto-scaling groups or managed node groups are being used then this does not apply to Fargate use cases.  
  Please provide the following as evidence:  
  * Description on strategy about how to address IP exhaustion within the VPC that the ECS Tasks are being deployed to such as, Multiple subnets, custom ENI configurations with Trunking, changing task density based on official documentation found here:[AWS ECS Documentation for IP Exhaustion](https://docs.aws.amazon.com/pdfs/AmazonECS/latest/bestpracticesguide/bestpracticesguide.pdf#%5B%7B%22num%22%3A1407%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C72%2C213.821%2Cnull%5D)  
* **ECS-017 \- Partner has mechanisms to facilitate communication within the customer’s services, AWS Services and external systems.**  
  Partners deploying tasks to Amazon ECS need to consider the collection of customer tasks and ensure communication between them is facilitated without traversing external load balancers. There are a variety of mechanisms to permit communication within ECS, with AWS services and with other external systems.  
  Please provide the following as evidence:  
  * Description of networking choices made to connect to AWS Services, to customer services, to external systems such as, service mesh (ECS Service Connect or AppMesh), internal load balancers, integration with API gateway, etc based on official documentation found here: [AWS ECS Documentation for connectivity](https://docs.aws.amazon.com/pdfs/AmazonECS/latest/bestpracticesguide/bestpracticesguide.pdf#%5B%7B%22num%22%3A1436%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C72%2C712.8%2Cnull%5D)  
* **ECS-018 \- Solutions have proper observability mechanisms in place**  
  Partner must have proper observability mechanisms in place that address logging, metrics, and tracing with ability to drill down to the individual app/container level:  
  * Ability to collect and filter metrics at both the application/container layer and the infrastructure layer.  
  * Ability to capture metrics and logs during service-level scaling event  
  * Ability to support monitoring of several environments \- environments that span multiple AWS Regions, accounts, and/or hybrid (ECS & ECS Anywhere, if applicable)  
  * Ability to support distributed tracing to analyze and debug applications running within an Amazon ECS cluster  
* Please provide the following as evidence:  
  * Description of observability mechanism that addresses the above.  
* Persistent Storage: Partner should follow the best practices for persistent storage use to maintain reliability, availability and performance of the customer applications deployed within Amazon ECS  
* **ECS-019 \- Partners have selected storage options best suited for the needs of the application based upon scalability, access latency, performance and OS requirements**  
  Partner must determine the storage needs of the ECS tasks and provision the appropriate type of storage for the containers. Best-practice matching use cases for storage each type include:  
  * EFS for Linux containers on Fargate or EC2 with concurrent access and horizontal scalability requirements  
  * EBS for EC2 deployed transactional database applications with sub-millisecond latency requirements, that do not require a shared file system when scaled horizontally. (EBS is unavailable for Fargate deployments currently).  
  * External Database service integrations for workloads without ultra-low latency requirements  
  * EBS for workloads that require high performance storage during their lifecycle but do not require data persistence after task completion  
  * Docker Volumes plugin may be used for ECS tasks using the docker container runtime provided they are hosted on an EC2 instance with an EBS volume available to mount to, however use of this volume type may result in data loss if the instance is stopped and the task is relocated  
  * FSx for Windows File Server for clusters that contain windows instances  
  * Other 3rd party plugins or integrations may be used depending on the specific requirements for the workload and performance characteristics of the storage option selected  
* Please Provide the following as evidence:  
  * Description of the workload and storage selected, required (or expected) performance metrics needed and the reasoning for each storage/workload pairing  
* **ECS-020 \- Workloads using Amazon Elastic File System (EFS) for persistent storage provide a mount target in each availability zone that will host ECS tasks**  
  For workloads that utilize EFS, an Amazon ECS task can only mount an Amazon EFS file system if the Amazon EFS filesystem has a mount target in the Availability Zone the task runs in. The Partner must ensure all Availability zones that will run tasks have a mount point available so that storage is accessible throughout the cluster  
  Please provide the following as evidence:  
  * Confirmation of whether EFS was or was not used (If no EFS was used, this requirement is N/A)  
  * A list of the Availability zones that are expected to run tasks, and confirmation that access points have been made in each of these availability zones  
* **ECS-021 \- Access to Persistent Storage is secure and only accessible to applications that need it.**  
  Access restrictions can be applied via several methods:  
  * Security Groups can be configured to permit and deny traffic to EFS mount targets on port 2049 based upon the security group connected to the ECS instances, or when using awsvpc network mode within the cluster at the ECS task level  
  * ECS tasks can be configured to require an IAM role for file system access when mounting to the EFS file system. See Using IAM to control file system data access (https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html) in the Amazon Elastic File System User Guide.  
  * Amazon EFS access points are application-specific entry points into an Amazon EFS file system. You can use access points to enforce a user identity, including the user's POSIX groups, for all file system requests that are made through the access point. Access points can also enforce a different root directory for the file system. This is so that clients can only access data in the specified directory or its sub-directories.  
* Please Provide the following as evidence:  
  * Description of how access requirements were evaluated  
  * Description of the method chosen to secure access to only the entities requiring access  
  * Example configuration showing the access control in place (Security group configuration, IAM role based EFS access setup, EFS Access point identity requirements)  
* **ECS-022 \- Workloads using EBS to persist container data utilize task placement constraints appropriately to maintain access to data throughout the task lifecycle**  
  When using EBS to store data for tasks in Amazon EC2, it's recommended to use task placement constraints to ensure that the task and its data are kept together. This is important for applications that need to persist data after the task ends, like a MySQL database. For tasks that don't need to persist data, task placement constraints are not necessary. For example, a task that processes large amounts of data may need high performance storage, which EBS can provide, but data persistence is not important.  
  Please provide the following as evidence:  
  * List of EBS volumes and tasks associated with each volume  
  * Task description for each workload using an EBS volume, and data persistency requirements  
  * If the workload(s) required data to persist outside the task’s lifecycle, provide an example of the task placement constraints that will ensure restarted tasks are placed with the EBS volume they require  
* **ECS-023 \- Partner has mechanism for addressing multi-tenant workloads**  
  Partners that are implementing multi-tenant workloads on behalf of their customer must be aware of the various levels of tenancy that can be achieved on Amazon ECS. “Soft” isolation or multi-tenancy on Amazon ECS is the approach of leveraging task level resource quotas, tenant specific IAM roles for ECS tasks, and namespaces in AWS Cloud Map to create isolation boundaries between tasks within an Amazon ECS cluster.  
  Please provide the following as evidence:  
  * Task definition file used as part of the case study submitted that has resource quotas defined in the task file  
  * IAM role that is used as part of the case study submitted to isolate tenants operating within the same ECS cluster  
  * Namespace configuration defined for service discovery in AWS Cloud Map  
* Partners that need to adhere to highly-regulated industries or in SaaS environments where strong isolation is required, the partner must demonstrate that they understand the drawbacks of operating in an environment with strong multi-tenancy requirements. This typically includes tenants having their own fully isolated ECS cluster along with tenants having their own dedicated AWS account.  
  Please provide the following as evidence:  
  * Short description of the specific requirements set out by the client that constitutes operating in an environment with hard multi-tenancy.  
  * Description of a Tenant Operator being used to manage tenants within a cluster.  
  * Tooling/ISV solution to help run/manage multiple virtualized clusters on a single underlying cluster which allows for hard(er) multi-tenancy.  
  * Tooling/ISV solution to help run/manage multiple AWS accounts i.e AWS Organizations

## **Common Customer Reference Requirements**

**If you have completed an AWS Well-Architected Framework Review (WAFR) for the customer example which shows zero outstanding high-risk issues (HRIs) in the Security, Operational Excellence, and Reliability pillars, you are not required to provide evidence for the following requirements. Please upload an exported WAFR report for each of the customer example instead.**

All of the following requirements must be met by at least one of the two submitted customer examples. See specific evidence for each control. Refer to [calibration guide](https://partnercentral.awspartner.com/partnercentral2/s/resources?Id=0698W00000neE5cQAE) for example responses. All of the following requirements must be met by at least one of the submitted customer references. See specific evidence for each control.

### **Documentation**

Requirements in this category relate to the documentation provided for each customer example.

* **DOC-001 \- Provide Architecture diagram designed with scalability and high availability**  
  AWS Partner must submit architecture diagrams depicting the overall design and deployment of its AWS Partner solution on AWS as well as any other relevant details of the solution for the specific customer in question.  
  The submitted diagrams are intended to provide context to the AWS Solutions Architect conducting the Technical Validation. It is critical to provide clear diagrams with an appropriate level of detail that enable the AWS Solutions Architect to validate the other requirements listed below.  
  Each architecture diagram must show:  
  * All of the AWS services used  
  * How the AWS services are deployed, including virtual private clouds (VPCs), availability zones, subnets, and connections to systems outside of AWS.  
  * Elements deployed outside of AWS, e.g. on-premises components, or hardware devices.  
  * how design scales automatically \- Solution adapts to changes in demand. The architecture uses services that automatically scale such as Amazon S3, Amazon CloudFront, AWS Auto Scaling, and AWS Lambda.  
  * how design has high availability with multi-AZ or multi-region deployment. When intentional tradeoffs have been made (e.g. to optimize cost in favor of high availability), please explain the customer's requirements.  
* Please provide the following as evidence (required for all provided customer examples):  
  * An architecture diagram depicting the overall design and deployment of your solution on AWS.  
  * Explanation of how the major solutions elements will keep running in case of failure.  
  * Description of how the major solutions elements scale up automatically.

### **Secure Customer AWS Account Governance and Access**

Any AWS accounts created by the AWS Partner on behalf of the customer or AWS accounts that the AWS Partner administers as part of the engagement must meet the following requirements.

* **ACCT-001 \- Define Secure AWS Account Governance Best Practice**  
  AWS expects all Services Partners to be prepared to create AWS accounts and implement basic security best practices. Even if most of your customer engagements do not require this, you should be prepared in the event you work with a customer who needs you to create new accounts for them.  
  Establish internal processes regarding how to create AWS accounts on behalf of customers when needed, including:  
  * When to use root account for workload activities  
  * Enable MFA on root  
  * Set the contact information to corporate email address or phone number  
  * Enable CloudTrail logs in all region and protect CloudTrail logs from accidental deletion with a dedicated S3 bucket  
* Please provide the following as evidence:  
  * Documents describing Security engagement SOPs which met all the 4 criteria defined above. Acceptable evidence types are security training documents, internal wikis, or standard operating procedures documents.  
  * Description of how Secure AWS Account Governance is implemented in one (1) of the submitted customer examples.  
* **ACCT-002 \- Define identity security best practice on how to access customer environment by leveraging IAM**  
  Define standard approach to access customer-owned AWS accounts, including:  
  * Both AWS Management Console access and programmatic access using the AWS Command Line Interface or other custom tools.  
  * When and how to use temporary credentials such as IAM roles  
  * Leverage customer's existing enterprise user identities and their credentials to access AWS services through Identity Federation or migrating to AWS Managed Active Directory  
* Establish best practices around AWS Identity and Access Management (IAM) and other identity and access management systems, including:  
  * IAM principals are only granted the minimum privileges necessary. Wildcards in Action and Resource elements should be avoided as much as possible.  
  * Every AWS Partner individual who accesses an AWS account must do so using dedicated credentials  
* Please provide the following as evidence:  
  * Security engagement Standard Operation Procedure (SOP) which met all the 2 criteria defined above. Acceptable evidence types are: security training documents, internal wikis, standard operating procedures documents. Written descriptions in the self-assessment excel is not acceptable.  
  * Description of how IAM best practices are implemented in one (1) of the submitted customer examples.

### **Operational Excellence**

Requirements in this category relate to the ability of the AWS Partner and the customer to run and monitor systems to deliver business value and to continually improve supporting processes and procedures.

* **OPE-001 \- Define, monitor and analyze customer workload health KPIs**  
  AWS Partner has defined metrics for determining the health of each component of the workload and provided the customer with guidance on how to detect operational events based on these metrics.  
  Establish the capability to run, monitor and improve operational procedure by:  
  * Defining, collecting and analyzing workload health metrics w/AWS services or 3rd Party tool  
  * Exporting standard application logs that capture errors and aid in troubleshooting and response to operational events.  
  * Defining threshold of operational metrics to generate alert for any issues  
* Please provide the following as evidence:  
  * Standardized documents or guidance on how to develop customer workload health KPIs with the three components above  
  * Description of how workload health KPIs are implemented in (1) of the submitted customer examples.  
* **OPE-002 \- Define a customer runbook/playbook to guide operational tasks**  
  Create a runbook to document routine activities and guide issue resolution process with a list of operational tasks and troubleshooting scenarios covered that specifically addresses the KPI metrics defined in OPE-001.  
  Please provide the following as evidence:  
  * Standardized documents or runbook met the criteria defined above.  
* **OPE-003 \- Use consistent processes (e.g. checklist) to assess deployment readiness**  
  Deployments are tested or otherwise validated before being applied to the production environment. For example, DevOps pipelines used for the project for provisioning resources or releasing software and applications.  
  Use a consistent approach to deploy to customers including:  
  * A well-defined testing process before launching in production environment  
  * Automated testing components  
* Please provide the following as evidence:  
  * A deployment checklist example or written descriptions met all the criteria defined above.

### **Security \- Networking**

Requirements in this category focus on security best practices for Virtual Private Cloud (Amazon VPC) and other network security considerations.

* **NETSEC-001 \- Define security best practices for Virtual Private Cloud (Amazon VPC) and other network security considerations.**  
  Establish internal processes regarding how to secure traffic within VPC, including:  
  * Security Groups to restrict traffic between Internet and Amazon VPC  
  * Security Groups to restrict traffic within the Amazon VPC  
  * Network ACL to restrict inbound and outbound traffic  
  * Other AWS security services to protect network security  
* Please provide the following as evidence:  
  * Written descriptions/documents on network security best practices met the criteria defined above.  
  * Description of how network security is implementation in one (1) of the submitted customer examples.  
* **NETSEC-002 \- Define data encryption policy for data at rest and in transit**  
  Establish internal processes regarding a data encryption policy used across all customer projects  
  * Summary of any endpoints exposed to the Internet and how traffic is encrypted  
  * Summary of processes that make requests to external endpoints over the Internet and how traffic is encrypted  
  * Enforcing encryption at rest. By default you should enable the native encryption features in an AWS service that stores data unless there is a reason not to.  
* All cryptographic keys are stored and managed using a dedicated key management solution  
  Please provide the following as evidence:  
  * Data encryption and key management policy met the criteria defined above.  
  * Description of how data encryption is implementation in one (1) of the submitted customer examples.

### **Reliability**

Requirements in this section focus on the ability of the AWS Partner solution to prevent, and quickly recover from failures to meet business and customer demand.

* **REL-001 \- Automate Deployment and leverage infrastructure-as-code tools.**  
  Changes to infrastructure are automated for customer implementation  
  * Tools like AWS CloudFormation, the AWS CLI, or other scripting tools were used for automation.  
  * Changes to the production environment were not done using the AWS Management Console.  
* Please provide the following as evidence:  
  * Written description of deployment automation and an example template (e.g., CloudFormation templates, architecture diagram for CI/CD pipeline) met the criteria defined above.  
* **REL-002 \- Plan for disaster recovery and recommend Recoverty Time Objective (RTO) and Recoverty Point Objective (RPO).**  
  Incorporate resilience discussion and advise a RTO\&PRO target when engaging with customer. Customer acceptance and adoption on RTO/RPO is not required.  
  * Establish a process to establish workload resilience including:  
  * RTO & RPO target  
  * Explanation of the recovery process for the core components of the architecture  
  * Customer awareness and communication on this topic  
* Please provide the following as evidence:  
  * Descriptions or documents on workload resilience guidance met the three criteria defined above  
  * Description of how resilience is implementation in one (1) of the submitted customer examples including reasons for exception when RTO\&RPO is not defined

### **Cost Optimization**

Requirements in this category relate to the AWS Partner's ability to help customers run systems that deliver business value at the lowest price point.

* **COST-001 \- Develop total cost of ownership analysis or cost modelling**  
  Determine solution costs using right sizing and right pricing for both technical and business justification.  
  Conducted TCO analysis or other form of cost modelling to provide the customer with an understanding of the ongoing costs including all the following 3 areas:  
  * Description of the inputs used to estimate the cost of the solution  
  * Summary of the estimates or cost model provided to the customer before implementation  
  * Business value analysis or value stream mapping of AWS solution  
* Please provide the following as evidence:  
  * Description of how to develop cost analysis or modeling with the critical components defined above  
  * Cost analysis example in one (1) of the submitted customer examples. Acceptable evidence types are: price calculator link, reports or presentations on business values analysis

## **Resources**

[AWS Specialization Program Guide](https://partnercentral.awspartner.com/partnercentral2/s/resources?Id=0698a00000BpB2yAAF)

Provides step-by-step instructions when applying for an AWS Specialization.

[AWS Specialization Program Benefits Guide](https://partnercentral.awspartner.com/partnercentral2/s/resources?Id=0698W00000dzAkaQAE)

Provides a deeper description of the AWS Service Delivery benefits.

[How to build a microsite](https://partnercentral.awspartner.com/partnercentral2/s/resources?Id=0698W00000wgPO4QAM)

Provides guidance on how to build a microsite to highlight your AWS Specialization.

[How to build a public case study](https://partnercentral.awspartner.com/partnercentral2/s/resources?Id=0698W00000wgPO9QAM)

Provides guidance on how to build a public customer case study that will showcase your success with AWS Customers.

[AWS Competency & Service Delivery Program Common Customer Example Requirement Calibration Guide](https://partnercentral.awspartner.com/partnercentral2/s/resources?Id=0698W00000neE5cQAE)

Provides control-by-control best practices, resources to implement, good example responses.

[How to build an architecture diagram](https://partnercentral.awspartner.com/partnercentral2/s/resources?Id=0690L000004kfwH)

Provides guidance on how to build an architecture diagrams that will meet program requirements.

[Well Architected Website](https://aws.amazon.com/architecture/well-architected/)

Learn about the Well Architected Framework and its approach.

[Changes between previous and current versions](https://apn-checklists.s3.amazonaws.com/changelog/Validation_Checklist_Change_Log.pdf)

Change Log
