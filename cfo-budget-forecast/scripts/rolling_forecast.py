#!/usr/bin/env python3
"""
rolling_forecast.py, met à jour la projection annuelle avec le réel YTD.

Input : budget annuel (JSON depuis budget_builder.py) + réel YTD (CSV)
Output : rolling forecast avec atterrissage annuel révisé
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def load_reel_ytd(path: Path) -> dict[str, float]:
    """Charge réel YTD : CSV avec colonnes poste,montant_ytd."""
    reel = {}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                poste = row.get("poste", "")
                montant = float((row.get("montant_ytd") or "0").replace(",", "."))
                reel[poste] = montant
            except (ValueError, KeyError):
                continue
    return reel


def compute_atterrissage(budget: dict, reel_ytd: dict, mois_ecoules: int) -> dict:
    """Calcule atterrissage annuel = réel YTD + projection du reste."""
    mois_restants = 12 - mois_ecoules

    # Méthode simple : projection du reste selon budget initial
    scenarios = {}
    for label, scenario in budget.get("scenarios", {}).items():
        ca_budget_annuel = scenario["ca_ht_annuel"]
        ca_budget_mensuel = ca_budget_annuel / 12
        ebitda_budget_annuel = scenario["ebitda_annuel"]
        ebitda_budget_mensuel = ebitda_budget_annuel / 12

        ca_reel_ytd = reel_ytd.get("ca_ht", 0)
        ebitda_reel_ytd = reel_ytd.get("ebitda", 0)

        ca_projete_reste = ca_budget_mensuel * mois_restants
        ebitda_projete_reste = ebitda_budget_mensuel * mois_restants

        ca_atterrissage = ca_reel_ytd + ca_projete_reste
        ebitda_atterrissage = ebitda_reel_ytd + ebitda_projete_reste

        variance_ca = ca_atterrissage - ca_budget_annuel
        variance_ebitda = ebitda_atterrissage - ebitda_budget_annuel

        scenarios[label] = {
            "budget_annuel": {
                "ca": ca_budget_annuel,
                "ebitda": ebitda_budget_annuel,
            },
            "reel_ytd": {
                "ca": ca_reel_ytd,
                "ebitda": ebitda_reel_ytd,
            },
            "atterrissage": {
                "ca": round(ca_atterrissage, 0),
                "ebitda": round(ebitda_atterrissage, 0),
            },
            "variance_vs_budget": {
                "ca_eur": round(variance_ca, 0),
                "ca_pct": round(variance_ca / ca_budget_annuel * 100, 1) if ca_budget_annuel > 0 else 0,
                "ebitda_eur": round(variance_ebitda, 0),
                "ebitda_pct": round(variance_ebitda / ebitda_budget_annuel * 100, 1) if ebitda_budget_annuel > 0 else 0,
            },
        }

    # Alerte selon scénario réaliste
    realiste = scenarios.get("realiste", {})
    variance_pct = abs(realiste.get("variance_vs_budget", {}).get("ebitda_pct", 0))
    if variance_pct > 10:
        niveau = "🔴 Budget révisé recommandé"
    elif variance_pct > 5:
        niveau = "🟠 Alerte"
    elif variance_pct > 2:
        niveau = "🟡 Vigilance"
    else:
        niveau = "🟢 OK"

    return {
        "_version": "0.1.0",
        "mois_ecoules": mois_ecoules,
        "mois_restants": mois_restants,
        "scenarios": scenarios,
        "niveau_alerte": niveau,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rolling forecast mensuel")
    parser.add_argument("--budget", type=Path, required=True, help="JSON budget annuel")
    parser.add_argument("--reel-ytd", type=Path, required=True, help="CSV réel YTD")
    parser.add_argument("--mois-ecoules", type=int, required=True, help="Nb mois écoulés (1-12)")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if args.mois_ecoules < 1 or args.mois_ecoules > 12:
        print("❌ --mois-ecoules doit être entre 1 et 12", file=sys.stderr)
        return 1

    budget = json.loads(args.budget.read_text(encoding="utf-8"))
    reel_ytd = load_reel_ytd(args.reel_ytd)

    result = compute_atterrissage(budget, reel_ytd, args.mois_ecoules)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Rolling forecast : {args.output}", file=sys.stderr)
        print(f"  → Niveau alerte : {result['niveau_alerte']}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
