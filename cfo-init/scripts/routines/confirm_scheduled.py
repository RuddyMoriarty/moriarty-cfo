#!/usr/bin/env python3
"""
confirm_scheduled.py

Met a jour l'etat des routines dans routines-index.json apres que le harnais
Claude Code a programme les scheduled-tasks via MCP.

Le workflow type :
  1. schedule_routines.py genere les payloads (state = pending_schedule)
  2. Claude Code appelle mcp__scheduled-tasks__create_scheduled_task pour chaque
  3. Ce script confirme le succes en passant l'etat en "scheduled"

Usage :
  python3 cfo-init/scripts/routines/confirm_scheduled.py --siren 552120222
  python3 cfo-init/scripts/routines/confirm_scheduled.py --siren 552120222 --task-id cfo-cloture-mensuelle-552120222-2026-05
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"


def load_index() -> dict:
    index_path = PRIVATE / "routines-index.json"
    if not index_path.exists():
        return {}
    return json.loads(index_path.read_text(encoding="utf-8"))


def save_index(index: dict) -> None:
    index_path = PRIVATE / "routines-index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def confirm(siren: str, task_id: str | None = None) -> int:
    index = load_index()
    updated = 0

    for tid, entry in index.items():
        if entry.get("siren") != siren:
            continue
        if task_id and tid != task_id:
            continue
        if entry.get("state") == "pending_schedule":
            entry["state"] = "scheduled"
            updated += 1

    if updated == 0:
        print(f"Aucune routine pending_schedule trouvee pour SIREN {siren}", file=sys.stderr)
        return 1

    save_index(index)
    print(f"OK: {updated} routine(s) confirmee(s) en 'scheduled' pour SIREN {siren}")

    # Mettre a jour aussi le routines.json de l'entite
    routines_path = PRIVATE / "companies" / siren / "routines.json"
    if routines_path.exists():
        routines = json.loads(routines_path.read_text(encoding="utf-8"))
        for r in routines.get("routines", []):
            if r.get("state") == "pending_schedule":
                if task_id is None or r.get("task_id") == task_id:
                    r["state"] = "scheduled"
        routines_path.write_text(json.dumps(routines, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Confirme la programmation des routines apres succes MCP")
    parser.add_argument("--siren", required=True, help="SIREN de l'entite")
    parser.add_argument("--task-id", default=None, help="Confirmer un seul task_id (sinon tous)")
    args = parser.parse_args()
    return confirm(args.siren, args.task_id)


if __name__ == "__main__":
    sys.exit(main())
