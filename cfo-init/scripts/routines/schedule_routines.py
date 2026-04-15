#!/usr/bin/env python3
"""
schedule_routines.py

Programme les routines d'une entité via scheduled-tasks (cross-session) ou
CronCreate (session courante).

Ce script ne peut PAS appeler directement les outils MCP (pas d'accès depuis
un script Python autonome). Son rôle est :

  1. Lire private/companies/<siren>/routines.json.
  2. Générer un JSON de payloads prêts à être passés aux outils MCP par le
     harnais Claude Code qui invoque ensuite chaque task via les outils MCP.
  3. Mettre à jour private/routines-index.json avec les task_ids programmés
     pour garantir l'idempotence et permettre la purge ultérieure.

Usage :
  python3 cfo-init/scripts/routines/schedule_routines.py --siren 552120222
  python3 cfo-init/scripts/routines/schedule_routines.py --siren 552120222 --output payloads.json
  python3 cfo-init/scripts/routines/schedule_routines.py --siren 552120222 --refresh

--refresh : recalcule les task_ids pour les routines qui sont passées ou qui
            ont un task_id absent. Réutilise les task_ids existants pour les
            routines encore actives (idempotence).

Exit codes :
  0 = OK
  1 = routines.json absent pour ce SIREN
  2 = Erreur d'écriture index
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
LOG_PATH = PRIVATE / "routines.log"


def log(action: str, details: str) -> None:
    PRIVATE.mkdir(exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} | {action} | {details}\n")


def load_routines(siren: str) -> dict:
    path = PRIVATE / "companies" / siren / "routines.json"
    if not path.exists():
        print(f"ERREUR: routines.json introuvable pour SIREN {siren}. Lance compute_entity_routines.py d'abord.", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def save_routines(siren: str, data: dict) -> None:
    path = PRIVATE / "companies" / siren / "routines.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_index() -> dict:
    if not INDEX_PATH.exists():
        return {"_meta": {"version": "0.1.2"}, "tasks": {}}
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def save_index(index: dict) -> None:
    PRIVATE.mkdir(exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def build_task_id(routine: dict, siren: str, now: dt.datetime) -> str:
    """Construit un task_id stable selon la fréquence de la routine."""
    freq = routine["frequency"]
    rid = routine["id"]

    if freq == "weekly":
        week = now.isocalendar().week
        return f"cfo-{rid}-{siren}-{now.year}-W{week:02d}"
    if freq == "monthly":
        return f"cfo-{rid}-{siren}-{now.year}{now.month:02d}"
    if freq == "quarterly":
        quarter = (now.month - 1) // 3 + 1
        return f"cfo-{rid}-{siren}-{now.year}-T{quarter}"
    if freq == "yearly":
        return f"cfo-{rid}-{siren}-{now.year}"
    return f"cfo-{rid}-{siren}"


def build_prompt(routine: dict, siren: str, denomination: str) -> str:
    """Construit le prompt qui sera enqueué au fire de la routine."""
    rid = routine["id"]
    name = routine["name"]
    chain = routine["skills_chain"]
    artefact = routine["artefact"]

    prompt = f"""Exécution routine "{rid}" pour {denomination} (SIREN {siren}).

Routine : {name}
Description : {routine.get('description', '')}

