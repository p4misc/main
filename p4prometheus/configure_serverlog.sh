#!/bin/bash

P4DBIN=/usr/sbin/p4d
P4ROOT=/opt/perforce/servers/master/root

$P4DBIN -r $P4ROOT "-cset serverlog.file.1=audit.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.1=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.1=10"

$P4DBIN -r $P4ROOT "-cset serverlog.file.2=auth.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.2=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.2=10"

$P4DBIN -r $P4ROOT "-cset serverlog.file.3=commands.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.3=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.3=10"

$P4DBIN -r $P4ROOT "-cset serverlog.file.4=errors.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.4=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.4=10"

$P4DBIN -r $P4ROOT "-cset serverlog.file.5=events.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.5=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.5=10"

$P4DBIN -r $P4ROOT "-cset serverlog.file.6=ldapsync.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.6=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.6=10"

$P4DBIN -r $P4ROOT "-cset serverlog.file.7=integrity.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.7=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.7=10"

$P4DBIN -r $P4ROOT "-cset serverlog.file.8=track.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.8=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.8=10"

$P4DBIN -r $P4ROOT "-cset serverlog.file.9=user.csv"
$P4DBIN -r $P4ROOT "-cset serverlog.maxmb.9=100"
$P4DBIN -r $P4ROOT "-cset serverlog.retain.9=10"

