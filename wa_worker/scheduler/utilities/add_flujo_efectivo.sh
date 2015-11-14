#!/usr/bin/env bash

# Venta dia semana de lunes a domingo
python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name flujo_efectivo \
--phones 5212289790978 5212281404251 5212281049275 \
--mails pmarin@crediland.com.mx hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx \
--cron "15 10-23 * * 1-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/flujo_efectivo.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@LEYENDA=CONCAT('FLUJO DE EFECTIVO ',DATE_FORMAT(@FECHA_ACTUAL,'%d/%m/%Y'))"

python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name flujo_efectivo_dom \
--phones 5212289790978 5212281404251 5212281049275 \
--mails pmarin@crediland.com.mx hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx \
--cron "15 11-23 * * 0" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/flujo_efectivo.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@LEYENDA=CONCAT('FLUJO DE EFECTIVO ',DATE_FORMAT(@FECHA_ACTUAL,'%d/%m/%Y'))"


python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name flujo_efectivo_cierre \
--phones 5212289790978 5212281404251 5212281049275 \
--mails pmarin@crediland.com.mx hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx \
--cron "45 23 * * *" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/flujo_efectivo.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@LEYENDA=CONCAT('FLUJO DE EFECTIVO ',DATE_FORMAT(@FECHA_ACTUAL,'%d/%m/%Y'))"
