from __future__ import annotations

def generate_recommendations(total_30d_forecast: float, anomalies_count: int, tag_coverage: float | None = None) -> list[dict]:
    recs: list[dict] = []

    if total_30d_forecast > 20000:
        recs.append({
            "category": "commitment",
            "recommendation": "Evaluate Savings Plans or Reserved Instances for steady-state workloads",
            "estimated_savings": "medium-high",
            "confidence": "high",
        })

    if anomalies_count >= 3:
        recs.append({
            "category": "anomaly",
            "recommendation": "Investigate spend spikes; correlate with deployments, scaling, or misconfigured resources",
            "estimated_savings": "medium",
            "confidence": "medium",
        })

    if tag_coverage is not None and tag_coverage < 0.85:
        recs.append({
            "category": "governance",
            "recommendation": "Improve tagging coverage and enforce tag policies for cost allocation (Budgets/Cost Categories)",
            "estimated_savings": "medium",
            "confidence": "medium",
        })

    if not recs:
        recs.append({
            "category": "steady",
            "recommendation": "Costs appear stable; continue monitoring and tighten budgets/alerts for critical services",
            "estimated_savings": "low",
            "confidence": "medium",
        })

    return recs
