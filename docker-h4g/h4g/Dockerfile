######
FROM ubuntu:bionic as ubuntu18
LABEL maintainer "p4misc <p4miscjp@gmail.com>"

RUN apt-get update -y && \
    apt-get install -y vim \
                       wget \
                       unzip \
                       gnupg2 \
                       git-lfs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -qO - https://package.perforce.com/perforce.pubkey | apt-key add -
RUN echo "deb http://package.perforce.com/apt/ubuntu bionic release" > /etc/apt/sources.list.d/perforce.list
RUN apt-get update -y

######
FROM ubuntu18 as ubuntu18upd

# Set environment variables
ENV P4PORT p4d:1666
ENV P4USER bruno
ENV P4PASSWD Brunopass
ENV GCUSERP4PASSW gconn-user
ENV GRAPHDEPOT git 

RUN apt-get install helix-git-connector -y

ADD run_h4g.sh /root/run_h4g.sh

WORKDIR /root
RUN chmod u+x /root/run_h4g.sh

# Expose default HTTPS port
EXPOSE 443

CMD ["/root/run_h4g.sh"]
