#!/usr/bin/env bash
pip install -r /mnt/wa_worker/requirements.txt
python /mnt/wa_worker/message_receiver/start.py
while true; do
    echo running;
    sleep 1;
done
