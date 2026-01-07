# AI Cost Optimization Engine (Pro)
**Finance + Cloud + AI** — production-style cost forecasting + waste detection + optimization recommendations.

A production-style cloud cost optimization platform built on AWS that ingests billing data, forecasts spend using time-series machine learning, detects anomalies and waste, simulates Savings Plan / Reserved Instance savings, and exposes results via a secure API Gateway endpoint to a React + TypeScript dashboard.

This project demonstrates rare crossover expertise across:

Cloud Infrastructure

Financial Operations (FinOps)

Applied Machine Learning

Security & IAM Governance

DevSecOps Automation

#  🏗️ System Architecture (End-to-End)
Architecture Flow

<img width="936" height="556" alt="image" src="https://github.com/user-attachments/assets/97bddda5-5e98-4e22-994e-7ec4187a92f8" />


<img width="1999" height="1235" alt="image" src="https://github.com/user-attachments/assets/88ade830-cc34-48aa-adca-d57ef8d34a1c" />


<img width="1457" height="654" alt="image" src="https://github.com/user-attachments/assets/5c14885b-6154-4277-a7ba-2d5401283aaa" />



Amazon EventBridge (Scheduled)
   ↓
AWS Lambda – Cost Analysis Engine (Python)
   ↓
AWS Cost Explorer (Billing Data – Read Only)
   ↓
Forecasting • Anomaly Detection • Savings Simulation
   ↓
Amazon S3 (Private Reports Bucket)
   ↓
Amazon API Gateway (GET /report)
   ↓
React + TypeScript Dashboard

#  Component Breakdown
Amazon EventBridge (Scheduled)

- Triggers daily automated cost scans

- Enables continuous FinOps monitoring without manual intervention

# AWS Lambda – Cost Analysis Engine (Python)

- Pulls billing data from AWS Cost Explorer

- Forecasts spend using ARIMA

- Detects anomalies and cost waste

- Simulates Savings Plans / Reserved Instances

Produces:

- latest-report.json

- executive-report.pdf

#  Amazon S3 (Private Reports Bucket)

- Stores JSON + PDF artifacts

- No public access

- IAM-scoped to a single bucket and prefix

# Amazon API Gateway (HTTP API)

- Endpoint: GET /report

- Returns the latest optimization report

- CORS-enabled for frontend consumption

# React + TypeScript Dashboard

- Fetches live data from API Gateway

- Visualizes forecasts, anomalies, and savings

- Zero AWS credentials in the browser

# 🔐 Security & IAM Boundaries
# Security Design Principles
# Least Privilege by Default
The Lambda IAM role allows only:

- ce:GetCostAndUsage (read-only billing access)

- S3 access limited to a single bucket + prefix

- CloudWatch Logs

# Clear Trust Boundaries Frontend

- No AWS credentials

- Accesses data only via HTTPS API Gateway

# API Layer

- Read-only access to reports

- Designed for optional future auth (Cognito / JWT)

# Analysis Engine

- Isolated Lambda execution

- No inbound network access

# Storage

- Private S3 bucket

- Blocked from public access

# Defense-in-Depth

- IAM + API Gateway + CORS controls

- Clear separation of:

      - Data ingestion

      - Analysis

      - Presentation

This design aligns well with enterprise, government, and regulated cloud environments.

# 🧠 Key Capabilities
# 🤖 AI / ML Forecasting

- Time-series forecasting using ARIMA

- Fallback model for limited historical data

- Produces daily and 30-day spend forecasts

# 🚨 Waste & Anomaly Detection

- Isolation Forest for spend spike detection

- Identifies regressions after deployments

- Surfaces anomalies for investigation

# 📈 Savings Simulation

- Rule-based Savings Plans / RI estimator

- Explainable assumptions (FinOps-friendly)

- Produces estimated monthly savings ranges

# 🧾 Executive Reporting

- Auto-generated PDF executive report

- CFO-ready and audit-friendly

- Includes forecasts, risks, and recommendations

# 📊 Dashboard (React + TypeScript)

- Strict TypeScript

- API-driven state

- Recharts visualizations

- Production-ready structure

Configure Dashboard
cd dashboard
echo "VITE_API_URL=https://<api-id>.execute-api.us-east-1.amazonaws.com" > .env.local
npm install
npm run dev

☁️ AWS Deployment (Terraform)
cd infra/terraform
terraform init
terraform apply

# Outputs

- api_base_url → used by the dashboard

- report_bucket_name

- report_prefix

#🚦 DevSecOps & Automation

# GitHub Actions CI

- Python validation

- Sample report generation

# Scheduled Cost Scans

   - Weekly GitHub workflow (optional)

   - EventBridge-driven production scans

- Fully automated

- No manual intervention required

# 🎯 Why This Project Stands Out

