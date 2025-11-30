pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python3 -m pip install --upgrade pip'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                // --json-report generates results.json
                // "|| true" means pipeline continues even if tests fail
                sh 'pytest --json-report --json-report-file=results.json || true'
            }
        }
    }

    post {
        always {
            // Always notify, even if tests fail or error
            sh 'python3 notify.py || true'
        }
    }
}
