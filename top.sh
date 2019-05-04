#!/bin/sh
# From: https://dzone.com/articles/monitoring-process-memorycpu-usage-with-top-and-pl
# Usage: ./monitor-usage.sh <PID of the process>
export PID=$1
rm top.dat
while true; do top -p $PID -b -n1 | egrep '^[0-9]+' | awk -v now=$(date +%s) '{print now,$6,$9}' >> top.dat; done