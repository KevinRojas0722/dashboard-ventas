# 📊 Dashboard de Análisis de Ventas — Costa Rica

Dashboard interactivo de ventas estilo BI construido con Python y Streamlit, orientado a portafolio para puestos de **Analista de Datos / BI Junior**.

---

## Funcionalidades

| Sección | Descripción |
|---------|-------------|
| **KPIs** | Ventas totales, ticket promedio, transacciones y clientes únicos |
| **Tendencia** | Ventas mensuales con área degradada y marca del mes pico |
| **Por provincia** | Barras horizontales con % de participación por provincia de CR |
| **Top productos** | Los 10 productos con mayor ingreso con gradiente de color |
| **Por categoría** | Barras apiladas mensuales por categoría de producto |
| **Filtros** | Sidebar con rango de fechas, provincia y categoría; resumen en tiempo real |
| **Tabla** | Detalle de transacciones colapsable |

---

## Stack tecnológico

| Herramienta | Uso |
|------------|-----|
| **Python 3.11** | Lenguaje base |
| **Streamlit 1.57** | Framework del dashboard |
| **Pandas 3.0** | Análisis y transformación de datos |
| **Plotly 6.7** | Gráficos interactivos |
| **Faker + NumPy** | Generación de datos sintéticos realistas |

---

## Cómo ejecutarlo localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/KevinRojas0722/dashboard-ventas.git
cd dashboard-ventas

# 2. Crear y activar el entorno virtual
python -m venv venv
source venv/Scripts/activate   # Windows
# source venv/bin/activate     # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Generar el dataset de ventas
python data/generar_datos.py

# 5. Ejecutar el dashboard
streamlit run app/main.py
```

Abre [http://localhost:8501](http://localhost:8501) en tu navegador.

---

## Estructura del proyecto

```
dashboard-ventas/
├── .streamlit/
│   └── config.toml         # Tema oscuro y configuración del servidor
├── app/
│   ├── main.py             # Entry point — layout y lógica de UI
│   ├── kpis.py             # Cálculo de KPIs principales
│   ├── graficos.py         # Componentes de visualización (Plotly)
│   └── utils.py            # Carga de datos con caché y filtros
├── data/
│   ├── generar_datos.py    # Genera ventas.csv con datos sintéticos realistas
│   └── ventas.csv          # Dataset generado (~5,000 transacciones, 2024–2025)
├── notebooks/
│   └── exploracion.ipynb   # Análisis exploratorio con hallazgos clave
├── requirements.txt
└── README.md
```

---

## Dataset

El dataset es sintético pero realista, generado con `data/generar_datos.py`:

- **5,000 transacciones** entre enero 2024 y diciembre 2025
- **7 provincias** de Costa Rica con distribución proporcional a actividad comercial
- **23 productos** en 4 categorías (Electrónica, Oficina, Software, Accesorios)
- **~800 clientes únicos** con frecuencia de compra variable
- Estacionalidad incorporada: picos en noviembre–diciembre y enero

---

## Autor

**Kevin Rojas Hernández** — [GitHub](https://github.com/KevinRojas0722) · [LinkedIn](https://www.linkedin.com/in/kevin-rojas-hernandez-dev)
