#!/usr/bin/env python3
"""
moriarty-cfo evals runner.

Exécute les 3 niveaux de tests (PDF Anthropic Skills Guide Ch. 3) :
  1. Triggering tests   — phrase déclenche-t-elle le bon skill ?
  2. Functional tests   — sortie produite est-elle correcte ?
  3. Structure checks   — frontmatter conforme, fichiers requis présents ?

Usage:
  python evals/run_evals.py --check-structure
  python evals/run_evals.py --triggering [--quick]
  python evals/run_evals.py --functional [--quick] [--sample N]
  python evals/run_evals.py --skill cfo-init
  python evals/run_evals.py --quick    # = --check-structure + --triggering --quick
  python evals/run_evals.py --full     # tout
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
SKILLS_DIRS = [p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("cfo-")]


# ─────────────────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────────────────

@dataclass
class TestResult:
    test_id: str
    test_label: str
    passed: bool
    reason: str = ""
    duration_seconds: float = 0.0


@dataclass
class Report:
    structure_results: list[TestResult] = field(default_factory=list)
    triggering_results: list[TestResult] = field(default_factory=list)
    functional_results: list[TestResult] = field(default_factory=list)

    def passed_count(self) -> int:
        return sum(
            1
            for r in self.structure_results + self.triggering_results + self.functional_results
            if r.passed
        )

    def total_count(self) -> int:
        return len(self.structure_results + self.triggering_results + self.functional_results)

    def summary(self) -> str:
        lines = []
        if self.structure_results:
            ok = sum(1 for r in self.structure_results if r.passed)
            lines.append(f"  Structure : {ok}/{len(self.structure_results)}")
        if self.triggering_results:
            ok = sum(1 for r in self.triggering_results if r.passed)
            lines.append(f"  Triggering: {ok}/{len(self.triggering_results)}")
        if self.functional_results:
            ok = sum(1 for r in self.functional_results if r.passed)
            lines.append(f"  Functional: {ok}/{len(self.functional_results)}")
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Structure checks
# ─────────────────────────────────────────────────────────────────────

def parse_frontmatter(skill_md_path: Path) -> dict[str, Any] | None:
    """Extrait le YAML frontmatter d'un SKILL.md. Renvoie None si absent."""
    text = skill_md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


def check_structure(config: dict[str, Any], skill_filter: str | None = None) -> list[TestResult]:
    results: list[TestResult] = []

    constraints = config.get("structure_checks", {})
    required_files = constraints.get("required_files_per_skill", ["SKILL.md"])
    required_dirs = constraints.get("required_dirs_per_skill", [])
    forbidden_files = constraints.get("forbidden_files_per_skill", ["README.md"])
    required_fm_fields = constraints.get("required_frontmatter_fields", ["name", "description"])
    fm_constraints = constraints.get("frontmatter_constraints", {})
    name_pattern = fm_constraints.get("name_pattern", "^cfo-[a-z][a-z0-9-]*$")
    desc_max = fm_constraints.get("description_max_length", 1024)

    for skill_dir in sorted(SKILLS_DIRS):
        if skill_filter and skill_dir.name != skill_filter:
            continue
        prefix = skill_dir.name

        # Fichiers requis
        for f in required_files:
            present = (skill_dir / f).exists()
            results.append(TestResult(
                test_id=f"struct:{prefix}:has-{f}",
                test_label=f"{prefix} contient {f}",
                passed=present,
                reason="" if present else f"Fichier manquant : {skill_dir / f}",
            ))

        # Dossiers requis
        for d in required_dirs:
            present = (skill_dir / d).is_dir()
            results.append(TestResult(
                test_id=f"struct:{prefix}:has-dir-{d}",
                test_label=f"{prefix} contient dossier {d}/",
                passed=present,
                reason="" if present else f"Dossier manquant : {skill_dir / d}",
            ))

        # Fichiers interdits (PDF règle : pas de README dans dossier de skill)
        for f in forbidden_files:
            absent = not (skill_dir / f).exists()
            results.append(TestResult(
                test_id=f"struct:{prefix}:no-{f}",
                test_label=f"{prefix} ne contient PAS {f}",
                passed=absent,
                reason="" if absent else f"Fichier interdit présent : {skill_dir / f}",
            ))

        # Frontmatter SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            fm = parse_frontmatter(skill_md)
            if fm is None:
                results.append(TestResult(
                    test_id=f"struct:{prefix}:fm-valid",
                    test_label=f"{prefix} frontmatter YAML valide",
                    passed=False,
                    reason="Frontmatter absent ou YAML invalide",
                ))
            else:
                for field_name in required_fm_fields:
                    has_field = field_name in fm
                    results.append(TestResult(
                        test_id=f"struct:{prefix}:fm-{field_name}",
                        test_label=f"{prefix} frontmatter contient '{field_name}'",
                        passed=has_field,
                        reason="" if has_field else f"Champ manquant : {field_name}",
                    ))
                # name kebab-case + commence par cfo-
                name = fm.get("name", "")
                ok = bool(re.match(name_pattern, name))
                results.append(TestResult(
                    test_id=f"struct:{prefix}:fm-name-pattern",
                    test_label=f"{prefix} name match {name_pattern}",
                    passed=ok,
                    reason="" if ok else f"name='{name}' ne respecte pas le pattern",
                ))
                # name == dossier
                ok = name == prefix
                results.append(TestResult(
                    test_id=f"struct:{prefix}:fm-name-matches-folder",
                    test_label=f"{prefix} name matches folder name",
                    passed=ok,
                    reason="" if ok else f"name='{name}' != folder='{prefix}'",
                ))
                # description longueur
                desc = fm.get("description", "")
                if isinstance(desc, list):
                    desc = " ".join(str(x) for x in desc)
                ok = len(desc) <= desc_max
                results.append(TestResult(
                    test_id=f"struct:{prefix}:fm-desc-length",
                    test_label=f"{prefix} description ≤ {desc_max} chars",
                    passed=ok,
                    reason="" if ok else f"description ({len(desc)} chars) dépasse {desc_max}",
                ))
                # Pas de XML brackets
                no_xml = "<" not in desc and ">" not in desc
                results.append(TestResult(
                    test_id=f"struct:{prefix}:fm-desc-no-xml",
                    test_label=f"{prefix} description sans XML brackets",
                    passed=no_xml,
                    reason="" if no_xml else "description contient < ou > (interdit Anthropic)",
                ))

    return results


