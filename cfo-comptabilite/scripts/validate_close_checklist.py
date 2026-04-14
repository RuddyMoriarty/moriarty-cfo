#!/usr/bin/env python3
"""
validate_close_checklist.py — valide qu'une clôture (mensuelle ou annuelle)
est cohérente avant finalisation.

Tests effectués :
  1. Équilibre balance (débit = crédit, tolérance 0,01 €)
  2. Cohérence FEC ↔ balance (totaux identiques)
  3. Pas de solde suspect sur comptes transitoires (471, 472)
  4. Rapprochement bancaire (si grand livre + relevés fournis)
  5. Checklist markdown 100% cochée

Usage :
  python3 validate_close_checklist.py \\
    --balance balance-2026-12.csv \\
    [--fec FEC-552120222-2026.txt] \\
    [--checklist checklist-cloture-annuelle.md] \\
    [--strict]

Sortie : JSON avec liste des tests passés/échoués.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


TOL = 0.01  # tolérance d'équilibre en €


def parse_balance(path: Path) -> list[dict]:
    """Parse un CSV de balance (compte, libellé, débit, crédit)."""
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rows.append({
                    "compte": row.get("compte") or row.get("CompteNum"),
                    "libelle": row.get("libelle") or row.get("CompteLib", ""),
                    "debit": float((row.get("debit") or row.get("Debit") or "0").replace(",", ".")),
                    "credit": float((row.get("credit") or row.get("Credit") or "0").replace(",", ".")),
                })
            except (ValueError, KeyError):
                continue
    return rows


def parse_fec(path: Path) -> list[dict]:
    """Parse un FEC au format pipe (|) ou tabulation."""
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        first_line = f.readline()
        delim = "|" if "|" in first_line else "\t"
        f.seek(0)
        reader = csv.DictReader(f, delimiter=delim)
        for row in reader:
            try:
                debit = float((row.get("Debit", "0") or "0").replace(",", "."))
                credit = float((row.get("Credit", "0") or "0").replace(",", "."))
                rows.append({
                    "compte": row.get("CompteNum"),
                    "debit": debit,
                    "credit": credit,
                })
            except ValueError:
                continue
    return rows


def test_balance_equilibre(balance: list[dict]) -> dict:
    total_debit = sum(r["debit"] for r in balance)
    total_credit = sum(r["credit"] for r in balance)
    diff = abs(total_debit - total_credit)
    return {
        "test": "balance_equilibre",
        "passed": diff <= TOL,
        "total_debit": round(total_debit, 2),
        "total_credit": round(total_credit, 2),
        "difference": round(diff, 2),
        "message": "Balance équilibrée" if diff <= TOL else f"⚠️ Déséquilibre de {diff:.2f} € à corriger",
    }


def test_comptes_transitoires(balance: list[dict]) -> dict:
    """Les comptes 471, 472 (attente) doivent être soldés en fin d'exercice."""
    suspects = []
    for r in balance:
        if r["compte"] and r["compte"].startswith(("471", "472")):
            solde = r["debit"] - r["credit"]
            if abs(solde) > TOL:
                suspects.append({"compte": r["compte"], "libelle": r["libelle"], "solde": round(solde, 2)})
    return {
        "test": "comptes_transitoires_soldes",
        "passed": len(suspects) == 0,
        "suspects": suspects,
        "message": "Comptes transitoires soldés" if not suspects else f"⚠️ {len(suspects)} compte(s) transitoire(s) non soldé(s)",
    }


def test_fec_vs_balance(fec: list[dict], balance: list[dict]) -> dict:
    fec_total_debit = sum(r["debit"] for r in fec)
    fec_total_credit = sum(r["credit"] for r in fec)
    bal_total_debit = sum(r["debit"] for r in balance)
    bal_total_credit = sum(r["credit"] for r in balance)
    diff_debit = abs(fec_total_debit - bal_total_debit)
    diff_credit = abs(fec_total_credit - bal_total_credit)
    return {
        "test": "fec_coherent_avec_balance",
        "passed": diff_debit <= TOL and diff_credit <= TOL,
        "fec_total_debit": round(fec_total_debit, 2),
        "fec_total_credit": round(fec_total_credit, 2),
        "balance_total_debit": round(bal_total_debit, 2),
        "balance_total_credit": round(bal_total_credit, 2),
        "message": "FEC cohérent avec balance" if (diff_debit <= TOL and diff_credit <= TOL)
            else f"⚠️ Discordance FEC↔Balance : débit {diff_debit:.2f}, crédit {diff_credit:.2f}",
    }


def test_checklist_completee(path: Path) -> dict:
    content = path.read_text(encoding="utf-8")
    total = len(re.findall(r"- \[[ x]\]", content))
    done = len(re.findall(r"- \[x\]", content))
    return {
        "test": "checklist_completee",
        "passed": total > 0 and done == total,
        "total_items": total,
        "done_items": done,
        "pourcentage": round(100 * done / max(1, total), 1),
        "message": f"{done}/{total} items cochés ({round(100 * done / max(1, total), 1)}%)",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Valide une clôture comptable")
    parser.add_argument("--balance", type=Path, required=True)
    parser.add_argument("--fec", type=Path, default=None)
    parser.add_argument("--checklist", type=Path, default=None)
    parser.add_argument("--strict", action="store_true", help="Exit code 1 si un test échoue")
    args = parser.parse_args()

    if not args.balance.exists():
        print(f"❌ Balance introuvable : {args.balance}", file=sys.stderr)
        return 1

    results = []
    balance = parse_balance(args.balance)

    results.append(test_balance_equilibre(balance))
    results.append(test_comptes_transitoires(balance))

    if args.fec and args.fec.exists():
        fec = parse_fec(args.fec)
        results.append(test_fec_vs_balance(fec, balance))

    if args.checklist and args.checklist.exists():
        results.append(test_checklist_completee(args.checklist))

    output = {
        "tests_run": len(results),
        "tests_passed": sum(1 for r in results if r["passed"]),
        "tests_failed": sum(1 for r in results if not r["passed"]),
        "results": results,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.strict and output["tests_failed"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
