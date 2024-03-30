# CI/CD Pipeline for Stock Screener Application
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
- Containerization and pushing
- Deployment into K8s

## Setting up Jenkins

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

        stage('Testing stock_screeener') {
            steps {
		sh "bash stock_screener_test.sh"
            }
        }
    }    
}
```

## Integrating SonarQube
sqp_0a464021d32ab3b6f36214e488ddd6fe892b80b3

sonar-scanner \
  -Dsonar.projectKey=stock_screener \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://192.168.122.98:9000 \
  -Dsonar.token=sqp_0a464021d32ab3b6f36214e488ddd6fe892b80b3

  ### Installing SonarQube

  In this project, for simplicity the SonarQube instance is installed in the Jenkins node itself as a container. To run a container let's install docker. 

  ```bash
	apt-get install docker.io
  ```

  To run SonarQube as container execute the below command.
  ```bash
	docker run -d --name sonarqube -p 9000:9000 -p 9092:9092
  ```
