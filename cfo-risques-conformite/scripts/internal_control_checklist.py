#!/usr/bin/env python3
"""
internal_control_checklist.py — génère checklist contrôle interne par fonction.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CHECKLIST_TEMPLATE = {
    "achats": [
        "Procédure d'achat formalisée (du besoin à la facture)",
        "Séparation : commande ≠ validation facture ≠ paiement",
        "Bons de commande pré-numérotés",
        "Validation hiérarchique selon montant (matrice de pouvoirs)",
        "Réception physique avec bon de livraison signé",
        "Rapprochement BC / BL / facture (3-way matching)",
        "Liste fournisseurs validée + à jour (référencement)",
        "Politique anti-corruption (cadeaux clients/fournisseurs)",
    ],
    "ventes": [
        "Procédure de vente formalisée (devis → contrat → facture → encaissement)",
        "Validation crédit client avant ouverture (KYC + scoring financier)",
        "Conditions générales de vente (CGV) à jour",
        "Encours client surveillés (alerte si > limite)",
        "Politique de relance amiable + contentieux",
        "Provision créances douteuses revue trimestriellement",
    ],
    "tresorerie": [
        "Liste signataires bancaires limitée + à jour",
        "Double signature pour paiements > seuil (5k€ ou 10k€)",
        "Rapprochement bancaire mensuel (par personne ≠ qui passe les écritures)",
        "Cartes corporate avec plafond + relevé mensuel signé",
        "Caisse : tenue + comptage + supervision",
        "Sécurisation des moyens de paiement (chéquier, terminal)",
    ],
    "paie": [
        "Procédure de paie formalisée",
        "Séparation : préparation paie (RH) ≠ validation montants (DG) ≠ versement (trésorerie)",
        "DSN mensuelle dans les délais",
        "Rapprochement comptes 421/431/437 vs DSN trimestriel",
        "Politique notes de frais formalisée + plafonds",
        "Audit annuel par cabinet paie ou EC",
    ],
    "stocks": [
        "Inventaire physique annuel obligatoire (L. 123-12)",
        "Méthode de valorisation cohérente (CMP ou PEPS, pas de mix)",
        "Procédure entrées / sorties stock (BL, ordres de fab)",
        "Sécurisation physique (accès limité)",
        "Suivi ABC (top 20% références = focus sur la précision)",
        "Provisions stocks obsolètes / dépréciations annuelles",
    ],
    "it": [
        "Politique de sécurité IT formalisée",
        "Sauvegardes 3-2-1 + tests restauration",
        "MFA (Multi-Factor Authentication) sur tous les accès sensibles",
        "Antivirus / EDR sur tous les postes",
        "Mises à jour automatiques / patching",
        "Plan de continuité IT (DRP) testé annuellement",
        "Politique BYOD / télétravail",
        "Formation sécurité annuelle (phishing, social engineering)",
    ],
    "compliance": [
        "Politique LCB-FT (si applicable) — cf. references/lcb-ft.md",
        "RGPD : registre traitements + DPO + politique confidentialité",
        "Conventions réglementées identifiées + déclarées",
        "Veille réglementaire active — cf. references/veille-reglementaire.md",
        "Audit annuel des contrôles clés",
        "Cartographie des risques mise à jour annuellement",
    ],
}


def generate_checklist(fonctions: list[str] | None = None) -> dict:
    """Génère la checklist pour les fonctions demandées (toutes par défaut)."""
    if not fonctions:
        fonctions = list(CHECKLIST_TEMPLATE.keys())

    checklist = {}
    total_items = 0
    for f in fonctions:
        items = CHECKLIST_TEMPLATE.get(f.lower(), [])
        checklist[f] = [{"item": it, "applied": False, "evidence": "", "owner": ""} for it in items]
        total_items += len(items)

    return {
        "_version": "0.1.0",
        "nb_fonctions": len(checklist),
        "nb_items_total": total_items,
        "checklist": checklist,
        "instruction": (
            "Pour chaque item : noter applied=true si le contrôle est en place, "
            "renseigner evidence (URL, document, nom de fichier preuve) et owner. "
            "Réviser annuellement."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Checklist contrôle interne")
    parser.add_argument("--fonctions", nargs="+", default=None,
                        help="Fonctions à inclure (achats ventes tresorerie paie stocks it compliance)")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    result = generate_checklist(args.fonctions)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Checklist contrôle interne ({result['nb_items_total']} items / {result['nb_fonctions']} fonctions) : {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
