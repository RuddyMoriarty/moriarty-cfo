#!/usr/bin/env python3
"""
mark_routine.py

Marque une routine comme done ou failed apres execution par le harnais.

Usage :
  python3 cfo-init/scripts/routines/mark_routine.py --siren 552120222 --routine cloture-mensuelle --state done
  python3 cfo-init/scripts/routines/mark_routine.py --siren 552120222 --routine cloture-mensuelle --state failed
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
MAX_RETRIES = 3


def main() -> int:
    parser = argparse.ArgumentParser(description="Marque une routine done ou failed")
    parser.add_argument("--siren", required=True)
    parser.add_argument("--routine", required=True, help="ID de la routine")
    parser.add_argument("--state", required=True, choices=["done", "failed"])
    parser.add_argument("--reason", default="", help="Raison de l'echec (si failed)")
    args = parser.parse_args()

    routines_path = PRIVATE / "companies" / args.siren / "routines.json"
    if not routines_path.exists():
        print(f"ERREUR: routines.json introuvable pour SIREN {args.siren}", file=sys.stderr)
        return 1

    data = json.loads(routines_path.read_text(encoding="utf-8"))
    now_iso = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    found = False

    for r in data.get("routines", []):
        if r.get("id") == args.routine:
            found = True
            r["state"] = args.state
            r["last_state_change"] = now_iso

            if args.state == "failed":
                r["retry_count"] = r.get("retry_count", 0) + 1
                r["last_error"] = args.reason or "erreur non specifiee"
                retry = r["retry_count"]
                if retry < MAX_RETRIES:
                    print(f"FAILED: {args.routine} (retry {retry}/{MAX_RETRIES})")
                    print(f"Relancer : python3 cfo-init/scripts/routines/schedule_routines.py --siren {args.siren} --refresh")
                else:
                    r["state"] = "abandoned"
                    print(f"ABANDONED: {args.routine} apres {MAX_RETRIES} tentatives")
                    print("Intervention manuelle requise. Verifier les donnees sources.")
            else:
                r["retry_count"] = 0
                r.pop("last_error", None)
                print(f"DONE: {args.routine}")
            break

    if not found:
        print(f"ERREUR: routine {args.routine} introuvable pour SIREN {args.siren}", file=sys.stderr)
        return 1

    routines_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
