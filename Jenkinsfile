//@Library('Utilities') _
import groovy.json.JsonSlurper
import hudson.model.*
def BuildVersion
def Current_version
def NextVersion
def dev_rep_docker = 'lidorabo/docker_repo'
def colons = ':'
def module = 'intweb'
def underscore = '_'
def path_json_file
def int_web_folder = 'INT_WEB'
def release_folder = 'Release'
pipeline {

    options {
        timeout(time: 30, unit: 'MINUTES')
    }
    agent { label 'slave' }
    stages {
        stage('Checkout') {
            steps {
                script {
                    node('master') {
                        dir(release_folder) {
                            deleteDir()
                            checkout([$class: 'GitSCM', branches: [[name: 'master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'git-cred', url: "https://github.com/lidorabo/Release.git"]]])
                            path_json_file = sh(script: "pwd", returnStdout: true).trim() + '/' + 'dev' + '.json'
                            Current_version = Return_Json_From_File("$path_json_file").Services.INT_WEB

                        }
                    }
                        dir(int_web_folder) {
                            deleteDir()
                            checkout([$class: 'GitSCM', branches: [[name: 'master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'git-cred', url: "https://github.com/lidorabo/INT_WEB.git"]]])
                            Commit_Id = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                            BuildVersion = Current_version + '_' + Commit_Id
                            last_digit_current_version = sh(script: "echo $Current_version | cut -d'.' -f3", returnStdout: true).trim()
                            NextVersion = sh(script: "echo $Current_version | cut -d. -f1", returnStdout: true).trim() + '.' + sh(script: "echo $Current_version |cut -d'.' -f2", returnStdout: true).trim() + '.' + (Integer.parseInt(last_digit_current_version) + 1)

                        }


                }
            }
        }
        stage('Build') {
            steps {
                script {
                    dir(int_web_folder) {
                        try {
                            sh "sudo docker build . -t $module$colons$BuildVersion"
                            println("The build image is successfully")

                        }
                        catch (exception) {
                            println "The image build is failed"
                            currentBuild.result = 'FAILURE'
                            throw exception
                        }

                    }

                }


            }
        }
        stage('Push image to repository'){
            steps{
                script{
                    try{
                        withCredentials([usernamePassword(credentialsId: 'docker-cred', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                            sh "sudo docker login -u=${DOCKER_USERNAME} -p=${DOCKER_PASSWORD}"
                            sh "sudo docker tag $module$colons$BuildVersion $dev_rep_docker$colons$module$underscore$NextVersion"
                            sh "sudo docker push $dev_rep_docker$colons$module$underscore$NextVersion"

                        }
                    }
                    catch (exception){
                        println "The image pushing to dockehub  failed"
                        currentBuild.result = 'FAILURE'
                        throw exception
                    }
                }
            }
        }
        stage('Update version in release file'){
            steps{
                script{
                    node('master'){
                        dir(release_folder){
                            withCredentials([usernamePassword(credentialsId: 'git-cred', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                                sh """
                            git config --global user.name "LidorAbo"
                            git config --global user.email "lidorabo2@gmail.com"                         
                            sed -i  -r 's/("INT_WEB")(\\s+\\:\\s+)(.*)/\\1\\2"$NextVersion"\\,/' $path_json_file
                            git add .
                            git commit -m "next version of INT_WEB is updated to $NextVersion in dev.json file"
                            git push  https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/lidorabo/Release.git HEAD:master 
                            """
                            }
                        }
                    }


                }
            }
        }
        stage('Pushing tag to master branch'){
            steps{
                script{
                    node('master'){
                        dir(int_web_folder){
                            withCredentials([usernamePassword(credentialsId: 'git-cred', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                                sh """
                         git config --global user.name "LidorAbo"
                         git config --global user.email "Lidorabo2@gmail.com"
                         git tag -d \$(git tag -l) > /dev/null
                         git tag -a $NextVersion -m "Tag for release version of INT_WEB module"
                         git push  https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/lidorabo/INT_WEB.git $NextVersion
                            """
                            }
                        }

                    }
                }
            }
        }
    }

}
def Return_Json_From_File(file_name){
    return new JsonSlurper().parse(new File(file_name))
}