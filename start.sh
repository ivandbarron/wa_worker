#!/usr/bin/env bash
echo ' [*] Changing timezone to Mexico City...';
rm /etc/localtime
ln -s /usr/share/zoneinfo/America/Mexico_City /etc/localtime
echo ''
echo ' [*] Saving current environment vars'
echo '#!/usr/bin/bash' > /tmp/set_environment_vars.sh
chmod 0755 /tmp/set_environment_vars.sh
env > /tmp/environment_vars
sed -e 's/^/export\ /' /tmp/environment_vars >> /tmp/set_environment_vars.sh
rm /tmp/environment_vars
echo ''
echo ' [*] Starting crond...'
crond -p
echo '';
echo ' [*] Loading requirements...';
pip install -r $MOUNT_POINT/wa_worker/requirements.txt
echo '';
echo ' [*] Starting message receiver...';
python $MOUNT_POINT/wa_worker/wa_worker/message_receiver/start.py &
echo '';
echo ' [*] Starting scheduler...';
python $MOUNT_POINT/wa_worker/wa_worker/scheduler/start.py &
while true; do
    echo ' [*] running...';
    sleep 10;
done
