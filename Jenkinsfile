pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git 'https://github.com/varsha-santhanam-2/DEVOPS-DEMO'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t twitter-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5000:5000 twitter-app'
            }
        }
    }
}