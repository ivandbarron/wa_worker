#!/usr/bin/env bash
echo ' [*] Changing timezone to Mexico City';
rm /etc/localtime
ln -s /usr/share/zoneinfo/America/Mexico_City /etc/localtime
echo '';
echo ' [*] Loading pyhon requirments...';
pip install -r $MOUNT_POINT/wa_worker/requirements.txt
echo '';
echo ' [*] Starting message receiver...';
python $MOUNT_POINT/wa_worker/message_receiver/start.py &
echo '';
echo ' [*] Starting scheduler...';
python $MOUNT_POINT/wa_worker/scheduler/start.py &
while true; do
    echo ' [*] running...';
    sleep 10;
done
