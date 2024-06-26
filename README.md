# CI/CD Pipeline for Stock Screener Application
_Devops Portfolio Project 2_

![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/e4b64d0c-ae4c-4dea-9aaf-fd389a0fd6b3)

## Introduction
This project focuses on establishing a Continuous Integration/Continuous Deployment (CI/CD) pipeline for the Stock Screener application. 
The Stock Screener is a web application built on the Python Streamlit framework, designed to retrieve financial ratios of stocks for fundamental analysis. 
The pipeline integrates various tools and technologies such as Jenkins, Docker, Python, Bash, and Kubernetes to automate the deployment process.

## Tools and Technologies
- **Jenkins:**
    Jenkins is used as the automation server to orchestrate the CI/CD pipeline. It facilitates building, testing, and deployment processes.

- **Docker:** 
     Docker is utilized for containerization, enabling easy deployment and scaling of the application across different environments.

- **Python:**
    Python is the primary programming language used for developing the Stock Screener application and implementing necessary scripts.

- **Bash:**
    Bash scripting is employed for automation and execution of various tasks within the pipeline.
  
- **Kubernetes:**
      Kubernetes is chosen for container orchestration, managing and scaling containerized applications efficiently.
  
- **Streamlit:**
      Streamlit is the framework used to develop the Stock Screener web application, providing an interactive and intuitive user interface for analyzing financial data.

## Steps involved in building the project
- Setting up Jenkins
- Creating the testing script
- Integrating SonarQube
- Containerization 
- Deployment into K8s

## Setting up Jenkins

This section consists of 
- Prerequisites
- Creating a pipeline project
- Jenkinsfile Build

