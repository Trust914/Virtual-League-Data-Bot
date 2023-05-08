pipeline {
    agent any

    environment {
        registryCredential = "ecr:us-east-1:AWS_CREDENTIALS"
        appRegistry = "869704209971.dkr.ecr.us-east-1.amazonaws.com/leaguetest"
        leagueBotRegistry = "https://869704209971.dkr.ecr.us-east-1.amazonaws.com"
        //LAMBDA_FUNCTION_NAME = 'your-lambda-function-name'
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
    }
}