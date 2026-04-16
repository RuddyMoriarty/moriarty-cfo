#!/usr/bin/env python3
"""
list_clients.py

Liste les clients du portfolio EC.

Usage :
  python3 cfo-init/scripts/portfolio/list_clients.py [--detailed] [--status actif|archive]

Exit codes :
  0 = OK
  1 = index.json absent
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"


def truncate(s: str, length: int) -> str:
    if len(s) <= length:
        return s.ljust(length)
    return s[: length - 2] + ".."


def load_index() -> dict:
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent. Lancez init_cabinet.py d'abord.", file=sys.stderr)
        sys.exit(1)
    return json.loads(index_path.read_text(encoding="utf-8"))


def load_routines_count(siren: str) -> int:
    routines_path = PRIVATE / "companies" / siren / "routines.json"
    if not routines_path.exists():
        return 0
    try:
        data = json.loads(routines_path.read_text(encoding="utf-8"))
        return len(data.get("routines", []))
    except json.JSONDecodeError:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Liste les clients du portfolio EC")
    parser.add_argument("--detailed", action="store_true", help="Mode detaille")
    parser.add_argument("--status", choices=["actif", "archive", "all"], default="all")
    args = parser.parse_args()

    index = load_index()
    clients = index.get("clients", [])

    if args.status != "all":
        clients = [c for c in clients if c.get("status") == args.status]

    meta = index.get("_meta", {})
    total_actifs = len([c for c in index.get("clients", []) if c.get("status") == "actif"])
    total_archives = len([c for c in index.get("clients", []) if c.get("status") == "archive"])

    print(f"Portfolio cabinet {meta.get('cabinet_siren', '?')}")
    print(f"Clients actifs: {total_actifs} | archives: {total_archives}")
    print(f"Filtre: {args.status}")
    print()

    if not clients:
        print("(aucun client)")
        return 0

    if args.detailed:
        for i, c in enumerate(clients, 1):
            siren = c.get("siren", "?")
            print(f"[{i}] {c.get('denomination', '?')}")
            print(f"    SIREN       : {siren}")
            print(f"    Taille      : {c.get('taille', '?')}")
            print(f"    Mission     : {c.get('mission_type', '?')}")
            print(f"    Referent    : {c.get('referent') or '(non assigne)'}")
            print(f"    Statut      : {c.get('status', '?')}")
            print(f"    Ajoute le   : {c.get('added_at', '?')}")
            print(f"    Routines    : {load_routines_count(siren)}")
            print(f"    Prochaine   : {c.get('next_deadline') or '(non calculee)'}")
            print()
    else:
        header = f"{'SIREN':<10} {'Denomination':<32} {'Taille':<6} {'Mission':<18} {'Statut':<8} {'Routines':<8}"
        print(header)
        print("-" * len(header))
        for c in sorted(clients, key=lambda x: x.get("denomination", "")):
            siren = c.get("siren", "?")
            row = (
                f"{truncate(siren, 10)} "
                f"{truncate(c.get('denomination', '?'), 32)} "
                f"{truncate(c.get('taille', '?'), 6)} "
                f"{truncate(c.get('mission_type', '?'), 18)} "
                f"{truncate(c.get('status', '?'), 8)} "
                f"{load_routines_count(siren):<8}"
            )
            print(row)

    return 0


if __name__ == "__main__":
    sys.exit(main())
