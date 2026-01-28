pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = 'github-credentials'
        REPO_OWNER = 'rfazal853ml'
        REPO_NAME = 'Task-Managemet-System'
    }
    
    stages {
        stage('Verify PR Context') {
            steps {
                script {
                    echo "=== Build Information ==="
                    echo "Branch: ${env.GIT_BRANCH}"
                    echo "PR Number: ${env.CHANGE_ID}"
                    echo "Source Branch: ${env.CHANGE_BRANCH}"
                    echo "Target Branch: ${env.CHANGE_TARGET}"
                    echo "========================="
                    
                    // Only proceed if this is a PR
                    if (!env.CHANGE_ID) {
                        echo "⚠️ This is not a Pull Request. Pipeline will skip merge stage."
                    } else {
                        echo "✓ This is PR #${env.CHANGE_ID}"
                    }
                }
            }
        }
        
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    if (env.CHANGE_ID) {
                        echo "Building PR #${env.CHANGE_ID}: ${env.CHANGE_BRANCH} → ${env.CHANGE_TARGET}"
                    } else {
                        echo "Building branch: ${env.GIT_BRANCH}"
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
                    pytest test_api.py -v --cov=main --cov-report=term --cov-report=xml
                '''
            }
        }
        
        stage('Auto-Merge PR to Master') {
            when {
                allOf {
                    expression { env.CHANGE_ID != null }
                    expression { env.CHANGE_BRANCH == 'development' }
                    expression { env.CHANGE_TARGET == 'master' }
                }
            }
            steps {
                script {
                    echo "✅ All tests passed!"
                    echo "Auto-merging PR #${env.CHANGE_ID}: development → master"
                    
                    withCredentials([usernamePassword(
                        credentialsId: env.GITHUB_CREDENTIALS,
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_PASSWORD'
                    )]) {
                        bat """
                            git config user.name "Jenkins CI"
                            git config user.email "jenkins@cicd.local"
                            
                            echo === Fetching all branches ===
                            git fetch origin
                            
                            echo === Available branches ===
                            git branch -a
                            
                            echo === Checking out master ===
                            git checkout master || git checkout -b master origin/master
                            
                            echo === Pulling latest master ===
                            git pull origin master
                            
                            echo === Merging development into master ===
                            git merge origin/development --no-ff -m "Auto-merge PR #${env.CHANGE_ID}: development -> master [Jenkins CI - Tests Passed ✓]"
                            
                            echo === Pushing to master ===
                            git push https://%GIT_USERNAME%:%GIT_PASSWORD%@github.com/%REPO_OWNER%/%REPO_NAME%.git master
                            
                            echo.
                            echo ==========================================
                            echo   SUCCESS! PR #${env.CHANGE_ID} MERGED
                            echo   Railway and Vercel deploying...
                            echo ==========================================
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo '================================================'
                echo '✅ BUILD SUCCESSFUL!'
                echo '================================================'
                if (env.CHANGE_ID) {
                    echo "PR #${env.CHANGE_ID} tests passed ✓"
                    echo "Merged development → master ✓"
                    echo 'Railway & Vercel deploying ✓'
                } else {
                    echo 'Tests passed ✓'
                }
                echo '================================================'
            }
        }
        failure {
            script {
                echo '================================================'
                echo '❌ BUILD FAILED!'
                echo '================================================'
                if (env.CHANGE_ID) {
                    echo "PR #${env.CHANGE_ID} tests FAILED ❌"
                    echo 'PR will NOT be merged'
                } else {
                    echo 'Tests failed ❌'
                }
                echo 'Please fix issues and try again'
                echo '================================================'
            }
        }
        always {
            cleanWs()
        }
    }
}