"""
Funciones auxiliares: carga de datos y aplicación de filtros.
Es el único lugar donde se lee el CSV — el resto de módulos recibe DataFrames ya filtrados.
"""

import pandas as pd
import streamlit as st
from pathlib import Path

RUTA_CSV = Path(__file__).parent.parent / "data" / "ventas.csv"


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """
    Lee el CSV una sola vez y lo cachea en sesión.
    st.cache_data evita releer el archivo en cada interacción del usuario.
    """
    df = pd.read_csv(RUTA_CSV, parse_dates=["fecha"], encoding="utf-8-sig")
    df["mes"] = df["fecha"].dt.to_period("M")
    df["anio"] = df["fecha"].dt.year
    df["trimestre"] = df["fecha"].dt.to_period("Q")
    return df


def aplicar_filtros(
    df: pd.DataFrame,
    fecha_inicio: pd.Timestamp,
    fecha_fin: pd.Timestamp,
    regiones: list[str],
    categorias: list[str],
) -> pd.DataFrame:
    """Filtra el DataFrame según los valores seleccionados en el sidebar."""
    mask = (
        (df["fecha"] >= fecha_inicio)
        & (df["fecha"] <= fecha_fin)
    )
    if regiones:
        mask &= df["region"].isin(regiones)
    if categorias:
        mask &= df["categoria"].isin(categorias)
    return df[mask].copy()


def opciones_filtro(df: pd.DataFrame) -> dict:
    """Devuelve los valores únicos disponibles para cada filtro."""
    return {
        "fecha_min": df["fecha"].min(),
        "fecha_max": df["fecha"].max(),
        "regiones": sorted(df["region"].unique().tolist()),
        "categorias": sorted(df["categoria"].unique().tolist()),
    }
