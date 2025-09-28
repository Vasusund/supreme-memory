pipeline {
    agent any
    environment {
        PYTHON = "python3"
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh "${PYTHON} -m pip install --upgrade pip"
                sh "${PYTHON} -m pip install -r requirements.txt"
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh "${PYTHON} -m unittest discover tests"
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Checking code quality with flake8...'
                sh "${PYTHON} -m pip install flake8"
                sh "flake8 --max-line-length=120 ."
            }
        }

        stage('Security') {
            steps {
                echo 'Scanning dependencies with Bandit...'
                sh "${PYTHON} -m pip install bandit"
                sh "bandit -r . -lll"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to test environment...'
                sh "cp -r * /tmp/hd-todo-test/"  // Example simple deploy
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing to production...'
                sh "cp -r * /tmp/hd-todo-prod/"  // Example simple release
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking monitoring endpoint...'
                sh "curl -s http://127.0.0.1:5000/dashboard || echo 'App not running!'"
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
        }
    }
}
