#!/usr/bin/env python3
"""
schedule_all.py

Itere sur tous les clients actifs du portfolio et programme leurs routines.
Appelle compute_entity_routines.py puis schedule_routines.py pour chaque SIREN.

Usage :
  python3 cfo-init/scripts/portfolio/schedule_all.py [--dry-run] [--level N]

Exit codes :
  0 = OK (meme si certains clients ont echoue, voir le resume)
  1 = index.json absent
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
COMPUTE = ROOT / "cfo-init" / "scripts" / "routines" / "compute_entity_routines.py"
SCHEDULE = ROOT / "cfo-init" / "scripts" / "routines" / "schedule_routines.py"


def load_index() -> dict:
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent. Lancez init_cabinet.py d'abord.", file=sys.stderr)
        sys.exit(1)
    return json.loads(index_path.read_text(encoding="utf-8"))


def run_compute(siren: str, level: int, dry_run: bool) -> tuple[bool, str]:
    args = [sys.executable, str(COMPUTE), "--siren", siren, "--level", str(level)]
    if dry_run:
        args.append("--dry-run")
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return proc.returncode == 0, proc.stderr[:200] if proc.returncode else ""
    except subprocess.TimeoutExpired:
        return False, "timeout"


def run_schedule(siren: str) -> tuple[bool, int]:
    """Retourne (succes, nombre de payloads generes)."""
    payloads_path = PRIVATE / "companies" / siren / "schedule-payloads.json"
    args = [sys.executable, str(SCHEDULE), "--siren", siren, "--output", str(payloads_path)]
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            return False, 0
        if payloads_path.exists():
            try:
                data = json.loads(payloads_path.read_text(encoding="utf-8"))
                return True, len(data.get("payloads", []))
            except json.JSONDecodeError:
                return True, 0
        return True, 0
    except subprocess.TimeoutExpired:
        return False, 0


def main() -> int:
    global PRIVATE
    parser = argparse.ArgumentParser(description="Programme les routines pour tout le portfolio")
    parser.add_argument("--dry-run", action="store_true", help="N'ecrit rien, affiche seulement")
    parser.add_argument("--level", type=int, default=2, help="Niveau de notifications (1-4)")
    parser.add_argument("--private-dir", type=Path, default=None,
                        help="Repertoire prive (default: <repo>/private)")
    args = parser.parse_args()
    if args.private_dir is not None:
        PRIVATE = args.private_dir

    index = load_index()
    clients = [c for c in index.get("clients", []) if c.get("status") == "actif"]

    if not clients:
        print("(aucun client actif dans le portfolio)")
        return 0

    print(f"Programmation des routines pour {len(clients)} client(s) actif(s)")
    if args.dry_run:
        print("Mode --dry-run : aucune ecriture, analyse uniquement")
    print()

    success_count = 0
    failed = []
    total_payloads = 0

    for i, client in enumerate(clients, 1):
        siren = client.get("siren", "?")
        denom = client.get("denomination", "?")[:40]
        print(f"[{i}/{len(clients)}] {denom} (SIREN {siren})")

        ok_compute, err_compute = run_compute(siren, args.level, args.dry_run)
        if not ok_compute:
            print(f"  FAILED compute: {err_compute or 'erreur inconnue'}")
            failed.append(siren)
            continue

        if args.dry_run:
            print("  OK dry-run compute (pas de scheduling)")
            success_count += 1
            continue

        ok_schedule, nb_payloads = run_schedule(siren)
        if not ok_schedule:
            print("  FAILED schedule")
            failed.append(siren)
            continue

        total_payloads += nb_payloads
        print(f"  OK ({nb_payloads} payloads generes)")
        success_count += 1

        # Mettre a jour index.json avec routines_active=true
        client["routines_active"] = True

    # Sauvegarder l'index mis a jour (hors dry-run)
    if not args.dry_run and success_count > 0:
        index_path = PRIVATE / "companies" / "index.json"
        index_path.write_text(
            json.dumps(index, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print()
    print("=" * 60)
    print(f"Resume: {success_count}/{len(clients)} OK, {len(failed)} en echec")
    if not args.dry_run:
        print(f"Total payloads generes: {total_payloads}")
    if failed:
        print(f"Echecs: {', '.join(failed)}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
