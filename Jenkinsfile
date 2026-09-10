pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                docker run --rm \
                  -e TESTING=1 \
                  -v "$WORKSPACE:/app" \
                  -w /app \
                  python:3.12-slim \
                  sh -c "pip install -r requirements.txt && python -m pytest -v"
                '''
            }
        }
    }
}