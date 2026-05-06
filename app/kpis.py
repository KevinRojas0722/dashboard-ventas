"""
Cálculo de los KPIs principales del dashboard.
Cada función recibe un DataFrame ya filtrado y devuelve un valor listo para mostrar.
"""

import pandas as pd


def ventas_totales(df: pd.DataFrame) -> float:
    return df["total"].sum()


def ticket_promedio(df: pd.DataFrame) -> float:
    """Promedio de venta por transacción (una fila = una transacción)."""
    if df.empty:
        return 0.0
    return df["total"].mean()


def num_transacciones(df: pd.DataFrame) -> int:
    return len(df)


def clientes_unicos(df: pd.DataFrame) -> int:
    return df["cliente_id"].nunique()


def variacion_vs_periodo_anterior(
    df_actual: pd.DataFrame,
    df_anterior: pd.DataFrame,
    metrica: str = "total",
) -> float:
    """
    Calcula el % de cambio entre dos períodos.
    Útil para mostrar las flechas de tendencia en los KPI cards.
    Retorna None si el período anterior no tiene datos.
    """
    valor_anterior = df_anterior[metrica].sum()
    if valor_anterior == 0:
        return None
    valor_actual = df_actual[metrica].sum()
    return ((valor_actual - valor_anterior) / valor_anterior) * 100


def resumen_kpis(df: pd.DataFrame) -> dict:
    """Agrupa todos los KPIs en un solo dict para pasarlos cómodamente al dashboard."""
    return {
        "ventas_totales":   ventas_totales(df),
        "ticket_promedio":  ticket_promedio(df),
        "transacciones":    num_transacciones(df),
        "clientes_unicos":  clientes_unicos(df),
    }
