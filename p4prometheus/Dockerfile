## Create a base centos7
FROM centos:7 as centos7
LABEL maintainer "p4misc <p4miscjp@gmail.com>"

RUN yum update -y && \
    yum install -y epel-release \
                   wget \
                   rsync \
                   sudo \
                   which \
                   cronie \
                   sysfsutils && \
    rm -rf /var/cache/yum/* && \
    yum clean all && \
    echo /usr/local/lib>> /etc/ld.so.conf; \
    echo /usr/lib64>> /etc/ld.so.conf; \
    sed -ie "s/^Defaults[ \t]*requiretty/#Defaults  requiretty/g" /etc/sudoers; \
    sed -ie '/pam_loginuid.so/s/^/#/' /etc/pam.d/crond

FROM centos7 as centos7upd
WORKDIR /root
 
## Install node_exporter
RUN useradd --no-create-home --shell /bin/false node_exporter
RUN export PVER="0.18.1" && \
    wget https://github.com/prometheus/node_exporter/releases/download/v$PVER/node_exporter-$PVER.linux-amd64.tar.gz && \
    tar xvf node_exporter-$PVER.linux-amd64.tar.gz && \
    mv node_exporter-$PVER.linux-amd64/node_exporter /usr/local/bin/ && \
    rm -rf node_exporter-$PVER.linux-amd64 && \
    rm -rf node_exporter-$PVER.linux-amd64.tar.gz

## Install p4prometheus
RUN wget https://github.com/rcowham/p4prometheus/files/3595236/p4prometheus.linux-amd64.gz && \
    gzip -d p4prometheus.linux-amd64.gz && \
    chmod +x p4prometheus.linux-amd64 && \
    mv p4prometheus.linux-amd64 /usr/local/bin/p4prometheus

## Install helix-p4d
RUN rpm --import https://package.perforce.com/perforce.pubkey
ADD perforce.repo /etc/yum.repos.d/perforce.repo
RUN yum install -y helix-p4d && \
    /opt/perforce/sbin/configure-helix-p4d.sh master -p 1666 -r /opt/perforce/servers/master -u super -P super123456 --unicode --case=1 -n

RUN mkdir /opt/perforce/servers/master/metrics && \
    chown -R perforce:perforce /opt/perforce/servers/master/metrics

COPY --chown=perforce:perforce p4prometheus.d /var/spool/cron/perforce
RUN chmod 0644 /var/spool/cron/perforce

WORKDIR /home/perforce
USER perforce
COPY --chown=perforce:perforce p4prometheus.yml .
COPY --chown=perforce:perforce p4d_run.sh .
COPY --chown=perforce:perforce monitor_metrics.sh .
RUN chmod +x *.sh

EXPOSE 1666
EXPOSE 9100

USER root

CMD ["./p4d_run.sh"]
