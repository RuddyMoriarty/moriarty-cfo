# Coverage snapshot, v0.3.2

Snapshot du rapport `coverage.py` pour illustrer la couverture reelle des 27 scripts du bundle. A regenerer apres chaque evolution majeure via `python3 evals/run_coverage.py`.

## Resultat global

**77.5 % de couverture** sur 3608 lignes de code executable, 813 lignes non couvertes.

## Detail par skill

### Couverture forte (>= 85 %)

| Script | Stmts | Miss | Cover | Notes |
|--------|-------|------|-------|-------|
| `cfo-financement-croissance/moriarty_link.py` | 29 | 0 | **100.0%** | Script le plus simple |
| `cfo-tresorerie/forecast_12m.py` | 61 | 1 | 98.4% | - |
| `cfo-controle-gestion/pricing_simulator.py` | 39 | 1 | 97.4% | - |
| `cfo-csrd-esg/scope_emissions_estimator.py` | 59 | 2 | 96.6% | - |
| `cfo-financement-croissance/valuation_calculator.py` | 54 | 2 | 96.3% | - |
| `cfo-init/compute_calendar.py` | 187 | 11 | 94.1% | Script complexe bien couvert |
| `cfo-reporting/extract_variances.py` | 62 | 4 | 93.5% | Durci en v0.2.0 |
| `cfo-controle-gestion/profitability_analyzer.py` | 74 | 5 | 93.2% | - |
| `cfo-controle-gestion/variance_analyzer.py` | 43 | 3 | 93.0% | - |
| `cfo-risques/internal_control_checklist.py` | 28 | 2 | 92.9% | - |
| `cfo-financement/diagnostic_financement.py` | 40 | 3 | 92.5% | - |
| `cfo-risques/veille_scheduler.py` | 39 | 3 | 92.3% | - |
| `cfo-budget-forecast/budget_builder.py` | 54 | 5 | 90.7% | Durci en v0.2.0 |
| `cfo-csrd-esg/double_materiality_assessor.py` | 55 | 6 | 89.1% | - |
| `cfo-risques/risk_mapping_generator.py` | 58 | 7 | 87.9% | Durci en v0.2.0 |
| `cfo-fiscalite/cir_estimator.py` | 40 | 5 | 87.5% | - |
| `cfo-fiscalite/is_simulator.py` | 40 | 5 | 87.5% | - |
| `cfo-budget-forecast/capex_analyzer.py` | 62 | 8 | 87.1% | - |
| `cfo-fiscalite/tva_checker.py` | 69 | 9 | 87.0% | Durci en v0.2.0 |
| `cfo-init/portfolio/generate_lettre_mission.py` | 92 | 12 | 87.0% | - |
| `cfo-tresorerie/bfr_calculator.py` | 73 | 10 | 86.3% | Durci en v0.2.0 |
| `cfo-init/routines/compute_entity_routines.py` | 176 | 26 | 85.2% | - |

### Couverture moyenne (70 % a 85 %)

| Script | Stmts | Miss | Cover |
|--------|-------|------|-------|
| `cfo-budget-forecast/rolling_forecast.py` | 66 | 10 | 84.8% |
| `cfo-csrd-esg/csrd_scope_calculator.py` | 38 | 7 | 81.6% |
| `cfo-init/routines/schedule_routines.py` | 130 | 25 | 80.8% |
| `cfo-reporting/cfo_unified_dashboard.py` | 154 | 31 | 79.9% |
| `cfo-reporting/compute_kpis.py` | 82 | 18 | 78.0% |
| `cfo-comptabilite/prepare_fec_export.py` | 88 | 21 | 76.1% |
| `cfo-tresorerie/forecast_13w.py` | 82 | 21 | 74.4% |

### Couverture faible (< 70 %), a ameliorer en priorite

| Script | Stmts | Miss | Cover | Branches non couvertes typiques |
|--------|-------|------|-------|---------------------------------|
| `cfo-init/portfolio/init_cabinet.py` | 83 | 25 | 69.9% | Erreurs template chargement |
| `cfo-init/portfolio/list_clients.py` | 66 | 23 | 65.2% | Mode detailed |
| `cfo-reporting/generate_dashboard.py` | 69 | 24 | 65.2% | Chrome headless PDF gen |
| `cfo-init/portfolio/remove_client.py` | 60 | 21 | 65.0% | Mode --delete |
| `cfo-init/portfolio/schedule_all.py` | 92 | 37 | 59.8% | Iteration portfolio entier |
| `cfo-init/portfolio/encaissements_aging.py` | 117 | 48 | 59.0% | Rendu HTML + main |
| `cfo-init/portfolio/forfait_tracker.py` | 97 | 41 | 57.7% | Rendu HTML + main |
| `cfo-init/fetch_pappers.py` | 71 | 30 | 57.7% | Mode --mode api (pas de cle API en CI) |
| `cfo-init/portfolio/portfolio_dashboard.py` | 156 | 68 | 56.4% | Blocs HTML complexes |
| `cfo-comptabilite/validate_close_checklist.py` | 78 | 34 | 56.4% | Checks avances (cut-off, provisions) |
| `cfo-comptabilite/generate_closing_journal.py` | 101 | 48 | 52.5% | Mode annuel, ajustements |

## Lecture

Les scripts avec les plus gros trous sont ceux qui ont :

1. **De la generation HTML complexe** (dashboards portfolio, aging, forfait) : les branches de rendu sont peu testees car les tests fonctionnels valident l'existence du fichier HTML, pas chaque bloc de template.
2. **Des modes avances** (fetch en mode api, closing annuel) : non couverts car ils necessitent des cles API ou des fixtures plus riches.
3. **Du main() avec option --output vs stdout** : une seule branche testee sur les deux.

## Cible v0.4

- Atteindre 85 % global (actuellement 77.5 %) en ajoutant des fixtures :
  - Pour les dashboards portfolio : tester le mode --detailed et les alertes vides
  - Pour les closures : tester le mode annuel avec fixtures bilan + compte de resultat
  - Pour les fetches : ajouter un test avec mock API (sans vraie cle)
- Aucun script en dessous de 70 %.
- Couverture des 5 scripts durcis en v0.2.0 (bfr, extract_variances, tva_checker, risk_mapping, moriarty_link) >= 95 %. Trois y sont deja (87 %, 93 %, 87 %), les deux autres oscillent (86 %, 100 %).

## Reproduction

```bash
pip install coverage
python3 evals/run_coverage.py                # Rapport texte
python3 evals/run_coverage.py --html         # + HTML dans htmlcov/
python3 evals/run_coverage.py --threshold 70 # Fail si coverage < 70 %
```

Le runner `evals/run_coverage.py` est stdlib-compatible pour son import mais necessite `coverage` installe pour fonctionner. Il skip proprement sinon.
