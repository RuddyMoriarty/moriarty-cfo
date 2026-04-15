#!/usr/bin/env python3
"""Test helper: valide que les templates de cfo-init sont JSON valides et contiennent les champs attendus."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = ROOT / "cfo-init" / "templates"

EXPECTED = {
    "company.template.json": ["identification", "classification", "exercice_comptable", "secteur"],
    "cabinet.template.json": ["cabinet", "structure", "configuration", "portfolio_clients"],
}


def main() -> int:
    errors = []
    ok_count = 0
    for name, required_keys in EXPECTED.items():
        path = TEMPLATES_DIR / name
        if not path.exists():
            errors.append(f"manquant: {name}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{name}: JSON invalide ({e})")
            continue
        missing = [k for k in required_keys if k not in data]
        if missing:
            errors.append(f"{name}: champs manquants {missing}")
            continue
        ok_count += 1

    if errors:
        for e in errors:
            print(e)
        return 1

    print(f"templates_ok={ok_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
