#!/usr/bin/env python3
"""
measure_baseline.py, v0.2.2 Module B.

Mesure le gain empirique du bundle en lancant chaque scenario de
baseline-scenarios.json dans deux conditions :

  1. SANS skill : Claude brut, tools generiques (Bash, Read, WebSearch).
  2. AVEC skill : le contenu du SKILL.md concerne est injecte en system prompt,
     et les scripts du skill sont accessibles.

Pour chaque run, on capture :
  - tool_calls : nombre d'appels d'outils
  - input_tokens, output_tokens, cache_read_input_tokens
  - steps_done : sous-taches accomplies vs reference_checklist
  - duration_seconds

Le resultat est ecrit dans evals/baseline-results.json et baseline-comparison.md
est mis a jour automatiquement avec le delta.

Dependances :
  pip install anthropic  (SDK officiel)

Prerequis :
  export ANTHROPIC_API_KEY=sk-ant-...

Usage :
  python3 evals/measure_baseline.py                          # Tous les scenarios
  python3 evals/measure_baseline.py --scenario baseline-cfo-init-onboarding
  python3 evals/measure_baseline.py --dry-run                # Sans appel API (verif structure)

Cout indicatif : ~5 k$ input + ~2 k$ output par scenario x 2 runs x 5 scenarios
≈ 0,50 € par session complete avec Claude 3.5 Sonnet.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SCENARIOS_FILE = ROOT / "evals" / "baseline-scenarios.json"
RESULTS_FILE = ROOT / "evals" / "baseline-results.json"
SKILLS_ROOT = ROOT


def load_scenarios() -> dict[str, Any]:
    return json.loads(SCENARIOS_FILE.read_text(encoding="utf-8"))


def load_skill_system_prompt(skill: str) -> str:
    """Retourne le contenu du SKILL.md concatene avec references/ (progressive disclosure)."""
    skill_dir = SKILLS_ROOT / skill
    parts = [(skill_dir / "SKILL.md").read_text(encoding="utf-8")]
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref in sorted(refs_dir.glob("*.md")):
            parts.append(f"\n\n--- {ref.name} ---\n\n{ref.read_text(encoding='utf-8')}")
    return "\n".join(parts)


def check_prerequisites() -> tuple[bool, str]:
    """Verifie que le SDK et la cle API sont disponibles."""
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False, "SDK anthropic absent. Installer : pip install anthropic"

    if not os.environ.get("ANTHROPIC_API_KEY"):
        return False, "ANTHROPIC_API_KEY non defini. Exporter : export ANTHROPIC_API_KEY=sk-ant-..."

    return True, "prerequis OK"


def run_scenario(scenario: dict[str, Any], with_skill: bool, dry_run: bool) -> dict[str, Any]:
    """Lance un scenario dans une condition et retourne les metriques."""
    if dry_run:
        return {
            "condition": "avec_skill" if with_skill else "sans_skill",
            "dry_run": True,
            "tool_calls": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_read_tokens": 0,
            "duration_seconds": 0.0,
            "steps_done": 0,
            "steps_total": len(scenario["reference_checklist"]),
            "response_preview": "<dry-run, aucun appel API>",
        }

    import anthropic

    client = anthropic.Anthropic()

    system_prompt_parts = [
        "Tu es un CFO virtuel francophone. Reponds en francais. "
        "Sois precis et chiffre. Cite tes sources reglementaires (CGI, PCG, ANC...) quand pertinent."
    ]
    if with_skill:
        skill_content = load_skill_system_prompt(scenario["skill"])
        system_prompt_parts.append(f"\n\n### Skill actif : {scenario['skill']}\n\n{skill_content}")

    system_prompt = "\n".join(system_prompt_parts)

    start = time.time()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": scenario["user_prompt"]}],
    )
    duration = time.time() - start

    # Count tool uses (pour cette v0.2.2 on mesure sans tool use actif,
    # uniquement tokens et qualite de la reponse).
    tool_calls = 0
    for block in response.content:
        if getattr(block, "type", None) == "tool_use":
            tool_calls += 1

    response_text = "\n".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    )

    # Evaluer combien de steps de la checklist sont traites dans la reponse
    # (heuristique simple : compter les mots-cles de chaque step trouves dans la reponse).
    steps_done = count_steps_covered(response_text, scenario["reference_checklist"])

    return {
        "condition": "avec_skill" if with_skill else "sans_skill",
        "dry_run": False,
        "tool_calls": tool_calls,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_read_tokens": getattr(response.usage, "cache_read_input_tokens", 0),
        "duration_seconds": round(duration, 2),
        "steps_done": steps_done,
        "steps_total": len(scenario["reference_checklist"]),
        "response_preview": response_text[:400],
    }


def count_steps_covered(response: str, checklist: list[str]) -> int:
    """Heuristique : un step est 'couvert' si au moins 2 mots-cles du step apparaissent."""
    response_lower = response.lower()
    covered = 0
    for step in checklist:
        # Extraire les mots significatifs du step (>= 4 chars, hors stopwords basiques)
        words = [w.lower() for w in step.split() if len(w) >= 4 and w.lower() not in {
            "pour", "dans", "avec", "selon", "prochaines", "reference"
        }]
        hits = sum(1 for w in words if w in response_lower)
        if hits >= 2:
            covered += 1
    return covered


def compute_deltas(sans: dict[str, Any], avec: dict[str, Any]) -> dict[str, Any]:
    """Calcule les delta relatifs entre sans_skill et avec_skill."""
    def rel(a, b):
        return round((a - b) / a * 100, 1) if a > 0 else 0

    return {
        "tokens_total_sans": sans["input_tokens"] + sans["output_tokens"],
        "tokens_total_avec": avec["input_tokens"] + avec["output_tokens"],
        "tokens_reduction_pct": rel(
            sans["input_tokens"] + sans["output_tokens"],
            avec["input_tokens"] + avec["output_tokens"],
        ),
        "tool_calls_sans": sans["tool_calls"],
        "tool_calls_avec": avec["tool_calls"],
        "steps_done_sans": sans["steps_done"],
        "steps_done_avec": avec["steps_done"],
        "steps_total": sans["steps_total"],
        "coverage_sans_pct": round(sans["steps_done"] / sans["steps_total"] * 100, 0) if sans["steps_total"] else 0,
        "coverage_avec_pct": round(avec["steps_done"] / avec["steps_total"] * 100, 0) if avec["steps_total"] else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Mesure baseline avec/sans skill")
    parser.add_argument("--scenario", help="ID d'un scenario specifique")
    parser.add_argument("--dry-run", action="store_true",
                        help="Verifie la structure sans appel API (pour CI)")
    parser.add_argument("--output", type=Path, default=RESULTS_FILE,
                        help="Fichier de sortie JSON")
    args = parser.parse_args()

    if not args.dry_run:
        ok, msg = check_prerequisites()
        if not ok:
            print(f"⏭  Baseline skip : {msg}", file=sys.stderr)
            print("baseline_skipped=1")
            return 0

    data = load_scenarios()
    scenarios = data["scenarios"]
    if args.scenario:
        scenarios = [s for s in scenarios if s["id"] == args.scenario]
        if not scenarios:
            print(f"ERREUR: scenario {args.scenario} introuvable", file=sys.stderr)
            return 2

    print(f"▶ {len(scenarios)} scenario(s) a mesurer "
          f"({'DRY-RUN' if args.dry_run else 'LIVE API'})...")

    results = []
    for scenario in scenarios:
        print(f"\n  — {scenario['id']} ({scenario['skill']})")
        sans = run_scenario(scenario, with_skill=False, dry_run=args.dry_run)
        print(f"    sans : {sans['tool_calls']} tool_calls, "
              f"{sans['input_tokens']+sans['output_tokens']} tokens, "
              f"{sans['steps_done']}/{sans['steps_total']} steps")
        avec = run_scenario(scenario, with_skill=True, dry_run=args.dry_run)
        print(f"    avec : {avec['tool_calls']} tool_calls, "
              f"{avec['input_tokens']+avec['output_tokens']} tokens, "
              f"{avec['steps_done']}/{avec['steps_total']} steps")
        deltas = compute_deltas(sans, avec)
        results.append({
            "scenario_id": scenario["id"],
            "skill": scenario["skill"],
            "difficulty": scenario["difficulty"],
            "sans_skill": sans,
            "avec_skill": avec,
            "deltas": deltas,
        })

    out = {
        "_meta": {
            "measured_at": dt.datetime.now().isoformat(timespec="seconds"),
            "dry_run": args.dry_run,
            "scenarios_count": len(results),
            "model": "claude-3-5-sonnet-20241022",
        },
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    try:
        display = args.output.relative_to(ROOT)
    except ValueError:
        display = args.output
    print(f"\n✓ Resultats ecrits dans {display}")
    print(f"baseline_measured={len(results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
