from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import boto3

from engine.ingestion.aws_cost_explorer import fetch_cost_data
from engine.reports.generate_report import build_report
from engine.reports.pdf_report import generate_executive_pdf

s3 = boto3.client("s3")

REPORT_BUCKET = os.environ.get("REPORT_BUCKET", "")
REPORT_PREFIX = os.environ.get("REPORT_PREFIX", "reports")
CORS_ORIGIN = os.environ.get("CORS_ORIGIN", "*")

def _resp(status: int, body: object):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": CORS_ORIGIN,
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
        },
        "body": json.dumps(body),
    }

def handler(event, context):
    # Handle preflight
    method = (event.get("requestContext", {}) or {}).get("http", {}).get("method") or event.get("httpMethod")
    if method == "OPTIONS":
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": CORS_ORIGIN,
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
            },
            "body": "",
        }

    if not REPORT_BUCKET:
        # If bucket isn't configured, generate on-demand and return
        df = fetch_cost_data(days=120)
        report = build_report(df)
        report["generated_at"] = datetime.utcnow().isoformat() + "Z"
        report["source"] = "on-demand"
        return _resp(200, report)

    json_key = f"{REPORT_PREFIX.rstrip('/')}/latest-report.json"
    try:
        obj = s3.get_object(Bucket=REPORT_BUCKET, Key=json_key)
        payload = obj["Body"].read().decode("utf-8")
        report = json.loads(payload)
        report["source"] = "s3"
        return _resp(200, report)
    except s3.exceptions.NoSuchKey:
        # Generate once if missing, upload, and return
        df = fetch_cost_data(days=120)
        report = build_report(df)
        tmp = Path("/tmp/latest-report.json")
        tmp.write_text(json.dumps(report, indent=2), encoding="utf-8")
        s3.upload_file(str(tmp), REPORT_BUCKET, json_key, ExtraArgs={"ContentType":"application/json"})
        report["source"] = "generated"
        return _resp(200, report)
    except Exception as e:
        return _resp(500, {"error": "Failed to fetch report", "details": str(e)})
