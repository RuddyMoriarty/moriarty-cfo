#!/usr/bin/env python3
"""
Agrège les résultats de baseline-comparison en un rapport markdown.

Lit les outputs JSON produits par baseline_runner.py (à venir v0.2) et génère
un tableau récapitulatif avec deltas.

Pour l'instant : stub minimal, à enrichir quand baseline_runner.py existera.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
RESULTS_DIR = EVALS / "results"


def main() -> int:
    if not RESULTS_DIR.exists():
        print("# Benchmark Report\n")
        print(f"_{datetime.now().isoformat()}_\n")
        print("⚠️ Pas de résultats de baseline disponibles dans `evals/results/`.")
        print("Exécuter `evals/baseline_runner.py` (à venir v0.2) pour générer les données.")
        return 0

    results = []
    for f in sorted(RESULTS_DIR.glob("*.json")):
        try:
            results.append(json.loads(f.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            print(f"⚠️ Ignoré (JSON invalide) : {f}", file=sys.stderr)

    if not results:
        print("# Benchmark Report\n_Aucun résultat exploitable_")
        return 0

    print("# Benchmark Report, moriarty-cfo")
    print(f"\n_Généré le {datetime.now().isoformat()}_\n")
    print("| Skill | Tâche | Tool calls Δ | Tokens Δ | Étapes Δ |")
    print("|-------|-------|--------------|----------|----------|")
    for r in results:
        delta_tools = (r["with_skill"]["tool_calls"] - r["without_skill"]["tool_calls"]) / max(1, r["without_skill"]["tool_calls"]) * 100
        delta_tokens = (r["with_skill"]["tokens"] - r["without_skill"]["tokens"]) / max(1, r["without_skill"]["tokens"]) * 100
        delta_steps = (r["with_skill"]["steps_missed"] - r["without_skill"]["steps_missed"]) / max(1, r["without_skill"]["steps_missed"]) * 100
        print(f"| {r['skill']} | {r['test_label']} | {delta_tools:+.0f}% | {delta_tokens:+.0f}% | {delta_steps:+.0f}% |")

    return 0


if __name__ == "__main__":
    sys.exit(main())
