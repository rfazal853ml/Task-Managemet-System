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
                script {
                    echo "Building branch: ${env.GIT_BRANCH}"
                    if (env.CHANGE_ID) {
                        echo "PR #${env.CHANGE_ID}: ${env.CHANGE_BRANCH} → ${env.CHANGE_TARGET}"
                    }
                }
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                bat '''
                    cd backend
                    echo === Creating virtual environment ===
                    python -m venv venv
                    echo.
                    echo === Activating virtual environment ===
                    call venv\\Scripts\\activate.bat
                    echo.
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
                    call venv\\Scripts\\activate.bat
                    echo === Running pytest ===
                    pytest test_api.py -v --cov=main --cov-report=term
                '''
            }
        }
        
        stage('Merge PR') {
            when {
                allOf {
                    expression { env.CHANGE_TARGET == 'master' }
                    expression { env.CHANGE_BRANCH == 'development' }
                }
            }
            steps {
                script {
                    echo "✅ Tests passed! Merging PR..."
                    
                    withCredentials([usernamePassword(
                        credentialsId: env.GITHUB_CREDENTIALS,
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_PASSWORD'
                    )]) {
                        bat """
                            git config user.name "Jenkins CI"
                            git config user.email "jenkins@cicd.local"
                            git fetch origin
                            git checkout master
                            git pull origin master
                            git merge origin/development --no-ff -m "Auto-merge PR: Tests Passed ✓"
                            git push https://%GIT_USERNAME%:%GIT_PASSWORD%@github.com/%REPO_OWNER%/%REPO_NAME%.git master
                        """
                    }
                }
            }
        }
        
        stage('Merge Direct Push') {
            when {
                allOf {
                    expression { env.CHANGE_ID == null }
                    anyOf {
                        branch 'development'
                        expression { env.GIT_BRANCH == 'origin/development' }
                    }
                }
            }
            steps {
                script {
                    echo "✅ Tests passed! Merging to master..."
                    
                    withCredentials([usernamePassword(
                        credentialsId: env.GITHUB_CREDENTIALS,
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_PASSWORD'
                    )]) {
                        bat """
                            git config user.name "Jenkins CI"
                            git config user.email "jenkins@cicd.local"
                            git fetch origin
                            git checkout master
                            git pull origin master
                            git merge origin/development --no-ff -m "Auto-merge: Tests Passed ✓"
                            git push https://%GIT_USERNAME%:%GIT_PASSWORD%@github.com/%REPO_OWNER%/%REPO_NAME%.git master
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ BUILD SUCCESSFUL - Tests passed and merged!'
        }
        failure {
            echo '❌ BUILD FAILED - Tests failed, NOT merged'
        }
        always {
            cleanWs()
        }
    }
}