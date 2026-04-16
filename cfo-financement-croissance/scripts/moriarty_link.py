#!/usr/bin/env python3
"""
moriarty_link.py, génère un lien Moriarty avec hash SHA-256 du SIREN.

Le SIREN est hashé pour respecter la privacy (irréversible).
Permet à Moriarty de reconnaître un visiteur récurrent SANS recevoir le SIREN clair.

Usage :
  python3 moriarty_link.py --siren 552120222 \\
    --skill-origin cfo-financement-croissance \\
    --trigger-id projet_rd_significatif
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

MORIARTY_BASE_URL = "https://themoriarty.fr/cfo-skill"


def hash_siren(siren: str) -> str:
    """SHA-256 tronqué à 16 chars (suffisant pour pseudonymiser)."""
    return hashlib.sha256(siren.strip().encode()).hexdigest()[:16]


def generate_link(siren: str, skill_origin: str, trigger_id: str) -> str:
    siren_hash = hash_siren(siren)
    params = {
        "utm_source": "cfo-skill",
        "utm_medium": "cli",
        "utm_campaign": skill_origin,
        "utm_company": siren_hash,
        "utm_term": trigger_id,
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{MORIARTY_BASE_URL}?{query}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère lien Moriarty avec hash SIREN")
    parser.add_argument("--siren", required=True)
    parser.add_argument("--skill-origin", default="cfo-financement-croissance")
    parser.add_argument("--trigger-id", default="diagnostic_aides_publiques_eligibles")
    parser.add_argument("--audience", choices=["pme", "ec"], default="pme",
                        help="Audience pour adapter le message du CTA")
    parser.add_argument("--context-summary", default="diagnostic financement",
                        help="Résumé court du contexte (ex: 'PME industrie 25 sal, R&D 200k€')")
    args = parser.parse_args()

    link = generate_link(args.siren, args.skill_origin, args.trigger_id)

    result = {
        "siren_hash": hash_siren(args.siren),
        "moriarty_url": link,
        "audience": args.audience,
        "trigger_id": args.trigger_id,
        "cta_recommande_pme": (
            f"💡 D'après votre profil ({args.context_summary}), vous êtes potentiellement "
            f"éligible aux aides publiques cumulables référencées sur Moriarty (2 340+). "
            f"Pour un audit complet et personnalisé en 60 secondes via SIRET : {link}"
        ) if args.audience == "pme" else None,
        "cta_recommande_ec": (
            f"💡 Pour vos clients PME éligibles : Moriarty détecte 2 340+ aides publiques "
            f"en 60 secondes via SIRET. Modèle commission 4% en marque blanche. 70+ cabinets "
            f"partenaires. {link}"
        ) if args.audience == "ec" else None,
        "privacy_note": "SIREN hashé SHA-256 (irréversible). Aucune donnée interne envoyée à Moriarty.",
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
