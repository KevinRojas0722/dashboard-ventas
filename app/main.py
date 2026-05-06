"""
Entry point del dashboard. Ejecutar con: streamlit run app/main.py
"""

import streamlit as st
import pandas as pd

from utils import cargar_datos, aplicar_filtros, opciones_filtro
from kpis import resumen_kpis
from graficos import (
    grafico_tendencia,
    grafico_top_productos,
    grafico_ventas_region,
    grafico_ventas_categoria,
)

# ── Configuración de página ───────────────────────────────────────────────────

st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Carga de datos ────────────────────────────────────────────────────────────

df = cargar_datos()
opciones = opciones_filtro(df)

# ── Sidebar — Filtros ─────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Filtros")

    fecha_inicio, fecha_fin = st.date_input(
        "Rango de fechas",
        value=(opciones["fecha_min"].date(), opciones["fecha_max"].date()),
        min_value=opciones["fecha_min"].date(),
        max_value=opciones["fecha_max"].date(),
    )

    regiones = st.multiselect(
        "Región",
        options=opciones["regiones"],
        default=opciones["regiones"],
    )

    categorias = st.multiselect(
        "Categoría",
        options=opciones["categorias"],
        default=opciones["categorias"],
    )

    st.divider()
    st.caption("Dashboard de Ventas · Portafolio BI")

# ── Aplicar filtros ───────────────────────────────────────────────────────────

df_filtrado = aplicar_filtros(
    df,
    pd.Timestamp(fecha_inicio),
    pd.Timestamp(fecha_fin),
    regiones,
    categorias,
)

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────

st.title("📊 Dashboard de Análisis de Ventas")
st.caption(
    f"Mostrando {len(df_filtrado):,} transacciones · "
    f"{fecha_inicio} al {fecha_fin}"
)

# ── KPI Cards ─────────────────────────────────────────────────────────────────

kpis = resumen_kpis(df_filtrado)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Ventas Totales",
    value=f"${kpis['ventas_totales']:,.0f}",
)
col2.metric(
    label="Ticket Promedio",
    value=f"${kpis['ticket_promedio']:,.0f}",
)
col3.metric(
    label="Transacciones",
    value=f"{kpis['transacciones']:,}",
)
col4.metric(
    label="Clientes Únicos",
    value=f"{kpis['clientes_unicos']:,}",
)

st.divider()

# ── Gráficos — fila 1 ─────────────────────────────────────────────────────────

col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.plotly_chart(grafico_tendencia(df_filtrado), use_container_width=True)

with col_der:
    st.plotly_chart(grafico_ventas_region(df_filtrado), use_container_width=True)

# ── Gráficos — fila 2 ─────────────────────────────────────────────────────────

col_izq2, col_der2 = st.columns([1, 1])

with col_izq2:
    st.plotly_chart(grafico_top_productos(df_filtrado), use_container_width=True)

with col_der2:
    st.plotly_chart(grafico_ventas_categoria(df_filtrado), use_container_width=True)

# ── Tabla de datos (colapsable) ───────────────────────────────────────────────

with st.expander("Ver datos en tabla"):
    st.dataframe(
        df_filtrado[["fecha", "producto", "categoria", "cantidad",
                     "precio_unitario", "total", "region", "vendedor", "cliente_id"]]
        .sort_values("fecha", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
