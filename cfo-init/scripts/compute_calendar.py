#!/usr/bin/env python3
"""
compute_calendar.py — génère le calendrier fiscal absolu pour une société.

Lit `data/calendar-fiscal-base.json` (offsets relatifs) et applique la date
de clôture + régime TVA + régime IS pour produire `private/calendar-fiscal.json`
avec les dates absolues sur 18 mois glissants.

Règles d'applicabilité (filtres via `_applicable_si` + `obligation`) :
  - is_regime : uniquement si société à l'IS
  - effectif > 0 : uniquement si salariés
  - effectif >= 50 : uniquement si 50+ salariés
  - regime_tva : filtre selon mensuel/trimestriel/simplifié/franchise

Usage :
  python3 compute_calendar.py \\
    --closing-date 2026-12-31 \\
    --tva-regime reel_normal_mensuelle \\
    --is-regime is \\
    --effectif 40 \\
    --output private/calendar-fiscal.json
"""

from __future__ import annotations

import argparse
import calendar
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_CALENDAR = ROOT / "data" / "calendar-fiscal-base.json"

# Jours fériés France 2026-2028 (statiques, à compléter pour production)
JOURS_FERIES = {
    date(2026, 1, 1), date(2026, 4, 6), date(2026, 5, 1), date(2026, 5, 8),
    date(2026, 5, 14), date(2026, 5, 25), date(2026, 7, 14), date(2026, 8, 15),
    date(2026, 11, 1), date(2026, 11, 11), date(2026, 12, 25),
    date(2027, 1, 1), date(2027, 3, 29), date(2027, 5, 1), date(2027, 5, 6),
    date(2027, 5, 8), date(2027, 5, 17), date(2027, 7, 14), date(2027, 8, 15),
    date(2027, 11, 1), date(2027, 11, 11), date(2027, 12, 25),
    date(2028, 1, 1), date(2028, 4, 17), date(2028, 5, 1), date(2028, 5, 8),
    date(2028, 5, 25), date(2028, 6, 5), date(2028, 7, 14), date(2028, 8, 15),
    date(2028, 11, 1), date(2028, 11, 11), date(2028, 12, 25),
}


# ─────────────────────────────────────────────────────────────────────
# Helpers date
# ─────────────────────────────────────────────────────────────────────

def add_days(d: date, n: int) -> date:
    return d + timedelta(days=n)


def add_months(d: date, n: int) -> date:
    """Ajoute n mois à une date, clamp sur le dernier jour du mois si besoin."""
    month = d.month - 1 + n
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def next_business_day(d: date) -> date:
    """Si d est un jour férié ou week-end, renvoyer le prochain jour ouvré."""
    while d.weekday() >= 5 or d in JOURS_FERIES:
        d += timedelta(days=1)
    return d


def colorize(days_from_now: int) -> str:
    if days_from_now < 0:
        return "⚪"  # passée
    if days_from_now < 7:
        return "🔴"
    if days_from_now < 15:
        return "🟠"
    if days_from_now < 31:
        return "🟡"
    return "🟢"


def parse_offset_days(s: str) -> int:
    """Parse un offset du genre '+75d' ou '+165d'."""
    m = re.match(r"^([+-]?)(\d+)d$", s.strip())
    if not m:
        raise ValueError(f"Offset invalide : {s}")
    sign = -1 if m.group(1) == "-" else 1
    return sign * int(m.group(2))


def parse_annual_calendar(s: str) -> tuple[int, int]:
    """Parse 'annual:DD/MM' → (day, month)."""
    m = re.match(r"^annual:(\d{1,2})/(\d{1,2})$", s.strip())
    if not m:
        raise ValueError(f"Calendar annuel invalide : {s}")
    return int(m.group(1)), int(m.group(2))


# ─────────────────────────────────────────────────────────────────────
# Applicabilité des échéances
# ─────────────────────────────────────────────────────────────────────

def is_applicable(category_meta: dict, context: dict) -> bool:
    """Renvoie True si la catégorie d'échéances s'applique à ce contexte."""
    cond = category_meta.get("_applicable_si", "")
    if not cond:
        return True

    # Conditions simples reconnues
    if "regime_fiscal == 'is'" in cond and context.get("is_regime") != True:
        return False
    if "regime_tva == 'reel_normal'" in cond and "reel_normal" not in context.get("regime_tva", ""):
        return False
    if "AND frequence_declaration == 'mensuelle'" in cond and "mensuelle" not in context.get("regime_tva", ""):
        return False
    if "tva_annuelle_eur < 4000" in cond and "trimestriel" not in context.get("regime_tva", ""):
        return False
    if "regime_tva == 'reel_simplifie'" in cond and context.get("regime_tva") != "reel_simplifie":
        return False
    if "effectif > 0" in cond and context.get("effectif", 0) <= 0:
        return False
    if "csrd_wave != 'hors_scope'" in cond and context.get("csrd_wave", "hors_scope") == "hors_scope":
        return False

    return True


def is_echeance_applicable(echeance: dict, context: dict) -> bool:
    """Filtres au niveau d'une échéance individuelle (effectif >= 50 par ex.)."""
    cond = echeance.get("applicable_si") or echeance.get("_applicable_si", "")
    if not cond:
        return True
    if "effectif >= 50" in cond and context.get("effectif", 0) < 50:
        return False
    return True


# ─────────────────────────────────────────────────────────────────────
# Expansion des offsets
# ─────────────────────────────────────────────────────────────────────

