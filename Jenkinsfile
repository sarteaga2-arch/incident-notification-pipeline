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
                 sh """
                 python3 -m venv venv
                 . venv/bin/activate
                 pip install --upgrade pip
                 pip install -r requirements.txt
                 """
            }
        }

        stage('Run tests') {
            steps {
                sh """
                . venv/bin/activate
                pytest --json-report --json-report-file=results.json || true
                """
            }
        }
    }

    post {
        always {
            sh """
            . venv/bin/activate || true
            python3 notify.py || true
            """
        }
    }
}
