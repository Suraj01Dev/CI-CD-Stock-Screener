    pipeline{
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
    }    
}
