export ETCD_ENDPOINT="$(ifconfig docker0 | awk '/\<inet\>/ { print $2}')"
pip install -r /mnt/wa_worker/requirements.txt
while true; do
    echo ".";
    sleep 10;
done
