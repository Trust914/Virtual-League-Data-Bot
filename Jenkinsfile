pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        REGISTRY_CREDENTIALS = "ecr:$AWS_REGION:"
        LEAGUE_BOT_APP_REGISTRY = "869704209971.dkr.ecr.us-east-1.amazonaws.com/leaguetest"
        LEAGUE_BOT_REGISTRY = "https://869704209971.dkr.ecr.us-east-1.amazonaws.com"
        //LAMBDA_FUNCTION_NAME = 'your-lambda-function-name'
    }

    stages {
        stage('Fetch code'){
            steps {
                 checkout([$class: 'GitSCM',
                            branches: [[name: '*/main' ]],
                            extensions: scm.extensions,
                            userRemoteConfigs: [[
                                url: 'https://github.com/Trust914/django-todo.git',
                                credentialsId: 'GITHUB_CREDENTIALS'
                            ]]
                ])
            }
        }
//         stage('Build App Image') {
//             steps {
//                 script {
//                     dockerImage = docker.build("$ECR_REGISTRY:$BUILD_NUMBER", "./")
//                 }
//             }
//         }
//
//         stage('Upload App Image') {
//             steps {
//                 script {
//                     withCredentials([awsEcr(usernamePassword(credentialsId: 'aws-ecr-creds', passwordVariable: 'password', usernameVariable: 'username'))]) {
//                         docker.withRegistry("$ECR_REGISTRY", "ecr:$AWS_REGION") {
//                             dockerImage.push("$BUILD_NUMBER")
//                             dockerImage.push('latest')
//                         }
//                     }
//
//                     sh "aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --image-uri $ECR_REGISTRY:$BUILD_NUMBER"
//                 }
//             }
//         }
     }
}