#!/usr/bin/env bash

# Venta dia semana de lunes a domingo
python task_manager.py \
--op add \
--name venta_semana \
--phones 5212287779788 \
--mails dbarron@crediland.com.mx \
--cron "0 10-21/1 * * 1-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/venta.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 364 DAY)" \
    "@LEYENDA=CONCAT('Del mismo dia en la semana ',WEEK(@FECHA_ACTUAL,6),' del anio')" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"

python task_manager.py \
--op add \
--name venta_semana_dom \
--phones 5212287779788 \
--mails dbarron@crediland.com.mx \
--cron "0 11-19/1 * * 7" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/venta.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 364 DAY)" \
    "@LEYENDA=CONCAT('Del mismo dia en la semana ',WEEK(@FECHA_ACTUAL,6),' del anio')" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"

# Venta dia calendario de lunes a domingo
python task_manager.py \
--op add \
--name venta_calendario \
--phones 5212287779788 \
--mails dbarron@crediland.com.mx \
--cron "1 10-21/1 * * 1-6" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/venta.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 1 YEAR)" \
    "@LEYENDA='Del mismo dia del calendario'" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"

python task_manager.py \
--op add \
--name venta_calendario_dom \
--phones 5212287779788 \
--mails dbarron@crediland.com.mx \
--cron "1 11-19/1 * * 7" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/venta.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 1 YEAR)" \
    "@LEYENDA='Del mismo dia del calendario'" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"
