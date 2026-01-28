pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = 'github-credentials'
        REPO_OWNER = 'rfazal853ml'
        REPO_NAME = 'Task-Managemet-System'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Building branch: ${env.GIT_BRANCH}"
            }
        }
        
        stage('Verify Structure') {
            steps {
                bat '''
                    echo === Repository Structure ===
                    dir
                    echo.
                    echo === Backend Folder Contents ===
                    dir backend
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat '''
                    cd backend
                    echo === Upgrading pip ===
                    python -m pip install --upgrade pip
                    echo.
                    echo === Installing requirements ===
                    pip install -r requirements.txt
                    echo.
                    echo === Installed packages ===
                    pip list
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                bat '''
                    cd backend
                    echo === Running pytest ===
                    pytest test_api.py -v --cov=main --cov-report=term --cov-report=xml
                '''
            }
        }
        
        stage('Merge to Main') {
            when {
                anyOf {
                    branch 'development'
                    expression { env.GIT_BRANCH == 'origin/development' }
                }
            }
            steps {
                script {
                    echo "✅ All tests passed! Merging development → main"
                    
                    withCredentials([usernamePassword(
                        credentialsId: env.GITHUB_CREDENTIALS,
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_PASSWORD'
                    )]) {
                        bat """
                            git config user.name "Jenkins CI"
                            git config user.email "jenkins@cicd.local"
                            
                            git fetch origin
                            git checkout main
                            git pull origin main
                            
                            git merge origin/development --no-ff -m "Auto-merge: development -> main [Jenkins CI - Tests Passed]"
                            
                            git push https://%GIT_USERNAME%:%GIT_PASSWORD%@github.com/%REPO_OWNER%/%REPO_NAME%.git main
                            
                            echo.
                            echo ========================================
                            echo   MERGE SUCCESSFUL!
                            echo   Railway and Vercel will auto-deploy
                            echo ========================================
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo '================================================'
            echo '✅ BUILD SUCCESSFUL!'
            echo '================================================'
            echo 'All tests passed ✓'
            echo 'Merged to main branch ✓'
            echo 'Auto-deployment triggered ✓'
            echo '================================================'
        }
        failure {
            echo '================================================'
            echo '❌ BUILD FAILED!'
            echo '================================================'
            echo 'Check console output for error details'
            echo '================================================'
        }
        always {
            cleanWs()
        }
    }
}