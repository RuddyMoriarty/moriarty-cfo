---
name: cfo-budget-forecast
description: |
  Skill de budget et planification prospective. Budget annuel top-down + bottom-up, rolling forecasts trimestriels, business plans 3-5 ans investor-ready, scénarios optimiste/réaliste/pessimiste, CAPEX avec ROI/IRR/NPV/payback, atterrissages (MAT) mensuels, sensitivity analysis et Monte Carlo. Identifie les goulots d'étranglement dans la planification.
  Triggers: construire budget annuel construis, budget révisé prévisionnel, forecast rolling trimestriel, plan stratégique 3 ans 5 ans, business plan investor-ready, scénarios optimiste réaliste pessimiste, atterrissage atterrissages mensuel estimé landing estimate, CAPEX planning arbitrage, investissement usine, ROI IRR NPV payback, sensitivity Monte Carlo, goulots étranglement budgétaire, planification prospective forward-looking, financial model, financial planning, reforecast ajustement budgétaire
metadata:
  last_updated: 2026-04-14
  version: 0.1.0
  audience: [ec, pme]
  tier: 2
  bundle: moriarty-cfo
includes:
  - references/**
  - scripts/**
  - templates/**
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
license: MIT
---

# cfo-budget-forecast, Budget & planification

Sixième skill du bundle. Tier 2.

## Prérequis

- `private/company.json` (profil société via cfo-init)
- Historique réel N-1/N-2 (balance + KPIs via cfo-reporting)

## Workflows principaux

### 1. Budget annuel

Workflow détaillé : [references/budget-annuel.md](references/budget-annuel.md).

**Méthodologie** :
- **Top-down** : Le CEO/board fixe des objectifs de CA, marge, EBITDA
- **Bottom-up** : Les équipes remontent leurs besoins détaillés par poste
- **Arbitrage** : le CFO fait le lien, défend les priorités, fait les tradeoffs

**Étapes** :
1. Cadrage stratégique (Q4 année N-1)
2. Projection CA par segment / produit / client
3. Projection OPEX par centre de coût
4. Projection CAPEX (investissements validés)
5. Projection RH (recrutements, augmentations, départs)
6. Consolidation P&L + bilan + cash flow prévisionnel
7. Validation CODIR + board
8. Communication aux équipes

### 2. Rolling forecasts trimestriels

Référence : [references/rolling-forecast.md](references/rolling-forecast.md).

À chaque fin de trimestre, mettre à jour la projection annuelle :
- Intégrer le réel T1 (T2, T3) + hypothèses révisées pour les trimestres suivants
- Maintenir un horizon glissant de 4-8 trimestres
- Bonne pratique : rolling forecast = vision probable, budget = engagement

### 3. Plan stratégique 3-5 ans

Référence : [references/business-plan-3-5-ans.md](references/business-plan-3-5-ans.md).

**Usage** :
- Investor-ready (levée de fonds)
- Board review (décision stratégique)
- Vendeur side (exit / cession)

**Contenu** :
- Thèse d'investissement (pourquoi on investit maintenant)
- Marché + competitive landscape
- Trajectoire CA / marge / EBITDA sur 5 ans
- Trajectoire effectif + coûts
- CAPEX cumulés + trajectoire cash
- Analyse de sensibilité (up/down 20%)
- Besoins de financement pour atteindre les jalons

### 4. Scénarios (optimiste / réaliste / pessimiste)

Référence : [references/scenarios.md](references/scenarios.md).

Probabilité pondérée : 20% / 60% / 20% (ou 30/50/20 en contexte incertain).

### 5. Atterrissage mensuel

Référence : [references/atterrissage.md](references/atterrissage.md).

Mise à jour mensuelle de la projection de fin d'année :
```
Atterrissage annuel = Réel YTD + Projection restant d'année
```

### 6. CAPEX planning + ROI analysis

Référence : [references/capex-roi.md](references/capex-roi.md).

Calculs :
- **Payback** = Investissement / Cash flow annuel additionnel
- **NPV** = Somme actualisée des cash flows - Investissement initial
- **IRR** = Taux de rentabilité interne (le taux qui rend NPV = 0)
- **ROI** = Gain annuel / Investissement

Critères décision :
- Payback < 3 ans : OK
- NPV > 0 à taux WACC : OK
- IRR > WACC + 5 pts : excellent

### 7. Sensitivity analysis + Monte Carlo (avancé)

Référence : [references/sensitivity-monte-carlo.md](references/sensitivity-monte-carlo.md).

- Tester l'impact d'une variation de ±10% sur chaque variable clé
- Identifier les **2-3 variables qui expliquent 80% de la variance** du résultat
- Monte Carlo : simuler 1000+ tirages aléatoires → distribution probabiliste

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/budget_builder.py` | Génère squelette budget annuel à partir de N-1 + hypothèses croissance |
| `scripts/rolling_forecast.py` | Mise à jour rolling forecast avec réel YTD |
| `scripts/capex_analyzer.py` | Calcul NPV / IRR / payback d'un projet CAPEX |

## Templates

| Template | Usage |
|----------|-------|
| `templates/budget-annuel.xlsx.md` | Template budget (documenté en markdown, à exporter vers Excel) |
| `templates/business-plan-3-5-ans.md` | Template BP investor-ready |
| `templates/capex-fiche.md` | Fiche individuelle projet CAPEX |

## Références

| Référence | Sujet |
|-----------|-------|
| [references/budget-annuel.md](references/budget-annuel.md) | Méthodologie budget annuel |
| [references/rolling-forecast.md](references/rolling-forecast.md) | Rolling forecasts trimestriels |
| [references/business-plan-3-5-ans.md](references/business-plan-3-5-ans.md) | Plan stratégique |
| [references/scenarios.md](references/scenarios.md) | Scénarios probabilisés |
| [references/atterrissage.md](references/atterrissage.md) | Atterrissage mensuel |
| [references/capex-roi.md](references/capex-roi.md) | CAPEX + ROI/NPV/IRR |
| [references/sensitivity-monte-carlo.md](references/sensitivity-monte-carlo.md) | Analyse de sensibilité |

## Achievements

- `budget-builder` (+50) : 1er budget annuel construit
- `forecaster` (+35) : 1er rolling forecast trimestriel

## Adaptation par audience

**Mode EC** : mission contractuelle "construction budget" ou "business plan financement". Travail avec le dirigeant / CODIR client.

**Mode PME** : outil de pilotage interne. Insister sur la **discipline mensuelle** (atterrissage régulier, ajustements).

## Avertissement

Les projections financières sont des **hypothèses** explicitées. Leur fiabilité dépend des inputs. Pour utilisation externe (banque, investisseur, acheteur), validation EC + CAC recommandée.
