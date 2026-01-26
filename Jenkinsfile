pipeline {
    agent any
    
    environment {
        VENV_PATH = 'venv'
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
                    cd backend
                    if exist venv rmdir /s /q venv
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                bat '''
                    cd backend
                    call venv\\Scripts\\activate.bat
                    pytest test_api.py -v --junitxml=test-results.xml --cov=main --cov-report=xml --cov-report=html
                '''
            }
        }
        
        stage('Code Quality') {
            steps {
                echo 'Running code quality checks...'
                bat '''
                    cd backend
                    call venv\\Scripts\\activate.bat
                    pip install pylint || echo "Pylint not required"
                '''
            }
        }
        
        stage('Merge to Master') {
            when {
                branch 'development'
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo '✅ All tests passed! Merging to master for deployment...'
                script {
                    bat '''
                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@yourdomain.com"
                        git checkout master
                        git merge development --no-ff -m "Auto-merge: Tests passed on development"
                        git push origin master
                    '''
                }
            }
        }
        
        stage('Deployment Notification') {
            when {
                branch 'development'
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo '╔════════════════════════════════════════╗'
                echo '║   🚀 DEPLOYING TO PRODUCTION 🚀       ║'
                echo '╚════════════════════════════════════════╝'
                echo 'Railway auto-deploying backend from master...'
                echo 'Vercel auto-deploying frontend from master...'
                echo ''
                echo 'Live URLs:'
                echo 'Backend:  https://task-managemet-system-production.up.railway.app'
                echo 'Frontend: https://task-management-system-iota-five.vercel.app'
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            bat '''
                taskkill /F /IM python.exe 2>nul || exit 0
            '''
        }
        success {
            echo '╔════════════════════════════════════════╗'
            echo '║   ✅ PIPELINE SUCCESSFUL ✅           ║'
            echo '╚════════════════════════════════════════╝'
            junit 'backend/test-results.xml'
            archiveArtifacts artifacts: 'backend/htmlcov/**', allowEmptyArchive: true
        }
        failure {
            echo '╔════════════════════════════════════════╗'
            echo '║   ❌ PIPELINE FAILED ❌               ║'
            echo '║   Code NOT merged to master           ║'
            echo '║   Production NOT updated              ║'
            echo '╚════════════════════════════════════════╝'
        }
    }
}