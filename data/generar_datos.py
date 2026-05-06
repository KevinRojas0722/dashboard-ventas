"""
Genera un dataset sintético de ventas para el dashboard de análisis.
Produce ~5000 transacciones con 2 años de historia y patrones realistas.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import date
import random
import os

fake = Faker("es")
rng = np.random.default_rng(seed=42)  # seed fija para reproducibilidad

# ── Catálogos ────────────────────────────────────────────────────────────────

PRODUCTOS = {
    "Electrónica": [
        ("Laptop Lenovo IdeaPad", 8_500),
        ("Monitor Samsung 24\"", 3_200),
        ("Teclado Mecánico Redragon", 950),
        ("Mouse Inalámbrico Logitech", 450),
        ("Auriculares Sony WH", 2_100),
        ("Webcam Logitech C920", 1_350),
        ("Tablet Samsung A8", 4_800),
        ("Hub USB-C 7 puertos", 680),
    ],
    "Oficina": [
        ("Silla Ergonómica Pro", 5_200),
        ("Escritorio de Pie", 7_800),
        ("Lámpara LED de Escritorio", 420),
        ("Organizador de Cables", 180),
        ("Porta Monitores Doble", 1_650),
        ("Pizarrón Magnético 90x60", 890),
    ],
    "Software": [
        ("Licencia Microsoft 365", 1_800),
        ("Antivirus Kaspersky 1 año", 650),
        ("Adobe Creative Cloud", 3_400),
        ("Slack Pro mensual", 280),
        ("Zoom Business anual", 1_200),
    ],
    "Accesorios": [
        ("Mochila para Laptop 15\"", 720),
        ("Funda Neopreno 14\"", 290),
        ("Limpiador de Pantalla Kit", 95),
        ("Cable HDMI 2m", 150),
        ("Regleta con supresor", 380),
        ("Base Enfriadora Laptop", 560),
    ],
}

# Provincias de Costa Rica con distribución proporcional a su actividad comercial
REGIONES = {
    "San José":    0.35,
    "Alajuela":    0.20,
    "Heredia":     0.17,
    "Cartago":     0.13,
    "Guanacaste":  0.07,
    "Puntarenas":  0.05,
    "Limón":       0.03,
}

VENDEDORES = [
    "Andrea Mora", "Carlos Quesada", "María Solís",
    "José Vargas", "Laura Jiménez", "Luis Arias",
    "Sofía Brenes", "Diego Rojas", "Valeria Monge",
    "Andrés Campos",
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def peso_estacional(fecha: date) -> float:
    """Más ventas en Q4 (noviembre/diciembre) y en enero por reposición."""
    mes = fecha.month
    pesos = {1: 1.2, 2: 0.9, 3: 1.0, 4: 1.0, 5: 1.1, 6: 0.95,
             7: 0.9, 8: 0.95, 9: 1.05, 10: 1.1, 11: 1.4, 12: 1.6}
    return pesos[mes]


def generar_fechas(n: int, inicio: date, fin: date) -> list[date]:
    """Fechas aleatorias con más transacciones en días laborables."""
    fechas = []
    dias_totales = (fin - inicio).days
    while len(fechas) < n:
        offset = rng.integers(0, dias_totales)
        d = inicio + pd.Timedelta(days=int(offset))
        # días de semana tienen el doble de probabilidad que fin de semana
        prob = 1.0 if d.weekday() < 5 else 0.45
        if rng.random() < prob * peso_estacional(d):
            fechas.append(d)
    return fechas[:n]


def variacion_precio(precio_base: float) -> float:
    """Precio con variación de ±8% para simular promociones y precios distintos."""
    return round(precio_base * rng.uniform(0.92, 1.08), 2)

# ── Generación principal ──────────────────────────────────────────────────────

def generar_dataset(n_filas: int = 5_000) -> pd.DataFrame:
    inicio = date(2024, 1, 1)
    fin = date(2025, 12, 31)

    fechas = generar_fechas(n_filas, inicio, fin)

    # Construir listas planas de productos con su categoría
    productos_lista = [
        (nombre, precio, cat)
        for cat, items in PRODUCTOS.items()
        for nombre, precio in items
    ]
    nombres_productos = [p[0] for p in productos_lista]
    precios_base     = [p[1] for p in productos_lista]
    categorias_prod  = [p[2] for p in productos_lista]

    # Índices de producto con distribución no uniforme (algunos venden más)
    pesos_prod = rng.dirichlet(np.ones(len(productos_lista)) * 0.5)
    idx_prod   = rng.choice(len(productos_lista), size=n_filas, p=pesos_prod)

    # Regiones con probabilidades del catálogo
    regiones = list(REGIONES.keys())
    probs_reg = list(REGIONES.values())
    region_col = rng.choice(regiones, size=n_filas, p=probs_reg)

    # Cantidad: mayoría 1-3 unidades, ocasionalmente más (compras corporativas)
    cantidades = rng.choice([1, 1, 1, 2, 2, 3, 5, 10], size=n_filas,
                            p=[0.40, 0.20, 0.15, 0.10, 0.07, 0.04, 0.02, 0.02])

    # IDs de cliente: ~800 clientes únicos → algunos compran varias veces
    cliente_ids = rng.integers(1001, 1801, size=n_filas)

    filas = []
    for i in range(n_filas):
        p_idx = idx_prod[i]
        precio = variacion_precio(precios_base[p_idx])
        cant   = int(cantidades[i])
        total  = round(precio * cant, 2)

        filas.append({
            "fecha":           fechas[i],
            "producto":        nombres_productos[p_idx],
            "categoria":       categorias_prod[p_idx],
            "cantidad":        cant,
            "precio_unitario": precio,
            "total":           total,
            "region":          str(region_col[i]),
            "vendedor":        random.choice(VENDEDORES),
            "cliente_id":      f"CLI-{cliente_ids[i]}",
        })

    df = pd.DataFrame(filas)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha").reset_index(drop=True)
    return df


def main():
    print("Generando dataset de ventas...")
    df = generar_dataset(5_000)

    # Guardar CSV en la misma carpeta data/
    ruta_salida = os.path.join(os.path.dirname(__file__), "ventas.csv")
    df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")

    print(f"[OK] Dataset guardado en: {ruta_salida}")
    print(f"  Filas:            {len(df):,}")
    print(f"  Rango de fechas:  {df['fecha'].min().date()} a {df['fecha'].max().date()}")
    print(f"  Clientes únicos:  {df['cliente_id'].nunique():,}")
    print(f"  Productos únicos: {df['producto'].nunique():,}")
    print(f"  Venta total:     ${df['total'].sum():,.2f}")
    print(f"\nVentas por categoría:")
    print(df.groupby("categoria")["total"].sum().sort_values(ascending=False)
            .apply(lambda x: f"  ${x:,.0f}").to_string())


if __name__ == "__main__":
    main()
