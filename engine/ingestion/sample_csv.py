from __future__ import annotations
import pandas as pd
from pathlib import Path

def load_sample_daily_costs(csv_path: str | Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)
