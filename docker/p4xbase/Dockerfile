FROM ubuntu:bionic
LABEL maintainer "p4misc <p4miscjp@gmail.com>"
RUN apt-get update -y
RUN apt-get install vim -y
RUN apt-get install gnupg2 -y
RUN apt-get install wget -y
RUN wget -qO - https://package.perforce.com/perforce.pubkey | apt-key add -
RUN echo "deb http://package.perforce.com/apt/ubuntu bionic release" > /etc/apt/sources.list.d/perforce.list
RUN apt-get update -y
WORKDIR /root
RUN useradd --no-create-home --shell /bin/false node_exporter
RUN export PVER="0.18.1" && \
    wget https://github.com/prometheus/node_exporter/releases/download/v$PVER/node_exporter-$PVER.linux-amd64.tar.gz && \
    tar xvf node_exporter-$PVER.linux-amd64.tar.gz && \
    mv node_exporter-$PVER.linux-amd64/node_exporter /usr/local/bin/ && \
    rm -rf node_exporter-$PVER.linux-amd64 && \
    rm -rf node_exporter-$PVER.linux-amd64.tar.gz
RUN mkdir -p /hxlogs/metrics
RUN wget https://github.com/rcowham/p4prometheus/files/3446515/p4prometheus.linux-amd64.gz && \
    gzip -d p4prometheus.linux-amd64.gz && \
    chmod +x p4prometheus.linux-amd64 && \
    mv p4prometheus.linux-amd64 /usr/local/bin/p4prometheus
ADD run_node_exporter.sh .
ADD p4prometheus.yaml .
RUN chmod u+x run_node_exporter.sh
