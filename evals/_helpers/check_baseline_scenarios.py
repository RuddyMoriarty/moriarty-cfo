#!/usr/bin/env python3
"""
check_baseline_scenarios.py, v0.2.2 Module B.

Test statique : valide la structure de baseline-scenarios.json sans appeler l'API.
Verifie que chaque scenario reference un skill existant, a une checklist non vide,
et des budgets de temps coherents. Garantit que le framework de mesure est pret
a tourner meme si on n'execute pas les runs en CI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS = ROOT / "evals" / "baseline-scenarios.json"


def main() -> int:
    if not SCENARIOS.exists():
        print(f"ERREUR: {SCENARIOS.relative_to(ROOT)} introuvable", file=sys.stderr)
        return 1

    data = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    scenarios = data.get("scenarios", [])

    if len(scenarios) < 3:
        print(f"ERREUR: au moins 3 scenarios attendus, trouve {len(scenarios)}", file=sys.stderr)
        return 1

    required_fields = {
        "id", "skill", "user_prompt", "reference_checklist",
        "difficulty", "time_budget_without_skill_seconds", "time_budget_with_skill_seconds",
    }

    skills_seen: set[str] = set()
    for s in scenarios:
        missing = required_fields - set(s.keys())
        if missing:
            print(f"ERREUR: scenario {s.get('id')} manque {sorted(missing)}", file=sys.stderr)
            return 1

        skill_dir = ROOT / s["skill"]
        if not (skill_dir / "SKILL.md").exists():
            print(f"ERREUR: skill {s['skill']} introuvable ou SKILL.md manquant", file=sys.stderr)
            return 1

        if len(s["reference_checklist"]) < 3:
            print(
                f"ERREUR: scenario {s['id']} a une checklist trop courte ({len(s['reference_checklist'])} steps)",
                file=sys.stderr,
            )
            return 1

        if s["difficulty"] not in {"easy", "medium", "hard"}:
            print(f"ERREUR: difficulty invalide pour {s['id']} : {s['difficulty']}", file=sys.stderr)
            return 1

        # Budget temps : avec_skill doit etre plus bas que sans_skill (l'interet du skill)
        if s["time_budget_with_skill_seconds"] >= s["time_budget_without_skill_seconds"]:
            print(
                f"ERREUR: scenario {s['id']} a un budget avec_skill >= sans_skill "
                f"({s['time_budget_with_skill_seconds']} vs {s['time_budget_without_skill_seconds']})",
                file=sys.stderr,
            )
            return 1

        skills_seen.add(s["skill"])

    # Les 5 scenarios doivent couvrir au moins 4 skills differents
    if len(skills_seen) < 4:
        print(
            f"ERREUR: diversite de skills insuffisante : {len(skills_seen)} skills couverts "
            f"({sorted(skills_seen)}), attendu >= 4",
            file=sys.stderr,
        )
        return 1

    print(f"baseline_scenarios_ok={len(scenarios)}")
    print(f"skills_couverts={len(skills_seen)}")
    print(f"skills={sorted(skills_seen)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
