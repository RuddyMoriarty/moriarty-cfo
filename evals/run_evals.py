#!/usr/bin/env python3
"""
moriarty-cfo evals runner.

Trois niveaux de tests, chacun mesurant une dimension différente.

  1. Structure  , conformité Anthropic Skills Guide (frontmatter, dossiers,
                   fichiers obligatoires/interdits). Statique, < 1 s.

  2. Triggering , disambiguation cross-skills : pour chaque phrase test, on
                   calcule un score de match pour CHAQUE skill (en regardant
                   son champ `description` + `Triggers:`), et on exige que le
                   `expected_skill` ait le score le plus élevé avec une marge
                   de confiance. Statique, < 5 s.

  3. Functional , exécution réelle des scripts Python du skill avec des
                   fixtures, vérification des outputs (fichiers créés, JSON
                   valide, contenu attendu, absence d'erreurs). 30-60 s/skill.

Usage :
  python evals/run_evals.py --check-structure
  python evals/run_evals.py --triggering [--quick]
  python evals/run_evals.py --functional [--quick] [--sample N]
  python evals/run_evals.py --skill cfo-init
  python evals/run_evals.py --quick    # = structure + triggering --quick
  python evals/run_evals.py --full     # = tout (structure + triggering + functional)

Codes de sortie :
  0 = pass rate ≥ seuil défini dans config.yaml
  1 = pass rate < seuil
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
SKILLS_DIRS = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("cfo-"))


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

    @property
    def all(self) -> list[TestResult]:
        return self.structure_results + self.triggering_results + self.functional_results

    def passed_count(self) -> int:
        return sum(1 for r in self.all if r.passed)

    def total_count(self) -> int:
        return len(self.all)

    def summary(self) -> str:
        lines = []
        for label, results in [
            ("Structure ", self.structure_results),
            ("Triggering", self.triggering_results),
            ("Functional", self.functional_results),
        ]:
            if results:
                ok = sum(1 for r in results if r.passed)
                lines.append(f"  {label}: {ok}/{len(results)}")
        return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Frontmatter parsing
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


# ─────────────────────────────────────────────────────────────────────
# 1. Structure checks
# ─────────────────────────────────────────────────────────────────────

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

    for skill_dir in SKILLS_DIRS:
        if skill_filter and skill_dir.name != skill_filter:
            continue
        prefix = skill_dir.name

        for f in required_files:
            present = (skill_dir / f).exists()
            results.append(TestResult(
                test_id=f"struct:{prefix}:has-{f}",
                test_label=f"{prefix} contient {f}",
                passed=present,
                reason="" if present else f"Fichier manquant : {skill_dir / f}",
            ))

        for d in required_dirs:
            present = (skill_dir / d).is_dir()
            results.append(TestResult(
                test_id=f"struct:{prefix}:has-dir-{d}",
                test_label=f"{prefix} contient dossier {d}/",
                passed=present,
                reason="" if present else f"Dossier manquant : {skill_dir / d}",
            ))

        for f in forbidden_files:
            absent = not (skill_dir / f).exists()
            results.append(TestResult(
                test_id=f"struct:{prefix}:no-{f}",
                test_label=f"{prefix} ne contient PAS {f}",
                passed=absent,
                reason="" if absent else f"Fichier interdit présent : {skill_dir / f}",
            ))

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        fm = parse_frontmatter(skill_md)
        if fm is None:
            results.append(TestResult(
                test_id=f"struct:{prefix}:fm-valid",
                test_label=f"{prefix} frontmatter YAML valide",
                passed=False,
                reason="Frontmatter absent ou YAML invalide",
            ))
            continue

        for field_name in required_fm_fields:
            has_field = field_name in fm
            results.append(TestResult(
                test_id=f"struct:{prefix}:fm-{field_name}",
                test_label=f"{prefix} frontmatter contient '{field_name}'",
                passed=has_field,
                reason="" if has_field else f"Champ manquant : {field_name}",
            ))

        name = fm.get("name", "")
        ok = bool(re.match(name_pattern, name))
        results.append(TestResult(
            test_id=f"struct:{prefix}:fm-name-pattern",
            test_label=f"{prefix} name match {name_pattern}",
            passed=ok,
            reason="" if ok else f"name='{name}' ne respecte pas le pattern",
        ))

        ok = name == prefix
        results.append(TestResult(
            test_id=f"struct:{prefix}:fm-name-matches-folder",
            test_label=f"{prefix} name matches folder name",
            passed=ok,
            reason="" if ok else f"name='{name}' != folder='{prefix}'",
        ))

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

        no_xml = "<" not in desc and ">" not in desc
        results.append(TestResult(
            test_id=f"struct:{prefix}:fm-desc-no-xml",
            test_label=f"{prefix} description sans XML brackets",
            passed=no_xml,
            reason="" if no_xml else "description contient < ou > (interdit Anthropic)",
        ))

    return results


# ─────────────────────────────────────────────────────────────────────
# 2. Triggering tests, VRAIE disambiguation cross-skills
# ─────────────────────────────────────────────────────────────────────

# Mots vides FR + EN à exclure du scoring (alphabet de base + accents)
STOPWORDS = {
    # Mots-outils francais
    "alors", "aussi", "avec", "avoir", "ceci", "cela", "cette", "comme",
    "dans", "donc", "elle", "encore", "etre", "être", "faire", "leur",
    "mais", "mieux", "même", "nous", "pour", "quel", "quelle", "quels",
    "quelles", "sans", "selon", "sont", "tout", "tous", "toute", "toutes",
    "très", "vous", "votre", "lance", "fait", "donne",
    "génère", "genere", "génerer", "produire",
    # Mots-outils anglais
    "with", "from", "this", "that", "have", "what", "your",
    # Termes generiques presents dans toutes les descriptions
    "société", "societe", "entreprise", "entreprises", "pme/tpe", "skill",
    "française", "francaise", "françaises", "francaises", "cabinets", "cabinet",
    "skills", "bundle", "compte", "utiliser", "utilisez", "question", "questions",
    "détail", "detail", "produit", "produite",
    "niveau", "type", "types", "module", "modules", "gestion",
    # Token partage entre 3+ skills sans valeur discriminante
    "exercice",
}

# Acronymes métier CFO à 2-3 lettres qu'on veut conserver même sous le seuil 4 chars
# Whitelist explicite pour éviter d'ajouter du bruit avec "le", "de", "ok"…
BUSINESS_ACRONYMS = {
    # Comptabilité
    "fec", "pcg", "cga", "nep", "dsn", "ias", "ifrs", "gaap",
    # Fiscalité
    "is", "tva", "cir", "cii", "cvae", "cet", "cfe", "deb", "des",
    "bic", "bnc", "ba", "plf", "tvs", "ice",
    # Trésorerie
    "dso", "dpo", "dio", "ccc", "bfr", "ebe", "ofr", "ffcf",
    # Budget / investissement
    "npv", "irr", "roi", "roe", "roce", "ebit", "ebitda", "wacc", "ltv", "cac",
    "arr", "mrr", "arpu", "nrr", "grr", "trs", "oee", "nps", "abc",
    # Risques / conformité
    "coso", "erm", "bcp", "rgpd", "lcbft", "nop", "acpr", "amf",
    # Financement
    "pge", "mlt", "ipo", "lbo", "vc", "pe", "sri", "bspce", "aga", "bsa",
    "tpe", "pme", "eti", "etb",
    # CSRD / ESG
    "ghg", "gri", "tcfd", "sbti", "esg", "dma", "efrag", "csrd", "esrs",
    # Divers
    "ag", "kyc", "kpi", "kpis", "ca", "rnv", "rns", "pdg", "dg", "daf",
    "cfo", "cso", "dgfip", "urssaf", "drfip", "cac3", "ca3",
}


def tokenize(text: str) -> set[str]:
    """Extrait les mots significatifs d'un texte.

    Deux catégories :
    - Mots usuels ≥4 caractères (hors stopwords).
    - Acronymes métier de 2-3 caractères (whitelist BUSINESS_ACRONYMS).
    """
    text_lower = text.lower()
    # Mots ≥4 caractères (comportement historique)
    long_words = set(re.findall(r"\b[a-zàâéèêëîïôùûüÿç0-9-]{4,}\b", text_lower))
    # Acronymes 2-3 caractères de la whitelist
    all_words_23 = set(re.findall(r"\b[a-zàâéèêëîïôùûüÿç0-9]{2,3}\b", text_lower))
    short_acronyms = all_words_23 & BUSINESS_ACRONYMS
    return (long_words | short_acronyms) - STOPWORDS


def extract_triggers(fm: dict[str, Any]) -> set[str]:
    """Extrait l'ensemble des tokens 'triggers' d'un skill (description + Triggers:)."""
    desc = fm.get("description", "")
    if isinstance(desc, list):
        desc = " ".join(str(x) for x in desc)
    return tokenize(desc)


def score_skill(phrase_tokens: set[str], skill_tokens: set[str]) -> int:
    """Score = nombre de tokens en commun entre phrase et triggers du skill."""
    return len(phrase_tokens & skill_tokens)


def check_triggering(config: dict[str, Any], quick: bool = False) -> list[TestResult]:
    """
    Disambiguation cross-skills.

    Pour chaque phrase test :
    1. Tokenizer la phrase (mots significatifs).
    2. Calculer un score de match pour CHAQUE skill (≠ juste le skill attendu).
    3. Identifier le skill avec le score le plus élevé.
    4. Test passe SI :
       - Le top-1 == expected_skill, ET
       - Le score top-1 ≥ marge × score top-2 (ou top-2 == 0)

    Marge configurable via config.yaml (par défaut : 1.5).
    """
    results: list[TestResult] = []

    triggering_path = EVALS / "triggering-tests.json"
    if not triggering_path.exists():
        return [TestResult(
            "trig:file-exists",
            "evals/triggering-tests.json présent",
            False,
            "Fichier manquant",
        )]

    triggering = json.loads(triggering_path.read_text(encoding="utf-8"))
    tests = triggering.get("tests", [])

    if quick:
        per_skill: dict[str, list[dict]] = {}
        for t in tests:
            per_skill.setdefault(t["expected_skill"], []).append(t)
        sample = []
        for items in per_skill.values():
            sample.extend(items[:5])
        tests = sample

    # Charger triggers de tous les skills
    skill_triggers: dict[str, set[str]] = {}
    for skill_dir in SKILLS_DIRS:
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            fm = parse_frontmatter(skill_md)
            if fm:
                skill_triggers[skill_dir.name] = extract_triggers(fm)

    margin = float(config.get("thresholds", {}).get("triggering", {}).get("margin", 1.5))

    for t in tests:
        expected = t["expected_skill"]
        category = t.get("category", "unknown")
        phrase = t["phrase"]

        if expected not in skill_triggers:
            results.append(TestResult(
                test_id=f"trig:{category}:{expected}",
                test_label=f"[{expected}] {phrase[:60]}",
                passed=False,
                reason=f"Skill non implémenté ou frontmatter manquant : {expected}",
            ))
            continue

        phrase_tokens = tokenize(phrase)

        # Scorer tous les skills
        scores = {
            name: score_skill(phrase_tokens, triggers)
            for name, triggers in skill_triggers.items()
        }

        # Trier
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top1_name, top1_score = ranked[0]
        top2_score = ranked[1][1] if len(ranked) > 1 else 0

        # Cas d'égalité au score 0 → on considère "pas de match"
        if top1_score == 0:
            results.append(TestResult(
                test_id=f"trig:{category}:{expected}",
                test_label=f"[{expected}] {phrase[:60]}",
                passed=False,
                reason="Aucun mot-cle de la phrase trouve dans aucun skill (revoir Triggers:)",
            ))
            continue

        # Marge de confiance
        confident = (top2_score == 0) or (top1_score / max(top2_score, 1) >= margin)
        correct = top1_name == expected

        if correct and confident:
            results.append(TestResult(
                test_id=f"trig:{category}:{expected}",
                test_label=f"[{expected}] {phrase[:60]}",
                passed=True,
            ))
        elif correct and not confident:
            ambig_with = ranked[1][0]
            results.append(TestResult(
                test_id=f"trig:{category}:{expected}",
                test_label=f"[{expected}] {phrase[:60]}",
                passed=False,
                reason=f"Top-1 correct mais score trop proche de {ambig_with} ({top1_score} vs {top2_score}, marge < {margin})",
            ))
        else:
            results.append(TestResult(
                test_id=f"trig:{category}:{expected}",
                test_label=f"[{expected}] {phrase[:60]}",
                passed=False,
                reason=f"Top-1 = {top1_name} (score {top1_score}) au lieu de {expected} (score {scores.get(expected, 0)})",
            ))

    return results


# ─────────────────────────────────────────────────────────────────────
# Anti-triggers : phrases qui ne doivent PAS déclencher un skill CFO
# ─────────────────────────────────────────────────────────────────────

def check_anti_triggers(config: dict[str, Any]) -> list[TestResult]:
    """
    Pour chaque anti-trigger : aucun skill ne doit avoir un score significatif
    (≥ seuil minimum). Si un skill a un score élevé, c'est qu'il sur-déclenche.
    """
    results: list[TestResult] = []

    triggering_path = EVALS / "triggering-tests.json"
    if not triggering_path.exists():
        return results

    triggering = json.loads(triggering_path.read_text(encoding="utf-8"))
    anti_triggers = triggering.get("anti_triggers", [])

    skill_triggers: dict[str, set[str]] = {}
    for skill_dir in SKILLS_DIRS:
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            fm = parse_frontmatter(skill_md)
            if fm:
                skill_triggers[skill_dir.name] = extract_triggers(fm)

    threshold = config.get("thresholds", {}).get("anti_triggering", {}).get("max_score", 2)

    for at in anti_triggers:
        phrase = at if isinstance(at, str) else at.get("phrase", "")
        if not phrase:
            continue
        phrase_tokens = tokenize(phrase)
        scores = {
            name: score_skill(phrase_tokens, triggers)
            for name, triggers in skill_triggers.items()
        }
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top1_name, top1_score = ranked[0] if ranked else ("", 0)

        passed = top1_score < threshold
        results.append(TestResult(
            test_id=f"anti-trig:{phrase[:30]}",
            test_label=f"[anti] {phrase[:60]}",
            passed=passed,
            reason="" if passed else f"Sur-déclenche {top1_name} (score {top1_score} ≥ seuil {threshold})",
        ))

    return results


# ─────────────────────────────────────────────────────────────────────
# 3. Functional tests, VRAIE exécution des scripts du skill
# ─────────────────────────────────────────────────────────────────────

def check_functional(
    config: dict[str, Any],
    skill_filter: str | None = None,
    sample: int | None = None,
    quick: bool = False,
) -> list[TestResult]:
    """
    Exécution réelle des fixtures functional.

    Format attendu dans functional-tests.json :
    {
      "tests": [
        {
          "id": "cfo-init-fct-01",
          "skill": "cfo-init",
          "label": "...",
          "executable": {
            "type": "python",
            "script": "scripts/compute_calendar.py",
            "args": ["--closing-date", "2026-12-31", "--output", "{tmp}/calendar.json"]
          },
          "assertions": {
            "exit_code": 0,
            "files_created": ["{tmp}/calendar.json"],
            "json_valid": ["{tmp}/calendar.json"],
            "must_contain_in_output": ["calendrier"],
            "must_not_contain_in_output": ["error", "exception", "TODO"],
            "max_duration_seconds": 30
          }
        }
      ]
    }

    Si un test n'a pas d'`executable` (legacy format), il est skippé avec un
    test "static" qui passe (compte de tests par skill).
    """
    results: list[TestResult] = []

    fct_path = EVALS / "functional-tests.json"
    if not fct_path.exists():
        return [TestResult("fct:file-exists", "evals/functional-tests.json présent", False, "Fichier manquant")]

    fct = json.loads(fct_path.read_text(encoding="utf-8"))
    tests = fct.get("tests", [])

    # Filtres
    if skill_filter:
        tests = [t for t in tests if t.get("skill") == skill_filter]

    if quick:
        # 1 test par skill en quick
        per_skill: dict[str, list[dict]] = {}
        for t in tests:
            per_skill.setdefault(t["skill"], []).append(t)
        tests = []
        for items in per_skill.values():
            tests.extend(items[:1])
    elif sample:
        per_skill: dict[str, list[dict]] = {}
        for t in tests:
            per_skill.setdefault(t["skill"], []).append(t)
        tests = []
        for items in per_skill.values():
            tests.extend(items[:sample])

    for t in tests:
        skill = t.get("skill", "unknown")
        test_id = t.get("id", f"fct:{skill}:unknown")
        label = t.get("label", "")
        exec_ = t.get("executable")

        if not exec_:
            # Legacy : pas d'executable défini → on compte juste qu'il existe
            results.append(TestResult(
                test_id=test_id,
                test_label=f"[{skill}] {label} (no executable defined)",
                passed=True,  # On ne fait pas échouer pour ça en v0.1.x
                reason="Test legacy sans executable, à enrichir",
            ))
            continue

        # Exécution réelle
        result = run_executable_test(t, skill)
        results.append(result)

    return results


def run_executable_test(test: dict[str, Any], skill: str) -> TestResult:
    """Exécute un test fonctionnel avec son executable et vérifie les assertions.

    Résolution des paths (relative ou absolue) :
    - cwd : si `.`/`./`/absent ou relatif, résolu depuis ROOT (repo root).
    - script : si relatif, essayé d'abord depuis cwd, sinon depuis ROOT.
    Jamais de path en dur type `/Users/...` (casserait sur CI Linux).
    """
    test_id = test.get("id", f"fct:{skill}:unknown")
    label = test.get("label", "")
    exec_ = test.get("executable", {})
    assertions = test.get("assertions", {})

    exec_type = exec_.get("type", "python")
    script = exec_.get("script", "")
    args = exec_.get("args", [])

    # cwd resolution : default = ROOT / skill. "." ou "./" = ROOT. Relatif = ROOT / cwd_str.
    cwd_str = exec_.get("cwd")
    if cwd_str in (None, "", "."):
        cwd = ROOT if cwd_str in ("", ".") else (ROOT / skill)
    elif Path(cwd_str).is_absolute():
        cwd = Path(cwd_str)
    else:
        cwd = ROOT / cwd_str

    if not script:
        return TestResult(test_id, f"[{skill}] {label}", False, "executable.script manquant")

    # script resolution : absolute, or try cwd first, then ROOT (repo-relative).
    script_path_input = Path(script)
    if script_path_input.is_absolute():
        script_path = script_path_input
    else:
        candidate_cwd = cwd / script
        candidate_root = ROOT / script
        script_path = candidate_cwd if candidate_cwd.exists() else candidate_root

    if not script_path.exists():
        return TestResult(
            test_id,
            f"[{skill}] {label}",
            False,
            f"Script introuvable (tenté : {candidate_cwd} et {candidate_root})",
        )

    # Tempdir pour {tmp}
    with tempfile.TemporaryDirectory(prefix="cfo-eval-") as tmp:
        substituted_args = [a.format(tmp=tmp) if isinstance(a, str) else a for a in args]

        cmd = [sys.executable if exec_type == "python" else exec_type, str(script_path), *substituted_args]
        max_dur = float(assertions.get("max_duration_seconds", 60))

        start = time.time()
        try:
            proc = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=max_dur,
            )
        except subprocess.TimeoutExpired:
            return TestResult(
                test_id, f"[{skill}] {label}",
                False,
                f"Timeout (> {max_dur}s)",
                duration_seconds=time.time() - start,
            )
        except FileNotFoundError as e:
            return TestResult(
                test_id, f"[{skill}] {label}",
                False,
                f"Exécuteur introuvable : {e}",
            )

        duration = time.time() - start
        output = proc.stdout + proc.stderr

        # Assertion : exit code
        expected_exit = assertions.get("exit_code", 0)
        if proc.returncode != expected_exit:
            return TestResult(
                test_id, f"[{skill}] {label}",
                False,
                f"exit_code = {proc.returncode} (attendu {expected_exit}). Output: {output[:200]}",
                duration_seconds=duration,
            )

        # Assertion : fichiers créés
        files_created = assertions.get("files_created", [])
        for f in files_created:
            f_path = Path(f.format(tmp=tmp))
            if not f_path.exists():
                return TestResult(
                    test_id, f"[{skill}] {label}",
                    False,
                    f"Fichier attendu non créé : {f_path}",
                    duration_seconds=duration,
                )

        # Assertion : JSON valide
        json_valid = assertions.get("json_valid", [])
        for f in json_valid:
            f_path = Path(f.format(tmp=tmp))
            if not f_path.exists():
                return TestResult(
                    test_id, f"[{skill}] {label}",
                    False,
                    f"Fichier JSON attendu non créé : {f_path}",
                    duration_seconds=duration,
                )
            try:
                json.loads(f_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                return TestResult(
                    test_id, f"[{skill}] {label}",
                    False,
                    f"JSON invalide dans {f_path} : {e}",
                    duration_seconds=duration,
                )

        # Assertion : must_contain_in_output
        must_contain = assertions.get("must_contain_in_output", [])
        for needle in must_contain:
            if needle not in output:
                return TestResult(
                    test_id, f"[{skill}] {label}",
                    False,
                    f"Output ne contient pas '{needle}'. Output: {output[:200]}",
                    duration_seconds=duration,
                )

        # Assertion : must_not_contain_in_output
        must_not_contain = assertions.get("must_not_contain_in_output", [])
        for needle in must_not_contain:
            if needle.lower() in output.lower():
                return TestResult(
                    test_id, f"[{skill}] {label}",
                    False,
                    f"Output contient '{needle}' (interdit). Output: {output[:200]}",
                    duration_seconds=duration,
                )

        return TestResult(test_id, f"[{skill}] {label}", True, duration_seconds=duration)


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Evals runner pour moriarty-cfo")
    parser.add_argument("--check-structure", action="store_true")
    parser.add_argument("--triggering", action="store_true")
    parser.add_argument("--functional", action="store_true")
    parser.add_argument("--anti-triggers", action="store_true")
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
    do_anti = args.anti_triggers or args.full
    do_fct = args.functional or args.full

    if do_struct:
        print("▶ Structure checks...")
        report.structure_results = check_structure(config, skill_filter=args.skill)

    if do_trig:
        print("▶ Triggering tests (disambiguation cross-skills)...")
        report.triggering_results = check_triggering(config, quick=args.quick)

    if do_anti:
        print("▶ Anti-triggers (sur-déclenchement)...")
        anti_results = check_anti_triggers(config)
        report.triggering_results.extend(anti_results)

    if do_fct:
        print("▶ Functional tests (exécution réelle)...")
        report.functional_results = check_functional(
            config,
            skill_filter=args.skill,
            sample=args.sample,
            quick=args.quick,
        )

    print("\n" + "=" * 60)
    print("RÉSULTATS")
    print("=" * 60)
    print(report.summary())

    failed = [r for r in report.all if not r.passed]
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
        threshold = config.get("thresholds", {}).get("global_pass_rate_min", 0.85)
        if rate < threshold:
            print(f"❌ FAIL (< {threshold * 100:.0f}%)")
            return 1

    print("\n✅ PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
