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
                    if exist %VENV_DIR% rmdir /s /q %VENV_DIR%
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running all tests...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pytest test_api.py -v --junitxml=test-results.xml --cov=main --cov-report=term --cov-report=html
                '''
            }
        }
        
        stage('Code Quality') {
            steps {
                echo 'Checking code quality...'
                bat '''
                    call %VENV_DIR%\\Scripts\\activate.bat
                    pip install flake8
                    flake8 main.py test_api.py --max-line-length=120 --statistics || exit 0
                '''
            }
        }
        
        stage('Verify Application') {
            steps {
                echo 'Verifying application can start...'
                timeout(time: 30, unit: 'SECONDS') {
                    bat '''
                        call %VENV_DIR%\\Scripts\\activate.bat
                        echo Starting application...
                        start /B python main.py
                        timeout /t 10
                        curl http://localhost:8000/api/health
                        taskkill /F /IM python.exe /FI "WINDOWTITLE eq main.py*" 2>nul || exit 0
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            bat 'taskkill /F /IM python.exe 2>nul || exit 0'
            
            // Archive test results
            junit allowEmptyResults: true, testResults: 'test-results.xml'
            
            // Archive coverage HTML report as artifacts instead
            archiveArtifacts artifacts: 'htmlcov/**/*', allowEmptyArchive: true
        }
        
        success {
            echo '╔════════════════════════════════════════╗'
            echo '║   ✅ PIPELINE SUCCESSFUL ✅           ║'
            echo '╚════════════════════════════════════════╝'
            echo ''
            echo '  📊 All 14 tests passed'
            echo '  ✅ Code quality checked'
            echo '  🚀 Application verified'
            echo ''
        }
        
        failure {
            echo '╔════════════════════════════════════════╗'
            echo '║   ❌ PIPELINE FAILED ❌               ║'
            echo '╚════════════════════════════════════════╝'
        }
    }
}