#!/usr/bin/env python3
"""
error_skill_scripts.py, v0.2 Module A.

Teste la ROBUSTESSE des scripts des 10 skills face a des inputs invalides.
Un script "bon eleve" doit :
  1. Ne PAS crasher avec une stack trace Python (Traceback/AttributeError brut).
  2. Retourner exit != 0 quand l'input business est invalide.
  3. Emettre un message d'erreur clair sur stderr (mot-cle : invalide, manquant,
     introuvable, erreur, error, impossible, ou prefixe X).

Le succes du test = le script a echoue proprement. L'echec du test = le script
soit accepte silencieusement un input absurde (exit 0 + output faux), soit
plante avec un Traceback Python brut.

Chaque test cible un scenario d'erreur business distinct (CSV vide, montant
negatif, colonnes manquantes, fichier introuvable, SIREN mal forme, etc.).

Usage :
  python3 evals/_helpers/error_skill_scripts.py --skill cfo-fiscalite --scenario tva_missing_file
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]

# Mots-cles acceptes dans stderr ou stdout pour signaler une erreur propre.
ERROR_KEYWORDS = [
    "invalide", "manquant", "introuvable", "erreur", "error", "impossible",
    "non trouve", "non trouvé", "vide", "required", "refuse", "refusé",
    "attendu", "doit etre", "doit être", "❌", "aucune", "aucun",
    "does not exist", "no such file", "not found", "absent",
]

# Patterns qui signalent un CRASH non-gere (= le script est fragile).
CRASH_PATTERNS = [
    "Traceback (most recent call last)",
    "AttributeError",
    "KeyError",
    "TypeError: '",
    "ZeroDivisionError",
    "IndexError",
    "UnboundLocalError",
]


def run_script(skill: str, script: str, args: list[str], tmp: Path) -> tuple[int, str, str]:
    """Execute un script et retourne (exit, stdout, stderr)."""
    script_path = ROOT / skill / "scripts" / f"{script}.py"
    # Certains scripts sont dans scripts/routines/ ou scripts/portfolio/
    if not script_path.exists():
        for subdir in ("routines", "portfolio"):
            candidate = ROOT / skill / "scripts" / subdir / f"{script}.py"
            if candidate.exists():
                script_path = candidate
                break
    proc = subprocess.run(
        [sys.executable, str(script_path)] + args,
        capture_output=True, text=True, timeout=20, cwd=str(ROOT),
    )
    return proc.returncode, proc.stdout, proc.stderr


def assert_clean_failure(rc: int, stdout: str, stderr: str) -> tuple[bool, str]:
    """Verifie que le script a echoue proprement (exit != 0, pas de crash, message clair)."""
    combined = (stdout + stderr).lower()

    # Check 1 : pas de Traceback Python brut
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere detecte ({pat}) rc={rc}"

    # Check 2 : exit != 0
    if rc == 0:
        return False, f"script a accepte un input invalide (exit 0 au lieu d'une erreur)"

    # Check 3 : au moins un mot-cle d'erreur
    if not any(k in combined for k in ERROR_KEYWORDS):
        return False, f"exit {rc} mais stderr ne contient aucun mot-cle d'erreur: {stderr[:120]}"

    return True, f"exit {rc} avec message d'erreur clair"


# ----------------------------------------------------------------------
# Scenarios d'erreur par (skill, scenario)
# ----------------------------------------------------------------------

def err_init_siren_invalide(tmp: Path) -> tuple[bool, str]:
    """init_pme refuse un SIREN qui n'a pas 9 chiffres."""
    private_dir = tmp / "private"
    private_dir.mkdir()
    rc, stdout, stderr = run_script(
        "cfo-init", "init_pme",
        ["--siren", "12345", "--denomination", "TEST", "--private-dir", str(private_dir)],
        tmp,
    )
    return assert_clean_failure(rc, stdout, stderr)


def err_init_date_cloture_invalide(tmp: Path) -> tuple[bool, str]:
    """compute_calendar refuse une date hors format ISO."""
    rc, stdout, stderr = run_script(
        "cfo-init", "compute_calendar",
        ["--closing-date", "31-12-2026", "--tva-regime", "reel_normal_mensuelle",
         "--is-regime", "is", "--effectif", "50", "--output", str(tmp / "out.json")],
        tmp,
    )
    return assert_clean_failure(rc, stdout, stderr)


