#!/usr/bin/env python3
"""
check_coverage_setup.py, verifie la configuration coverage.

Test statique (pas de run_coverage reel) qui valide :
  1. `.coveragerc` existe et est syntaxiquement valide (INI)
  2. `source` liste les 10 skills du bundle
  3. `parallel = true` est active (necessaire pour subprocess)
  4. `evals/_coverage_bootstrap/sitecustomize.py` existe
  5. `evals/run_coverage.py` existe et importable

Pas besoin que `coverage` soit installe : on teste uniquement la config.
"""

from __future__ import annotations

import configparser
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXPECTED_SKILLS = [
    "cfo-init", "cfo-comptabilite", "cfo-tresorerie", "cfo-reporting",
    "cfo-controle-gestion", "cfo-budget-forecast", "cfo-fiscalite",
    "cfo-risques-conformite", "cfo-financement-croissance", "cfo-csrd-esg",
]


def check_coveragerc_exists() -> tuple[bool, str]:
    rc = ROOT / ".coveragerc"
    if not rc.exists():
        return False, f".coveragerc absent : {rc}"
    return True, f".coveragerc present ({rc.stat().st_size} octets)"


def check_coveragerc_valid() -> tuple[bool, str]:
    rc = ROOT / ".coveragerc"
    if not rc.exists():
        return False, ".coveragerc absent"
    parser = configparser.ConfigParser()
    try:
        parser.read(rc, encoding="utf-8")
    except configparser.Error as e:
        return False, f"parsing KO : {e}"
    required_sections = ["run", "report"]
    missing = [s for s in required_sections if s not in parser.sections()]
    if missing:
        return False, f"sections manquantes : {missing}"
    return True, f"{len(parser.sections())} sections"


def check_coveragerc_sources() -> tuple[bool, str]:
    rc = ROOT / ".coveragerc"
    parser = configparser.ConfigParser()
    parser.read(rc, encoding="utf-8")
    sources = parser.get("run", "source", fallback="")
    source_list = [s.strip() for s in sources.splitlines() if s.strip()]
    missing = [s for s in EXPECTED_SKILLS if s not in source_list]
    if missing:
        return False, f"skills manquants dans source : {missing}"
    return True, f"{len(source_list)} sources listees"


def check_coveragerc_parallel() -> tuple[bool, str]:
    rc = ROOT / ".coveragerc"
    parser = configparser.ConfigParser()
    parser.read(rc, encoding="utf-8")
    parallel = parser.get("run", "parallel", fallback="false").lower()
    if parallel != "true":
        return False, f"parallel={parallel} (attendu true pour subprocess tracking)"
    return True, "parallel=true"


def check_sitecustomize() -> tuple[bool, str]:
    sc = ROOT / "evals" / "_coverage_bootstrap" / "sitecustomize.py"
    if not sc.exists():
        return False, f"sitecustomize.py absent : {sc}"
    text = sc.read_text(encoding="utf-8")
    if "coverage.process_startup" not in text:
        return False, "sitecustomize.py ne contient pas coverage.process_startup()"
    if "COVERAGE_PROCESS_START" not in text:
        return False, "sitecustomize.py ne check pas COVERAGE_PROCESS_START"
    return True, "bootstrap OK"


def check_run_coverage_script() -> tuple[bool, str]:
    rc = ROOT / "evals" / "run_coverage.py"
    if not rc.exists():
        return False, f"evals/run_coverage.py absent"
    # Check py_compile
    import py_compile
    try:
        py_compile.compile(str(rc), doraise=True)
    except py_compile.PyCompileError as e:
        return False, f"compile KO : {e}"
    return True, "script OK et compile"


def main() -> int:
    checks = [
        ("coveragerc_exists", check_coveragerc_exists),
        ("coveragerc_valid", check_coveragerc_valid),
        ("coveragerc_sources", check_coveragerc_sources),
        ("coveragerc_parallel", check_coveragerc_parallel),
        ("sitecustomize", check_sitecustomize),
        ("run_coverage_script", check_run_coverage_script),
    ]
    ok = 0
    for name, fn in checks:
        try:
            passed, detail = fn()
        except Exception as e:
            passed, detail = False, f"exception {type(e).__name__}: {e}"
        status = "OK" if passed else "KO"
        print(f"[{status}] {name} : {detail}")
        if passed:
            ok += 1

    if ok == len(checks):
        print(f"coverage_setup_ok={ok}")
        return 0
    print(f"ERREUR: {len(checks) - ok} check(s) KO", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
