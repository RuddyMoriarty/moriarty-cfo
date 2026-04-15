#!/usr/bin/env python3
"""
list_routines.py

Liste les routines actives d'une entite. Mode --detailed pour voir les skills
chains et les metadata completes.

Usage :
  python3 cfo-init/scripts/routines/list_routines.py --siren 552120222
  python3 cfo-init/scripts/routines/list_routines.py --siren 552120222 --detailed

Exit codes :
  0 = OK
  1 = SIREN ou routines.json introuvable
  2 = Fichier corrompu
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
LOG_PATH = PRIVATE / "routines.log"


def log(action: str, details: str) -> None:
    PRIVATE.mkdir(exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} | {action} | {details}\n")


def load_routines_for_siren(siren: str) -> dict:
    path = PRIVATE / "companies" / siren / "routines.json"
    if not path.exists():
        print(f"ERREUR: routines.json introuvable pour SIREN {siren}.", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERREUR: routines.json invalide : {e}", file=sys.stderr)
        sys.exit(2)


def load_company(siren: str) -> dict:
    multi = PRIVATE / "companies" / siren / "company.json"
    mono = PRIVATE / "company.json"
    if multi.exists():
        return json.loads(multi.read_text(encoding="utf-8"))
    if mono.exists():
        d = json.loads(mono.read_text(encoding="utf-8"))
        if d.get("siren") == siren:
            return d
    return {"denomination": siren}


def load_profile() -> dict:
    profile_path = PRIVATE / "profile.json"
    if not profile_path.exists():
        return {"notifications_level": 1}
    return json.loads(profile_path.read_text(encoding="utf-8"))


def next_occurrence_display(routine: dict) -> str:
    """Formate une string lisible pour la prochaine occurrence."""
    fire_at = routine.get("fire_at_absolute")
    if fire_at:
        try:
            d = dt.datetime.fromisoformat(fire_at.replace("Z", "+00:00"))
            return d.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return fire_at
    cron = routine.get("cron_expression")
    if cron:
        return f"cron({cron})"
    return "n/a"


def truncate(s: str, length: int) -> str:
    if len(s) <= length:
        return s.ljust(length)
    return s[: length - 1] + ".."


def print_routines_compact(routines_data: dict, company: dict, profile: dict, siren: str) -> None:
    routines = routines_data.get("routines", [])
    denom = company.get("denomination", siren)
    level = profile.get("notifications_level", 1)
    count = len(routines)

    print(f"Routines actives pour {denom} (SIREN {siren})")
    print(f"Niveau: {level} | Actives: {count}")
    print()
    if count == 0:
        print("(aucune routine)")
        return

    # Largeurs fixes pour un tableau lisible
    print(f"{'ID':<30} {'Frequence':<10} {'Prochaine occurrence':<25} {'Etat':<10} {'Dernier run':<20}")
    print("-" * 100)

    for r in sorted(routines, key=lambda x: (x.get("frequency", ""), x.get("id", ""))):
        rid = truncate(r.get("id", "?"), 30)
        freq = truncate(r.get("frequency", "?"), 10)
        next_occ = truncate(next_occurrence_display(r), 25)
        state = truncate(r.get("state", "pending"), 10)
        last_run = r.get("last_run")
        if last_run:
            last_run_str = last_run[:10]
        else:
            last_run_str = "(jamais)"
        last_run_str = truncate(last_run_str, 20)
        print(f"{rid} {freq} {next_occ} {state} {last_run_str}")


def print_routines_detailed(routines_data: dict, company: dict, profile: dict, siren: str) -> None:
    routines = routines_data.get("routines", [])
    denom = company.get("denomination", siren)
    level = profile.get("notifications_level", 1)

    print(f"Routines actives (detaille) pour {denom} (SIREN {siren})")
    print(f"Niveau notifications: {level} | Actives: {len(routines)}")
    print()

    if not routines:
        print("(aucune routine)")
        return

    for i, r in enumerate(sorted(routines, key=lambda x: (x.get("frequency", ""), x.get("id", ""))), 1):
        print(f"[{i}] {r.get('id', '?')}")
        print(f"    Nom        : {r.get('name', '?')}")
        print(f"    Description: {r.get('description', '?')}")
        print(f"    Categorie  : {r.get('category', '?')}")
        print(f"    Frequence  : {r.get('frequency', '?')}")
        print(f"    Skills     : {', '.join(r.get('skills_chain', []))}")
        artefact = r.get("artefact", {})
        print(f"    Artefact   : {artefact.get('type', '?')} | {artefact.get('path_pattern', '?')}")
        print(f"    Cron       : {r.get('cron_expression') or '(non cron)'}")
        print(f"    Fire_at    : {r.get('fire_at_absolute') or '(cron)'}")
        print(f"    Task id    : {r.get('task_id') or '(non programme)'}")
        print(f"    Etat       : {r.get('state', 'pending')}")
        print(f"    Dernier run: {r.get('last_run') or '(jamais)'}")
        artefact_path = r.get("last_artefact")
        if artefact_path:
            print(f"    Dernier art: {artefact_path}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Liste les routines actives d'une entite.")
    parser.add_argument("--siren", required=True, help="SIREN 9 chiffres")
    parser.add_argument("--detailed", action="store_true",
                        help="Affiche le detail (skills_chain, type artefact, task_id)")
    args = parser.parse_args()

    routines_data = load_routines_for_siren(args.siren)
    company = load_company(args.siren)
    profile = load_profile()

    if args.detailed:
        print_routines_detailed(routines_data, company, profile, args.siren)
    else:
        print_routines_compact(routines_data, company, profile, args.siren)

    log("list", f"siren={args.siren} | mode={'detailed' if args.detailed else 'compact'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
