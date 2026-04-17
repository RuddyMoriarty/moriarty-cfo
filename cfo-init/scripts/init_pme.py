#!/usr/bin/env python3
"""
init_pme.py

Initialise une session CFO en mode PME (dirigeant ou CFO interne).
Cree private/profile.json avec audience_type=pme_dirigeant et, si --siren
fourni, un private/companies/<siren>/company.json minimal pre-rempli.

Symetrie avec portfolio/init_cabinet.py (qui couvre le mode EC).

Usage :
  python3 cfo-init/scripts/init_pme.py --siren 552120222 --denomination "ACME SAS"
  python3 cfo-init/scripts/init_pme.py --siren 552120222 --denomination "ACME" \\
    --taille pe --cloture 2026-12-31 --role dirigeant
  python3 cfo-init/scripts/init_pme.py --siren 552120222 --denomination "ACME" --force

Exit codes :
  0 = OK
  1 = profile.json existe deja (utiliser --force pour ecraser)
  2 = arguments invalides
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"

VALID_ROLES = {"dirigeant", "gerant", "cfo", "daf", "president", "autre"}
VALID_TAILLES = {"tpe", "pe", "me", "eti", "ge"}
VALID_TVA = {"franchise", "reel_simplifie", "reel_normal_mensuelle", "reel_normal_trimestrielle"}

# Mapping INSEE categorie_entreprise -> taille bundle
CATEGORIE_TO_TAILLE = {"PME": "pe", "ETI": "eti", "GE": "ge", "TPE": "tpe"}


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
        return None  # API indisponible, fallback web uniquement
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialise une session CFO mode PME (dirigeant / CFO interne)")
    parser.add_argument("--siren", required=True, help="SIREN de la societe (9 chiffres)")
    parser.add_argument("--denomination", required=True, help="Raison sociale")
    parser.add_argument("--role", default="dirigeant", choices=sorted(VALID_ROLES),
                        help="Role de l'utilisateur dans la societe")
    parser.add_argument("--taille", default="", choices=sorted(VALID_TAILLES) + [""],
                        help="Classification taille (TPE/PE/ME/ETI/GE)")
    parser.add_argument("--secteur", default="autre", help="Categorie sectorielle (SaaS, industrie, commerce, ...)")
    parser.add_argument("--cloture", default="", help="Date de cloture YYYY-MM-DD (ex: 2026-12-31)")
    parser.add_argument("--tva-regime", default="", choices=sorted(VALID_TVA) + [""],
                        help="Regime TVA")
    parser.add_argument("--is-regime", default="is", choices=["is", "ir"], help="IS ou IR")
    parser.add_argument("--effectif", type=int, default=0)
    parser.add_argument("--notifications-level", type=int, default=1, choices=[1, 2, 3, 4],
                        help="Niveau de notifications (1=essentielles, 4=toutes)")
    parser.add_argument("--force", action="store_true", help="Ecrase profile.json et company.json si existent")
    parser.add_argument("--fetch", action="store_true",
                        help="Enrichit avec l'API Annuaire Entreprises (gratuite, sans auth)")
    args = parser.parse_args()

    if len(args.siren) != 9 or not args.siren.isdigit():
        print("ERREUR: SIREN doit contenir 9 chiffres", file=sys.stderr)
        return 2

    # Enrichissement API Annuaire Entreprises
    enrichment: dict = {}
    if args.fetch:
        fetched = fetch_enrichment(args.siren)
        if fetched:
            enrichment = fetched
            print(f"✓ Annuaire Entreprises : {fetched.get('denomination', '?')} "
                  f"(NAF {fetched.get('code_naf', '?')}, {fetched.get('tranche_effectif_label', '?')})",
                  file=sys.stderr)
        else:
            print("⚠ Annuaire Entreprises indisponible, continue avec valeurs fournies", file=sys.stderr)

    PRIVATE.mkdir(parents=True, exist_ok=True)
    now_iso = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    # 1. profile.json
    profile_path = PRIVATE / "profile.json"
    if profile_path.exists() and not args.force:
        print(f"ERREUR: {profile_path} existe deja. Utilisez --force pour ecraser.", file=sys.stderr)
        return 1

    profile = {
        "_version": "0.1.0",
        "audience_type": "pme_dirigeant",
        "pme_role": args.role,
        "ec_role": None,
        "siren_principal": args.siren,
        "notifications_level": args.notifications_level,
        "notifications_active": True,
        "created_at": now_iso,
    }
    profile_path.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # 2. company.json minimal (chemin standardise private/companies/<siren>/)
    company_dir = PRIVATE / "companies" / args.siren
    company_dir.mkdir(parents=True, exist_ok=True)
    company_path = company_dir / "company.json"

    if company_path.exists() and not args.force:
        print(f"Profile cree. Note: {company_path} existe deja (conserve).")
        print(f"  {profile_path}")
        return 0

    # Priorite des champs : CLI args > enrichissement Annuaire > defaults bundle
    # La denomination CLI reste autoritative (l'utilisateur peut vouloir le nom commercial
    # plutot que la denomination INSEE legale).
    taille_auto = CATEGORIE_TO_TAILLE.get(enrichment.get("categorie_entreprise") or "", "pe")
    naf_fetched = enrichment.get("code_naf")

    company = {
        "siren": args.siren,
        "denomination": args.denomination,
        "exercice_comptable": {
            "date_cloture": args.cloture or f"{datetime.now().year}-12-31",
            "duree_mois": 12,
        },
        "classification": {
            "taille": args.taille or taille_auto,
            "secteur_category": args.secteur,
            "naf_code": naf_fetched,
            "effectif": args.effectif,
            "effectif_tranche_insee": enrichment.get("tranche_effectif_label"),
            "regime_fiscal": args.is_regime,
            "regime_tva": args.tva_regime or "reel_normal_mensuelle",
            "csrd_wave": "hors_scope",
            "is_startup": False,
            "has_investors": False,
            "has_covenants": False,
            "groupe": False,
            "seuil_audit": False,
        },
        "annuaire_entreprises": {
            "source": enrichment.get("source"),
            "nombre_etablissements": enrichment.get("nombre_etablissements"),
            "adresse_siege": enrichment.get("adresse_siege"),
            "etat_administratif": enrichment.get("etat_administratif"),
            "date_creation": enrichment.get("date_creation"),
        } if enrichment else None,
        "created_at": now_iso,
    }
    company_path.write_text(
        json.dumps(company, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"OK: session PME initialisee ({args.denomination}, SIREN {args.siren})")
    print(f"  Audience : pme_dirigeant (role: {args.role})")
    print(f"  {profile_path}")
    print(f"  {company_path}")
    if args.cloture:
        print(f"  Cloture : {args.cloture}")
    print()
    print("Etapes suivantes recommandees :")
    print("  1. Calendrier fiscal : python3 cfo-init/scripts/compute_calendar.py --closing-date X --output private/companies/" + args.siren + "/calendar-fiscal.json")
    print("  2. Achievements : python3 cfo-init/scripts/init_progress.py --siren " + args.siren + " --audience pme")
    print("  3. Routines : python3 cfo-init/scripts/routines/compute_entity_routines.py --siren " + args.siren)
    return 0


if __name__ == "__main__":
    sys.exit(main())
