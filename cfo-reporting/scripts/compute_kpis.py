#!/usr/bin/env python3
"""
compute_kpis.py, calcule les KPIs depuis la balance comptable + données opérationnelles.

Charge le KPI pack sectoriel depuis data/kpi-catalog.json.

Usage :
  python3 compute_kpis.py \\
    --balance balance-2026-03.csv \\
    --operational-data ops-mars.json \\
    --secteur saas \\
    --periode 2026-03 \\
    --output out/kpis-2026-03.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KPI_CATALOG = ROOT / "data" / "kpi-catalog.json"


def load_catalog() -> dict:
    return json.loads(KPI_CATALOG.read_text(encoding="utf-8"))


def load_balance(path: Path) -> dict[str, float]:
    """Charge la balance et renvoie un dict compte → solde net."""
    balance = {}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                compte = row.get("compte") or row.get("CompteNum")
                debit = float((row.get("debit") or row.get("Debit") or "0").replace(",", "."))
                credit = float((row.get("credit") or row.get("Credit") or "0").replace(",", "."))
                balance[compte] = (balance.get(compte, 0) + debit - credit)
            except (ValueError, KeyError):
                continue
    return balance


def sum_accounts(balance: dict, prefix: str) -> float:
    """Somme des soldes de tous les comptes commençant par 'prefix'."""
    return sum(s for c, s in balance.items() if c and c.startswith(prefix))


def compute_pme_kpis(balance: dict, ops: dict, periode: str) -> dict:
    """Calcule les KPIs standard PME depuis la balance."""
    # P&L approché (comptes 6 = charges, comptes 7 = produits, inversés car P&L)
    ca_ht = -sum_accounts(balance, "70")  # classe 70 en crédit = produit
    achats = sum_accounts(balance, "60")   # classe 60 en débit = charge
    services_exterieurs = sum_accounts(balance, "61") + sum_accounts(balance, "62")
    impots_taxes = sum_accounts(balance, "63")
    salaires = sum_accounts(balance, "64")

    marge_brute = ca_ht - achats
    taux_marge_brute = (marge_brute / ca_ht * 100) if ca_ht > 0 else 0

    valeur_ajoutee = ca_ht - (achats + services_exterieurs)
    ebe = valeur_ajoutee - (impots_taxes + salaires)
    taux_ebe = (ebe / ca_ht * 100) if ca_ht > 0 else 0

    # Bilan
    creances_clients = sum_accounts(balance, "411") + sum_accounts(balance, "418")
    dettes_fournisseurs = -sum_accounts(balance, "401") - sum_accounts(balance, "408")
    stocks = sum_accounts(balance, "31") + sum_accounts(balance, "32") + sum_accounts(balance, "33") + sum_accounts(balance, "34") + sum_accounts(balance, "35") + sum_accounts(balance, "37")
    tresorerie = sum_accounts(balance, "512") + sum_accounts(balance, "51")

    bfr = creances_clients + stocks - dettes_fournisseurs

    # Ratios
    dso = creances_clients * 365 / ca_ht if ca_ht > 0 else 0
    dpo = dettes_fournisseurs * 365 / achats if achats > 0 else 0

    return {
        "periode": periode,
        "pl": {
            "ca_ht": round(ca_ht, 0),
            "marge_brute": round(marge_brute, 0),
            "taux_marge_brute_pct": round(taux_marge_brute, 1),
            "valeur_ajoutee": round(valeur_ajoutee, 0),
            "ebe": round(ebe, 0),
            "taux_ebe_pct": round(taux_ebe, 1),
        },
        "bilan": {
            "creances_clients": round(creances_clients, 0),
            "dettes_fournisseurs": round(dettes_fournisseurs, 0),
            "stocks": round(stocks, 0),
            "tresorerie": round(tresorerie, 0),
            "bfr": round(bfr, 0),
        },
        "ratios": {
            "dso_jours": round(dso, 1),
            "dpo_jours": round(dpo, 1),
            "bfr_en_jours_ca": round(bfr * 365 / ca_ht if ca_ht > 0 else 0, 1),
        },
    }


def compute_saas_kpis(ops: dict) -> dict:
    """KPIs spécifiques SaaS depuis data opérationnelle."""
    if not ops:
        return {}

    mrr = ops.get("mrr", 0)
    arr = mrr * 12
    new_mrr = ops.get("new_mrr", 0)
    expansion_mrr = ops.get("expansion_mrr", 0)
    churn_mrr = ops.get("churn_mrr", 0)
    net_new_mrr = new_mrr + expansion_mrr - churn_mrr
    burn = ops.get("burn_mensuel", 0)
    cash = ops.get("cash_actuel", 0)
    nb_clients = ops.get("nb_clients_payants", 0)
    cac = ops.get("cac", 0)
    ltv = ops.get("ltv", 0)

    return {
        "arr": arr,
        "mrr": mrr,
        "new_mrr": new_mrr,
        "net_new_mrr": net_new_mrr,
        "churn_mrr": churn_mrr,
        "nrr_pct": round((mrr + expansion_mrr - churn_mrr) / mrr * 100, 1) if mrr > 0 else 0,
        "burn_mensuel": burn,
        "cash": cash,
        "runway_mois": round(cash / burn, 1) if burn > 0 else None,
        "burn_multiple": round(burn / net_new_mrr, 2) if net_new_mrr > 0 else None,
        "nb_clients_payants": nb_clients,
        "ltv_sur_cac": round(ltv / cac, 1) if cac > 0 else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calcul KPIs depuis balance + ops data")
    parser.add_argument("--balance", type=Path, required=True)
    parser.add_argument("--operational-data", type=Path, default=None)
    parser.add_argument("--secteur", default="services_btob",
                        help="Module sectoriel (saas_techno, industrie, commerce_negoce, services_btob, startup)")
    parser.add_argument("--periode", required=True, help="YYYY-MM")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    catalog = load_catalog()
    balance = load_balance(args.balance)
    ops = json.loads(args.operational_data.read_text(encoding="utf-8")) if args.operational_data and args.operational_data.exists() else {}

    result = {
        "_version": "0.1.0",
        "periode": args.periode,
        "secteur": args.secteur,
        "pme_standard": compute_pme_kpis(balance, ops, args.periode),
    }

    if args.secteur in ("saas_techno", "startup"):
        result["saas"] = compute_saas_kpis(ops)

    # KPI pack sectoriel
    kpi_pack_key = {"saas_techno": "saas", "startup": "startup", "industrie": "industrie",
                    "commerce_negoce": "commerce", "services_btob": "services_btob"}.get(args.secteur, "services_btob")
    result["kpi_pack"] = catalog.get("kpi_packs_par_secteur", {}).get(kpi_pack_key, [])

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ KPIs calculés : {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
