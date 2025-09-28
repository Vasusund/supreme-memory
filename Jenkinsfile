pipeline {
    agent any

    environment {
        PYTHON = "python3"
        PATH = "$PATH:/Users/vasusund8556/Library/Python/3.9/bin"
    }

    stages {
        stage('Checkout') { steps { checkout scm } }

        stage('Build') {
            steps {
                echo 'Building the project and creating artefact...'
                sh "${PYTHON} -m pip install --upgrade pip"
                sh "${PYTHON} -m pip install -r requirements.txt"
                sh "zip -r app_build.zip . -x '*.git*' '*.venv*'"
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
                echo 'Running security checks with bandit...'
                sh "${PYTHON} -m pip install bandit"
                sh "bandit -r . -ll"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application to test environment...'
                sh "nohup ${PYTHON} app.py &"
            }
        }

        stage('Release') {
            steps {
                echo 'Releasing application to production...'
                sh "git tag v1.0.${BUILD_NUMBER}"
                sh "git push origin --tags"
                sh "cp app_build.zip ~/prod_release/"
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Monitoring application...'
                sh "ps aux | grep app.py"
                sh "curl -s http://localhost:5000 || echo 'App not running!'"
            }
        }
    }

    post { always { echo 'Cleaning up...' } }
}
