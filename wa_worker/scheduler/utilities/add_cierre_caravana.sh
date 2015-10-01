#!/usr/bin/env bash

# Venta dia semana de lunes a domingo
python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name cierre_semana_caravana \
--phones 5212289790978 5212281404251 5212281049275 \
--mails hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx pmarin@crediland.com.mx \
--cron "10 23 * * 0-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/cierre.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 385 DAY)" \
    "@LEYENDA='CARAVANA VIERNES 2015 vs 2014'" \
    "#FILTROS=v.clave_muebleria = 'TC99'"

# Venta dia calendario de lunes a domingo
python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name cierre_calendario_caravana \
--phones 5212289790978 5212281404251 5212281049275 \
--mails hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx pmarin@crediland.com.mx \
--cron "11 23 * * 0-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/cierre.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 384 DAY)" \
    "@LEYENDA='CARAVANA 2/OCT/2015 vs 13/SEP/2014'" \
    "#FILTROS=v.clave_muebleria = 'TC99'"

