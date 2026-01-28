pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = 'github-credentials'
        GITHUB_API_URL = 'https://api.github.com'
        REPO_OWNER = 'YOUR_USERNAME'
        REPO_NAME = 'YOUR_REPO'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    // Get PR number from environment
                    env.PR_NUMBER = sh(
                        script: "echo ${env.CHANGE_ID}",
                        returnStdout: true
                    ).trim()
                    echo "Processing PR #${env.PR_NUMBER}"
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'pytest test_api.py -v --cov=main'
            }
        }
        
        stage('Merge PR') {
            when {
                expression {
                    return env.CHANGE_TARGET == 'main' && 
                           env.CHANGE_BRANCH == 'development'
                }
            }
            steps {
                script {
                    withCredentials([string(
                        credentialsId: GITHUB_CREDENTIALS,
                        variable: 'GITHUB_TOKEN'
                    )]) {
                        sh """
                            curl -X PUT \
                              -H "Authorization: token ${GITHUB_TOKEN}" \
                              -H "Accept: application/vnd.github.v3+json" \
                              ${GITHUB_API_URL}/repos/${REPO_OWNER}/${REPO_NAME}/pulls/${env.PR_NUMBER}/merge \
                              -d '{"commit_title":"Auto-merge by Jenkins","merge_method":"merge"}'
                        """
                    }
                }
            }
        }
    }
    
    post {
        success {
            script {
                echo "✅ All tests passed!"
                // Update PR status
                updateGitHubStatus('success', 'All tests passed')
            }
        }
        failure {
            script {
                echo "❌ Tests failed!"
                updateGitHubStatus('failure', 'Tests failed')
            }
        }
    }
}

def updateGitHubStatus(state, description) {
    withCredentials([string(credentialsId: env.GITHUB_CREDENTIALS, variable: 'GITHUB_TOKEN')]) {
        sh """
            curl -X POST \
              -H "Authorization: token ${GITHUB_TOKEN}" \
              -H "Accept: application/vnd.github.v3+json" \
              ${env.GITHUB_API_URL}/repos/${env.REPO_OWNER}/${env.REPO_NAME}/statuses/${env.GIT_COMMIT} \
              -d '{"state":"${state}","description":"${description}","context":"Jenkins CI"}'
        """
    }
}