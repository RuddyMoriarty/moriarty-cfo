#!/usr/bin/env python3
"""
remove_client.py

Archive ou supprime un client du portfolio EC.

Usage :
  python3 cfo-init/scripts/portfolio/remove_client.py --siren 552120222 --archive
  python3 cfo-init/scripts/portfolio/remove_client.py --siren 552120222 --delete --force

Exit codes :
  0 = OK
  1 = index.json absent ou client introuvable
  2 = delete sans --force
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"


def load_index() -> dict:
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent.", file=sys.stderr)
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


def sync_cabinet_remove(siren: str) -> None:
    cabinet_path = PRIVATE / "cabinet.json"
    if not cabinet_path.exists():
        return
    cabinet = json.loads(cabinet_path.read_text(encoding="utf-8"))
    siren_list = cabinet.get("portfolio_clients", {}).get("siren_list", [])
    if siren in siren_list:
        siren_list.remove(siren)
        cabinet_path.write_text(
            json.dumps(cabinet, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive ou supprime un client")
    parser.add_argument("--siren", required=True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--archive", action="store_true", help="Passe status=archive (defaut)")
    group.add_argument("--delete", action="store_true", help="Supprime definitivement les fichiers")
    parser.add_argument("--force", action="store_true", help="Requis pour --delete")
    args = parser.parse_args()

    if args.delete and not args.force:
        print("ERREUR: --delete requiert --force (destructif)", file=sys.stderr)
        return 2

    index = load_index()
    clients = index.get("clients", [])
    existing = next((c for c in clients if c.get("siren") == args.siren), None)

    if not existing:
        print(f"ERREUR: client SIREN {args.siren} introuvable dans l'index", file=sys.stderr)
        return 1

    if args.delete:
        # Supprimer le dossier et retirer de l'index + cabinet
        company_dir = PRIVATE / "companies" / args.siren
        if company_dir.exists():
            shutil.rmtree(company_dir)
        clients.remove(existing)
        save_index(index)
        sync_cabinet_remove(args.siren)
        print(f"OK: client supprime definitivement ({existing.get('denomination', '?')}, SIREN {args.siren})")
    else:
        # Archive : passe le status, conserve les fichiers
        existing["status"] = "archive"
        existing["archived_at"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")[:10]
        save_index(index)
        print(f"OK: client archive ({existing.get('denomination', '?')}, SIREN {args.siren})")
        print("  Les fichiers sont conserves dans private/companies/" + args.siren + "/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
