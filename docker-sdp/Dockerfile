FROM ubuntu18upd
LABEL maintainer "p4misc <p4miscjp@gmail.com>"
RUN mkdir -p /hxdepots/reset
WORKDIR /hxdepots/reset
RUN curl -k -s -O https://swarm.workshop.perforce.com/downloads/guest/perforce_software/helix-installer/main/src/reset_sdp.sh && \
    chmod +x reset_sdp.sh && \
    ./reset_sdp.sh -C > settings.cfg && \
    ./reset_sdp.sh -c settings.cfg -fast 2>&1 | tee log.reset_sdp
USER perforce
WORKDIR /hxdepots/sdp/Server/Unix/setup
RUN export USER=perforce && \
    ./install_sdp_python.sh
USER root
WORKDIR /home/perforce
ADD p4d_run.sh .
RUN chown perforce:perforce p4d_run.sh && \
    chmod u+x p4d_run.sh
USER perforce
EXPOSE 1999
CMD ["/home/perforce/p4d_run.sh", "start"]
