export type DailyForecastPoint = { date: string; yhat: number };
export type Report = {
  generated_at: string;
  data: { days_used: number; last_30d_spend: number };
  forecast: { model: string; total_30d_forecast: number; daily_forecast: DailyForecastPoint[] };
  anomalies: { date: string; cost: number }[];
  recommendations: { category: string; recommendation: string; estimated_savings: string; confidence: string }[];
  savings_simulation: {
    eligible_estimated: number;
    savings_plans: { low: number; high: number };
    reserved_instances: { low: number; high: number };
    notes: string;
  };
};
