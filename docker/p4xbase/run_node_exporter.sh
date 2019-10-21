#!/bin/sh

/usr/local/bin/node_exporter --collector.textfile.directory="/hxlogs/metrics" &
/usr/local/bin/p4prometheus  --config=/root/p4prometheus.yaml &
