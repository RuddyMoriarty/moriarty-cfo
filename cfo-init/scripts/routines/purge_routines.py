#!/usr/bin/env python3
"""
purge_routines.py

Nettoyage des routines programmees. Produit un JSON de task_ids a supprimer
cote scheduled-tasks MCP par le harnais, retire les entrees de routines-index.json,
et marque les routines concernees en state=purged dans routines.json.

Modes :
  --siren SIREN --routine ID        Supprime une routine specifique pour une entite
  --siren SIREN --all                Supprime toutes les routines pour une entite
  --all-sirens --force               Supprime tout le repo (confirmation obligatoire)
  --suspend                          Passe notifications_active a false dans profile.json
                                     (garde les programmations, arrete les notifs)

Usage :
  python3 cfo-init/scripts/routines/purge_routines.py --siren 552120222 --routine cloture-mensuelle
  python3 cfo-init/scripts/routines/purge_routines.py --siren 552120222 --all
  python3 cfo-init/scripts/routines/purge_routines.py --all-sirens --force
  python3 cfo-init/scripts/routines/purge_routines.py --suspend

Output :
  JSON sur stdout (ou dans --output) listant les task_ids MCP a supprimer.
  Le harnais Claude Code relaie ces IDs vers l'outil MCP approprie.

Exit codes :
  0 = OK
  1 = Arguments incoherents ou SIREN introuvable
  2 = Erreur index ou ecriture
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
INDEX_PATH = PRIVATE / "routines-index.json"
PROFILE_PATH = PRIVATE / "profile.json"
LOG_PATH = PRIVATE / "routines.log"


def log(action: str, details: str) -> None:
    PRIVATE.mkdir(exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} | {action} | {details}\n")


def load_index() -> dict:
    if not INDEX_PATH.exists():
        return {"_meta": {"version": "0.1.2"}, "tasks": {}}
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERREUR: routines-index.json invalide : {e}", file=sys.stderr)
        sys.exit(2)


def save_index(index: dict) -> None:
    PRIVATE.mkdir(exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def load_routines(siren: str) -> dict | None:
    path = PRIVATE / "companies" / siren / "routines.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERREUR: routines.json invalide pour SIREN {siren} : {e}", file=sys.stderr)
        sys.exit(2)


def save_routines(siren: str, data: dict) -> None:
    path = PRIVATE / "companies" / siren / "routines.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def list_sirens_in_index(index: dict) -> list[str]:
    sirens = set()
    for task_info in index.get("tasks", {}).values():
        s = task_info.get("siren")
        if s:
            sirens.add(s)
    return sorted(sirens)


def purge_specific_routine(siren: str, routine_id: str, index: dict) -> list[str]:
    """Purge une routine specifique. Retourne la liste de task_ids supprimes."""
    routines_data = load_routines(siren)
    if routines_data is None:
        print(f"ERREUR: routines.json introuvable pour SIREN {siren}", file=sys.stderr)
        sys.exit(1)

    removed_task_ids = []
    updated_routines = []

    for r in routines_data.get("routines", []):
        if r.get("id") == routine_id:
            task_id = r.get("task_id")
            if task_id:
                removed_task_ids.append(task_id)
                if task_id in index.get("tasks", {}):
                    del index["tasks"][task_id]
            r_updated = dict(r)
            r_updated["state"] = "purged"
            r_updated["task_id"] = None
            updated_routines.append(r_updated)
        else:
            updated_routines.append(r)

    routines_data["routines"] = updated_routines
    save_routines(siren, routines_data)

    return removed_task_ids


def purge_all_routines_for_siren(siren: str, index: dict) -> list[str]:
    """Purge toutes les routines d'une entite."""
    routines_data = load_routines(siren)
    if routines_data is None:
        print(f"ERREUR: routines.json introuvable pour SIREN {siren}", file=sys.stderr)
        sys.exit(1)

    removed_task_ids = []

    for r in routines_data.get("routines", []):
        task_id = r.get("task_id")
        if task_id:
            removed_task_ids.append(task_id)
            if task_id in index.get("tasks", {}):
                del index["tasks"][task_id]

    # Supprime totalement l'entree routines.json
    path = PRIVATE / "companies" / siren / "routines.json"
    if path.exists():
        path.unlink()

    return removed_task_ids


