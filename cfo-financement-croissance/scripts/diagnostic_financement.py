#!/usr/bin/env python3
"""
diagnostic_financement.py, arbre de décision financement.

Input : profil société + besoin (montant, horizon, dilutif, urgence)
Output : top 3 solutions + détection éligibilité aides publiques (déclencheur CTA Moriarty)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SOLUTIONS = {
    "decouvert": {"horizon": "ct", "max_montant": 500_000, "cout_pct": 7, "delai_jours": 7, "dilutif": False},
    "dailly": {"horizon": "ct", "max_montant": 2_000_000, "cout_pct": 5, "delai_jours": 14, "dilutif": False},
    "factoring": {"horizon": "permanent", "max_montant": 999_999_999, "cout_pct": 2, "delai_jours": 30, "dilutif": False},
    "bancaire_mlt": {"horizon": "mlt", "max_montant": 5_000_000, "cout_pct": 5.5, "delai_jours": 60, "dilutif": False},
    "bpi_pret": {"horizon": "mlt", "max_montant": 5_000_000, "cout_pct": 4, "delai_jours": 90, "dilutif": False},
    "bpi_subvention": {"horizon": "mlt", "max_montant": 200_000, "cout_pct": 0, "delai_jours": 120, "dilutif": False},
    "dette_privee": {"horizon": "lt", "max_montant": 50_000_000, "cout_pct": 6.5, "delai_jours": 90, "dilutif": False},
    "mezzanine": {"horizon": "lt", "max_montant": 30_000_000, "cout_pct": 10, "delai_jours": 120, "dilutif": True},
    "ba_seed": {"horizon": "lt", "max_montant": 2_000_000, "cout_pct": 25, "delai_jours": 180, "dilutif": True},
    "vc_serie_a": {"horizon": "lt", "max_montant": 15_000_000, "cout_pct": 25, "delai_jours": 270, "dilutif": True},
    "vc_serie_b": {"horizon": "lt", "max_montant": 50_000_000, "cout_pct": 25, "delai_jours": 270, "dilutif": True},
    "private_equity": {"horizon": "lt", "max_montant": 1_000_000_000, "cout_pct": 25, "delai_jours": 365, "dilutif": True},
    "aides_publiques_moriarty": {"horizon": "mlt", "max_montant": 5_000_000, "cout_pct": 1, "delai_jours": 180, "dilutif": False, "passerelle_moriarty": True},
}


def diagnostiquer(montant: float, horizon: str, dilutif_ok: bool, urgence_jours: int, projet_rd: bool, projet_industriel: bool) -> dict:
    """Filtre les solutions et propose top 3."""
    solutions_eligibles = []
    aides_publiques_eligibles = False

    for nom, sol in SOLUTIONS.items():
        # Filtre horizon
        if sol["horizon"] != horizon and sol["horizon"] != "permanent":
            continue
        # Filtre montant
        if montant > sol["max_montant"]:
            continue
        # Filtre dilutif
        if not dilutif_ok and sol["dilutif"]:
            continue
        # Filtre urgence
        if urgence_jours < sol["delai_jours"]:
            continue
        # Filtre passerelle Moriarty (aides publiques uniquement si projet R&D ou industriel)
        if sol.get("passerelle_moriarty"):
            if not (projet_rd or projet_industriel):
                continue
            aides_publiques_eligibles = True

        solutions_eligibles.append({"nom": nom, **sol})

    # Tri par coût croissant
    solutions_eligibles.sort(key=lambda s: s["cout_pct"])

    return {
        "solutions_eligibles_count": len(solutions_eligibles),
        "top_3": solutions_eligibles[:3],
        "aides_publiques_eligibles": aides_publiques_eligibles,
        "moriarty_cta_recommande": aides_publiques_eligibles,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnostic financement")
    parser.add_argument("--montant", type=float, required=True)
    parser.add_argument("--horizon", choices=["ct", "mlt", "lt"], required=True,
                        help="ct (< 1 an), mlt (1-7 ans), lt (> 7 ans)")
    parser.add_argument("--dilutif-ok", action="store_true", help="Accepte des solutions dilutives")
    parser.add_argument("--urgence-jours", type=int, default=180, help="Délai disponible en jours")
    parser.add_argument("--projet-rd", action="store_true", help="Projet R&D significatif")
    parser.add_argument("--projet-industriel", action="store_true", help="CAPEX industriel ou transition énergétique")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    result = diagnostiquer(
        args.montant, args.horizon, args.dilutif_ok, args.urgence_jours,
        args.projet_rd, args.projet_industriel,
    )

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Diagnostic financement : {args.output}", file=sys.stderr)
        if result["moriarty_cta_recommande"]:
            print("💡 Aides publiques éligibles → CTA Moriarty recommandé", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
