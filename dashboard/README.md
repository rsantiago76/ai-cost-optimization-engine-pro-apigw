# Cost Optimization Dashboard (React + TypeScript + Vite + Recharts)

Visualizes a live cost-optimization report.

## Option A (Recommended): API Gateway URL
After deploying Terraform, set the API URL output:
```bash
echo "VITE_API_URL=https://xxxx.execute-api.us-east-1.amazonaws.com" > .env.local
npm install
npm run dev
```

## Option B: Direct report JSON URL
```bash
echo "VITE_REPORT_URL=https://example.com/latest-report.json" > .env.local
npm install
npm run dev
```