def purge_all_sirens(index: dict) -> dict[str, list[str]]:
    """Purge tout le repo : toutes les entites, toutes leurs routines."""
    removed_by_siren = {}
    sirens = list_sirens_in_index(index)
    for siren in sirens:
        removed_by_siren[siren] = purge_all_routines_for_siren(siren, index)
    # Vide aussi l'index resident
    index["tasks"] = {}
    return removed_by_siren


def suspend_notifications() -> None:
    """Passe notifications_active a false dans profile.json, garde les programmations."""
    if not PROFILE_PATH.exists():
        profile = {"notifications_level": 1, "notifications_active": False}
    else:
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        profile["notifications_active"] = False
    PRIVATE.mkdir(exist_ok=True)
    PROFILE_PATH.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Nettoyage des routines programmees.")
    parser.add_argument("--siren", help="SIREN 9 chiffres")
    parser.add_argument("--routine", help="ID de la routine a purger (avec --siren)")
    parser.add_argument("--all", action="store_true", help="Purge toutes les routines du SIREN")
    parser.add_argument("--all-sirens", action="store_true", help="Purge toutes les entites du repo")
    parser.add_argument("--force", action="store_true", help="Confirmation requise pour --all-sirens")
    parser.add_argument("--suspend", action="store_true",
                        help="notifications_active=false, garde les programmations")
    parser.add_argument("--output", default=None, help="Fichier JSON de sortie (defaut: stdout)")
    args = parser.parse_args()

    # Mode suspend : met en pause sans supprimer
    if args.suspend:
        suspend_notifications()
        log("suspend", "notifications_active=false")
        output = {
            "action": "suspend",
            "message": "Notifications suspendues. Les routines restent programmees.",
            "task_ids_to_delete": [],
        }
        if args.output:
            Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Suspend applique. Output ecrit dans {args.output}")
        else:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    # Mode all-sirens : purge tout avec confirmation
    if args.all_sirens:
        if not args.force:
            print("ERREUR: --all-sirens requiert --force pour confirmer la purge complete.", file=sys.stderr)
            sys.exit(1)
        index = load_index()
        removed = purge_all_sirens(index)
        save_index(index)
        all_task_ids = [tid for tids in removed.values() for tid in tids]
        log("purge_all", f"total task_ids supprimes={len(all_task_ids)} | sirens={len(removed)}")
        output = {
            "action": "purge_all_sirens",
            "sirens_purged": list(removed.keys()),
            "task_ids_to_delete": all_task_ids,
            "count_by_siren": {s: len(tids) for s, tids in removed.items()},
            "instructions_to_harness": (
                "Pour chaque task_id ci-dessus, le harnais Claude Code doit appeler "
                "mcp__scheduled-tasks__delete_scheduled_task ou CronDelete selon la source "
                "de programmation. L'index routines-index.json a deja ete vide."
            ),
        }
        if args.output:
            Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Purge totale. Output ecrit dans {args.output}")
        else:
            print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    # Les autres modes requierent --siren
    if not args.siren:
        print("ERREUR: --siren obligatoire sauf avec --all-sirens ou --suspend.", file=sys.stderr)
        sys.exit(1)

    index = load_index()

    if args.routine:
        # Purge d'une routine specifique
        task_ids = purge_specific_routine(args.siren, args.routine, index)
        save_index(index)
        log("purge_routine", f"siren={args.siren} | routine={args.routine} | task_ids={len(task_ids)}")
        output = {
            "action": "purge_routine",
            "siren": args.siren,
            "routine": args.routine,
            "task_ids_to_delete": task_ids,
            "instructions_to_harness": (
                "Pour chaque task_id ci-dessus, le harnais Claude Code doit appeler "
                "mcp__scheduled-tasks__delete_scheduled_task. L'index et routines.json "
                "ont ete mis a jour (state=purged)."
            ),
        }
    elif args.all:
        # Purge toutes les routines de l'entite
        task_ids = purge_all_routines_for_siren(args.siren, index)
        save_index(index)
        log("purge_all_entity", f"siren={args.siren} | task_ids={len(task_ids)}")
        output = {
            "action": "purge_all_for_siren",
            "siren": args.siren,
            "task_ids_to_delete": task_ids,
            "instructions_to_harness": (
                "Pour chaque task_id ci-dessus, le harnais Claude Code doit appeler "
                "mcp__scheduled-tasks__delete_scheduled_task. routines.json a ete supprime "
                "pour cette entite, et l'index a ete mis a jour."
            ),
        }
    else:
        print("ERREUR: avec --siren, preciser --routine ID ou --all.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Purge executee. Output ecrit dans {args.output}")
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
