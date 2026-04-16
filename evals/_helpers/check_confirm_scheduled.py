#!/usr/bin/env python3
"""Test helper: verifie que confirm_scheduled.py met a jour l'etat pending -> scheduled."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIRM = ROOT / "cfo-init" / "scripts" / "routines" / "confirm_scheduled.py"


def main() -> int:
    errors = []
    siren = "777888999"

    private = ROOT / "private"
    company_dir = private / "companies" / siren
    company_dir.mkdir(parents=True, exist_ok=True)
    index_path = private / "routines-index.json"

    # Fixture: 2 routines en pending_schedule + 1 en scheduled (deja faite)
    index_fixture = {
        "cfo-cloture-mensuelle-777888999-2026-05": {
            "siren": siren,
            "routine_id": "cloture-mensuelle",
            "state": "pending_schedule",
        },
        "cfo-dashboard-cfo-777888999-2026-05": {
            "siren": siren,
            "routine_id": "dashboard-cfo",
            "state": "pending_schedule",
        },
        "cfo-veille-reglementaire-777888999-2026-W20": {
            "siren": siren,
            "routine_id": "veille-reglementaire",
            "state": "scheduled",  # deja faite, ne doit pas changer
        },
    }

    # Sauvegarder l'index original si il existe
    original_index = None
    if index_path.exists():
        original_index = index_path.read_text(encoding="utf-8")

    # Ecrire le fixture routines.json de l'entite
    routines_fixture = {
        "siren": siren,
        "routines": [
            {"id": "cloture-mensuelle", "state": "pending_schedule", "task_id": "cfo-cloture-mensuelle-777888999-2026-05"},
            {"id": "dashboard-cfo", "state": "pending_schedule", "task_id": "cfo-dashboard-cfo-777888999-2026-05"},
        ],
    }
    routines_path = company_dir / "routines.json"
    routines_path.write_text(json.dumps(routines_fixture, ensure_ascii=False, indent=2), encoding="utf-8")

    try:
        index_path.write_text(json.dumps(index_fixture, ensure_ascii=False, indent=2), encoding="utf-8")

        proc = subprocess.run(
            [sys.executable, str(CONFIRM), "--siren", siren],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if proc.returncode != 0:
            errors.append(f"exit code {proc.returncode}: {proc.stderr[:200]}")
        else:
            # Verifier que l'index a ete mis a jour
            updated = json.loads(index_path.read_text(encoding="utf-8"))

            t1 = updated.get("cfo-cloture-mensuelle-777888999-2026-05", {})
            if t1.get("state") != "scheduled":
                errors.append(f"cloture-mensuelle: attendu scheduled, obtenu {t1.get('state')}")

            t2 = updated.get("cfo-dashboard-cfo-777888999-2026-05", {})
            if t2.get("state") != "scheduled":
                errors.append(f"dashboard-cfo: attendu scheduled, obtenu {t2.get('state')}")

            t3 = updated.get("cfo-veille-reglementaire-777888999-2026-W20", {})
            if t3.get("state") != "scheduled":
                errors.append(f"veille (deja scheduled): attendu scheduled, obtenu {t3.get('state')}")

            # Verifier stdout
            if "2 routine(s) confirmee(s)" not in proc.stdout:
                errors.append(f"stdout inattendu: {proc.stdout[:200]}")

            # Verifier que routines.json de l'entite a aussi ete mis a jour
            if routines_path.exists():
                rdata = json.loads(routines_path.read_text(encoding="utf-8"))
                for r in rdata.get("routines", []):
                    if r.get("state") != "scheduled":
                        errors.append(f"routines.json: {r['id']} encore en {r['state']}")

    finally:
        # Restaurer l'index original
        if original_index is not None:
            index_path.write_text(original_index, encoding="utf-8")
        elif index_path.exists():
            index_path.unlink()

        # Cleanup
        if routines_path.exists():
            routines_path.unlink()
        try:
            company_dir.rmdir()
        except OSError:
            pass

    if errors:
        for e in errors:
            print(f"ERREUR: {e}")
        return 1

    print("confirm_scheduled_ok=2")
    print("states_verified=pending_schedule->scheduled")
    return 0


if __name__ == "__main__":
    sys.exit(main())
