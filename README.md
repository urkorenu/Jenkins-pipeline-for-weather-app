# Jenkins Pipeline for Application Deployment

This README documents the process of setting up and running a Jenkins pipeline for deploying an application. The pipeline involves four EC2 instances running in containers, each playing a specific role.

## Overview

The pipeline consists of the following nodes:

- **GitLab**: Sends triggers to start the pipeline.
- **Jenkins Master**: Receives the push from GitLab and triggers the worker node.
- **Jenkins Worker**: Executes the pipeline steps.
- **Deployment Instance**: The target instance where the application is deployed if the process completes successfully.

## Network Configuration

- **Public Subnet**: Contains the Jenkins Master and GitLab instances. These instances are behind a NAT Gateway and are accessible through an Application Load Balancer (ALB).
- **Private Subnet**: Contains the Jenkins Worker and the Production (Deployment) Instance. These instances are isolated from direct internet access and communicate with the public subnet via the NAT Gateway.

## Node Configuration

### Node 1: GitLab
- **Purpose**: To manage the source code repository and send triggers to start the pipeline.

**Setup**:
- Host GitLab in a container on an EC2 instance within the public subnet.
- Use an Elastic IP for consistent access.

### Node 2: Jenkins Master
- **Purpose**: To receive the push from GitLab and trigger the Jenkins worker node.

**Setup**:
- Host Jenkins Master in a container on an EC2 instance within the public subnet.
- Set up Jenkins Master using Docker Compose.
- Ensure that the Jenkins Master can be accessed via the Application Load Balancer (ALB).

### Node 3: Jenkins Worker
- **Purpose**: To execute the pipeline steps.

**Setup**:
- Host Jenkins Worker in a container on an EC2 instance within the private subnet.
- Configure the worker to connect to the Jenkins Master.
- Set up the Jenkins Worker using a Dockerfile.

### Node 4: Deployment Instance
- **Purpose**: The target instance where the application is deployed.

**Setup**:
- Host the deployment environment in a container on an EC2 instance within the private subnet.
- Ensure the environment is configured to receive and run the deployed application.

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

1. Insert the private key into jenkins mater credentials and use it in the pipeline


