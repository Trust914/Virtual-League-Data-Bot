pipeline {
    agent any

    environment {

        awsRegion  = 'us-east-1'
        awsCredentials = "ecr:$AWS_REGION:AWS_CREDENTIALS"
        appRegistry = "869704209971.dkr.ecr.us-east-1.amazonaws.com/leaguetest"
        botRegistry = "https://869704209971.dkr.ecr.us-east-1.amazonaws.com"
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
//         stage('Upload App Image') {
//             steps {
//                 script {
//                     withCredentials([aws(credentialsId: 'aws-ecr-creds', passwordVariable: 'password', usernameVariable: 'username')]) {
//                         docker.withRegistry("$LEAGUE_BOT_REGISTRY","$REGISTRY_CREDENTIALS") {
//                             dockerImage.push("$BUILD_NUMBER")
//                             dockerImage.push('latest')
//                         }
//                     }
//
// //                     sh "aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --image-uri $ECR_REGISTRY:$BUILD_NUMBER"
//                 }
//             }
//         }
     }
}