# Atterrissage annuel (landing)

Projection de fin d'année mise à jour chaque mois.

## Formule

```
Atterrissage = Réel YTD + Projection du reste d'année
```

## Méthode simple (à partir du mois 3-4)

Tendance linéaire : annualiser le YTD
```
Atterrissage = Réel YTD × (12 / mois écoulés)
```

⚠️ Piège : ignore la saisonnalité. À utiliser seulement si activité linéaire.

## Méthode affinée (mois par mois)

```
Atterrissage = Réel YTD + Σ forecast (mois M+1 à décembre)
```

Le forecast des mois restants est :
- Budget initial ajusté par la trajectoire du YTD
- Événements connus non encore budgetés (signature nouveau contrat, départ salarié)
- Hypothèses révisées (dégradation matière, retard produit)

## Présentation mensuelle

```markdown
# Atterrissage {MOIS} {ANNEE}

## YTD à fin {MOIS}
- CA : 530 k€ (vs budget YTD 520 k€, +2%)
- EBITDA : 45 k€ (vs budget YTD 60 k€, -25%)

## Atterrissage N
- CA : 1 150 k€ (budget 1 200, -4%)
- EBITDA : 85 k€ (budget 140, -39%)

## Hypothèses révisées
- {Hypothèse 1}
- {Hypothèse 2}

## Actions en cours pour combler l'écart
- {Action 1 — impact}
- {Action 2 — impact}
```

## Seuils d'alerte

| Atterrissage vs Budget | Niveau | Action |
|------------------------|--------|--------|
| ± 2% | 🟢 OK | Continuer |
| -2% à -5% | 🟡 Vigilance | Plan d'action tactique |
| -5% à -10% | 🟠 Alerte | Révision budget à envisager |
| < -10% | 🔴 Budget révisé | Communication board, révision formelle |

## Intégration

- Produit chaque mois par le script `scripts/rolling_forecast.py` après le reporting mensuel
- Inclus dans le pack mensuel CFO (`cfo-reporting`)
- Présenté au CODIR mensuel
- Si seuil 🟠 ou 🔴 : escalade au board
