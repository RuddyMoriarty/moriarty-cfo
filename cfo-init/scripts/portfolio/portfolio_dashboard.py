#!/usr/bin/env python3
"""
portfolio_dashboard.py

Genere un dashboard HTML agrege du portfolio EC : statistiques, alertes
echeances, tableau complet des clients actifs.

Usage :
  python3 cfo-init/scripts/portfolio/portfolio_dashboard.py \\
    --output private/portfolio-dashboard.html [--pdf]

Exit codes :
  0 = OK
  1 = index.json absent
  2 = template HTML introuvable
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRIVATE = ROOT / "private"
TEMPLATE_PATH = ROOT / "cfo-init" / "templates" / "portfolio-dashboard.html"


def load_index() -> dict:
    index_path = PRIVATE / "companies" / "index.json"
    if not index_path.exists():
        print("ERREUR: index.json absent. Lancez init_cabinet.py d'abord.", file=sys.stderr)
        sys.exit(1)
    return json.loads(index_path.read_text(encoding="utf-8"))


def load_cabinet() -> dict:
    cabinet_path = PRIVATE / "cabinet.json"
    if not cabinet_path.exists():
        return {"cabinet": {"siren": "?", "denomination": "(cabinet non initialise)"}}
    return json.loads(cabinet_path.read_text(encoding="utf-8"))


def load_routines_count(siren: str) -> int:
    routines_path = PRIVATE / "companies" / siren / "routines.json"
    if not routines_path.exists():
        return 0
    try:
        data = json.loads(routines_path.read_text(encoding="utf-8"))
        return len(data.get("routines", []))
    except json.JSONDecodeError:
        return 0


def load_next_deadline(siren: str) -> tuple[str | None, int | None]:
    """Retourne (date_ISO, jours_restants) de la prochaine echeance du client."""
    cal_path = PRIVATE / "companies" / siren / "calendar-fiscal.json"
    if not cal_path.exists():
        return None, None
    try:
        cal = json.loads(cal_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, None

    today = date.today()
    upcoming = []
    for e in cal.get("echeances", []):
        date_str = e.get("date_absolue")
        if not date_str:
            continue
        try:
            d = date.fromisoformat(date_str)
        except ValueError:
            continue
        if d >= today:
            upcoming.append((d, e))

    if not upcoming:
        return None, None
    upcoming.sort(key=lambda x: x[0])
    d, _ = upcoming[0]
    return d.isoformat(), (d - today).days


def compute_alerts(clients: list, today: date) -> list:
    """Retourne la liste des alertes echeances (rouge < 7j, orange 7-14j, jaune 15-30j)."""
    alerts = []
    for c in clients:
        if c.get("status") != "actif":
            continue
        deadline_iso, days = load_next_deadline(c.get("siren", ""))
        if deadline_iso is None or days is None:
            continue
        if days < 7:
            couleur = "rouge"
        elif days < 15:
            couleur = "orange"
        elif days < 31:
            couleur = "jaune"
        else:
            continue
        alerts.append({
            "couleur": couleur,
            "days": days,
            "deadline": deadline_iso,
            "siren": c.get("siren"),
            "denomination": c.get("denomination"),
        })
    alerts.sort(key=lambda a: a["days"])
    return alerts


def build_alerts_html(alerts: list) -> str:
    if not alerts:
        return (
            '<div class="empty">Aucune echeance dans les 30 prochains jours.</div>'
        )
    lines = []
    for a in alerts:
        label = f"{a['denomination']} (SIREN {a['siren']})"
        meta = f"J-{a['days']} &middot; {a['deadline']}"
        lines.append(
            f'<div class="alerte {a["couleur"]}">'
            f'<div class="bar"></div>'
            f'<div class="body">'
            f'<span class="alerte-label">{label}</span>'
            f'<span class="alerte-meta">{meta}</span>'
            f'</div>'
            f'</div>'
        )
    return "\n".join(lines)


def build_clients_rows(clients: list) -> str:
    rows = []
    for c in sorted(clients, key=lambda x: x.get("denomination", "")):
        siren = c.get("siren", "?")
        deadline_iso, days = load_next_deadline(siren)
        deadline_str = f"{deadline_iso} ({days} j)" if deadline_iso else "—"
        status_class = "badge-actif" if c.get("status") == "actif" else "badge-archive"
        taille = c.get("taille", "?")
        rows.append(
            "<tr>"
            f'<td class="siren">{siren}</td>'
            f'<td class="denom">{c.get("denomination", "?")}</td>'
            f'<td><span class="badge badge-taille">{taille}</span></td>'
            f'<td>{c.get("mission_type", "?")}</td>'
            f'<td>{c.get("referent") or "—"}</td>'
            f'<td>{load_routines_count(siren)}</td>'
            f"<td>{deadline_str}</td>"
            f'<td><span class="badge {status_class}">{c.get("status", "?")}</span></td>'
            "</tr>"
        )
    return "\n".join(rows)


def build_resume(alerts: list, clients_actifs: int) -> str:
    if clients_actifs == 0:
        return "Aucun client actif dans le portfolio."
    rouges = len([a for a in alerts if a["couleur"] == "rouge"])
    oranges = len([a for a in alerts if a["couleur"] == "orange"])
    jaunes = len([a for a in alerts if a["couleur"] == "jaune"])
    parts = [f"{clients_actifs} client(s) actif(s)."]
    if rouges:
        parts.append(f"Echeance(s) urgente(s) (< 7j) : {rouges}.")
    if oranges:
        parts.append(f"A preparer (7-14j) : {oranges}.")
    if jaunes:
        parts.append(f"A planifier (15-30j) : {jaunes}.")
    if not (rouges or oranges or jaunes):
        parts.append("Aucune echeance urgente ce mois-ci.")
    return " ".join(parts)


def render_html(template: str, data: dict) -> str:
    out = template
    for key, value in data.items():
        out = out.replace("{{" + key + "}}", str(value))
    return out


def export_pdf(html_path: Path, pdf_path: Path) -> bool:
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chrome")
    if chrome is None:
        # macOS fallback
        mac_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if mac_chrome.exists():
            chrome = str(mac_chrome)
    if chrome is None:
        print("AVERTISSEMENT: Chrome introuvable, PDF non genere", file=sys.stderr)
        return False
    try:
        subprocess.run(
            [
                chrome, "--headless", "--disable-gpu",
                f"--print-to-pdf={pdf_path}",
                f"file://{html_path.resolve()}",
            ],
            check=True, capture_output=True, timeout=30,
        )
        return pdf_path.exists()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"AVERTISSEMENT: echec PDF : {e}", file=sys.stderr)
        return False


def main() -> int:
    global PRIVATE
    parser = argparse.ArgumentParser(description="Dashboard HTML du portfolio EC")
    parser.add_argument("--output", type=Path, default=None,
                        help="Fichier HTML de sortie (default: <private>/portfolio-dashboard.html)")
    parser.add_argument("--pdf", action="store_true", help="Exporte aussi en PDF via Chrome")
    parser.add_argument("--private-dir", type=Path, default=None,
                        help="Repertoire prive (default: <repo>/private)")
    args = parser.parse_args()
    if args.private_dir is not None:
        PRIVATE = args.private_dir
    if args.output is None:
        args.output = PRIVATE / "portfolio-dashboard.html"

    if not TEMPLATE_PATH.exists():
        print(f"ERREUR: template introuvable : {TEMPLATE_PATH}", file=sys.stderr)
        return 2

    cabinet = load_cabinet()
    index = load_index()
    clients = index.get("clients", [])
    today = date.today()

    clients_actifs = [c for c in clients if c.get("status") == "actif"]
    clients_archives = [c for c in clients if c.get("status") == "archive"]

    alerts = compute_alerts(clients_actifs, today)
    alertes_7j = len([a for a in alerts if a["couleur"] == "rouge"])

    routines_total = sum(load_routines_count(c.get("siren", "")) for c in clients_actifs)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    data = {
        "CABINET_NOM": cabinet.get("cabinet", {}).get("denomination", "?"),
        "CABINET_SIREN": cabinet.get("cabinet", {}).get("siren", "?"),
        "DATE_GENERATION": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "CLIENTS_ACTIFS": len(clients_actifs),
        "CLIENTS_ARCHIVES": len(clients_archives),
        "ROUTINES_COUNT": routines_total,
        "ALERTES_7J": alertes_7j,
        "RESUME_TEXT": build_resume(alerts, len(clients_actifs)),
        "ALERTES_ROWS": build_alerts_html(alerts),
        "CLIENTS_ROWS": build_clients_rows(clients),
    }

    html = render_html(template, data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")

    print(f"OK: dashboard HTML genere : {args.output}")

    if args.pdf:
        pdf_path = args.output.with_suffix(".pdf")
        if export_pdf(args.output, pdf_path):
            print(f"OK: PDF genere : {pdf_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
