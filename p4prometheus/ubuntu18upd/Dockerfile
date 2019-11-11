FROM ubuntu:bionic
LABEL maintainer "p4misc <p4miscjp@gmail.com>"
RUN apt-get update -y && \
    apt-get install -y curl \
                       vim \
                       gnupg2 \
                       wget \
                       zlib1g-dev \
                       libssl-dev \
                       build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

