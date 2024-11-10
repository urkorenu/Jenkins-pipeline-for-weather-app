def dockerImageApp = ''
def appContainerId = ''

pipeline {
    environment {
        registry_app = "urkoren/do19"
        registryCredential = 'docker-cred'
        slackChannelSuccess = '#success-builds'
        slackChannelFailure = '#fail-builds'
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        AWS_DEFAULT_REGION = 'eu-north-1'
    }
    agent {
        docker {
            label 'node_for_docker'
            image 'urkoren/jenkins-worker:1'
            args '-u 0:0 -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage("Clone Git Repository") {
            steps {
                // cleanWs()
                checkout scmGit(
                    branches: [[name: 'refs/heads/main']],
                    extensions: [],
                    userRemoteConfigs: [[credentialsId: 'git-cred2', url: 'http://13.50.133.63/root/weatherapp']]
                )

                script {
                    sh '''
                    #!/bin/bash
                    git config --global --add safe.directory /home/ubuntu/workspace/weather-app-pipeline
                    '''

                    // Run git command and capture output
                    def branchOutput = sh(script: "git branch -r --contains origin/main || echo 'No branches found'", returnStdout: true).trim()
                    if (branchOutput.contains('No branches found')) {
                        error("No branches found that contain 'origin/main'")
                    } else {
                        BRANCH_NAME = branchOutput
                        echo "Branch: ${BRANCH_NAME}"
                    }
                }
            }
        }

        stage('Test') {
            steps {
                sh 'pylint --output-format=parseable --fail-under=1 ./weather_project/*.py'
            }
        }

        stage("Build Docker Images") {
            steps {
                script {
                    dockerImageApp = docker.build("${registry_app}:${BUILD_NUMBER}", "./app")
                    dockerImageAppLatest = docker.build("${registry_app}:latest", "./app")
                }
            }
        }

        stage('Running Images') {
            steps {
                script {
                    appContainerId = sh(script: 'docker run -p 5001:5001 -d "${registry_app}:${BUILD_NUMBER}"', returnStdout: true).trim()
                }
            }
        }

        stage('Connectivity Test') {
            steps {
                script {
                    def result = sh(script: "python3 app/tests/check_connectivity.py", returnStatus: true)

                    if (result != 200) {
                        error "Connectivity test failed"
                    }
                }
            }
        }


        stage('Push Images') {
            when {
                expression { BRANCH_NAME == 'origin/main' }
            }
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImageApp.push()
                    }
                }
            }
        }

        stage('Setup EKS') {
            when {
                expression { BRANCH_NAME == 'origin/main' }
            }
            steps {
                sh 'aws eks update-kubeconfig --name production-test-cluster --region $AWS_DEFAULT_REGION'
            }
        }

        stage('Helm Deploy') {
            when {
                expression { BRANCH_NAME == 'origin/main' }
            }
            steps {
                script {
                    sh 'helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace'
                    sh 'kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/name=ingress-nginx --timeout=120s'
                    // Extract Load Balancer DNS name
                    def lbDns = sh(script: 'kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath="{.status.loadBalancer.ingress[0].hostname}"', returnStdout: true).trim()
                    sh "helm upgrade --install 'my-release' './helm' --set ingress.host=${lbDns}"
                    echo "Helm deployment completed successfully with Load Balancer DNS: ${lbDns}"
                }
            }
        }
    }

    post {
        always {
            script {
                try {
                    sh "docker stop ${appContainerId} && docker rm ${appContainerId}"
                } catch (Exception err) {
                    echo "Error during container cleanup: ${err.getMessage()}"
                }
            }
        }

        success {
            slackSend(
                channel: slackChannelSuccess,
                color: 'good',
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} \n build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
            )
            updateGitlabCommitStatus name: 'build', state: 'success'
        }

        failure {
            slackSend(
                channel: slackChannelFailure,
                color: 'danger',
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} \n build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
            )
            updateGitlabCommitStatus name: 'build', state: 'failed'
        }
    }
}

