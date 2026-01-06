from __future__ import annotations
import argparse
import json
from pathlib import Path

import pandas as pd

from engine.ingestion.aws_cost_explorer import fetch_cost_data
from engine.ingestion.sample_csv import load_sample_daily_costs
from engine.features.feature_engineering import prepare_daily_features
from engine.models.forecast_arima import forecast_daily_cost_arima
from engine.models.anomaly import detect_cost_anomalies
from engine.recommendations.rules import generate_recommendations
from engine.recommendations.savings_sim import simulate_savings_plans_and_ri
from engine.reports.pdf_report import generate_executive_pdf

def build_report(df_raw: pd.DataFrame) -> dict:
    df_feat = prepare_daily_features(df_raw)
    forecast = forecast_daily_cost_arima(df_feat, horizon_days=30)

    anomalies_df = detect_cost_anomalies(df_feat, contamination=0.05)
    anomalies = [
        {"date": str(pd.to_datetime(row["date"]).date()), "cost": float(row["cost"])}
        for _, row in anomalies_df.iterrows()
    ]

    total_30d = float(forecast["total_forecast"])
    recs = generate_recommendations(total_30d_forecast=total_30d, anomalies_count=len(anomalies))

    last30 = float(df_feat.tail(30)["cost"].astype(float).sum())
    savings = simulate_savings_plans_and_ri(monthly_on_demand_spend=last30)

    return {
        "generated_at": pd.Timestamp.utcnow().isoformat(),
        "data": {"days_used": int(len(df_raw)), "last_30d_spend": last30},
        "forecast": {"model": forecast["model"], "total_30d_forecast": total_30d, "daily_forecast": forecast["daily_forecast"]},
        "anomalies": anomalies,
        "recommendations": recs,
        "savings_simulation": savings,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-sample", action="store_true")
    parser.add_argument("--out-dir", default="out")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.use_sample:
        df = load_sample_daily_costs(Path("data/sample/daily_costs.csv"))
    else:
        df = fetch_cost_data(days=120)

    report = build_report(df)

    json_path = out_dir / "latest-report.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    pdf_path = out_dir / "executive-report.pdf"
    generate_executive_pdf(report, str(pdf_path))

    print("Wrote:", json_path)
    print("Wrote:", pdf_path)

if __name__ == "__main__":
    main()
