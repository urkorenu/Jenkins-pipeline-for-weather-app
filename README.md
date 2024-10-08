# Jenkins Pipeline for Application Deployment

This README documents the process of setting up and running a Jenkins pipeline for deploying an application. The pipeline involves five EC2 instances running in containers, each playing a specific role.

## Infrastructure Management

### Terraform

The infrastructure is provisioned and managed via **Terraform**, ensuring the automated setup and configuration of the environment. This includes the creation of the VPC, subnets, security groups, and the EKS cluster itself.

**Terraform Setup**:

1. **Install Terraform**: Ensure Terraform is installed locally or on the Jenkins worker node.
2. **Define Terraform Configuration**: In the `tf/` directory, define the configuration files for provisioning the AWS infrastructure (VPC, subnets, NAT gateway, EKS cluster, etc.).

## Pipeline Overview

The pipeline is designed for seamless application deployment using a combination of tools and services. It involves the following nodes and processes:

- **GitLab**: Serves as the source control and CI/CD trigger. Code changes in GitLab trigger the Jenkins pipeline through webhooks.
  
- **Jenkins Master**: Acts as the orchestrator, receiving the webhook triggers from GitLab and managing the overall flow of the pipeline. The Jenkins master delegates tasks to the worker node, including building Docker images, running Terraform, and deploying to EKS using Helm.

- **Jenkins Worker**: Executes the tasks in the pipeline, including:
  1. Cloning the GitLab repository.
  2. Building and pushing Docker images to the registry.
  3. Applying infrastructure changes via **Terraform**, including setting up or updating the AWS VPC, subnets, NAT gateway, and the **EKS cluster**.
  4. Deploying the application to the EKS cluster using **Helm**.
  
- **Deployment Instance**: The application is deployed to the Kubernetes cluster (EKS) via Helm, making it available for end-users.

- **NAT Instance**: This instance resides in the public subnet and provides internet access for instances in the private subnet, such as the Jenkins worker and deployment instances. It allows for communication with AWS services and external resources.

### Network Topology
- **Public Subnet**: Contains the NAT instance, which routes internet traffic to instances in the private subnet.
- **Private Subnet**: Hosts the Jenkins worker, Jenkins master, GitLab, and the deployment instance. These are isolated from direct internet access and communicate with the public subnet via the NAT instance.

### Deployment Steps:
1. **GitLab Trigger**: A push or merge request in GitLab triggers the Jenkins pipeline.
2. **Terraform Infrastructure**: The pipeline provisions or updates AWS infrastructure using **Terraform**, including the VPC, subnets, and EKS cluster.
3. **Docker Build**: The application is containerized using Docker, and the images are pushed to a Docker registry.
4. **EKS and Helm Deployment**: The EKS cluster is updated, and the application is deployed using **Helm**, including the configuration of ingress and services.


   

## Node Configuration

### Node 1: GitLab
- **Purpose**: Manages the source code repository and sends triggers to start the pipeline.

**Setup**:
- Host GitLab in a container on an EC2 instance within the private subnet.
- Use an Elastic IP for consistent access.

### Node 2: Jenkins Master
- **Purpose**: Receives the push from GitLab and triggers the Jenkins Worker node.

**Setup**:
- Host Jenkins Master in a container on an EC2 instance within the private subnet.
- Set up Jenkins Master using Docker Compose.
- Ensure that the Jenkins Master is accessible via the Application Load Balancer (ALB).

### Node 3: Jenkins Worker
- **Purpose**: Executes the pipeline steps.

**Setup**:
- Host Jenkins Worker in a container on an EC2 instance within the private subnet.
- Configure the Worker to connect to the Jenkins Master.
- Set up the Jenkins Worker using a Dockerfile.

### Node 4: Deployment Instance
- **Purpose**: The target instance where the application is deployed.

**Setup**:
- Host the deployment environment in a container on an EC2 instance within the private subnet.
- Ensure the environment is configured to receive and run the deployed application.

### Node 5: NAT Instance
- **Purpose**: Provides internet access for instances in the private subnet.

**Setup**:
- Host the NAT instance in the public subnet.
- Ensure proper routing and security group configuration for secure internet access.

## Pipeline Configuration


