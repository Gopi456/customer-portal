pipeline {

    agent any

    environment {
        IMAGE_NAME = 'customer-portal'
        CONTAINER_NAME = 'customer-portal-test'
        APP_PORT = '8080'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'

                git(
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/Gopi456/customer-portal.git',
                    branch: 'main'
                )
            }
        }

        stage('Build') {
            steps {
                echo 'Building application...'

                bat '"C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'

                bat '"C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'

                bat '"C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:build-${BUILD_NUMBER}"

                bat "docker build -t ${IMAGE_NAME}:build-${BUILD_NUMBER} ."
            }
        }

        stage('Container Verification') {
            steps {
                echo 'Starting temporary container...'

                bat "docker run -d --name ${CONTAINER_NAME} -p 8080:8080 ${IMAGE_NAME}:build-${BUILD_NUMBER}"

                echo 'Waiting for application to start...'

                sleep time: 5, unit: 'SECONDS'

                echo 'Checking application health endpoint...'

                bat 'curl --fail http://localhost:8080/health'
            }
        }
    }

    post {

        always {
            echo 'Cleaning up temporary container...'

            bat "docker rm -f ${CONTAINER_NAME} || exit 0"
        }

        success {
            echo "Pipeline completed successfully."
            echo "Docker image: ${IMAGE_NAME}:build-${BUILD_NUMBER}"
        }

        failure {
            echo "Pipeline failed."
        }
    }
}