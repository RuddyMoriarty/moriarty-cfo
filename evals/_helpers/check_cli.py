#!/usr/bin/env python3
"""
check_cli.py, tests du wrapper CLI ./cfo.

6 checks :
  1. --help retourne 0 et liste les 10 categories attendues
  2. --version affiche "moriarty-cfo v<numero>"
  3. --list retourne >= 40 commandes
  4. Commande inconnue : exit 2 + suggestion sur typo
  5. Dispatch reel : ./cfo calendar --help forward bien a compute_calendar
  6. Dispatch avec arguments : ./cfo bfr calcule un BFR valide
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "cfo"

EXPECTED_CATEGORIES = [
    "Onboarding",
    "Portfolio EC",
    "Routines",
    "Comptabilite",
    "Tresorerie",
    "Reporting",
    "Controle de gestion",
    "Budget et forecast",
    "Fiscalite",
    "Risques et conformite",
    "Financement et croissance",
    "CSRD / ESG",
]


def run_cli(args: list[str], stdin_data: str = "") -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(CLI)] + args,
        capture_output=True, text=True, timeout=15, cwd=str(ROOT),
    )
    return proc.returncode, proc.stdout, proc.stderr


def check_help() -> tuple[bool, str]:
    rc, stdout, stderr = run_cli(["--help"])
    if rc != 0:
        return False, f"--help exit {rc}"
    missing = [c for c in EXPECTED_CATEGORIES if c not in stdout]
    if missing:
        return False, f"categories manquantes : {missing}"
    return True, f"{len(EXPECTED_CATEGORIES)} categories listees"


def check_version() -> tuple[bool, str]:
    rc, stdout, stderr = run_cli(["--version"])
    if rc != 0:
        return False, f"--version exit {rc}"
    if "moriarty-cfo v" not in stdout:
        return False, f"sortie inattendue : {stdout[:60]}"
    # Doit contenir un numero X.Y.Z
    import re
    if not re.search(r"v\d+\.\d+\.\d+", stdout):
        return False, f"pas de numero semver : {stdout[:60]}"
    return True, stdout.strip()


def check_list() -> tuple[bool, str]:
    rc, stdout, stderr = run_cli(["--list"])
    if rc != 0:
        return False, f"--list exit {rc}"
    cmds = [line for line in stdout.splitlines() if line.strip()]
    if len(cmds) < 40:
        return False, f"seulement {len(cmds)} commandes (attendu >= 40)"
    # Verifier quelques commandes critiques
    critical = {"init-pme", "init-cabinet", "calendar", "bfr", "budget", "cir", "is", "tva"}
    missing = critical - set(cmds)
    if missing:
        return False, f"commandes critiques manquantes : {missing}"
    return True, f"{len(cmds)} commandes"


def check_unknown_command() -> tuple[bool, str]:
    rc, stdout, stderr = run_cli(["forecas"])  # typo volontaire
    if rc == 0:
        return False, "commande inconnue acceptee (attendu exit != 0)"
    combined = (stdout + stderr).lower()
    if "inconnue" not in combined and "unknown" not in combined:
        return False, "pas de message d'erreur clair"
    if "forecast-13w" not in combined:
        return False, "pas de suggestion de commande proche"
    return True, f"exit {rc} avec suggestion"


def check_dispatch_help() -> tuple[bool, str]:
    """./cfo calendar --help doit forward vers compute_calendar --help."""
    rc, stdout, stderr = run_cli(["calendar", "--help"])
    if rc != 0:
        return False, f"calendar --help exit {rc}"
    combined = stdout + stderr
    if "compute_calendar" not in combined and "--closing-date" not in combined:
        return False, f"forward incorrect : {combined[:100]}"
    return True, "dispatch OK"


def check_dispatch_exec() -> tuple[bool, str]:
    """./cfo bfr calcule un resultat reel."""
    rc, stdout, stderr = run_cli([
        "bfr",
        "--creances-clients", "200000", "--dettes-fournisseurs", "100000",
        "--ca-ttc", "1200000", "--achats-ttc", "400000",
        "--stocks", "50000", "--cout-ventes", "300000",
    ])
    if rc != 0:
        return False, f"bfr exit {rc}: {stderr[:100]}"
    if '"dso"' not in stdout or '"bfr"' not in stdout:
        return False, f"output BFR incomplet : {stdout[:100]}"
    return True, "bfr dispatch + execution OK"


def main() -> int:
    checks = [
        ("help", check_help),
        ("version", check_version),
        ("list", check_list),
        ("unknown_command", check_unknown_command),
        ("dispatch_help", check_dispatch_help),
        ("dispatch_exec", check_dispatch_exec),
    ]
    ok = 0
    for name, fn in checks:
        try:
            passed, detail = fn()
        except Exception as e:
            passed, detail = False, f"exception {type(e).__name__}: {e}"
        status = "OK" if passed else "KO"
        print(f"[{status}] {name} : {detail}")
        if passed:
            ok += 1

    if ok == len(checks):
        print(f"cli_ok={ok}")
        return 0
    print(f"ERREUR: {len(checks) - ok} check(s) KO", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
