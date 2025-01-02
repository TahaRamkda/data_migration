pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'schema-migration:latest'
        SCT_SCRIPT = 'schema_con.py'
        SCHEMA_TEST_SCRIPT = 'schema_test.py'
        MIGRATION_SCRIPT = 'migration.py'
        DATA_TEST_SCRIPT = 'data_test.py'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Run Schema Conversion') {
            steps {
                echo 'Running schema conversion script...'
                script {
                    def exitCode = sh(script: "docker run --rm ${DOCKER_IMAGE} python ${SCT_SCRIPT}", returnStatus: true)
                    if (exitCode != 0) {
                        error("Schema conversion script failed. Exiting pipeline.")
                    }
                }
            }
        }

        stage('Test Schema') {
            steps {
                echo 'Testing schema...'
                script {
                    def exitCode = sh(script: "docker run --rm ${DOCKER_IMAGE} python ${SCHEMA_TEST_SCRIPT}", returnStatus: true)
                    if (exitCode != 0) {
                        error("Schema testing failed. Exiting pipeline.")
                    }
                }
            }
        }

        stage('Run Migration Script') {
            steps {
                echo 'Running migration script...'
                script {
                    def exitCode = sh(script: "docker run --rm ${DOCKER_IMAGE} python ${MIGRATION_SCRIPT}", returnStatus: true)
                    if (exitCode != 0) {
                        error("Migration script failed. Exiting pipeline.")
                    }
                }
            }
        }

        stage('Test Data') {
            steps {
                echo 'Testing data migration accuracy...'
                script {
                    def exitCode = sh(script: "docker run --rm ${DOCKER_IMAGE} python ${DATA_TEST_SCRIPT}", returnStatus: true)
                    if (exitCode != 0) {
                        error("Data migration accuracy testing failed. Exiting pipeline.")
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker rmi ${DOCKER_IMAGE} || true'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
