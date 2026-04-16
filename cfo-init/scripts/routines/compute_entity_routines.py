#!/usr/bin/env python3
"""
compute_entity_routines.py

Dérive les routines applicables à une entité en lisant son `company.json` et le
catalogue `data/routines-catalog.json`. Écrit le résultat dans
`private/companies/<siren>/routines.json`.

Usage :
  python3 cfo-init/scripts/routines/compute_entity_routines.py --siren 552120222
  python3 cfo-init/scripts/routines/compute_entity_routines.py --siren 552120222 --level 2
  python3 cfo-init/scripts/routines/compute_entity_routines.py --siren 552120222 --dry-run

Exit codes :
  0 = OK
  1 = SIREN introuvable ou company.json absent
  2 = Catalogue invalide
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CATALOG_PATH = ROOT / "data" / "routines-catalog.json"
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


def load_company(siren: str) -> dict:
    """Charge private/companies/<siren>/company.json ou private/company.json (mono)."""
    multi = PRIVATE / "companies" / siren / "company.json"
    mono = PRIVATE / "company.json"
    if multi.exists():
        return json.loads(multi.read_text(encoding="utf-8"))
    if mono.exists():
        d = json.loads(mono.read_text(encoding="utf-8"))
        if d.get("siren") == siren:
            return d
    print(f"ERREUR: company.json introuvable pour SIREN {siren}", file=sys.stderr)
    sys.exit(1)


def load_profile() -> dict:
    profile_path = PRIVATE / "profile.json"
    if not profile_path.exists():
        return {"notifications_level": 1, "notifications_active": True}
    return json.loads(profile_path.read_text(encoding="utf-8"))


def matches_conditions(company: dict, conditions: dict) -> bool:
    """Teste si l'entité matche toutes les conditions d'une routine (AND)."""
    if conditions.get("always"):
        # Règles additionnelles spécifiques même pour universelles
        pass

    classif = company.get("classification", {})

    if "size_in" in conditions:
        if classif.get("taille") not in conditions["size_in"]:
            return False

    if "secteur_category" in conditions:
        if classif.get("secteur_category") != conditions["secteur_category"]:
            return False

    if "secteur_naf_prefix" in conditions:
        naf = classif.get("code_naf", "")
        if not any(naf.startswith(p) for p in conditions["secteur_naf_prefix"]):
            return False

    for bool_key in ("is_startup", "has_investors", "has_covenants", "is_groupe", "seuil_audit"):
        if bool_key in conditions:
            expected = conditions[bool_key]
            actual = classif.get(bool_key, False)
            if bool(actual) != bool(expected):
                return False

    if "has_employees" in conditions:
        if conditions["has_employees"] and classif.get("effectif", 0) <= 0:
            return False

    if "csrd_wave_in" in conditions:
        if classif.get("csrd_wave") not in conditions["csrd_wave_in"]:
            return False

    if "has_stocks" in conditions and conditions["has_stocks"]:
        category = classif.get("secteur_category", "")
        if category not in ("industrie", "commerce", "negoce"):
            return False

    return True


def pick_minute(minute_pool: list[int], siren: str) -> int:
    """Choisit une minute stable par hash du SIREN. Zéro collision :00/:30."""
    if not minute_pool:
        return 13
    idx = int(hashlib.sha256(siren.encode()).hexdigest(), 16) % len(minute_pool)
    return int(minute_pool[idx])


def build_cron_expression(trigger: dict, siren: str) -> str | None:
    """Construit un cron standard 5 champs depuis le catalogue.

    Retourne None si le trigger est `date_derived` ou `date_fixed` (pas de cron).
    """
    ttype = trigger.get("type")
    minute = pick_minute(trigger.get("minute_pool", [13]), siren)
    hour = trigger.get("hour", 9)

    if ttype == "cron_day_of_month":
        day = trigger.get("day", 5)
        months = trigger.get("months_only")
        months_expr = ",".join(str(m) for m in months) if months else "*"
        return f"{minute} {hour} {day} {months_expr} *"

    if ttype == "cron_day_of_week":
        dow = trigger.get("day", 1)  # lundi
        return f"{minute} {hour} * * {dow}"

    if ttype == "date_fixed_annual":
        month = trigger.get("month", 1)
        day = trigger.get("day", 1)
        return f"{minute} {hour} {day} {month} *"

    return None


def compute_next_fire(trigger: dict, company: dict, siren: str, now: dt.datetime) -> dt.datetime | None:
    """Calcule la prochaine date de fire pour les triggers non-cron.

    Pour les triggers cron, on laisse scheduled-tasks faire le calcul.
    Ici on gère uniquement `date_derived` (offset depuis clôture).
    """
    ttype = trigger.get("type")

    if ttype == "date_derived":
        # Cherche date_cloture dans exercice_comptable (YYYY-MM-DD)
        # puis fallback sur classification.date_cloture (MM-DD)
        closing_str = (
            company.get("exercice_comptable", {}).get("date_cloture")
            or company.get("classification", {}).get("date_cloture")
        )
        if not closing_str:
            return None
        parts = closing_str.split("-")
        if len(parts) == 3:
            # Format YYYY-MM-DD : on extrait mois et jour
            month, day = int(parts[1]), int(parts[2])
        elif len(parts) == 2:
            # Format MM-DD legacy
            month, day = int(parts[0]), int(parts[1])
        else:
            return None
        # Prochaine date de clôture (année courante ou suivante)
        year = now.year
        closing_date = dt.datetime(year, month, day, 0, 0, 0)
        if closing_date < now:
            closing_date = closing_date.replace(year=year + 1)

        offset_days = int(trigger.get("offset_from_closing_days", 0))
        fire_at = closing_date + dt.timedelta(days=offset_days)
        hour = trigger.get("hour", 9)
        minute = pick_minute(trigger.get("minute_pool", [13]), siren)
        fire_at = fire_at.replace(hour=hour, minute=minute)

        if fire_at < now:
            return None  # échéance passée, la prochaine sera l'année suivante
        return fire_at

    return None


def compute_routines_for_company(
    company: dict,
    catalog: dict,
    profile: dict,
    override_level: int | None = None,
    now: dt.datetime | None = None,
) -> list[dict]:
    """Retourne la liste des routines applicables à une entité."""
    level = override_level if override_level is not None else profile.get("notifications_level", 1)
    active = profile.get("notifications_active", True)
    if not active or level == 4:
        return []

    siren = company.get("siren", "")
    now = now or dt.datetime.now()

    retained = []
    for routine in catalog.get("routines", []):
        if routine.get("level_min", 1) > level:
            continue

        if not matches_conditions(company, routine.get("conditions", {})):
            continue

        # Construction du triggering (cron ou date_derived)
        trigger = routine.get("trigger", {})

        # Override pour routines qui ont un trigger alternatif (ex: dashboard startup)
        if routine["id"] == "dashboard-cfo" and company.get("classification", {}).get("is_startup"):
            trigger = routine.get("trigger_override_if_startup", trigger)

        cron = build_cron_expression(trigger, siren)
        fire_at = None
        if cron is None:
            fire_at = compute_next_fire(trigger, company, siren, now)
            if fire_at is None:
                # Trigger non calculable, on retient quand même en état "waiting"
                pass

        retained.append({
            "id": routine["id"],
            "name": routine["name"],
            "description": routine["description"],
            "category": routine["category"],
            "frequency": routine["frequency"],
            "skills_chain": routine["skills_chain"],
            "artefact": routine["artefact"],
            "cron_expression": cron,
            "fire_at_absolute": fire_at.isoformat() if fire_at else None,
            "task_id": None,  # rempli par schedule_routines
            "state": "pending",
            "last_run": None,
        })

    return retained


def write_routines_file(siren: str, routines: list[dict]) -> Path:
    """Écrit private/companies/<siren>/routines.json."""
    out_dir = PRIVATE / "companies" / siren
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "routines.json"
    out_path.write_text(
        json.dumps({
            "_meta": {
                "siren": siren,
                "last_computed": dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
                "count": len(routines),
            },
            "routines": routines,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Calcule les routines applicables à une entité.")
    parser.add_argument("--siren", required=True, help="SIREN 9 chiffres de l'entité")
    parser.add_argument("--level", type=int, help="Override du niveau notifications (1-4)")
    parser.add_argument("--dry-run", action="store_true", help="N'écrit pas le fichier, affiche juste")
    args = parser.parse_args()

    catalog = load_catalog()
    company = load_company(args.siren)
    profile = load_profile()

    routines = compute_routines_for_company(company, catalog, profile, override_level=args.level)

    denom = company.get("denomination", "?")
    classif = company.get("classification", {})
    print(f"Entité : {denom} (SIREN {args.siren})")
    print(f"  taille={classif.get('taille')} secteur={classif.get('secteur_category')} csrd={classif.get('csrd_wave')}")
    print(f"  is_startup={classif.get('is_startup', False)} groupe={classif.get('groupe', False)} effectif={classif.get('effectif', 0)}")
    print(f"Niveau notifications : {args.level or profile.get('notifications_level', 1)}")
    print(f"Routines retenues : {len(routines)}")
    for r in routines:
        fire = r.get("fire_at_absolute") or f"cron({r.get('cron_expression')})"
        print(f"  - {r['id']} | {r['frequency']:10} | {fire}")

    if args.dry_run:
        print("Mode dry-run, aucun fichier écrit.")
        return 0

    out_path = write_routines_file(args.siren, routines)
    log("compute", f"siren={args.siren} | {len(routines)} routines retenues")
    print(f"\nÉcrit : {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
