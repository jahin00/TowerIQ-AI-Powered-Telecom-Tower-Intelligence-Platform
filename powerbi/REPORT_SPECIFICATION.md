# TowerIQ Power BI Report Specification

## Relationships
- DimRegion[region_key] 1:* DimTower[region_id]
- DimTower[tower_key] 1:* FactTowerMonthly[tower_id]
- DimDate[date_key] 1:* FactTowerMonthly[date_key]
- DimDate[date_key] 1:* FactNetworkForecast[month]
- DimTower[tower_key] 1:* FactTowerForecast[tower_id]

Use single-direction filtering from dimensions to facts.

## Page 1: Executive Overview
KPI cards: Total Revenue, Revenue MoM %, Tenancy Rate, At Risk Towers, Critical Towers.
Charts: Monthly Revenue, Revenue by Region, Tenancy by Region, Downtime by Region, Risk Band Distribution.
Slicers: Year, Region, Tower Type.

## Page 2: Regional Intelligence
Revenue trend, Revenue per Tenant, Tenancy Rate, Downtime, Incidents, Tower Count and region-filtered tower table.

## Page 3: Tower Risk
Tower ID, Region, Revenue, MoM %, Tenancy, Downtime, Incidents, Risk Score and Risk Band.
Use drill-through to a tower detail page.

## Page 4: Forecast & Revenue-at-Risk
Actual vs forecast revenue, forecast change, forecast model and revenue-at-risk tower table.

## Page 5: Data Quality
Raw rows, clean rows, quality-flagged rows, missing/invalid counts and validation notes.
