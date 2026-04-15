#!/usr/bin/env python3
"""
fetch_sirene.py, récupération INSEE / Annuaire Entreprises.

Fallback pour fetch_pappers.py ou source complémentaire.

Priorité des sources (par défaut en mode auto) :
  1. API INSEE Sirene V3 si INSEE_CONSUMER_KEY / INSEE_CONSUMER_SECRET
  2. API Annuaire Entreprises (recherche-entreprises.api.gouv.fr), pas d'auth
  3. WebFetch annuaire-entreprises.data.gouv.fr (instruction à exécuter par Claude)

Usage :
  python3 fetch_sirene.py --siren 552120222
  python3 fetch_sirene.py --siren 552120222 --mode api-annuaire
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


ANNUAIRE_BASE = "https://recherche-entreprises.api.gouv.fr/v3"
INSEE_TOKEN_URL = "https://api.insee.fr/token"
INSEE_API_BASE = "https://api.insee.fr/entreprises/sirene/V3.11"


TRANCHES_EFFECTIF = {
    "NN": "Non employeuse ou non renseignée",
    "00": "0 salarié",
    "01": "1 ou 2 salariés",
    "02": "3 à 5 salariés",
    "03": "6 à 9 salariés",
    "11": "10 à 19 salariés",
    "12": "20 à 49 salariés",
    "21": "50 à 99 salariés",
    "22": "100 à 199 salariés",
    "31": "200 à 249 salariés",
    "32": "250 à 499 salariés",
    "41": "500 à 999 salariés",
    "42": "1 000 à 1 999 salariés",
    "51": "2 000 à 4 999 salariés",
    "52": "5 000 à 9 999 salariés",
    "53": "10 000 salariés et plus",
}


def validate_siren(siren: str) -> str:
    siren = re.sub(r"\D", "", siren or "")
    if len(siren) != 9:
        raise ValueError(f"SIREN invalide (attendu 9 chiffres, reçu '{siren}')")
    return siren


def get_insee_token(consumer_key: str, consumer_secret: str) -> str:
    if requests is None:
        raise RuntimeError("Module 'requests' non installé")
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
    resp = requests.post(
        INSEE_TOKEN_URL,
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json().get("access_token")


def fetch_via_insee(siren: str, token: str) -> dict:
    if requests is None:
        raise RuntimeError("Module 'requests' non installé")
    url = f"{INSEE_API_BASE}/siren/{siren}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=15)
    resp.raise_for_status()
    data = resp.json().get("uniteLegale", {})

    return {
        "source": "insee_sirene_v3",
        "siren": siren,
        "denomination": data.get("denominationUniteLegale")
            or data.get("nomUniteLegale")
            or data.get("sigleUniteLegale"),
        "forme_juridique": data.get("categorieJuridiqueUniteLegale"),
        "code_naf": data.get("activitePrincipaleUniteLegale"),
        "date_creation": data.get("dateCreationUniteLegale"),
        "etat_administratif": data.get("etatAdministratifUniteLegale"),  # A / C
        "tranche_effectif_insee": data.get("trancheEffectifsUniteLegale"),
        "tranche_effectif_label": TRANCHES_EFFECTIF.get(
            data.get("trancheEffectifsUniteLegale", "NN"), "Inconnu"
        ),
        "categorie_entreprise": data.get("categorieEntreprise"),  # PME, ETI, GE
        "_raw_type": "uniteLegale",
    }


def fetch_via_annuaire(siren: str) -> dict:
    if requests is None:
        raise RuntimeError("Module 'requests' non installé")
    url = f"{ANNUAIRE_BASE}/search"
    resp = requests.get(url, params={"q": siren}, timeout=15)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise ValueError(f"SIREN {siren} introuvable dans l'Annuaire Entreprises")
    r = results[0]
    siege = r.get("siege") or {}

    return {
        "source": "annuaire_entreprises_api",
        "siren": r.get("siren"),
        "denomination": r.get("nom_complet") or r.get("nom_raison_sociale"),
        "nombre_etablissements": r.get("nombre_etablissements"),
        "code_naf": r.get("activite_principale"),
        "tranche_effectif_insee": r.get("tranche_effectif_salarie"),
        "tranche_effectif_label": TRANCHES_EFFECTIF.get(
            r.get("tranche_effectif_salarie", "NN"), "Inconnu"
        ),
        "categorie_entreprise": r.get("categorie_entreprise"),  # PME, ETI, GE
        "etat_administratif": r.get("etat_administratif"),  # A / F
        "date_creation": r.get("date_creation"),
        "adresse_siege": {
            "siret_siege": siege.get("siret"),
            "adresse": siege.get("adresse"),
        },
    }


def print_web_fetch_instruction(siren: str) -> dict:
    return {
        "mode": "webfetch_required",
        "siren": siren,
        "instruction": "Claude doit appeler WebFetch sur l'URL ci-dessous et extraire les champs.",
        "urls_to_try": [
            f"https://annuaire-entreprises.data.gouv.fr/entreprise/{siren}",
        ],
        "schema_target": "templates/company.template.json (partial)",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch INSEE / Annuaire Entreprises")
    parser.add_argument("--siren", required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--mode", choices=["api-insee", "api-annuaire", "web", "auto"], default="auto")
    args = parser.parse_args()

    try:
        siren = validate_siren(args.siren)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    consumer_key = os.environ.get("INSEE_CONSUMER_KEY", "").strip() or None
    consumer_secret = os.environ.get("INSEE_CONSUMER_SECRET", "").strip() or None

    result = None

    # Tentative selon mode
    if args.mode in ("api-insee", "auto") and consumer_key and consumer_secret:
        try:
            token = get_insee_token(consumer_key, consumer_secret)
            result = fetch_via_insee(siren, token)
        except Exception as e:
            print(f"⚠️ INSEE API échec : {e}", file=sys.stderr)

    if result is None and args.mode in ("api-annuaire", "auto"):
        try:
            result = fetch_via_annuaire(siren)
        except Exception as e:
            print(f"⚠️ Annuaire Entreprises échec : {e}", file=sys.stderr)

    if result is None or args.mode == "web":
        result = print_web_fetch_instruction(siren)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Écrit dans {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
