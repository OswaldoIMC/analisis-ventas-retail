-- =========================================================
-- Análisis de ventas - Consultas SQL
-- Base de datos: data/ventas.db | Tabla: ventas
-- =========================================================

-- 1. Ingresos totales y ticket promedio por sucursal
SELECT
    sucursal,
    COUNT(DISTINCT id_venta) AS num_transacciones,
    ROUND(SUM(total), 2) AS ingresos_totales,
    ROUND(SUM(total) * 1.0 / COUNT(DISTINCT id_venta), 2) AS ticket_promedio
FROM ventas
GROUP BY sucursal
ORDER BY ingresos_totales DESC;

-- 2. Ventas mensuales (tendencia en el tiempo)
SELECT
    strftime('%Y-%m', fecha) AS mes,
    ROUND(SUM(total), 2) AS ingresos,
    COUNT(DISTINCT id_venta) AS transacciones
FROM ventas
GROUP BY mes
ORDER BY mes;

-- 3. Top 10 productos por ingresos generados
SELECT
    producto,
    categoria,
    SUM(cantidad) AS unidades_vendidas,
    ROUND(SUM(total), 2) AS ingresos
FROM ventas
GROUP BY producto, categoria
ORDER BY ingresos DESC
LIMIT 10;

-- 4. Ingresos por categoría
SELECT
    categoria,
    ROUND(SUM(total), 2) AS ingresos,
    ROUND(SUM(total) * 100.0 / (SELECT SUM(total) FROM ventas), 1) AS porcentaje_del_total
FROM ventas
GROUP BY categoria
ORDER BY ingresos DESC;

-- 5. Ventas por día de la semana
SELECT
    CASE CAST(strftime('%w', fecha) AS INTEGER)
        WHEN 0 THEN '0-Domingo' WHEN 1 THEN '1-Lunes' WHEN 2 THEN '2-Martes'
        WHEN 3 THEN '3-Miércoles' WHEN 4 THEN '4-Jueves' WHEN 5 THEN '5-Viernes'
        WHEN 6 THEN '6-Sábado'
    END AS dia_semana,
    COUNT(DISTINCT id_venta) AS transacciones,
    ROUND(AVG(total), 2) AS venta_promedio_linea
FROM ventas
GROUP BY dia_semana
ORDER BY dia_semana;

-- 6. Método de pago más utilizado
SELECT
    metodo_pago,
    COUNT(DISTINCT id_venta) AS transacciones,
    ROUND(SUM(total), 2) AS ingresos,
    ROUND(COUNT(DISTINCT id_venta) * 100.0 /
        (SELECT COUNT(DISTINCT id_venta) FROM ventas), 1) AS porcentaje
FROM ventas
GROUP BY metodo_pago
ORDER BY transacciones DESC;

-- 7. Clientes más frecuentes (top 10) - para programas de lealtad
SELECT
    cliente_id,
    COUNT(DISTINCT id_venta) AS num_compras,
    ROUND(SUM(total), 2) AS gasto_total,
    ROUND(SUM(total) * 1.0 / COUNT(DISTINCT id_venta), 2) AS ticket_promedio
FROM ventas
GROUP BY cliente_id
ORDER BY gasto_total DESC
LIMIT 10;

-- 8. Crecimiento mes a mes (variación % de ingresos)
WITH mensual AS (
    SELECT strftime('%Y-%m', fecha) AS mes, SUM(total) AS ingresos
    FROM ventas
    GROUP BY mes
)
SELECT
    mes,
    ROUND(ingresos, 2) AS ingresos,
    ROUND(
        (ingresos - LAG(ingresos) OVER (ORDER BY mes)) * 100.0
        / LAG(ingresos) OVER (ORDER BY mes), 1
    ) AS variacion_pct
FROM mensual
ORDER BY mes;
