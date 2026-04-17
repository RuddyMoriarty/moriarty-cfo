# Baseline Comparison, moriarty-cfo

Mesure empirique du gain que les skills du bundle apportent vs Claude brut.
Inspiree du guide Anthropic Skills Ch. 3 §3 (Baseline Comparison).

## Methodologie

Pour chaque scenario defini dans `baseline-scenarios.json`, on lance exactement
la meme tache dans deux conditions :

1. **Sans skill** : Claude 3.5 Sonnet avec un system prompt minimal ("Tu es un
   CFO virtuel francophone"). Claude doit tout inventer ou rechercher.
2. **Avec skill** : meme prompt, plus le contenu du `SKILL.md` concerne et de
   ses `references/` injectes dans le system prompt.

On mesure :

- **tool_calls** : nombre d'appels d'outils
- **input_tokens, output_tokens, cache_read_tokens** : consommation tokens
- **steps_done / steps_total** : couverture de la `reference_checklist` du
  scenario (heuristique : ≥ 2 mots-cles du step presents dans la reponse)
- **duration_seconds** : temps wall-clock par run

## Scenarios (v0.2.2)

5 scenarios realistes, diversite difficulty easy/medium/hard sur 5 skills :

| ID | Skill | Difficulty | Budget sans/avec (s) |
|----|-------|------------|----------------------|
| baseline-cfo-init-onboarding | cfo-init | easy | 180 / 60 |
| baseline-cfo-tresorerie-bfr | cfo-tresorerie | medium | 300 / 90 |
| baseline-cfo-fiscalite-cir | cfo-fiscalite | hard | 420 / 120 |
| baseline-cfo-csrd-scope | cfo-csrd-esg | medium | 360 / 90 |
| baseline-cfo-financement-diagnostic | cfo-financement-croissance | hard | 480 / 120 |

## Cibles

- **Tool calls** : -50 % minimum
- **Tokens total** : -40 % minimum
- **Steps couverts** : +40 % minimum (passer de ~50 % de la checklist a ≥ 90 %)

## Comment executer

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# Tous les scenarios (~ 0,50 € sur Claude 3.5 Sonnet)
python3 evals/measure_baseline.py

# Un scenario specifique
python3 evals/measure_baseline.py --scenario baseline-cfo-init-onboarding

# Dry-run (sans appel API, pour CI)
python3 evals/measure_baseline.py --dry-run
```

Le script ecrit le resultat dans `evals/baseline-results.json` avec un
timestamp et les deltas calcules. Commit ce fichier avec un message expliquant
le contexte (quelle version du bundle, quel modele, quelle date).

## Resultats

> **TODO** : mesurer avec une cle API et commiter `evals/baseline-results.json`.
> Les scenarios sont prets et valides. L'execution necessite `ANTHROPIC_API_KEY`
> et coute environ 0,50 € par session complete.

Les resultats seront presentes sous cette forme une fois mesures :

| Scenario | Tokens sans | Tokens avec | Reduction tokens | Steps sans | Steps avec | Coverage delta |
|----------|-------------|-------------|------------------|------------|------------|----------------|
| onboarding | TBD | TBD | TBD | TBD | TBD | TBD |
| bfr | TBD | TBD | TBD | TBD | TBD | TBD |
| cir | TBD | TBD | TBD | TBD | TBD | TBD |
| csrd | TBD | TBD | TBD | TBD | TBD | TBD |
| diagnostic | TBD | TBD | TBD | TBD | TBD | TBD |

## CI

`evals/_helpers/check_baseline_scenarios.py` valide la structure des scenarios
sans appeler l'API (test statique present dans `functional-tests.json`). La
mesure reelle reste manuelle pour maitriser le cout et ne pas dependre d'une
cle API en CI publique.

## Notes

- Le modele teste est `claude-3-5-sonnet-20241022` (ajuster dans
  `measure_baseline.py` si besoin d'un autre).
- L'heuristique `count_steps_covered` est volontairement simple (≥ 2 mots-cles
  du step dans la reponse) : elle peut sous-estimer la couverture quand Claude
  paraphrase, mais fonctionne bien comme mesure relative (biais constant sur
  les deux conditions).
- Pour un gold standard, un juge LLM (GPT-4 ou Claude Opus) pourrait etre
  utilise a la place de l'heuristique, au prix de 3x plus de tokens.
