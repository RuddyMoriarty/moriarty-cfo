#!/usr/bin/env python3
"""
veille_scheduler.py, programme les tâches de veille réglementaire.

Génère le payload pour mcp__scheduled-tasks__create_scheduled_task selon le
niveau de veille configuré dans private/profile.json.

Output : liste JSON de tâches à programmer (le harnais Claude Code crée
ensuite via les outils MCP en session interactive).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def jittered_minute(siren: str, base: int = 7) -> int:
    """Minute pinée hors :00 et :30, jittered selon SIREN."""
    h = int(hashlib.sha256(siren.encode()).hexdigest()[:8], 16)
    minute = (h % 28) + 1  # 1 à 28
    if minute in (29, 30):
        minute = 27
    return minute


def generate_tasks(siren: str, niveau: int = 2) -> list[dict]:
    """Génère les tâches de veille selon le niveau (1-4)."""
    if niveau == 4:  # aucune
        return []

    minute = jittered_minute(siren)
    tasks = []

    # Hebdo : lundi 9h jittered (niveaux 1-3)
    if niveau >= 1:
        tasks.append({
            "task_id": f"veille-hebdo-{siren[:6]}",
            "cron_expression": f"{minute} 9 * * 1",  # lundi 9h+jit
            "description": "Veille réglementaire hebdomadaire (lundi 9h)",
            "prompt": (
                "Veille réglementaire hebdomadaire, semaine en cours.\n\n"
                "Sources à consulter (lire data/sources.json categories.frameworks_cfo et risque_conformite) :\n"
                "- Légifrance (lois publiées cette semaine)\n"
                "- BoFip (instructions fiscales)\n"
                "- ANC (règlements comptables)\n"
                "- IASB / EFRAG (IFRS, ESRS)\n"
                "- AMF (régulation marchés)\n\n"
                "Pour chaque évolution impactant le profil société (lire private/company.json) :\n"
                "1. Résumer en 2-3 lignes\n"
                "2. Évaluer impact (faible / moyen / fort)\n"
                "3. Proposer action si applicable\n\n"
                "Sortie : `out/veille-{date}.md`"
            ),
        })

    # Mensuel : 1er du mois 9h (niveaux 2-3)
    if niveau >= 2:
        tasks.append({
            "task_id": f"veille-mensuelle-{siren[:6]}",
            "cron_expression": f"{minute + 6} 9 1 * *",
            "description": "Synthèse mensuelle veille réglementaire (1er du mois)",
            "prompt": (
                "Synthèse mensuelle de la veille réglementaire.\n\n"
                "Compiler les veilles hebdomadaires du mois écoulé en 1 synthèse :\n"
                "- Top 5 évolutions retenues\n"
                "- Calendrier des prochaines applications\n"
                "- Actions en cours\n\n"
                "Sortie : `out/synthese-veille-{mois}-{annee}.md`"
            ),
        })

    # Annuel : 1er octobre (PLF), tous niveaux >= 1
    if niveau >= 1:
        tasks.append({
            "task_id": f"veille-plf-{siren[:6]}",
            "cron_expression": f"{minute} 9 1 10 *",  # 1er octobre 9h+jit
            "description": "Projet de Loi de Finance N+1 (1er octobre)",
            "prompt": (
                "Le Projet de Loi de Finance pour l'année prochaine vient d'être déposé.\n\n"
                "Analyser les mesures impactant la société (lire private/company.json) :\n"
                "1. Mesures fiscales (taux IS/TVA, crédits d'impôt, déductibilité)\n"
                "2. Mesures sociales (cotisations, plafonds)\n"
                "3. Mesures sectorielles\n\n"
                "Préparer une note pour le CODIR avec impacts estimés €/an.\n"
                "Sortie : `out/analyse-plf-{annee+1}.md`"
            ),
        })

    return tasks


def main() -> int:
    parser = argparse.ArgumentParser(description="Programmation veille réglementaire")
    parser.add_argument("--siren", required=True)
    parser.add_argument("--niveau", type=int, default=2, choices=[1, 2, 3, 4])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    tasks = generate_tasks(args.siren, args.niveau)

    result = {
        "_version": "0.1.0",
        "niveau_veille": args.niveau,
        "nb_taches": len(tasks),
        "tasks": tasks,
        "instruction": (
            "Pour effectivement programmer ces tâches, exécuter chacune via "
            "mcp__scheduled-tasks__create_scheduled_task dans la session Claude Code "
            "(ce script génère uniquement le payload, les appels MCP doivent être "
            "lancés en interactif)."
        ),
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ {len(tasks)} tâche(s) de veille générée(s) : {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
