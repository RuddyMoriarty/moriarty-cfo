#!/usr/bin/env python3
"""Test helper: vérifie que les 5 scripts de routines compilent."""
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "cfo-init" / "scripts" / "routines"


def main() -> int:
    expected = {
        "compute_entity_routines.py",
        "schedule_routines.py",
        "run_routine.py",
        "list_routines.py",
        "purge_routines.py",
    }
    found = 0
    errors = []
    for name in expected:
        path = SCRIPTS_DIR / name
        if not path.exists():
            errors.append(f"manquant: {name}")
            continue
        try:
            py_compile.compile(str(path), doraise=True)
            found += 1
        except py_compile.PyCompileError as e:
            errors.append(f"SyntaxError dans {name}: {e}")

    if errors:
        for e in errors:
            print(e)
        return 1

    print(f"scripts_ok={found}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
