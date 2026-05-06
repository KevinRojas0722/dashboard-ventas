# Dashboard de Análisis de Ventas

Dashboard interactivo de ventas construido con Python y Streamlit, orientado a demostrar capacidades de análisis de datos y visualización BI.

## Stack

- **Python 3.11**
- **Streamlit** — interfaz del dashboard
- **Pandas** — análisis y transformación de datos
- **Plotly** — gráficos interactivos
- **Faker + NumPy** — generación de datos sintéticos realistas

## Características

- KPIs principales: ventas totales, ticket promedio, transacciones, clientes únicos
- Tendencia de ventas en el tiempo
- Top productos más vendidos
- Ventas por región/sucursal
- Análisis por categoría de producto
- Filtros interactivos: rango de fechas, región, categoría

## Cómo correrlo

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/Scripts/activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar datos de muestra
python data/generar_datos.py

# 4. Correr el dashboard
streamlit run app/main.py
```

## Estructura del proyecto

```
dashboard-ventas/
├── data/
│   ├── ventas.csv          # Dataset generado (~5000 registros)
│   └── generar_datos.py    # Script para regenerar el dataset
├── app/
│   ├── main.py             # Entry point de Streamlit
│   ├── kpis.py             # Cálculo de KPIs
│   ├── graficos.py         # Componentes de gráficos
│   └── utils.py            # Funciones auxiliares
├── notebooks/
│   └── exploracion.ipynb   # Análisis exploratorio
├── requirements.txt
└── README.md
```
