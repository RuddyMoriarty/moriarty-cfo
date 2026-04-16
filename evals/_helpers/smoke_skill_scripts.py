#!/usr/bin/env python3
"""
smoke_skill_scripts.py

Smoke test generique pour les scripts Python d'un skill. Verifie :
  1. Chaque script compile (py_compile)
  2. Chaque script repond a --help (exit 0) avec un docstring ou une aide argparse

Usage :
  python3 evals/_helpers/smoke_skill_scripts.py --skill cfo-comptabilite
"""

from __future__ import annotations

import argparse
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test scripts d'un skill")
    parser.add_argument("--skill", required=True)
    args = parser.parse_args()

    skill_dir = ROOT / args.skill
    scripts_dir = skill_dir / "scripts"

    if not scripts_dir.exists():
        print(f"ERREUR: {scripts_dir} introuvable", file=sys.stderr)
        return 1

    # Exclure les sous-dossiers routines/ et portfolio/ (testes separement)
    scripts = sorted(p for p in scripts_dir.iterdir() if p.is_file() and p.suffix == ".py")
    if not scripts:
        print(f"AVERTISSEMENT: aucun script dans {scripts_dir}")
        return 0

    errors: list[str] = []
    compiled = 0
    help_ok = 0

    for script in scripts:
        # 1. Compilation
        try:
            py_compile.compile(str(script), doraise=True)
            compiled += 1
        except py_compile.PyCompileError as e:
            errors.append(f"{script.name}: SyntaxError : {e}")
            continue

        # 2. Help
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--help"],
                capture_output=True, text=True, timeout=10,
            )
            if proc.returncode != 0:
                errors.append(f"{script.name}: --help exit {proc.returncode}")
            elif not proc.stdout or len(proc.stdout) < 50:
                errors.append(f"{script.name}: --help output vide ou trop court")
            elif "usage:" not in proc.stdout.lower():
                errors.append(f"{script.name}: --help ne contient pas 'usage:'")
            else:
                help_ok += 1
        except subprocess.TimeoutExpired:
            errors.append(f"{script.name}: --help timeout")

    if errors:
        print(f"smoke_{args.skill.replace('-','_')}_compiled={compiled}/{len(scripts)}")
        print(f"smoke_{args.skill.replace('-','_')}_help_ok={help_ok}/{len(scripts)}")
        for e in errors:
            print(f"ERREUR: {e}")
        return 1

    print(f"smoke_{args.skill.replace('-','_')}_ok={len(scripts)}")
    print(f"scripts_tested={','.join(s.stem for s in scripts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
