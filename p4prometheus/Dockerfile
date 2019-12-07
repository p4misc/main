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

ARG p4super
ARG p4passwd
 
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
ADD perforce.repo /etc/yum.repos.d/perforce.repo

RUN rpm --import https://package.perforce.com/perforce.pubkey && \
    yum install -y helix-p4d && \
    /opt/perforce/sbin/configure-helix-p4d.sh master -p 1666 -r /opt/perforce/servers/master -u "${p4super}" -P "${p4passwd}" --unicode --case=1 -n; \
    mkdir -p /opt/perforce/servers/master/metrics

RUN echo "HOG"

ADD --chown=perforce:perforce p4prometheus.d /var/spool/cron/perforce
ADD --chown=perforce:perforce p4prometheus.yml /home/perforce/
ADD --chown=perforce:perforce p4d_run.sh /home/perforce/
ADD --chown=perforce:perforce monitor_metrics.sh /home/perforce/
ADD --chown=perforce:perforce configure_serverlog.sh /home/perforce/

RUN chmod 0644 /var/spool/cron/perforce; \
    chmod +x /home/perforce/*.sh; \
    chown -R perforce:perforce /opt/perforce/servers/master/metrics; \
    /home/perforce/configure_serverlog.sh; \
    sed -ie "s/P4USER=p4super/P4USER=${p4super}/g" /home/perforce/monitor_metrics.sh; \
    sed -ie "s/P4PASSWD=p4passwd/P4PASSWD=${p4passwd}/g" /home/perforce/monitor_metrics.sh

EXPOSE 1666
EXPOSE 9100

CMD ["/home/perforce/p4d_run.sh"]
