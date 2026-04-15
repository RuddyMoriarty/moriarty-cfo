#!/usr/bin/env python3
"""
profitability_analyzer.py, identifie top/bottom produits ou clients par rentabilité.

Input : CSV ventes détaillées (colonnes: client, produit, date, ca, cout_direct)
Output : top/bottom N + analyse Pareto
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path


def load_ventes(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows.append({
                    "client": row.get("client", "").strip(),
                    "produit": row.get("produit", "").strip(),
                    "canal": row.get("canal", "").strip(),
                    "date": row.get("date", ""),
                    "ca": float((row.get("ca") or "0").replace(",", ".")),
                    "cout_direct": float((row.get("cout_direct") or "0").replace(",", ".")),
                })
            except (ValueError, KeyError):
                continue
    return rows


def aggregate_by(ventes: list[dict], key: str) -> dict:
    """Agrège par dimension (client, produit, canal)."""
    agg = defaultdict(lambda: {"ca": 0.0, "cout": 0.0, "nb_transactions": 0})
    for v in ventes:
        k = v.get(key, "") or "inconnu"
        agg[k]["ca"] += v["ca"]
        agg[k]["cout"] += v["cout_direct"]
        agg[k]["nb_transactions"] += 1

    for k, data in agg.items():
        data["marge"] = round(data["ca"] - data["cout"], 2)
        data["marge_pct"] = round((data["marge"] / data["ca"] * 100), 1) if data["ca"] > 0 else 0
        data["ca"] = round(data["ca"], 2)
        data["cout"] = round(data["cout"], 2)

    return dict(agg)


def top_bottom(agg: dict, n: int, by: str = "marge") -> tuple[list, list]:
    """Renvoie top et bottom n selon le critère."""
    sorted_items = sorted(agg.items(), key=lambda x: x[1][by], reverse=True)
    top = [{"name": k, **v} for k, v in sorted_items[:n]]
    bottom = [{"name": k, **v} for k, v in sorted_items[-n:]]
    return top, bottom


def pareto_analysis(agg: dict) -> dict:
    """Analyse Pareto 20/80 sur le CA et la marge."""
    sorted_ca = sorted(agg.items(), key=lambda x: x[1]["ca"], reverse=True)
    sorted_marge = sorted(agg.items(), key=lambda x: x[1]["marge"], reverse=True)

    total_ca = sum(v["ca"] for _, v in sorted_ca)
    total_marge = sum(v["marge"] for _, v in sorted_marge)

    # Top 20% items
    n_top_20 = max(1, int(len(sorted_ca) * 0.2))

    top_20_ca = sum(v["ca"] for _, v in sorted_ca[:n_top_20])
    top_20_marge = sum(v["marge"] for _, v in sorted_marge[:n_top_20])

    return {
        "nb_items_total": len(agg),
        "nb_items_top_20pct": n_top_20,
        "part_ca_top_20pct": round(top_20_ca / total_ca * 100, 1) if total_ca > 0 else 0,
        "part_marge_top_20pct": round(top_20_marge / total_marge * 100, 1) if total_marge > 0 else 0,
        "total_ca": round(total_ca, 2),
        "total_marge": round(total_marge, 2),
    }


def identify_loss_makers(agg: dict) -> list[dict]:
    """Identifie les segments en perte (marge négative)."""
    return [{"name": k, **v} for k, v in agg.items() if v["marge"] < 0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyse rentabilité produit/client/canal")
    parser.add_argument("--ventes", type=Path, required=True,
                        help="CSV : client,produit,canal,date,ca,cout_direct")
    parser.add_argument("--dimension", choices=["client", "produit", "canal"], default="client")
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if not args.ventes.exists():
        print(f"❌ Fichier introuvable : {args.ventes}", file=sys.stderr)
        return 1

    ventes = load_ventes(args.ventes)
    if not ventes:
        print("⚠️ Aucune vente à analyser", file=sys.stderr)
        return 1

    agg = aggregate_by(ventes, args.dimension)
    top, bottom = top_bottom(agg, args.top_n, "marge")
    pareto = pareto_analysis(agg)
    losers = identify_loss_makers(agg)

    result = {
        "_version": "0.1.0",
        "dimension_analyse": args.dimension,
        "nb_transactions": len(ventes),
        "nb_items_uniques": len(agg),
        "summary": {
            "ca_total": pareto["total_ca"],
            "marge_total": pareto["total_marge"],
            "taux_marge_global_pct": round(pareto["total_marge"] / pareto["total_ca"] * 100, 1) if pareto["total_ca"] > 0 else 0,
        },
        "pareto": pareto,
        "top_n_par_marge": top,
        "bottom_n_par_marge": bottom,
        "loss_makers": losers,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Analyse rentabilité : {args.output}", file=sys.stderr)
        print(f"  → Top 20% = {pareto['part_marge_top_20pct']}% de la marge", file=sys.stderr)
        print(f"  → {len(losers)} segments en perte", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
