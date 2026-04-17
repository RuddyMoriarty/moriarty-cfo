# Snapshots de regression

Ce dossier contient les outputs JSON de reference pour un echantillon de scripts
deterministes du bundle. Le helper `evals/_helpers/snapshot_compare.py` compare
chaque run a ces snapshots et detecte toute derive silencieuse (ex: un `cir_estime`
qui passerait de 85 800 a 94 380 apres un refacto de `cir_estimator.py`).

## Structure

```
evals/_snapshots/
├── <skill>/
│   └── <script>.<scenario_id>.json   Fige le JSON de sortie avec sort_keys=True
```

Exemple : `cfo-tresorerie/bfr_calculator.bfr_calculator_basic.json` est le snapshot
du scenario "basic" (CA 1,2 M €, creances 200k, dettes 100k) pour `bfr_calculator.py`.

## Mise a jour

Quand un changement de comportement est VOULU (evolution du barreme IS, nouvelle
formule CIR, ajustement benchmark), regenerer les snapshots :

```bash
python3 evals/_helpers/snapshot_compare.py --all --update    # Tous les snapshots
python3 evals/_helpers/snapshot_compare.py --scenario cir_estimator_basic --update
```

Commiter le delta avec un message qui explique le POURQUOI du changement (loi de
finance, barreme ANC, feedback utilisateur). Jamais regenerer sans justifier.

## Ajouter un nouveau scenario

Editer `evals/_helpers/snapshot_compare.py`, section `SCENARIOS`, et ajouter une
entree avec :

- `skill`, `script` : localisation du script
- `args_builder(tmp) -> list[str]` : fonction qui construit les args CLI pour
  une fixture reproductible (jamais de date courante, uniquement des valeurs
  figees)
- `output_file` : nom du fichier JSON produit dans `tmp`, ou `None` si le
  script ecrit sur stdout
- `ignore_keys` : cles a exclure de la comparaison (pour les scripts qui
  embarquent un timestamp de generation, un hash de session, etc.)
- `float_tol` : tolerance relative pour les floats (default 0.5 %)

## Tolerance

Les floats sont compares avec une tolerance relative (default 0.5 %) pour
absorber les variations d'arrondi entre plateformes (Linux CI vs macOS dev).
Les strings, ints et bools sont compares strictement.

## Scripts couverts en v0.2.1

1. `cfo-tresorerie/bfr_calculator` (BFR + benchmarks sectoriels)
2. `cfo-budget-forecast/capex_analyzer` (NPV / IRR / payback)
3. `cfo-fiscalite/is_simulator` (IS + acomptes + solde)
4. `cfo-fiscalite/cir_estimator` (CIR eligible)
5. `cfo-csrd-esg/csrd_scope_calculator` (wave CSRD determinee)
6. `cfo-financement-croissance/valuation_calculator` (DCF + multiples)
7. `cfo-controle-gestion/pricing_simulator` (3 scenarios + best)
8. `cfo-financement-croissance/moriarty_link` (URL + hash SIREN)
