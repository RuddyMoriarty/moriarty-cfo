#!/usr/bin/env python3
"""
check_unified_dashboard.py, test de cfo_unified_dashboard.py.

Valide que le dashboard PME unifie :
  1. Genere un HTML valide avec les sections attendues (alertes, KPIs,
     echeances, routines, progression)
  2. Substitue correctement les placeholders {{DENOMINATION}}, {{SIREN}},
     {{KPIS_GRID}}, etc.
  3. Degrade proprement quand les donnees manquent : chaque KPI absent
     affiche une instruction "Lancer ./cfo X" au lieu de crasher
  4. Detecte les echeances urgentes (< 7 j) et les affiche dans une section
     alerte rouge
  5. Refuse un SIREN invalide
  6. Refuse si le repertoire client n'existe pas (avec message d'aide)
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "cfo-reporting" / "scripts" / "cfo_unified_dashboard.py"


def run_script(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True, text=True, timeout=15, cwd=str(ROOT),
    )
    return proc.returncode, proc.stdout, proc.stderr


def setup_fixture(tmp: Path, siren: str = "552120222") -> Path:
    company_dir = tmp / "companies" / siren
    company_dir.mkdir(parents=True, exist_ok=True)
    (company_dir / "company.json").write_text(json.dumps({
        "siren": siren,
        "denomination": "ACME FIXTURE SAS",
        "classification": {
            "taille": "pe", "naf_code": "62.01Z", "effectif": 25,
            "regime_fiscal": "is",
        },
        "exercice_comptable": {"date_cloture": "2026-12-31"},
    }), encoding="utf-8")
    (company_dir / "calendar-fiscal.json").write_text(json.dumps({
        "echeances": [
            {"date_absolue": "2026-04-20", "days_from_now": 3,
             "label": "TVA avril 2026", "type": "fiscal",
             "skill_recommande": "cfo-fiscalite"},
            {"date_absolue": "2026-04-30", "days_from_now": 13,
             "label": "Effort construction", "type": "social",
             "skill_recommande": "cfo-comptabilite"},
            {"date_absolue": "2026-05-15", "days_from_now": 28,
             "label": "DSN mai", "type": "social",
             "skill_recommande": "cfo-comptabilite"},
        ]
    }), encoding="utf-8")
    (company_dir / "bfr.json").write_text(json.dumps({
        "ratios": {"dso": 62, "dpo": 91, "dio": 0, "bfr": 150000}
    }), encoding="utf-8")
    return company_dir


def check_basic_generation() -> tuple[bool, str]:
    """Scenario complet avec fixtures : verifie les sections principales."""
    with tempfile.TemporaryDirectory(prefix="ud-") as td:
        tmp = Path(td)
        setup_fixture(tmp)
        out = tmp / "dash.html"
        rc, stdout, stderr = run_script([
            "--siren", "552120222",
            "--private-dir", str(tmp),
            "--output", str(out),
        ])
        if rc != 0:
            return False, f"rc={rc}: {stderr[:150]}"
        if not out.exists():
            return False, "fichier HTML non genere"
        html = out.read_text(encoding="utf-8")

        required = [
            "ACME FIXTURE SAS",  # denomination substituee
            "552120222",  # SIREN
            "62.01Z",  # NAF
            "TVA avril 2026",  # echeance injectee
            "DSO",  # KPI cle
            "BFR",
            "Alertes critiques",  # section alerte declenchee par J-3
            "J-3",  # deadline urgente
            "Dashboard CFO unifie",  # title du template
            "moriarty-cfo",  # footer
        ]
        missing = [k for k in required if k not in html]
        if missing:
            return False, f"sections manquantes : {missing}"

        # Pas de placeholder non substitue
        import re
        unresolved = re.findall(r"\{\{[A-Z_]+\}\}", html)
        if unresolved:
            return False, f"placeholders non substitues : {set(unresolved)}"

        return True, f"HTML {len(html)} chars, {len(required)} sections OK"


def check_graceful_degradation() -> tuple[bool, str]:
    """Avec uniquement company.json, les autres sections doivent afficher des instructions."""
    with tempfile.TemporaryDirectory(prefix="ud-") as td:
        tmp = Path(td)
        company_dir = tmp / "companies" / "123456789"
        company_dir.mkdir(parents=True, exist_ok=True)
        (company_dir / "company.json").write_text(json.dumps({
            "siren": "123456789",
            "denomination": "MIN FIXTURE",
            "classification": {"taille": "tpe"},
            "exercice_comptable": {"date_cloture": "2026-12-31"},
        }), encoding="utf-8")

        out = tmp / "min.html"
        rc, _, stderr = run_script([
            "--siren", "123456789",
            "--private-dir", str(tmp),
            "--output", str(out),
        ])
        if rc != 0:
            return False, f"rc={rc}: {stderr[:150]}"
        html = out.read_text(encoding="utf-8")

        # Doit contenir au moins 3 instructions "Lancer ./cfo X" pour les sections manquantes
        hints = html.count("Lancer <code>./cfo")
        if hints < 3:
            return False, f"seulement {hints} instructions de fallback (attendu >= 3)"

        # La section alertes critiques doit etre absente (pas d'echeances)
        if "Alertes critiques" in html:
            return False, "section alertes remontee alors que calendar absent"

        return True, f"{hints} instructions de fallback, alertes absentes"


def check_siren_validation() -> tuple[bool, str]:
    """SIREN a 5 chiffres doit etre rejete."""
    rc, _, stderr = run_script([
        "--siren", "12345",
        "--output", "/tmp/dummy.html",
    ])
    if rc == 0:
        return False, "SIREN a 5 chiffres accepte"
    combined = stderr.lower()
    if "siren" not in combined and "9 chiffres" not in combined:
        return False, f"message pas explicite : {stderr[:100]}"
    return True, f"rejete avec rc={rc}"


def check_missing_company_dir() -> tuple[bool, str]:
    """Si le repertoire client n'existe pas, message d'aide clair."""
    with tempfile.TemporaryDirectory(prefix="ud-") as td:
        tmp = Path(td)
        rc, _, stderr = run_script([
            "--siren", "987654321",
            "--private-dir", str(tmp),
        ])
        if rc == 0:
            return False, "accepte un SIREN sans company_dir"
        if "init-pme" not in stderr and "introuvable" not in stderr.lower():
            return False, f"message d'aide manquant : {stderr[:100]}"
        return True, "rejete avec instruction init-pme"


def main() -> int:
    checks = [
        ("basic_generation", check_basic_generation),
        ("graceful_degradation", check_graceful_degradation),
        ("siren_validation", check_siren_validation),
        ("missing_company_dir", check_missing_company_dir),
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
        print(f"unified_dashboard_ok={ok}")
        return 0
    print(f"ERREUR: {len(checks) - ok} check(s) KO", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
