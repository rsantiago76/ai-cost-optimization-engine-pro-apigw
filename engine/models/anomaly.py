from __future__ import annotations
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_cost_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    df = df.copy()
    model = IsolationForest(contamination=contamination, random_state=42)
    df["anomaly"] = model.fit_predict(df[["cost"]])
    return df[df["anomaly"] == -1].copy()
