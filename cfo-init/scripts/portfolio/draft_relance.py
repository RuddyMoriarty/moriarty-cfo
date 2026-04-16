#!/usr/bin/env python3
"""
draft_relance.py

Genere un mail de relance pour les pieces manquantes d'un client EC.
Utilise les templates relance-premiere.md ou relance-urgente.md selon le type.

Usage :
  python3 cfo-init/scripts/portfolio/draft_relance.py --siren 552120222 --type premiere
  python3 cfo-init/scripts/portfolio/draft_relance.py --siren 552120222 --type urgente \\
    --date-echeance 2026-05-15

Exit codes :
  0 = OK
  1 = SIREN ou catalogue absent
  2 = dossier deja complet (rien a relancer)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
CATALOG_PATH = ROOT / "data" / "pieces-dossier.json"
TEMPLATES_DIR = ROOT / "cfo-init" / "templates"

MISSION_LABELS = {
    "presentation": "mission de presentation",
    "examen_limite": "examen limite",
    "audit_legal_cac": "audit legal CAC",
    "social_paie": "suivi social et paie",
    "juridique": "mission juridique",
    "conseil_financier": "conseil financier",
    "cir_cii": "dossier CIR/CII",
    "aides_publiques": "dossier aides publiques",
}


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        print(f"ERREUR: catalogue introuvable : {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_client(siren: str) -> tuple[dict, dict]:
    """Retourne (index_entry, company.json)."""
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent", file=sys.stderr)
        sys.exit(1)
    index = json.loads(index_path.read_text(encoding="utf-8"))
    entry = next((c for c in index.get("clients", []) if c.get("siren") == siren), None)
    if entry is None:
        print(f"ERREUR: SIREN {siren} introuvable dans l'index", file=sys.stderr)
        sys.exit(1)

    company_path = PRIVATE / "companies" / siren / "company.json"
    company = {}
    if company_path.exists():
        company = json.loads(company_path.read_text(encoding="utf-8"))
    return entry, company


def load_cabinet() -> dict:
    path = PRIVATE / "cabinet.json"
    if not path.exists():
        return {"cabinet": {"denomination": "?"}}
    return json.loads(path.read_text(encoding="utf-8"))


def load_pieces_recues(siren: str) -> dict:
    path = PRIVATE / "companies" / siren / "pieces.json"
    if not path.exists():
        return {"pieces_recues": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def compute_missing(siren: str, mission: str) -> list:
    catalog = load_catalog()
    expected = catalog.get("pieces_par_mission", {}).get(mission, [])
    received = load_pieces_recues(siren).get("pieces_recues", {})
    missing = []
    for p in expected:
        if not received.get(p["id"], {}).get("recu"):
            missing.append(p)
    return missing


def render(template: str, data: dict) -> str:
    out = template
    for key, value in data.items():
        out = out.replace("{{" + key + "}}", str(value))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Genere un mail de relance")
    parser.add_argument("--siren", required=True)
    parser.add_argument("--type", choices=["premiere", "urgente"], default="premiere")
    parser.add_argument("--date-echeance", default="", help="Date echeance legale (YYYY-MM-DD, relance urgente)")
    parser.add_argument("--jours-delai", type=int, default=10, help="Jours avant date limite de reponse")
    parser.add_argument("--output", type=Path, help="Fichier de sortie (par defaut stdout)")
    args = parser.parse_args()

    entry, company = load_client(args.siren)
    cabinet = load_cabinet()
    mission = entry.get("mission_type", "presentation")

    missing = compute_missing(args.siren, mission)
    obligatoires = [p for p in missing if p["obligatoire"]]

    if not obligatoires:
        print(f"Dossier {args.siren} complet (0 piece obligatoire manquante). Rien a relancer.")
        return 2

    template_path = TEMPLATES_DIR / f"relance-{args.type}.md"
    if not template_path.exists():
        print(f"ERREUR: template introuvable : {template_path}", file=sys.stderr)
        return 1

    today = date.today()
    liste_str = "\n".join(f"- {p['label']}" for p in missing)

    data = {
        "DENOMINATION": entry.get("denomination", "?"),
        "REFERENT_CLIENT": entry.get("referent") or "(referent a preciser)",
        "MISSION_LABEL": MISSION_LABELS.get(mission, mission),
        "DATE_CLOTURE": company.get("exercice_comptable", {}).get("date_cloture", "?"),
        "LISTE_PIECES_MANQUANTES": liste_str,
        "DATE_LIMITE": (today + timedelta(days=args.jours_delai)).isoformat(),
        "DATE_LIMITE_URGENTE": (today + timedelta(days=5)).isoformat(),
        "DATE_ECHEANCE": args.date_echeance or "(date a preciser)",
        "TYPE_DEPOT": "liasse fiscale" if mission == "presentation" else "dossier",
        "CABINET_NOM": cabinet.get("cabinet", {}).get("denomination", "?"),
        "EMAIL_CABINET": "contact@cabinet.fr",
        "TEL_CABINET": "(a renseigner)",
        "SIGNATAIRE": entry.get("referent") or "(a signer)",
        "ROLE_SIGNATAIRE": "Expert-comptable",
    }

    template = template_path.read_text(encoding="utf-8")
    rendered = render(template, data)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"OK: relance {args.type} ecrite dans {args.output}")
        print(f"  {len(missing)} pieces manquantes ({len(obligatoires)} obligatoires)")
    else:
        print(rendered)

    # Log dans private/companies/<siren>/relances.json
    relances_path = PRIVATE / "companies" / args.siren / "relances.json"
    if relances_path.exists():
        hist = json.loads(relances_path.read_text(encoding="utf-8"))
    else:
        hist = {"relances": []}
    hist["relances"].append({
        "type": args.type,
        "date": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "pieces_manquantes": [p["id"] for p in missing],
        "output": str(args.output) if args.output else None,
    })
    relances_path.parent.mkdir(parents=True, exist_ok=True)
    relances_path.write_text(
        json.dumps(hist, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
