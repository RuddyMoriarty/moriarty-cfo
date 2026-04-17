#!/usr/bin/env python3
"""
extract_variances.py, identifie automatiquement les top variances budget vs réel.

Input : budget (CSV compte,montant) + réel (CSV compte,montant)
Output : top N variances > seuil (€ et %)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def load_csv_as_dict(path: Path) -> dict[str, float]:
    """Charge un CSV au format compte,montant en dict.

    Leve ValueError si aucune colonne reconnue pour le compte ou le montant.
    """
    result = {}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        has_compte = any(c in cols for c in ("compte", "CompteNum", "poste"))
        has_montant = "montant" in cols
        if not has_compte or not has_montant:
            raise ValueError(
                f"CSV {path.name} invalide : colonnes attendues 'compte'|'CompteNum'|'poste' "
                f"et 'montant'. Trouve : {cols}"
            )
        for row in reader:
            try:
                compte = row.get("compte") or row.get("CompteNum") or row.get("poste")
                montant = float((row.get("montant") or "0").replace(",", "."))
                result[compte] = montant
            except (ValueError, KeyError):
                continue
    return result


def compute_variances(budget: dict, reel: dict, seuil_eur: float, seuil_pct: float, top_n: int) -> list[dict]:
    """Compare budget vs réel et extrait les top variances significatives."""
    variances = []
    all_keys = set(budget.keys()) | set(reel.keys())

    for compte in all_keys:
        b = budget.get(compte, 0)
        r = reel.get(compte, 0)
        diff_eur = r - b
        diff_pct = (diff_eur / b * 100) if b != 0 else (100 if r != 0 else 0)

        if abs(diff_eur) >= seuil_eur or abs(diff_pct) >= seuil_pct:
            variances.append({
                "compte": compte,
                "budget": round(b, 0),
                "reel": round(r, 0),
                "ecart_eur": round(diff_eur, 0),
                "ecart_pct": round(diff_pct, 1),
                "direction": "favorable" if diff_eur < 0 and compte.startswith("6") else
                            "favorable" if diff_eur > 0 and compte.startswith("7") else
                            "defavorable",
            })

    # Trier par valeur absolue décroissante
    variances.sort(key=lambda v: abs(v["ecart_eur"]), reverse=True)
    return variances[:top_n]


def main() -> int:
    parser = argparse.ArgumentParser(description="Top variances budget vs réel")
    parser.add_argument("--budget", type=Path, required=True)
    parser.add_argument("--reel", type=Path, required=True)
    parser.add_argument("--seuil-eur", type=float, default=5000)
    parser.add_argument("--seuil-pct", type=float, default=5.0)
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    try:
        budget = load_csv_as_dict(args.budget)
        reel = load_csv_as_dict(args.reel)
    except FileNotFoundError as e:
        print(f"❌ Fichier introuvable : {e.filename}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    variances = compute_variances(budget, reel, args.seuil_eur, args.seuil_pct, args.top_n)

    result = {
        "_version": "0.1.0",
        "seuils": {"eur": args.seuil_eur, "pct": args.seuil_pct},
        "top_n": args.top_n,
        "variances": variances,
        "total_favorable_eur": round(sum(v["ecart_eur"] for v in variances if v["direction"] == "favorable"), 0),
        "total_defavorable_eur": round(sum(v["ecart_eur"] for v in variances if v["direction"] == "defavorable"), 0),
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ {len(variances)} variances identifiées > seuils", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
