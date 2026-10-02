# TowerIQ Phase 3: Exploratory Data Analysis & Statistical Intelligence

## Dataset
The clean analytical layer contains 12,000 tower-month records covering
500 towers and 24 months.

## Executive observations

### Revenue
- Total observed revenue: 1,816,204,792
- Highest-total-revenue region: **Dhaka**
- Lowest-total-revenue region: **Rangpur**
- Mean monthly network revenue: 75,675,200

### Tenancy and operations
- Average tenancy rate: 72.87%
- Median tenancy rate: 75.00%
- Average downtime: 3.63 hours/tower-month
- Median downtime: 3.48 hours/tower-month

## Correlation analysis

Spearman correlations from the current synthetic dataset:
- Revenue vs tenancy rate: 0.329
- Revenue vs downtime: -0.010
- Revenue vs incidents: -0.023
- Revenue vs operating cost: -0.013
- Revenue vs active tenants: 0.910

**Interpretation rule:** correlation describes association in this synthetic dataset.
It does not establish that one operational factor caused a revenue change.

## Anomaly detection

Isolation Forest was applied at the tower-month level using revenue, tenancy,
downtime, incidents, operating cost, and revenue-per-tenant features.

- Anomalous tower-month rows flagged: 360
- Normal tower-month rows: 11,640

The anomaly detector is a screening mechanism. Analysts should investigate the
underlying records rather than treating the model flag as proof of an operational problem.

## Declining-asset screening

The current risk score is intentionally transparent and project-defined. It combines:
- revenue decline
- tenant decline
- downtime relative to each tower's median
- latest-month anomaly status

Current screening counts:
- Healthy: 383
- Watch: 110
- At Risk: 6
- Critical: 1

### Highest-risk examples
tower_id region_name  revenue_change_pct  tenant_change  downtime_hours  risk_score risk_band
   T0148    Rajshahi              -30.86           -1.0             7.2        80.3  Critical

## Next analytical step

The next phase should move from descriptive/statistical screening to **forecasting and
validated predictive modeling**. We will compare simple baselines with ARIMA/Exponential
Smoothing and a tree-based model, then expose the results in Power BI.

> Important: all thresholds and scoring rules in this portfolio project are explicit
> analytical assumptions, not claims about telecom industry standards.
