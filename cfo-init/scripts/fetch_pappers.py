#!/usr/bin/env python3
"""
fetch_pappers.py — récupération de la fiche société via Pappers.

Mode hybride :
  - Si PAPPERS_API_KEY dans env → API Pappers (https://api.pappers.fr/v2)
  - Sinon → WebFetch (à faire côté Claude Code, ce script génère alors
    l'instruction à exécuter plutôt que d'essayer le fetch lui-même).

Usage :
  python3 fetch_pappers.py --siren 552120222
  python3 fetch_pappers.py --siren 552120222 --output /tmp/carrefour.json
  python3 fetch_pappers.py --siren 552120222 --mode api|web|auto

Output : JSON sur stdout (ou fichier --output) avec les champs normalisés :
  siren, denomination, forme_juridique, code_naf, libelle_naf,
  adresse_siege, rcs, date_creation, tranche_effectif, etat_administratif,
  categorie_entreprise, capital, finances (CA, résultat, bilan sur N-1/N-2).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


PAPPERS_API_BASE = "https://api.pappers.fr/v2"


def validate_siren(siren: str) -> str:
    siren = re.sub(r"\D", "", siren or "")
    if len(siren) != 9:
        raise ValueError(f"SIREN invalide (attendu 9 chiffres, reçu '{siren}')")
    return siren


def normalize_pappers_response(data: dict) -> dict:
    """Normalise la réponse API Pappers vers le schéma company.template.json."""
    siege = data.get("siege") or {}
    finances_raw = data.get("finances") or []
    finances = []
    for f in finances_raw[:3]:  # N, N-1, N-2
        finances.append({
            "annee": f.get("annee"),
            "ca_eur": f.get("chiffre_affaires") or f.get("ca"),
            "resultat_net_eur": f.get("resultat"),
            "total_bilan_eur": f.get("bilan_total") or f.get("total_bilan"),
            "effectif": f.get("effectif"),
        })

    return {
        "source": "pappers_api_v2",
        "fetched_at": data.get("_fetched_at"),
        "siren": data.get("siren"),
        "denomination": data.get("nom_entreprise") or data.get("denomination"),
        "forme_juridique": data.get("forme_juridique"),
        "code_naf": data.get("code_naf") or data.get("code_ape"),
        "libelle_naf": data.get("libelle_code_naf") or data.get("libelle_code_ape"),
        "date_creation": data.get("date_creation"),
        "etat_administratif": "F" if data.get("etablissement_cesse") else "A",
        "capital_eur": data.get("capital"),
        "adresse_siege": {
            "ligne_1": siege.get("adresse_ligne_1"),
            "code_postal": siege.get("code_postal"),
            "ville": siege.get("ville"),
            "siret_siege": siege.get("siret") or (data.get("siren") or "") + (siege.get("nic") or ""),
        },
        "tranche_effectif_insee": data.get("tranche_effectif"),
        "tranche_effectif_label": data.get("tranche_effectif_libelle"),
        "rcs_greffe": data.get("greffe"),
        "finances": finances,
        "_raw": None,  # On ne conserve pas le raw dans le fichier persistant
    }


def fetch_via_api(siren: str, api_key: str) -> dict:
    if requests is None:
        raise RuntimeError("Module 'requests' non installé. Lancer : pip install requests")

    url = f"{PAPPERS_API_BASE}/entreprise"
    params = {"siren": siren, "api_token": api_key}
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    from datetime import datetime, timezone
    data["_fetched_at"] = datetime.now(timezone.utc).isoformat()
    return normalize_pappers_response(data)


def print_web_fetch_instruction(siren: str) -> dict:
    """
    Mode WebFetch : on ne peut pas le faire depuis Python seul.
    On retourne un objet d'instruction que Claude Code pourra exécuter via WebFetch.
    """
    return {
        "mode": "webfetch_required",
        "siren": siren,
        "instruction": "Claude doit appeler WebFetch avec l'URL ci-dessous et en extraire les champs.",
        "urls_to_try": [
            f"https://www.pappers.fr/entreprise/{siren}",
            f"https://annuaire-entreprises.data.gouv.fr/entreprise/{siren}",
        ],
        "schema_target": "templates/company.template.json (partial)",
        "note": (
            "Aucune clé API Pappers détectée (variable PAPPERS_API_KEY). "
            "Claude doit utiliser WebFetch pour récupérer les données publiques "
            "et les normaliser dans le schéma company."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch société via Pappers API ou WebFetch")
    parser.add_argument("--siren", required=True, help="SIREN (9 chiffres)")
    parser.add_argument("--output", type=Path, default=None, help="Fichier de sortie (défaut : stdout)")
    parser.add_argument("--mode", choices=["api", "web", "auto"], default="auto")
    args = parser.parse_args()

    try:
        siren = validate_siren(args.siren)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    api_key = os.environ.get("PAPPERS_API_KEY", "").strip() or None

    # Décision de mode
    if args.mode == "api" and not api_key:
        print("❌ --mode api exige PAPPERS_API_KEY dans l'environnement", file=sys.stderr)
        return 1
    if args.mode == "web" or (args.mode == "auto" and not api_key):
        result = print_web_fetch_instruction(siren)
    else:
        try:
            result = fetch_via_api(siren, api_key)
        except Exception as e:
            print(f"⚠️ API Pappers échec : {e} — fallback WebFetch", file=sys.stderr)
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
