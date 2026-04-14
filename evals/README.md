# Evals — moriarty-cfo

Suite d'évaluation programmatique des 10 skills du bundle, inspirée du framework de [paperasse/evals](https://github.com/romainsimon/paperasse/tree/main/evals).

## Trois niveaux de tests (PDF Anthropic Skills Guide Ch. 3)

### 1. Triggering tests
- **Goal** : vérifier que le bon skill se déclenche sur les bonnes phrases
- **Format** : `triggering-tests.json` — phrases ✅ doit déclencher / ❌ ne doit PAS déclencher
- **Cible** : ≥ 90% de match sur 10+ phrases par skill = 100+ tests

### 2. Functional tests
- **Goal** : vérifier que les sorties sont correctes (format, structure, contenu)
- **Format** : `functional-tests.json` — cas réel + assertions sur la sortie attendue
- **Cible** : ≥ 90% de pass sur 3+ cas par skill = 30+ tests

### 3. Performance comparison
- **Goal** : prouver que le skill améliore les résultats vs baseline (sans skill)
- **Format** : `baseline-comparison.md` — métriques avec/sans skill
- **Cible** : -50% tool calls, -50% tokens, -90% étapes oubliées

## Lancer les tests

```bash
# Subset rapide (~3 min, validation locale)
python evals/run_evals.py --quick

# Suite triggering uniquement
python evals/run_evals.py --triggering

# Suite functional uniquement
python evals/run_evals.py --functional

# Un seul skill
python evals/run_evals.py --skill cfo-init

# Suite complète (~30 min, à lancer avant release)
python evals/run_evals.py --full

# Validation structure (frontmatter, file structure, sources.json freshness)
python evals/run_evals.py --check-structure
```

## CI GitHub Actions

`.github/workflows/evals.yml` lance automatiquement :
- **Sur PR** : `--check-structure` + `--quick` (rapide)
- **Sur main** : `--full` + agrégation benchmark

## Conventions

- Toutes les phrases test sont en français (audience principale FR)
- Pas de SIREN client réel : utiliser `552120222` (Carrefour, public) ou SIREN inventés (000000001, etc.)
- Les baselines sont mesurées une fois par release (v0.1.0, v0.2.0, etc.)
- Les seuils peuvent évoluer avec l'expérience — modifier `config.yaml`

## Voir aussi

- [`config.yaml`](config.yaml) — configuration globale
- [`triggering-tests.json`](triggering-tests.json) — corpus tests déclenchement
- [`functional-tests.json`](functional-tests.json) — corpus tests fonctionnels
- [`baseline-comparison.md`](baseline-comparison.md) — résultats benchmarks
- [`run_evals.py`](run_evals.py) — script principal
- [`aggregate_benchmark.py`](aggregate_benchmark.py) — agrégation reports CI
