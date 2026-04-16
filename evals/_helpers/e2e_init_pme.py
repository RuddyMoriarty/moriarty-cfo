#!/usr/bin/env python3
"""
Test E2E : init_pme.py cree profile.json (audience=pme_dirigeant) + company.json
minimal au chemin standardise private/companies/<siren>/.

Verifie aussi l'idempotence (exit 1 sans --force) et l'integration avec
compute_entity_routines (qui doit lire le company.json nouvellement cree).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
INIT_PME = ROOT / "cfo-init" / "scripts" / "init_pme.py"
COMPUTE = ROOT / "cfo-init" / "scripts" / "routines" / "compute_entity_routines.py"

SIREN = "654321987"


def run(script: Path, args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(script)] + args,
        capture_output=True, text=True, timeout=15, cwd=str(ROOT),
    )
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    errors: list[str] = []
    steps_ok = 0

    profile_path = PRIVATE / "profile.json"
    company_dir = PRIVATE / "companies" / SIREN
    company_path = company_dir / "company.json"
    routines_path = company_dir / "routines.json"

    # Backup
    profile_backup = profile_path.read_text(encoding="utf-8") if profile_path.exists() else None

    try:
        # Etape 1 : init PME
        rc, stdout, stderr = run(INIT_PME, [
            "--siren", SIREN,
            "--denomination", "TEST PME SAS",
            "--taille", "pe",
            "--cloture", "2026-12-31",
            "--role", "cfo",
            "--secteur", "saas",
            "--force",
        ])
        if rc != 0:
            errors.append(f"init_pme: exit {rc}, stderr={stderr[:200]}")
        elif not profile_path.exists():
            errors.append("init_pme: profile.json non cree")
        elif not company_path.exists():
            errors.append("init_pme: company.json non cree au chemin standardise")
        else:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
            if profile.get("audience_type") != "pme_dirigeant":
                errors.append(f"audience_type attendu pme_dirigeant, obtenu {profile.get('audience_type')}")
            elif profile.get("pme_role") != "cfo":
                errors.append(f"pme_role attendu cfo, obtenu {profile.get('pme_role')}")
            elif profile.get("siren_principal") != SIREN:
                errors.append(f"siren_principal attendu {SIREN}")
            else:
                steps_ok += 1

        # Etape 2 : idempotence (doit fail sans --force)
        rc, _, _ = run(INIT_PME, ["--siren", SIREN, "--denomination", "AUTRE"])
        if rc != 1:
            errors.append(f"idempotence: exit 1 attendu sans --force, obtenu {rc}")
        else:
            steps_ok += 1

        # Etape 3 : integration avec compute_entity_routines
        # (verifie que le company.json genere par init_pme est lisible)
        rc, stdout, _ = run(COMPUTE, ["--siren", SIREN, "--level", "2", "--dry-run"])
        if rc != 0:
            errors.append(f"compute_routines depuis company.json init_pme: exit {rc}")
        elif "Routines retenues" not in stdout and "cloture-mensuelle" not in stdout:
            errors.append("compute_routines: pas de routines retenues")
        else:
            steps_ok += 1

    except Exception as e:
        errors.append(f"exception: {type(e).__name__}: {e}")
    finally:
        # Cleanup
        if profile_backup is not None:
            profile_path.write_text(profile_backup, encoding="utf-8")
        elif profile_path.exists():
            profile_path.unlink()

        if company_dir.exists():
            for f in company_dir.rglob("*"):
                if f.is_file():
                    f.unlink()
            try:
                company_dir.rmdir()
            except OSError:
                pass

        # Cleanup routines.json orphelin si cree par le dry-run
        if routines_path.exists():
            routines_path.unlink()

    if errors:
        print(f"e2e_init_pme_steps_ok={steps_ok}/3")
        for e in errors:
            print(f"ERREUR: {e}")
        return 1

    print("e2e_init_pme_ok=3")
    print("steps=init,idempotence,integration_compute")
    print(f"siren={SIREN}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
