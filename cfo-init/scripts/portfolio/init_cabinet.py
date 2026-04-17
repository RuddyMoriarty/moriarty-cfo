#!/usr/bin/env python3
"""
init_cabinet.py

Initialise un cabinet d'expertise comptable en mode EC portfolio.
Cree private/cabinet.json depuis cabinet.template.json, private/profile.json
avec audience_type=ec_collaborateur, et private/companies/index.json vide.

Usage :
  python3 cfo-init/scripts/portfolio/init_cabinet.py --siren 123456789 \\
    --denomination "CABINET DURAND & ASSOCIES" \\
    [--forme selarl] [--ville Nancy] [--force]

Exit codes :
  0 = OK
  1 = cabinet.json existe deja (utiliser --force pour ecraser)
  2 = template introuvable ou corrompu
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
TEMPLATE_PATH = ROOT / "cfo-init" / "templates" / "cabinet.template.json"


def fetch_enrichment(siren: str) -> dict | None:
    """Appelle fetch_sirene.py --mode api-annuaire. Retourne dict ou None si echec."""
    script = ROOT / "cfo-init" / "scripts" / "fetch_sirene.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--siren", siren, "--mode", "api-annuaire"],
        capture_output=True, text=True, timeout=15, cwd=str(ROOT),
    )
    if proc.returncode != 0:
        return None
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None
    if data.get("mode") == "webfetch_required":
        return None
    return data


def load_template() -> dict:
    if not TEMPLATE_PATH.exists():
        print(f"ERREUR: template introuvable : {TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERREUR: template JSON invalide : {e}", file=sys.stderr)
        sys.exit(2)


def strip_meta(template: dict) -> dict:
    """Retire les cles qui commencent par _ (meta/commentaires)."""
    if isinstance(template, dict):
        return {k: strip_meta(v) for k, v in template.items() if not k.startswith("_")}
    if isinstance(template, list):
        return [strip_meta(x) for x in template]
    return template


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialise un cabinet EC")
    parser.add_argument("--siren", required=True, help="SIREN du cabinet (9 chiffres)")
    parser.add_argument("--denomination", required=True, help="Raison sociale du cabinet")
    parser.add_argument("--forme", default="", help="Forme juridique (selarl, selas, sarl, sas...)")
    parser.add_argument("--ville", default="", help="Ville principale")
    parser.add_argument("--force", action="store_true", help="Ecrase cabinet.json si existe")
    parser.add_argument("--fetch", action="store_true",
                        help="Enrichit avec l'API Annuaire Entreprises (gratuite, sans auth)")
    parser.add_argument("--private-dir", type=Path, default=None,
                        help="Repertoire prive (default: <repo>/private)")
    args = parser.parse_args()
    global PRIVATE
    if args.private_dir is not None:
        PRIVATE = args.private_dir

    enrichment: dict = {}
    if args.fetch:
        fetched = fetch_enrichment(args.siren)
        if fetched:
            enrichment = fetched
            print(f"✓ Annuaire Entreprises : {fetched.get('denomination', '?')}, "
                  f"NAF {fetched.get('code_naf', '?')}", file=sys.stderr)
        else:
            print("⚠ Annuaire Entreprises indisponible, continue avec valeurs fournies", file=sys.stderr)

    PRIVATE.mkdir(parents=True, exist_ok=True)
    cabinet_path = PRIVATE / "cabinet.json"

    if cabinet_path.exists() and not args.force:
        print(f"ERREUR: {cabinet_path} existe deja. Utilisez --force pour ecraser.", file=sys.stderr)
        return 1

    template = strip_meta(load_template())
    template["cabinet"]["siren"] = args.siren
    template["cabinet"]["denomination"] = args.denomination
    if args.forme:
        template["cabinet"]["forme_juridique"] = args.forme
    if args.ville:
        template["cabinet"]["ville_principale"] = args.ville
    # Enrichissement Annuaire Entreprises si dispo
    if enrichment:
        adresse = enrichment.get("adresse_siege") or {}
        template["cabinet"]["annuaire_entreprises"] = {
            "source": enrichment.get("source"),
            "code_naf": enrichment.get("code_naf"),
            "nombre_etablissements": enrichment.get("nombre_etablissements"),
            "adresse_siege": adresse,
            "etat_administratif": enrichment.get("etat_administratif"),
            "date_creation": enrichment.get("date_creation"),
        }

    cabinet_path.write_text(
        json.dumps(template, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # profile.json : cree si absent
    profile_path = PRIVATE / "profile.json"
    if not profile_path.exists():
        profile = {
            "audience_type": "ec_collaborateur",
            "notifications_level": 1,
            "notifications_active": True,
            "created_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        }
        profile_path.write_text(
            json.dumps(profile, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    # index.json : cree si absent
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index = {
            "_meta": {
                "cabinet_siren": args.siren,
                "last_updated": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "count": 0,
            },
            "clients": [],
        }
        index_path.write_text(
            json.dumps(index, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"OK: cabinet initialise ({args.denomination}, SIREN {args.siren})")
    print(f"  {cabinet_path}")
    print(f"  {profile_path}")
    print(f"  {index_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
