from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/"data/processed/tower_monthly_clean.csv",parse_dates=["month"])
print(f"Loaded {len(df):,} clean tower-month observations.")
