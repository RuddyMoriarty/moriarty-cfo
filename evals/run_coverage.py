#!/usr/bin/env python3
"""
run_coverage.py, mesure la coverage reelle des 27 scripts du bundle.

Lance les 65 tests fonctionnels sous `coverage run --parallel-mode` pour
capturer les subprocess Python spawnees par les tests. Agrege les fichiers
.coverage.* avec `coverage combine` puis genere un rapport texte + HTML.

Pre-requis :
  pip install coverage

Usage :
  python3 evals/run_coverage.py                          # Rapport texte
  python3 evals/run_coverage.py --html                   # + rapport HTML dans htmlcov/
  python3 evals/run_coverage.py --threshold 70           # Echec si < 70 % couverture

Skip proprement si coverage n'est pas installe (baseline_skipped=1).

Le rapport affiche :
  - % global
  - % par skill (10 skills)
  - lignes non couvertes par script (pour identifier les branches non testees)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def check_coverage_installed() -> tuple[bool, str]:
    try:
        import coverage  # noqa: F401
        return True, "coverage installe"
    except ImportError:
        return False, "coverage absent. Lancer : pip install coverage"


def clean_previous_data() -> None:
    """Supprime les .coverage et .coverage.* de la derniere mesure (PAS .coveragerc)."""
    main_file = ROOT / ".coverage"
    if main_file.is_file():
        try:
            main_file.unlink()
        except OSError:
            pass
    for p in ROOT.glob(".coverage.*"):
        # Skip .coveragerc (config file)
        if p.name == ".coveragerc":
            continue
        try:
            p.unlink()
        except OSError:
            pass
    htmlcov = ROOT / "htmlcov"
    if htmlcov.exists():
        import shutil
        shutil.rmtree(htmlcov, ignore_errors=True)


def run_tests_under_coverage() -> tuple[int, str]:
    """Lance evals/run_evals.py --functional sous coverage.

    Chaque subprocess Python heritant de l'env lancera notre sitecustomize.py
    qui appelle coverage.process_startup() (trace les lignes executees).
    """
    import os
    bootstrap_dir = ROOT / "evals" / "_coverage_bootstrap"
    existing_pp = os.environ.get("PYTHONPATH", "")
    # Prepend bootstrap pour que sitecustomize.py soit trouve
    new_pp = str(bootstrap_dir) + (os.pathsep + existing_pp if existing_pp else "")

    cmd = [
        sys.executable, "-m", "coverage", "run",
        "--parallel-mode",
        "--rcfile=.coveragerc",
        "evals/run_evals.py", "--functional",
    ]
    env = {
        **os.environ,
        "PYTHONPATH": new_pp,
        "COVERAGE_PROCESS_START": str(ROOT / ".coveragerc"),
    }
    proc = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def combine_data() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "coverage", "combine"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def generate_text_report() -> tuple[int, str, float]:
    """Retourne (exit, text, pct_global). pct_global = -1 si parsing echec."""
    proc = subprocess.run(
        [sys.executable, "-m", "coverage", "report"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    # Parser le % global depuis la derniere ligne "TOTAL"
    pct = -1.0
    for line in proc.stdout.splitlines():
        if line.strip().startswith("TOTAL"):
            parts = line.split()
            for part in parts:
                if part.endswith("%"):
                    try:
                        pct = float(part.rstrip("%"))
                    except ValueError:
                        pass
    return proc.returncode, proc.stdout, pct


def generate_html_report() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "coverage", "html"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    parser = argparse.ArgumentParser(description="Mesure coverage reelle du bundle")
    parser.add_argument("--html", action="store_true", help="Genere un rapport HTML dans htmlcov/")
    parser.add_argument("--threshold", type=float, default=0.0,
                        help="Echec si coverage < threshold %% (default 0 = no gate)")
    args = parser.parse_args()

    ok, msg = check_coverage_installed()
    if not ok:
        print(f"⏭  Coverage skip : {msg}", file=sys.stderr)
        print("coverage_skipped=1")
        return 0

    print("▶ Nettoyage des donnees precedentes...")
    clean_previous_data()

    print("▶ Execution des tests sous coverage...")
    rc, output = run_tests_under_coverage()
    if rc != 0:
        print(f"⚠ Certains tests ont echoue (rc={rc}), coverage mesuree sur ceux qui ont tourne", file=sys.stderr)
        print(output[-500:], file=sys.stderr)

    print("▶ Agregation des donnees (coverage combine)...")
    rc_combine, out_combine = combine_data()
    if rc_combine != 0:
        print(f"⚠ Combine echec : {out_combine}", file=sys.stderr)

    print("▶ Generation du rapport texte...")
    rc_report, text_report, pct = generate_text_report()
    print()
    print(text_report)

    if args.html:
        print("▶ Generation du rapport HTML...")
        rc_html, out_html = generate_html_report()
        if rc_html == 0:
            print(f"✓ Rapport HTML : {ROOT}/htmlcov/index.html")
        else:
            print(f"⚠ HTML echec : {out_html}", file=sys.stderr)

    if pct < 0:
        print("ERREUR: impossible de parser le pourcentage global", file=sys.stderr)
        return 1

    print()
    print(f"coverage_pct={pct:.1f}")
    if args.threshold > 0:
        if pct < args.threshold:
            print(f"❌ Coverage {pct:.1f} %% < seuil {args.threshold:.1f} %%", file=sys.stderr)
            return 1
        print(f"✓ Coverage {pct:.1f} %% >= seuil {args.threshold:.1f} %%")

    return 0


if __name__ == "__main__":
    sys.exit(main())
