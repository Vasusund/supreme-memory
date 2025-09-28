pipeline {
    agent any

    environment {
        VENV = "${WORKSPACE}/venv"
    }

    stages {
        stage('Build') {
            steps {
                echo "Setting up virtual environment and installing dependencies"
                sh 'python3 -m venv venv'
                sh '${VENV}/bin/pip install --upgrade pip'
                sh '${VENV}/bin/pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo "Running unit tests"
                sh '${VENV}/bin/python -m unittest discover tests'
            }
        }

        stage('Code Quality') {
            steps {
                echo "Running code quality analysis"
                sh '${VENV}/bin/pip install flake8'
                sh '${VENV}/bin/flake8 --max-line-length=120 .'
            }
        }

        stage('Security') {
            steps {
                echo "Checking for security vulnerabilities"
                sh '${VENV}/bin/pip install bandit'
                sh '${VENV}/bin/bandit -r .'
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying to test environment"
                sh 'cp -r . ~/hd-todo-test-env/'
            }
        }

        stage('Release') {
            steps {
                echo "Simulating release to production"
                sh 'cp -r ~/hd-todo-test-env/ ~/hd-todo-prod-env/'
            }
        }

        stage('Monitoring') {
            steps {
                echo "Monitoring app logs"
                sh 'tail -n 20 ~/hd-todo-prod-env/app.log || echo "No logs yet"'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
    }
}
