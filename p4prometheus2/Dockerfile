FROM centos:7
LABEL maintainer "p4misc <p4miscjp@gmail.com>"

RUN yum update -y && \
    yum install -y epel-release \
                   wget \
                   rsync \
                   sysfsutils && \
                   rm -rf /var/cache/yum/* && \
                   yum clean all

WORKDIR /root
 
## Install node_exporter
RUN useradd --no-create-home --shell /bin/false node_exporter
RUN export PVER="0.18.1" && \
    wget https://github.com/prometheus/node_exporter/releases/download/v$PVER/node_exporter-$PVER.linux-amd64.tar.gz && \
    tar xvf node_exporter-$PVER.linux-amd64.tar.gz && \
    mv node_exporter-$PVER.linux-amd64/node_exporter /usr/local/bin/ && \
    rm -rf node_exporter-$PVER.linux-amd64 && \
    rm -rf node_exporter-$PVER.linux-amd64.tar.gz
RUN mkdir -p /hxlogs/metrics

## Install p4prometheus
RUN wget https://github.com/rcowham/p4prometheus/files/3595236/p4prometheus.linux-amd64.gz && \
    gzip -d p4prometheus.linux-amd64.gz && \
    chmod +x p4prometheus.linux-amd64 && \
    mv p4prometheus.linux-amd64 /usr/local/bin/p4prometheus

RUN mkdir -p /hxdepots/reset
WORKDIR /hxdepots/reset
RUN curl -k -s -O https://swarm.workshop.perforce.com/downloads/guest/perforce_software/helix-installer/main/src/reset_sdp.sh && \
    chmod +x reset_sdp.sh && \
    ./reset_sdp.sh -C > settings.cfg && \
    ./reset_sdp.sh -c settings.cfg -fast 2>&1 | tee log.reset_sdp

WORKDIR /home/perforce
ADD p4prometheus.yml .
ADD p4d_run.sh .
RUN chown -R perforce:perforce /home/perforce /hxlogs/metrics

USER perforce
WORKDIR /hxdepots/sdp/Server/Unix/setup
#RUN export USER=perforce && \
#    ./install_sdp_python.sh

WORKDIR /home/perforce
RUN chmod u+x p4d_run.sh

EXPOSE 1999
EXPOSE 9100
CMD ["/home/perforce/p4d_run.sh"]
