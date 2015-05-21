#!/usr/bin/env bash
python add_task.py \
--name "venta_david" \
--phones 5212287779788 \
--mails dbarron@crediland.com.mx \
--cron "*/5 * * * *" \
--sql_file $MOUNT_POINT/wa_worker/wa_worker/scheduler/utilities/queries/venta.dia_semana.sql \
--params \
    "@FECHA_ACTUAL=CURDATE()" \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 364 DAY)" \
    "@LEYENDA=CONCAT('Del mismo dia en la semana ',WEEK(@FECHA_ACTUAL,6),' del anio')" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"
