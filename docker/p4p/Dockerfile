FROM p4xbase
LABEL maintainer "p4misc <p4miscjp@gmail.com>"
ARG TARGET="TARGET"
ARG PORT="PORT"
RUN apt-get install helix-proxy -y
RUN mkdir /opt/perforce/servers/p4p-master
RUN echo "#!/bin/sh\np4p -r /opt/perforce/servers/p4p-master -p ${PORT} -t ${TARGET}" > /root/run_p4p.sh
RUN chmod u+x /root/run_p4p.sh
WORKDIR /root
EXPOSE $PORT
CMD ["/root/run_p4p.sh"]
