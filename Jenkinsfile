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
                git "https://github.com/Suraj01Dev/CI-CD-Stock-Screener"
            }
        }
    }    
}
