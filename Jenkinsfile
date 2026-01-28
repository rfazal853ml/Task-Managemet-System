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
                echo "Building PR from ${env.CHANGE_BRANCH} to ${env.CHANGE_TARGET}"
            }
        }
        
        stage('Verify Structure') {
            steps {
                bat '''
                    dir
                    echo.
                    dir backend
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat '''
                    cd backend
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                bat '''
                    cd backend
                    pytest test_api.py -v --cov=main --cov-report=term
                '''
            }
        }
        
        stage('Merge PR') {
            when {
                allOf {
                    expression { env.CHANGE_TARGET == 'main' }
                    expression { env.CHANGE_BRANCH == 'development' }
                }
            }
            steps {
                script {
                    echo "✅ Tests passed! Auto-merging PR..."
                    
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
                            git merge origin/development --no-ff -m "Auto-merge PR: Tests Passed ✓"
                            git push https://%GIT_USERNAME%:%GIT_PASSWORD%@github.com/%REPO_OWNER%/%REPO_NAME%.git main
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ Tests passed and PR merged!'
        }
        failure {
            echo '❌ Tests failed - PR NOT merged'
        }
        always {
            cleanWs()
        }
    }
}