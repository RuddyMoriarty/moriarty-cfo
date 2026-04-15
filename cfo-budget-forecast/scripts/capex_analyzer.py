#!/usr/bin/env python3
"""
capex_analyzer.py, calcule Payback, NPV, IRR, ROI pour un projet CAPEX.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def compute_npv(cash_flows: list[float], rate: float) -> float:
    """NPV = Σ CF_t / (1+r)^t."""
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))


def compute_irr(cash_flows: list[float], max_iterations: int = 1000, tolerance: float = 1e-6) -> float | None:
    """IRR par bissection."""
    low, high = -0.99, 10.0  # taux entre -99% et 1000%
    for _ in range(max_iterations):
        mid = (low + high) / 2
        npv = compute_npv(cash_flows, mid)
        if abs(npv) < tolerance:
            return round(mid * 100, 2)
        if npv > 0:
            low = mid
        else:
            high = mid
    return None


def compute_payback(cash_flows: list[float]) -> float | None:
    """Payback simple (non actualisé)."""
    cumulative = 0
    for t, cf in enumerate(cash_flows):
        cumulative += cf
        if cumulative >= 0 and t > 0:
            # Interpolation linéaire
            prev_cum = cumulative - cf
            return round(t - 1 + (-prev_cum) / cf, 2)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyse CAPEX (Payback, NPV, IRR, ROI)")
    parser.add_argument("--investissement", type=float, required=True, help="Investissement initial (€)")
    parser.add_argument("--cash-flows", type=float, nargs="+", required=True,
                        help="Cash flows annuels attendus (ex: 40 40 40 40 40 pour 5 ans de 40k€)")
    parser.add_argument("--wacc", type=float, default=10.0, help="WACC en %% (défaut 10)")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    cash_flows = [-args.investissement] + args.cash_flows

    npv = compute_npv(cash_flows, args.wacc / 100)
    irr = compute_irr(cash_flows)
    payback = compute_payback(cash_flows)
    roi_annuel = sum(args.cash_flows) / len(args.cash_flows) / args.investissement * 100

    # Décision
    decision = "🔴 NO-GO"
    reasons = []
    if npv > 0:
        reasons.append(f"NPV positive ({npv:,.0f} €)")
    else:
        reasons.append(f"NPV NÉGATIVE ({npv:,.0f} €) → destruction de valeur")

    if irr and irr > args.wacc:
        reasons.append(f"IRR {irr}% > WACC {args.wacc}%")
    else:
        reasons.append(f"IRR {irr}% ≤ WACC {args.wacc}% → rendement insuffisant")

    if payback and payback < 5:
        reasons.append(f"Payback {payback} ans < 5 ans")
    else:
        reasons.append(f"Payback {payback} ans ≥ 5 ans (long)")

    if npv > 0 and irr and irr > args.wacc and payback and payback < 5:
        decision = "🟢 GO"
    elif npv > 0 and irr and irr > args.wacc:
        decision = "🟡 GO (attention payback)"

    result = {
        "_version": "0.1.0",
        "inputs": {
            "investissement": args.investissement,
            "cash_flows": args.cash_flows,
            "wacc_pct": args.wacc,
        },
        "metrics": {
            "npv_eur": round(npv, 2),
            "irr_pct": irr,
            "payback_annees": payback,
            "roi_annuel_pct": round(roi_annuel, 1),
        },
        "decision": decision,
        "raisons": reasons,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Analyse CAPEX : {args.output}", file=sys.stderr)
        print(f"  → {decision}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
