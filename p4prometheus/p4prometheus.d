SHELL = /bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=""
*/1 * * * * /home/perforce/monitor_metrics.sh > /dev/null 2>&1
