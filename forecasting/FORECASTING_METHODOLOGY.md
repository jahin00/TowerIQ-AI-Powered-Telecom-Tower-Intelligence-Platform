# TowerIQ Phase 4: Forecasting

## Validation
The final 4 historical months are held out as a future-like test period. No random shuffling is used.

## Models
- Naive last-value baseline
- 3-month moving-average baseline
- Holt linear trend (non-seasonal) for the limited 24-month dataset
- Seasonal ARIMA(1,1,1) × (1,0,1,12) where supported by the training window

## Network model selection
Best model by holdout RMSE: **ARIMA**.

## Tower-level forecast
Ten high-revenue towers are evaluated separately using the same time-based holdout. Each tower selects its model by lowest RMSE.

## Revenue-at-risk screen
- High: next-month forecast decline <= 10%
- Watch: next-month forecast decline > 5% and < 10%
- Stable / Growing: forecast decline < 5%

These thresholds are project-defined analytical assumptions, not telecom-industry standards.
Forecasts are estimates and should trigger investigation rather than be treated as certainties.
