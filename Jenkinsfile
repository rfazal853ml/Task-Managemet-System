pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        VENV_DIR = 'venv'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest test_api.py -v --junitxml=test-results.xml --cov=main --cov-report=xml --cov-report=html
                '''
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo 'Running code quality checks...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pip install flake8
                    flake8 main.py --max-line-length=120 --ignore=E402,W503 || true
                '''
            }
        }
        
        stage('Start Application') {
            steps {
                echo 'Starting application for smoke test...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    nohup python main.py > app.log 2>&1 &
                    echo $! > app.pid
                    sleep 5
                '''
            }
        }
        
        stage('Smoke Test') {
            steps {
                echo 'Running smoke test...'
                sh '''
                    max_attempts=10
                    attempt=0
                    while [ $attempt -lt $max_attempts ]; do
                        if curl -f http://localhost:8000/api/health; then
                            echo "Health check passed!"
                            exit 0
                        fi
                        attempt=$((attempt + 1))
                        echo "Attempt $attempt failed, retrying..."
                        sleep 2
                    done
                    echo "Health check failed after $max_attempts attempts"
                    exit 1
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh '''
                if [ -f app.pid ]; then
                    kill $(cat app.pid) || true
                    rm app.pid
                fi
            '''
            
            // Archive test results
            junit 'test-results.xml'
            
            // Publish coverage report
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
        
        success {
            echo 'Pipeline completed successfully! ✅'
        }
        
        failure {
            echo 'Pipeline failed! ❌'
        }
    }
}