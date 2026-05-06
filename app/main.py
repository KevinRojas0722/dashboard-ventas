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
    page_title="Sales Dashboard | Costa Rica",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS global ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }

.stApp { background-color: #0F172A; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0D1B2A !important;
    border-right: 1px solid #1E3A5F;
}
/* Texto base del sidebar */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div { color: #94A3B8; }
section[data-testid="stSidebar"] hr { border-color: #1E3A5F !important; opacity: 1 !important; }

/* Inputs y selects del sidebar */
section[data-testid="stSidebar"] [data-baseweb="input"],
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background-color: #1E293B !important;
    border-color: #334155 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-baseweb="input"] input {
    color: #E2E8F0 !important;
}
/* Tags del multiselect */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #1E3A5F !important;
    border-radius: 4px !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span { color: #93C5FD !important; }
section[data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] { color: #64748B !important; }

/* Sidebar brand header */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 0 20px 0;
    border-bottom: 1px solid #1E3A5F;
    margin-bottom: 24px;
}
.sb-brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #1D4ED8, #00C9A7);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.sb-brand-text { line-height: 1.2; }
.sb-brand-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: #F1F5F9 !important;
    display: block;
}
.sb-brand-sub {
    font-size: 0.7rem;
    color: #475569 !important;
}

/* Etiqueta de sección de filtro */
.filter-label {
    display: flex;
    align-items: center;
    gap: 7px;
    margin-bottom: 6px;
    margin-top: 16px;
}
.filter-label-icon {
    width: 22px; height: 22px;
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 5px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
}
.filter-label-text {
    font-size: 0.72rem;
    font-weight: 600;
    color: #64748B !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* Tarjeta de resumen al fondo del sidebar */
.sb-summary {
    background: #1E293B;
    border: 1px solid #1E3A5F;
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 20px;
}
.sb-summary-title {
    font-size: 0.68rem;
    font-weight: 600;
    color: #475569 !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 12px;
}
.sb-summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid #1E3A5F;
}
.sb-summary-row:last-child { border-bottom: none; }
.sb-summary-key { font-size: 0.75rem; color: #64748B !important; }
.sb-summary-val { font-size: 0.78rem; font-weight: 600; color: #93C5FD !important; }

/* ── Contenido principal ── */
.block-container { padding: 1.5rem 2rem 2rem 2rem; background-color: #0F172A; }

/* Header */
.dash-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 20px;
}
.dash-header-left h1 {
    margin: 0 0 2px 0;
    font-size: 1.5rem;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: -0.3px;
}
.dash-header-left p { margin: 0; font-size: 0.8rem; color: #64748B; }
.dash-header-badge {
    background: #4F8EF720;
    border: 1px solid #4F8EF750;
    color: #4F8EF7;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 600;
}

/* KPI Cards */
.kpi-card {
    background: #1E293B;
    border: 1px solid #1E3A5F;
    border-radius: 10px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
}
.kpi-icon { font-size: 1.2rem; margin-bottom: 10px; display: block; }
.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #F1F5F9;
    line-height: 1;
    letter-spacing: -0.5px;
}

/* Ocultar footer de Streamlit */
footer { visibility: hidden; }

/* Contenedor de gráficos */
.chart-wrapper {
    background: #1E293B;
    border: 1px solid #1E3A5F;
    border-radius: 10px;
    padding: 4px;
    margin-bottom: 14px;
}
</style>
""", unsafe_allow_html=True)

# ── Carga de datos ────────────────────────────────────────────────────────────

df = cargar_datos()
opciones = opciones_filtro(df)

# ── Sidebar — Filtros ─────────────────────────────────────────────────────────

with st.sidebar:

    # Brand header
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-icon">📊</div>
        <div class="sb-brand-text">
            <span class="sb-brand-name">SalesDash CR</span>
            <span class="sb-brand-sub">Análisis de Ventas 2024–2025</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filtro: rango de fechas
    st.markdown("""
    <div class="filter-label">
        <span class="filter-label-icon">📅</span>
        <span class="filter-label-text">Período</span>
    </div>
    """, unsafe_allow_html=True)
    rango = st.date_input(
        "Período",
        value=(opciones["fecha_min"].date(), opciones["fecha_max"].date()),
        min_value=opciones["fecha_min"].date(),
        max_value=opciones["fecha_max"].date(),
        label_visibility="collapsed",
    )
    if isinstance(rango, (list, tuple)) and len(rango) == 2:
        fecha_inicio, fecha_fin = pd.Timestamp(rango[0]), pd.Timestamp(rango[1])
    else:
        fecha_inicio = fecha_fin = pd.Timestamp(rango[0] if isinstance(rango, (list, tuple)) else rango)

    # Filtro: provincia
    st.markdown("""
    <div class="filter-label">
        <span class="filter-label-icon">📍</span>
        <span class="filter-label-text">Provincia</span>
    </div>
    """, unsafe_allow_html=True)
    regiones = st.multiselect(
        "Provincia",
        options=opciones["regiones"],
        default=opciones["regiones"],
        label_visibility="collapsed",
        placeholder="Seleccionar provincias...",
    )

    # Filtro: categoría
    st.markdown("""
    <div class="filter-label">
        <span class="filter-label-icon">🏷️</span>
        <span class="filter-label-text">Categoría</span>
    </div>
    """, unsafe_allow_html=True)
    categorias = st.multiselect(
        "Categoría",
        options=opciones["categorias"],
        default=opciones["categorias"],
        label_visibility="collapsed",
        placeholder="Seleccionar categorías...",
    )

# ── Filtros ───────────────────────────────────────────────────────────────────

df_filtrado = aplicar_filtros(df, fecha_inicio, fecha_fin, regiones, categorias)

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

# Tarjeta de resumen en el sidebar (necesita df_filtrado, va en bloque separado)
with st.sidebar:
    kpis_sb = resumen_kpis(df_filtrado)
    st.markdown(f"""
    <div class="sb-summary">
        <div class="sb-summary-title">Resumen actual</div>
        <div class="sb-summary-row">
            <span class="sb-summary-key">Transacciones</span>
            <span class="sb-summary-val">{kpis_sb['transacciones']:,}</span>
        </div>
        <div class="sb-summary-row">
            <span class="sb-summary-key">Ventas totales</span>
            <span class="sb-summary-val">₡{kpis_sb['ventas_totales']:,.0f}</span>
        </div>
        <div class="sb-summary-row">
            <span class="sb-summary-key">Clientes únicos</span>
            <span class="sb-summary-val">{kpis_sb['clientes_unicos']:,}</span>
        </div>
        <div class="sb-summary-row">
            <span class="sb-summary-key">Provincias</span>
            <span class="sb-summary-val">{len(regiones)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="dash-header">
    <div class="dash-header-left">
        <h1>📊 Dashboard de Ventas</h1>
        <p>Costa Rica &nbsp;·&nbsp; {fecha_inicio.strftime('%d %b %Y')} — {fecha_fin.strftime('%d %b %Y')}</p>
    </div>
    <div class="dash-header-badge">{len(df_filtrado):,} transacciones</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────

kpis = resumen_kpis(df_filtrado)

KPIS = [
    ("💰", "Ventas Totales",  f"₡{kpis['ventas_totales']:,.0f}",  "#4F8EF7"),
    ("🎯", "Ticket Promedio", f"₡{kpis['ticket_promedio']:,.0f}", "#00C9A7"),
    ("📦", "Transacciones",   f"{kpis['transacciones']:,}",        "#F59E0B"),
    ("👥", "Clientes Únicos", f"{kpis['clientes_unicos']:,}",      "#F472B6"),
]

cols = st.columns(4)
for col, (icon, label, value, color) in zip(cols, KPIS):
    col.markdown(f"""
    <div class="kpi-card" style="--accent: {color}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Gráficos fila 1 ───────────────────────────────────────────────────────────

c1, c2 = st.columns([3, 2])
with c1:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.plotly_chart(grafico_tendencia(df_filtrado), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.plotly_chart(grafico_ventas_region(df_filtrado), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Gráficos fila 2 ───────────────────────────────────────────────────────────

c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.plotly_chart(grafico_top_productos(df_filtrado), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.plotly_chart(grafico_ventas_categoria(df_filtrado), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Tabla ─────────────────────────────────────────────────────────────────────

with st.expander("Ver detalle de transacciones"):
    st.dataframe(
        df_filtrado[["fecha", "producto", "categoria", "cantidad",
                     "precio_unitario", "total", "region", "vendedor", "cliente_id"]]
        .sort_values("fecha", ascending=False)
        .rename(columns={
            "fecha": "Fecha", "producto": "Producto", "categoria": "Categoría",
            "cantidad": "Cantidad", "precio_unitario": "Precio Unit.",
            "total": "Total", "region": "Provincia",
            "vendedor": "Vendedor", "cliente_id": "Cliente",
        }),
        use_container_width=True,
        hide_index=True,
    )
