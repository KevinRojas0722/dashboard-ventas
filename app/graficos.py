"""
Componentes de visualización con Plotly.
Cada función devuelve un go.Figure listo para pasar a st.plotly_chart().
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Paleta consistente en todo el dashboard
COLORES = px.colors.qualitative.Set2
COLOR_PRIMARIO = "#2E86AB"


def grafico_tendencia(df: pd.DataFrame) -> go.Figure:
    """Línea de ventas totales agrupadas por mes."""
    ventas_mes = (
        df.groupby(df["fecha"].dt.to_period("M"))["total"]
        .sum()
        .reset_index()
    )
    ventas_mes["fecha"] = ventas_mes["fecha"].dt.to_timestamp()

    fig = px.line(
        ventas_mes,
        x="fecha",
        y="total",
        title="Tendencia de Ventas Mensuales",
        labels={"fecha": "Mes", "total": "Ventas ($)"},
        color_discrete_sequence=[COLOR_PRIMARIO],
    )
    fig.update_traces(mode="lines+markers", marker_size=5)
    fig.update_layout(
        hovermode="x unified",
        yaxis_tickformat="$,.0f",
        title_font_size=16,
    )
    return fig


def grafico_top_productos(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Barras horizontales con los productos más vendidos por ingresos."""
    top = (
        df.groupby("producto")["total"]
        .sum()
        .nlargest(top_n)
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        top,
        x="total",
        y="producto",
        orientation="h",
        title=f"Top {top_n} Productos por Ingresos",
        labels={"total": "Ventas ($)", "producto": ""},
        color="total",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        xaxis_tickformat="$,.0f",
        coloraxis_showscale=False,
        title_font_size=16,
    )
    return fig


def grafico_ventas_region(df: pd.DataFrame) -> go.Figure:
    """Pie chart de participación de ventas por región."""
    por_region = (
        df.groupby("region")["total"]
        .sum()
        .reset_index()
        .sort_values("total", ascending=False)
    )

    fig = px.pie(
        por_region,
        values="total",
        names="region",
        title="Ventas por Región",
        color_discrete_sequence=COLORES,
        hole=0.35,  # donut chart, más moderno que pie sólido
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        title_font_size=16,
        showlegend=True,
        legend=dict(orientation="v", x=1, y=0.5),
    )
    return fig


def grafico_ventas_categoria(df: pd.DataFrame) -> go.Figure:
    """Barras agrupadas de ventas por categoría y mes."""
    ventas = (
        df.groupby([df["fecha"].dt.to_period("M"), "categoria"])["total"]
        .sum()
        .reset_index()
    )
    ventas["fecha"] = ventas["fecha"].dt.to_timestamp()

    fig = px.bar(
        ventas,
        x="fecha",
        y="total",
        color="categoria",
        title="Ventas Mensuales por Categoría",
        labels={"fecha": "Mes", "total": "Ventas ($)", "categoria": "Categoría"},
        color_discrete_sequence=COLORES,
    )
    fig.update_layout(
        yaxis_tickformat="$,.0f",
        hovermode="x unified",
        title_font_size=16,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
