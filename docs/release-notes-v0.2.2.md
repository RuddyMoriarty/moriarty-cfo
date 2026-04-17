# Release v0.2.2 — Roadmap v0.2 finalisee

Cette release consolide 9 versions successives (v0.1.4 a v0.2.2) qui ont amene le bundle a un plateau de qualite industrielle.

## Points forts

- **Mode EC Portfolio complet** : un cabinet d'expertise comptable peut initialiser son portfolio, ajouter et archiver ses clients, programmer les routines en batch, et generer un dashboard agrege des echeances.
- **10 skills avec 3 tests fonctionnels reels chacun** : tous les 27 scripts Python sont exerces par au moins un test avec fixture et assertions, zero smoke test restant.
- **Robustesse validee** : 14 scenarios d'erreur en CI, 5 scripts durcis pour rejeter proprement les inputs invalides au lieu de crasher.
- **Detection de regression** : 8 snapshots figes avec tolerance 0,5 % sur les floats pour detecter toute derive silencieuse entre deux releases.
- **Framework baseline pret** : 5 scenarios CFO avec checklists de reference pour mesurer empiriquement le gain vs Claude brut (execution manuelle avec cle API).

## Metriques

| | v0.1.3 | v0.2.2 | Delta |
|---|---|---|---|
| Tests globaux | 228 | 349 | +53 % |
| Tests fonctionnels | 13 | 73 | +462 % |
| Scripts couverts | 0 (smoke only) | 27/27 | +100 % |
| Scenarios erreur | 0 | 14 | nouveau |
| Snapshots regression | 0 | 8 | nouveau |
| Lint ruff | 0 warning | 0 warning | stable |

## Changelog par version

### v0.2.2 — Module B baseline comparison framework

5 scenarios CFO (init, tresorerie, fiscalite, csrd, financement) avec user_prompt, expected_skill, checklist de reference. Script `evals/measure_baseline.py` skip proprement sans cle API. Test CI en dry-run pour valider la structure. Execution reelle coute ~0,50 € par session Claude 3.5 Sonnet.

### v0.2.1 — Module C snapshot regression

8 snapshots deterministes figes dans `evals/_snapshots/`. Comparaison deep recursive avec tolerance 0,5 % sur les floats. Script `evals/_helpers/snapshot_compare.py` avec modes `--check` et `--update`.

### v0.2.0 — Module A scenarios d'erreur + 5 scripts durcis

14 scenarios qui valident qu'un input malforme echoue proprement (exit non-zero + message stderr clair) sans Traceback Python. Scripts renforces : bfr_calculator (CA=0), extract_variances (colonnes CSV), tva_checker (fichiers absents), risk_mapping_generator (colonnes requises), moriarty_link (SIREN 9 chiffres).

### v0.1.9 — Couverture fonctionnelle 27/27

Le 3e script de chaque skill est teste : prepare_fec_export, forecast_13w, generate_dashboard, profitability_analyzer, rolling_forecast, tva_checker, risk_mapping_generator, valuation_calculator, double_materiality_assessor.

### v0.1.8 — 2 tests fonctionnels reels par skill

Passe de 1 smoke a 2+ tests avec fixtures et assertions sur les outputs JSON/CSV/HTML.

### v0.1.7 — Couverture fonctionnelle 10 skills smoke

Le helper `smoke_skill_scripts.py` valide que les 3 scripts de chaque skill compilent et repondent a `--help`.

### v0.1.6 — init_pme.py symetrique

`cfo-init/scripts/init_pme.py` cree en parallele de `init_cabinet.py`. Les deux modes (PME dirigeant et collaborateur cabinet EC) ont desormais un point d'entree CLI explicite.

### v0.1.5 — Modules metier EC

4 nouveaux modules dans `cfo-init/scripts/portfolio/` : check_dossier, draft_relance, generate_lettre_mission (3 templates NP 2300 / 2400 / social-paie), encaissements_aging (LME buckets), forfait_tracker.

### v0.1.4 — Mode EC Portfolio

6 scripts portfolio : init_cabinet, add_client, list_clients, remove_client (archive/delete), schedule_all, portfolio_dashboard. Template HTML A4 landscape avec charte Moriarty, alertes rouge <7j / orange 7-14j / jaune 15-30j.

## Breaking changes

Aucun. Toutes les API de scripts et tous les formats de fichiers sont retrocompatibles depuis v0.1.3.

## Prochaine etape

v0.3 se concentre sur l'usage reel : integration Pappers/INSEE live pour `fetch_siren`, guide de test client (POC PME et POC cabinet EC), et potentiellement mesure baseline reelle avec cle API pour valider empiriquement les cibles -40 % tokens / -50 % tool_calls.
