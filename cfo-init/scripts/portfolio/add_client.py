#!/usr/bin/env python3
"""
add_client.py

Ajoute un client au portfolio du cabinet EC.
Cree private/companies/<siren>/company.json (minimal), ajoute l'entree dans
private/companies/index.json, et synchronise private/cabinet.json.

Usage :
  python3 cfo-init/scripts/portfolio/add_client.py \\
    --siren 552120222 --denomination "BOULANGERIE MARTIN SAS" \\
    --taille pe --secteur commerce --cloture 2026-12-31 \\
    [--mission presentation] [--referent "Jean Dupont"]

Exit codes :
  0 = OK
  1 = index.json absent (lancer init_cabinet.py d'abord)
  2 = arguments invalides
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"

VALID_TAILLES = {"tpe", "pe", "me", "eti", "ge"}
VALID_MISSIONS = {
    "presentation",
    "examen_limite",
    "audit_legal_cac",
    "social_paie",
    "juridique",
    "conseil_financier",
    "cir_cii",
    "aides_publiques",
    "m_and_a",
    "csrd_esrs",
}


def load_index() -> dict:
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent. Lancez init_cabinet.py d'abord.", file=sys.stderr)
        sys.exit(1)
    return json.loads(index_path.read_text(encoding="utf-8"))


def save_index(index: dict) -> None:
    index_path = PRIVATE / "companies" / "index.json"
    index["_meta"]["last_updated"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    index["_meta"]["count"] = len([c for c in index.get("clients", []) if c.get("status") == "actif"])
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sync_cabinet(siren: str) -> None:
    """Ajoute le SIREN dans cabinet.json > portfolio_clients.siren_list."""
    cabinet_path = PRIVATE / "cabinet.json"
    if not cabinet_path.exists():
        return
    cabinet = json.loads(cabinet_path.read_text(encoding="utf-8"))
    siren_list = cabinet.setdefault("portfolio_clients", {}).setdefault("siren_list", [])
    if siren not in siren_list:
        siren_list.append(siren)
        cabinet_path.write_text(
            json.dumps(cabinet, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Ajoute un client au portfolio EC")
    parser.add_argument("--siren", required=True, help="SIREN du client (9 chiffres)")
    parser.add_argument("--denomination", required=True)
    parser.add_argument("--taille", required=True, choices=sorted(VALID_TAILLES))
    parser.add_argument("--secteur", default="autre", help="Categorie sectorielle")
    parser.add_argument("--cloture", required=True, help="Date cloture YYYY-MM-DD")
    parser.add_argument("--mission", default="presentation", choices=sorted(VALID_MISSIONS))
    parser.add_argument("--referent", default="", help="Collaborateur referent")
    args = parser.parse_args()

    if len(args.siren) != 9 or not args.siren.isdigit():
        print("ERREUR: SIREN doit contenir 9 chiffres", file=sys.stderr)
        return 2

    now_iso = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    today = now_iso[:10]

    # 1. company.json minimal
    company_dir = PRIVATE / "companies" / args.siren
    company_dir.mkdir(parents=True, exist_ok=True)
    company_path = company_dir / "company.json"

    if not company_path.exists():
        company = {
            "siren": args.siren,
            "denomination": args.denomination,
            "exercice_comptable": {
                "date_cloture": args.cloture,
                "duree_mois": 12,
            },
            "classification": {
                "taille": args.taille,
                "secteur_category": args.secteur,
                "effectif": 0,
                "csrd_wave": "hors_scope",
                "is_startup": False,
                "has_investors": False,
                "has_covenants": False,
                "groupe": False,
                "seuil_audit": False,
            },
            "added_by_portfolio_at": now_iso,
        }
        company_path.write_text(
            json.dumps(company, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    # 2. index.json : ajouter ou mettre a jour
    index = load_index()
    clients = index.setdefault("clients", [])
    existing = next((c for c in clients if c.get("siren") == args.siren), None)

    entry = {
        "siren": args.siren,
        "denomination": args.denomination,
        "taille": args.taille,
        "status": "actif",
        "mission_type": args.mission,
        "referent": args.referent,
        "added_at": today,
        "routines_active": False,
        "next_deadline": None,
    }

    if existing:
        existing.update(entry)
        action = "mis a jour"
    else:
        clients.append(entry)
        action = "ajoute"

    save_index(index)

    # 3. sync cabinet.json
    sync_cabinet(args.siren)

    print(f"OK: client {action} ({args.denomination}, SIREN {args.siren})")
    print(f"  {company_path}")
    print(f"  mission={args.mission}, taille={args.taille}, cloture={args.cloture}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
