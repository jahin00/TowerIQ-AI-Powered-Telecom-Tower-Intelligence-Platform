# TowerIQ: AI-Powered Telecom Tower Intelligence Platform

**TowerIQ** is an end-to-end telecom analytics and decision-support portfolio project that turns messy tower-level operational data into **quality-controlled KPIs, anomaly and risk signals, revenue forecasts, and evidence-backed natural-language investigations**.

The project is designed to demonstrate a practical data analyst / analytics engineer workflow rather than a standalone machine-learning model.

> **Core idea:** Data quality → SQL analytics → statistical analysis → anomaly detection → operational risk → forecasting → BI → LLM-assisted investigation.

## 🚀 What TowerIQ Does

- Cleans and validates tower-month operational data with SQL
- Preserves flagged records in a data-quality audit layer instead of silently deleting them
- Produces network, regional, and tower-level KPIs
- Detects anomalous tower-month observations using Isolation Forest
- Calculates a project-defined tower risk score for screening
- Forecasts network and selected tower revenue
- Screens towers for potential revenue-at-risk
- Provides a Power BI-ready star schema and DAX measures
- Provides a Streamlit investigation console
- Uses an evidence-first LLM workflow for natural-language explanations
- Applies read-only SQL guardrails to the investigation engine

## 🧩 Architecture

```text
                 RAW TELECOM DATA
                        │
                        ▼
              SQL DATA QUALITY LAYER
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
   CLEAN ANALYTICAL DATA       QUALITY AUDIT DATA
          │
          ▼
 ┌───────────────────────────────┐
 │ EDA + Statistics              │
 │ Correlation + Anomaly Screen  │
 │ Tower Risk Scoring            │
 └───────────────┬───────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
  FORECASTING          POWER BI MODEL
        │                 │
        └────────┬────────┘
                 ▼
       TOWERIQ INVESTIGATION ENGINE
                 │
        Evidence Extraction
                 │
        Optional LLM Reasoning
                 │
                 ▼
          STREAMLIT APP
```

## 📊 Main Modules

### 1. SQL Data Quality

The pipeline separates raw, flagged, and clean analytical records.

- Missing / invalid value checks
- Duplicate detection
- Range validation
- Quality flags
- Clean analytical view
- Auditability of rejected records

### 2. EDA & Operational Analytics

- Descriptive statistics
- Regional revenue comparison
- Monthly network trends
- Tenancy / revenue relationships
- Downtime / revenue relationships
- Tower-level anomaly screening

### 3. Risk Intelligence

Isolation Forest is used to screen unusual tower-month observations. A project-defined risk score combines selected operational indicators such as revenue movement, tenancy movement, downtime, and anomaly status.

**Important:** the risk score is a portfolio-project screening mechanism, not an industry-standard risk rating.

### 4. Revenue Forecasting

Models include:

- Naive last-value baseline
- 3-month moving average
- Holt exponential smoothing
- ARIMA

A time-based holdout is used rather than random train/test splitting to respect the temporal structure of the data.

### 5. Power BI

The project provides a Power BI-ready semantic model with:

- `DimRegion`
- `DimTower`
- `DimDate`
- `FactTowerMonthly`
- `FactNetworkForecast`
- `FactTowerForecast`

Suggested report pages cover executive overview, regional intelligence, tower risk, forecasting, and data quality.

### 6. LLM-Assisted Investigation

TowerIQ does **not** ask an LLM to invent an explanation from raw data.

Instead:

```text
Question
   ↓
Evidence extraction
   ↓
Controlled read-only SQL
   ↓
Structured metrics
   ↓
LLM reasoning
   ↓
Evidence-backed explanation
```

For example:

> "Why did tower T0148 decline?"

The system can retrieve revenue change, tenancy movement, downtime, and other relevant evidence before generating an explanation. It explicitly distinguishes **observed association from proven causation**.

## 🖥️ Streamlit Application

Run the included `app.py` to open the interactive TowerIQ console.

The app includes:

