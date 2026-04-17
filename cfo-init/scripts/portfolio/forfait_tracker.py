#!/usr/bin/env python3
"""
forfait_tracker.py

Suivi des forfaits vs heures consommees par mission client.
Lit private/companies/<siren>/forfait.json avec les heures forfaitisees
et private/companies/<siren>/temps-passes.json avec les temps saisis.

Schema forfait.json :
  { "forfait_heures": 40, "tjm_reference": 680, "annee": 2026 }

Schema temps-passes.json :
  { "saisies": [ { "date": "2026-04-01", "collaborateur": "X", "heures": 3.5, "tache": "..." } ] }

Usage :
  python3 cfo-init/scripts/portfolio/forfait_tracker.py
  python3 cfo-init/scripts/portfolio/forfait_tracker.py --siren X --detailed
  python3 cfo-init/scripts/portfolio/forfait_tracker.py --json

Alertes :
  - 70-90 % consomme : jaune (vigilance)
  - 90-100 % consomme : orange (communiquer au client)
  - > 100 % consomme : rouge (renegocier ou refacturer)

Exit codes :
  0 = OK
  1 = index.json absent
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"


def load_index() -> dict:
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent", file=sys.stderr)
        sys.exit(1)
    return json.loads(index_path.read_text(encoding="utf-8"))


def load_forfait(siren: str) -> dict | None:
    path = PRIVATE / "companies" / siren / "forfait.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_temps(siren: str) -> list:
    path = PRIVATE / "companies" / siren / "temps-passes.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("saisies", [])


def compute_statut(pct: float) -> str:
    if pct >= 100:
        return "depassement"
    if pct >= 90:
        return "limite_atteinte"
    if pct >= 70:
        return "vigilance"
    return "ok"


def compute_for_client(siren: str) -> dict | None:
    forfait = load_forfait(siren)
    if forfait is None:
        return None

    heures_forfait = float(forfait.get("forfait_heures", 0))
    annee = forfait.get("annee", str(date.today().year))
    saisies = load_temps(siren)

    # Filtrer par annee
    saisies_annee = [s for s in saisies if str(s.get("date", "")).startswith(str(annee))]
    heures_consommees = sum(float(s.get("heures", 0)) for s in saisies_annee)

    if heures_forfait == 0:
        pct = 0.0
    else:
        pct = (heures_consommees / heures_forfait) * 100

    tjm = float(forfait.get("tjm_reference", 0))
    # TJM base 7h, donc cout horaire = TJM / 7
    cout_horaire = tjm / 7 if tjm else 0
    depassement_heures = max(0, heures_consommees - heures_forfait)
    cout_depassement = depassement_heures * cout_horaire

    return {
        "annee": annee,
        "forfait_heures": heures_forfait,
        "heures_consommees": round(heures_consommees, 1),
        "pct_consomme": round(pct, 1),
        "depassement_heures": round(depassement_heures, 1),
        "cout_depassement_eur": round(cout_depassement, 0),
        "statut": compute_statut(pct),
        "nb_saisies": len(saisies_annee),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Suivi forfaits vs heures consommees")
    parser.add_argument("--siren", help="Limite a un seul client")
    parser.add_argument("--detailed", action="store_true", help="Detail des saisies")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--private-dir", type=Path, default=None,
                        help="Repertoire prive (default: <repo>/private)")
    args = parser.parse_args()
    global PRIVATE
    if args.private_dir is not None:
        PRIVATE = args.private_dir

    index = load_index()
    if args.siren:
        clients = [c for c in index.get("clients", []) if c.get("siren") == args.siren]
    else:
        clients = [c for c in index.get("clients", []) if c.get("status") == "actif"]

    output = {"clients": [], "totaux": {"depassements_count": 0, "cout_total_depassement_eur": 0.0}}
    sans_forfait = []

    for c in clients:
        siren = c.get("siren", "?")
        result = compute_for_client(siren)
        if result is None:
            sans_forfait.append(c)
            continue
        result["siren"] = siren
        result["denomination"] = c.get("denomination", "?")
        result["mission_type"] = c.get("mission_type", "?")
        output["clients"].append(result)
        if result["statut"] == "depassement":
            output["totaux"]["depassements_count"] += 1
            output["totaux"]["cout_total_depassement_eur"] += result["cout_depassement_eur"]

    if args.json:
        output["sans_forfait"] = [c.get("siren") for c in sans_forfait]
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    # Affichage texte
    print("Suivi forfaits vs heures consommees")
    print(f"Clients avec forfait : {len(output['clients'])} | Sans forfait : {len(sans_forfait)}")
    print()

    if output["clients"]:
        header = f"{'Client':<28} {'Mission':<18} {'Forfait':>8} {'Conso':>8} {'%':>6} {'Statut':<16}"
        print(header)
        print("-" * len(header))
        for c in sorted(output["clients"], key=lambda x: -x["pct_consomme"]):
            denom = c["denomination"][:26]
            row = (
                f"{denom:<28} "
                f"{c['mission_type']:<18} "
                f"{c['forfait_heures']:>8.0f} "
                f"{c['heures_consommees']:>8.1f} "
                f"{c['pct_consomme']:>5.1f}% "
                f"{c['statut']:<16}"
            )
            print(row)

    tot = output["totaux"]
    if tot["depassements_count"] > 0:
        print()
        print("ALERTES :")
        print(f"  - {tot['depassements_count']} mission(s) en depassement forfait")
        print(f"  - Cout theorique des depassements : {tot['cout_total_depassement_eur']:.0f} EUR")
        print("  -> Renegocier les forfaits ou facturer en sus (avenant lettre de mission)")

    if sans_forfait:
        print()
        print(f"Clients sans forfait.json ({len(sans_forfait)}) :")
        for c in sans_forfait[:5]:
            print(f"  - {c.get('denomination', '?')} (SIREN {c.get('siren', '?')})")
        if len(sans_forfait) > 5:
            print(f"  ... et {len(sans_forfait) - 5} autres")

    if args.detailed and args.siren:
        saisies = load_temps(args.siren)
        if saisies:
            print()
            print(f"Saisies de temps pour {args.siren} ({len(saisies)}) :")
            for s in sorted(saisies, key=lambda x: x.get("date", "")):
                print(f"  {s.get('date', '?')} - {s.get('collaborateur', '?')} - {s.get('heures', 0)}h - {s.get('tache', '?')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
