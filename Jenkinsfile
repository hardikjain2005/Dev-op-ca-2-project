// ============================================================
//  Jenkinsfile – Student Enrollment Portal CI Pipeline
//  Pipeline type : Declarative
//  Triggered by  : SCM poll / GitHub webhook
// ============================================================

pipeline {

    agent any

    // ── Global environment variables ──────────────────────────
    environment {
        PROJECT_NAME  = 'student-enrollment-portal'
        PYTHON        = 'python3'
        VENV_DIR      = '.venv'
        REPORTS_DIR   = 'reports'
    }

    // ── Limit concurrent builds ───────────────────────────────
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    stages {

        // ── Stage 1 : Source Checkout ─────────────────────────
        stage('Checkout') {
            steps {
                echo "Checking out source code for ${env.PROJECT_NAME}…"
                checkout scm
            }
        }

        // ── Stage 2 : Environment Setup ───────────────────────
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies…'
                sh """
                    ${PYTHON} -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install selenium
                """
            }
        }

        // ── Stage 3 : Static Analysis / Lint ──────────────────
        stage('Lint') {
            steps {
                echo 'Running static analysis with flake8…'
                sh """
                    . ${VENV_DIR}/bin/activate
                    pip install flake8 --quiet
                    flake8 test_enrollment_form.py \
                        --max-line-length=110 \
                        --statistics \
                        || true          # treat lint warnings as non-blocking
                """
            }
        }

        // ── Stage 4 : Selenium Tests ──────────────────────────
        stage('Run Selenium Tests') {
            steps {
                echo 'Executing Selenium test suite…'
                sh """
                    mkdir -p ${REPORTS_DIR}
                    . ${VENV_DIR}/bin/activate
                    ${PYTHON} -m pytest test_enrollment_form.py \
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

        // ── Stage 5 : Archive Artifacts ───────────────────────
        stage('Archive') {
            steps {
                echo 'Archiving build artifacts…'
                archiveArtifacts artifacts: "${REPORTS_DIR}/**", allowEmptyArchive: true
            }
        }

    }   // end stages

    // ── Post-build actions ────────────────────────────────────
    post {
        success {
            echo "✅ Pipeline succeeded for build #${env.BUILD_NUMBER}."
        }
        failure {
            echo "❌ Pipeline failed for build #${env.BUILD_NUMBER}. Check the console output."
        }
        always {
            cleanWs()   // clean workspace after every run
        }
    }

}
