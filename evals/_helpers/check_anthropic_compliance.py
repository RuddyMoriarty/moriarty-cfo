#!/usr/bin/env python3
"""
check_anthropic_compliance.py, audit du bundle contre le Guide Anthropic
"The Complete Guide to Building Skills for Claude" (33 pages, oct 2025).

Verifie pour chaque skill (10 dossiers cfo-*) :

  1. Folder kebab-case (cfo-init OK, cfo_init / CfoInit KO)
  2. SKILL.md present, casse exacte (no skill.md ni SKILL.MD)
  3. Pas de README.md DANS le skill folder (regle stricte page 10)
  4. Frontmatter YAML valide entre --- ---
  5. name == folder name + kebab-case
  6. description : 1-1024 chars, contient WHAT + WHEN, pas de XML brackets
  7. Pas de prefixe reserve "claude-" ou "anthropic-" dans le name
  8. SKILL.md sous 5000 mots (page 27 : large context issues)
  9. Description contient des trigger phrases reconnaissables
 10. License declaree OK (MIT recommande pour open source)

Usage : python3 evals/_helpers/check_anthropic_compliance.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

MAX_DESCRIPTION_CHARS = 1024
MAX_SKILL_MD_WORDS = 5000
RESERVED_PREFIXES = ("claude-", "anthropic-")
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


def parse_frontmatter(path: Path) -> tuple[dict | None, str]:
    """Retourne (frontmatter_dict ou None, body_text)."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None, m.group(2)
    return fm, m.group(2)


def audit_skill(skill_dir: Path) -> list[tuple[str, str]]:
    """Retourne une liste de (severity, message) pour ce skill."""
    issues: list[tuple[str, str]] = []
    name = skill_dir.name

    # Rule 1 : folder kebab-case
    if not NAME_PATTERN.match(name):
        issues.append(("CRITICAL", f"folder name '{name}' not kebab-case"))

    # Rule 7 : pas de prefixe reserve
    for pref in RESERVED_PREFIXES:
        if name.startswith(pref):
            issues.append(("CRITICAL", f"folder name '{name}' uses reserved prefix '{pref}'"))

    # Rule 2 : SKILL.md present, casse exacte
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        # Chercher des variations
        variants = [p.name for p in skill_dir.iterdir() if p.name.lower() == "skill.md"]
        if variants:
            issues.append(("CRITICAL", f"SKILL.md case incorrect : trouve {variants}, attendu 'SKILL.md'"))
        else:
            issues.append(("CRITICAL", "SKILL.md absent"))
        return issues

    # Rule 3 : pas de README.md dans le skill folder
    readme = skill_dir / "README.md"
    if readme.exists():
        issues.append(("CRITICAL", "README.md present DANS le skill folder (interdit page 10 du guide)"))

    # Parse frontmatter
    fm, body = parse_frontmatter(skill_md)
    if fm is None:
        issues.append(("CRITICAL", "frontmatter YAML absent ou invalide"))
        return issues

    # Rule 5 : name match folder + kebab-case
    fm_name = fm.get("name", "")
    if not isinstance(fm_name, str) or not fm_name:
        issues.append(("CRITICAL", "champ 'name' absent dans frontmatter"))
    else:
        if fm_name != name:
            issues.append(("CRITICAL", f"frontmatter name='{fm_name}' != folder='{name}'"))
        if not NAME_PATTERN.match(fm_name):
            issues.append(("CRITICAL", f"frontmatter name='{fm_name}' not kebab-case"))
        for pref in RESERVED_PREFIXES:
            if fm_name.startswith(pref):
                issues.append(("CRITICAL", f"frontmatter name uses reserved prefix '{pref}'"))

    # Rule 6 : description
    desc = fm.get("description", "")
    if isinstance(desc, list):
        desc = " ".join(str(x) for x in desc)
    if not desc:
        issues.append(("CRITICAL", "champ 'description' absent ou vide"))
    else:
        # Length
        n = len(desc)
        if n > MAX_DESCRIPTION_CHARS:
            issues.append(("CRITICAL", f"description {n} chars > {MAX_DESCRIPTION_CHARS}"))
        # XML brackets
        if "<" in desc or ">" in desc:
            issues.append(("CRITICAL", "description contient des brackets XML (< ou >) - interdit"))
        # WHAT + WHEN heuristique : doit contenir au moins une mention de "Use when" / "When to use"
        # ou des trigger phrases (separes par , ;)
        triggers_hint = any(kw in desc.lower() for kw in [
            "use when", "when to use", "when user", "trigger", "déclencher",
            "appel", "lance", "à utiliser", "use this"
        ])
        # Ou la presence d'une liste de triggers (Triggers: ou plusieurs phrases)
        has_triggers_block = "trigger" in desc.lower() or len(desc.split(",")) >= 5
        if not triggers_hint and not has_triggers_block:
            issues.append(("WARNING", "description ne contient ni 'Use when' ni liste de triggers explicite"))

    # Rule 8 : SKILL.md sous 5000 mots
    word_count = len(body.split())
    if word_count > MAX_SKILL_MD_WORDS:
        issues.append((
            "WARNING",
            f"SKILL.md body {word_count} mots > {MAX_SKILL_MD_WORDS} (deplacer details vers references/)"
        ))

    # Rule 10 : license declaree (recommande)
    if "license" not in fm:
        issues.append(("INFO", "license non declaree dans frontmatter (recommande : MIT)"))

    return issues


def main() -> int:
    skills = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("cfo-"))
    if not skills:
        print("ERREUR: aucun skill cfo-* trouve a la racine", file=sys.stderr)
        return 1

    total_critical = 0
    total_warning = 0
    total_info = 0

    print(f"Audit Anthropic Skills Guide pour {len(skills)} skills :")
    print()

    for skill_dir in skills:
        issues = audit_skill(skill_dir)
        critical = [i for i in issues if i[0] == "CRITICAL"]
        warning = [i for i in issues if i[0] == "WARNING"]
        info = [i for i in issues if i[0] == "INFO"]

        total_critical += len(critical)
        total_warning += len(warning)
        total_info += len(info)

        if not issues:
            print(f"[ OK ] {skill_dir.name}")
        else:
            tag = "[FAIL]" if critical else "[WARN]"
            print(f"{tag} {skill_dir.name}")
            for sev, msg in issues:
                marker = {"CRITICAL": "  ✗", "WARNING": "  ⚠", "INFO": "  ℹ"}[sev]
                print(f"{marker} {msg}")

    print()
    print(f"Total : {total_critical} critical / {total_warning} warning / {total_info} info")

    if total_critical == 0:
        print(f"compliance_ok={len(skills)}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
