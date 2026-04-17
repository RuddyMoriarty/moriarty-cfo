#!/usr/bin/env python3
"""
snapshot_compare.py, v0.2 Module C.

Detection de regression fine : fige les outputs de reference de certains scripts
deterministes dans evals/_snapshots/<skill>/<script>.json, puis compare a chaque
run. Une derive silencieuse (ex: marge_ebitda_pct passe de 15.2 a 15.8 apres
refacto du budget_builder) est detectee immediatement.

Les champs non-deterministes (dates de generation, hash de session) sont listes
dans `ignore_keys` par scenario. Les floats tolerent une marge relative fixe
(default 0.5 %) pour absorber les variations d'arrondi cross-plateforme.

Usage :
  python3 evals/_helpers/snapshot_compare.py --scenario bfr_calculator_basic
  python3 evals/_helpers/snapshot_compare.py --scenario bfr_calculator_basic --update
  python3 evals/_helpers/snapshot_compare.py --all
  python3 evals/_helpers/snapshot_compare.py --all --update  # Regenere tous les snapshots
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOTS_DIR = ROOT / "evals" / "_snapshots"

# Tolerance par defaut pour les floats : 0.5 % relatif.
DEFAULT_FLOAT_TOL = 0.005


# ----------------------------------------------------------------------
# Scenarios : chaque scenario decrit un run deterministe d'un script.
# `args_builder(tmp) -> list[str]` retourne les args CLI.
# `output_file` est le nom du fichier JSON produit dans tmp (ou None si stdout).
# ----------------------------------------------------------------------

def args_bfr_basic(tmp: Path) -> list[str]:
    return [
        "--creances-clients", "200000", "--dettes-fournisseurs", "100000",
        "--ca-ttc", "1200000", "--achats-ttc", "400000",
        "--stocks", "50000", "--cout-ventes", "300000",
        "--secteur", "services_btob",
        "--output", str(tmp / "out.json"),
    ]


def args_capex_basic(tmp: Path) -> list[str]:
    return [
        "--investissement", "500000",
        "--cash-flows", "120000", "140000", "150000", "160000", "180000",
        "--wacc", "10",
        "--output", str(tmp / "out.json"),
    ]


def args_is_simulator_basic(tmp: Path) -> list[str]:
    return [
        "--resultat-comptable", "500000",
        "--output", str(tmp / "out.json"),
    ]


def args_cir_basic(tmp: Path) -> list[str]:
    return [
        "--salaires-chercheurs", "200000",
        "--output", str(tmp / "out.json"),
    ]


def args_csrd_scope_basic(tmp: Path) -> list[str]:
    return [
        "--effectif", "300",
        "--ca-eur", "50000000",
        "--bilan-eur", "30000000",
        "--output", str(tmp / "out.json"),
    ]


def args_valuation_basic(tmp: Path) -> list[str]:
    return [
        "--cash-flows", "100", "120", "140", "160", "180",
        "--ebitda", "200", "--revenue", "1000",
        "--wacc", "12", "--growth-perpetual", "2",
        "--multiples-ebitda", "6", "8", "10",
        "--output", str(tmp / "out.json"),
    ]


def args_pricing_basic(tmp: Path) -> list[str]:
    return [
        "--prix-actuel", "100",
        "--cout-variable", "40",
        "--volume-actuel", "1000",
        "--elasticite", "-1.5",
        "--output", str(tmp / "out.json"),
    ]


def args_moriarty_basic(tmp: Path) -> list[str]:
    # SIREN Carrefour, argument valide. moriarty_link ecrit sur stdout.
    return [
        "--siren", "652014051",
        "--skill-origin", "cfo-financement-croissance",
        "--trigger-id", "snapshot_test",
        "--audience", "pme",
        "--context-summary", "snapshot reference",
    ]


SCENARIOS: dict[str, dict[str, Any]] = {
    "bfr_calculator_basic": {
        "skill": "cfo-tresorerie",
        "script": "bfr_calculator",
        "args_builder": args_bfr_basic,
        "output_file": "out.json",
        "ignore_keys": [],
        "float_tol": DEFAULT_FLOAT_TOL,
    },
    "capex_analyzer_basic": {
        "skill": "cfo-budget-forecast",
        "script": "capex_analyzer",
        "args_builder": args_capex_basic,
        "output_file": "out.json",
        "ignore_keys": [],
        "float_tol": DEFAULT_FLOAT_TOL,
    },
    "is_simulator_basic": {
        "skill": "cfo-fiscalite",
        "script": "is_simulator",
        "args_builder": args_is_simulator_basic,
        "output_file": "out.json",
        "ignore_keys": [],
        "float_tol": DEFAULT_FLOAT_TOL,
    },
    "cir_estimator_basic": {
        "skill": "cfo-fiscalite",
        "script": "cir_estimator",
        "args_builder": args_cir_basic,
        "output_file": "out.json",
        "ignore_keys": [],
        "float_tol": DEFAULT_FLOAT_TOL,
    },
    "csrd_scope_basic": {
        "skill": "cfo-csrd-esg",
        "script": "csrd_scope_calculator",
        "args_builder": args_csrd_scope_basic,
        "output_file": "out.json",
        "ignore_keys": [],
        "float_tol": DEFAULT_FLOAT_TOL,
    },
    "valuation_basic": {
        "skill": "cfo-financement-croissance",
        "script": "valuation_calculator",
        "args_builder": args_valuation_basic,
        "output_file": "out.json",
        "ignore_keys": [],
        "float_tol": DEFAULT_FLOAT_TOL,
    },
    "pricing_simulator_basic": {
        "skill": "cfo-controle-gestion",
        "script": "pricing_simulator",
        "args_builder": args_pricing_basic,
        "output_file": "out.json",
        "ignore_keys": [],
        "float_tol": DEFAULT_FLOAT_TOL,
    },
    "moriarty_link_basic": {
        "skill": "cfo-financement-croissance",
        "script": "moriarty_link",
        "args_builder": args_moriarty_basic,
        "output_file": None,  # stdout
        "ignore_keys": [],
        "float_tol": DEFAULT_FLOAT_TOL,
    },
}


def run_script(skill: str, script: str, args: list[str]) -> tuple[int, str, str]:
    """Execute un script et retourne (exit, stdout, stderr)."""
    script_path = ROOT / skill / "scripts" / f"{script}.py"
    proc = subprocess.run(
        [sys.executable, str(script_path)] + args,
        capture_output=True, text=True, timeout=30, cwd=str(ROOT),
    )
    return proc.returncode, proc.stdout, proc.stderr


def run_scenario(scenario_id: str, tmp: Path) -> dict[str, Any]:
    """Execute le scenario et retourne le JSON d'output."""
    cfg = SCENARIOS[scenario_id]
    args = cfg["args_builder"](tmp)
    rc, stdout, stderr = run_script(cfg["skill"], cfg["script"], args)
    if rc != 0:
        raise RuntimeError(f"Script a echoue rc={rc}: {stderr[:200]}")
    output_file = cfg.get("output_file")
    if output_file:
        path = tmp / output_file
        if not path.exists():
            raise RuntimeError(f"Output attendu non cree : {path}")
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(stdout)


