#!/usr/bin/env python3
"""Test helper: lance compute_entity_routines.py --dry-run sur un SIREN fixture."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPUTE = ROOT / "cfo-init" / "scripts" / "routines" / "compute_entity_routines.py"


def main() -> int:
    siren = "999888777"
    # Fixture en tempdir (n'interfère pas avec private/ réel)
    with tempfile.TemporaryDirectory(prefix="cfo-eval-routines-") as tmp:
        # On utilise private/ du ROOT mais avec un siren factice qui n'existe pas déjà
        private = ROOT / "private"
        company_dir = private / "companies" / siren
        company_dir.mkdir(parents=True, exist_ok=True)
        company_path = company_dir / "company.json"

        fixture = {
            "siren": siren,
            "denomination": "FIXTURE TEST SAS",
            "classification": {
                "taille": "PE",
                "secteur_category": "saas",
                "code_naf": "6201Z",
                "is_startup": True,
                "has_investors": True,
                "has_covenants": False,
                "groupe": False,
                "effectif": 15,
                "csrd_wave": "hors_scope",
                "seuil_audit": False,
                "date_cloture": "12-31",
            },
        }
        company_path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2), encoding="utf-8")

        try:
            proc = subprocess.run(
                [sys.executable, str(COMPUTE), "--siren", siren, "--level", "2", "--dry-run"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            print(proc.stdout)
            if proc.stderr:
                print(proc.stderr, file=sys.stderr)
            return proc.returncode
        finally:
            # Cleanup
            if company_path.exists():
                company_path.unlink()
            try:
                company_dir.rmdir()
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main())
