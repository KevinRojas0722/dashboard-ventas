"""
Componentes de visualización con Plotly.
Cada función devuelve un go.Figure listo para pasar a st.plotly_chart().
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLOR_PRIMARIO  = "#4F8EF7"   # azul eléctrico
COLOR_ACENTO    = "#00C9A7"   # teal
COLOR_TEXTO     = "#E2E8F0"   # gris claro para labels en fondo oscuro
FONDO_GRAFICO   = "#1E293B"   # azul oscuro para el area del gráfico
FONDO_PAPEL     = "#1E293B"

PALETA = ["#4F8EF7", "#00C9A7", "#F59E0B", "#F472B6", "#A78BFA", "#34D399", "#FB923C"]


def _layout_base(titulo: str, alto: int = 340) -> dict:
    return dict(
        title=dict(text=titulo, font=dict(size=14, color="#94A3B8"), x=0),
        paper_bgcolor=FONDO_PAPEL,
        plot_bgcolor=FONDO_GRAFICO,
        font=dict(family="Segoe UI, sans-serif", color="#94A3B8", size=11),
        margin=dict(l=12, r=12, t=44, b=12),
        height=alto,
    )


def _ejes_oscuros(fig: go.Figure) -> go.Figure:
    fig.update_xaxes(
        showgrid=False,
        linecolor="#334155",
        tickcolor="#334155",
        tickfont=dict(color="#64748B", size=10),
    )
    fig.update_yaxes(
        gridcolor="#334155",
        linecolor="#334155",
        tickfont=dict(color="#64748B", size=10),
        zeroline=False,
    )
    return fig


def grafico_tendencia(df: pd.DataFrame) -> go.Figure:
    """Área con gradiente de ventas mensuales. Marca el mes pico."""
    ventas_mes = (
        df.groupby(df["fecha"].dt.to_period("M"))["total"]
        .sum()
        .reset_index()
    )
    ventas_mes["fecha"] = ventas_mes["fecha"].dt.to_timestamp()

    idx_pico = ventas_mes["total"].idxmax()

    fig = go.Figure()

    # Área de relleno degradado
    fig.add_trace(go.Scatter(
        x=ventas_mes["fecha"],
        y=ventas_mes["total"],
        fill="tozeroy",
        fillgradient=dict(
            type="vertical",
            colorscale=[[0, "rgba(0,201,167,0.0)"], [1, "rgba(79,142,247,0.35)"]],
        ),
        line=dict(color=COLOR_PRIMARIO, width=2),
        mode="lines",
        name="Ventas",
        hovertemplate="<b>%{x|%b %Y}</b><br>₡%{y:,.0f}<extra></extra>",
    ))

    # Punto y etiqueta del mes pico
    fig.add_trace(go.Scatter(
        x=[ventas_mes.loc[idx_pico, "fecha"]],
        y=[ventas_mes.loc[idx_pico, "total"]],
        mode="markers+text",
        marker=dict(size=10, color=COLOR_ACENTO, symbol="circle"),
        text=[f"₡{ventas_mes.loc[idx_pico, 'total']:,.0f}"],
        textposition="top center",
        textfont=dict(color=COLOR_ACENTO, size=10),
        showlegend=False,
        hoverinfo="skip",
    ))

    fig.update_layout(
        yaxis_tickformat="₡,.0f",
        hovermode="x unified",
        showlegend=False,
        **_layout_base("Tendencia de Ventas Mensuales"),
    )
    return _ejes_oscuros(fig)


def grafico_top_productos(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Barras horizontales con gradiente de color por valor."""
    top = (
        df.groupby("producto")["total"]
        .sum()
        .nlargest(top_n)
        .sort_values()
        .reset_index()
    )

    fig = go.Figure(go.Bar(
        x=top["total"],
        y=top["producto"],
        orientation="h",
        marker=dict(
            color=top["total"],
            colorscale=[[0, "#1E3A5F"], [0.5, COLOR_PRIMARIO], [1, COLOR_ACENTO]],
            showscale=False,
            line=dict(width=0),
        ),
        hovertemplate="<b>%{y}</b><br>₡%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        xaxis_tickformat="₡,.0f",
        **_layout_base(f"Top {top_n} Productos por Ingresos"),
    )
    return _ejes_oscuros(fig)


def grafico_ventas_region(df: pd.DataFrame) -> go.Figure:
    """Barras horizontales por provincia con porcentaje de participación."""
    por_region = (
        df.groupby("region")["total"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )
    total_global = por_region["total"].sum()
    por_region["pct"] = (por_region["total"] / total_global * 100).round(1)

    fig = go.Figure()

    # Barra de fondo (100%) como referencia visual
    fig.add_trace(go.Bar(
        x=[total_global] * len(por_region),
        y=por_region["region"],
        orientation="h",
        marker=dict(color="#1E3A5F", line=dict(width=0)),
        showlegend=False,
        hoverinfo="skip",
    ))

    # Barra real con valor
    fig.add_trace(go.Bar(
        x=por_region["total"],
        y=por_region["region"],
        orientation="h",
        marker=dict(
            color=PALETA[:len(por_region)],
            line=dict(width=0),
        ),
        text=[f"{p}%" for p in por_region["pct"]],
        textposition="outside",
        textfont=dict(color="#94A3B8", size=10),
        hovertemplate="<b>%{y}</b><br>₡%{x:,.0f} (%{text})<extra></extra>",
        showlegend=False,
    ))

    fig.update_layout(
        barmode="overlay",
        xaxis_tickformat="₡,.0f",
        **_layout_base("Ventas por Provincia"),
    )
    return _ejes_oscuros(fig)


def grafico_ventas_categoria(df: pd.DataFrame) -> go.Figure:
    """Barras apiladas por categoría y mes."""
    ventas = (
        df.groupby([df["fecha"].dt.to_period("M"), "categoria"])["total"]
        .sum()
        .reset_index()
    )
    ventas["fecha"] = ventas["fecha"].dt.to_timestamp()

    fig = go.Figure()
    for i, cat in enumerate(sorted(ventas["categoria"].unique())):
        subset = ventas[ventas["categoria"] == cat]
        fig.add_trace(go.Bar(
            x=subset["fecha"],
            y=subset["total"],
            name=cat,
            marker=dict(color=PALETA[i % len(PALETA)], line=dict(width=0)),
            hovertemplate=f"<b>{cat}</b><br>%{{x|%b %Y}}<br>₡%{{y:,.0f}}<extra></extra>",
        ))

    fig.update_layout(
        barmode="stack",
        yaxis_tickformat="₡,.0f",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(size=10, color="#94A3B8"),
            bgcolor="rgba(0,0,0,0)",
        ),
        **_layout_base("Ventas por Categoría y Mes"),
    )
    return _ejes_oscuros(fig)
