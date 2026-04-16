#!/usr/bin/env python3
"""
generate_dashboard.py, génère un dashboard HTML responsive + PDF (Chrome headless).

Input : KPIs (JSON depuis compute_kpis.py) + variances (JSON depuis extract_variances.py)
Output : HTML + PDF (si Chrome dispo)
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "cfo-reporting" / "templates" / "dashboard-cfo.html"


def find_chrome() -> str | None:
    """Trouve une binaire Chrome pour export PDF."""
    for bin_name in ("google-chrome", "chrome", "chromium", "Google Chrome"):
        if shutil.which(bin_name):
            return shutil.which(bin_name)
    # macOS default path
    default = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if Path(default).exists():
        return default
    return None


def render_html(template: str, data: dict) -> str:
    """Rendu simple par remplacement {{KEY}}, pas de Jinja2 en v0.1 pour rester léger."""
    out = template
    for key, value in data.items():
        placeholder = "{{" + key + "}}"
        out = out.replace(placeholder, str(value))
    return out


def build_data(kpis: dict, variances: dict, company: dict) -> dict:
    """Prépare les données pour le template."""
    pl = kpis.get("pme_standard", {}).get("pl", {})
    bilan = kpis.get("pme_standard", {}).get("bilan", {})
    ratios = kpis.get("pme_standard", {}).get("ratios", {})

    variances_rows = ""
    for v in variances.get("variances", [])[:10]:
        direction_emoji = "🟢" if v["direction"] == "favorable" else "🔴"
        variances_rows += f"<tr><td>{v['compte']}</td><td>{v['budget']:,.0f}€</td><td>{v['reel']:,.0f}€</td><td>{v['ecart_eur']:+,.0f}€ ({v['ecart_pct']:+.1f}%)</td><td>{direction_emoji}</td></tr>\n"

    return {
        "COMPANY_NAME": company.get("denomination", "-"),
        "SIREN": company.get("siren", "-"),
        "PERIODE": kpis.get("periode", "-"),
        "DATE_GEN": kpis.get("periode", "-"),
        "CA_HT": f"{pl.get('ca_ht', 0):,.0f}",
        "MARGE_BRUTE": f"{pl.get('marge_brute', 0):,.0f}",
        "TAUX_MARGE_PCT": f"{pl.get('taux_marge_brute_pct', 0):.1f}",
        "EBE": f"{pl.get('ebe', 0):,.0f}",
        "TAUX_EBE_PCT": f"{pl.get('taux_ebe_pct', 0):.1f}",
        "TRESORERIE": f"{bilan.get('tresorerie', 0):,.0f}",
        "BFR": f"{bilan.get('bfr', 0):,.0f}",
        "DSO": f"{ratios.get('dso_jours', 0):.1f}",
        "DPO": f"{ratios.get('dpo_jours', 0):.1f}",
        "VARIANCES_ROWS": variances_rows,
    }


def export_pdf(html_path: Path, pdf_path: Path) -> bool:
    chrome = find_chrome()
    if not chrome:
        print("⚠️ Chrome introuvable, PDF non généré", file=sys.stderr)
        return False

    try:
        subprocess.run([
            chrome, "--headless", "--disable-gpu",
            f"--print-to-pdf={pdf_path}",
            f"file://{html_path.resolve()}",
        ], check=True, capture_output=True, timeout=30)
        return True
    except Exception as e:
        print(f"⚠️ Export PDF échec : {e}", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère dashboard HTML + PDF")
    parser.add_argument("--kpis", type=Path, required=True)
    parser.add_argument("--variances", type=Path, default=None)
    parser.add_argument("--company", type=Path, default=None, help="private/company.json")
    parser.add_argument("--output-html", type=Path, required=True)
    parser.add_argument("--output-pdf", type=Path, default=None)
    args = parser.parse_args()

    if not TEMPLATE.exists():
        print(f"❌ Template introuvable : {TEMPLATE}", file=sys.stderr)
        return 1

    template_content = TEMPLATE.read_text(encoding="utf-8")
    kpis = json.loads(args.kpis.read_text(encoding="utf-8"))
    variances = json.loads(args.variances.read_text(encoding="utf-8")) if args.variances and args.variances.exists() else {"variances": []}
    company = json.loads(args.company.read_text(encoding="utf-8")) if args.company and args.company.exists() else {}
    company_data = company.get("identification", {}) if isinstance(company, dict) else {}

    data = build_data(kpis, variances, company_data)
    html = render_html(template_content, data)

    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(html, encoding="utf-8")
    print(f"✓ Dashboard HTML : {args.output_html}", file=sys.stderr)

    if args.output_pdf:
        args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
        if export_pdf(args.output_html, args.output_pdf):
            print(f"✓ Dashboard PDF : {args.output_pdf}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