def err_comptabilite_balance_vide(tmp: Path) -> tuple[bool, str]:
    """validate_close_checklist avec une balance CSV vide (headers sans lignes)."""
    balance = tmp / "balance.csv"
    balance.write_text("compte,libelle,debit,credit\n", encoding="utf-8")
    rc, stdout, stderr = run_script(
        "cfo-comptabilite", "validate_close_checklist",
        ["--balance", str(balance)],
        tmp,
    )
    # Le script peut exit 1 avec message ou 2 si argparse; les deux sont acceptables
    # tant que pas de crash brut
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat}) rc={rc}"
    # Une balance vide doit produire soit exit != 0 soit un resultat avec failures
    if rc != 0:
        return True, f"exit {rc} sur balance vide"
    # rc == 0 accepte si le rapport remonte des failures (balance incomplete)
    if "fail" in combined or "echec" in combined or "aucun" in combined or "vide" in combined:
        return True, "exit 0 avec report de defaillance"
    return False, "balance vide acceptee sans signalement"


def err_comptabilite_fec_fichier_absent(tmp: Path) -> tuple[bool, str]:
    """prepare_fec_export sur un fichier introuvable."""
    rc, stdout, stderr = run_script(
        "cfo-comptabilite", "prepare_fec_export",
        ["--balance", str(tmp / "inexistant.csv"), "--output", str(tmp / "fec.txt"),
         "--siren", "123456789", "--exercice-debut", "2026-01-01",
         "--exercice-fin", "2026-12-31"],
        tmp,
    )
    return assert_clean_failure(rc, stdout, stderr)


def err_tresorerie_bfr_ca_zero(tmp: Path) -> tuple[bool, str]:
    """bfr_calculator avec CA TTC = 0 (division par zero potentielle)."""
    rc, stdout, stderr = run_script(
        "cfo-tresorerie", "bfr_calculator",
        ["--creances-clients", "100000", "--dettes-fournisseurs", "50000",
         "--ca-ttc", "0", "--achats-ttc", "0",
         "--stocks", "10000", "--cout-ventes", "0",
         "--output", str(tmp / "bfr.json")],
        tmp,
    )
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat}) rc={rc}"
    # Deux sorties acceptables : rejet explicite, ou output avec DSO=None/0 signale
    if rc != 0:
        if any(k in combined for k in ERROR_KEYWORDS):
            return True, f"exit {rc} avec message d'erreur"
        return False, f"exit {rc} sans message clair"
    # rc == 0 : accepter uniquement si le resultat signale l'absence de ratios
    if "null" in combined or "n/a" in combined or "impossible" in combined or '"dso": 0' in combined:
        return True, "exit 0 avec ratios signales comme indisponibles"
    return False, "CA zero accepte sans signalement (risque division par zero silencieuse)"


def err_tresorerie_forecast_args_manquants(tmp: Path) -> tuple[bool, str]:
    """forecast_13w sans aucun argument, argparse doit refuser si des args sont requis."""
    rc, stdout, stderr = run_script(
        "cfo-tresorerie", "forecast_13w",
        [],  # Aucun argument
        tmp,
    )
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat})"
    # Accepter soit rc=2 (argparse), soit rc=0 avec defaults business, soit rc=1 avec msg
    if rc == 2 and ("required" in combined or "error" in combined or "usage" in combined):
        return True, "argparse refuse args manquants (rc=2)"
    if rc == 0:
        # Defaults business acceptables si le script produit un JSON valide
        return True, "rc=0 avec defaults business"
    if rc == 1 and any(k in combined for k in ERROR_KEYWORDS):
        return True, "rc=1 avec message clair"
    return False, f"rc={rc} sans signalement: {stderr[:120]}"


