#!/usr/bin/env python3
"""
Test E2E : onboarding cfo-init bout en bout.

Enchaine les 4 etapes scriptables du parcours utilisateur avec une fixture :
  1. compute_calendar.py       (calendrier fiscal)
  2. compute_entity_routines.py (derivation des routines applicables)
  3. schedule_routines.py       (generation des payloads scheduled-tasks)
  4. init_progress.py           (achievements)

Chaque etape verifie les side-effects (fichiers crees, JSON valide, contenu attendu).
Tout est nettoye en fin de test (fixture dans private/).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
SIREN = "999777555"
COMPANY_DIR = PRIVATE / "companies" / SIREN

# Fichiers crees par le test (a nettoyer)
CREATED_FILES: list[Path] = []
CREATED_DIRS: list[Path] = []


def cleanup() -> None:
    """Supprime tous les fichiers et dossiers crees par le test."""
    for f in CREATED_FILES:
        if f.exists():
            f.unlink()
    # Nettoyer les dossiers (les plus profonds d'abord)
    for d in sorted(CREATED_DIRS, key=lambda p: len(p.parts), reverse=True):
        try:
            if d.exists() and not any(d.iterdir()):
                d.rmdir()
        except OSError:
            pass


def run(script: str, args: list[str], label: str) -> tuple[int, str, str]:
    """Execute un script Python et retourne (exit_code, stdout, stderr)."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / script)] + args,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(ROOT),
    )
    if proc.returncode != 0:
        print(f"ERREUR [{label}]: exit code {proc.returncode}")
        if proc.stderr:
            print(f"  stderr: {proc.stderr[:300]}")
        if proc.stdout:
            print(f"  stdout: {proc.stdout[:300]}")
    return proc.returncode, proc.stdout, proc.stderr