def expand_echeance(echeance: dict, context: dict, today: date, horizon_months: int = 18) -> list[dict]:
    """Transforme une échéance template en une liste de dates absolues sur 18 mois."""
    expanded = []
    horizon_date = add_months(today, horizon_months)

    closing = date.fromisoformat(context["closing_date"])
    closing_current = closing
    # Si la date de clôture est passée, partir de la prochaine clôture
    while closing_current < today:
        closing_current = add_months(closing_current, 12)

    # offset_from_closing : +Nd depuis la clôture
    if "offset_from_closing" in echeance:
        offset_days = parse_offset_days(echeance["offset_from_closing"])
        # Pour 3 prochaines clôtures (horizon 3 ans max)
        for i in range(-1, 3):
            d_closing = add_months(closing_current, 12 * i)
            d = next_business_day(add_days(d_closing, offset_days))
            if today <= d <= horizon_date:
                expanded.append({
                    "date_absolue": d.isoformat(),
                    "exercice_clotures_le": d_closing.isoformat(),
                })

    # offset_each_month : +Nd chaque mois
    elif "offset_each_month" in echeance:
        offset_days = parse_offset_days(echeance["offset_each_month"])
        d = today.replace(day=1)
        for _ in range(horizon_months + 2):
            # Fin du mois M → échéance le jour M+offset
            mois_label = d.strftime("%B %Y")
            last_day = calendar.monthrange(d.year, d.month)[1]
            fin_mois = date(d.year, d.month, last_day)
            echeance_date = next_business_day(add_days(fin_mois, offset_days))
            if today <= echeance_date <= horizon_date:
                expanded.append({
                    "date_absolue": echeance_date.isoformat(),
                    "mois_concerne": mois_label,
                })
            d = add_months(d, 1)

    # offset_each_quarter : +Nd chaque trimestre
    elif "offset_each_quarter" in echeance:
        offset_days = parse_offset_days(echeance["offset_each_quarter"])
        # Identifier les fins de trimestre
        for m in [3, 6, 9, 12]:
            for yoff in range(0, 3):
                annee = today.year + yoff
                fin_trim = date(annee, m, calendar.monthrange(annee, m)[1])
                echeance_date = next_business_day(add_days(fin_trim, offset_days))
                if today <= echeance_date <= horizon_date:
                    expanded.append({
                        "date_absolue": echeance_date.isoformat(),
                        "trimestre": f"T{(m // 3)} {annee}",
                    })

    # offset_calendar : annual:DD/MM
    elif "offset_calendar" in echeance:
        s = echeance["offset_calendar"]
        if s.startswith("annual:"):
            day, month = parse_annual_calendar(s)
            for yoff in range(0, 3):
                annee = today.year + yoff
                try:
                    echeance_date = next_business_day(date(annee, month, day))
                except ValueError:
                    continue
                if today <= echeance_date <= horizon_date:
                    expanded.append({"date_absolue": echeance_date.isoformat()})

    # offset_recurring : non géré ici (géré par skill de veille)
    elif "offset_recurring" in echeance:
        return []

    return expanded


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────

def generate_calendar(context: dict, today: date | None = None) -> dict:
    today = today or date.today()
    base = json.loads(BASE_CALENDAR.read_text(encoding="utf-8"))

    echeances = []
    for key, category in base.items():
        if key.startswith("_"):
            continue
        if not isinstance(category, dict):
            continue
        if not is_applicable(category, context):
            continue

        for template_echeance in category.get("echeances", []):
            if not is_echeance_applicable(template_echeance, context):
                continue

            dates = expand_echeance(template_echeance, context, today)
            for d in dates:
                fire_date = date.fromisoformat(d["date_absolue"])
                days_from_now = (fire_date - today).days
                label = template_echeance["label"]
                # Customisation du label avec le mois/trimestre concerné
                if "mois_concerne" in d:
                    label = f"{label.replace('mois M', d['mois_concerne'])}"
                elif "trimestre" in d:
                    label = f"{label} ({d['trimestre']})"

                echeances.append({
                    "id": f"{template_echeance['id']}-{d['date_absolue']}",
                    "template_id": template_echeance["id"],
                    "label": label,
                    "date_absolue": d["date_absolue"],
                    "type": template_echeance.get("type"),
                    "categorie_calendrier": template_echeance.get("categorie_calendrier"),
                    "skill_recommande": template_echeance.get("skill_recommande"),
                    "days_from_now": days_from_now,
                    "couleur": colorize(days_from_now),
                })

    # Tri par date
    echeances.sort(key=lambda e: e["date_absolue"])

    return {
        "_version": "0.1.0",
        "_generated_at": datetime.utcnow().isoformat() + "Z",
        "_inputs": context,
        "echeances": echeances,
        "_next_30_days_count": sum(1 for e in echeances if 0 <= e["days_from_now"] < 31),
        "_next_90_days_count": sum(1 for e in echeances if 0 <= e["days_from_now"] < 91),
        "_next_18_months_count": len(echeances),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère le calendrier fiscal absolu")
    parser.add_argument("--closing-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--tva-regime", default="reel_normal_mensuelle",
                        choices=["franchise", "reel_simplifie", "reel_normal_mensuelle", "reel_normal_trimestrielle"])
    parser.add_argument("--is-regime", default="is", choices=["is", "ir"])
    parser.add_argument("--effectif", type=int, default=0)
    parser.add_argument("--csrd-wave", default="hors_scope")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    context = {
        "closing_date": args.closing_date,
        "regime_tva": args.tva_regime,
        "is_regime": args.is_regime == "is",
        "effectif": args.effectif,
        "csrd_wave": args.csrd_wave,
    }

    try:
        result = generate_calendar(context)
    except Exception as e:
        print(f"❌ Erreur génération calendrier : {e}", file=sys.stderr)
        return 1

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"✓ {result['_next_30_days_count']} échéances 30j · {result['_next_90_days_count']} à 90j · {result['_next_18_months_count']} sur 18 mois", file=sys.stderr)
        print(f"✓ Écrit dans {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
