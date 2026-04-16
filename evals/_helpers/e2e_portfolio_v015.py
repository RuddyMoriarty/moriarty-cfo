#!/usr/bin/env python3
"""
Test E2E v0.1.5 : les 4 modules EC portfolio complementaires.

Enchaine :
  1. init_cabinet + add_client
  2. check_dossier + draft_relance
  3. generate_lettre_mission (v1 + v2 renouvellement)
  4. encaissements_aging (avec fixture factures.json)
  5. forfait_tracker (avec fixture forfait.json + temps-passes.json)

Cleanup automatique.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
PORT = ROOT / "cfo-init" / "scripts" / "portfolio"

CABINET_SIREN = "999888111"
CLIENT_SIREN = "123987654"


def run(script: str, args: list[str], label: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(PORT / script)] + args,
        capture_output=True, text=True, timeout=30, cwd=str(ROOT),
    )
    return proc.returncode, proc.stdout, proc.stderr


def cleanup() -> None:
    files_to_remove = [
        PRIVATE / "cabinet.json",
        PRIVATE / "profile.json",
        PRIVATE / "companies" / "index.json",
    ]
    for f in files_to_remove:
        if f.exists():
            f.unlink()
    client_dir = PRIVATE / "companies" / CLIENT_SIREN
    if client_dir.exists():
        for sub in client_dir.rglob("*"):
            if sub.is_file():
                sub.unlink()
        for sub in sorted(client_dir.rglob("*"), key=lambda p: -len(p.parts)):
            if sub.is_dir():
                try:
                    sub.rmdir()
                except OSError:
                    pass
        try:
            client_dir.rmdir()
        except OSError:
            pass


def main() -> int:
    errors: list[str] = []
    steps_ok = 0

    # Backup
    profile_path = PRIVATE / "profile.json"
    cabinet_path = PRIVATE / "cabinet.json"
    index_path = PRIVATE / "companies" / "index.json"
    backups = {}
    for p in (profile_path, cabinet_path, index_path):
        if p.exists():
            backups[p] = p.read_text(encoding="utf-8")

    try:
        # Setup cabinet + client
        rc, _, _ = run("init_cabinet.py", [
            "--siren", CABINET_SIREN,
            "--denomination", "CABINET E2E V015",
            "--force",
        ], "init")
        if rc != 0:
            errors.append("init_cabinet: exit " + str(rc))
            return 1

        rc, _, _ = run("add_client.py", [
            "--siren", CLIENT_SIREN,
            "--denomination", "CLIENT E2E V015 SAS",
            "--taille", "pe",
            "--secteur", "services",
            "--cloture", "2026-12-31",
            "--mission", "presentation",
            "--referent", "Marie E2E",
        ], "add")
        if rc != 0:
            errors.append("add_client: exit " + str(rc))

        # Module 1 : relances
        rc, stdout, _ = run("check_dossier.py", ["--siren", CLIENT_SIREN], "check")
        if rc != 0:
            errors.append("check_dossier: exit " + str(rc))
        elif "INCOMPLET" not in stdout:
            errors.append("check_dossier: attendu INCOMPLET")
        else:
            steps_ok += 1

        relance_out = PRIVATE / "companies" / CLIENT_SIREN / "relance-v1.txt"
        rc, _, _ = run("draft_relance.py", [
            "--siren", CLIENT_SIREN,
            "--type", "premiere",
            "--output", str(relance_out),
        ], "relance")
        if rc != 0:
            errors.append("draft_relance: exit " + str(rc))
        elif not relance_out.exists():
            errors.append("draft_relance: fichier non cree")
        else:
            content = relance_out.read_text(encoding="utf-8")
            if "Marie E2E" not in content or "CLIENT E2E V015" not in content:
                errors.append("draft_relance: placeholders non remplis")
            else:
                steps_ok += 1

        # Module 2 : lettre de mission
        rc, _, _ = run("generate_lettre_mission.py", [
            "--siren", CLIENT_SIREN,
            "--honoraires", "4200",
            "--exercice", "2026",
            "--representant-client", "Jean Test",
        ], "lettre v1")
        if rc != 0:
            errors.append("lettre_mission v1: exit " + str(rc))

        rc, _, _ = run("generate_lettre_mission.py", [
            "--siren", CLIENT_SIREN,
            "--honoraires", "4500",
            "--exercice", "2027",
            "--representant-client", "Jean Test",
            "--new-version",
        ], "lettre v2")
        if rc != 0:
            errors.append("lettre_mission v2: exit " + str(rc))
        else:
            lm_dir = PRIVATE / "companies" / CLIENT_SIREN / "lettres-mission"
            if not (lm_dir / "v1.md").exists() or not (lm_dir / "v2.md").exists():
                errors.append("lettres v1+v2 non creees")
            else:
                meta = json.loads((lm_dir / "metadata.json").read_text(encoding="utf-8"))
                if len(meta.get("versions", [])) != 2:
                    errors.append("metadata versions != 2")
                else:
                    steps_ok += 1

        # Module 3 : encaissements (avec fixture factures)
        (PRIVATE / "companies" / CLIENT_SIREN / "factures.json").write_text(json.dumps({
            "factures": [
                {"numero": "F01", "date_emission": "2026-04-01", "montant_ht": 1000, "statut": "emise"},
                {"numero": "F02", "date_emission": "2026-01-01", "montant_ht": 1500, "statut": "emise"},
                {"numero": "F03", "date_emission": "2026-02-15", "montant_ht": 800, "statut": "encaissee"},
            ]
        }), encoding="utf-8")

        rc, stdout, _ = run("encaissements_aging.py", ["--json"], "aging")
        if rc != 0:
            errors.append("aging: exit " + str(rc))
        else:
            try:
                data = json.loads(stdout)
                if data.get("totaux", {}).get("non_encaisse_ht", 0) < 2000:
                    errors.append("aging: total non_encaisse_ht trop bas")
                else:
                    steps_ok += 1
            except json.JSONDecodeError:
                errors.append("aging: stdout non JSON")

        # Module 4 : forfaits (avec fixture)
        (PRIVATE / "companies" / CLIENT_SIREN / "forfait.json").write_text(json.dumps({
            "forfait_heures": 30, "tjm_reference": 680, "annee": 2026,
        }), encoding="utf-8")
        (PRIVATE / "companies" / CLIENT_SIREN / "temps-passes.json").write_text(json.dumps({
            "saisies": [
                {"date": "2026-02-01", "collaborateur": "Jean", "heures": 20, "tache": "Cloture"},
                {"date": "2026-03-15", "collaborateur": "Marie", "heures": 18, "tache": "Liasse"},
            ]
        }), encoding="utf-8")

        rc, stdout, _ = run("forfait_tracker.py", ["--json"], "forfait")
        if rc != 0:
            errors.append("forfait: exit " + str(rc))
        else:
            try:
                data = json.loads(stdout)
                if len(data.get("clients", [])) == 0:
                    errors.append("forfait: aucun client avec forfait")
                elif data["clients"][0].get("statut") != "depassement":
                    errors.append(f"forfait: statut attendu depassement, obtenu {data['clients'][0].get('statut')}")
                else:
                    steps_ok += 1
            except json.JSONDecodeError:
                errors.append("forfait: stdout non JSON")

    except Exception as e:
        errors.append(f"exception : {type(e).__name__}: {e}")
    finally:
        cleanup()
        for p, content in backups.items():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")

    if errors:
        print(f"e2e_v015_steps_ok={steps_ok}/5")
        for e in errors:
            print(f"ERREUR: {e}")
        return 1

    print("e2e_v015_ok=5")
    print("modules=relances,lettres_mission,encaissements,forfaits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
