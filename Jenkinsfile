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
                  --volumes-from jenkins \
                  -e TESTING=1 \
                  -e DATABASE_URL="postgresql+psycopg://test:test@localhost:5432/testdb" \
                  -w "$WORKSPACE" \
                  python:3.12-slim \
                  sh -c "pip install -r requirements.txt && python -m pytest -v"
                '''
            }
        }

stage('Build Docker image') {
    steps {
        sh '''
        docker build \
          -t secure-task-api:${BUILD_NUMBER} \
          -t secure-task-api:latest \
          .
        '''
    }
}

    }
}