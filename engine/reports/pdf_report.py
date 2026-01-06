from __future__ import annotations
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime

def generate_executive_pdf(report: dict, out_path: str) -> str:
    c = canvas.Canvas(out_path, pagesize=letter)
    width, height = letter

    c.setTitle("Executive Cloud Cost Report")

    y = height - 0.9 * inch
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.8 * inch, y, "Executive Cloud Cost Report")

    y -= 0.35 * inch
    c.setFont("Helvetica", 10)
    c.drawString(0.8 * inch, y, f"Generated: {datetime.utcnow().isoformat()}Z")

    y -= 0.5 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.8 * inch, y, "30-Day Forecast Summary")
    y -= 0.25 * inch
    c.setFont("Helvetica", 11)

    forecast_total = float(report.get("forecast", {}).get("total_30d_forecast", 0.0))
    c.drawString(0.9 * inch, y, f"Forecasted spend (30 days): ${forecast_total:,.2f}")
    y -= 0.22 * inch

    anomalies = report.get("anomalies", [])
    c.drawString(0.9 * inch, y, f"Anomalies detected: {len(anomalies)}")
    y -= 0.35 * inch

    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.8 * inch, y, "Estimated Savings Opportunities (SP/RI Simulation)")
    y -= 0.25 * inch
    c.setFont("Helvetica", 11)
    sim = report.get("savings_simulation", {})
    sp = sim.get("savings_plans", {})
    ri = sim.get("reserved_instances", {})
    c.drawString(0.9 * inch, y, f"Savings Plans: ${float(sp.get('low',0)):,.2f} - ${float(sp.get('high',0)):,.2f} / month (est.)")
    y -= 0.22 * inch
    c.drawString(0.9 * inch, y, f"Reserved Instances: ${float(ri.get('low',0)):,.2f} - ${float(ri.get('high',0)):,.2f} / month (est.)")
    y -= 0.35 * inch

    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.8 * inch, y, "Top Recommendations")
    y -= 0.25 * inch
    c.setFont("Helvetica", 10)

    recs = report.get("recommendations", []) or [{"recommendation":"No recommendations generated.", "confidence":"n/a"}]

    for i, r in enumerate(recs[:6], start=1):
        line = f"{i}. {r.get('recommendation','')} (confidence: {r.get('confidence','')})"
        if y < 1.2 * inch:
            c.showPage()
            y = height - 0.9 * inch
            c.setFont("Helvetica", 10)
        c.drawString(0.9 * inch, y, line[:120])
        y -= 0.18 * inch

    c.showPage()
    c.save()
    return out_path
