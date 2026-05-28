# Dashboard de Análisis de Ventas — Costa Rica

Interactive BI sales dashboard built with Python and Streamlit, focused on portfolio Data Analyst / BI Junior positions.

## Features

| Section | Description |
|---|---|
| KPIs | Total sales, average ticket, transactions and unique clients |
| Trend | Monthly sales with degraded area and peak month |
| By province | Horizontal bars with % of participation per province in CR |
| Top products | Top 10 products by revenue with color gradient |
| By category | Stacked bars per product category |
| Filters | Sidebar with date range, province and category; real-time refresh |
| Table | Collapsible table of transactions |

## Tech stack

| Tool | Use |
|---|---|
| Python 3.11 | Base language |
| Streamlit 1.57 | Dashboard framework |
| Pandas 3.0 | Data analysis and transformation |
| Plotly 6.7 | Interactive charts |
| Faker + NumPy | Realistic synthetic data generation |

## How to run it locally

```bash
# 1. Clone the repository
git clone https://github.com/KevinRojas0722/dashboard-ventas.git
cd dashboard-ventas

# 2. Create and activate the virtual environment
python -m venv venv
source venv/Scripts/activate     # Windows
source venv/bin/activate         # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the sales dataset
python data/generar_datos.py

# 5. Run the app
streamlit run app/main.py
```

Open `http://localhost:8501` in your browser.

## Project structure

```
dashboard-ventas/
├── .streamlit/
│   └── config.toml              # Dark theme and server configuration
├── app/
│   ├── main.py                  # Entry point — layout and KPIs
│   ├── api.py                   # Aggregations and metrics calculation
│   ├── charts.py                # Visualization components (Plotly)
│   └── utils.py                 # Data loading and filters
├── data/
│   ├── generar_datos.py         # Generates realistic sales data with Faker
│   └── ventas.csv               # Generated dataset (~5,000 transactions, 2024–2025)
├── notebooks/
│   └── exploracion.ipynb        # Exploratory analysis and key findings
├── requirements.txt
└── README.md
```

## Dataset

The synthetic but realistic dataset, generated with `data/generar_datos.py`:

- **5,000 transactions** between January 2024 and December 2025
- **7 provinces** of Costa Rica with commercial activity-based distribution
- **23 products in 4 categories** (Electronics, Office, Software, Accessories)
- **~400 unique clients** with variable purchase frequency
- **Seasonality incorporated** with peaks in November–December and sales

## Author

Kevin Rojas Hernández — [GitHub](https://github.com/KevinRojas0722) · [LinkedIn](https://www.linkedin.com/in/kevin-rojas-hernandez-dev)
