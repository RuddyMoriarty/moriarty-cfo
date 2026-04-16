#!/usr/bin/env python3
"""
check_dossier.py

Verifie la completude du dossier d'un client EC en fonction de son type de mission.
Compare les pieces presentes (declarees dans private/companies/<siren>/pieces.json)
avec la liste attendue (data/pieces-dossier.json).

Usage :
  python3 cfo-init/scripts/portfolio/check_dossier.py --siren 552120222
  python3 cfo-init/scripts/portfolio/check_dossier.py --siren 552120222 --json

Exit codes :
  0 = OK ou dossier incomplet (utiliser --strict pour 1 si incomplet)
  1 = erreur (SIREN introuvable, catalogue absent)
  2 = --strict et dossier incomplet
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
CATALOG_PATH = ROOT / "data" / "pieces-dossier.json"


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        print(f"ERREUR: catalogue introuvable : {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_client_entry(siren: str) -> dict:
    """Charge l'entree client depuis l'index."""
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent. Lancez init_cabinet.py d'abord.", file=sys.stderr)
        sys.exit(1)
    index = json.loads(index_path.read_text(encoding="utf-8"))
    for c in index.get("clients", []):
        if c.get("siren") == siren:
            return c
    print(f"ERREUR: client SIREN {siren} introuvable dans l'index", file=sys.stderr)
    sys.exit(1)


def load_pieces_recues(siren: str) -> dict:
    """Charge private/companies/<siren>/pieces.json si existe, sinon vide."""
    path = PRIVATE / "companies" / siren / "pieces.json"
    if not path.exists():
        return {"pieces_recues": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def check(siren: str, strict: bool, as_json: bool) -> int:
    catalog = load_catalog()
    client = load_client_entry(siren)
    mission = client.get("mission_type", "presentation")
    denom = client.get("denomination", "?")

    expected = catalog.get("pieces_par_mission", {}).get(mission, [])
    if not expected:
        print(f"AVERTISSEMENT: aucune piece catalog pour mission {mission}", file=sys.stderr)

    received = load_pieces_recues(siren).get("pieces_recues", {})

    missing_obligatoire = []
    missing_facultatif = []
    received_ok = []

    for piece in expected:
        pid = piece["id"]
        if received.get(pid, {}).get("recu") is True:
            received_ok.append(piece)
        elif piece["obligatoire"]:
            missing_obligatoire.append(piece)
        else:
            missing_facultatif.append(piece)

    complet = len(missing_obligatoire) == 0

    if as_json:
        print(json.dumps({
            "siren": siren,
            "denomination": denom,
            "mission_type": mission,
            "total_attendues": len(expected),
            "recues": len(received_ok),
            "manquantes_obligatoires": [p["id"] for p in missing_obligatoire],
            "manquantes_facultatives": [p["id"] for p in missing_facultatif],
            "dossier_complet": complet,
            "checked_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        }, ensure_ascii=False, indent=2))
    else:
        status = "COMPLET" if complet else "INCOMPLET"
        print(f"Dossier {denom} (SIREN {siren}) - Mission: {mission}")
        print(f"Status : {status}")
        print(f"Pieces recues : {len(received_ok)}/{len(expected)}")
        print()
        if missing_obligatoire:
            print(f"Pieces obligatoires manquantes ({len(missing_obligatoire)}) :")
            for p in missing_obligatoire:
                print(f"  - {p['label']}")
        if missing_facultatif:
            print(f"\nPieces facultatives manquantes ({len(missing_facultatif)}) :")
            for p in missing_facultatif:
                print(f"  - {p['label']}")
        if received_ok and not missing_obligatoire:
            print("Toutes les pieces obligatoires sont recues.")

    if strict and not complet:
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifie la completude d'un dossier client")
    parser.add_argument("--siren", required=True)
    parser.add_argument("--strict", action="store_true", help="Exit 2 si dossier incomplet")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    args = parser.parse_args()
    return check(args.siren, args.strict, args.json)


if __name__ == "__main__":
    sys.exit(main())
