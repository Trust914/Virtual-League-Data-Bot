pipeline {
    agent any

    environment {
        registryCredential = "ecr:us-east-1:AWS_CREDENTIALS"
        appRegistry = "869704209971.dkr.ecr.us-east-1.amazonaws.com/league-project-docker-lambda"
        leagueBotRegistry = "https://869704209971.dkr.ecr.us-east-1.amazonaws.com"
        lambdaFunctionArn = 'arn:aws:lambda:us-east-1:869704209971:function:league-test'
    }

    stages {
        stage('Fetch code'){
            steps {
                 checkout([$class: 'GitSCM',
                            branches: [[name: '*/master' ]],
                            extensions: scm.extensions,
                            userRemoteConfigs: [[
                                url: 'https://github.com/Trust914/Virtual-League-Data-Bot.git',
                                credentialsId: 'GITHUB_CREDENTIALS'
                            ]]
                ])
            }
        }
        stage('Build App Image') {
            steps {
                script {
                    dockerImage = docker.build( appRegistry + ":$BUILD_NUMBER", "./")
                }
            }
        }
        stage('Upload App Image') {
             steps{
                script {
                    docker.withRegistry( leagueBotRegistry, registryCredential ) {
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
             }
        }

        stage('Update Lambda Function') {
            steps {
                script {
                    withAWS(region: "us-east-1", credentials: 'AWS_CREDENTIALS') {
                        sh "/usr/local/bin/aws lambda update-function-code --function-name arn:aws:${lambdaFunctionArn} --image-uri '${appRegistry}:$BUILD_NUMBER'"

                    }
                }
            }
        }
    }
}