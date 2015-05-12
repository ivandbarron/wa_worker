#!/usr/bin/env bash
export ETCD_ENDPOINT="$(ifconfig docker0 | awk '/\<inet\>/ { print $2}')"
#pip install -r /mnt/wa_worker/requirements.txt
while true; do
    echo running;
    sleep 1;
done
