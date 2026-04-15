#!/usr/bin/env python3
"""Test helper: valide le catalogue routines-catalog.json."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "data" / "routines-catalog.json"


def main() -> int:
    if not CATALOG.exists():
        print(f"ERREUR: catalogue introuvable : {CATALOG}")
        return 1
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERREUR: catalogue JSON invalide : {e}")
        return 1

    routines = data.get("routines", [])
    required_fields = {"id", "name", "description", "category", "frequency", "trigger", "conditions", "skills_chain", "artefact"}

    ids = set()
    for r in routines:
        missing = required_fields - r.keys()
        if missing:
            print(f"ERREUR: routine {r.get('id', '?')} sans champs {missing}")
            return 1
        if r["id"] in ids:
            print(f"ERREUR: routine id duplicated : {r['id']}")
            return 1
        ids.add(r["id"])

    print(f"catalog_valid=true routines_count={len(routines)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
