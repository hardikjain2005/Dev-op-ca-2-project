pipeline {

    agent any

    environment {
        PROJECT_NAME = 'student-feedback-portal'
        PROJECT_DIR  = '/Users/hardikjain/Downloads/DevOpsProject'
        PYTHON       = 'python3'
        VENV_DIR     = '.venv'
        REPORTS_DIR  = 'reports'
    }

    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Copying project files from ${env.PROJECT_DIR}…"
                sh """
                    cp -r ${PROJECT_DIR}/. .
                    echo "Files in workspace:"
                    ls -lh
                """
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment…'
                sh """
                    ${PYTHON} -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip --quiet
                    pip install selenium webdriver-manager pytest --quiet
                """
            }
        }

        stage('Lint') {
            steps {
                echo 'Running static analysis with flake8…'
                sh """
                    . ${VENV_DIR}/bin/activate
                    pip install flake8 --quiet
                    flake8 test_feedback_form.py --max-line-length=110 --statistics || true
                """
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Executing Selenium test suite…'
                sh """
                    mkdir -p ${REPORTS_DIR}
                    . ${VENV_DIR}/bin/activate
                    ${PYTHON} -m pytest test_feedback_form.py \
                        --tb=short \
                        --junit-xml=${REPORTS_DIR}/test-results.xml \
                        -v
                """
            }
            post {
                always {
                    junit "${REPORTS_DIR}/test-results.xml"
                }
            }
        }

        stage('Archive') {
            steps {
                echo 'Archiving build artifacts…'
                archiveArtifacts artifacts: "${REPORTS_DIR}/**", allowEmptyArchive: true
            }
        }

    }

    post {
        success {
            echo "✅ Pipeline succeeded for build #${env.BUILD_NUMBER}."
        }
        failure {
            echo "❌ Pipeline failed for build #${env.BUILD_NUMBER}. Check the console output."
        }
        always {
            cleanWs()
        }
    }

}
