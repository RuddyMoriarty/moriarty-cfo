#!/usr/bin/env python3
"""
fct_skill_scripts.py

Tests fonctionnels reels pour les scripts des 9 skills (hors cfo-init).
Pour chaque script, execute avec une fixture minimale et verifie les
assertions sur l'output JSON (structure, types, valeurs).

Appeler avec --skill X --script Y pour tester une combinaison.

Usage :
  python3 evals/_helpers/fct_skill_scripts.py --skill cfo-tresorerie --script bfr_calculator
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def run_script(skill: str, script: str, args: list[str], tmp: Path, stdin_data: str = "") -> tuple[int, str, str]:
    """Execute un script et retourne (exit, stdout, stderr)."""
    script_path = ROOT / skill / "scripts" / f"{script}.py"
    proc = subprocess.run(
        [sys.executable, str(script_path)] + args,
        capture_output=True, text=True, timeout=30, cwd=str(ROOT),
        input=stdin_data if stdin_data else None,
    )
    return proc.returncode, proc.stdout, proc.stderr


def parse_output(stdout: str, output_path: Path | None) -> dict:
    """Retourne le JSON depuis stdout ou le fichier output."""
    if output_path and output_path.exists():
        return json.loads(output_path.read_text(encoding="utf-8"))
    return json.loads(stdout)


# ──────────────────────────────────────────────
# TESTS PAR (skill, script)
# Chaque test retourne (True, detail) si OK, (False, erreur) sinon.
# ──────────────────────────────────────────────

def test_comptabilite_generate_closing_journal(tmp: Path) -> tuple[bool, str]:
    out = tmp / "closing.json"
    rc, stdout, stderr = run_script(
        "cfo-comptabilite", "generate_closing_journal",
        ["--date-cloture", "2026-12-31", "--mode", "mensuel", "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if data.get("mode") != "mensuel":
        return False, f"mode attendu mensuel, obtenu {data.get('mode')}"
    if "ecritures_automatiques" not in data:
        return False, "cle ecritures_automatiques manquante"
    return True, "OK"


def test_comptabilite_validate_close_checklist(tmp: Path) -> tuple[bool, str]:
    balance = tmp / "balance.csv"
    balance.write_text(
        "compte,libelle,debit,credit\n"
        "411000,Clients,10000,0\n"
        "512000,Banque,5000,0\n"
        "401000,Fournisseurs,0,3000\n"
        "101000,Capital,0,12000\n",
        encoding="utf-8",
    )
    rc, stdout, stderr = run_script(
        "cfo-comptabilite", "validate_close_checklist",
        ["--balance", str(balance)],
        tmp,
    )
    if rc not in (0, 1):  # exit 1 si check fail, acceptable
        return False, f"exit {rc}: {stderr[:150]}"
    data = json.loads(stdout)
    if data.get("tests_run", 0) < 1:
        return False, "aucun test execute"
    tests = [r.get("test") for r in data.get("results", [])]
    if "balance_equilibre" not in tests:
        return False, "test balance_equilibre manquant"
    return True, f"{data['tests_run']} tests"


def test_tresorerie_bfr_calculator(tmp: Path) -> tuple[bool, str]:
    out = tmp / "bfr.json"
    rc, stdout, stderr = run_script(
        "cfo-tresorerie", "bfr_calculator",
        ["--creances-clients", "200000", "--dettes-fournisseurs", "100000",
         "--ca-ttc", "1200000", "--achats-ttc", "400000",
         "--stocks", "50000", "--cout-ventes", "300000",
         "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if data.get("ratios", {}).get("dso", 0) <= 0:
        return False, "DSO invalide"
    if "benchmark" not in data:
        return False, "benchmark manquant"
    return True, f"DSO={data['ratios']['dso']}"


def test_tresorerie_forecast_12m(tmp: Path) -> tuple[bool, str]:
    out = tmp / "fc12m.json"
    rc, stdout, stderr = run_script(
        "cfo-tresorerie", "forecast_12m",
        ["--solde-initial", "150000", "--ca-mensuel", "100000",
         "--marge-ebitda", "15", "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    realiste = data.get("scenarios", {}).get("realiste", [])
    if len(realiste) != 12:
        return False, f"12 mois attendus, obtenu {len(realiste)}"
    if "summary" not in data:
        return False, "summary manquant"
    return True, "12 mois OK"


def test_reporting_extract_variances(tmp: Path) -> tuple[bool, str]:
    budget = tmp / "budget.csv"
    budget.write_text("poste,montant\nCA,100000\nAchats,40000\nSalaires,30000\n", encoding="utf-8")
    reel = tmp / "reel.csv"
    reel.write_text("poste,montant\nCA,95000\nAchats,42000\nSalaires,31000\n", encoding="utf-8")
    out = tmp / "var.json"
    rc, stdout, stderr = run_script(
        "cfo-reporting", "extract_variances",
        ["--budget", str(budget), "--reel", str(reel), "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if "variances" not in data or not isinstance(data["variances"], list):
        return False, "variances manquantes ou mauvais type"
    return True, f"{len(data['variances'])} variances"


def test_reporting_compute_kpis(tmp: Path) -> tuple[bool, str]:
    balance = tmp / "balance.csv"
    balance.write_text(
        "compte,libelle,debit,credit\n"
        "70100,Ventes,0,500000\n"
        "60100,Achats,200000,0\n"
        "64100,Salaires,150000,0\n"
        "411000,Clients,80000,0\n"
        "401000,Fournisseurs,0,30000\n"
        "512000,Banque,40000,0\n"
        "101000,Capital,0,100000\n"
        "120000,Resultat,0,40000\n",
        encoding="utf-8",
    )
    out = tmp / "kpis.json"
    rc, stdout, stderr = run_script(
        "cfo-reporting", "compute_kpis",
        ["--balance", str(balance), "--periode", "2026-03", "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if "pme_standard" not in data:
        return False, "pme_standard manquant"
    if "ratios" not in data.get("pme_standard", {}):
        return False, "ratios manquants"
    return True, "KPIs calcules"


def test_controle_pricing_simulator(tmp: Path) -> tuple[bool, str]:
    out = tmp / "pricing.json"
    rc, stdout, stderr = run_script(
        "cfo-controle-gestion", "pricing_simulator",
        ["--prix-actuel", "100", "--volume-actuel", "1000", "--cout-variable", "40",
         "--scenarios", "-10", "5", "10", "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if len(data.get("scenarios", [])) < 3:
        return False, f"3 scenarios attendus, obtenu {len(data.get('scenarios', []))}"
    if "best_scenario" not in data:
        return False, "best_scenario manquant"
    return True, f"{len(data['scenarios'])} scenarios"


def test_controle_variance_analyzer(tmp: Path) -> tuple[bool, str]:
    seg = tmp / "segments.csv"
    seg.write_text(
        "segment,volume_budget,prix_budget,volume_reel,prix_reel\n"
        "A,100,50,110,48\n"
        "B,200,30,180,32\n",
        encoding="utf-8",
    )
    out = tmp / "var.json"
    rc, stdout, stderr = run_script(
        "cfo-controle-gestion", "variance_analyzer",
        ["--segments", str(seg), "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if "summary" not in data:
        return False, "summary manquant"
    if "effet_volume_total" not in data["summary"]:
        return False, "effet_volume_total manquant"
    return True, "OK"


def test_budget_capex_analyzer(tmp: Path) -> tuple[bool, str]:
    out = tmp / "capex.json"
    rc, stdout, stderr = run_script(
        "cfo-budget-forecast", "capex_analyzer",
        ["--investissement", "100000",
         "--cash-flows", "30000", "30000", "30000", "30000", "30000",
         "--wacc", "10", "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if "metrics" not in data:
        return False, "metrics manquant"
    if "npv_eur" not in data["metrics"]:
        return False, "npv_eur manquant"
    return True, f"NPV={data['metrics']['npv_eur']}"


def test_budget_budget_builder(tmp: Path) -> tuple[bool, str]:
    pnl = tmp / "pnl.csv"
    pnl.write_text(
        "poste,montant_annuel\n"
        "ca_ht,1000000\n"
        "charge_achats,400000\n"
        "charge_salaires,350000\n"
        "charge_externes,80000\n",
        encoding="utf-8",
    )
    out = tmp / "budget.json"
    rc, stdout, stderr = run_script(
        "cfo-budget-forecast", "budget_builder",
        ["--pnl-n1", str(pnl), "--growth-ca", "10", "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if "realiste" not in data.get("scenarios", {}):
        return False, "scenario realiste manquant"
    if data["scenarios"]["realiste"].get("ca_ht_annuel", 0) <= 0:
        return False, "CA realiste invalide"
    return True, "OK"


def test_fiscalite_cir_estimator(tmp: Path) -> tuple[bool, str]:
    out = tmp / "cir.json"
    rc, stdout, stderr = run_script(
        "cfo-fiscalite", "cir_estimator",
        ["--salaires-chercheurs", "200000",
         "--sous-traitance-agreee", "50000",
         "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if data.get("cir_estime", 0) <= 0:
        return False, "cir_estime invalide"
    if "depenses_eligibles_detail" not in data:
        return False, "depenses_eligibles_detail manquant"
    return True, f"CIR={data['cir_estime']}"


def test_fiscalite_is_simulator(tmp: Path) -> tuple[bool, str]:
    out = tmp / "is.json"
    rc, stdout, stderr = run_script(
        "cfo-fiscalite", "is_simulator",
        ["--resultat-comptable", "300000",
         "--acomptes-verses", "50000",
         "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if "calcul" not in data:
        return False, "calcul manquant"
    if data["calcul"].get("is_brut", -1) < 0:
        return False, "is_brut invalide"
    return True, "OK"


def test_risques_internal_control_checklist(tmp: Path) -> tuple[bool, str]:
    out = tmp / "ic.json"
    rc, stdout, stderr = run_script(
        "cfo-risques-conformite", "internal_control_checklist",
        ["--fonctions", "achats", "ventes", "tresorerie", "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if data.get("nb_items_total", 0) <= 0:
        return False, "nb_items_total invalide"
    if "checklist" not in data:
        return False, "checklist manquant"
    return True, f"{data['nb_items_total']} items"


def test_risques_veille_scheduler(tmp: Path) -> tuple[bool, str]:
    out = tmp / "veille.json"
    rc, stdout, stderr = run_script(
        "cfo-risques-conformite", "veille_scheduler",
        ["--siren", "552120222", "--niveau", "2", "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if data.get("nb_taches", 0) < 1:
        return False, "nb_taches < 1"
    tasks = data.get("tasks", [])
    if not tasks:
        return False, "tasks vides"
    return True, f"{data['nb_taches']} taches"


def test_financement_diagnostic(tmp: Path) -> tuple[bool, str]:
    out = tmp / "diag.json"
    rc, stdout, stderr = run_script(
        "cfo-financement-croissance", "diagnostic_financement",
        ["--montant", "500000", "--horizon", "mlt",
         "--urgence-jours", "180", "--projet-rd",
         "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if "top_3" not in data:
        return False, "top_3 manquant"
    if not isinstance(data.get("aides_publiques_eligibles"), bool):
        return False, "aides_publiques_eligibles pas bool"
    return True, "OK"


def test_financement_moriarty_link(tmp: Path) -> tuple[bool, str]:
    rc, stdout, stderr = run_script(
        "cfo-financement-croissance", "moriarty_link",
        ["--siren", "552120222", "--audience", "pme"],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = json.loads(stdout)
    url = data.get("moriarty_url", "")
    if not url.startswith("https://themoriarty.fr"):
        return False, f"URL inattendue: {url}"
    h = data.get("siren_hash", "")
    if len(h) != 16:
        return False, f"hash longueur {len(h)} != 16"
    return True, "OK"


def test_csrd_scope_calculator(tmp: Path) -> tuple[bool, str]:
    out = tmp / "scope.json"
    rc, stdout, stderr = run_script(
        "cfo-csrd-esg", "csrd_scope_calculator",
        ["--effectif", "300", "--ca-eur", "60000000", "--bilan-eur", "30000000",
         "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    wave = data.get("wave", "")
    if wave not in ("wave_1", "wave_2", "wave_3", "wave_4", "hors_scope"):
        return False, f"wave inattendu: {wave}"
    return True, f"wave={wave}"


def test_csrd_scope_emissions(tmp: Path) -> tuple[bool, str]:
    out = tmp / "emissions.json"
    rc, stdout, stderr = run_script(
        "cfo-csrd-esg", "scope_emissions_estimator",
        ["--diesel-litres", "1000", "--electricite-kwh", "50000",
         "--pays-electricite", "france", "--achats-services-eur", "100000",
         "--output", str(out)],
        tmp,
    )
    if rc != 0:
        return False, f"exit {rc}: {stderr[:150]}"
    data = parse_output(stdout, out)
    if "emissions_tCO2e" not in data:
        return False, "emissions_tCO2e manquant"
    if "total" not in data["emissions_tCO2e"]:
        return False, "total manquant"
    return True, "OK"


TESTS: dict[str, Any] = {
    "cfo-comptabilite": {
        "generate_closing_journal": test_comptabilite_generate_closing_journal,
        "validate_close_checklist": test_comptabilite_validate_close_checklist,
    },
    "cfo-tresorerie": {
        "bfr_calculator": test_tresorerie_bfr_calculator,
        "forecast_12m": test_tresorerie_forecast_12m,
    },
    "cfo-reporting": {
        "extract_variances": test_reporting_extract_variances,
        "compute_kpis": test_reporting_compute_kpis,
    },
    "cfo-controle-gestion": {
        "pricing_simulator": test_controle_pricing_simulator,
        "variance_analyzer": test_controle_variance_analyzer,
    },
    "cfo-budget-forecast": {
        "capex_analyzer": test_budget_capex_analyzer,
        "budget_builder": test_budget_budget_builder,
    },
    "cfo-fiscalite": {
        "cir_estimator": test_fiscalite_cir_estimator,
        "is_simulator": test_fiscalite_is_simulator,
    },
    "cfo-risques-conformite": {
        "internal_control_checklist": test_risques_internal_control_checklist,
        "veille_scheduler": test_risques_veille_scheduler,
    },
    "cfo-financement-croissance": {
        "diagnostic_financement": test_financement_diagnostic,
        "moriarty_link": test_financement_moriarty_link,
    },
    "cfo-csrd-esg": {
        "csrd_scope_calculator": test_csrd_scope_calculator,
        "scope_emissions_estimator": test_csrd_scope_emissions,
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Tests fonctionnels reels skill+script")
    parser.add_argument("--skill", required=True, choices=sorted(TESTS.keys()))
    parser.add_argument("--script", required=True)
    args = parser.parse_args()

    fn = TESTS.get(args.skill, {}).get(args.script)
    if fn is None:
        print(f"ERREUR: pas de test pour ({args.skill}, {args.script})", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="fct-") as tmpdir:
        tmp = Path(tmpdir)
        try:
            ok, detail = fn(tmp)
        except Exception as e:
            print(f"ERREUR: exception {type(e).__name__}: {e}", file=sys.stderr)
            return 1

    if not ok:
        print(f"ERREUR: {detail}", file=sys.stderr)
        return 1

    print(f"fct_{args.skill.replace('-','_')}_{args.script}_ok=1")
    print(f"detail={detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
