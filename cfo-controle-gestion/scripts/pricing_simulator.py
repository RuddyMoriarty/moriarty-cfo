#!/usr/bin/env python3
"""
pricing_simulator.py, simule l'impact d'un changement de prix selon élasticité.

Input : prix actuel + volume actuel + coût variable unitaire + élasticité estimée
Output : scénarios CA + marge avec différents niveaux de prix
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def simulate(
    prix_actuel: float,
    volume_actuel: float,
    cout_variable_unitaire: float,
    elasticite: float,
    nouveau_prix: float,
) -> dict:
    """Simule l'impact d'un changement de prix."""
    pct_variation_prix = (nouveau_prix - prix_actuel) / prix_actuel
    pct_variation_volume = -elasticite * pct_variation_prix
    nouveau_volume = volume_actuel * (1 + pct_variation_volume)

    ca_actuel = prix_actuel * volume_actuel
    ca_nouveau = nouveau_prix * nouveau_volume

    marge_actuelle = (prix_actuel - cout_variable_unitaire) * volume_actuel
    marge_nouvelle = (nouveau_prix - cout_variable_unitaire) * nouveau_volume

    return {
        "prix_actuel": prix_actuel,
        "prix_nouveau": nouveau_prix,
        "variation_prix_pct": round(pct_variation_prix * 100, 1),
        "volume_actuel": volume_actuel,
        "volume_nouveau_estime": round(nouveau_volume, 0),
        "variation_volume_pct": round(pct_variation_volume * 100, 1),
        "ca_actuel": round(ca_actuel, 0),
        "ca_nouveau": round(ca_nouveau, 0),
        "variation_ca_eur": round(ca_nouveau - ca_actuel, 0),
        "variation_ca_pct": round((ca_nouveau - ca_actuel) / ca_actuel * 100, 1),
        "marge_actuelle": round(marge_actuelle, 0),
        "marge_nouvelle": round(marge_nouvelle, 0),
        "variation_marge_eur": round(marge_nouvelle - marge_actuelle, 0),
        "variation_marge_pct": round((marge_nouvelle - marge_actuelle) / marge_actuelle * 100, 1) if marge_actuelle > 0 else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Pricing simulator")
    parser.add_argument("--prix-actuel", type=float, required=True)
    parser.add_argument("--volume-actuel", type=float, required=True)
    parser.add_argument("--cout-variable", type=float, required=True)
    parser.add_argument("--elasticite", type=float, default=1.0,
                        help="Élasticité prix-demande (1.0 = neutre, >1 élastique)")
    parser.add_argument("--scenarios", type=float, nargs="+", default=[-10, -5, 5, 10, 15],
                        help="Variations de prix en %% à tester")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    scenarios = []
    for pct in args.scenarios:
        nouveau_prix = args.prix_actuel * (1 + pct / 100)
        sim = simulate(
            args.prix_actuel, args.volume_actuel, args.cout_variable,
            args.elasticite, nouveau_prix,
        )
        sim["scenario_label"] = f"{pct:+.0f}%"
        scenarios.append(sim)

    # Identifier le meilleur scénario (plus forte marge)
    best = max(scenarios, key=lambda s: s["marge_nouvelle"])

    result = {
        "_version": "0.1.0",
        "inputs": {
            "prix_actuel": args.prix_actuel,
            "volume_actuel": args.volume_actuel,
            "cout_variable_unitaire": args.cout_variable,
            "elasticite_estimée": args.elasticite,
        },
        "scenarios": scenarios,
        "best_scenario": {
            "label": best["scenario_label"],
            "prix": best["prix_nouveau"],
            "marge": best["marge_nouvelle"],
            "variation_marge_pct": best["variation_marge_pct"],
        },
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Pricing simulation : {args.output}", file=sys.stderr)
        print(f"  → Meilleur scénario : {best['scenario_label']} ({best['variation_marge_pct']:+.1f}% de marge)", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
