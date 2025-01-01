pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'schema-migration:latest'
        SCT_SCRIPT = 'schema_con.py'
        SCHEMA_TEST_SCRIPT = 'schema_test.py'
        DATA_TEST_SCRIPT = 'data_test.py'
        AWS_REGION = 'us-east-1' // Replace with your AWS region
        MIGRATION_TASK_ARN = 'arn:aws:dms:us-east-1:767397679048:task:7LTM2EIYEVAXTAMGBBDGC6BSHU'
        AWS_CREDENTIALS_ID = 'aws-credentials' // The ID of your AWS credentials in Jenkins
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                sh 'git clone -b main https://github.com/TahaRamkda/data_migration.git'
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
                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, region: AWS_REGION)]) {
                    script {
                        def exitCode = sh(script: "docker run --rm -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_REGION=${AWS_REGION} ${DOCKER_IMAGE} python ${SCT_SCRIPT}", returnStatus: true)
                        if (exitCode != 0) {
                            error("Schema conversion script failed. Exiting pipeline.")
                        }
                    }
                }
            }
        }

        stage('Test Schema') {
            steps {
                echo 'Testing schema...'
                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, region: AWS_REGION)]) {
                    script {
                        def exitCode = sh(script: "docker run --rm -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_REGION=${AWS_REGION} ${DOCKER_IMAGE} python ${SCHEMA_TEST_SCRIPT}", returnStatus: true)
                        if (exitCode != 0) {
                            error("Schema testing failed. Exiting pipeline.")
                        }
                    }
                }
            }
        }

        stage('Start Migration Task') {
            steps {
                echo 'Starting AWS DMS migration task...'
                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, region: AWS_REGION)]) {
                    sh "aws dms start-replication-task --replication-task-arn ${MIGRATION_TASK_ARN} --start-replication-task-type reload-target --region ${AWS_REGION}"
                }
            }
        }

        stage('Wait for Migration Completion') {
            steps {
                echo 'Waiting for AWS DMS migration task to complete...'
                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, region: AWS_REGION)]) {
                    script {
                        def maxRetries = 60 // Maximum number of checks (1 hour total)
                        def delay = 60      // Delay between checks in seconds (1 minute)
                        def status = ""

                        for (int i = 0; i < maxRetries; i++) {
                            status = sh(script: "aws dms describe-replication-tasks --filters Name=replication-task-arn,Values=${MIGRATION_TASK_ARN} --region ${AWS_REGION} --query 'ReplicationTasks[0].Status' --output text", returnStdout: true).trim()
                            echo "Current migration status: ${status}"

                            if (status == "completed") {
                                echo "Migration task completed successfully."
                                break
                            } else if (status == "failed") {
                                error("Migration task failed. Exiting pipeline.")
                            }

                            sleep(delay)
                        }

                        if (status != "completed") {
                            error("Migration task did not complete within the expected time. Exiting pipeline.")
                        }
                    }
                }
            }
        }

        stage('Test Data') {
            steps {
                echo 'Testing data migration accuracy...'
                withCredentials([aws(credentialsId: AWS_CREDENTIALS_ID, region: AWS_REGION)]) {
                    script {
                        def exitCode = sh(script: "docker run --rm -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_REGION=${AWS_REGION} ${DOCKER_IMAGE} python ${DATA_TEST_SCRIPT}", returnStatus: true)
                        if (exitCode != 0) {
                            error("Data migration accuracy testing failed. Exiting pipeline.")
                        }
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
