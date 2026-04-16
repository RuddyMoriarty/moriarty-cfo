#!/usr/bin/env python3
"""
generate_lettre_mission.py

Genere une lettre de mission pour un client EC selon son mission_type.
Versioning automatique : v1, v2, v3... stockes dans
private/companies/<siren>/lettres-mission/.

Usage :
  python3 cfo-init/scripts/portfolio/generate_lettre_mission.py --siren X \\
    --honoraires 4500 --exercice 2026

  # Renouveler (nouvelle version avec montant revise) :
  python3 cfo-init/scripts/portfolio/generate_lettre_mission.py --siren X \\
    --honoraires 4800 --exercice 2027 --new-version

Exit codes :
  0 = OK
  1 = SIREN introuvable ou template absent
  2 = version existe deja (utiliser --new-version pour incrementer)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
TEMPLATES_DIR = ROOT / "cfo-init" / "templates"

LIASSE_PAR_FORME = {
    "SA": "2065",
    "SAS": "2065",
    "SASU": "2065",
    "SARL": "2065",
    "EURL": "2031",
    "EI": "2031",
}


def load_client(siren: str) -> tuple[dict, dict]:
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent", file=sys.stderr)
        sys.exit(1)
    index = json.loads(index_path.read_text(encoding="utf-8"))
    entry = next((c for c in index.get("clients", []) if c.get("siren") == siren), None)
    if entry is None:
        print(f"ERREUR: SIREN {siren} introuvable", file=sys.stderr)
        sys.exit(1)

    company_path = PRIVATE / "companies" / siren / "company.json"
    company = {}
    if company_path.exists():
        company = json.loads(company_path.read_text(encoding="utf-8"))
    return entry, company


def load_cabinet() -> dict:
    path = PRIVATE / "cabinet.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def next_version(lettres_dir: Path, force_new: bool) -> int:
    existing = sorted(lettres_dir.glob("v*.md"))
    if not existing:
        return 1
    # Extraire les numeros de version existants
    versions = []
    for p in existing:
        stem = p.stem  # v1, v2, v3-signed, etc.
        if stem.startswith("v"):
            try:
                num = int(stem[1:].split("-")[0])
                versions.append(num)
            except ValueError:
                continue
    if not versions:
        return 1
    return max(versions) + 1 if force_new else max(versions)


def render(template: str, data: dict) -> str:
    out = template
    for key, value in data.items():
        out = out.replace("{{" + key + "}}", str(value))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Genere une lettre de mission versionee")
    parser.add_argument("--siren", required=True)
    parser.add_argument("--honoraires", type=float, required=True, help="Montant HT en EUR")
    parser.add_argument("--tva", type=float, default=20.0, help="Taux TVA (defaut 20%%)")
    parser.add_argument("--exercice", required=True, help="Annee de l'exercice (ex: 2026)")
    parser.add_argument("--preavis-mois", type=int, default=3)
    parser.add_argument("--modalites", default="paiement en 3 fois (30 % a la signature, 40 % a mi-mission, 30 % a la remise)")
    parser.add_argument("--representant-client", default="", help="Nom dirigeant client")
    parser.add_argument("--new-version", action="store_true", help="Force une nouvelle version")
    args = parser.parse_args()

    entry, company = load_client(args.siren)
    cabinet = load_cabinet()
    mission = entry.get("mission_type", "presentation")

    template_path = TEMPLATES_DIR / f"lettre-mission-{mission.replace('_', '-')}.md"
    if not template_path.exists():
        print(f"ERREUR: pas de template pour mission {mission} (attendu {template_path.name})", file=sys.stderr)
        return 1

    lettres_dir = PRIVATE / "companies" / args.siren / "lettres-mission"
    lettres_dir.mkdir(parents=True, exist_ok=True)

    # Calculer la version
    version = next_version(lettres_dir, force_new=args.new_version)
    output_path = lettres_dir / f"v{version}.md"

    # Verifier qu'on n'ecrase pas sans --new-version
    if output_path.exists() and not args.new_version:
        print(f"ERREUR: {output_path.name} existe deja. Utilisez --new-version pour v{version + 1}.", file=sys.stderr)
        return 2

    # Forme juridique du client (depuis company.json ou devinee)
    client_forme = company.get("forme_juridique", "SAS")
    liasse = LIASSE_PAR_FORME.get(client_forme.upper(), "2065")

    ville = cabinet.get("cabinet", {}).get("ville_principale", "Paris")

    data = {
        "VERSION": f"v{version}",
        "REFERENCE_LETTRE": f"LM-{args.siren}-{args.exercice}-v{version}",
        "CABINET_NOM": cabinet.get("cabinet", {}).get("denomination", "(cabinet)"),
        "CABINET_FORME": cabinet.get("cabinet", {}).get("forme_juridique") or "SELARL d'expertise comptable",
        "CABINET_ADRESSE": cabinet.get("cabinet", {}).get("adresse_siege") or cabinet.get("cabinet", {}).get("ville_principale", "(adresse a renseigner)"),
        "CABINET_SIREN": cabinet.get("cabinet", {}).get("siren", "?"),
        "CABINET_REPRESENTANT": entry.get("referent") or cabinet.get("referent_moriarty_cfo", {}).get("nom") or "(expert-comptable)",
        "CLIENT_DENOMINATION": entry.get("denomination", "?"),
        "CLIENT_FORME": client_forme,
        "CLIENT_ADRESSE": company.get("identification", {}).get("adresse", "(adresse client)"),
        "CLIENT_SIREN": args.siren,
        "CLIENT_REPRESENTANT": args.representant_client or "(representant legal)",
        "DATE_CLOTURE": company.get("exercice_comptable", {}).get("date_cloture", "?"),
        "LIASSE_FORMULAIRE": liasse,
        "MONTANT_HONORAIRES": f"{args.honoraires:,.0f}".replace(",", " "),
        "MONTANT_HONORAIRES_TTC": f"{args.honoraires * (1 + args.tva / 100):,.0f}".replace(",", " "),
        "EXERCICE": args.exercice,
        "MODALITES_PAIEMENT": args.modalites,
        "DATE_REMISE_PIECES": f"{args.exercice}-03-15",
        "DATE_REMISE_COMPTES": f"{args.exercice}-05-15",
        "PREAVIS_MOIS": args.preavis_mois,
        "TRIBUNAL_COMPETENT": ville,
        "VILLE_SIGNATURE": ville,
        "DATE_SIGNATURE": date.today().isoformat(),
        # Specifiques social_paie
        "CONVENTION_COLLECTIVE": company.get("convention_collective", "(a renseigner)"),
        "JOUR_LIMITE_VARIABLES": "5",
        "FORFAIT_MENSUEL": f"{args.honoraires:,.0f}".replace(",", " "),
        "PRIX_BULLETIN": "18",
        "SEUIL_BULLETINS": "10",
        "TAUX_HORAIRE": "95",
        "DATE_DEBUT_MISSION": date.today().isoformat(),
    }

    rendered = render(template_path.read_text(encoding="utf-8"), data)
    output_path.write_text(rendered, encoding="utf-8")

    # Metadonnees
    meta_path = lettres_dir / "metadata.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    else:
        meta = {"versions": []}

    meta["versions"].append({
        "version": version,
        "mission_type": mission,
        "honoraires_ht": args.honoraires,
        "exercice": args.exercice,
        "created_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "file": f"v{version}.md",
        "signed": False,
    })
    meta_path.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"OK: lettre de mission v{version} generee")
    print(f"  {output_path}")
    print(f"  Mission: {mission}, Honoraires: {args.honoraires} EUR HT, Exercice: {args.exercice}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
