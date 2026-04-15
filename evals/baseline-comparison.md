# Baseline Comparison, moriarty-cfo

Mesure de la performance des skills vs baseline (sans skill activé).

## Méthodologie

Pour chaque skill, on lance la même tâche dans deux conditions :
1. **Sans skill** : Claude résout la tâche from scratch
2. **Avec skill** : Claude utilise le skill du bundle

On mesure :
- **Tool calls** : nombre d'appels d'outils (Read, WebFetch, Bash, etc.)
- **Tokens** : tokens consommés (entrée + sortie + cache)
- **Étapes oubliées** : nombre de sous-tâches manquantes vs checklist de référence
- **Durée** : temps wall-clock

Les baselines sont mesurées une fois par release majeure (v0.1.0, v0.2.0...).

## Résultats v0.1.0, TODO (à mesurer après implémentation complète)

> Cette section sera remplie après implémentation des 10 skills, en exécutant
> chaque test fonctionnel dans les deux conditions et en agrégeant les métriques
> via `aggregate_benchmark.py`.

### Template (à compléter)

| Skill | Tâche | Tool calls (sans/avec) | Tokens (sans/avec) | Étapes oubliées (sans/avec) | Delta |
|-------|-------|------------------------|--------------------|-----------------------------|-------|
| cfo-init | Onboarding société SIREN 552120222 | TBD | TBD | TBD | TBD |
| cfo-comptabilite | Clôture mensuelle simple | TBD | TBD | TBD | TBD |
| cfo-tresorerie | Forecast 13w | TBD | TBD | TBD | TBD |
| cfo-reporting | Reporting mensuel | TBD | TBD | TBD | TBD |
| cfo-controle-gestion | KPIs sectoriels SaaS | TBD | TBD | TBD | TBD |
| cfo-budget-forecast | Budget annuel | TBD | TBD | TBD | TBD |
| cfo-fiscalite | Estimation CIR | TBD | TBD | TBD | TBD |
| cfo-risques-conformite | Cartographie risques | TBD | TBD | TBD | TBD |
| cfo-financement-croissance | Diagnostic financement | TBD | TBD | TBD | TBD |
| cfo-csrd-esg | Détermination wave CSRD | TBD | TBD | TBD | TBD |

### Cibles (config.yaml)

- Tool calls : -50% minimum
- Tokens : -40% minimum
- Étapes oubliées : -80% minimum

## Comment reproduire

Voir `evals/run_evals.py` (mode --full requiert exécution interactive Claude Code,
non automatisable en CI pour cette mesure).

```bash
# Approche 1 : exécution manuelle dans Claude Code
# - Désactiver tous les skills cfo-*
# - Lancer la tâche depuis evals/functional-tests.json
# - Mesurer (Tasks panel → tokens consommés)
# - Réactiver les skills cfo-*
# - Relancer la même tâche
# - Comparer

# Approche 2 : automatisation via SDK Claude Agent (à venir v0.2)
python evals/baseline_runner.py --skill cfo-init --test cfo-init-fct-01
```
