#!/usr/bin/env python3
"""
cfo_unified_dashboard.py, le "livrable du lundi matin" pour un CFO PME.

Agrège dans un seul HTML A4 portrait :
  - Alertes critiques : echeances fiscales < 7 jours, routines en echec
  - 5 KPIs : DSO, BFR, tresorerie, marge EBITDA, CA (si dispos)
  - Prochaines echeances 30 jours (tableau trie par date)
  - Routines actives + prochaine a lancer
  - Progression / achievements

Mode PME : lit private/companies/<siren>/ et ses artefacts (company.json,
calendar-fiscal.json, routines.json, bfr.json si present, kpis.json si present).
Mode EC : utiliser portfolio-dashboard a la place (vue portfolio multi-clients).

Chaque section degrade proprement si la donnee n'existe pas (message
"lancer ./cfo X pour alimenter cette section" au lieu de crasher).

Usage :
  ./cfo unified-dashboard --siren 552120222 --output /tmp/unified.html
  ./cfo unified-dashboard --siren 552120222  # auto : private/companies/.../unified-dashboard.html
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "cfo-reporting" / "templates" / "unified-dashboard.html"

TAILLE_LABELS = {
    "tpe": "TPE",
    "pe": "Petite entreprise",
    "me": "Moyenne entreprise",
    "eti": "ETI",
    "ge": "Grande entreprise",
}


def load_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def read_version() -> str:
    pyproj = ROOT / "pyproject.toml"
    if not pyproj.exists():
        return "?"
    for line in pyproj.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("version"):
            return s.split("=", 1)[1].strip().strip('"').strip("'")
    return "?"


def render_alerts_section(deadlines_urgentes: list[dict], routines_failed: list[dict]) -> str:
    items: list[str] = []
    for e in deadlines_urgentes:
        days = e.get("days_from_now", "?")
        items.append(f"<li><b>J-{days}</b> &middot; {e.get('label','?')} ({e.get('date_absolue','?')})</li>")
    for r in routines_failed:
        items.append(f"<li><b>routine en echec</b> &middot; {r.get('label','?')} (retry {r.get('retry_count', 0)}/3)</li>")

    if not items:
        return ""  # Pas de section alertes si rien a remonter

    return (
        '<section class="alert">'
        '<h2>Alertes critiques</h2>'
        f'<ul style="padding-left: 20px; font-size: 12px;">{"".join(items)}</ul>'
        '</section>'
    )


def render_kpis_grid(kpis: dict, bfr: dict | None, fc13: dict | None) -> str:
    cards: list[str] = []

    # 1. CA HT
    ca = kpis.get("CA_HT") if kpis else None
    if ca:
        cards.append(_kpi_card("CA HT mois", f"{ca:,.0f}", "€"))
    else:
        cards.append(_kpi_placeholder("CA HT mois", "./cfo kpis"))

    # 2. Marge EBITDA
    ebitda = kpis.get("EBITDA_PCT") if kpis else None
    if ebitda is not None:
        severity = "good" if ebitda >= 10 else "warning" if ebitda >= 5 else "critical"
        cards.append(_kpi_card("Marge EBITDA", f"{ebitda:.1f}", "%", severity=severity))
    else:
        cards.append(_kpi_placeholder("Marge EBITDA", "./cfo kpis"))

    # 3. DSO (depuis bfr.json ou kpis.json)
    dso = None
    if bfr:
        dso = bfr.get("ratios", {}).get("dso")
    elif kpis:
        dso = kpis.get("DSO_JOURS")
    if dso is not None:
        severity = "good" if dso <= 45 else "warning" if dso <= 75 else "critical"
        cards.append(_kpi_card("DSO", f"{dso:.0f}", "jours", severity=severity))
    else:
        cards.append(_kpi_placeholder("DSO", "./cfo bfr"))

    # 4. BFR
    if bfr:
        bfr_val = bfr.get("ratios", {}).get("bfr", 0)
        cards.append(_kpi_card("BFR", f"{bfr_val:,.0f}", "€"))
    else:
        cards.append(_kpi_placeholder("BFR", "./cfo bfr"))

    # 5. Tresorerie
    treso = None
    if fc13:
        treso = fc13.get("semaines", [{}])[0].get("solde_fin")
    elif kpis:
        treso = kpis.get("TRESORERIE")
    if treso is not None:
        severity = "good" if treso > 100000 else "warning" if treso > 0 else "critical"
        cards.append(_kpi_card("Tresorerie J", f"{treso:,.0f}", "€", severity=severity))
    else:
        cards.append(_kpi_placeholder("Tresorerie", "./cfo forecast-13w"))

    # 6. Niveau alerte cash (si forecast 13w dispo)
    if fc13:
        niveau = fc13.get("niveau_alerte", "?")
        sev_map = {
            "healthy_vert": "good",
            "vigilance_jaune": "warning",
            "plan_action_orange": "warning",
            "urgence_rouge": "critical",
        }
        cards.append(_kpi_card("Cash 13 sem.", niveau.replace("_", " "), "", severity=sev_map.get(niveau, "")))
    else:
        cards.append(_kpi_placeholder("Cash 13 sem.", "./cfo forecast-13w"))

    return "\n".join(cards)


def _kpi_card(label: str, value: str, unit: str, severity: str = "") -> str:
    cls = f"kpi {severity}" if severity else "kpi"
    unit_span = f'<span class="kpi-unit">{unit}</span>' if unit else ""
    return (
        f'<div class="{cls}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}{unit_span}</div>'
        '</div>'
    )


def _kpi_placeholder(label: str, hint: str) -> str:
    return (
        '<div class="kpi">'
        f'<div class="kpi-label">{label}</div>'
        '<div class="kpi-value" style="color:#999;font-size:14px;">-</div>'
        f'<div class="kpi-note">Lancer <code>{hint}</code></div>'
        '</div>'
    )


def render_deadlines_table(deadlines: list[dict]) -> str:
    if not deadlines:
        return '<div class="empty">Aucune echeance dans les 30 prochains jours.</div>'

    rows: list[str] = []
    for e in sorted(deadlines, key=lambda x: x.get("days_from_now", 999)):
        days = e.get("days_from_now", "?")
        cls = "urgent" if isinstance(days, int) and days <= 7 else "soon" if isinstance(days, int) and days <= 14 else ""
        rows.append(
            f'<tr class="{cls}">'
            f'<td>{e.get("date_absolue","?")}</td>'
            f'<td>J-{days}</td>'
            f'<td>{e.get("label","?")}</td>'
            f'<td>{e.get("type","?")}</td>'
            f'<td>{e.get("skill_recommande","?")}</td>'
            '</tr>'
        )
    return (
        '<table>'
        '<thead><tr><th>Date</th><th>Jours</th><th>Echeance</th><th>Type</th><th>Skill</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
    )


def render_routines_block(routines_data: dict | None) -> str:
    if not routines_data or not routines_data.get("routines"):
        return '<div class="empty">Aucune routine programmee. Lancer <code>./cfo routine-compute --siren X</code></div>'

    routines = routines_data["routines"]
    active = [r for r in routines if r.get("etat") in ("actif", "scheduled")]
    if not active:
        return f'<div class="empty">{len(routines)} routine(s) au catalogue, aucune active.</div>'

    # Prochaine a lancer (date la plus proche)
    sorted_active = sorted(
        [r for r in active if r.get("next_due")],
        key=lambda r: r.get("next_due", "9999-12-31"),
    )
    lines = [f'<p><b>{len(active)}</b> routine(s) active(s) sur {len(routines)} au catalogue.</p>']
    if sorted_active:
        next_r = sorted_active[0]
        lines.append(
            f'<p style="font-size:12px; margin-top:4px;">Prochaine : '
            f'<b>{next_r.get("label","?")}</b> le {next_r.get("next_due","?")}</p>'
        )
    return "".join(lines)


def render_progress_block(progress: dict | None) -> str:
    if not progress:
        return '<div class="empty">Aucune progression enregistree. Lancer <code>./cfo progress --siren X</code></div>'

    unlocked = len(progress.get("unlocked", []))
    total = progress.get("total_achievements", 25)
    pct = int(unlocked / total * 100) if total else 0
    return (
        f'<div class="progress-label">{unlocked} / {total} achievements ({pct} %)</div>'
        '<div class="progress-bar">'
        f'<div class="progress-fill" style="width:{pct}%"></div>'
        '</div>'
    )


def build_dashboard(siren: str, private_dir: Path) -> str:
    company_dir = private_dir / "companies" / siren
    if not company_dir.exists():
        raise FileNotFoundError(
            f"Repertoire client introuvable : {company_dir}. "
            f"Lancer ./cfo init-pme --siren {siren} d'abord."
        )

    company = load_json(company_dir / "company.json") or {}
    calendar = load_json(company_dir / "calendar-fiscal.json") or {}
    routines = load_json(company_dir / "routines.json")
    bfr = load_json(company_dir / "bfr.json")
    fc13 = load_json(company_dir / "fc13.json")
    kpis_file = load_json(company_dir / "kpis.json") or {}
    progress = load_json(private_dir / "cfo-progress.json")

    echeances = calendar.get("echeances", [])
    next_30 = [e for e in echeances if isinstance(e.get("days_from_now"), int) and 0 <= e["days_from_now"] <= 30]
    urgentes = [e for e in next_30 if e.get("days_from_now", 100) <= 7]

    routines_failed = []
    if routines:
        routines_failed = [
            r for r in routines.get("routines", [])
            if r.get("etat") == "failed" or r.get("retry_count", 0) >= 2
        ]

    template = TEMPLATE.read_text(encoding="utf-8")

    classification = company.get("classification", {})
    substitutions = {
        "{{DENOMINATION}}": company.get("denomination", "Societe"),
        "{{SIREN}}": siren,
        "{{TAILLE_LABEL}}": TAILLE_LABELS.get(classification.get("taille", ""), "Non classe"),
        "{{NAF_CODE}}": classification.get("naf_code", "NAF ?"),
        "{{CLOTURE}}": company.get("exercice_comptable", {}).get("date_cloture", "?"),
        "{{GENERATED_AT}}": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M"),
        "{{VERSION}}": read_version(),
        "{{ALERTS_SECTION}}": render_alerts_section(urgentes, routines_failed),
        "{{KPIS_GRID}}": render_kpis_grid(kpis_file, bfr, fc13),
        "{{DEADLINES_TABLE}}": render_deadlines_table(next_30),
        "{{ROUTINES_BLOCK}}": render_routines_block(routines),
        "{{PROGRESS_BLOCK}}": render_progress_block(progress),
    }

    html = template
    for placeholder, value in substitutions.items():
        html = html.replace(placeholder, str(value))
    return html


def main() -> int:
    parser = argparse.ArgumentParser(description="Dashboard CFO unifie mode PME (1 HTML A4)")
    parser.add_argument("--siren", required=True, help="SIREN de la societe")
    parser.add_argument("--private-dir", type=Path, default=ROOT / "private",
                        help="Repertoire prive (default: private/)")
    parser.add_argument("--output", type=Path, default=None,
                        help="Fichier HTML (default: private/companies/<siren>/unified-dashboard.html)")
    args = parser.parse_args()

    if len(args.siren) != 9 or not args.siren.isdigit():
        print("ERREUR: SIREN doit contenir 9 chiffres", file=sys.stderr)
        return 2

    try:
        html = build_dashboard(args.siren, args.private_dir)
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    out = args.output or (args.private_dir / "companies" / args.siren / "unified-dashboard.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"✓ Dashboard unifie genere : {out}", file=sys.stderr)
    print("unified_dashboard_ok=1", file=sys.stderr)
    print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
