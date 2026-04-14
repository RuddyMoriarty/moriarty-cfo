# Scénarios probabilisés (optimiste / réaliste / pessimiste)

## Principe

Ne JAMAIS présenter un seul scénario. Toujours 3 cas pour :
- Montrer la plage d'issues possibles
- Forcer le dirigeant à réfléchir aux risques downside
- Convaincre les investisseurs par la rigueur

## Probabilités standards

Contexte stable : **20% / 60% / 20%**
Contexte incertain : **30% / 50% / 20%**
Contexte très incertain : **40% / 40% / 20%**

La probabilité pondérée donne la **valeur attendue** :
```
Valeur attendue = Opt × 0.20 + Réel × 0.60 + Pess × 0.20
```

## Hypothèses typiques par scénario

### Scénario réaliste (central)

- Croissance CA conforme au budget
- Marge stable
- Exécution sur la roadmap produit comme prévu
- Environnement macro neutre

### Scénario optimiste (upside)

- Croissance CA +15% vs réaliste
- Marge améliorée (+2 pts)
- Gros contrat signé qui n'était pas au budget
- Environnement macro favorable
- Acquisition opportunité sur concurrent en difficulté

### Scénario pessimiste (downside)

- Croissance CA -10% vs réaliste
- Marge dégradée (-3 pts) par tension coûts
- Churn d'un gros client
- Retard produit de 3-6 mois
- Récession macroéconomique impactant les budgets clients

## Mode calcul

Chaque variable a 3 valeurs (opt/réel/pess). Les scénarios cohérents :
- Scénario optimiste = tous les upsides alignés
- Scénario pessimiste = tous les downsides alignés (prudent mais réaliste)
- Scénario réaliste = valeurs médianes pondérées

Ne pas mélanger des upsides avec des downsides sur le même scénario (perd la cohérence).

## Présentation

Tableau synthétique 3 colonnes :

```
                       Optimiste  Réaliste  Pessimiste   Pondéré (20/60/20)
CA 12M                 1 500      1 250     1 000        1 250
EBITDA 12M             200        100       -50          85
Cash fin 12M           500        300       -150         275
Runway (startup)       > 18 mois  14 mois   8 mois       —
```

## Utiliser pour décider

### Go / No-go d'une décision

Si le pessimiste fait basculer en perte catastrophique → **trop risqué**.
Si l'optimiste apporte peu → **rendement insuffisant**.
Si le réaliste est déjà très bon → **décision facile**.

### Gérer la confiance

Plus l'écart entre opt et pess est faible → plus forte visibilité, plus faible risque.
Plus l'écart est large → plus d'incertitude, prudence requise.

## Implémentation

Le script `scripts/budget_builder.py` génère automatiquement les 3 scénarios à partir du budget réaliste en appliquant des coefficients (±15%, ±3pts, etc.).
