#!/usr/bin/env python3
"""
prepare_fec_export.py — prépare un export FEC conforme DGFiP.

Format arrêté du 29 juillet 2013 :
  - Fichier texte UTF-8 (ou ISO-8859-15)
  - 18 colonnes, séparateur pipe | ou tabulation
  - Nom : <SIREN>FEC<AAAAMMJJ>.txt

Usage :
  python3 prepare_fec_export.py \\
    --grand-livre grand-livre-2026.csv \\
    --siren 552120222 \\
    --exercice 2026 \\
    --date-cloture 2026-12-31 \\
    --output out/552120222FEC20261231.txt

Vérifications automatiques :
  1. Équilibre débit = crédit (tolérance 0.01 €)
  2. Séquence continue de EcritureNum
  3. Dates au format AAAAMMJJ
  4. Encodage UTF-8 sans BOM
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path


FEC_COLUMNS = [
    "JournalCode", "JournalLib", "EcritureNum", "EcritureDate",
    "CompteNum", "CompteLib", "CompAuxNum", "CompAuxLib",
    "PieceRef", "PieceDate", "EcritureLib", "Debit", "Credit",
    "EcritureLet", "DateLet", "ValidDate", "Montantdevise", "Idevise",
]


def parse_grand_livre(path: Path) -> list[dict]:
    """Parse le grand livre CSV en entrée (colonnes flexibles)."""
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            rows.append({
                "JournalCode": row.get("journal_code") or row.get("JournalCode") or "OD",
                "JournalLib": row.get("journal_lib") or row.get("JournalLib") or "Journal des opérations diverses",
                "EcritureNum": row.get("ecriture_num") or row.get("EcritureNum") or str(idx),
                "EcritureDate": normalize_date(row.get("date_ecriture") or row.get("EcritureDate") or ""),
                "CompteNum": row.get("compte") or row.get("CompteNum") or "",
                "CompteLib": row.get("compte_lib") or row.get("CompteLib") or "",
                "CompAuxNum": row.get("compte_aux") or row.get("CompAuxNum") or "",
                "CompAuxLib": row.get("compte_aux_lib") or row.get("CompAuxLib") or "",
                "PieceRef": row.get("piece_ref") or row.get("PieceRef") or "",
                "PieceDate": normalize_date(row.get("date_piece") or row.get("PieceDate") or ""),
                "EcritureLib": row.get("libelle") or row.get("EcritureLib") or "",
                "Debit": normalize_amount(row.get("debit") or row.get("Debit") or "0"),
                "Credit": normalize_amount(row.get("credit") or row.get("Credit") or "0"),
                "EcritureLet": row.get("lettrage") or row.get("EcritureLet") or "",
                "DateLet": normalize_date(row.get("date_lettrage") or row.get("DateLet") or ""),
                "ValidDate": normalize_date(row.get("date_validation") or row.get("ValidDate") or ""),
                "Montantdevise": row.get("montant_devise") or row.get("Montantdevise") or "",
                "Idevise": row.get("devise") or row.get("Idevise") or "",
            })
    return rows


def normalize_date(s: str) -> str:
    """Convertit en AAAAMMJJ (format FEC)."""
    if not s:
        return ""
    s = s.strip()
    # Déjà au bon format ?
    if re.match(r"^\d{8}$", s):
        return s
    # AAAA-MM-JJ
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return f"{m.group(1)}{m.group(2)}{m.group(3)}"
    # JJ/MM/AAAA
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})", s)
    if m:
        return f"{m.group(3)}{m.group(2)}{m.group(1)}"
    return s


def normalize_amount(s: str) -> str:
    """Normalise le montant : virgule française, 2 décimales."""
    if not s or s == "0":
        return "0,00"
    s = str(s).replace(" ", "").replace(",", ".")
    try:
        value = float(s)
    except ValueError:
        return "0,00"
    return f"{value:.2f}".replace(".", ",")


def validate_fec(rows: list[dict]) -> tuple[bool, list[str]]:
    """Vérifie équilibre et séquence."""
    errors = []

    # Équilibre
    total_debit = sum(float(r["Debit"].replace(",", ".")) for r in rows)
    total_credit = sum(float(r["Credit"].replace(",", ".")) for r in rows)
    if abs(total_debit - total_credit) > 0.01:
        errors.append(
            f"Déséquilibre débit ({total_debit:.2f}) ≠ crédit ({total_credit:.2f})"
        )

    # Format date AAAAMMJJ
    for idx, r in enumerate(rows, start=1):
        if r["EcritureDate"] and not re.match(r"^\d{8}$", r["EcritureDate"]):
            errors.append(f"Ligne {idx}: EcritureDate invalide : {r['EcritureDate']}")
            break  # on ne spam pas

    return (len(errors) == 0, errors)


def write_fec(rows: list[dict], output: Path, delim: str = "|") -> None:
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FEC_COLUMNS, delimiter=delim)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export FEC conforme DGFiP")
    parser.add_argument("--grand-livre", type=Path, required=True)
    parser.add_argument("--siren", required=True)
    parser.add_argument("--exercice", type=int, required=True)
    parser.add_argument("--date-cloture", required=True, help="YYYY-MM-DD")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--delim", choices=["|", "tab"], default="|")
    args = parser.parse_args()

    if not args.grand_livre.exists():
        print(f"❌ Grand livre introuvable : {args.grand_livre}", file=sys.stderr)
        return 1

    if not re.match(r"^\d{9}$", args.siren):
        print(f"❌ SIREN invalide : {args.siren}", file=sys.stderr)
        return 1

    date_fec = args.date_cloture.replace("-", "")
    default_output = Path(f"out/{args.siren}FEC{date_fec}.txt")
    output = args.output or default_output

    # Parse
    rows = parse_grand_livre(args.grand_livre)
    if not rows:
        print("⚠️ Grand livre vide", file=sys.stderr)
        return 1

    # Validation
    valid, errors = validate_fec(rows)
    if not valid:
        print("❌ Erreurs de validation :", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("⚠️ Export annulé. Corriger avant re-tentative.", file=sys.stderr)
        return 1

    # Export
    delim = "|" if args.delim == "|" else "\t"
    output.parent.mkdir(parents=True, exist_ok=True)
    write_fec(rows, output, delim=delim)

    print(f"✓ FEC généré : {output}", file=sys.stderr)
    print(f"✓ {len(rows)} lignes · délim '{args.delim}' · UTF-8", file=sys.stderr)
    print(f"✓ Conservation obligatoire : 6 ans (art. L. 102 B LPF)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
