#!/usr/bin/env bash

# Venta dia semana de lunes a domingo
python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name cierre_semana \
--phones 5212289790978 5212281404251 5212281049275 \
--mails pmarin@crediland.com.mx hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx \
--cron "45 23 * * 1-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/cierre.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 364 DAY)" \
    "@LEYENDA=CONCAT('Del mismo dia en la semana ',WEEK(@FECHA_ACTUAL,6),' del anio')" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"

python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name cierre_semana_dom \
--phones 5212289790978 5212281404251 5212281049275 \
--mails pmarin@crediland.com.mx hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx \
--cron "45 23 * * 0" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/cierre.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 364 DAY)" \
    "@LEYENDA=CONCAT('Del mismo dia en la semana ',WEEK(@FECHA_ACTUAL,6),' del anio')" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"

# Venta dia calendario de lunes a domingo
#python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name cierre_calendario \
--phones 5212289790978 5212281404251 5212281049275 \
--mails pmarin@crediland.com.mx hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx \
--cron "11 21 * * 1-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/cierre.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 1 YEAR)" \
    "@LEYENDA='Del mismo dia del calendario'" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"

#python $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/task_manager.py \
--op add \
--name cierre_calendario_dom \
--phones 5212289790978 5212281404251 5212281049275 \
--mails pmarin@crediland.com.mx hrodriguez@crediland.com.mx julio.tovar@crediland.com.mx \
--cron "11 19 * * 0" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/cierre.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 1 YEAR)" \
    "@LEYENDA='Del mismo dia del calendario'" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"
