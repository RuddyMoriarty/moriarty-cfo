#!/usr/bin/env python3
"""
variance_analyzer.py, décompose les variances budget vs réel en effet volume/prix/mix.

Input : CSV avec colonnes segment,volume_budget,prix_budget,volume_reel,prix_reel
Output : décomposition effet volume / prix / mix par segment
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def analyze_variance_segment(
    segment: str,
    vol_budget: float, prix_budget: float,
    vol_reel: float, prix_reel: float,
) -> dict:
    """Décompose la variance d'un segment en effets volume/prix."""
    ca_budget = vol_budget * prix_budget
    ca_reel = vol_reel * prix_reel
    variance_totale = ca_reel - ca_budget

    # Méthode standard
    # Effet volume : variation quantité à prix budget
    effet_volume = (vol_reel - vol_budget) * prix_budget

    # Effet prix : variation prix à quantité réelle
    effet_prix = (prix_reel - prix_budget) * vol_reel

    # Vérification : volume + prix = variance totale
    # (Le mix est implicite si on analyse plusieurs segments)

    return {
        "segment": segment,
        "ca_budget": round(ca_budget, 2),
        "ca_reel": round(ca_reel, 2),
        "variance_totale": round(variance_totale, 2),
        "effet_volume": round(effet_volume, 2),
        "effet_prix": round(effet_prix, 2),
        "effet_volume_pct": round(effet_volume / ca_budget * 100, 1) if ca_budget > 0 else 0,
        "effet_prix_pct": round(effet_prix / ca_budget * 100, 1) if ca_budget > 0 else 0,
        "vol_budget": vol_budget,
        "vol_reel": vol_reel,
        "prix_budget": prix_budget,
        "prix_reel": prix_reel,
    }


def compute_mix_effect(variances: list[dict]) -> dict:
    """Calcule l'effet mix au niveau global."""
    ca_budget_total = sum(v["ca_budget"] for v in variances)
    ca_reel_total = sum(v["ca_reel"] for v in variances)

    # Marge budget pondérée vs marge réelle pondérée (simplifié: pas de marge par segment dans cette version)
    # Mix = différence entre CA réel au prix budget vs CA budget global
    ca_reel_au_prix_budget = sum(v["vol_reel"] * v["prix_budget"] for v in variances)

    effet_mix_approx = ca_reel_au_prix_budget - ca_budget_total - sum(v["effet_volume"] for v in variances)

    return {
        "ca_budget_total": round(ca_budget_total, 2),
        "ca_reel_total": round(ca_reel_total, 2),
        "variance_totale": round(ca_reel_total - ca_budget_total, 2),
        "effet_volume_total": round(sum(v["effet_volume"] for v in variances), 2),
        "effet_prix_total": round(sum(v["effet_prix"] for v in variances), 2),
        "effet_mix_approx": round(effet_mix_approx, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Variance analysis (volume/prix/mix)")
    parser.add_argument("--segments", type=Path, required=True,
                        help="CSV : segment,volume_budget,prix_budget,volume_reel,prix_reel")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    variances = []
    with args.segments.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                v = analyze_variance_segment(
                    row["segment"],
                    float(row["volume_budget"]),
                    float(row["prix_budget"]),
                    float(row["volume_reel"]),
                    float(row["prix_reel"]),
                )
                variances.append(v)
            except (KeyError, ValueError):
                continue

    summary = compute_mix_effect(variances)
    # Tri par variance totale absolue
    variances.sort(key=lambda x: abs(x["variance_totale"]), reverse=True)

    result = {
        "_version": "0.1.0",
        "summary": summary,
        "variances_par_segment": variances,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Variance analysis : {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
