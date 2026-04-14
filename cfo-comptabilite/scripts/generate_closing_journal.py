#!/usr/bin/env python3
"""
generate_closing_journal.py — génère un squelette de journal des écritures
de clôture (mensualisées ou annuelles).

Produit les écritures AUTOMATISABLES :
  - Amortissements mensualisés (1/12 de l'annuel pour chaque immo)
  - Charges constatées d'avance (CCA) pour abonnements / assurances récurrents
  - Produits constatés d'avance (PCA) pour contrats SaaS facturés annuellement

Les écritures NON AUTOMATISABLES (jugement humain requis) sont LISTÉES mais
non-pré-remplies :
  - FAR / FNP (liste fournisseurs sans facture reçue)
  - Provisions pour litiges
  - Dépréciations clients douteux
  - Valorisation stocks obsolètes

Usage :
  python3 generate_closing_journal.py \\
    --immobilisations immos.csv \\
    --abonnements abos.csv \\
    --contrats-saas saas.csv \\
    --date-cloture 2026-12-31 \\
    --mode mensuel|annuel \\
    --output journal-cloture.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path


def parse_csv(path: Path) -> list[dict]:
    if not path or not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def ecritures_amortissements(immos: list[dict], mode: str, date_cloture: date) -> list[dict]:
    """Génère les écritures d'amortissement (compte 681x → compte 281x)."""
    ecritures = []
    for immo in immos:
        try:
            base = float(immo.get("base_amortissable", 0))
            duree_annees = int(immo.get("duree_annees", 0))
            compte_immo = immo.get("compte_immo", "2183")  # matériel informatique par défaut
            compte_amort = f"28{compte_immo[1:]}"
            compte_charge = f"681{compte_immo[1:3]}"
        except (ValueError, KeyError):
            continue

        if duree_annees == 0:
            continue

        annuite = base / duree_annees
        montant = annuite / 12 if mode == "mensuel" else annuite

        ecritures.append({
            "date": date_cloture.isoformat(),
            "journal": "OD",
            "libelle": f"Amortissement {mode} {immo.get('designation', compte_immo)}",
            "lignes": [
                {"compte": compte_charge, "debit": round(montant, 2), "credit": 0.00},
                {"compte": compte_amort, "debit": 0.00, "credit": round(montant, 2)},
            ],
        })
    return ecritures


def ecritures_cca(abonnements: list[dict], date_cloture: date) -> list[dict]:
    """Génère les CCA pour abonnements payés d'avance."""
    ecritures = []
    for abo in abonnements:
        try:
            date_debut = date.fromisoformat(abo["date_debut"])
            date_fin = date.fromisoformat(abo["date_fin"])
            montant_total = float(abo["montant_total"])
            compte_charge = abo.get("compte_charge", "616")
        except (ValueError, KeyError):
            continue

        if date_cloture <= date_debut or date_cloture >= date_fin:
            continue  # hors période

        total_jours = (date_fin - date_debut).days
        jours_restants = (date_fin - date_cloture).days
        if total_jours <= 0:
            continue

        montant_cca = montant_total * jours_restants / total_jours

        ecritures.append({
            "date": date_cloture.isoformat(),
            "journal": "OD",
            "libelle": f"CCA {abo.get('designation', compte_charge)} - période {date_cloture.isoformat()} → {date_fin.isoformat()}",
            "lignes": [
                {"compte": "486", "debit": round(montant_cca, 2), "credit": 0.00},
                {"compte": compte_charge, "debit": 0.00, "credit": round(montant_cca, 2)},
            ],
        })
    return ecritures


def ecritures_pca(contrats_saas: list[dict], date_cloture: date) -> list[dict]:
    """Génère les PCA pour contrats SaaS facturés annuellement."""
    ecritures = []
    for contrat in contrats_saas:
        try:
            date_debut = date.fromisoformat(contrat["date_debut"])
            date_fin = date.fromisoformat(contrat["date_fin"])
            montant_total = float(contrat["montant_total"])
            compte_produit = contrat.get("compte_produit", "706")
        except (ValueError, KeyError):
            continue

        if date_cloture <= date_debut or date_cloture >= date_fin:
            continue

        total_jours = (date_fin - date_debut).days
        jours_restants = (date_fin - date_cloture).days
        if total_jours <= 0:
            continue

        montant_pca = montant_total * jours_restants / total_jours

        ecritures.append({
            "date": date_cloture.isoformat(),
            "journal": "OD",
            "libelle": f"PCA {contrat.get('client', '')} - période non acquise",
            "lignes": [
                {"compte": compte_produit, "debit": round(montant_pca, 2), "credit": 0.00},
                {"compte": "487", "debit": 0.00, "credit": round(montant_pca, 2)},
            ],
        })
    return ecritures


def liste_items_manuels(immos_count: int, balance_clients_count: int) -> list[str]:
    """Liste les écritures qui nécessitent un jugement humain."""
    items = [
        "FAR/FNP — Lister les fournisseurs ayant livré sans facture reçue (rapprocher BL et factures reçues)",
        "Provisions pour litiges — Revoir avec l'avocat les contentieux en cours, chiffrer les risques probables",
        "Dépréciation clients douteux — Revoir la balance clients, identifier les créances > 6 mois impayées et provisionner",
        "Dépréciation stocks obsolètes — Inventaire physique : lister les références non vendues depuis 12+ mois",
    ]
    if immos_count > 0:
        items.append(f"Test de dépréciation immobilisations — Revoir les {immos_count} immo(s) pour indices de perte de valeur (IAS 36 si IFRS)")
    if balance_clients_count > 100:
        items.append("Revue d'ancienneté créances clients — Aging report détaillé obligatoire au-delà de 100 clients")
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère squelette journal écritures clôture")
    parser.add_argument("--immobilisations", type=Path, default=None)
    parser.add_argument("--abonnements", type=Path, default=None)
    parser.add_argument("--contrats-saas", type=Path, default=None)
    parser.add_argument("--date-cloture", required=True, help="YYYY-MM-DD")
    parser.add_argument("--mode", choices=["mensuel", "annuel"], default="mensuel")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    date_cloture = date.fromisoformat(args.date_cloture)

    immos = parse_csv(args.immobilisations)
    abos = parse_csv(args.abonnements)
    contrats = parse_csv(args.contrats_saas)

    ecritures = []
    ecritures.extend(ecritures_amortissements(immos, args.mode, date_cloture))
    ecritures.extend(ecritures_cca(abos, date_cloture))
    ecritures.extend(ecritures_pca(contrats, date_cloture))

    items_manuels = liste_items_manuels(len(immos), 0)

    result = {
        "date_cloture": args.date_cloture,
        "mode": args.mode,
        "ecritures_automatiques": {
            "count": len(ecritures),
            "total_debit": round(sum(sum(l["debit"] for l in e["lignes"]) for e in ecritures), 2),
            "total_credit": round(sum(sum(l["credit"] for l in e["lignes"]) for e in ecritures), 2),
            "items": ecritures,
        },
        "items_manuels_a_revoir": items_manuels,
        "note": (
            "Ce journal est un SQUELETTE : les écritures automatiques sont "
            "à valider avec votre EC avant intégration en compta. Les items manuels "
            "nécessitent un jugement humain (FAR, provisions, dépréciations)."
        ),
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ {len(ecritures)} écritures auto + {len(items_manuels)} items manuels", file=sys.stderr)
        print(f"✓ Écrit dans {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