def assert_json_file(path: Path, label: str) -> dict:
    """Verifie qu'un fichier existe et contient du JSON valide."""
    if not path.exists():
        raise AssertionError(f"[{label}] fichier manquant : {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise AssertionError(f"[{label}] JSON invalide dans {path}: {e}") from e
    return data


def main() -> int:
    errors: list[str] = []
    steps_ok = 0

    try:
        # ──────────────────────────────────────────────
        # Setup : fixture company.json + profile.json
        # ──────────────────────────────────────────────
        COMPANY_DIR.mkdir(parents=True, exist_ok=True)
        CREATED_DIRS.extend([
            COMPANY_DIR,
            PRIVATE / "companies" / SIREN,
            PRIVATE / "companies",
        ])

        fixture_company = {
            "siren": SIREN,
            "denomination": "E2E TEST INDUSTRIES SAS",
            "exercice_comptable": {
                "date_cloture": "2026-12-31",
                "duree_mois": 12,
                "exercice_en_cours": "2026",
            },
            "classification": {
                "taille": "PE",
                "secteur_category": "saas",
                "code_naf": "6201Z",
                "is_startup": True,
                "has_investors": True,
                "has_covenants": False,
                "groupe": False,
                "effectif": 25,
                "csrd_wave": "hors_scope",
                "seuil_audit": False,
            },
        }
        company_path = COMPANY_DIR / "company.json"
        company_path.write_text(json.dumps(fixture_company, ensure_ascii=False, indent=2), encoding="utf-8")
        CREATED_FILES.append(company_path)

        profile_path = PRIVATE / "profile.json"
        profile_existed = profile_path.exists()
        if not profile_existed:
            profile_path.write_text(json.dumps({
                "audience_type": "pme",
                "notifications_level": 2,
                "notifications_active": True,
            }, indent=2), encoding="utf-8")
            CREATED_FILES.append(profile_path)

        # ──────────────────────────────────────────────
        # Etape 1 : compute_calendar.py
        # ──────────────────────────────────────────────
        calendar_out = COMPANY_DIR / "calendar-fiscal.json"
        CREATED_FILES.append(calendar_out)

        rc, stdout, stderr = run(
            "cfo-init/scripts/compute_calendar.py",
            [
                "--closing-date", "2026-12-31",
                "--tva-regime", "reel_normal_mensuelle",
                "--is-regime", "is",
                "--effectif", "25",
                "--output", str(calendar_out),
            ],
            "Etape 1: calendrier fiscal",
        )
        if rc != 0:
            errors.append(f"etape1_calendar: exit code {rc}")
        else:
            cal = assert_json_file(calendar_out, "etape1_calendar")
            echeances = cal.get("echeances", [])
            if len(echeances) == 0:
                errors.append("etape1_calendar: aucune echeance generee")
            else:
                # Verifier la structure d'une echeance
                first = echeances[0]
                required_keys = {"id", "label", "date_absolue"}
                missing = required_keys - set(first.keys())
                if missing:
                    errors.append(f"etape1_calendar: cles manquantes dans echeance : {missing}")
                # Verifier qu'on a des echeances IS (regime is)
                is_echeances = [e for e in echeances if "is" in e.get("id", "").lower() or "IS" in e.get("label", "")]
                if len(is_echeances) == 0:
                    errors.append("etape1_calendar: aucune echeance IS trouvee (regime is)")
                steps_ok += 1

        # ──────────────────────────────────────────────
        # Etape 2 : compute_entity_routines.py
        # ──────────────────────────────────────────────
        routines_path = COMPANY_DIR / "routines.json"
        CREATED_FILES.append(routines_path)

        rc, stdout, stderr = run(
            "cfo-init/scripts/routines/compute_entity_routines.py",
            ["--siren", SIREN, "--level", "2"],
            "Etape 2: compute routines",
        )
        if rc != 0:
            errors.append(f"etape2_routines: exit code {rc}")
        else:
            rdata = assert_json_file(routines_path, "etape2_routines")
            routines = rdata.get("routines", [])
            if len(routines) == 0:
                errors.append("etape2_routines: aucune routine derivee")
            else:
                # Verifier que cloture-mensuelle est retenue (universelle)
                ids = {r.get("id") for r in routines}
                if "cloture-mensuelle" not in ids:
                    errors.append("etape2_routines: cloture-mensuelle manquante")
                # Verifier la structure
                first = routines[0]
                if "id" not in first or "frequency" not in first:
                    errors.append("etape2_routines: structure routine invalide (manque id/frequency)")
                steps_ok += 1

        # ──────────────────────────────────────────────
        # Etape 3 : schedule_routines.py
        # ──────────────────────────────────────────────
        payloads_out = COMPANY_DIR / "payloads.json"
        CREATED_FILES.append(payloads_out)
        index_path = PRIVATE / "routines-index.json"
        index_existed = index_path.exists()
        if not index_existed:
            CREATED_FILES.append(index_path)
        log_path = PRIVATE / "routines.log"
        log_existed = log_path.exists()
        if not log_existed:
            CREATED_FILES.append(log_path)

        rc, stdout, stderr = run(
            "cfo-init/scripts/routines/schedule_routines.py",
            ["--siren", SIREN, "--output", str(payloads_out)],
            "Etape 3: schedule routines",
        )
        if rc != 0:
            errors.append(f"etape3_schedule: exit code {rc}")
        else:
            pdata = assert_json_file(payloads_out, "etape3_payloads")
            payloads = pdata.get("payloads", [])
            if len(payloads) == 0:
                errors.append("etape3_schedule: aucun payload genere")
            else:
                # Verifier la structure d'un payload
                first = payloads[0]
                required_keys = {"task_id", "prompt", "description"}
                missing = required_keys - set(first.keys())
                if missing:
                    errors.append(f"etape3_schedule: cles manquantes dans payload : {missing}")
                # Verifier que le task_id suit le pattern
                tid = first.get("task_id", "")
                if not tid.startswith("cfo-"):
                    errors.append(f"etape3_schedule: task_id ne commence pas par cfo- : {tid}")
                steps_ok += 1

            # Verifier l'index
            if index_path.exists():
                idx = assert_json_file(index_path, "etape3_index")
                if len(idx) == 0:
                    errors.append("etape3_schedule: routines-index.json vide")

        # ──────────────────────────────────────────────
        # Etape 4 : init_progress.py
        # ──────────────────────────────────────────────
        progress_path = PRIVATE / "cfo-progress.json"
        progress_existed = progress_path.exists()
        if not progress_existed:
            CREATED_FILES.append(progress_path)

        rc, stdout, stderr = run(
            "cfo-init/scripts/init_progress.py",
            ["--siren", SIREN, "--audience", "pme"],
            "Etape 4: init progress",
        )
        if rc != 0:
            errors.append(f"etape4_progress: exit code {rc}")
        else:
            pdata = assert_json_file(progress_path, "etape4_progress")
            totals = pdata.get("totals", {})
            unlocked = totals.get("achievements_unlocked", 0)
            if unlocked < 1:
                errors.append("etape4_progress: welcome-aboard non deblocke")
            tier = totals.get("current_tier", "")
            if "Apprenti" not in tier:
                errors.append(f"etape4_progress: tier inattendu : {tier}")
            # Verifier stdout JSON
            try:
                result = json.loads(stdout)
                if "welcome-aboard" not in str(result.get("unlocked", [])):
                    errors.append("etape4_progress: welcome-aboard absent du stdout")
            except json.JSONDecodeError:
                errors.append(f"etape4_progress: stdout n'est pas du JSON valide : {stdout[:100]}")
            steps_ok += 1

    except AssertionError as e:
        errors.append(str(e))
    except Exception as e:
        errors.append(f"exception inattendue : {type(e).__name__}: {e}")
    finally:
        cleanup()

    # ──────────────────────────────────────────────
    # Rapport
    # ──────────────────────────────────────────────
    if errors:
        print(f"e2e_steps_ok={steps_ok}")
        for e in errors:
            print(f"ERREUR: {e}")
        return 1

    print(f"e2e_onboarding_ok=4")
    print(f"steps=calendar,routines,schedule,achievements")
    print(f"siren={SIREN}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
