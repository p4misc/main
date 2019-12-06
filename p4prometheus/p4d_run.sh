#!/bin/bash

sudo -u perforce /usr/sbin/p4dctl start master
crond
sudo -u perforce /usr/local/bin/node_exporter --collector.textfile.directory="/opt/perforce/servers/master/metrics" &
sudo -u perforce /usr/local/bin/p4prometheus  --config=/home/perforce/p4prometheus.yml &
tail -f /dev/null
