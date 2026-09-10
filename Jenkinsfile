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

stage('Push Docker image to GHCR') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: 'github-ghcr',
                usernameVariable: 'GHCR_USER',
                passwordVariable: 'GHCR_TOKEN'
            )
        ]) {
            sh '''
                echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin

                docker tag secure-task-api:${BUILD_NUMBER} \
                  ghcr.io/aminelm1/secure-task-api:${BUILD_NUMBER}

                docker tag secure-task-api:latest \
                  ghcr.io/aminelm1/secure-task-api:latest

                docker push ghcr.io/aminelm1/secure-task-api:${BUILD_NUMBER}
                docker push ghcr.io/aminelm1/secure-task-api:latest

                docker logout ghcr.io
            '''
        }
    }
}

    }
}