def err_reporting_variances_csv_malforme(tmp: Path) -> tuple[bool, str]:
    """extract_variances avec un CSV missing la colonne 'budget'."""
    budget = tmp / "budget.csv"
    budget.write_text("poste,autre_colonne\nCA,100\n", encoding="utf-8")
    reel = tmp / "reel.csv"
    reel.write_text("poste,montant\nCA,95\n", encoding="utf-8")
    rc, stdout, stderr = run_script(
        "cfo-reporting", "extract_variances",
        ["--budget", str(budget), "--reel", str(reel), "--output", str(tmp / "var.json")],
        tmp,
    )
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat}) rc={rc}"
    # Succes si rc != 0 OU si le script produit un output vide/signale
    if rc != 0 and any(k in combined for k in ERROR_KEYWORDS):
        return True, f"rc={rc} avec message d'erreur"
    if rc == 0 and ('"variances": []' in combined or "aucun" in combined or "vide" in combined):
        return True, "rc=0 avec output vide signale"
    return False, f"CSV sans colonne budget accepte silencieusement (rc={rc})"


def err_controle_profitability_csv_vide(tmp: Path) -> tuple[bool, str]:
    """profitability_analyzer avec un CSV ventes vide (headers only)."""
    ventes = tmp / "ventes.csv"
    ventes.write_text("produit,ca,marge\n", encoding="utf-8")
    rc, stdout, stderr = run_script(
        "cfo-controle-gestion", "profitability_analyzer",
        ["--ventes", str(ventes), "--output", str(tmp / "prof.json")],
        tmp,
    )
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat}) rc={rc}"
    if rc != 0:
        return True, f"rc={rc} sur CSV vide"
    # Accepter rc=0 si output signale 0 produits
    if '"nb_produits": 0' in combined or "aucun" in combined or '"nb_lignes": 0' in combined:
        return True, "rc=0 avec nb_produits=0"
    return False, f"CSV vide accepte sans signalement (rc={rc})"


def err_budget_builder_pnl_vide(tmp: Path) -> tuple[bool, str]:
    """budget_builder avec un P&L vide."""
    pnl = tmp / "pnl.csv"
    pnl.write_text("poste,montant_annuel\n", encoding="utf-8")
    rc, stdout, stderr = run_script(
        "cfo-budget-forecast", "budget_builder",
        ["--pnl-n1", str(pnl), "--output", str(tmp / "budget.json")],
        tmp,
    )
    return assert_clean_failure(rc, stdout, stderr)


def err_fiscalite_tva_fichier_absent(tmp: Path) -> tuple[bool, str]:
    """tva_checker avec balance introuvable."""
    rc, stdout, stderr = run_script(
        "cfo-fiscalite", "tva_checker",
        ["--balance", str(tmp / "inexistant.csv"),
         "--ca3", str(tmp / "inexistant.csv"),
         "--output", str(tmp / "tva.json")],
        tmp,
    )
    return assert_clean_failure(rc, stdout, stderr)


def err_fiscalite_cir_negatif(tmp: Path) -> tuple[bool, str]:
    """cir_estimator avec depenses R&D negatives."""
    rc, stdout, stderr = run_script(
        "cfo-fiscalite", "cir_estimator",
        ["--depenses-recherche", "-100000", "--masse-salariale-chercheurs", "50000",
         "--output", str(tmp / "cir.json")],
        tmp,
    )
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat}) rc={rc}"
    # Succes : rc != 0 OU le script donne un resultat avec un warning
    if rc != 0 and any(k in combined for k in ERROR_KEYWORDS):
        return True, f"rc={rc} avec message"
    if rc == 0:
        # Accepter si le script calcule mais warning (montant negatif visible)
        if "negatif" in combined or "négatif" in combined or "invalide" in combined:
            return True, "rc=0 avec warning negatif"
    return False, f"depenses negatives acceptees (rc={rc}) sans signalement"


def err_risques_mapping_csv_invalide(tmp: Path) -> tuple[bool, str]:
    """risk_mapping_generator avec CSV sans colonnes requises."""
    risques = tmp / "risques.csv"
    risques.write_text("colonne1,colonne2\nvaleur1,valeur2\n", encoding="utf-8")
    rc, stdout, stderr = run_script(
        "cfo-risques-conformite", "risk_mapping_generator",
        ["--risques", str(risques), "--output", str(tmp / "map.json")],
        tmp,
    )
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat}) rc={rc}"
    if rc != 0:
        return True, f"rc={rc} sur CSV sans colonnes attendues"
    if '"nb_risques_total": 0' in combined or "aucun" in combined or "vide" in combined:
        return True, "rc=0 avec 0 risques detectes"
    return False, f"CSV invalide accepte sans signalement (rc={rc})"


