DROP TEMPORARY TABLE IF EXISTS venta_hora;

CREATE TEMPORARY TABLE IF NOT EXISTS venta_hora
SELECT
    v.fecha_venta AS dia,
    SUM(IF(v.tipo_venta = '0E',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 0E,
    SUM(IF(v.tipo_venta = '0T',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 0T,
    SUM(IF(v.tipo_venta = '1D',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 1D,
    SUM(IF(v.tipo_venta = '1I',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 1I,
    SUM(v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16'))) AS vta
FROM
    ventas AS v
    INNER JOIN mueblerias AS m ON
        m.clave_muebleria = v.clave_muebleria
WHERE
    v.fecha_venta = @FECHA_ANTERIOR AND
    v.valor_venta > 0 AND
    v.tipo_venta <> '0A' AND
    #FILTROS AND
    v.hora <= '24:00:00' AND
    m.activa = 1
GROUP BY v.fecha_venta,v.hora;

INSERT INTO venta_hora
SELECT
    b.fecha AS dia,
    0-SUM(IF(v.tipo_venta = '0E',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 0E,
    0-SUM(IF(v.tipo_venta = '0T',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 0T,
    0-SUM(IF(v.tipo_venta = '1D',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 1D,
    0-SUM(IF(v.tipo_venta = '1I',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 1I,
    0-SUM(v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16'))) AS vta
FROM
    baja AS b
    INNER JOIN ventas AS v ON
        v.folio_venta = b.folio_venta
    INNER JOIN mueblerias AS m ON
        m.clave_muebleria = v.clave_muebleria
WHERE
    b.fecha = @FECHA_ANTERIOR AND
    b.causa LIKE 'C%' AND
    #FILTROS AND
    v.hora <= '24:00:00' AND
    m.activa = 1
GROUP BY b.fecha,v.hora;

SELECT
    CONCAT_WS(
        CHAR(10 USING utf8),
        CONCAT('Ventas ',YEAR(@FECHA_ANTERIOR)),
        '',
        CONCAT('Fecha: ',DATE_FORMAT(dia,'%d/%m/%Y')),
        CONCAT('Contado efectivo $ ',FORMAT(SUM(0E),2)),
        CONCAT('Contado tarjeta  $ ',FORMAT(SUM(0T),2)),
        CONCAT('Credito directo  $ ',FORMAT(SUM(1D),2)),
        CONCAT('Credinomina      $ ',FORMAT(SUM(1I),2)),
               '----------------------------------',
        CONCAT('Total            $ ',FORMAT(SUM(vta),2))
    ) INTO @RESUMEN_ANIO_ANTERIOR
FROM venta_hora;

SELECT SUM(vta) INTO @VENTA_ANIO_ANTERIOR FROM venta_hora;

DROP TEMPORARY TABLE IF EXISTS venta_hora;

CREATE TEMPORARY TABLE IF NOT EXISTS venta_hora
SELECT
    v.fecha_venta AS dia,
    SUM(IF(v.tipo_venta = '0E',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 0E,
    SUM(IF(v.tipo_venta = '0T',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 0T,
    SUM(IF(v.tipo_venta = '1D',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 1D,
    SUM(IF(v.tipo_venta = '1I',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 1I,
    SUM(v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16'))) AS vta
FROM
    ventas AS v
    INNER JOIN mueblerias AS m ON
        m.clave_muebleria = v.clave_muebleria
WHERE
    v.fecha_venta = @FECHA_ACTUAL AND
    v.valor_venta > 0 AND
    v.tipo_venta <> '0A' AND
    #FILTROS AND
    v.hora <= '24:00:00' AND
    m.activa = 1
GROUP BY v.fecha_venta,v.hora;

INSERT INTO venta_hora
SELECT
    b.fecha AS dia,
    0-SUM(IF(v.tipo_venta = '0E',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 0E,
    0-SUM(IF(v.tipo_venta = '0T',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 0T,
    0-SUM(IF(v.tipo_venta = '1D',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 1D,
    0-SUM(IF(v.tipo_venta = '1I',v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16')),0)) AS 1I,
    0-SUM(v.valor_venta/(IF(v.clave_muebleria = 'TC18' AND v.fecha_venta < '2014-01-01','1.11','1.16'))) AS vta
FROM
    baja AS b
    INNER JOIN ventas AS v ON
        v.folio_venta = b.folio_venta
    INNER JOIN mueblerias AS m ON
        m.clave_muebleria = v.clave_muebleria
WHERE
    b.fecha = @FECHA_ACTUAL AND
    b.causa LIKE 'C%' AND
    #FILTROS AND
    v.hora <= '24:00:00' AND
    m.activa = 1
GROUP BY b.fecha,v.hora;

SELECT
    CONCAT_WS(
        CHAR(10 USING utf8),
        '',
        CONCAT('Ventas ',YEAR(@FECHA_ACTUAL)),
        '',
        CONCAT('Fecha: ',DATE_FORMAT(@FECHA_ACTUAL,'%d/%m/%Y')),
        CONCAT('Contado efectivo $ ',FORMAT(SUM(0E),2)),
        CONCAT('Contado tarjeta  $ ',FORMAT(SUM(0T),2)),
        CONCAT('Credito directo  $ ',FORMAT(SUM(1D),2)),
        CONCAT('Credinomina      $ ',FORMAT(SUM(1I),2)),
               '----------------------------------',
        CONCAT('Total            $ ',FORMAT(SUM(vta),2)),
        CONCAT('Diferencia       $ ',FORMAT((SUM(vta) - @VENTA_ANIO_ANTERIOR),2),' (',FORMAT(((SUM(vta)/ @VENTA_ANIO_ANTERIOR)-1)*100.0,2),' %)')
    ) INTO @RESUMEN_ANIO_ACTUAL
FROM venta_hora;

SELECT
    CONCAT_WS(
        CHAR(10 USING utf8),
        @LEYENDA,
        '',
        @RESUMEN_ANIO_ANTERIOR,
        @RESUMEN_ANIO_ACTUAL);