Étapes à exécuter dans l'ordre :
"""
    for i, skill in enumerate(chain, 1):
        prompt += f"  {i}. Invoque le skill {skill}.\n"
    prompt += f"  {len(chain) + 1}. Produis l'artefact de type {artefact['type']} au chemin {artefact['path_pattern']}.\n"
    prompt += f"  {len(chain) + 2}. Mets à jour private/companies/{siren}/routines.json (last_run, state=done).\n"
    prompt += f"  {len(chain) + 3}. Planifie la prochaine occurrence via schedule_routines.py --siren {siren} --refresh.\n"
    prompt += f"\n(Routine programmée par cfo-init, catalogue v0.1.2)"
    return prompt


def build_payloads(routines_data: dict, siren: str, denomination: str, existing_index: dict) -> list[dict]:
    """Produit les payloads scheduled-tasks à envoyer au harnais MCP."""
    now = dt.datetime.now()
    payloads = []
    updated_routines = []

    for routine in routines_data.get("routines", []):
        task_id = build_task_id(routine, siren, now)
        existing_task = existing_index.get("tasks", {}).get(task_id)

        # Idempotence : si déjà scheduled ET encore valide (future fire), skip
        if existing_task and existing_task.get("state") in ("scheduled", "firing"):
            # Already scheduled, reuse
            routine_updated = dict(routine)
            routine_updated["task_id"] = task_id
            routine_updated["state"] = existing_task.get("state", "scheduled")
            updated_routines.append(routine_updated)
            continue

        prompt = build_prompt(routine, siren, denomination)
        description = f"Routine {routine['name']} pour {denomination}"

        payload: dict = {
            "task_id": task_id,
            "description": description,
            "prompt": prompt,
            "notify_on_completion": False,
        }

        if routine.get("cron_expression"):
            payload["cron_expression"] = routine["cron_expression"]
        elif routine.get("fire_at_absolute"):
            payload["fire_at"] = routine["fire_at_absolute"]
        else:
            # Trigger non programmable, on marque en waiting
            routine_updated = dict(routine)
            routine_updated["state"] = "waiting"
            routine_updated["task_id"] = None
            updated_routines.append(routine_updated)
            continue

        payloads.append(payload)

        routine_updated = dict(routine)
        routine_updated["task_id"] = task_id
        routine_updated["state"] = "pending_schedule"
        updated_routines.append(routine_updated)

    routines_data["routines"] = updated_routines
    return payloads


def update_index(index: dict, payloads: list[dict], siren: str) -> dict:
    """Met à jour private/routines-index.json avec les nouveaux task_ids."""
    tasks = index.setdefault("tasks", {})
    now_iso = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    for p in payloads:
        tasks[p["task_id"]] = {
            "siren": siren,
            "state": "pending_schedule",
            "registered_at": now_iso,
            "cron_expression": p.get("cron_expression"),
            "fire_at": p.get("fire_at"),
        }
    index["_meta"]["last_updated"] = now_iso
    return index


def main() -> int:
    parser = argparse.ArgumentParser(description="Programme les routines d'une entité.")
    parser.add_argument("--siren", required=True, help="SIREN 9 chiffres")
    parser.add_argument("--output", default=None, help="Fichier de sortie JSON des payloads (default: stdout)")
    parser.add_argument("--refresh", action="store_true", help="Recalcule les task_ids et supprime les obsolètes")
    args = parser.parse_args()

    routines_data = load_routines(args.siren)

    company_path = PRIVATE / "companies" / args.siren / "company.json"
    mono_path = PRIVATE / "company.json"
    if company_path.exists():
        denomination = json.loads(company_path.read_text(encoding="utf-8")).get("denomination", args.siren)
    elif mono_path.exists():
        denomination = json.loads(mono_path.read_text(encoding="utf-8")).get("denomination", args.siren)
    else:
        denomination = args.siren

    index = load_index()
    payloads = build_payloads(routines_data, args.siren, denomination, index)
    index = update_index(index, payloads, args.siren)

    save_routines(args.siren, routines_data)
    try:
        save_index(index)
    except OSError as e:
        print(f"ERREUR: Impossible d'écrire l'index : {e}", file=sys.stderr)
        return 2

    output = {
        "siren": args.siren,
        "denomination": denomination,
        "count_payloads": len(payloads),
        "payloads": payloads,
        "instructions_to_harness": (
            "Pour chaque payload ci-dessus, le harnais Claude Code doit appeler "
            "mcp__scheduled-tasks__create_scheduled_task avec taskId, prompt, "
            "description, et cron_expression OU fire_at. L'index routines-index.json "
            "a déjà été marqué en pending_schedule. Après succès côté MCP, relire "
            "l'index et passer l'état de chaque task en 'scheduled'."
        ),
    }

    if args.output:
        Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Payloads écrits dans : {args.output}")
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))

    log("schedule", f"siren={args.siren} | {len(payloads)} payloads générés")
    return 0


if __name__ == "__main__":
    sys.exit(main())
