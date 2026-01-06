from __future__ import annotations
import boto3
import pandas as pd
from datetime import datetime, timedelta

def fetch_cost_data(days: int = 90) -> pd.DataFrame:
    client = boto3.client("ce")
    end = datetime.utcnow().date()
    start = end - timedelta(days=days)

    resp = client.get_cost_and_usage(
        TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
    )

    records: list[dict[str, object]] = []
    for r in resp["ResultsByTime"]:
        records.append({
            "date": r["TimePeriod"]["Start"],
            "cost": float(r["Total"]["UnblendedCost"]["Amount"]),
        })

    return pd.DataFrame(records)
