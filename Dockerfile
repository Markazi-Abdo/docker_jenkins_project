FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y docker-cli
RUN usermod -aG docker jenkins

USER jenkins
