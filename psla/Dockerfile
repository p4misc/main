FROM ubuntu:bionic
LABEL maintainer "p4misc <p4miscjp@gmail.com>"

RUN apt-get update -y && \
    apt-get install -y vim \
                       wget \
                       unzip \
                       python3 \
                       python3-pip \
                       language-pack-ja && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root
RUN update-locale LC_ALL=ja_JP.UTF-8
RUN wget https://swarm.workshop.perforce.com/projects/perforce-software-log-analyzer/archives/psla.zip && \
    unzip psla.zip
WORKDIR /root/psla/psla
RUN pip3 install -r requirements.txt

ENV LC_ALL ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
EXPOSE 5050
CMD ["./run_psla.sh", "5050"]
