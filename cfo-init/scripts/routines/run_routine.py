#!/usr/bin/env python3
"""
run_routine.py

Exécute une routine pour une entité donnée : charge le template, substitue les
placeholders de base, écrit l'artefact au chemin prévu par le catalogue, et
met à jour routines.json (last_run, state=done).

Les placeholders business ({{ca_mois}}, {{ebe_pct}}, etc.) sont laissés en
l'état dans l'artefact. Ils seront remplis plus tard par les skills listés
dans `skills_chain`, invoqués par le harnais Claude Code après ce run.

Usage :
  python3 cfo-init/scripts/routines/run_routine.py --siren 552120222 --routine cloture-mensuelle
  python3 cfo-init/scripts/routines/run_routine.py --siren 552120222 --routine reporting-trimestriel --period 2026-T2
  python3 cfo-init/scripts/routines/run_routine.py --siren 552120222 --routine cashflow-13w --period 2026-W17

Exit codes :
  0 = OK
  1 = SIREN ou routine introuvable
  2 = Erreur catalogue / template / index
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CATALOG_PATH = ROOT / "data" / "routines-catalog.json"
TEMPLATES_DIR = ROOT / "cfo-init" / "templates"
PRIVATE = ROOT / "private"
LOG_PATH = PRIVATE / "routines.log"


def log(action: str, details: str) -> None:
    """Log horodaté dans private/routines.log."""
    PRIVATE.mkdir(exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} | {action} | {details}\n")


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        print(f"ERREUR: Catalogue introuvable : {CATALOG_PATH}", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERREUR: Catalogue JSON invalide : {e}", file=sys.stderr)
        sys.exit(2)


def load_routines_for_siren(siren: str) -> dict:
    path = PRIVATE / "companies" / siren / "routines.json"
    if not path.exists():
        print(f"ERREUR: routines.json introuvable pour SIREN {siren}. "
              f"Lancer compute_entity_routines.py d'abord.", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERREUR: routines.json invalide pour SIREN {siren} : {e}", file=sys.stderr)
        sys.exit(2)


def save_routines_for_siren(siren: str, data: dict) -> None:
    path = PRIVATE / "companies" / siren / "routines.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_company(siren: str) -> dict:
    """Charge private/companies/<siren>/company.json, migre depuis private/ si besoin."""
    canonical = PRIVATE / "companies" / siren / "company.json"
    if canonical.exists():
        return json.loads(canonical.read_text(encoding="utf-8"))
    mono = PRIVATE / "company.json"
    if mono.exists():
        d = json.loads(mono.read_text(encoding="utf-8"))
        if d.get("siren") == siren:
            canonical.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            return d
    print(f"ERREUR: company.json introuvable pour SIREN {siren}", file=sys.stderr)
    sys.exit(1)


def find_routine_in_catalog(catalog: dict, routine_id: str) -> dict | None:
    for r in catalog.get("routines", []):
        if r.get("id") == routine_id:
            return r
    return None


def find_routine_for_siren(routines_data: dict, routine_id: str) -> dict | None:
    for r in routines_data.get("routines", []):
        if r.get("id") == routine_id:
            return r
    return None


def parse_period(period: str | None, frequency: str, now: dt.datetime) -> dict:
    """Parse le paramètre --period et retourne les placeholders temporels.

    Formats acceptés :
    - YYYY-MM (mensuel)
    - YYYY-Www (hebdomadaire)
    - YYYY-Tq (trimestriel)
    - YYYY (annuel)
    - None : utilise la période courante selon la fréquence
    """
    if period is None:
        year = now.year
        month = now.month
        week = now.isocalendar().week
        quarter = (now.month - 1) // 3 + 1
    else:
        if re.match(r"^\d{4}-\d{2}$", period):
            parts = period.split("-")
            year, month = int(parts[0]), int(parts[1])
            try:
                week = dt.date(year, month, 15).isocalendar().week
            except ValueError:
                week = 1
            quarter = (month - 1) // 3 + 1
        elif re.match(r"^\d{4}-W\d{1,2}$", period):
            parts = period.split("-W")
            year, week = int(parts[0]), int(parts[1])
            # Approxime le mois du milieu de la semaine ISO
            try:
                ref = dt.datetime.strptime(f"{year}-W{week:02d}-1", "%G-W%V-%u")
                month = ref.month
            except ValueError:
                month = 1
            quarter = (month - 1) // 3 + 1
        elif re.match(r"^\d{4}-T[1-4]$", period):
            parts = period.split("-T")
            year, quarter = int(parts[0]), int(parts[1])
            month = (quarter - 1) * 3 + 2  # milieu de trimestre
            week = dt.date(year, month, 15).isocalendar().week
        elif re.match(r"^\d{4}$", period):
            year = int(period)
            month = now.month if year == now.year else 12
            week = now.isocalendar().week if year == now.year else 1
            quarter = (month - 1) // 3 + 1
        else:
            print(f"ERREUR: format --period invalide : {period}. "
                  f"Attendu YYYY-MM, YYYY-Www, YYYY-Tq ou YYYY.", file=sys.stderr)
            sys.exit(2)

    # period_label humain
    if frequency == "monthly":
        period_label = f"{month:02d}/{year}"
    elif frequency == "weekly":
        period_label = f"W{week:02d}/{year}"
    elif frequency == "quarterly":
        period_label = f"T{quarter} {year}"
    elif frequency == "yearly":
        period_label = f"{year}"
    else:
        period_label = f"{month:02d}/{year}"

    return {
        "yyyy": str(year),
        "yyyy_prev": str(year - 1),
        "mm": f"{month:02d}",
        "qq": str(quarter),
        "ww": f"{week:02d}",
        "period_label": period_label,
    }


def build_placeholders(
    siren: str,
    company: dict,
    period_ctx: dict,
) -> dict:
    """Construit le dictionnaire de placeholders de base."""
    now = dt.datetime.now()
    return {
        "siren": siren,
        "denomination": company.get("denomination", siren),
        "date_today": now.strftime("%Y-%m-%d"),
        **period_ctx,
    }


def substitute(template: str, placeholders: dict) -> str:
    """Substitue les placeholders {{key}} dans le texte.

    Les placeholders non présents dans le dict sont laissés en l'état (ils
    seront remplis plus tard par les skills de la chaîne).
    """
    out = template
    for key, value in placeholders.items():
        out = out.replace("{{" + key + "}}", str(value))
    return out


def format_path(pattern: str, placeholders: dict) -> str:
    """Applique les placeholders au path_pattern du catalogue.

    Le pattern utilise des accolades simples {siren}, {yyyy}, etc.
    """
    out = pattern
    for key, value in placeholders.items():
        out = out.replace("{" + key + "}", str(value))
    return out


def run_routine(siren: str, routine_id: str, period: str | None) -> int:
    catalog = load_catalog()
    routines_data = load_routines_for_siren(siren)
    company = load_company(siren)

    routine_catalog = find_routine_in_catalog(catalog, routine_id)
    if routine_catalog is None:
        print(f"ERREUR: routine '{routine_id}' introuvable dans le catalogue.", file=sys.stderr)
        sys.exit(1)

    routine_entity = find_routine_for_siren(routines_data, routine_id)
    if routine_entity is None:
        print(f"ERREUR: routine '{routine_id}' non activée pour SIREN {siren}. "
              f"Vérifier que compute_entity_routines.py l'a bien retenue.", file=sys.stderr)
        sys.exit(1)

    frequency = routine_catalog.get("frequency", "monthly")
    now = dt.datetime.now()
    period_ctx = parse_period(period, frequency, now)
    placeholders = build_placeholders(siren, company, period_ctx)

    # Charge le template
    template_rel = routine_catalog["artefact"]["template"]
    template_path = ROOT / "cfo-init" / template_rel
    if not template_path.exists():
        print(f"ERREUR: template introuvable : {template_path}", file=sys.stderr)
        sys.exit(2)
    template = template_path.read_text(encoding="utf-8")

    # Substitution
    content = substitute(template, placeholders)

    # Calcul du path de sortie
    path_pattern = routine_catalog["artefact"]["path_pattern"]
    out_path_str = format_path(path_pattern, placeholders)
    out_path = ROOT / out_path_str
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")

    # Mise a jour de routines.json : etat "running" (les skills de la chaine
    # doivent encore remplir les donnees business). Le harnais Claude Code
    # passera l'etat en "done" apres succes ou "failed" si un skill echoue.
    now_iso = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    for r in routines_data.get("routines", []):
        if r.get("id") == routine_id:
            r["last_run"] = now_iso
            r["state"] = "running"
            r["last_artefact"] = str(out_path_str)
            r["retry_count"] = r.get("retry_count", 0)
            break
    save_routines_for_siren(siren, routines_data)

    skills = routine_catalog.get("skills_chain", [])
    log("run", f"siren={siren} | routine={routine_id} | period={period_ctx['period_label']} | artefact={out_path_str}")

    print(f"OK: artefact ecrit a {out_path_str}")
    print(f"Skills a invoquer maintenant : {', '.join(skills)}")
    print("Ces skills doivent :")
    print("  1. Lire l'artefact ecrit")
    print("  2. Collecter les donnees business necessaires (balance, CRM, bilans)")
    print("  3. Remplir les placeholders business restants (ca_mois, ebe_pct, etc.)")
    print("  4. Ecraser le fichier avec la version finale")
    print("  5. Mettre state=done dans routines.json (ou state=failed si erreur)")
    print("")
    print("En cas d'echec, le harnais doit :")
    print("  - Mettre state=failed et incrementer retry_count dans routines.json")
    print("  - Si retry_count < 3 : reprogrammer via schedule_routines.py --refresh")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute une routine pour une entite.")
    parser.add_argument("--siren", required=True, help="SIREN 9 chiffres")
    parser.add_argument("--routine", required=True, help="ID de la routine (ex: cloture-mensuelle)")
    parser.add_argument("--period", default=None,
                        help="Periode cible : YYYY-MM | YYYY-Www | YYYY-Tq | YYYY (defaut: periode courante)")
    args = parser.parse_args()

    return run_routine(args.siren, args.routine, args.period)


if __name__ == "__main__":
    sys.exit(main())
