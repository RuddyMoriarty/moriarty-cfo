#!/usr/bin/env python3
"""
check_fetch_siren.py, v0.2.3 Module B (integration SIREN).

Tests offline (sans reseau) des scripts fetch_pappers.py et fetch_sirene.py.
Mode `web` renvoie une instruction WebFetch deterministe utilisable par Claude.

Verifie :
  1. Les scripts compilent (py_compile)
  2. Mode `web` sans reseau : JSON structure avec mode=webfetch_required,
     urls_to_try contenant le SIREN
  3. Validation SIREN : 9 chiffres strict (rejet a 5 chiffres)
  4. Stdlib-only : aucun import de `requests` ou autre module externe
"""

from __future__ import annotations

import json
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPPERS = ROOT / "cfo-init" / "scripts" / "fetch_pappers.py"
SIRENE = ROOT / "cfo-init" / "scripts" / "fetch_sirene.py"


def check_compile() -> tuple[bool, str]:
    try:
        py_compile.compile(str(PAPPERS), doraise=True)
        py_compile.compile(str(SIRENE), doraise=True)
        return True, "compile OK"
    except py_compile.PyCompileError as e:
        return False, f"compile KO : {e}"


def check_stdlib_only() -> tuple[bool, str]:
    """Verifie qu'aucun import de module externe (requests, httpx, aiohttp)."""
    forbidden = {"requests", "httpx", "aiohttp", "pycurl"}
    for script in (PAPPERS, SIRENE):
        text = script.read_text(encoding="utf-8")
        # Chercher "import X" ou "from X" pour chaque forbidden
        for mod in forbidden:
            for pattern in (f"import {mod}", f"from {mod}"):
                if pattern in text and "#" + pattern not in text:
                    return False, f"{script.name} importe encore {mod}"
    return True, "stdlib only OK"


def check_web_mode(script: Path, siren: str = "552120222") -> tuple[bool, str]:
    """Mode web doit retourner une instruction structurelle offline."""
    proc = subprocess.run(
        [sys.executable, str(script), "--siren", siren, "--mode", "web"],
        capture_output=True, text=True, timeout=10, cwd=str(ROOT),
    )
    if proc.returncode != 0:
        return False, f"{script.name} mode web exit {proc.returncode}: {proc.stderr[:150]}"
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        return False, f"{script.name} mode web JSON invalide : {e}"
    if data.get("mode") != "webfetch_required":
        return False, f"{script.name} mode=webfetch_required attendu, obtenu {data.get('mode')}"
    urls = data.get("urls_to_try", [])
    if not any(siren in u for u in urls):
        return False, f"{script.name} urls_to_try ne contient pas le SIREN : {urls}"
    return True, f"{script.name} mode web OK ({len(urls)} url(s))"


def check_siren_validation(script: Path) -> tuple[bool, str]:
    """SIREN a 5 chiffres doit etre rejete avec exit != 0."""
    proc = subprocess.run(
        [sys.executable, str(script), "--siren", "12345", "--mode", "web"],
        capture_output=True, text=True, timeout=10, cwd=str(ROOT),
    )
    if proc.returncode == 0:
        return False, f"{script.name} accepte SIREN a 5 chiffres (attendu rejet)"
    combined = (proc.stdout + proc.stderr).lower()
    if "invalide" not in combined and "invalid" not in combined:
        return False, f"{script.name} rejet sans message clair"
    return True, f"{script.name} rejette SIREN invalide"


def main() -> int:
    checks = [
        ("compile", check_compile),
        ("stdlib_only", check_stdlib_only),
        ("pappers_web", lambda: check_web_mode(PAPPERS)),
        ("sirene_web", lambda: check_web_mode(SIRENE)),
        ("pappers_validation", lambda: check_siren_validation(PAPPERS)),
        ("sirene_validation", lambda: check_siren_validation(SIRENE)),
    ]
    ok_count = 0
    for name, fn in checks:
        ok, detail = fn()
        status = "OK" if ok else "KO"
        print(f"[{status}] {name} : {detail}")
        if ok:
            ok_count += 1

    if ok_count == len(checks):
        print(f"fetch_siren_ok={ok_count}")
        return 0
    print(f"ERREUR: {len(checks) - ok_count} check(s) KO", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
