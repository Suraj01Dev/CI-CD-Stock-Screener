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
                            def scannerHome = tool name: 'sonarqube-scanner-latest'
                            withSonarQubeEnv('sonar_stock_screener') {
                                sh "${scannerHome}/bin/sonar-scanner"
                            }
                        }
                    }
                    }
            }
    }    
}
