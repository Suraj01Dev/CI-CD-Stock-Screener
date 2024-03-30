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


