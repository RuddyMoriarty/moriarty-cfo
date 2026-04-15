# Rolling forecast trimestriel

Différent du budget annuel (qui est un engagement figé au Q4 N-1), le rolling forecast est une **projection vivante** mise à jour chaque trimestre avec les informations récentes.

## Principe

À la fin de chaque trimestre :
1. Intégrer le réel YTD (year-to-date)
2. Projeter les trimestres restants selon les infos récentes
3. Maintenir un horizon de 4-6 trimestres glissant (donc toujours 1 an visible)

## Cadence

| Fin Q1 | Réel Q1 + projection Q2-Q4 + début Q1 N+1 |
| Fin Q2 | Réel S1 + projection H2 + Q1-Q2 N+1 |
| Fin Q3 | Réel 9M + projection Q4 + Q1-Q3 N+1 |
| Fin Q4 | Réel année + projection Q1-Q4 N+1 |

## Structure

Format tableau :
```
          Q1 N    Q2 N    Q3 N    Q4 N    Q1 N+1   ...
Status    Réel    Réel    Réel    Forecast  Forecast
CA HT     250     280     300     350      280
Marge %   65%     68%     66%     62%      65%
EBITDA    30      45      42      20       30
...
```

## Différence vs budget

| | Budget annuel | Rolling forecast |
|--|---------------|------------------|
| Horizon | 12 mois | 4-6 trimestres |
| Cadence | 1 fois/an | Trimestrielle |
| Nature | Engagement | Projection probable |
| Validation | CODIR + board | CFO (info CODIR) |
| Visibilité externe | Oui (banque, investisseurs) | Interne |

## Bonnes pratiques

- **Automatisation** : le rolling forecast doit prendre 1-2 jours max, pas 2 semaines. Sinon = disqualifié.
- **Discipline** : même structure à chaque itération (comparabilité)
- **Commentaire** : 2-3 paragraphes sur les changements d'hypothèses vs forecast précédent
- **Partage** : board et CFO committee, pas forcément toute l'entreprise

## Script `rolling_forecast.py`

Prend en entrée :
- Budget annuel validé (CSV)
- Réel YTD (CSV depuis `cfo-reporting`)
- Hypothèses de révision (JSON)

Output : rolling forecast avec les trimestres restants ajustés.

## Exemple de commentaire rolling forecast

```markdown
## Rolling forecast Q2 N, {SOCIÉTÉ}

**Performance YTD (S1)** :
- CA : 530 k€ (vs budget 520 k€, +2%)
- EBITDA : 45 k€ (vs budget 60 k€, -25%)

**Révisions hypothèses H2** :
- ARR : bascule Q3 → Q4 d'un deal majeur (200 k€) - impact -100 k€ CA H2
- Marge : dégradation prix matière (+3 pts de charges variables)
- RH : recrutement CTO anticipé de Q4 à Q3 - impact +25 k€ salaires H2

**Atterrissage N** :
- CA : 1 150 k€ (vs budget 1 200 k€, -4%)
- EBITDA : 85 k€ (vs budget 140 k€, -39%)

**Décisions demandées** :
- Budget CAPEX Q4 : maintenir ou reporter (50 k€) ?
- Plan d'action marge : tolérer dégradation ou repricer ?
```