This is a production-style cloud cost optimization platform built on AWS that ingests billing data, forecasts spend using time-series machine learning, detects anomalies and waste, simulates Savings Plan / Reserved Instance savings, and exposes results via a secure API Gateway endpoint to a React + TypeScript dashboard.

This project demonstrates rare crossover expertise across:

Cloud Infrastructure

Financial Operations (FinOps)

Applied Machine Learning

Security & IAM Governance

DevSecOps Automation

🏗️ System Architecture (End-to-End)
Architecture Flow

<img width="1536" height="1024" alt="end-to-end-architecture" src="https://github.com/user-attachments/assets/f55a40b8-ed96-4c57-b1f8-e967389ef77a" />



Amazon EventBridge (Scheduled)
   ↓
AWS Lambda – Cost Analysis Engine (Python)
   ↓
AWS Cost Explorer (Billing Data – Read Only)
   ↓
Forecasting • Anomaly Detection • Savings Simulation
   ↓
Amazon S3 (Private Reports Bucket)
   ↓
Amazon API Gateway (GET /report)
   ↓
React + TypeScript Dashboard

Component Breakdown
Amazon EventBridge (Scheduled)

Triggers daily automated cost scans

Enables continuous FinOps monitoring without manual intervention

AWS Lambda – Cost Analysis Engine (Python)

Pulls billing data from AWS Cost Explorer

Forecasts spend using ARIMA

Detects anomalies and cost waste

Simulates Savings Plans / Reserved Instances

Produces:

latest-report.json

executive-report.pdf

Amazon S3 (Private Reports Bucket)

Stores JSON + PDF artifacts

No public access

IAM-scoped to a single bucket and prefix

Amazon API Gateway (HTTP API)

Endpoint: GET /report

Returns the latest optimization report

CORS-enabled for frontend consumption

React + TypeScript Dashboard

Fetches live data from API Gateway

Visualizes forecasts, anomalies, and savings

Zero AWS credentials in the browser

🔐 Security & IAM Boundaries
Security Design Principles
Least Privilege by Default



The Lambda IAM role allows only:

<img width="1620" height="904" alt="image" src="https://github.com/user-attachments/assets/d2e748fe-7512-4c47-a529-86fd3a374800" />


ce:GetCostAndUsage (read-only billing access)

S3 access limited to a single bucket + prefix

CloudWatch Logs

Clear Trust Boundaries

Frontend

No AWS credentials

Accesses data only via HTTPS API Gateway

API Layer

Read-only access to reports

Designed for optional future auth (Cognito / JWT)

Analysis Engine

Isolated Lambda execution

No inbound network access

Storage

Private S3 bucket

Blocked from public access

Defense-in-Depth

IAM + API Gateway + CORS controls

Clear separation of:

Data ingestion

Analysis

Presentation

This design aligns well with enterprise, government, and regulated cloud environments.

🧠 Key Capabilities
🤖 AI / ML Forecasting

Time-series forecasting using ARIMA

Fallback model for limited historical data

Produces daily and 30-day spend forecasts

🚨 Waste & Anomaly Detection

Isolation Forest for spend spike detection

Identifies regressions after deployments

Surfaces anomalies for investigation

📈 Savings Simulation

Rule-based Savings Plans / RI estimator

Explainable assumptions (FinOps-friendly)

Produces estimated monthly savings ranges

🧾 Executive Reporting

Auto-generated PDF executive report

CFO-ready and audit-friendly

Includes forecasts, risks, and recommendations

📊 Dashboard (React + TypeScript)

Strict TypeScript

API-driven state

Recharts visualizations

Production-ready structure

Configure Dashboard
cd dashboard
echo "VITE_API_URL=https://<api-id>.execute-api.us-east-1.amazonaws.com" > .env.local
npm install
npm run dev

☁️ AWS Deployment (Terraform)
cd infra/terraform
terraform init
terraform apply

Outputs

api_base_url → used by the dashboard

report_bucket_name

report_prefix

🚦 DevSecOps & Automation

GitHub Actions CI

Python validation

Sample report generation

Scheduled Cost Scans

Weekly GitHub workflow (optional)

EventBridge-driven production scans

Fully automated

No manual intervention required

# 🎯 Why This Project Stands Out

This demonstrates:

- Real AWS billing integration

- Financial decision-making logic

- Serverless production architecture

- IAM-driven security boundaries

- Executive-level reporting

This is the type of system used by:

- Cloud platform teams

- FinOps organizations

- Security-conscious enterprises

- Government & regulated environments

# 🧾 Summary

Designed and implemented a serverless AI-driven cost optimization platform using AWS Lambda, EventBridge, API Gateway, and S3, featuring ARIMA-based spend forecasting, anomaly detection, Savings Plan/Reserved Instance simulations, least-privilege IAM controls, and a React/TypeScript dashboard consuming a live API.


