#!/bin/bash
# Generate monitoring metrics for use with Prometheus (collected via node_explorer)
# If required, put this job into perforce user crontab:
#
#   */1 * * * * /p4/common/site/bin/monitor_metrics.sh $INSTANCE > /dev/null 2>&1 ||:
#
# Please note you need to make sure that the specified directory below (which may be linked)
# can be read by the node_exporter user (and is setup via --collector.textfile.directory parameter)
#
# Note we use a tempfile for each metric to avoid partial reads. Textfile collector only looks for files
# ending in .prom so we do a finale rename when ready

if [[ -z "${BASH_VERSINFO}" ]] || [[ -z "${BASH_VERSINFO[0]}" ]] || [[ ${BASH_VERSINFO[0]} -lt 4 ]]; then
    echo "This script requires Bash version >= 4";
    exit 1;
fi

# This might also be /hxlogs/metrics
metrics_root=/opt/perforce/servers/master/metrics

# Load SDP controlled shell environment.
# shellcheck disable=SC1091
P4USER=super
P4PORT=1666
P4BIN=/usr/bin/p4

p4="$P4BIN -u $P4USER -p $P4PORT"
echo "super123456" | $p4 login

# Get server id
SERVER_ID=$($p4 serverid | awk '{print $3}')
SERVER_ID=${SERVER_ID:-unset}

