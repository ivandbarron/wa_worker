#!/usr/bin/env bash

# Venta dia semana de lunes a domingo
python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name venta_semana_caravana \
--phones 5212289790978 5212281404251 5212281049275 \
--mails hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx pmarin@crediland.com.mx \
--cron "5 11-23 * * 0-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/venta.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 385 DAY)" \
    "@LEYENDA='CARAVANA SABADO 2014 vs 2015'" \
    "#FILTROS=v.clave_muebleria = 'TC99'"


# Venta dia calendario de lunes a domingo
python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name venta_calendario_caravana \
--phones 5212289790978 5212281404251 5212281049275 \
--mails hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx pmarin@crediland.com.mx \
--cron "6 11-23 * * 0-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/venta.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 384 DAY)" \
    "@LEYENDA='CARAVANA 14/SEP/2014 vs 3/OCT/2015'" \
    "#FILTROS=v.clave_muebleria = 'TC99'"

