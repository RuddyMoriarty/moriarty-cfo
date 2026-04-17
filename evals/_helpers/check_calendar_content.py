#!/usr/bin/env python3
"""
check_calendar_content.py, validation de contenu du calendrier fiscal.

Remplace les tests cfo-init-fct-01/02 qui se contentaient de verifier
l'existence du fichier + l'absence de Traceback. Ici on execute
compute_calendar.py dans deux configurations reelles et on valide le
CONTENU du JSON produit (nombre d'echeances par type, presence des
natures attendues, horizon 18 mois).

2 scenarios :
  1. Cloture 31/12 + TVA mensuelle + IS : doit generer >= 12 TVA, >= 4 IS,
     >= 12 DSN, >= 50 echeances sur 18 mois.
  2. Cloture 30/06 + TVA trimestrielle + IS : doit generer >= 4 CA3,
     >= 12 DSN, >= 30 echeances sur 18 mois.

Usage :
  python3 evals/_helpers/check_calendar_content.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "cfo-init" / "scripts" / "compute_calendar.py"


def run_calendar(
    tmp: Path,
    closing_date: str,
    tva_regime: str,
    effectif: int,
) -> tuple[int, dict | None, str]:
    """Execute compute_calendar et charge le JSON produit."""
    out = tmp / f"calendar-{closing_date}.json"
    proc = subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "--closing-date", closing_date,
            "--tva-regime", tva_regime,
            "--is-regime", "is",
            "--effectif", str(effectif),
            "--output", str(out),
        ],
        capture_output=True, text=True, timeout=15, cwd=str(ROOT),
    )
    if proc.returncode != 0:
        return proc.returncode, None, proc.stderr[:200]
    if not out.exists():
        return 1, None, "fichier calendrier non cree"
    return 0, json.loads(out.read_text(encoding="utf-8")), ""


def check_scenario(
    closing_date: str,
    tva_regime: str,
    effectif: int,
    min_tva: int,
    min_is: int,
    min_dsn: int,
    min_total: int,
) -> tuple[bool, str]:
    """Execute un scenario et valide les seuils de contenu."""
    with tempfile.TemporaryDirectory(prefix="cal-") as tmpdir:
        tmp = Path(tmpdir)
        rc, data, err = run_calendar(tmp, closing_date, tva_regime, effectif)
        if rc != 0:
            return False, f"script rc={rc}: {err}"

    # Validation schema
    for key in ("_version", "echeances", "_next_30_days_count",
                "_next_90_days_count", "_next_18_months_count"):
        if key not in data:
            return False, f"cle manquante dans le JSON : {key}"

    echeances = data["echeances"]
    if not isinstance(echeances, list):
        return False, f"'echeances' doit etre une liste, obtenu {type(echeances).__name__}"

    # Compter par type de label
    labels = [e.get("label", "") for e in echeances]
    tva_count = sum(1 for label in labels if "TVA" in label.upper())
    is_count = sum(1 for label in labels
                   if "acompte is" in label.lower() or "solde is" in label.lower()
                   or "liasse" in label.lower())
    dsn_count = sum(1 for label in labels if "DSN" in label or "URSSAF" in label.upper())
    total = len(echeances)

    # Verifications seuils
    if tva_count < min_tva:
        return False, f"TVA {tva_count} < seuil {min_tva}"
    if is_count < min_is:
        return False, f"IS/liasse {is_count} < seuil {min_is}"
    if dsn_count < min_dsn:
        return False, f"DSN/URSSAF {dsn_count} < seuil {min_dsn}"
    if total < min_total:
        return False, f"Total echeances {total} < seuil {min_total}"

    # Verifier que chaque echeance a les champs minimaux
    for e in echeances[:5]:
        for field in ("date_absolue", "label", "type"):
            if field not in e:
                return False, f"echeance manque champ '{field}' : {e}"

    return True, f"{total} echeances (TVA={tva_count}, IS={is_count}, DSN={dsn_count})"


def main() -> int:
    scenarios = [
        {
            "name": "mensuel_31dec",
            "closing": "2026-12-31",
            "tva": "reel_normal_mensuelle",
            "effectif": 100,
            "min_tva": 12,
            "min_is": 5,  # 4 acomptes + solde/liasse
            "min_dsn": 12,
            "min_total": 50,
        },
        {
            "name": "trimestriel_30juin",
            "closing": "2026-06-30",
            "tva": "reel_normal_trimestrielle",
            "effectif": 25,
            "min_tva": 4,  # 4 CA3 trimestriels sur 12 mois minimum
            "min_is": 4,
            "min_dsn": 12,
            "min_total": 30,
        },
    ]

    ok_count = 0
    for s in scenarios:
        ok, detail = check_scenario(
            closing_date=s["closing"],
            tva_regime=s["tva"],
            effectif=s["effectif"],
            min_tva=s["min_tva"],
            min_is=s["min_is"],
            min_dsn=s["min_dsn"],
            min_total=s["min_total"],
        )
        status = "OK" if ok else "KO"
        print(f"[{status}] {s['name']} : {detail}")
        if ok:
            ok_count += 1

    if ok_count == len(scenarios):
        print(f"calendar_content_ok={ok_count}")
        return 0
    print(f"ERREUR: {len(scenarios) - ok_count} scenario(s) KO", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
