#!/usr/bin/env python3
"""
forecast_12m.py — prévision de trésorerie 12 mois glissants avec scénarios.

Input : hypothèses CA + variations BFR + CAPEX + service de la dette
Output : JSON avec 12 mois × 3 scénarios (opt/réel/pess) + probabilité pondérée.
"""

from __future__ import annotations

import argparse
import calendar
import csv
import json
import sys
from datetime import date
from pathlib import Path


def add_months(d: date, n: int) -> date:
    month = d.month - 1 + n
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def build_months(start: date, n: int = 12) -> list[dict]:
    months = []
    for i in range(n):
        d = add_months(start.replace(day=1), i)
        months.append({
            "m": i + 1,
            "label": d.strftime("%b %Y"),
            "date_debut": d.isoformat(),
            "date_fin": add_months(d, 1).isoformat(),
        })
    return months


def generate_scenario(
    months: list[dict],
    solde_initial: float,
    ca_mensuel_base: float,
    growth_rate_annual: float,
    marge_ebitda_pct: float,
    capex_mensuel: float,
    remboursement_pret_mensuel: float,
    var_bfr_mensuel: float,
    label: str,
) -> list[dict]:
    """Génère un scénario mensuel sur 12 mois."""
    result = []
    solde = solde_initial
    growth_monthly = (1 + growth_rate_annual) ** (1/12) - 1
    ca = ca_mensuel_base

    for i, m in enumerate(months):
        ca_mois = ca
        ca *= (1 + growth_monthly)  # croissance mensuelle composée

        ebitda = ca_mois * (marge_ebitda_pct / 100)
        capex = capex_mensuel
        pret = remboursement_pret_mensuel
        var_bfr = var_bfr_mensuel

        # Cash flow approché : EBITDA - CAPEX - remboursement dette - variation BFR
        # (simplification : on n'intègre pas IS mensuel, taxes, etc. — v0.2 raffinera)
        flux_net = ebitda - capex - pret - var_bfr

        result.append({
            "month": m["label"],
            "m": m["m"],
            "ca": round(ca_mois, 0),
            "ebitda": round(ebitda, 0),
            "capex": round(capex, 0),
            "pret": round(pret, 0),
            "var_bfr": round(var_bfr, 0),
            "flux_net": round(flux_net, 0),
            "solde_debut": round(solde, 0),
            "solde_fin": round(solde + flux_net, 0),
        })
        solde += flux_net

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Forecast trésorerie 12 mois (3 scénarios)")
    parser.add_argument("--solde-initial", type=float, required=True)
    parser.add_argument("--ca-mensuel", type=float, required=True, help="CA mensuel de départ (€)")
    parser.add_argument("--growth-realiste", type=float, default=0.10, help="Croissance annuelle scénario réaliste (ex. 0.10 = 10%)")
    parser.add_argument("--marge-ebitda", type=float, default=15.0, help="Marge EBITDA en % du CA")
    parser.add_argument("--capex-mensuel", type=float, default=0)
    parser.add_argument("--remb-pret-mensuel", type=float, default=0)
    parser.add_argument("--var-bfr-mensuel", type=float, default=0, help="Variation BFR mensuelle (+ = consomme cash)")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    months = build_months(date.today(), n=12)

    # Scénarios
    scenario_opt = generate_scenario(
        months, args.solde_initial, args.ca_mensuel,
        args.growth_realiste * 1.5, args.marge_ebitda + 2,
        args.capex_mensuel, args.remb_pret_mensuel, args.var_bfr_mensuel * 0.7,
        "optimiste",
    )
    scenario_reel = generate_scenario(
        months, args.solde_initial, args.ca_mensuel,
        args.growth_realiste, args.marge_ebitda,
        args.capex_mensuel, args.remb_pret_mensuel, args.var_bfr_mensuel,
        "realiste",
    )
    scenario_pess = generate_scenario(
        months, args.solde_initial, args.ca_mensuel,
        args.growth_realiste * 0.5, args.marge_ebitda - 3,
        args.capex_mensuel, args.remb_pret_mensuel, args.var_bfr_mensuel * 1.3,
        "pessimiste",
    )

    # Pondération
    def pondere(idx):
        return (
            scenario_opt[idx]["solde_fin"] * 0.20
            + scenario_reel[idx]["solde_fin"] * 0.60
            + scenario_pess[idx]["solde_fin"] * 0.20
        )

    scenario_weighted = [
        {"month": m["label"], "m": m["m"], "solde_fin_pondere": round(pondere(i), 0)}
        for i, m in enumerate(months)
    ]

    result = {
        "_version": "0.1.0",
        "generated_at": date.today().isoformat(),
        "inputs": vars(args) if not args.output else {k: v for k, v in vars(args).items() if not isinstance(v, Path)},
        "scenarios": {
            "optimiste": scenario_opt,
            "realiste": scenario_reel,
            "pessimiste": scenario_pess,
            "weighted": scenario_weighted,
        },
        "summary": {
            "solde_fin_opt_12m": scenario_opt[-1]["solde_fin"],
            "solde_fin_reel_12m": scenario_reel[-1]["solde_fin"],
            "solde_fin_pess_12m": scenario_pess[-1]["solde_fin"],
            "solde_fin_pondere_12m": scenario_weighted[-1]["solde_fin_pondere"],
            "runway_pess_mois": next(
                (m["m"] for m in scenario_pess if m["solde_fin"] < 0),
                ">12"
            ),
        },
    }

    output = json.dumps(result, indent=2, ensure_ascii=False, default=str)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Forecast 12m généré : {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
