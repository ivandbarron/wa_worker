SELECT CURTIME() INTO @HORA_ACTUAL;

DROP TEMPORARY TABLE IF EXISTS venta_hora;

CREATE TEMPORARY TABLE IF NOT EXISTS venta_hora
SELECT
    v.fecha_venta AS dia,
    HOUR(v.hora) AS hora,
    COUNT(v.folio_venta) AS ope,
    SUM(v.valor_venta/(IF(v.clave_muebleria = "TC18" AND v.fecha_venta < "2014-01-01","1.11","1.16"))) AS vta
FROM
    ventas AS v
    INNER JOIN mueblerias AS m ON
        m.clave_muebleria = v.clave_muebleria
WHERE
    v.fecha_venta = @FECHA_ACTUAL AND
    v.valor_venta > 0 AND
    v.tipo_venta <> "0A" AND
    #FILTROS AND
    HOUR(v.hora) < HOUR(@HORA_ACTUAL) AND
    m.activa = 1
GROUP BY v.fecha_venta,v.hora;

INSERT INTO venta_hora
SELECT
    b.fecha AS dia,
    HOUR(v.hora) AS hora,
    0-COUNT(b.folio_venta) AS ope,
    0-SUM(v.valor_venta/(IF(v.clave_muebleria = "TC18" AND v.fecha_venta < "2014-01-01","1.11","1.16"))) AS vta
FROM
    baja AS b
    INNER JOIN ventas AS v ON
        v.folio_venta = b.folio_venta
    INNER JOIN mueblerias AS m ON
        m.clave_muebleria = v.clave_muebleria
WHERE
    b.fecha = @FECHA_ACTUAL AND
    b.causa LIKE "C%" AND
    #FILTROS AND
    HOUR(v.hora) < HOUR(@HORA_ACTUAL) AND
    m.activa = 1
GROUP BY b.fecha,v.hora;

INSERT INTO venta_hora
SELECT
    v.fecha_venta AS dia,
    HOUR(v.hora) AS hora,
    COUNT(v.folio_venta) AS ope,
    SUM(v.valor_venta/(IF(v.clave_muebleria = "TC18" AND v.fecha_venta < "2014-01-01","1.11","1.16"))) AS vta
FROM
    ventas AS v
    INNER JOIN mueblerias AS m ON
        m.clave_muebleria = v.clave_muebleria
WHERE
    v.fecha_venta = @FECHA_ANTERIOR AND
    v.valor_venta > 0 AND
    v.tipo_venta <> "0A" AND
    #FILTROS AND
    HOUR(v.hora) < HOUR(@HORA_ACTUAL) AND
    m.activa = 1
GROUP BY v.fecha_venta,v.hora;

INSERT INTO venta_hora
SELECT
    b.fecha AS dia,
    HOUR(v.hora) AS hora,
    0-COUNT(b.folio_venta) AS ope,
    0-SUM(v.valor_venta/(IF(v.clave_muebleria = "TC18" AND v.fecha_venta < "2014-01-01","1.11","1.16"))) AS vta
FROM
    baja AS b
    INNER JOIN ventas AS v ON
        v.folio_venta = b.folio_venta
    INNER JOIN mueblerias AS m ON
        m.clave_muebleria = v.clave_muebleria
WHERE
    b.fecha = @FECHA_ANTERIOR AND
    b.causa LIKE "C%" AND
    #FILTROS AND
    HOUR(v.hora) < HOUR(@HORA_ACTUAL) AND
    m.activa = 1
GROUP BY b.fecha,v.hora;

SELECT (SUM(IF(dia = @FECHA_ACTUAL,vta,0)) - SUM(IF(dia = @FECHA_ANTERIOR,vta,0))) INTO @VARIACION_CANTIDAD
FROM venta_hora;

SELECT IF(@VARIACION_CANTIDAD > 0,'+','') INTO @SIGNO;

SELECT (((SUM(IF(dia = @FECHA_ACTUAL,vta,0)) / SUM(IF(dia = @FECHA_ANTERIOR,vta,0)))) - 1) * 100 INTO @VARIACION_PORCENTAJE
FROM venta_hora;

SELECT
    CONCAT_WS(
        CHAR(10 USING utf8),
        CONCAT('A las ',HOUR(@HORA_ACTUAL),' horas'),
        @LEYENDA,
        CONCAT('Venta ',YEAR(@FECHA_ANTERIOR),' $ ',FORMAT(SUM(IF(dia = @FECHA_ANTERIOR,vta,0)),2)),
        CONCAT('Venta ',YEAR(@FECHA_ACTUAL),' $ ',FORMAT(SUM(IF(dia = @FECHA_ACTUAL,vta,0)),2)),
        CONCAT('Variacion  $ ',FORMAT(@VARIACION_CANTIDAD,2),' (',@SIGNO,FORMAT(@VARIACION_PORCENTAJE,2),') %')
    ) AS mensaje
FROM venta_hora;
