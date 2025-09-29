pipeline {
    agent any

    stages {
        stage('Checkout & Build') {
            steps {
                echo 'Cloning repo and building artefact...'
                git url: 'https://github.com/Vasusund/supreme-memory.git', branch: 'main'
                sh 'zip -r build-artifact.zip .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'pip install -r requirements.txt || true'
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running code quality checks with flake8...'
                sh 'pip install flake8 || true'
                sh 'flake8 . || true'
            }
        }

        stage('Security') {
            steps {
                echo 'Running dependency vulnerability scan...'
                sh 'pip install pip-audit || true'
                sh 'pip-audit || true'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying app locally for testing...'
                sh 'nohup python3 app.py & sleep 5'
                sh 'curl -s http://127.0.0.1:5000/ || true'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished (success or fail).'
        }
    }
}
