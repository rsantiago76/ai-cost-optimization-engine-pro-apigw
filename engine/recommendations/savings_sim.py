from __future__ import annotations

def simulate_savings_plans_and_ri(monthly_on_demand_spend: float) -> dict:
    eligible = monthly_on_demand_spend * 0.55
    sp_low, sp_high = eligible * 0.20, eligible * 0.35
    ri_low, ri_high = eligible * 0.25, eligible * 0.45

    return {
        "eligible_estimated": round(eligible, 2),
        "savings_plans": {"low": round(sp_low, 2), "high": round(sp_high, 2)},
        "reserved_instances": {"low": round(ri_low, 2), "high": round(ri_high, 2)},
        "notes": "Rule-based estimate; replace with workload-specific analysis for production."
    }
