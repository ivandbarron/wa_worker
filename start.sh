#!/usr/bin/env bash
pip install -r $MOUNT_POINT/wa_worker/requirements.txt
python $MOUNT_POINT/wa_worker/message_receiver/start.py
while true; do
    echo running;
    sleep 1;
done