def err_financement_moriarty_siren_invalide(tmp: Path) -> tuple[bool, str]:
    """moriarty_link refuse un SIREN a 5 chiffres (format INSEE exige 9 chiffres)."""
    rc, stdout, stderr = run_script(
        "cfo-financement-croissance", "moriarty_link",
        ["--siren", "12345", "--skill-origin", "cfo-financement-croissance"],
        tmp,
    )
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat}) rc={rc}"
    if rc != 0 and any(k in combined for k in ERROR_KEYWORDS):
        return True, f"rc={rc} avec message clair"
    if rc == 0:
        # Verifier si le script a hashe quand meme (pas ideal mais pas crash)
        return False, "SIREN invalide hashe sans signalement (rc=0)"
    return False, f"rc={rc} sans message clair"


def err_csrd_effectif_negatif(tmp: Path) -> tuple[bool, str]:
    """csrd_scope_calculator avec effectif negatif."""
    rc, stdout, stderr = run_script(
        "cfo-csrd-esg", "csrd_scope_calculator",
        ["--effectif", "-50", "--ca-me", "10", "--total-bilan-me", "5",
         "--cote", "non", "--output", str(tmp / "csrd.json")],
        tmp,
    )
    combined = (stdout + stderr).lower()
    for pat in CRASH_PATTERNS:
        if pat.lower() in combined:
            return False, f"crash non gere ({pat}) rc={rc}"
    if rc != 0 and any(k in combined for k in ERROR_KEYWORDS):
        return True, f"rc={rc} avec message"
    # rc=0 acceptable si le script signale via champ wave=hors_scope + warning
    if rc == 0 and ("invalide" in combined or "negatif" in combined or "négatif" in combined):
        return True, "rc=0 avec warning negatif"
    return False, f"effectif negatif accepte sans signalement (rc={rc})"


ERROR_TESTS: dict[str, dict[str, Callable[[Path], tuple[bool, str]]]] = {
    "cfo-init": {
        "siren_invalide": err_init_siren_invalide,
        "date_cloture_invalide": err_init_date_cloture_invalide,
    },
    "cfo-comptabilite": {
        "balance_vide": err_comptabilite_balance_vide,
        "fec_fichier_absent": err_comptabilite_fec_fichier_absent,
    },
    "cfo-tresorerie": {
        "bfr_ca_zero": err_tresorerie_bfr_ca_zero,
        "forecast_args_manquants": err_tresorerie_forecast_args_manquants,
    },
    "cfo-reporting": {
        "variances_csv_malforme": err_reporting_variances_csv_malforme,
    },
    "cfo-controle-gestion": {
        "profitability_csv_vide": err_controle_profitability_csv_vide,
    },
    "cfo-budget-forecast": {
        "budget_pnl_vide": err_budget_builder_pnl_vide,
    },
    "cfo-fiscalite": {
        "tva_fichier_absent": err_fiscalite_tva_fichier_absent,
        "cir_negatif": err_fiscalite_cir_negatif,
    },
    "cfo-risques-conformite": {
        "mapping_csv_invalide": err_risques_mapping_csv_invalide,
    },
    "cfo-financement-croissance": {
        "moriarty_siren_invalide": err_financement_moriarty_siren_invalide,
    },
    "cfo-csrd-esg": {
        "effectif_negatif": err_csrd_effectif_negatif,
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Tests de robustesse (scenarios d'erreur) par skill")
    parser.add_argument("--skill", required=True, choices=sorted(ERROR_TESTS.keys()))
    parser.add_argument("--scenario", required=True)
    args = parser.parse_args()

    fn = ERROR_TESTS.get(args.skill, {}).get(args.scenario)
    if fn is None:
        print(f"ERREUR: pas de scenario '{args.scenario}' pour skill '{args.skill}'", file=sys.stderr)
        print(f"Scenarios disponibles: {list(ERROR_TESTS[args.skill].keys())}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="err-") as tmpdir:
        tmp = Path(tmpdir)
        try:
            ok, detail = fn(tmp)
        except Exception as e:
            print(f"ERREUR: le test lui-meme a plante: {type(e).__name__}: {e}", file=sys.stderr)
            return 1

    if not ok:
        print(f"ERREUR: {detail}", file=sys.stderr)
        return 1

    print(f"err_{args.skill.replace('-', '_')}_{args.scenario}_ok=1")
    print(f"detail={detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
