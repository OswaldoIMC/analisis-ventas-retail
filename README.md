# Análisis de Ventas - Tienda Minorista

Proyecto de análisis de datos que simula el comportamiento de ventas de un negocio
minorista con 3 sucursales, inspirado en un sistema de punto de venta (POS) real
que desarrollé anteriormente (Fellitofe).

El objetivo es responder preguntas de negocio reales usando el flujo de trabajo
típico de un analista de datos: **extracción con SQL → transformación y análisis
con pandas → visualización → conclusiones accionables.**

## Preguntas de negocio respondidas

- ¿Qué sucursal genera más ingresos y cuál tiene mejor ticket promedio?
- ¿Existe estacionalidad en las ventas a lo largo del año?
- ¿Cuáles son los productos y categorías más rentables?
- ¿Qué días de la semana tienen mayor demanda?
- ¿Qué tan concentrados están los ingresos en los clientes más frecuentes?

## Estructura del proyecto

```
proyecto-ventas/
├── generar_datos.py        # Genera el dataset sintético con patrones realistas
├── consultas.sql            # 8 consultas SQL de negocio, documentadas
├── analisis_ventas.ipynb    # Notebook con el análisis completo + gráficas + insights
├── data/
│   ├── ventas.csv            # Dataset en formato plano
│   └── ventas.db             # Mismo dataset cargado en SQLite
└── outputs/                  # Gráficas exportadas en PNG
```

## Sobre los datos

El dataset es **sintético** (generado con `generar_datos.py`), pero diseñado con
patrones estadísticos realistas:

- Estacionalidad (pico en diciembre, caída en enero)
- Efecto de fin de semana y quincena
- Distribución de popularidad de productos tipo Pareto
- Clientes recurrentes vs. ocasionales

Esto permite mostrar el proceso analítico completo sin depender de datos
confidenciales de un negocio real.

## Herramientas utilizadas

- **Python:** pandas, numpy, matplotlib, seaborn
- **SQL:** SQLite (consultas de agregación, ventana `LAG()` para variación mensual)
- **Jupyter Notebook** para el reporte final

## Principales hallazgos

1. La sucursal **Centro** concentra la mayor parte de los ingresos.
2. Las ventas tienen un pico claro en **diciembre** y caen en **enero**.
3. Las categorías **Abarrotes** y **Bebidas** generan la mayoría de los ingresos.
4. **Viernes y sábado** son los días de mayor actividad.
5. El **20% de los clientes más frecuentes genera cerca del 60% de los ingresos**
   — un fuerte argumento para un programa de lealtad dirigido.
