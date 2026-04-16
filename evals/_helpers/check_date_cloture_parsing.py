#!/usr/bin/env python3
"""Test helper: verifie que compute_entity_routines gere les deux formats date_cloture."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMPUTE = ROOT / "cfo-init" / "scripts" / "routines" / "compute_entity_routines.py"


def run_with_fixture(siren: str, fixture: dict, tmp_base: Path) -> tuple[int, str, str]:
    """Cree un company.json fixture et lance compute_entity_routines --dry-run."""
    company_dir = tmp_base / "companies" / siren
    company_dir.mkdir(parents=True, exist_ok=True)
    company_path = company_dir / "company.json"
    company_path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2), encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(COMPUTE), "--siren", siren, "--level", "4", "--dry-run"],
        capture_output=True,
        text=True,
        timeout=10,
        env={**__import__("os").environ, "CFO_PRIVATE_DIR": str(tmp_base)},
    )
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    errors = []

    with tempfile.TemporaryDirectory(prefix="cfo-eval-date-") as tmp:
        tmp_path = Path(tmp)

        # Format 1: YYYY-MM-DD (nouveau, dans exercice_comptable)
        fixture_yyyy = {
            "siren": "111222333",
            "denomination": "TEST YYYY-MM-DD SAS",
            "exercice_comptable": {
                "date_cloture": "2026-12-31",
                "duree_mois": 12,
            },
            "classification": {
                "taille": "PE",
                "secteur_category": "industrie",
                "code_naf": "2511Z",
                "is_startup": False,
                "has_investors": False,
                "has_covenants": False,
                "groupe": False,
                "effectif": 50,
                "csrd_wave": "hors_scope",
                "seuil_audit": False,
            },
        }

        # Format 2: MM-DD (legacy, dans classification)
        fixture_mmdd = {
            "siren": "444555666",
            "denomination": "TEST MM-DD SARL",
            "classification": {
                "taille": "TPE",
                "secteur_category": "commerce",
                "code_naf": "4711B",
                "is_startup": False,
                "has_investors": False,
                "has_covenants": False,
                "groupe": False,
                "effectif": 5,
                "csrd_wave": "hors_scope",
                "seuil_audit": False,
                "date_cloture": "06-30",
            },
        }

        # Le script utilise ROOT/private comme base par defaut.
        # On doit ecrire dans ROOT/private/companies/<siren>/ pour le test.
        private = ROOT / "private"

        for label, siren, fixture in [
            ("YYYY-MM-DD", "111222333", fixture_yyyy),
            ("MM-DD", "444555666", fixture_mmdd),
        ]:
            company_dir = private / "companies" / siren
            company_dir.mkdir(parents=True, exist_ok=True)
            company_path = company_dir / "company.json"
            company_path.write_text(json.dumps(fixture, ensure_ascii=False, indent=2), encoding="utf-8")

            try:
                proc = subprocess.run(
                    [sys.executable, str(COMPUTE), "--siren", siren, "--level", "4", "--dry-run"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if proc.returncode != 0:
                    errors.append(f"format {label}: exit code {proc.returncode}")
                    errors.append(f"  stderr: {proc.stderr[:200]}")
                elif "Routines retenues" not in proc.stdout and "cloture-mensuelle" not in proc.stdout:
                    errors.append(f"format {label}: pas de routines dans stdout")
                    errors.append(f"  stdout: {proc.stdout[:200]}")
            finally:
                if company_path.exists():
                    company_path.unlink()
                # Cleanup routines.json si cree
                rout = company_dir / "routines.json"
                if rout.exists():
                    rout.unlink()
                try:
                    company_dir.rmdir()
                except OSError:
                    pass

    if errors:
        for e in errors:
            print(e)
        return 1

    print("date_formats_ok=2")
    print("tested=YYYY-MM-DD,MM-DD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
