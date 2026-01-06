# AI Cost Optimization Engine (Pro)
**Finance + Cloud + AI** — production-style cost forecasting + waste detection + optimization recommendations.

This repo includes:
- ☁️ **AWS Lambda + EventBridge** scheduled scans (Terraform)
- 🔐 **Least-privilege IAM policy** (Terraform + JSON)
- 🤖 **ARIMA forecasting** (statsmodels) with a simple fallback model
- 📈 **Savings Plan / Reserved Instance simulation** (rule-based estimator)
- 🧾 **Executive PDF report** generation (ReportLab)
- 📊 **TypeScript dashboard** (React + Vite + Recharts) to visualize results
- 🚦 **DevSecOps CI + Scheduled cost scans** (GitHub Actions)

---

## Architecture (High Level)
```
EventBridge (daily schedule)
  -> Lambda (Python)
     -> AWS Cost Explorer (read-only)
     -> Forecast (ARIMA)
     -> Anomaly detection
     -> Recommendations + SP/RI simulation
     -> Write artifacts to S3 (JSON + PDF)
Dashboard (React/TS) -> fetch JSON report from S3 (or API/local)
```

---

## Local Run (no AWS required)
Uses sample cost data in `data/sample/daily_costs.csv`.
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python engine/reports/generate_report.py --use-sample
```

Artifacts:
- `out/latest-report.json`
- `out/executive-report.pdf`

---

## AWS Deploy (Terraform)
```bash
cd infra/terraform
terraform init
terraform apply
```

Outputs:
- `report_bucket_name`
- `report_prefix`

Lambda writes:
- `s3://<bucket>/<prefix>/latest-report.json`
- `s3://<bucket>/<prefix>/executive-report.pdf`

---

## Dashboard
```bash
cd dashboard
npm install
echo "VITE_REPORT_URL=http://localhost:8000/out/latest-report.json" > .env.local
npm run dev
```
Open: http://localhost:5173


## Live API Endpoint (API Gateway)
After `terraform apply`, use the output `api_base_url`.
The dashboard can hit:
- `${api_base_url}/report`

Set:
```bash
echo "VITE_API_URL=${api_base_url}" > dashboard/.env.local
```