def strip_ignored(data: Any, ignore_keys: list[str]) -> Any:
    """Supprime recursivement les cles listees dans ignore_keys (pour les dicts)."""
    if isinstance(data, dict):
        return {k: strip_ignored(v, ignore_keys) for k, v in data.items() if k not in ignore_keys}
    if isinstance(data, list):
        return [strip_ignored(v, ignore_keys) for v in data]
    return data


def deep_diff(
    expected: Any, actual: Any, float_tol: float, path: str = "$"
) -> list[tuple[str, Any, Any]]:
    """Retourne la liste des differences (path, expected, actual). Vide si identiques."""
    diffs: list[tuple[str, Any, Any]] = []
    if type(expected) is not type(actual):
        # Numeric cross-type (int vs float) accepte
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            pass
        else:
            diffs.append((path, f"type {type(expected).__name__}", f"type {type(actual).__name__}"))
            return diffs

    if isinstance(expected, dict):
        for k in expected:
            if k not in actual:
                diffs.append((f"{path}.{k}", expected[k], "<manquant>"))
            else:
                diffs.extend(deep_diff(expected[k], actual[k], float_tol, f"{path}.{k}"))
        for k in actual:
            if k not in expected:
                diffs.append((f"{path}.{k}", "<absent>", actual[k]))
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            diffs.append((f"{path}[len]", len(expected), len(actual)))
            return diffs
        for i, (e, a) in enumerate(zip(expected, actual)):
            diffs.extend(deep_diff(e, a, float_tol, f"{path}[{i}]"))
    elif isinstance(expected, float) or isinstance(actual, float):
        e = float(expected)
        a = float(actual)
        denom = max(abs(e), abs(a), 1e-9)
        if abs(e - a) / denom > float_tol:
            diffs.append((path, e, a))
    else:
        if expected != actual:
            diffs.append((path, expected, actual))
    return diffs


