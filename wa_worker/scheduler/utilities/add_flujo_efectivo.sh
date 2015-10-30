#!/usr/bin/env bash

# Venta dia semana de lunes a domingo
python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name flujo_efectivo \
--phones 5212281049275 \
--mails julio.tovar@crediland.com.mx \
--cron "15 10-21 * * 1-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/flujo_efectivo.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@LEYENDA=CONCAT('FLUJO DE EFECTIVO ',DATE_FORMAT(@FECHA_ACTUAL,'%d/%m/%Y'))"

python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name flujo_efectivo_dom \
--phones 5212281049275 \
--mails julio.tovar@crediland.com.mx \
--cron "15 11-19 * * 0" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/flujo_efectivo.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@LEYENDA=CONCAT('FLUJO DE EFECTIVO ',DATE_FORMAT(@FECHA_ACTUAL,'%d/%m/%Y'))"
