FROM p4xbase
LABEL maintainer "p4misc <p4miscjp@gmail.com>"
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
