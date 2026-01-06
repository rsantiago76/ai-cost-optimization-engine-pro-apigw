from __future__ import annotations
import pandas as pd

def prepare_daily_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    df["dayofweek"] = df["date"].dt.dayofweek
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month

    df["rolling_7"] = df["cost"].rolling(7).mean()
    df["rolling_30"] = df["cost"].rolling(30).mean()
    return df.dropna().reset_index(drop=True)