- Executive Overview
- Network performance
- Tower Explorer
- Revenue Forecast Center
- Revenue-at-Risk screen
- Ask TowerIQ investigation interface
- Data Quality monitoring
- Interactive Plotly visualizations
- Evidence-only fallback when no LLM API key is configured

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/TowerIQ.git
cd TowerIQ
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the application

```bash
streamlit run app.py
```

The browser should open the local Streamlit application automatically.

## 🤖 Optional LLM Configuration

TowerIQ works without an LLM API key. In that mode, the application returns evidence-based investigation summaries without external model reasoning.

For LLM-assisted responses, create a local `.env` file from `.env.example` and configure the API credentials appropriate to your provider.

**Never commit API keys to GitHub.**

## 📁 Repository Structure

```text
TowerIQ/
├── app.py                         # Streamlit application
├── requirements.txt               # Runtime dependencies
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
│
├── app/
│   ├── toweriq_engine.py          # Read-only investigation engine
│   ├── llm_client.py              # Optional LLM client
│   ├── report_generator.py
│   └── app.py                     # Original modular app
│
├── database/
│   ├── toweriq.db
│   ├── phase1_inspection.sql
│   └── phase2_cleaning.sql
│
├── data/
│   ├── raw/
│   └── processed/
│
├── analysis/
│   ├── descriptive_statistics.csv
│   ├── regional_performance.csv
│   ├── correlation_analysis.csv
│   ├── row_level_anomalies.csv
│   ├── tower_anomaly_summary.csv
│   └── tower_risk_latest.csv
│
├── forecasting/
│   ├── network_model_comparison.csv
│   ├── network_future_forecast.csv
│   ├── tower_future_forecasts.csv
│   └── revenue_at_risk_screen.csv
│
├── powerbi/
│   ├── data/
│   ├── TowerIQ_Measures.dax
│   ├── BUILD_ORDER.md
│   └── REPORT_SPECIFICATION.md
│
├── prompts/
├── reports/
├── figures/
├── docs/
└── tests/
```

## 🔬 Dataset

The repository uses a **synthetic telecom tower operations dataset** created for portfolio and demonstration purposes. It contains tower, regional, monthly revenue, tenancy, downtime, incident, cost, and related operational fields.

The project should therefore be interpreted as a demonstration of analytical methodology and engineering workflow, not as an analysis of a real telecom operator.

## ⚠️ Analytical Notes

- Correlation does not establish causation.
- Anomaly detection identifies unusual observations for investigation; it does not prove an operational fault.
- Forecasts are estimates and depend on historical patterns and model assumptions.
- Revenue-at-risk thresholds are project assumptions.
- The risk score is project-defined and should not be interpreted as a production telecom risk standard.

## 🎯 Portfolio Skills Demonstrated

**Data & Analytics:** Python, Pandas, SQL, statistics, EDA, anomaly detection, forecasting

**BI:** Power BI, DAX, KPI design, dimensional modelling, interactive dashboards

**Engineering:** SQLite, data-quality pipelines, validation, testing, read-only SQL controls

**AI:** LLM-assisted analytics, evidence extraction, prompt guardrails, uncertainty-aware explanations

**Application:** Streamlit, Plotly, modular Python architecture

## 🧪 Validation

The project includes automated tests for the investigation engine. Python modules can also be syntax-checked with:

```bash
python -m py_compile app.py
```

## 📌 Suggested Demo Flow

1. Open Executive Overview
2. Show network revenue and regional performance
3. Open Tower Explorer and select a declining tower
4. Show tenancy and downtime alongside revenue
5. Open Forecast Center
6. Demonstrate revenue-at-risk screening
7. Ask TowerIQ why a tower declined
8. Show the evidence packet before the generated explanation
9. Explain the distinction between evidence and causality

## 👤 Author

**Jahin Ahnaf Tasin**  
MSc in Data Science and Analytics | BSc in Electrical & Electronic Engineering

This project was developed as a portfolio demonstration of applied data analytics, BI, forecasting, and AI-assisted decision support.
