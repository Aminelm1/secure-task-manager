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
                  -w "$WORKSPACE" \
                  python:3.12-slim \
                  sh -c "pip install -r requirements.txt && python -m pytest -v"
                '''
            }
        }
    }
}