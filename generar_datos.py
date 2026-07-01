"""
Genera un dataset sintético de ventas para una tienda minorista (Fellitofe). Incluye estacionalidad, 
efecto de fin de semana, productos con distinta popularidad, y clientes recurrentes.
"""
import numpy as np
import pandas as pd
from datetime import date, timedelta
import sqlite3

np.random.seed(42)

# --- Catálogo de productos ---
productos = {
    "Refresco 600ml":        ("Bebidas",     14),
    "Agua 1L":                ("Bebidas",     12),
    "Cerveza 355ml":          ("Bebidas",     22),
    "Papas fritas":           ("Botanas",     18),
    "Chicharrón":             ("Botanas",     20),
    "Cacahuates":             ("Botanas",     15),
    "Pan de dulce":           ("Panadería",   10),
    "Bolillo":                ("Panadería",    3),
    "Leche 1L":               ("Lácteos",     24),
    "Queso 250g":             ("Lácteos",     45),
    "Huevo (docena)":         ("Abarrotes",   32),
    "Aceite 1L":              ("Abarrotes",   38),
    "Arroz 1kg":               ("Abarrotes",  22),
    "Frijol 1kg":              ("Abarrotes",  28),
    "Detergente":             ("Limpieza",     55),
    "Jabón de baño":          ("Limpieza",     14),
    "Papel higiénico (4u)":   ("Limpieza",     35),
    "Shampoo":                ("Cuidado personal", 48),
    "Pasta dental":           ("Cuidado personal", 30),
    "Cigarros (caja)":        ("Otros",        65),
}
prod_names = list(productos.keys())
# popularidad: algunos productos se venden mucho más que otros (ley de Pareto)
popularidad = np.random.dirichlet(np.ones(len(prod_names)) * 0.4)

sucursales = ["Centro", "Norte", "Del Valle"]
metodos_pago = ["Efectivo", "Tarjeta", "Transferencia"]

# --- Clientes: algunos son recurrentes, otros ocasionales ---
n_clientes = 220
clientes = [f"C{str(i).zfill(4)}" for i in range(1, n_clientes + 1)]
# 20% de los clientes concentra más frecuencia de compra (clientes frecuentes)
peso_clientes = np.concatenate([
    np.random.uniform(3, 6, int(n_clientes * 0.2)),
    np.random.uniform(0.3, 1.2, n_clientes - int(n_clientes * 0.2))
])
peso_clientes = peso_clientes / peso_clientes.sum()

# --- Rango de fechas: un año completo ---
start = date(2025, 7, 1)
end = date(2026, 6, 30)
dias = pd.date_range(start, end, freq="D")

filas = []
venta_id = 1

for dia in dias:
    dow = dia.dayofweek  # 0=lunes
    mes = dia.month

    # Estacionalidad: más ventas en diciembre (fiestas) y quincenas, menos en enero
    factor_mes = 1.0
    if mes == 12:
        factor_mes = 1.6
    elif mes == 1:
        factor_mes = 0.8
    elif mes in (7, 8):
        factor_mes = 1.1  # vacaciones

    # Efecto fin de semana
    factor_dow = 1.4 if dow in (4, 5) else (1.2 if dow == 6 else 1.0)

    # Efecto quincena (días 1, 15 del mes con más ventas)
    factor_quincena = 1.3 if dia.day in (1, 2, 15, 16) else 1.0

    base_transacciones = 14
    n_transacciones = np.random.poisson(
        base_transacciones * factor_mes * factor_dow * factor_quincena
    )

    for _ in range(n_transacciones):
        cliente = np.random.choice(clientes, p=peso_clientes)
        sucursal = np.random.choice(sucursales, p=[0.5, 0.3, 0.2])
        metodo = np.random.choice(metodos_pago, p=[0.55, 0.35, 0.10])

        n_items = np.random.randint(1, 6)
        productos_venta = np.random.choice(prod_names, size=n_items, p=popularidad, replace=True)

        for prod in productos_venta:
            categoria, precio_base = productos[prod]
            # pequeña variación de precio (promos / redondeos)
            precio = round(precio_base * np.random.uniform(0.95, 1.05), 2)
            cantidad = np.random.randint(1, 4)
            filas.append({
                "id_venta": venta_id,
                "fecha": dia.date().isoformat(),
                "cliente_id": cliente,
                "sucursal": sucursal,
                "metodo_pago": metodo,
                "producto": prod,
                "categoria": categoria,
                "cantidad": cantidad,
                "precio_unitario": precio,
                "total": round(precio * cantidad, 2),
            })
        venta_id += 1

df = pd.DataFrame(filas)
print(f"Filas generadas: {len(df):,}")
print(f"Transacciones (ventas) únicas: {df['id_venta'].nunique():,}")
print(f"Rango de fechas: {df['fecha'].min()} a {df['fecha'].max()}")

df.to_csv("/proyecto-ventas/data/ventas.csv", index=False, encoding="utf-8")

# --- Cargar a SQLite ---
conn = sqlite3.connect("/proyecto-ventas/data/ventas.db")
df.to_sql("ventas", conn, if_exists="replace", index=False)
conn.execute("CREATE INDEX IF NOT EXISTS idx_fecha ON ventas(fecha)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_cliente ON ventas(cliente_id)")
conn.commit()
conn.close()
print("Base de datos SQLite creada: data/ventas.db")
