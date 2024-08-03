# Jenkins Pipeline for Application Deployment

This README documents the process of setting up and running a Jenkins pipeline for deploying an application. The pipeline involves four EC2 instances running in containers, each playing a specific role.

## Overview

The pipeline consists of the following nodes:
1. **GitLab**: Sends triggers to start the pipeline.
2. **Jenkins Master**: Receives the push from GitLab and triggers the worker node.
3. **Jenkins Worker**: Executes the pipeline steps.
4. **Deployment Instance**: The target instance where the application is deployed if the process completes successfully.

## Node Configuration

### Node 1: GitLab
**Purpose**: To manage the source code repository and send triggers to start the pipeline.

**Setup**:
- Host GitLab in a container on an EC2 instance.
- Use an Elastic IP for consistency.

### Node 2: Jenkins Master
**Purpose**: To receive the push from GitLab and trigger the Jenkins worker node.

**Setup**:
- Host Jenkins Master in a container on an EC2 instance.
- Set up using Docker Compose.

### Node 3: Jenkins Worker
**Purpose**: To execute the pipeline steps.

**Setup**:
- Host Jenkins Worker in a container on an EC2 instance.
- Configure the worker to connect to the Jenkins master.
- Set up using a Dockerfile.

### Node 4: Deployment Instance
**Purpose**: The target instance where the application is deployed.

**Setup**:
- Host the deployment environment in a container on an EC2 instance.
- Ensure the environment is configured to receive and run the deployed application.

## Pipeline Configuration

### Step 1: Trigger from GitLab
- Configure GitLab to send a trigger to Jenkins upon code push or merge request:
  - Go to **Admin Settings > Network > Inbound** and allow local IPs.
  - In your project, go to **Settings > Integrations**.
  - Select Jenkins.
  - Create a new integration and choose what will trigger it.
  - Enter the Jenkins server URL.
  - Enter the Jenkins pipeline name (project).
  - Enter Jenkins credentials.

### Step 2: Jenkins Master Job
**Setting up the container**:
- Run `docker container ls` to list containers.
- Run `docker container logs jenkins_container` to get the initial admin password.
- Go to `http://your-server-ip:8080` and set up Jenkins using the password.

**Create a job in Jenkins Master to listen for the GitLab integration**:
- Install the `gitlab-plugin`.
- Go to **Manage Jenkins > Configure System**.
- In the GitLab section, enable the integration.
- Add Jenkins credential provider.
- Paste the GitLab API token.
- Enter the GitLab host URL.
- Test the connection.
- Configure the job to trigger the pipeline execution on the Jenkins worker:
  - On the pipeline, select GitLab connection.
  - Choose what triggers to accept.
  - Add DockerHub integration.
  - Add credentials (username and password) and give it an ID.

### Step 3: Pipeline Execution on Jenkins Worker
**Setting up the container**:
- Build and run the image.
- Go to Jenkins Master and add a new node. Give it a descriptive name.
- Paste `/var/jenkins_home` in the Remote root directory and create the node.
- Click on the new node.
- Run `docker exec -it <id> /bin/bash` to access the container.
- Download and execute the Jenkins agent jar file.

**Define the pipeline steps in a Jenkinsfile**.

### Step 4: Deployment to Target Instance
**EC2**:
- Launch an EC2 instance and install Docker.
- Allow SSH from the private IP of the worker instance in the security group.
- Log in to DockerHub.

**Jenkins Master**:
- Install the `ssh-agent` plugin.
- Add SSH credentials (username with private key).
  - Username: `ec2-user`
  - Paste the private key downloaded when the instance was created.

**Jenkins Worker**:
- Exec into the container.
- Generate an SSH key.
- Paste the public key into the instance's `authorized_hosts` file.

## Monitoring and Logging
- Set up a Slack server and channels for logs.

**Integration**:
- On Slack:
  - Go to **Settings > Manage Apps** and search for Jenkins CI.
  - Keep the page with credentials open.

- On Jenkins:
  - Install the `slack-notifications` plugin.
  - Go to **Manage Jenkins > Add Credentials**.
  - Select kind as `Secret Text`.
  - Enter the secret key and ID.
  - Go to **Manage Jenkins > System**.
  - Scroll down to the Slack section.
  - Workspace: Enter your team subdomain.
  - Select credentials and default channel.
  - Add syntax to the Jenkinsfile for Slack notifications.