def snapshot_path(scenario_id: str) -> Path:
    cfg = SCENARIOS[scenario_id]
    return SNAPSHOTS_DIR / cfg["skill"] / f"{cfg['script']}.{scenario_id}.json"


def do_update(scenario_id: str) -> tuple[bool, str]:
    """Regenere le snapshot de reference."""
    with tempfile.TemporaryDirectory(prefix="snap-") as tmpdir:
        tmp = Path(tmpdir)
        try:
            output = run_scenario(scenario_id, tmp)
        except RuntimeError as e:
            return False, str(e)
    cfg = SCENARIOS[scenario_id]
    stripped = strip_ignored(output, cfg.get("ignore_keys", []))
    snap = snapshot_path(scenario_id)
    snap.parent.mkdir(parents=True, exist_ok=True)
    snap.write_text(json.dumps(stripped, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return True, f"snapshot ecrit {snap.relative_to(ROOT)}"


def do_check(scenario_id: str) -> tuple[bool, str]:
    """Compare l'output actuel au snapshot de reference."""
    snap = snapshot_path(scenario_id)
    if not snap.exists():
        return False, f"snapshot manquant : {snap.relative_to(ROOT)}. Lancer --update d'abord."

    cfg = SCENARIOS[scenario_id]
    ignore = cfg.get("ignore_keys", [])
    tol = cfg.get("float_tol", DEFAULT_FLOAT_TOL)

    with tempfile.TemporaryDirectory(prefix="snap-") as tmpdir:
        tmp = Path(tmpdir)
        try:
            actual = run_scenario(scenario_id, tmp)
        except RuntimeError as e:
            return False, str(e)

    expected = json.loads(snap.read_text(encoding="utf-8"))
    actual_stripped = strip_ignored(actual, ignore)

    diffs = deep_diff(expected, actual_stripped, tol)
    if not diffs:
        return True, f"{scenario_id} conforme au snapshot (tol={tol*100:.2f}%)"

    detail_lines = [f"{len(diffs)} deviation(s) detectee(s) vs snapshot :"]
    for p, e, a in diffs[:5]:
        detail_lines.append(f"  {p}: attendu={e} actuel={a}")
    if len(diffs) > 5:
        detail_lines.append(f"  ... et {len(diffs) - 5} autres")
    return False, "\n".join(detail_lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot regression runner")
    parser.add_argument("--scenario", help="Un scenario specifique (ex: bfr_calculator_basic)")
    parser.add_argument("--all", action="store_true", help="Tous les scenarios")
    parser.add_argument("--update", action="store_true", help="Regenere les snapshots au lieu de les verifier")
    parser.add_argument("--list", action="store_true", help="Liste les scenarios disponibles")
    args = parser.parse_args()

    if args.list:
        print("Scenarios disponibles :")
        for sid, cfg in sorted(SCENARIOS.items()):
            print(f"  {sid}  ({cfg['skill']}/{cfg['script']})")
        return 0

    if args.all:
        scenarios = list(SCENARIOS.keys())
    elif args.scenario:
        if args.scenario not in SCENARIOS:
            print(f"ERREUR: scenario inconnu : {args.scenario}", file=sys.stderr)
            print(f"Disponibles : {list(SCENARIOS.keys())}", file=sys.stderr)
            return 2
        scenarios = [args.scenario]
    else:
        print("ERREUR: --scenario X ou --all requis", file=sys.stderr)
        return 2

    fn = do_update if args.update else do_check
    all_ok = True
    for sid in scenarios:
        ok, detail = fn(sid)
        status = "OK" if ok else "KO"
        print(f"[{status}] {sid} : {detail}")
        if not ok:
            all_ok = False

    if args.update:
        print(f"\n✓ {len(scenarios)} snapshot(s) regenere(s)")
        return 0 if all_ok else 1

    if all_ok:
        print(f"\nsnapshot_ok={len(scenarios)}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
