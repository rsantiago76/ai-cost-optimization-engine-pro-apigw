from __future__ import annotations
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def forecast_daily_cost_arima(df: pd.DataFrame, horizon_days: int = 30) -> dict:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    y = df["cost"].astype(float).values
    if len(y) < 45:
        return _fallback_forecast(df, horizon_days)

    model = ARIMA(y, order=(1, 1, 1))
    fitted = model.fit()

    forecast = fitted.forecast(steps=horizon_days)
    forecast = np.maximum(0, forecast)

    last_date = df["date"].iloc[-1].date()
    out = []
    for i, v in enumerate(forecast, start=1):
        out.append({"date": (last_date + pd.Timedelta(days=i)).date().isoformat(), "yhat": float(v)})

    return {
        "model": "ARIMA(1,1,1)",
        "daily_forecast": out,
        "total_forecast": float(np.sum(forecast)),
    }

def _fallback_forecast(df: pd.DataFrame, horizon_days: int) -> dict:
    last7 = df["cost"].astype(float).tail(7)
    avg = float(last7.mean()) if len(last7) else float(df["cost"].astype(float).mean())
    last_date = pd.to_datetime(df["date"]).max().date()
    out = [{"date": (last_date + pd.Timedelta(days=i)).date().isoformat(), "yhat": avg} for i in range(1, horizon_days + 1)]
    return {"model": "NaiveRollingAvg7", "daily_forecast": out, "total_forecast": float(avg * horizon_days)}
