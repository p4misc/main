######
FROM ubuntu:bionic as ubuntu18
LABEL maintainer "p4misc <p4miscjp@gmail.com>"

RUN apt-get update -y && \
    apt-get install -y vim \
                       wget \
                       unzip \
                       gnupg2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://package.perforce.com/perforce.pubkey | apt-key add -
RUN echo "deb http://package.perforce.com/apt/ubuntu bionic release" > /etc/apt/sources.list.d/perforce.list
RUN apt-get update -y

######
FROM ubuntu18 as ubuntu18upd

RUN apt-get install helix-p4d -y

WORKDIR /root
RUN wget http://ftp.perforce.com/pub/perforce/tools/sampledepot.tar.gz
RUN tar xzvf sampledepot.tar.gz
WORKDIR /root/PerforceSample
RUN p4d -r . -jr checkpoint
RUN p4d -r . -xi
RUN p4d -r . -xu
RUN echo "#!/bin/sh\np4d -r /root/PerforceSample -p 1666 -L /root/PerforceSample/log" > /root/run_p4d.sh

WORKDIR /root
RUN chmod u+x /root/run_p4d.sh
EXPOSE 1666
CMD ["/root/run_p4d.sh"]
