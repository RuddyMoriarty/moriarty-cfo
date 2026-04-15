#!/usr/bin/env python3
"""
risk_mapping_generator.py, génère matrice de risques 5x5 + plan d'action.

Input : CSV avec id_risque,libelle,categorie,probabilite(1-5),impact(1-5),owner
Output : matrice + top 10 risques + KRI proposés
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def classify_severity(proba: int, impact: int) -> tuple[str, str]:
    score = proba * impact
    if score >= 16:  # ex: 4×4, 5×4, 5×5
        return "🔴 critique", "Action immédiate (semaines)"
    elif score >= 9:
        return "🟠 élevé", "Plan d'action 30-90 jours"
    elif score >= 5:
        return "🟡 moyen", "Surveillance + revue trimestrielle"
    return "🟢 faible", "Tolérance, pas d'action immédiate"


def propose_kri(libelle: str, categorie: str) -> str:
    """Proposition de KRI (Key Risk Indicator) selon catégorie."""
    kri_map = {
        "financier": "Turn-over équipe finance, BFR en jours, ratio liquidité",
        "operationnel": "Taux d'indisponibilité SI, taux de défauts, taux d'incidents",
        "compliance": "Nb sanctions / non-conformités détectées, audits passés",
        "cyber": "Tentatives d'attaques détectées, MTTR (Mean Time To Recovery)",
        "rh": "Turnover, satisfaction (eNPS), absentéisme",
        "fournisseurs": "% CA top 3 fournisseurs, délai moyen livraison",
        "clients": "% CA top 3 clients, NPS, churn",
        "reglementaire": "Délais de conformité, nombre de procédures à jour",
    }
    return kri_map.get(categorie.lower(), "À définir avec le métier")


def main() -> int:
    parser = argparse.ArgumentParser(description="Risk mapping COSO ERM")
    parser.add_argument("--risques", type=Path, required=True,
                        help="CSV : id,libelle,categorie,probabilite,impact,owner")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    risques = []
    with args.risques.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                proba = int(row.get("probabilite", 0))
                impact = int(row.get("impact", 0))
                if not (1 <= proba <= 5 and 1 <= impact <= 5):
                    continue
                severite, action = classify_severity(proba, impact)
                risques.append({
                    "id": row.get("id", ""),
                    "libelle": row.get("libelle", ""),
                    "categorie": row.get("categorie", ""),
                    "owner": row.get("owner", ""),
                    "probabilite": proba,
                    "impact": impact,
                    "score": proba * impact,
                    "severite": severite,
                    "action_recommandee": action,
                    "kri_propose": propose_kri(row.get("libelle", ""), row.get("categorie", "")),
                })
            except (ValueError, KeyError):
                continue

    risques.sort(key=lambda r: r["score"], reverse=True)
    top_10 = risques[:10]

    # Matrice
    matrice = [[[] for _ in range(5)] for _ in range(5)]
    for r in risques:
        matrice[r["impact"] - 1][r["probabilite"] - 1].append(r["id"])

    result = {
        "_version": "0.1.0",
        "nb_risques_total": len(risques),
        "repartition_severite": {
            "critique": sum(1 for r in risques if "critique" in r["severite"]),
            "eleve": sum(1 for r in risques if "élevé" in r["severite"]),
            "moyen": sum(1 for r in risques if "moyen" in r["severite"]),
            "faible": sum(1 for r in risques if "faible" in r["severite"]),
        },
        "top_10_risques": top_10,
        "matrice_5x5": matrice,
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ Cartographie risques : {args.output}", file=sys.stderr)
        print(f"  → {len(risques)} risques · top 10 priorisés · {result['repartition_severite']['critique']} critiques", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
