pipeline {
    agent any

    environment {

        AWS_REGION = 'us-east-1'
        REGISTRY_CREDENTIALS = "ecr:$AWS_REGION:AWS_CREDENTIALS"
        LEAGUE_BOT_APP_REGISTRY = "869704209971.dkr.ecr.us-east-1.amazonaws.com/leaguetest"
        LEAGUE_BOT_REGISTRY = "https://869704209971.dkr.ecr.us-east-1.amazonaws.com"
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
                    withCredentials([aws(credentialsId: "AWS_CREDENTIALS", awsRegion: "${AWS_REGION}")])  {
                        sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${LEAGUE_BOT_REGISTRY}"
                        dockerImage = docker.build("${LEAGUE_BOT_APP_REGISTRY}:${BUILD_NUMBER}", "./")
                    }
                }
            }
       }

        stage('Upload App Image') {
            steps {
                script {
                    withCredentials([aws(credentialsId: 'aws-ecr-creds', passwordVariable: 'password', usernameVariable: 'username')]) {
                        docker.withRegistry("$LEAGUE_BOT_REGISTRY","$REGISTRY_CREDENTIALS") {
                            dockerImage.push("$BUILD_NUMBER")
                            dockerImage.push('latest')
                        }
                    }

//                     sh "aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --image-uri $ECR_REGISTRY:$BUILD_NUMBER"
                }
            }
        }
     }
}