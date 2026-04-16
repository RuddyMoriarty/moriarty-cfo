#!/usr/bin/env python3
"""
Test E2E : portfolio EC bout en bout.

Enchaine les 6 scripts du mode portfolio :
  1. init_cabinet.py
  2. add_client.py (x3 clients)
  3. list_clients.py
  4. schedule_all.py --dry-run
  5. portfolio_dashboard.py
  6. remove_client.py --archive

Cleanup automatique des fichiers crees dans private/.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private"
PORT = ROOT / "cfo-init" / "scripts" / "portfolio"

CABINET_SIREN = "888999777"
CLIENT_SIRENS = ["112233445", "223344556", "334455667"]

CREATED_FILES: list[Path] = []
CREATED_DIRS: list[Path] = []


def cleanup() -> None:
    for f in CREATED_FILES:
        if f.exists():
            f.unlink()
    for d in sorted(CREATED_DIRS, key=lambda p: len(p.parts), reverse=True):
        try:
            if d.exists():
                for sub in d.rglob("*"):
                    if sub.is_file():
                        sub.unlink()
                for sub in sorted(d.rglob("*"), key=lambda p: len(p.parts), reverse=True):
                    if sub.is_dir():
                        try:
                            sub.rmdir()
                        except OSError:
                            pass
                try:
                    d.rmdir()
                except OSError:
                    pass
        except OSError:
            pass


def run(script: str, args: list[str], label: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(PORT / script)] + args,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(ROOT),
    )
    if proc.returncode != 0:
        print(f"FAIL [{label}]: exit {proc.returncode}")
        if proc.stderr:
            print(f"  stderr: {proc.stderr[:200]}")
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    errors: list[str] = []
    steps_ok = 0

    # Tracking des fichiers a cleanup
    CREATED_FILES.extend([
        PRIVATE / "cabinet.json",
        PRIVATE / "profile.json",
        PRIVATE / "companies" / "index.json",
        PRIVATE / "portfolio-dashboard.html",
    ])
    for siren in CLIENT_SIRENS:
        CREATED_DIRS.append(PRIVATE / "companies" / siren)

    # Sauvegarder profile.json existant pour restauration
    profile_path = PRIVATE / "profile.json"
    profile_backup = profile_path.read_text(encoding="utf-8") if profile_path.exists() else None
    cabinet_path = PRIVATE / "cabinet.json"
    cabinet_backup = cabinet_path.read_text(encoding="utf-8") if cabinet_path.exists() else None
    index_path = PRIVATE / "companies" / "index.json"
    index_backup = index_path.read_text(encoding="utf-8") if index_path.exists() else None

    try:
        # Etape 1 : init_cabinet
        rc, stdout, _ = run("init_cabinet.py", [
            "--siren", CABINET_SIREN,
            "--denomination", "CABINET E2E TEST SELARL",
            "--forme", "selarl", "--ville", "Paris", "--force",
        ], "init_cabinet")
        if rc != 0:
            errors.append(f"init_cabinet: exit {rc}")
        else:
            if not cabinet_path.exists():
                errors.append("init_cabinet: cabinet.json non cree")
            elif not index_path.exists():
                errors.append("init_cabinet: index.json non cree")
            else:
                steps_ok += 1

        # Etape 2 : add_client (x3)
        clients_data = [
            (CLIENT_SIRENS[0], "CLIENT PE SAS", "pe", "commerce", "2026-12-31", "presentation"),
            (CLIENT_SIRENS[1], "CLIENT TPE SARL", "tpe", "services", "2026-06-30", "presentation"),
            (CLIENT_SIRENS[2], "CLIENT ME SA", "me", "industrie", "2026-12-31", "audit_legal_cac"),
        ]
        add_ok = 0
        for siren, denom, taille, secteur, cloture, mission in clients_data:
            rc, _, _ = run("add_client.py", [
                "--siren", siren, "--denomination", denom,
                "--taille", taille, "--secteur", secteur,
                "--cloture", cloture, "--mission", mission,
            ], f"add_client {siren}")
            if rc == 0:
                add_ok += 1
                # Verifier que company.json a ete cree
                if not (PRIVATE / "companies" / siren / "company.json").exists():
                    errors.append(f"add_client {siren}: company.json non cree")
        if add_ok != 3:
            errors.append(f"add_client: {add_ok}/3 OK")
        else:
            # Verifier l'index
            index = json.loads(index_path.read_text(encoding="utf-8"))
            if len(index.get("clients", [])) < 3:
                errors.append(f"add_client: {len(index.get('clients', []))} clients dans l'index au lieu de 3+")
            else:
                steps_ok += 1

        # Etape 3 : list_clients
        rc, stdout, _ = run("list_clients.py", [], "list_clients")
        if rc != 0:
            errors.append(f"list_clients: exit {rc}")
        else:
            if "CLIENT PE SAS" not in stdout or "CLIENT TPE SARL" not in stdout or "CLIENT ME SA" not in stdout:
                errors.append("list_clients: clients manquants dans stdout")
            else:
                steps_ok += 1

        # Etape 4 : schedule_all --dry-run
        rc, stdout, _ = run("schedule_all.py", ["--dry-run"], "schedule_all")
        if rc != 0:
            errors.append(f"schedule_all: exit {rc}")
        else:
            if "3/3 OK" not in stdout and "Resume: 3" not in stdout:
                errors.append(f"schedule_all: resume inattendu : {stdout[-200:]}")
            else:
                steps_ok += 1

        # Etape 5 : portfolio_dashboard
        dashboard_path = PRIVATE / "portfolio-dashboard.html"
        rc, _, _ = run("portfolio_dashboard.py", ["--output", str(dashboard_path)], "dashboard")
        if rc != 0:
            errors.append(f"portfolio_dashboard: exit {rc}")
        elif not dashboard_path.exists():
            errors.append("portfolio_dashboard: HTML non cree")
        else:
            html = dashboard_path.read_text(encoding="utf-8")
            if "CABINET E2E TEST" not in html:
                errors.append("dashboard: denomination cabinet absente")
            elif "CLIENT PE SAS" not in html:
                errors.append("dashboard: clients absents du tableau")
            else:
                steps_ok += 1

        # Etape 6 : remove_client --archive
        rc, _, _ = run("remove_client.py", [
            "--siren", CLIENT_SIRENS[0], "--archive",
        ], "remove_client archive")
        if rc != 0:
            errors.append(f"remove_client: exit {rc}")
        else:
            index = json.loads(index_path.read_text(encoding="utf-8"))
            archived = [c for c in index.get("clients", []) if c.get("status") == "archive"]
            if not any(c.get("siren") == CLIENT_SIRENS[0] for c in archived):
                errors.append("remove_client: client non archive dans l'index")
            else:
                steps_ok += 1

    except Exception as e:
        errors.append(f"exception : {type(e).__name__}: {e}")
    finally:
        # Restaurer les fichiers originaux
        if profile_backup is not None:
            profile_path.write_text(profile_backup, encoding="utf-8")
        elif profile_path.exists():
            profile_path.unlink()
        if cabinet_backup is not None:
            cabinet_path.write_text(cabinet_backup, encoding="utf-8")
        elif cabinet_path.exists():
            cabinet_path.unlink()
        if index_backup is not None:
            index_path.write_text(index_backup, encoding="utf-8")
        elif index_path.exists():
            index_path.unlink()

        # Nettoyer les clients crees
        for siren in CLIENT_SIRENS:
            client_dir = PRIVATE / "companies" / siren
            if client_dir.exists():
                for f in client_dir.rglob("*"):
                    if f.is_file():
                        f.unlink()
                try:
                    client_dir.rmdir()
                except OSError:
                    pass

        # Dashboard
        if (PRIVATE / "portfolio-dashboard.html").exists():
            (PRIVATE / "portfolio-dashboard.html").unlink()

    if errors:
        print(f"e2e_portfolio_steps_ok={steps_ok}")
        for e in errors:
            print(f"ERREUR: {e}")
        return 1

    print("e2e_portfolio_ok=6")
    print("steps=init,add,list,schedule_dry,dashboard,archive")
    print(f"cabinet_siren={CABINET_SIREN}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
