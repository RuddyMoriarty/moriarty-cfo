#!/usr/bin/env python3
"""
bfr_calculator.py, calcule BFR, DSO, DPO, DIO, CCC + propose leviers.

Input : balance + CA + achats
Output : ratios + benchmarks + leviers ciblés selon profil société.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BENCHMARKS_SECTORIELS = {
    "services_btob": {"dso": (45, 65), "dpo": (30, 50), "dio": (0, 15)},
    "industrie": {"dso": (60, 90), "dpo": (45, 65), "dio": (60, 120)},
    "commerce_negoce": {"dso": (15, 45), "dpo": (30, 60), "dio": (20, 60)},
    "saas_techno": {"dso": (30, 60), "dpo": (30, 50), "dio": (0, 5)},
    "btp": {"dso": (60, 90), "dpo": (45, 75), "dio": (30, 60)},
}


def compute_ratios(
    creances_clients_ttc: float,
    dettes_fournisseurs_ttc: float,
    stocks: float,
    ca_ttc: float,
    achats_ttc: float,
    cout_ventes: float,
) -> dict:
    """Calcule tous les ratios BFR."""
    def days(numer, denom):
        return round(numer * 365 / denom, 1) if denom > 0 else 0

    dso = days(creances_clients_ttc, ca_ttc)
    dpo = days(dettes_fournisseurs_ttc, achats_ttc) if achats_ttc > 0 else 0
    dio = days(stocks, cout_ventes) if cout_ventes > 0 else 0
    ccc = dso + dio - dpo

    bfr = creances_clients_ttc + stocks - dettes_fournisseurs_ttc
    bfr_en_jours = days(bfr, ca_ttc)

    return {
        "dso": dso,
        "dpo": dpo,
        "dio": dio,
        "ccc": round(ccc, 1),
        "bfr": round(bfr, 0),
        "bfr_en_jours_ca": bfr_en_jours,
    }


def benchmark(ratios: dict, secteur: str) -> dict:
    bench = BENCHMARKS_SECTORIELS.get(secteur, BENCHMARKS_SECTORIELS["services_btob"])
    def eval_ratio(val, rng, higher_is_worse=True):
        if higher_is_worse:
            if val < rng[0]:
                return "✓ meilleur que médiane"
            if val <= rng[1]:
                return "~ dans la norme"
            return "✗ au-dessus de médiane (à améliorer)"
        else:
            if val > rng[1]:
                return "✓ meilleur que médiane"
            if val >= rng[0]:
                return "~ dans la norme"
            return "✗ sous médiane (opportunité)"

    return {
        "secteur": secteur,
        "dso": eval_ratio(ratios["dso"], bench["dso"], higher_is_worse=True),
        "dpo": eval_ratio(ratios["dpo"], bench["dpo"], higher_is_worse=False),
        "dio": eval_ratio(ratios["dio"], bench["dio"], higher_is_worse=True),
        "benchmark_dso": bench["dso"],
        "benchmark_dpo": bench["dpo"],
        "benchmark_dio": bench["dio"],
    }


def propose_leviers(ratios: dict, benchmark_result: dict) -> list[dict]:
    """Propose des leviers d'optimisation ciblés selon les ratios."""
    leviers = []
    bench = benchmark_result

    if "✗" in bench["dso"]:
        dso_excess = ratios["dso"] - bench["benchmark_dso"][1]
        leviers.append({
            "type": "optimisation_dso",
            "priorite": "haute" if dso_excess > 20 else "moyenne",
            "description": "Réduire le DSO via relance active + acompte client",
            "gain_estime_jours": round(min(dso_excess, 20), 0),
            "difficulte": "⭐ facile",
        })

    if "✗" in bench["dpo"]:
        dpo_gap = bench["benchmark_dpo"][0] - ratios["dpo"]
        leviers.append({
            "type": "renegociation_dpo",
            "priorite": "moyenne",
            "description": "Renégocier conditions fournisseurs (LME max 60 jours)",
            "gain_estime_jours": round(min(dpo_gap, 15), 0),
            "difficulte": "⭐⭐⭐ difficile (rapport de force)",
        })

    if ratios["dio"] > 90:
        leviers.append({
            "type": "optimisation_stocks",
            "priorite": "haute",
            "description": "Passage JIT + ABC analysis + liquidation stocks obsolètes",
            "gain_estime_jours": round(ratios["dio"] * 0.3, 0),
            "difficulte": "⭐⭐⭐ industrie",
        })

    if ratios["dso"] > 60 and ratios["bfr"] > 500000:
        leviers.append({
            "type": "factoring",
            "priorite": "moyenne",
            "description": "Mettre en place l'affacturage",
            "gain_estime_jours": round(ratios["dso"] * 0.9, 0),
            "cout_estime_pct": "0.5-3% du CA cédé",
            "difficulte": "⭐⭐ moyen",
        })

    return leviers


def main() -> int:
    parser = argparse.ArgumentParser(description="Calcul BFR + leviers")
    parser.add_argument("--creances-clients", type=float, required=True, help="Créances clients TTC (€)")
    parser.add_argument("--dettes-fournisseurs", type=float, required=True)
    parser.add_argument("--stocks", type=float, default=0)
    parser.add_argument("--ca-ttc", type=float, required=True, help="CA TTC annualisé")
    parser.add_argument("--achats-ttc", type=float, required=True)
    parser.add_argument("--cout-ventes", type=float, default=0)
    parser.add_argument("--secteur", default="services_btob",
                        choices=list(BENCHMARKS_SECTORIELS.keys()))
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    # Validation business : CA TTC = 0 rend les ratios DSO/BFR/jours_ca impossibles a calculer.
    if args.ca_ttc <= 0:
        print(
            "❌ CA TTC invalide (doit etre > 0). Impossible de calculer DSO/BFR en jours.",
            file=sys.stderr,
        )
        return 1

    ratios = compute_ratios(
        args.creances_clients, args.dettes_fournisseurs, args.stocks,
        args.ca_ttc, args.achats_ttc, args.cout_ventes,
    )
    bench = benchmark(ratios, args.secteur)
    leviers = propose_leviers(ratios, bench)

    # Gain potentiel total
    gain_jours_total = sum(l.get("gain_estime_jours", 0) for l in leviers)
    gain_eur_potentiel = round(gain_jours_total * args.ca_ttc / 365, 0)

    result = {
        "_version": "0.1.0",
        "ratios": ratios,
        "benchmark": bench,
        "leviers": leviers,
        "gain_potentiel": {
            "jours_total": gain_jours_total,
            "eur_liberables": gain_eur_potentiel,
            "note": "Estimation basée sur application des leviers identifiés",
        },
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Analyse BFR : {args.output}", file=sys.stderr)
        print(f"✓ {len(leviers)} levier(s) identifié(s), gain potentiel {gain_eur_potentiel:,.0f} €", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
