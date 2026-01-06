# Terraform: Lambda + EventBridge Scheduled Cost Scan + API Gateway

Deploys:
- S3 bucket for reports (private)
- IAM role + least-privilege policy (Cost Explorer read + S3 prefix read/write + logs)
- Lambda scheduled job (EventBridge) that writes `latest-report.json` + `executive-report.pdf` to S3
- **API Gateway HTTP API** + Lambda proxy endpoint:
  - `GET /report` -> returns the latest JSON report (reads from S3; generates if missing)

## Deploy
```bash
terraform init
terraform apply
```

## Outputs
- `api_base_url` (use in dashboard as `VITE_API_URL`)
- `report_bucket_name`
- `report_prefix`
