#!/bin/bash

/usr/local/bin/node_exporter --collector.textfile.directory="/opt/perforce/servers/master/metrics" &
/usr/local/bin/p4prometheus  --config=/home/perforce/p4prometheus.yml &
/usr/sbin/p4dctl start master
tail -f /dev/null
