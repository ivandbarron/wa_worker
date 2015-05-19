#!/usr/bin/env bash
python send_message.py \
--name "venta_por_hora_todos" \
--phones 5212287779788
--emails dbarron@crediland.com.mx
--cron 0 9-21/1 * * 1-6
--sql_file queries/venta.dia_semana.sql
--params \
    @FECHA_ACTUAL=CURDATE() \
    "@FECHA_ANTERIOR=DATE_SUB(@FECHA_ACTUAL,INTERVAL 364 DAY)" \
    "@LEYENDA=CONCAT('Del mismo dia en la semana ',WEEK(@FECHA_ACTUAL,6),' del anio')" \
    "#FILTROS=v.clave_muebleria NOT LIKE 'TCI%' AND v.clave_muebleria NOT IN ('TC00','TC96','TC43','TC99')"
