pipeline {
    agent any

    environment {
        registryCredential = "ecr:us-east-1:AWS_CREDENTIALS"
        appRegistry = "869704209971.dkr.ecr.us-east-1.amazonaws.com/leaguetest"
        leagueBotRegistry = "https://869704209971.dkr.ecr.us-east-1.amazonaws.com"
        lambdaFunctionName = 'your-lambda-function-name'
        imageDigest = "sha256:3d71145c9550aa6864d9bf68dc650e9e17b47e6da75661e0cf1aa9d3d2b4c752"
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
//                         def aws = com.amazonaws.services
//                         def lambda = aws.lambda()
//                         def response = lambda.updateFunctionCode(LambdaFunctions:[lambdaFunctionName], ImageUri: appRegistry + ":$BUILD_NUMBER")
//                         echo "Update Lambda Function Response: ${response}"
                        sh "/usr/local/bin/aws lambda update-function-code --function-name arn:aws:lambda:us-east-1:869704209971:function:league-test --image-uri '${appRegistry}:$BUILD_NUMBER@$imageDigest'"

                    }
                }
            }
        }
    }
}