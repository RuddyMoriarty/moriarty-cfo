#!/usr/bin/env python3
"""
check_plugin_manifest.py, validation de plugin.json.

Verifie :
  1. plugin.json existe et est du JSON valide
  2. Tous les champs obligatoires sont presents (name, version, license, ...)
  3. version == pyproject.toml version (coherence)
  4. Les 10 skills declares correspondent aux 10 dossiers cfo-* sur disque
  5. L'entrypoint CLI `./cfo` existe et est executable
  6. Les fichiers de demo listes dans `demo.screenshots` existent
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "plugin.json"

REQUIRED_FIELDS = [
    "name", "version", "description_short", "description_long",
    "author", "license", "homepage", "repository",
    "category", "tags", "skills", "cli", "requirements",
    "installation", "security", "quality",
]


def read_pyproject_version() -> str:
    pyproj = ROOT / "pyproject.toml"
    if not pyproj.exists():
        return ""
    for line in pyproj.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("version"):
            return s.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def check_exists() -> tuple[bool, str]:
    if not MANIFEST.exists():
        return False, f"{MANIFEST.name} absent"
    return True, f"{MANIFEST.name} present ({MANIFEST.stat().st_size} octets)"


def check_valid_json() -> tuple[bool, str]:
    try:
        data = load_manifest()
    except json.JSONDecodeError as e:
        return False, f"JSON invalide : {e}"
    if not isinstance(data, dict):
        return False, f"type racine attendu dict, obtenu {type(data).__name__}"
    return True, f"{len(data)} cles racine"


def check_required_fields() -> tuple[bool, str]:
    data = load_manifest()
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return False, f"champs manquants : {missing}"
    return True, f"{len(REQUIRED_FIELDS)} champs obligatoires presents"


def check_version_coherence() -> tuple[bool, str]:
    data = load_manifest()
    manifest_v = data.get("version", "")
    pyproj_v = read_pyproject_version()
    if not pyproj_v:
        return False, "pyproject.toml version introuvable"
    if manifest_v != pyproj_v:
        return False, f"divergence : plugin.json={manifest_v} vs pyproject.toml={pyproj_v}"
    return True, f"version coherente : {manifest_v}"


def check_skills_match_disk() -> tuple[bool, str]:
    data = load_manifest()
    declared = {s["name"] for s in data.get("skills", [])}
    on_disk = {p.name for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("cfo-")}
    missing_on_disk = declared - on_disk
    missing_in_manifest = on_disk - declared
    if missing_on_disk:
        return False, f"skills declares mais absents du disque : {missing_on_disk}"
    if missing_in_manifest:
        return False, f"skills sur disque absents du manifest : {missing_in_manifest}"
    return True, f"{len(declared)} skills coherents"


def check_cli_entrypoint() -> tuple[bool, str]:
    data = load_manifest()
    entrypoint = data.get("cli", {}).get("entrypoint", "")
    if not entrypoint:
        return False, "cli.entrypoint manquant"
    path = ROOT / entrypoint.lstrip("./")
    if not path.exists():
        return False, f"entrypoint {entrypoint} introuvable"
    if not os.access(path, os.X_OK):
        return False, f"entrypoint {entrypoint} pas executable"
    return True, f"{entrypoint} OK"


def check_demo_files() -> tuple[bool, str]:
    data = load_manifest()
    screenshots = data.get("demo", {}).get("screenshots", [])
    scenarios = data.get("demo", {}).get("example_scenarios", [])
    all_files = screenshots + scenarios
    missing = []
    for f in all_files:
        if not (ROOT / f).exists():
            missing.append(f)
    if missing:
        return False, f"fichiers demo manquants : {missing}"
    return True, f"{len(all_files)} fichiers demo presents"


def check_counts_plausible() -> tuple[bool, str]:
    """Verifie que les compteurs quality.tests_total et cli.commands_count sont plausibles."""
    data = load_manifest()
    quality = data.get("quality", {})
    tests_total = quality.get("tests_total", 0)
    if tests_total < 300:
        return False, f"tests_total={tests_total} suspicieusement bas (attendu >= 300)"
    if tests_total > 500:
        return False, f"tests_total={tests_total} suspicieusement haut"

    cli = data.get("cli", {})
    cmd_count = cli.get("commands_count", 0)
    if cmd_count < 40:
        return False, f"commands_count={cmd_count} < 40"

    cov = quality.get("scripts_coverage_pct", 0)
    if cov < 50:
        return False, f"scripts_coverage_pct={cov} < 50"
    return True, f"tests={tests_total}, cli={cmd_count}, coverage={cov}"


def main() -> int:
    checks = [
        ("exists", check_exists),
        ("valid_json", check_valid_json),
        ("required_fields", check_required_fields),
        ("version_coherence", check_version_coherence),
        ("skills_match_disk", check_skills_match_disk),
        ("cli_entrypoint", check_cli_entrypoint),
        ("demo_files", check_demo_files),
        ("counts_plausible", check_counts_plausible),
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
        print(f"plugin_manifest_ok={ok}")
        return 0
    print(f"ERREUR: {len(checks) - ok} check(s) KO", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
