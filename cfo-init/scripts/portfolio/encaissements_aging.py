#!/usr/bin/env python3
"""
encaissements_aging.py

Calcule le aging des factures emises par le cabinet pour chaque client.
Lit private/companies/<siren>/factures.json avec la liste des factures
emises (numero, date, montant HT/TTC, date paiement, statut).

Usage :
  python3 cfo-init/scripts/portfolio/encaissements_aging.py
  python3 cfo-init/scripts/portfolio/encaissements_aging.py --siren 552120222 --detailed
  python3 cfo-init/scripts/portfolio/encaissements_aging.py --json

Buckets aging (Code de commerce art. L. 441-10 LME, delai legal 60 jours) :
  - A jour : < 30 jours
  - Echu 30-60j : en tolerance LME
  - Echu 60-90j : hors LME (relance ferme a envoyer)
  - Echu > 90j : provision a considerer

Exit codes :
  0 = OK
  1 = index.json absent
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"

BUCKETS = [
    ("a_jour", 0, 30),
    ("echu_30_60", 30, 60),
    ("echu_60_90", 60, 90),
    ("echu_sup_90", 90, 99999),
]


def load_index() -> dict:
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent", file=sys.stderr)
        sys.exit(1)
    return json.loads(index_path.read_text(encoding="utf-8"))


def load_factures(siren: str) -> list:
    path = PRIVATE / "companies" / siren / "factures.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("factures", [])


def classify_facture(facture: dict, today: date) -> tuple[str, int] | None:
    """Retourne (bucket, days_echu) ou None si deja encaissee."""
    if facture.get("statut") == "encaissee":
        return None
    try:
        date_facture = date.fromisoformat(facture.get("date_emission", ""))
    except ValueError:
        return None
    days = (today - date_facture).days
    if days < 0:
        return None
    for bucket, low, high in BUCKETS:
        if low <= days < high:
            return bucket, days
    return None


def compute_aging_client(siren: str, today: date) -> dict:
    factures = load_factures(siren)
    result = {bucket: {"count": 0, "montant_ht": 0.0} for bucket, _, _ in BUCKETS}
    result["encaissees"] = {"count": 0, "montant_ht": 0.0}
    result["total_non_encaisse_ht"] = 0.0
    result["nb_factures"] = len(factures)

    for f in factures:
        montant = float(f.get("montant_ht", 0))
        if f.get("statut") == "encaissee":
            result["encaissees"]["count"] += 1
            result["encaissees"]["montant_ht"] += montant
            continue
        classification = classify_facture(f, today)
        if classification is None:
            continue
        bucket, _days = classification
        result[bucket]["count"] += 1
        result[bucket]["montant_ht"] += montant
        result["total_non_encaisse_ht"] += montant

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Aging des encaissements du portfolio EC")
    parser.add_argument("--siren", help="Limite a un seul client (par defaut: tout le portfolio)")
    parser.add_argument("--detailed", action="store_true", help="Liste les factures de chaque bucket")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    args = parser.parse_args()

    index = load_index()
    today = date.today()

    if args.siren:
        clients = [c for c in index.get("clients", []) if c.get("siren") == args.siren]
        if not clients:
            print(f"ERREUR: SIREN {args.siren} introuvable", file=sys.stderr)
            return 1
    else:
        clients = [c for c in index.get("clients", []) if c.get("status") == "actif"]

    output = {"clients": [], "totaux": {b: {"count": 0, "montant_ht": 0.0} for b, _, _ in BUCKETS}}
    output["totaux"]["non_encaisse_ht"] = 0.0

    for c in clients:
        siren = c.get("siren", "?")
        aging = compute_aging_client(siren, today)
        output["clients"].append({
            "siren": siren,
            "denomination": c.get("denomination", "?"),
            "mission_type": c.get("mission_type", "?"),
            "aging": aging,
        })
        for bucket, _, _ in BUCKETS:
            output["totaux"][bucket]["count"] += aging[bucket]["count"]
            output["totaux"][bucket]["montant_ht"] += aging[bucket]["montant_ht"]
        output["totaux"]["non_encaisse_ht"] += aging["total_non_encaisse_ht"]

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
        return 0

    # Affichage texte
    print(f"Aging des encaissements au {today.isoformat()}")
    print(f"Clients analyses : {len(output['clients'])}")
    print()
    print(f"{'Client':<32} {'A jour':<12} {'30-60j':<12} {'60-90j':<12} {'> 90j':<12} {'Total du':<12}")
    print("-" * 96)
    for c in output["clients"]:
        siren = c["siren"]
        denom = c["denomination"][:30]
        a = c["aging"]
        row = (
            f"{denom:<32} "
            f"{a['a_jour']['montant_ht']:>10,.0f} "
            f"{a['echu_30_60']['montant_ht']:>10,.0f} "
            f"{a['echu_60_90']['montant_ht']:>10,.0f} "
            f"{a['echu_sup_90']['montant_ht']:>10,.0f} "
            f"{a['total_non_encaisse_ht']:>10,.0f}"
        )
        print(row.replace(",", " "))

    print("-" * 96)
    tot = output["totaux"]
    total_row = (
        f"{'TOTAL':<32} "
        f"{tot['a_jour']['montant_ht']:>10,.0f} "
        f"{tot['echu_30_60']['montant_ht']:>10,.0f} "
        f"{tot['echu_60_90']['montant_ht']:>10,.0f} "
        f"{tot['echu_sup_90']['montant_ht']:>10,.0f} "
        f"{tot['non_encaisse_ht']:>10,.0f}"
    )
    print(total_row.replace(",", " "))

    # Alertes
    if tot["echu_60_90"]["montant_ht"] > 0 or tot["echu_sup_90"]["montant_ht"] > 0:
        print()
        print("ALERTES :")
        if tot["echu_60_90"]["count"] > 0:
            print(f"  - {tot['echu_60_90']['count']} facture(s) echue(s) 60-90j (hors LME) : relancer")
        if tot["echu_sup_90"]["count"] > 0:
            print(f"  - {tot['echu_sup_90']['count']} facture(s) echue(s) > 90j : considerer provision ou creance douteuse")

    if args.detailed and args.siren:
        factures = load_factures(args.siren)
        print()
        print(f"Detail des factures non encaissees pour {args.siren} :")
        for f in factures:
            if f.get("statut") == "encaissee":
                continue
            cls = classify_facture(f, today)
            if cls is None:
                continue
            bucket, days = cls
            print(f"  [{bucket}] {f.get('numero', '?')} - {f.get('date_emission', '?')} - {f.get('montant_ht', 0):.0f} EUR HT ({days}j)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
