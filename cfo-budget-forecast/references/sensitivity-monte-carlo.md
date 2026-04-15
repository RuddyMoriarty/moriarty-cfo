# Analyse de sensibilité + Monte Carlo

Techniques pour évaluer l'incertitude d'une projection financière.

## Analyse de sensibilité (simple)

Tester l'impact d'une variation de ±10% (ou ±20%) **sur chaque variable clé** pour identifier celles qui ont le plus d'impact sur le résultat.

### Méthode

Pour chaque variable (CA, marge, coûts salariaux, CAPEX, etc.) :
1. Baseline : résultat attendu
2. Variable −10% : nouveau résultat
3. Variable +10% : nouveau résultat
4. Impact = |nouveau résultat - baseline|

### Exemple

Business plan à 5 ans, EBITDA cible en Y5 = 2 M€. Tester :

| Variable | Baseline | -10% | +10% | Impact ± 10% |
|----------|----------|------|------|--------------|
| Croissance CA | 30% | 20% | 40% | ±1.2 M€ EBITDA |
| Taux de marge brute | 65% | 55% | 75% | ±0.5 M€ |
| Coûts salariaux | 1.5M | 1.35M | 1.65M | ±0.15M |
| CAC | 2k€ | 2.2k€ | 1.8k€ | ±0.08M |

**Insight** : la croissance CA est la variable la plus sensible. 80% de l'incertitude du BP vient de là.

→ **Focus les efforts** sur la validation de l'hypothèse de croissance (études marché, signals tôts, pipeline).

## Monte Carlo (avancé)

Au lieu de tester ±10%, simuler **des milliers de tirages aléatoires** avec distributions probabilistes pour chaque variable.

### Méthode

1. Pour chaque variable clé, définir une **distribution** :
   - Normale (moyenne, écart-type)
   - Uniforme (min, max)
   - Triangulaire (min, mode, max)
   - Empirique (historique des 5 dernières années)

2. Tirer **1 000 à 10 000 itérations** :
   - Chaque itération = 1 tirage aléatoire de chaque variable
   - Calculer le résultat (EBITDA, cash...)
   - Stocker le résultat

3. Analyser la **distribution des résultats** :
   - Moyenne
   - Médiane
   - Intervalle de confiance 90% (P5 et P95)
   - Probabilité de résultat négatif

### Exemple : P(EBITDA 2M€ en Y5)

Simulation 10 000 itérations :
- 67% des itérations → EBITDA Y5 entre 1.5M et 2.5M
- 90% des itérations → EBITDA Y5 entre 0.8M et 3.2M
- **12% des itérations → EBITDA Y5 < 1M** (risque downside significatif)

### Quand faire un Monte Carlo

- Décision très structurante (levée de fonds, acquisition, gros CAPEX)
- Données fiables sur les distributions (historique suffisant)
- Management qui veut comprendre l'incertitude (investisseurs sophistiqués)

### Quand NE PAS faire un Monte Carlo

- PME simple avec peu de données
- Décision tactique routinière
- Faux sentiment de précision ("on voit que P(xxx) = 12.3%" alors que les inputs sont estimatifs à ±20%)

## Outils

- **Excel** : `=NORM.INV(RAND(), mean, std)` + table de résultats
- **Python** : numpy + pandas pour simulation + analyse statistique
- **Spécialisés** : @Risk (add-in Excel), Crystal Ball

## Implémentation

Le script `scripts/budget_builder.py` (en v0.2) pourra inclure une option `--monte-carlo N` pour simuler N itérations et sortir P5/P50/P95 du résultat.

Pour v0.1, sensibilité ±10% manuelle suffit pour la plupart des décisions PME.

## Limites

- **Garbage in, garbage out** : si les distributions d'entrée sont arbitraires, les résultats aussi
- **Corrélations ignorées** par défaut (si CA baisse, les coûts variables baissent aussi, corrélation à modéliser)
- **Fausse précision** : Monte Carlo donne des décimales, mais l'incertitude vient des distributions elles-mêmes