### Prerequisites
- Installing Jenkins [link](https://phoenixnap.com/kb/install-jenkins-ubuntu)
- Setting up SSH Jenkins Node [link](https://devopscube.com/setup-slaves-on-jenkins-2/)


### Creating a pipeline project

**Creating a new item**

![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/cf288898-4cc6-4ec8-bf0b-f09e73bb52ac)

**Running a Hello World Pipeline Script**

![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/bc704578-6c01-4478-bed1-1bb54bdaf3ef)

**Trail run successful**

![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/d59b7c85-788f-4f5d-838f-3a00208eb67d)

  
So, to make things more organized let's create a git repository to get the pipeline script from SCM. 

![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/7a4965d4-2763-49e2-81ff-6395f3502498)

After creating the repository, let's first create a **Jenkinsfile** to code the pipeline script.

### Jenkinsfile Build

```groovy
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
    }    
}
```

In the first stage **Clean Workspace**, we clear the workspace using **cleanWs()** step. This clears the workspace for us. In the next stage we create a **Git Checkout** where we clone the **CI-CD-Stock-Screener** repository from GitHub to the Jenkins node.

To verify this let's manually SSH into the Jenkins node, and list the files in the workspace directory.


![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/4668fe8f-48b8-4fb7-9df4-72d3c81c8924)

Now let's add the source code of the Stock-Screener application in the GitHub repo. The source code for the application ([link](https://github.com/Suraj01Dev/stock_screener/tree/main)).


## Creating the testing script

This section consists of 
- Prerequisites
- Scripting
- Jenkinsfile Build
  
### Prerequisites
Login into the Jenkins node and install the below prerequisites.

- Installing Python dependencies
  ```bash
  pip3 install requests pandas streamlit
  ```
- Installing Bandit
  ```bash
  apt-get install bandit
  ```
- Installing pylint
  ```bash
  pip3 install pylint
  ```

### Scripting

Bandit is used for finding security vulnerabilities in the Python code.
```bash
bandit --format json --output bandit-report.json --recursive stock_screener
```


Pylint is used for static code analysis.
```bash
pylint stock_screener -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt 
```

Combining the above commands, let's go ahead and create a bash script.

```bash
#!/bin/bash
bandit --format json --output bandit-report.json --recursive stock_screener
if [[ $? -ne 0 ]]; then
	exit 1
fi

pylint stock_screener -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt 
if [[ $? -ne 0 ]]; then
	exit 1
fi

exit 0

```

Let's go ahead and add this script in the CI-CD-Stock-Screener repo as **stock_screener_test.sh**.

Now let's add this testing step in the Jenkinsfile.

### Jenkinsfile Build
#### Stage:  Testing stock_screener

```groovy
        stage('Testing stock_screeener') {
            steps {
		sh "bash stock_screener_test.sh"
            }
        }
    
```

## Integrating SonarQube

This section consists of 
- Installing SonarQube
- Creating the project in SonarQube
- Integrating SonarQube with Jenkins
- Jenkinsfile Build

  ### Installing SonarQube

  In this project, for simplicity the SonarQube instance is installed in the Jenkins node itself as a container. To run a container let's install docker. 

  ```bash
	apt-get install docker.io
  ```

  To run SonarQube as a container execute the below command.
  ```bash
	docker run -d --name sonarqube -p 9000:9000 -p 9092:9092
  ```

The SonarQube UI will be running at port 9000 in the Jenkins node.


### Creating the project in SonarQube

![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/155d44e4-d390-4f93-b7bd-0a3beb3086c4)

![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/5afa1237-6be8-4a30-ad07-13507da9a829)

Creating a project locally.
![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/7e7a322b-fa7b-4fa2-bc6d-ba0a273a42cc)

Creating a token.
![Screenshot from 2024-03-30 11-57-42](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/9ec74c0a-f66d-4eea-b533-6c91ad6d6efc)

![image](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/assets/120789150/f3c9cf31-6c0b-4eba-abc2-79768ce3c22f)

To execute the scanner, this command can be executed

```bash
sonar-scanner \
  -Dsonar.projectKey=stock_screener \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://192.168.122.98:9000 \
  -Dsonar.token=sqp_a1552040b1d2d4207794898c41a0d905585c5fcf
```
and, **sqp_a1552040b1d2d4207794898c41a0d905585c5fcf** is the authentication token. Inorder to execute this command the sonar scanner should be installed in the Jenkins node.

### Integrating SonarQube with Jenkins

Follow this [article](https://sunilhari.medium.com/how-to-integrate-sonarqube-and-jenkins-721d5efd3cb6) to integrate SonarQube with Jenkins.

This article covers the following steps:

- Installing the Sonar Scanner using Jenkins.
- Connecting the Sonar instance with the Jenkins instance.
- Creating the secret text with the sonar authentication token in Jenkins.

Let's go ahead and create the **sonar-project.properties** file. This file should also be checked in the repository. This property file will be used by the sonar scanner.

```
sonar.projectKey = stock_screener
sonar.sources = .
sonar.language =  py
sonar.python.pylint.reportPath = pylint-report.txt
sonar.python.bandit.reportPaths = bandit-report.json
```

Adding the sonar scanner in the Jenkinsfile.

### Jenkinsfile Build
#### Stage: SonarQube Code Analysis

```groovy

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

```

### Creating a SonarQube Quality Gate
To create a SonarQube Quality Gate follow this [article](https://tomgregory.com/jenkins/sonarqube-quality-gates-in-jenkins-build-pipeline/#full-worked-example). This explains how to create a webhook and integrate it with Jenkins.

#### Stage: Quality Gate

```groovy
        stage("Quality gate") {
                    steps {
                        waitForQualityGate abortPipeline: true
                    }
	}
```

## Containerization

This step involves creation of a docker image using a [dockerfile](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/blob/main/Dockerfile) and pushing it into the DockerHub. 
Before building the docker file lets first create some environment variables.

```groovy
    environment{
        APPNAME="stock_screener_ui"
        RELEASE="1.0.0"
        DOCKER_USER="suraj01dev"
        DOCKER_PASS="dockerhub"
        IMAGE_NAME="${DOCKER_USER}"+"/"+"${APPNAME}"
        IMAGE_TAG="${RELEASE}"+"-"+"${BUILD_NUMBER}"
    }
```

The command to build the Docker image using Dockerfile is
```bash
docker build -t stock_screener .
```

To push the docker image, use the below command
```bash
docker push stock_screener
```

Let's create a Jenkins stage with the above command.



#### Stage: Building the docker image
```groovy
 stage("Building docker image"){
            steps{

                sh '''
                sudo docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''

            }
        }
```



#### Stage: Pushing the stock_screener docker image
```groovy

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
```

## Deployment into K8s
This final section is all about the deployment of the container into k8s. This section consists of the following steps:
- Creating a deployment.yaml file.
- Creating a passwordless SSH connection to the Minikube node.
- Deploying into the minikube server.


### Creating a deployment.yaml file

The first step in deployment is about creating a [deployment.yaml](https://github.com/Suraj01Dev/CI-CD-Stock-Screener/blob/main/deployment.yaml) file. This Kubernetes deployment contains two replicas and the image used is **suraj01dev/stock_screener** which was pushed into DockerHub in the previous step.


### Creating a passwordless SSH connection to the Minikube node

Passwordless SSH Login
To enable password-less login we have to create a public and private key in the Jenkins node and copy the public key to the minikube node.

```
ssh-keygen
```
The above command will create a public and private key under the ~/.ssh directory. To copy this public key to all the target nodes ssh-copy-id command has to be used.

```
ssh-copy-id -i ~/.ssh/id_rsa.pub suraj@minikube_server
```

### Deployment into the Minikube server

The deployment in this case consists of two steps,
- Moving the deployment.yaml into the Minikube server.
- Creating the deployment.

SCP is used to move the deployment.yaml into the minikube server.
```bash
scp deployment.yaml suraj@192.168.122.2:/home/suraj
```

To create a deployment in Kubernetes.
```bash
kubectl create -f deployment.yaml
```

Let's finally complete our Jenkins pipeline by implementing the deployment in the Jenkinsfile.

#### Stage: Deploy in k8's

```groovy
        stage("Deploy in k8s"){
            steps{
                       sh "scp pods.yaml suraj@192.168.122.2:/home/suraj"                // some block
                       sh "ssh suraj@192.168.122.2 kubectl create -f deployment.yaml"
                }
            }
```

## Summary
This whole project is a End to End complete pipeline which implements various tools and concepts such as 
- Docker
- Kubernetes
- Python
- Bash
- Jenkins
- SonarQube
- Networking
- Scripting
- Testing
- Containerization
- Deployment
The project starts with cloning a GitHub repository, then tests the application  using SonarQube. After testing passes it moves to building the Docker image and pushes it to dockerhub. The next stage is deployment where the image pushed in the previous stage is pulled and deployed into a Kubernetes cluster.

## References
- https://www.youtube.com/watch?v=PWhqbpVbaTo&list=PLH1ul2iNXl7txKuhhDMKenYOThDww6x8S
- https://dev.to/mmphego/how-i-configured-sonarqube-for-python-code-analysis-with-jenkins-and-docker-28fm
- https://tomgregory.com/jenkins/sonarqube-quality-gates-in-jenkins-build-pipeline/#full-worked-example
- https://dev.to/mmphego/how-i-configured-sonarqube-for-python-code-analysis-with-jenkins-and-docker-28fm
- https://github.com/tngTUDOR/pycodeq


