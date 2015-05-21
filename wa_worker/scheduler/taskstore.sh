#!/usr/bin/bash
source /tmp/set_environment_vars.sh
/usr/bin/python $MOUNT_POINT/wa_worker/wa_worker/scheduler/taskstore.py --task $1
