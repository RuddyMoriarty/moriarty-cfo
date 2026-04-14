# Dashboard CFO exécutif

Document HTML responsive auto-généré quotidiennement ou hebdomadairement. 5-8 KPIs maximum pour maintenir la lisibilité.

## Règle des 5-8 KPIs

Au-delà de 8 KPIs, le dashboard devient illisible. Si plus de KPIs nécessaires : créer plusieurs dashboards (Commercial, Produit, Finance, RH…) plutôt que surcharger.

## KPI packs par secteur

Source : `data/kpi-catalog.json > kpi_packs_par_secteur`.

### SaaS / scale-up

1. **ARR** (Annual Recurring Revenue) — growth YoY
2. **MRR net new** (net new MRR mensuel)
3. **NRR** (Net Revenue Retention — upsell/expansion vs churn)
4. **CAC payback** (mois pour amortir le CAC)
5. **LTV/CAC** ratio
6. **Burn multiple** (burn / net new ARR)
7. **Runway** (mois)
8. **Cash**

### Services B2B

1. **CA HT** (mensuel / cumul YTD)
2. **TJM moyen** (revenu / jour facturé)
3. **Taux d'utilisation** (jours facturés / jours disponibles)
4. **DSO** (creances clients)
5. **Marge brute %**
6. **EBITDA**
7. **Pipeline pondéré**
8. **Effectif actif**

### Industrie / fabrication

1. **CA HT**
2. **Production** (unités)
3. **Taux de rendement synthétique (TRS)**
4. **Marge brute**
5. **DIO** (rotation stocks)
6. **CAPEX YTD**
7. **Dette nette / EBITDA**
8. **Effectif**

### Commerce / négoce

1. **CA HT**
2. **Panier moyen**
3. **Same-store growth**
4. **Marge brute %**
5. **Rotation stocks**
6. **DSO + DPO**
7. **BFR % du CA**
8. **Cash**

### Startup early-stage

1. **MRR**
2. **Net new MRR**
3. **Burn mensuel**
4. **Cash**
5. **Runway**
6. **Nombre de clients payants**
7. **NPS ou CSAT**

## Couleurs et zones

| Zone | Critère | Couleur |
|------|---------|---------|
| 🟢 Excellent | > cible +10% | Vert foncé |
| 🟢 Dans la cible | cible ±10% | Vert clair |
| 🟠 Attention | cible -10% à -25% | Orange |
| 🔴 Critique | < cible -25% | Rouge |

## Fréquence

- **Startups** : hebdo (lundi matin)
- **PME** : mensuel (après J+5)
- **ETI** : mensuel + trimestriel agrégé

## Format

HTML responsive (mobile + desktop + print). Généré via `scripts/generate_dashboard.py` qui utilise :
- Chrome headless pour l'export PDF
- Template Jinja2 avec data injection depuis JSON

## Structure HTML

```
┌─────────────────────────────────────┐
│ LOGO    DASHBOARD CFO    PÉRIODE    │
├─────────────────────────────────────┤
│                                     │
│  [KPI 1]   [KPI 2]   [KPI 3]   ...  │
│  +VALEUR  +DELTA    +COULEUR        │
│                                     │
├─────────────────────────────────────┤
│  GRAPH TREND 12 MOIS (KPI PRINCIPAL)│
├─────────────────────────────────────┤
│  TOP 3 ALERTES  |  TOP 3 ACTIONS    │
├─────────────────────────────────────┤
│  FOOTER MORIARTY                    │
└─────────────────────────────────────┘
```

## Automatisation maximale

Tout ce qui peut être calculé doit l'être :
- KPIs depuis balance + extracts opérationnels
- Trends depuis historique stocké
- Couleurs automatiques selon seuils
- Alertes auto si seuil franchi

Ce qui reste manuel :
- Choix des "actions prioritaires" (jugement humain)
- Commentaire de contexte (optionnel)

## Template

`templates/dashboard-cfo.html` — HTML Jinja2 responsive.

## Exemple généré

Voir screenshots dans le README du repo `moriarty-cfo` (à ajouter en v0.1 post-release).
