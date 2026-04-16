#!/usr/bin/env python3
"""
budget_builder.py, génère un squelette de budget annuel.

Input : P&L réel N-1 (CSV) + hypothèses croissance
Output : budget annuel mensualisé CSV + 3 scénarios (opt/réel/pess)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

MONTHS = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]


def load_pnl_n1(path: Path) -> dict[str, float]:
    """Charge P&L N-1 : CSV avec colonnes poste,montant_annuel."""
    pnl = {}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                poste = row.get("poste", "")
                montant = float((row.get("montant_annuel") or "0").replace(",", "."))
                pnl[poste] = montant
            except (ValueError, KeyError):
                continue
    return pnl


def generate_scenario(pnl_n1: dict, growth_ca_pct: float, growth_charges_pct: float, marge_target_pct: float | None, label: str) -> dict:
    """Génère un scénario annuel + mensualisation linéaire simple."""
    ca_n1 = pnl_n1.get("ca_ht", 0)
    ca_n = ca_n1 * (1 + growth_ca_pct / 100)

    # Charges, croissance proportionnelle + correction si marge cible
    total_charges_n1 = sum(v for k, v in pnl_n1.items() if k.startswith("charge_"))
    total_charges_n = total_charges_n1 * (1 + growth_charges_pct / 100)

    # Si marge cible définie, ajuster les charges pour la respecter
    if marge_target_pct is not None:
        target_ebitda = ca_n * marge_target_pct / 100
        total_charges_n = ca_n - target_ebitda

    ebitda = ca_n - total_charges_n

    # Mensualisation linéaire (à affiner selon saisonnalité en v0.2)
    annee = {
        "label": label,
        "ca_ht_annuel": round(ca_n, 0),
        "charges_annuelles": round(total_charges_n, 0),
        "ebitda_annuel": round(ebitda, 0),
        "marge_ebitda_pct": round(ebitda / ca_n * 100, 1) if ca_n > 0 else 0,
        "mensualisation": {
            m: {
                "ca": round(ca_n / 12, 0),
                "charges": round(total_charges_n / 12, 0),
                "ebitda": round(ebitda / 12, 0),
            } for m in MONTHS
        },
    }
    return annee


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère budget annuel 3 scénarios")
    parser.add_argument("--pnl-n1", type=Path, required=True, help="CSV : poste,montant_annuel")
    parser.add_argument("--growth-ca", type=float, default=10.0, help="Pourcentage de croissance CA realiste")
    parser.add_argument("--growth-charges", type=float, default=8.0, help="Pourcentage de croissance charges")
    parser.add_argument("--marge-cible", type=float, default=None, help="Pourcentage marge EBITDA cible (facultatif)")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    pnl_n1 = load_pnl_n1(args.pnl_n1)
    if not pnl_n1:
        print("❌ P&L N-1 vide ou format invalide", file=sys.stderr)
        return 1

    scenarios = {
        "realiste": generate_scenario(pnl_n1, args.growth_ca, args.growth_charges, args.marge_cible, "réaliste"),
        "optimiste": generate_scenario(pnl_n1, args.growth_ca * 1.5, args.growth_charges * 0.8,
                                        (args.marge_cible + 2) if args.marge_cible else None, "optimiste"),
        "pessimiste": generate_scenario(pnl_n1, args.growth_ca * 0.5, args.growth_charges * 1.2,
                                         (args.marge_cible - 3) if args.marge_cible else None, "pessimiste"),
    }

    # Pondération 20/60/20
    pondere_ca = scenarios["optimiste"]["ca_ht_annuel"] * 0.20 + scenarios["realiste"]["ca_ht_annuel"] * 0.60 + scenarios["pessimiste"]["ca_ht_annuel"] * 0.20
    pondere_ebitda = scenarios["optimiste"]["ebitda_annuel"] * 0.20 + scenarios["realiste"]["ebitda_annuel"] * 0.60 + scenarios["pessimiste"]["ebitda_annuel"] * 0.20

    result = {
        "_version": "0.1.0",
        "pnl_n1": pnl_n1,
        "hypotheses": {
            "growth_ca_realiste_pct": args.growth_ca,
            "growth_charges_realiste_pct": args.growth_charges,
            "marge_cible_pct": args.marge_cible,
        },
        "scenarios": scenarios,
        "pondere_20_60_20": {
            "ca_ht_annuel": round(pondere_ca, 0),
            "ebitda_annuel": round(pondere_ebitda, 0),
        },
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Budget 3 scénarios : {args.output}", file=sys.stderr)
        print(f"  → Pondéré 20/60/20 : CA {pondere_ca:,.0f} € / EBITDA {pondere_ebitda:,.0f} €", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
