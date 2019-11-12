#!/bin/bash

/usr/local/bin/node_exporter --collector.textfile.directory="/hxlogs/metrics" &
/usr/local/bin/p4prometheus  --config=/home/perforce/p4prometheus.yml &
/p4/1/bin/p4d_1_init start
tail -f /dev/null
