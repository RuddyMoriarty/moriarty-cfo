#!/usr/bin/env python3
"""
valuation_calculator.py — calcule la valorisation par DCF + multiples.

Input : forecast cash flows + multiples sectoriels + WACC
Output : fourchette de valorisation (DCF + multiples EBITDA + multiples Revenue)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def compute_dcf(cash_flows: list[float], wacc: float, growth_perpetual: float, valeur_terminale_method: str = "gordon_shapiro") -> dict:
    """DCF avec valeur terminale Gordon-Shapiro."""
    # Actualisation des cash flows explicites
    pv_cfs = sum(cf / (1 + wacc) ** (t + 1) for t, cf in enumerate(cash_flows))

    # Valeur terminale (Gordon-Shapiro)
    if wacc <= growth_perpetual:
        return {"error": "WACC doit être > taux croissance perpétuelle"}

    cf_n_plus_1 = cash_flows[-1] * (1 + growth_perpetual)
    valeur_terminale = cf_n_plus_1 / (wacc - growth_perpetual)
    pv_valeur_terminale = valeur_terminale / (1 + wacc) ** len(cash_flows)

    enterprise_value = pv_cfs + pv_valeur_terminale

    return {
        "method": "DCF",
        "wacc_pct": round(wacc * 100, 2),
        "growth_perpetual_pct": round(growth_perpetual * 100, 2),
        "pv_cash_flows": round(pv_cfs, 0),
        "pv_valeur_terminale": round(pv_valeur_terminale, 0),
        "enterprise_value": round(enterprise_value, 0),
    }


def compute_multiples(ebitda: float, revenue: float, multiples_ebitda: list[float], multiples_revenue: list[float]) -> dict:
    """Valorisation par multiples (EBITDA + Revenue)."""
    return {
        "method": "Multiples",
        "ev_ebitda_low": round(ebitda * min(multiples_ebitda), 0) if multiples_ebitda else None,
        "ev_ebitda_avg": round(ebitda * (sum(multiples_ebitda) / len(multiples_ebitda)), 0) if multiples_ebitda else None,
        "ev_ebitda_high": round(ebitda * max(multiples_ebitda), 0) if multiples_ebitda else None,
        "ev_revenue_low": round(revenue * min(multiples_revenue), 0) if multiples_revenue else None,
        "ev_revenue_avg": round(revenue * (sum(multiples_revenue) / len(multiples_revenue)), 0) if multiples_revenue else None,
        "ev_revenue_high": round(revenue * max(multiples_revenue), 0) if multiples_revenue else None,
    }


def compute_equity_value(ev: float, net_debt: float, provisions: float, cash_excedentaire: float) -> float:
    """Equity Value = EV - Net Debt - Provisions + Cash excédentaire."""
    return ev - net_debt - provisions + cash_excedentaire


def main() -> int:
    parser = argparse.ArgumentParser(description="Valorisation entreprise (DCF + multiples)")
    parser.add_argument("--cash-flows", type=float, nargs="+", required=True,
                        help="Cash flows annuels prévisionnels (5 ans)")
    parser.add_argument("--wacc", type=float, default=12.0, help="WACC en %% (défaut 12)")
    parser.add_argument("--growth-perpetual", type=float, default=2.0, help="Croissance perpétuelle %% (défaut 2)")
    parser.add_argument("--ebitda", type=float, required=True, help="EBITDA actuel pour multiples")
    parser.add_argument("--revenue", type=float, required=True, help="Revenue actuel pour multiples")
    parser.add_argument("--multiples-ebitda", type=float, nargs="+", default=[6, 8, 10],
                        help="Multiples EBITDA sectoriels (ex: 6 8 10)")
    parser.add_argument("--multiples-revenue", type=float, nargs="+", default=[1, 2, 3])
    parser.add_argument("--net-debt", type=float, default=0)
    parser.add_argument("--provisions", type=float, default=0)
    parser.add_argument("--cash-excedentaire", type=float, default=0)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    dcf = compute_dcf(args.cash_flows, args.wacc / 100, args.growth_perpetual / 100)
    multiples = compute_multiples(args.ebitda, args.revenue, args.multiples_ebitda, args.multiples_revenue)

    # Triangulation
    ev_estimations = []
    if "enterprise_value" in dcf:
        ev_estimations.append(dcf["enterprise_value"])
    if multiples.get("ev_ebitda_avg"):
        ev_estimations.append(multiples["ev_ebitda_avg"])
    if multiples.get("ev_revenue_avg"):
        ev_estimations.append(multiples["ev_revenue_avg"])

    ev_min = min(ev_estimations) if ev_estimations else 0
    ev_max = max(ev_estimations) if ev_estimations else 0
    ev_avg = sum(ev_estimations) / len(ev_estimations) if ev_estimations else 0

    equity_avg = compute_equity_value(ev_avg, args.net_debt, args.provisions, args.cash_excedentaire)

    result = {
        "_version": "0.1.0",
        "dcf": dcf,
        "multiples": multiples,
        "triangulation": {
            "ev_min": round(ev_min, 0),
            "ev_max": round(ev_max, 0),
            "ev_avg": round(ev_avg, 0),
            "equity_value_avg": round(equity_avg, 0),
            "ajustements": {
                "net_debt": args.net_debt,
                "provisions": args.provisions,
                "cash_excedentaire": args.cash_excedentaire,
            },
        },
        "warning": "Toute valorisation est sensible aux hypothèses. Toujours présenter une fourchette avec sensibilités. Pour opérations réelles : cabinet de transaction services.",
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Valorisation : {args.output}", file=sys.stderr)
        print(f"  → EV moyenne triangulée : {ev_avg:,.0f} € (Equity Value : {equity_avg:,.0f} €)", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
