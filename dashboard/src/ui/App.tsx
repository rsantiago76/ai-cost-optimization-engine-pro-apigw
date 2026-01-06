import { useEffect, useMemo, useState } from "react";
import { loadReport } from "../lib/loadReport";
import type { Report } from "../lib/types";
import { ForecastChart } from "./charts/ForecastChart";

const REPORT_URL = (import.meta.env.VITE_REPORT_URL as string | undefined) ?? "";
const API_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? "";
const EFFECTIVE_REPORT_URL = API_URL ? `${API_URL.replace(/\/$/, "")}/report` : REPORT_URL;

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ border: "1px solid #e6e6e6", borderRadius: 14, padding: 16, background: "white" }}>
      <div style={{ fontWeight: 800, marginBottom: 10 }}>{title}</div>
      {children}
    </div>
  );
}

function money(n: number) {
  return `$${n.toLocaleString(undefined, { maximumFractionDigits: 2 })}`;
}

export function App() {
  const [report, setReport] = useState<Report | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const canLoad = useMemo(() => EFFECTIVE_REPORT_URL.startsWith("http"), []);

  useEffect(() => {
    if (!canLoad) {
      setErr("Set VITE_API_URL (preferred) or VITE_REPORT_URL in dashboard/.env.local");
      return;
    }
    loadReport(EFFECTIVE_REPORT_URL)
      .then(setReport)
      .catch((e: unknown) => setErr(e instanceof Error ? e.message : "Unknown error"));
  }, [canLoad]);

  return (
    <div style={{ padding: 24, maxWidth: 1100, margin: "0 auto", fontFamily: "system-ui", background: "#f6f7f9", minHeight: "100vh" }}>
      <h1 style={{ margin: 0 }}>AI Cost Optimization Dashboard</h1>
      <div style={{ opacity: 0.75, marginTop: 6 }}>
        API URL: <code>{API_URL || "(not set)"}</code> • Report URL: <code>{EFFECTIVE_REPORT_URL || "(not set)"}</code>
      </div>

      {err && <pre style={{ background: "#fee", padding: 12, borderRadius: 10, marginTop: 16 }}>{err}</pre>}

      {report && (
        <>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16, marginTop: 16 }}>
            <Card title="Last 30 Days Spend">{money(report.data.last_30d_spend)}</Card>
            <Card title="30-Day Forecast">{money(report.forecast.total_30d_forecast)}</Card>
            <Card title="Anomalies Detected">{report.anomalies.length}</Card>
          </div>

          <div style={{ marginTop: 16 }}>
            <Card title={`Forecast Trend (${report.forecast.model})`}>
              <ForecastChart data={report.forecast.daily_forecast} />
            </Card>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 16 }}>
            <Card title="Savings Plan / RI Simulation (Est.)">
              <div>Eligible (est.): <b>{money(report.savings_simulation.eligible_estimated)}</b></div>
              <div style={{ marginTop: 8 }}>
                Savings Plans: <b>{money(report.savings_simulation.savings_plans.low)} - {money(report.savings_simulation.savings_plans.high)}</b>
              </div>
              <div style={{ marginTop: 6 }}>
                Reserved Instances: <b>{money(report.savings_simulation.reserved_instances.low)} - {money(report.savings_simulation.reserved_instances.high)}</b>
              </div>
              <div style={{ opacity: 0.75, marginTop: 10 }}>{report.savings_simulation.notes}</div>
            </Card>

            <Card title="Top Recommendations">
              <ul style={{ margin: 0, paddingLeft: 18 }}>
                {report.recommendations.map((r, i) => (
                  <li key={i} style={{ marginBottom: 10 }}>
                    <div><b>{r.category}</b> — {r.recommendation}</div>
                    <div style={{ opacity: 0.75 }}>Confidence: {r.confidence} • Savings: {r.estimated_savings}</div>
                  </li>
                ))}
              </ul>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
