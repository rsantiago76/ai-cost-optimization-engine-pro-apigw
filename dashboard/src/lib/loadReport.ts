import type { Report } from "./types";
export async function loadReport(url: string): Promise<Report> {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`Failed to load report: ${r.status}`);
  return (await r.json()) as Report;
}
