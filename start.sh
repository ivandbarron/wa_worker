#!/usr/bin/env bash
rm /etc/localtime
ln -s /usr/share/zoneinfo/America/Mexico_City /etc/localtime
pip install -r $MOUNT_POINT/wa_worker/requirements.txt
echo ''
echo ' [*] Starting...'
python $MOUNT_POINT/wa_worker/message_receiver/start.py
while true; do
    echo ' [*] running...';
    sleep 10;
done
