    pipeline{
	    
    environment{
        APPNAME="stock_screener"
        RELEASE="1.0.0"
        DOCKER_USER="suraj01dev"
        DOCKER_PASS="dockerhub"
        IMAGE_NAME="${DOCKER_USER}"+"/"+"${APPNAME}"
        IMAGE_TAG="${RELEASE}"+"-"+"${BUILD_NUMBER}"
    }
	    
    agent{
        label "node1"
    }
    stages{
        stage('Clean Workspace') {
            steps {
            cleanWs()
            }
        }        
        stage('Git Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Suraj01Dev/CI-CD-Stock-Screener'
            }
        }

        stage('Testing stock_screeener') {
            steps {
		sh "bash stock_screener_test.sh"
            }
        }

        stage('SonarQube Code Analysis') {
                    steps {
                        dir("${WORKSPACE}"){
                        script {
                            def scannerHome = tool name: 'sonar_scanner'
                            withSonarQubeEnv('sonar-server') {
                                sh "${scannerHome}/bin/sonar-scanner"
                            }
                        }
                    }
                    }
            }
        stage("Quality gate") {
                    steps {
                        waitForQualityGate abortPipeline: true
                    }
                }
	    
        stage("Building docker"){
            steps{

                sh '''
                sudo docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''

            }
        }
	    
        stage("Pushing the stock_screener docker image"){
            steps{
                withCredentials([string(credentialsId: 'docker_pass', variable: 'docker_pass_var')]) {

                    sh '''
                    sudo docker login -u suraj01dev -p ${docker_pass_var}
                    '''

                    sh '''
                    sudo docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                
                        }

            }
        }
        stage("Deploy in k8s"){
            steps{
                       sh "scp deployment.yaml suraj@192.168.122.2:/home/suraj"                // some block
                       sh "ssh suraj@192.168.122.2 kubectl create -f deployment.yaml"
                }
            }

    }    
}