# ─────────────────────────────────────────────────────────────────────
# Triggering tests (statique - vérification présence triggers dans frontmatter)
# ─────────────────────────────────────────────────────────────────────

def check_triggering_static(config: dict[str, Any], quick: bool = False) -> list[TestResult]:
    """
    Tests statiques de triggering : vérifie que le frontmatter de chaque skill
    contient des triggers cohérents avec les phrases attendues dans triggering-tests.json.

    Note : la véritable mesure (Claude déclenche-t-il bien le skill ?) requiert un appel
    à l'API Claude. Ce test statique est une approximation rapide pour le CI.
    """
    results: list[TestResult] = []

    triggering_path = EVALS / "triggering-tests.json"
    if not triggering_path.exists():
        results.append(TestResult(
            test_id="trig:file-exists",
            test_label="evals/triggering-tests.json présent",
            passed=False,
            reason="Fichier manquant",
        ))
        return results

    triggering = json.loads(triggering_path.read_text(encoding="utf-8"))
    tests = triggering.get("tests", [])
    if quick:
        # En mode quick, échantillonner 5 tests par skill
        per_skill: dict[str, list[dict]] = {}
        for t in tests:
            per_skill.setdefault(t["expected_skill"], []).append(t)
        sample = []
        for skill_name, items in per_skill.items():
            sample.extend(items[:5])
        tests = sample

    # Charger frontmatters
    frontmatters: dict[str, dict] = {}
    for skill_dir in SKILLS_DIRS:
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            fm = parse_frontmatter(skill_md)
            if fm:
                frontmatters[skill_dir.name] = fm

    for t in tests:
        expected_skill = t["expected_skill"]
        if expected_skill not in frontmatters:
            results.append(TestResult(
                test_id=f"trig:{t.get('category', 'unknown')}",
                test_label=f"[{expected_skill}] {t['phrase']}",
                passed=False,
                reason=f"Skill non implémenté ou frontmatter manquant : {expected_skill}",
            ))
            continue

        fm = frontmatters[expected_skill]
        desc = fm.get("description", "")
        if isinstance(desc, list):
            desc = " ".join(str(x) for x in desc)

        # Heuristique : au moins un mot-clé de la phrase test doit être dans description
        # ou dans une section "Triggers:" de description
        phrase_lower = t["phrase"].lower()
        keywords = re.findall(r"\b[a-zàâéèêëîïôùûüÿ]{4,}\b", phrase_lower)
        # On considère le test passé si ≥ 1 keyword apparaît dans la description
        match = any(k.lower() in desc.lower() for k in keywords)
        results.append(TestResult(
            test_id=f"trig:{t.get('category', 'unknown')}:{expected_skill}",
            test_label=f"[{expected_skill}] {t['phrase'][:60]}",
            passed=match,
            reason="" if match else f"Aucun mot-clé de la phrase trouvé dans description du skill",
        ))

    return results


