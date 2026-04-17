# Coverage snapshot, v0.3.4

Snapshot du rapport `coverage.py` apres le coverage booster. Le cycle precedent (v0.3.2) mesurait 77.5 %. En v0.3.4, **82.7 %** sur 3638 lignes de code executable, 625 lignes non couvertes.

## Progression depuis v0.3.2

| Metrique | v0.3.2 | v0.3.4 | Delta |
|---|---|---|---|
| Coverage globale | 77.5 % | **82.7 %** | **+5.2 pts** |
| Scripts < 70 % | 11 | **5** | -6 (-55 %) |
| Lignes non couvertes | 813 | **625** | -188 |

## Resultat global

**82.7 %** de couverture sur 3638 lignes, 625 lignes non couvertes.

## Gains majeurs v0.3.4

Refactor `--private-dir` sur 6 scripts portfolio + helper dedie `fct_lowcov_scripts.py` (13 tests) ont permis :

| Script | v0.3.2 | v0.3.4 | Gain |
|--------|--------|--------|------|
| `cfo-init/portfolio/remove_client.py` | 65.0 % | **92.1 %** | +27 pts |
| `cfo-init/portfolio/list_clients.py` | 65.2 % | **88.4 %** | +23 pts |
| `cfo-init/portfolio/encaissements_aging.py` | 59.0 % | **89.8 %** | +31 pts |
| `cfo-init/portfolio/forfait_tracker.py` | 57.7 % | **81.0 %** | +23 pts |
| `cfo-comptabilite/validate_close_checklist.py` | 56.4 % | **88.5 %** | +32 pts |
| `cfo-comptabilite/generate_closing_journal.py` | 52.5 % | **71.3 %** | +19 pts |
| `cfo-init/portfolio/portfolio_dashboard.py` | 56.4 % | **72.7 %** | +16 pts |
| `cfo-init/portfolio/init_cabinet.py` | 69.9 % | **73.3 %** | +3 pts |

## Scripts encore sous 70 %

5 scripts restent sous le seuil, tous avec des branches qui necessitent un mock reseau ou Chrome headless :

| Script | Cover | Branche non couverte typique |
|--------|-------|------------------------------|
| `cfo-init/fetch_sirene.py` | 62.1 % | OAuth INSEE + fetch_via_annuaire reseau reel |
| `cfo-init/init_progress.py` | 61.2 % | `--unlock` et `--incr` qui modifient `private/cfo-progress.json` (partage avec e2e) |
| `cfo-init/fetch_pappers.py` | 64.8 % | `fetch_via_api` necessite `PAPPERS_API_KEY` |
| `cfo-init/portfolio/schedule_all.py` | 65.3 % | Execution non dry-run (appelle compute_entity_routines + schedule_routines) |
| `cfo-reporting/generate_dashboard.py` | 68.1 % | `export_pdf` via Chrome headless |

## Scripts a 100 % ou presque

| Script | Cover |
|--------|-------|
| `cfo-financement-croissance/moriarty_link.py` | **100.0 %** |
| `cfo-tresorerie/forecast_12m.py` | 98.4 % |
| `cfo-controle-gestion/pricing_simulator.py` | 97.4 % |
| `cfo-csrd-esg/scope_emissions_estimator.py` | 96.6 % |
| `cfo-financement-croissance/valuation_calculator.py` | 96.3 % |
| `cfo-init/compute_calendar.py` | 94.1 % |
| `cfo-reporting/extract_variances.py` | 93.5 % |
| `cfo-controle-gestion/profitability_analyzer.py` | 93.2 % |
| `cfo-controle-gestion/variance_analyzer.py` | 93.0 % |
| `cfo-risques-conformite/internal_control_checklist.py` | 92.9 % |
| `cfo-financement-croissance/diagnostic_financement.py` | 92.5 % |
| `cfo-risques-conformite/veille_scheduler.py` | 92.3 % |
| `cfo-init/portfolio/remove_client.py` | 92.1 % |

## Cible v0.4

- Atteindre 85 % global (actuellement 82.7 %), soit fermer 3 pts.
- Les 5 scripts < 70 % restants : necessitent des mocks reseau (urllib.request patchs) + Chrome headless (skip ou mock). Non critique, les branches sont `except` ou modes avances rarement utilises.

## Infrastructure

Refactor majeur v0.3.4 : 6 scripts portfolio acceptent desormais `--private-dir <path>` pour isoler les fixtures de test du vrai repertoire `private/`. Pattern `global PRIVATE` + override par argparse. Testabilite et portabilite ameliorees sans changer l'API publique (default reste `<repo>/private`).

## Reproduction

```bash
pip install coverage
python3 evals/run_coverage.py                # Rapport texte, ~20 secondes
python3 evals/run_coverage.py --html         # + HTML dans htmlcov/
python3 evals/run_coverage.py --threshold 80 # Fail si coverage < 80 %
```
