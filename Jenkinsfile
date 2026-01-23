pipeline {
    agent any
    
    environment {
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
                bat '''
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pytest test_api.py -v --junitxml=test-results.xml
                '''
            }
        }
        
        stage('Start Application') {
            steps {
                echo 'Starting application for smoke test...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    start /B python main.py
                    timeout /t 10 /nobreak
                '''
            }
        }
        
        stage('Smoke Test') {
            steps {
                echo 'Running smoke test...'
                bat '''
                    curl -f http://localhost:8000/api/health
                    if errorlevel 1 exit 1
                    echo Health check passed!
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            bat '''
                for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /F /PID %%a 2>nul
            '''
            
            // Archive test results if available
            junit allowEmptyResults: true, testResults: 'test-results.xml'
        }
        
        success {
            echo 'Pipeline completed successfully! ✅'
        }
        
        failure {
            echo 'Pipeline failed! ❌'
        }
    }
}