FROM ubuntu:bionic
LABEL maintainer "p4misc <p4miscjp@gmail.com>"
RUN apt-get update -y
RUN apt-get install vim -y
RUN apt-get install gnupg2 -y
RUN apt-get install wget -y
RUN wget -qO - https://package.perforce.com/perforce.pubkey | apt-key add -
RUN echo "deb http://package.perforce.com/apt/ubuntu bionic release" > /etc/apt/sources.list.d/perforce.list
RUN apt-get update -y
