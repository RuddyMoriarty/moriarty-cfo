#!/usr/bin/env python3
"""
forecast_13w.py — génère une prévision de trésorerie 13 semaines.

Input : historique flux bancaires (CSV) + projections encaissements/décaissements
Output : HTML + CSV avec 13 colonnes, point bas identifié, alertes automatiques.

Usage :
  python3 forecast_13w.py \\
    --solde-initial 150000 \\
    --historique flux-90j.csv \\
    --projections proj-13w.csv \\
    --seuil-tension 50000 \\
    --output out/forecast-13w.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date, timedelta
from pathlib import Path


def parse_csv_if_exists(path: Path | None) -> list[dict]:
    if not path or not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_weeks(start: date, n: int = 13) -> list[dict]:
    """Génère les N semaines à partir du lundi de la semaine en cours."""
    days_to_monday = start.weekday()
    monday = start - timedelta(days=days_to_monday)
    weeks = []
    for i in range(n):
        w_start = monday + timedelta(days=i * 7)
        w_end = w_start + timedelta(days=6)
        weeks.append({
            "w": i + 1,
            "start": w_start.isoformat(),
            "end": w_end.isoformat(),
            "label": f"W{i+1} ({w_start.strftime('%d/%m')})",
            "encaissements": 0.0,
            "decaissements": 0.0,
            "flux_net": 0.0,
            "solde_initial": 0.0,
            "solde_final": 0.0,
        })
    return weeks


def allocate_to_weeks(projections: list[dict], weeks: list[dict]) -> None:
    """Affecte les montants projetés aux semaines concernées."""
    for p in projections:
        try:
            d = date.fromisoformat(p.get("date", ""))
            montant = float(p.get("montant", 0))
            type_flux = p.get("type", "").lower()
        except (ValueError, KeyError):
            continue

        for w in weeks:
            if date.fromisoformat(w["start"]) <= d <= date.fromisoformat(w["end"]):
                if type_flux in ("encaissement", "enc", "in"):
                    w["encaissements"] += montant
                else:
                    w["decaissements"] += montant
                break


def compute_soldes(weeks: list[dict], solde_initial: float) -> None:
    solde = solde_initial
    for w in weeks:
        w["solde_initial"] = solde
        w["flux_net"] = w["encaissements"] - w["decaissements"]
        w["solde_final"] = solde + w["flux_net"]
        solde = w["solde_final"]


def detect_alerts(weeks: list[dict], seuil_tension: float) -> dict:
    point_bas = min(weeks, key=lambda w: w["solde_final"])
    solde_min = point_bas["solde_final"]

    if solde_min < 0:
        niveau = "urgence_rouge"
        message = f"Solde NÉGATIF projeté à {point_bas['label']} : {solde_min:,.0f} €"
    elif solde_min < seuil_tension:
        niveau = "plan_action_orange"
        message = f"Solde sous seuil de tension ({seuil_tension:,.0f} €) à {point_bas['label']}"
    elif weeks[-1]["solde_final"] < weeks[0]["solde_initial"] * 0.6:
        niveau = "vigilance_jaune"
        message = "Tendance décroissante (-40% sur 13w)"
    else:
        niveau = "healthy_vert"
        message = "Trésorerie saine sur 13 semaines"

    return {
        "niveau": niveau,
        "message": message,
        "point_bas": point_bas,
        "solde_min": solde_min,
        "solde_initial": weeks[0]["solde_initial"],
        "solde_final_w13": weeks[-1]["solde_final"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Forecast trésorerie 13 semaines")
    parser.add_argument("--solde-initial", type=float, required=True)
    parser.add_argument("--historique", type=Path, default=None)
    parser.add_argument("--projections", type=Path, default=None,
                        help="CSV : date,type(enc|dec),montant,libelle")
    parser.add_argument("--seuil-tension", type=float, default=50000,
                        help="Seuil alerte orange (défaut : 50k€)")
    parser.add_argument("--date-depart", default=None, help="YYYY-MM-DD (défaut: aujourd'hui)")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    start = date.fromisoformat(args.date_depart) if args.date_depart else date.today()
    weeks = build_weeks(start, n=13)

    projections = parse_csv_if_exists(args.projections)
    allocate_to_weeks(projections, weeks)

    compute_soldes(weeks, args.solde_initial)
    alerts = detect_alerts(weeks, args.seuil_tension)

    result = {
        "_version": "0.1.0",
        "generated_at": date.today().isoformat(),
        "inputs": {
            "solde_initial": args.solde_initial,
            "seuil_tension": args.seuil_tension,
            "nb_projections": len(projections),
        },
        "weeks": weeks,
        "alerts": alerts,
        "summary": {
            "encaissements_totaux": round(sum(w["encaissements"] for w in weeks), 2),
            "decaissements_totaux": round(sum(w["decaissements"] for w in weeks), 2),
            "flux_net_total": round(sum(w["flux_net"] for w in weeks), 2),
        },
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Forecast 13w généré : {args.output}", file=sys.stderr)
        print(f"✓ Alert level : {alerts['niveau']}", file=sys.stderr)
        print(f"✓ Point bas : {alerts['point_bas']['label']} = {alerts['solde_min']:,.0f} €", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