monitor_uptime () {
    # Server uptime as a simple seconds parameter - parsed from p4 info:
    # Server uptime: 168:39:20
    fname="$metrics_root/p4_uptime-${SERVER_ID}.prom"
    tmpfname="$fname.$$"
    uptime=$($p4 info 2>&1 | grep uptime | awk '{print $3}')
    [[ -z "$uptime" ]] && uptime="0:0:0"
    uptime=${uptime//:/ }
    arr=($uptime)
    hours=${arr[0]}
    mins=${arr[1]}
    secs=${arr[2]}
    #echo $hours $mins $secs
    # Ensure base 10 arithmetic used to avoid overflow errors
    uptime_secs=$(((10#$hours * 3600) + (10#$mins * 60) + 10#$secs))
    echo "# HELP p4_server_uptime P4D Server uptime (seconds)" > "$tmpfname"
    echo "# TYPE p4_server_uptime counter" >> "$tmpfname"
    echo "p4_server_uptime{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\"} $uptime_secs" >> "$tmpfname"
    mv "$tmpfname" "$fname"
}

monitor_change () {
    # Latest changelist counter as single counter value
    fname="$metrics_root/p4_change-${SERVER_ID}.prom"
    tmpfname="$fname.$$"
    curr_change=$($p4 counters 2>&1 | grep change | awk '{print $3}')
    if [[ ! -z "$curr_change" ]]; then
        echo "# HELP p4_change_counter P4D change counter" > "$tmpfname"
        echo "# TYPE p4_change_counter counter" >> "$tmpfname"
        echo "p4_change_counter{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\"} $curr_change" >> "$tmpfname"
        mv "$tmpfname" "$fname"
    fi
}

monitor_processes () {
    # Monitor metrics summarised by cmd or user
    fname="$metrics_root/p4_monitor-${SERVER_ID}.prom"
    tmpfname="$fname.$$"
    monfile="/tmp/mon.out"
    $p4 monitor show > "$monfile" 2> /dev/null
    echo "# HELP p4_monitor_by_cmd P4 running processes" > "$tmpfname"
    echo "# TYPE p4_monitor_by_cmd counter" >> "$tmpfname"
    awk '{print $5}' "$monfile" | sort | uniq -c | while read count cmd
    do
        echo "p4_monitor_by_cmd{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\",cmd=\"$cmd\"} $count" >> "$tmpfname"
    done

    echo "# HELP p4_monitor_by_user P4 running processes" >> "$tmpfname"
    echo "# TYPE p4_monitor_by_user counter" >> "$tmpfname"
    awk '{print $3}' "$monfile" | sort | uniq -c | while read count user
    do
        echo "p4_monitor_by_user{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\",user=\"$user\"} $count" >> "$tmpfname"
    done

    mv "$tmpfname" "$fname"
}

monitor_completed_cmds () {
    # Metric for completed commands by parsing log file - might be considered expensive to compute as log grows.
    fname="$metrics_root/p4_completed_cmds-${SERVER_ID}.prom"
    tmpfname="$fname.$$"
    num_cmds=$(grep -c completed "/opt/perforce/servers/master/logs/log")
    echo "#HELP p4_completed_cmds_per_day Completed p4 commands" > "$tmpfname"
    echo "#TYPE p4_completed_cmds_per_day counter" >> "$tmpfname"
    echo "p4_completed_cmds_per_day{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\"} $num_cmds" >> "$tmpfname"
    mv "$tmpfname" "$fname"
}

monitor_checkpoint () {
    # Metric for when SDP checkpoint last ran and how long it took.
    # Not as easy as it might first appear because:
    # - might be in progress
    # - multiple rotate_journal.sh may be run in between daily_checkpoint.sh - and they
    # both write to checkpoint.log!
    # The strings searched for have been present in SDP logs for years now...
    fname="$metrics_root/p4_checkpoint-${SERVER_ID}.prom"
    tmpfname="$fname.$$"

    echo "#HELP p4_sdp_checkpoint_log_time Time of last checkpoint log" > "$tmpfname"
    echo "#TYPE p4_sdp_checkpoint_log_time gauge" >> "$tmpfname"

    # Look for latest checkpoint log which has Start/End (avoids run in progress and rotate_journal logs)
    ckp_log=""
    for f in $(ls -tr /opt/perforce/servers/master/logs/checkpoint.log*);
    do
        if [[ `grep -cE "Start p4_$SDP_INSTANCE Checkpoint|End p4_$SDP_INSTANCE Checkpoint" $f` -eq 2 ]]; then
            ckp_log="$f"
        fi;
    done
    ckp_time=0
    if [[ ! -z "$ckp_log" ]]; then
        ckp_time=$(date -r "$ckp_log" +"%s")
    fi
    echo "p4_sdp_checkpoint_log_time{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\"} $ckp_time" >> "$tmpfname"

    echo "#HELP p4_sdp_checkpoint_duration Time taken for last checkpoint/restore action" >> "$tmpfname"
    echo "#TYPE p4_sdp_checkpoint_duration gauge" >> "$tmpfname"

    ckp_duration=0
    if [[ ! -z "$ckp_log" && $ckp_time -gt 0 ]]; then
        dt=$(grep "Start p4_$SDP_INSTANCE Checkpoint" "$ckp_log" | sed -e 's/\/p4.*//')
        start_time=$(date -d "$dt" +"%s")
        dt=$(grep "End p4_$SDP_INSTANCE Checkpoint" "$ckp_log" | sed -e 's/\/p4.*//')
        end_time=$(date -d "$dt" +"%s")
        ckp_duration=$(($end_time - $start_time))
    fi
    echo "p4_sdp_checkpoint_duration{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\"} $ckp_duration" >> "$tmpfname"

    mv "$tmpfname" "$fname"
}

monitor_replicas () {
    # Metric for server replicas
    fname="$metrics_root/p4_replication-${SERVER_ID}.prom"
    tmpfname="$fname.$$"

    valid_servers=""
    # Read like this to set global variables in loop
    while read svr_id type services
    do
        if [[ $services =~ standard|replica|commit-server|edge-server|forwarding-replica|build-server|standby|forwarding-standby ]]; then
            valid_servers="$valid_servers $svr_id"
        fi
    done < <($p4 -F "%serverID% %type% %services%" servers)
    declare -A svr_jnl
    declare -A svr_pos
    while read svr_id jnl pos
    do
        svr_jnl[$svr_id]=$jnl
        svr_pos[$svr_id]=$pos
    done < <($p4 -F "%serverID% %appliedJnl% %appliedPos%" servers -J)

    echo "#HELP p4_replica_curr_jnl Current journal for server" >> "$tmpfname"
    echo "#TYPE p4_replica_curr_jnl counter" >> "$tmpfname"
    for s in $valid_servers
    do
        curr_jnl=${svr_jnl[$s]}
        curr_jnl=${curr_jnl:-0}
        echo "p4_replica_curr_jnl{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\",servername=\"$s\"} $curr_jnl" >> "$tmpfname"
    done

    echo "#HELP p4_replica_curr_pos Current journal for server" >> "$tmpfname"
    echo "#TYPE p4_replica_curr_pos counter" >> "$tmpfname"
    for s in $valid_servers
    do
        curr_pos=${svr_pos[$s]}
        curr_pos=${curr_pos:-0}
        echo "p4_replica_curr_pos{serverid=\"$SERVER_ID\",sdpinst=\"$SDP_INSTANCE\",servername=\"$s\"} $curr_pos" >> "$tmpfname"
    done

    mv "$tmpfname" "$fname"
}

monitor_uptime
monitor_change
monitor_processes
monitor_completed_cmds
#monitor_checkpoint
#monitor_replicas

# Make sure all readable by node_explorer or other user
chmod 755 $metrics_root/*.prom

