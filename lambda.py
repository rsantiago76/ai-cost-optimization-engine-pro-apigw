from __future__ import annotations
import json
import os
from pathlib import Path
import boto3

from engine.reports.generate_report import build_report
from engine.ingestion.aws_cost_explorer import fetch_cost_data
from engine.reports.pdf_report import generate_executive_pdf

s3 = boto3.client("s3")

REPORT_BUCKET = os.environ.get("REPORT_BUCKET", "")
REPORT_PREFIX = os.environ.get("REPORT_PREFIX", "reports")

def handler(event, context):
    df = fetch_cost_data(days=120)
    report = build_report(df)

    out_json = Path("/tmp/latest-report.json")
    out_pdf = Path("/tmp/executive-report.pdf")
    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    generate_executive_pdf(report, str(out_pdf))

    if REPORT_BUCKET:
        json_key = f"{REPORT_PREFIX.rstrip('/')}/latest-report.json"
        pdf_key = f"{REPORT_PREFIX.rstrip('/')}/executive-report.pdf"
        s3.upload_file(str(out_json), REPORT_BUCKET, json_key, ExtraArgs={"ContentType":"application/json"})
        s3.upload_file(str(out_pdf), REPORT_BUCKET, pdf_key, ExtraArgs={"ContentType":"application/pdf"})
        return {"statusCode": 200, "body": json.dumps({"status":"uploaded","bucket":REPORT_BUCKET,"json_key":json_key,"pdf_key":pdf_key})}

    return {"statusCode": 200, "body": json.dumps({"status":"completed","note":"REPORT_BUCKET not set"})}
