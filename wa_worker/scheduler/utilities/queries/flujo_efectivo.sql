SELECT CURTIME() INTO @HORA_ACTUAL;

DROP TEMPORARY TABLE IF EXISTS tmp_ingresos_dia;
CREATE TEMPORARY TABLE IF NOT EXISTS tmp_ingresos_dia (
CE DOUBLE(12,2),
CT DOUBLE(12,2),
CR DOUBLE(12,2),
ENG DOUBLE(12,2),
ABOT DOUBLE(12,2),
ABOG DOUBLE(12,2),
ABOM DOUBLE(12,2),
ABOE DOUBLE(12,2),
ABOP DOUBLE(12,2),
ABOI DOUBLE(12,2),
OTR DOUBLE(12,2));

INSERT INTO tmp_ingresos_dia
SELECT
    IF(v.tipo_venta = '0E',v.valor_venta,0) AS CE,
    IF(v.tipo_venta = '0T',v.valor_venta,0) AS CT,
    IF(v.tipo_venta = '0D',c.enganche,0) AS CR,
    IF(v.tipo_venta LIKE '1%',c.enganche,0) AS ENG,
    0 AS ABOT,
    0 AS ABOG,
    0 AS ABOM,
    0 AS ABOE,
    0 AS ABOP,
    0 AS ABOI,
    0 AS OTR
FROM
    ventas AS v
    LEFT JOIN credito AS c ON
        c.folio_venta = v.folio_venta
WHERE v.fecha_venta = @FECHA_ACTUAL;

INSERT INTO tmp_ingresos_dia
SELECT
    IF(v.tipo_venta = '0E',0-(b.devolucion_enganche+b.devolucion_resto_enganche+b.devolucion_capital+b.devolucion_intereses),0) AS CE,
    IF(v.tipo_venta = '0T',0-(b.devolucion_enganche+b.devolucion_resto_enganche+b.devolucion_capital+b.devolucion_intereses),0) AS CT,
    IF(v.tipo_venta = '0D',0-(b.devolucion_enganche+b.devolucion_resto_enganche+b.devolucion_capital+b.devolucion_intereses),0) AS CR,
    IF(v.tipo_venta LIKE '1%',0-(b.devolucion_enganche+b.devolucion_resto_enganche+b.devolucion_capital+b.devolucion_intereses),0) AS ENG,
    0 AS ABOT,
    0 AS ABOG,
    0 AS ABOM,
    0 AS ABOE,
    0 AS ABOP,
    0 AS ABOI,
    0 AS OTR
FROM
    baja AS b
    INNER JOIN ventas AS v ON
        v.folio_venta = b.folio_venta
WHERE
    b.fecha = @FECHA_ACTUAL AND
    b.causa <> 'A1';

INSERT INTO tmp_ingresos_dia
SELECT
    0 AS CE,
    0 AS CT,
    0 AS CR,
    0 AS ENG,
    IF(c.jurisdiccion <> 'I' AND IF(a.responsable_cuenta='',c.responsable_cuenta,a.responsable_cuenta) LIKE 'T%',a.cantidad_abono+a.intereses,0) AS ABOT,
    IF(c.jurisdiccion <> 'I' AND IF(a.responsable_cuenta='',c.responsable_cuenta,a.responsable_cuenta) LIKE 'G%',a.cantidad_abono+a.intereses,0) AS ABOG,
    IF(c.jurisdiccion <> 'I' AND IF(a.responsable_cuenta='',c.responsable_cuenta,a.responsable_cuenta) LIKE 'M%',a.cantidad_abono+a.intereses,0) AS ABOM,
    IF(c.jurisdiccion <> 'I' AND IF(a.responsable_cuenta='',c.responsable_cuenta,a.responsable_cuenta) LIKE 'E%',a.cantidad_abono+a.intereses,0) AS ABOE,
    IF(c.jurisdiccion <> 'I' AND LEFT(IF(a.responsable_cuenta='',c.responsable_cuenta,a.responsable_cuenta),1) NOT IN ('T','G','M','E','U'),a.cantidad_abono+a.intereses,0) AS ABOP,
    IF(c.jurisdiccion <> 'I' AND IF(a.responsable_cuenta='',c.responsable_cuenta,a.responsable_cuenta) LIKE 'U%',a.cantidad_abono+a.intereses,0) AS ABOI,
    IF(c.jurisdiccion = 'I',a.cantidad_abono+a.intereses,0) AS OTR
FROM
    abonos AS a
    INNER JOIN credito AS c ON
        c.folio_venta = a.folio_venta
    INNER JOIN ventas AS v ON
        v.folio_venta = a.folio_venta
WHERE
    a.fecha_abono = @FECHA_ACTUAL AND
    a.punto_recepcion NOT LIKE 'CCI%' AND
    a.punto_recepcion <> 'CD02' AND
    v.clave_muebleria LIKE 'TC%';

SELECT
    CONCAT_WS(
        CHAR(10 USING utf8),
        @LEYENDA,
        CONCAT('A las ',HOUR(@HORA_ACTUAL),' horas'),
        CONCAT('Contado efectivo $ ',FORMAT(IFNULL(SUM(CE),0.0),2)),
        CONCAT('Contado tarjeta $ ',FORMAT(IFNULL(SUM(CT),0.0),2)),
        CONCAT('Contado resto $ ',FORMAT(IFNULL(SUM(CR),0.0),2)),
        CONCAT('Enganches $ ',FORMAT(IFNULL(SUM(ENG),0.0),2)),
        CONCAT('Cobros tienda $ ',FORMAT(IFNULL(SUM(ABOT),0.0),2)),
        CONCAT('Cobros telefonica $ ',FORMAT(IFNULL(SUM(ABOG),0.0),2)),
        CONCAT('Cobros presencial $ ',FORMAT(IFNULL(SUM(ABOM),0.0),2)),
        CONCAT('Cobros Extra-Jud. $ ',FORMAT(IFNULL(SUM(ABOE),0.0),2)),
        CONCAT('Cobros Pre-Jud. $ ',FORMAT(IFNULL(SUM(ABOP),0.0),2)),
        CONCAT('Cobros credinomina $ ',FORMAT(IFNULL(SUM(ABOI),0.0),2)),
        CONCAT('Cobros cart. dict. $ ',FORMAT(IFNULL(SUM(OTR),0.0),2)),
                      '------------------------------------',
        CONCAT('TOTAL:  $ ',FORMAT(IFNULL(SUM(CE+CT+CR+ENG+ABOT+ABOG+ABOM+ABOE+ABOP+ABOI+OTR),0.0),2)))
FROM tmp_ingresos_dia;