# ─────────────────────────────────────────────────────────────────────
# Functional tests (statique - vérifie présence des outputs attendus)
# ─────────────────────────────────────────────────────────────────────

def check_functional_static(config: dict[str, Any], skill_filter: str | None = None, sample: int | None = None) -> list[TestResult]:
    """
    Tests fonctionnels statiques. Pour vrais tests fonctionnels (exécution end-to-end),
    nécessite une session Claude Code interactive. Ici on vérifie juste que les tests
    sont bien définis pour les skills implémentés.
    """
    results: list[TestResult] = []
    fct_path = EVALS / "functional-tests.json"
    if not fct_path.exists():
        return [TestResult("fct:file-exists", "evals/functional-tests.json présent", False, "Fichier manquant")]

    fct = json.loads(fct_path.read_text(encoding="utf-8"))
    tests = fct.get("tests", [])

    # Compter les tests par skill
    per_skill: dict[str, int] = {}
    for t in tests:
        skill = t.get("skill")
        if skill_filter and skill != skill_filter:
            continue
        per_skill[skill] = per_skill.get(skill, 0) + 1

    # Vérifier qu'on a au moins 3 tests par skill implémenté
    implemented_skills = [d.name for d in SKILLS_DIRS if (d / "SKILL.md").exists()]
    for skill in implemented_skills:
        if skill_filter and skill != skill_filter:
            continue
        n = per_skill.get(skill, 0)
        ok = n >= 3
        results.append(TestResult(
            test_id=f"fct:{skill}:test-count",
            test_label=f"{skill} a ≥ 3 tests fonctionnels",
            passed=ok,
            reason="" if ok else f"Seulement {n} test(s) défini(s)",
        ))

    return results


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Evals runner pour moriarty-cfo")
    parser.add_argument("--check-structure", action="store_true")
    parser.add_argument("--triggering", action="store_true")
    parser.add_argument("--functional", action="store_true")
    parser.add_argument("--quick", action="store_true", help="Subset rapide")
    parser.add_argument("--full", action="store_true", help="Suite complète")
    parser.add_argument("--skill", type=str, help="Filtrer sur un skill")
    parser.add_argument("--sample", type=int, default=None, help="Nb max de tests par skill")
    args = parser.parse_args()

    config_path = EVALS / "config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}

    report = Report()

    do_struct = args.check_structure or args.full or args.quick
    do_trig = args.triggering or args.full or args.quick
    do_fct = args.functional or args.full

    if do_struct:
        print("▶ Structure checks...")
        report.structure_results = check_structure(config, skill_filter=args.skill)

    if do_trig:
        print("▶ Triggering tests (statique)...")
        report.triggering_results = check_triggering_static(config, quick=args.quick)

    if do_fct:
        print("▶ Functional tests (statique)...")
        report.functional_results = check_functional_static(config, skill_filter=args.skill, sample=args.sample)

    # Affichage résultats
    print("\n" + "=" * 60)
    print("RÉSULTATS")
    print("=" * 60)
    print(report.summary())

    failed = [r for r in (
        report.structure_results + report.triggering_results + report.functional_results
    ) if not r.passed]

    if failed:
        print(f"\n❌ {len(failed)} test(s) FAILED:")
        for r in failed[:20]:
            print(f"  - {r.test_id}: {r.test_label}")
            if r.reason:
                print(f"      reason: {r.reason}")
        if len(failed) > 20:
            print(f"  ... et {len(failed) - 20} autres")

    total = report.total_count()
    passed = report.passed_count()
    if total:
        rate = passed / total
        print(f"\nGlobal pass rate: {passed}/{total} ({rate * 100:.1f}%)")
        if rate < 0.85:
            print("❌ FAIL (< 85%)")
            return 1

    print("\n✅ PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
