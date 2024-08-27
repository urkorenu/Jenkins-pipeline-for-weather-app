def dockerImageApp = ''
def dockerImageAppLatest = ''
def appContainerId = ''

pipeline {
    environment {
        registry_app = "urkoren/do19"
        registryCredential = 'docker-cred'
        deploy_host = "172.31.33.25"
        deploy_user = "ec2-user"
        slackChannelSuccess = '#success-builds'
        slackChannelFailure = '#fail-builds'
    }
    agent any
    stages {
        stage("Clone Git Repository") {
            steps {
                updateGitlabCommitStatus name: 'build', state: 'pending'
                cleanWs()
                checkout scmGit(branches: [[name: env.GIT_BRANCH]],
                extensions: [],
                userRemoteConfigs: [[credentialsId: 'git-cred',
                url: 'http://51.21.112.83/do19/weather_app']])
            }
        }
        stage("Testing and Building") {
            parallel {
                stage("Testing with Pylint") {
                    when {
                        anyOf {
                            branch 'develop'
                            branch pattern: "feature/.*"
                        }
                    }
                    steps {
                        sh "/venv/bin/pylint --output-format=parseable --fail-under=5 --disable=E0401 app/"
                    }
                }
                stage("Build Docker Images") {
                    when {
                        anyOf {
                            branch 'develop'
                            branch pattern: "feature/.*"
                            branch 'release/*'
                            branch 'hotfix/*'
                            branch 'main'
                        }
                    }
                    steps {
                        script {
                            dockerImageApp = docker.build("${registry_app}:${BUILD_NUMBER}", "./app")
                            dockerImageAppLatest = docker.build("${registry_app}:latest", "./app")
                        }
                    }
                }
            }
        }
        stage('Running Images') {
            when {
                anyOf {
                    branch 'develop'
                    branch pattern: "feature/.*"
                    branch 'release/*'
                    branch 'hotfix/*'
                    branch 'main'
                }
            }
            steps {
                script {
                    appContainerId = sh(script: 'docker run -p 5001:5001 -d "${registry_app}:${BUILD_NUMBER}"', returnStdout: true).trim()
                }
            }
        }
        stage('Push Images') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImageApp.push()
                        dockerImageAppLatest.push()
                    }
                }
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sshagent(['ssh-app']) {
                        sh "scp -o StrictHostKeyChecking=no compose.yaml ${deploy_user}@${deploy_host}:/home/${deploy_user}/docker-compose.yml"
                        sh "scp -o StrictHostKeyChecking=no nginx/flask.conf ${deploy_user}@${deploy_host}:/home/${deploy_user}/flask.conf"
                        sh "ssh -o StrictHostKeyChecking=no ${deploy_user}@${deploy_host} docker-compose down"
                        sleep 10
                        try {
                            sh "ssh -o StrictHostKeyChecking=no ${deploy_user}@${deploy_host} docker rmi -f \$(docker images -aq)"
                        } catch (Exception err) {
                            echo "Error during image cleanup: ${err.getMessage()}"
                        }
                        sh "ssh -o StrictHostKeyChecking=no ${deploy_user}@${deploy_host} docker-compose pull"
                        sh "ssh -o StrictHostKeyChecking=no ${deploy_user}@${deploy_host} docker-compose up -d"
                    }
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

