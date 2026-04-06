pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/varsha-santhanam-2/DEVOPS-DEMO'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t twitter-app .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 5000:5000 twitter-app'
            }
        }
    }
}