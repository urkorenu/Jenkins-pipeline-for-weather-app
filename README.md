# Jenkins Pipeline for Application Deployment

This README documents the process of setting up and running a Jenkins pipeline for deploying an application. The pipeline involves five EC2 instances running in containers, each playing a specific role.

## Infrastructure Management

### Terraform

The infrastructure is provisioned and managed via **Terraform**, ensuring the automated setup and configuration of the environment. This includes the creation of the VPC, subnets, security groups, and the EKS cluster itself.

**Terraform Setup**:

1. **Install Terraform**: Ensure Terraform is installed locally or on the Jenkins worker node.
2. **Define Terraform Configuration**: In the `tf/` directory, define the configuration files for provisioning the AWS infrastructure (VPC, subnets, NAT gateway, EKS cluster, etc.).

## Pipeline Overview

The pipeline consists of the following nodes:

- **GitLab**: Sends triggers to start the pipeline.
- **Jenkins Master**: Receives the push from GitLab and triggers the worker node.
- **Jenkins Worker**: Executes the pipeline steps.
- **Deployment Instance**: The target instance where the application is deployed if the process completes successfully.
- **NAT Instance**: A NAT instance that enables traffic from the private subnet to the internet.

## Network Configuration

- **Public Subnet**: Contains the NAT instance, which provides internet access to instances in the private subnet.
- **Private Subnet**: Contains the Jenkins Worker, Jenkins Master, GitLab, and the Deployment Instance. These instances are isolated from direct internet access and communicate with the public subnet via the NAT Instance and are accessible through an Application Load Balancer (ALB).


   

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

### Step 1: Trigger from GitLab

Configure GitLab to send a trigger to Jenkins upon code push or merge request:

1. Go to **Admin Settings > Network > Inbound** and allow local IPs.
2. In your project, go to **Settings > Integrations**.
3. Select **Jenkins**.
4. Create a new integration and choose the events that will trigger it.
5. Enter the Jenkins server URL (pointing to the ALB).
6. Enter the Jenkins pipeline name (project).
7. Enter Jenkins credentials.

### Step 2: Jenkins Master Job

Setting up the container:

1. Run `docker container ls` to list containers.
2. Run `docker container logs jenkins_container` to get the initial admin password.
3. Go to `http://your-alb-dns-name:8080` and set up Jenkins using the password.
4. Create a job in Jenkins Master to listen for the GitLab integration:
   - Install the `gitlab-plugin`.
   - Go to **Manage Jenkins > Configure System**.
   - In the **GitLab** section, enable the integration.
   - Add Jenkins credential provider.
   - Paste the GitLab API token.
   - Enter the GitLab host URL.
   - Test the connection.
   - Configure the job to trigger the pipeline execution on the Jenkins Worker:
     - On the pipeline, select the GitLab connection.
     - Choose what triggers to accept.
     - Add DockerHub integration.
     - Add credentials (username and password) and give it an ID.

### Step 3: Pipeline Execution on Jenkins Worker

Setting up the container:

1. Build and run the image.
2. Go to Jenkins Master and add a new node. Give it a descriptive name.
3. Paste `/var/jenkins_home` in the **Remote root directory** and create the node.
4. Click on the new node.
5. Run `docker exec -it <id> /bin/bash` to access the container.
6. Download and execute the Jenkins agent jar file.
7. Define the pipeline steps in a `Jenkinsfile`.

### Step 4: Deployment to Target Instance

**EC2**:

1. Launch an EC2 instance and install Docker.
2. Allow SSH from the private IP of the worker instance in the security group.
3. Log in to DockerHub.

**Jenkins Master**:

1. Install the `ssh-agent` plugin.
2. Add SSH credentials (username with private key).
   - Username: `ec2-user`
   - Paste the private key downloaded when the instance was created.

**Jenkins Worker**:

1. Insert the private key into Jenkins master credentials and use it in the pipeline.

