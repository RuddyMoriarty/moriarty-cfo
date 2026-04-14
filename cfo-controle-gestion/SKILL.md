---
name: cfo-controle-gestion
description: |
  Skill de contrôle de gestion et analyse de performance pour PME/TPE françaises et cabinets EC. Produit les analyses de rentabilité par produit/client/canal/activité, la comptabilité analytique (ABC, full cost, direct cost), les analyses de marges, le pricing optimization, le break-even, et la variance analysis avec investigation des écarts. Catalogue 32 KPIs CFO selon secteur. À utiliser pour toute question de rentabilité, performance, marges ou analyse financière détaillée.
  Triggers: contrôle de gestion, KPIs, performance, rentabilité, rentabilité produit, rentabilité client, marge brute, marge contributive, comptabilité analytique, ABC, allocation coûts, centres de coûts, variance analysis, pricing, break-even, seuil rentabilité, ROCE, ROE, analyse financière, benchmark sectoriel, performance analysis, management control, cost accounting
metadata:
  last_updated: 2026-04-14
  version: 0.1.0
  author: Moriarty
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

# cfo-controle-gestion — Performance & rentabilité

Cinquième skill du bundle. Tier 2 — analyses fines de performance et rentabilité.

Sujet n°4 dans le corpus Phase 0.1 (47 occurrences "KPI dashboards" + 41 "rentabilité par produit/client") — c'est un **must-have PME+**.

## Prérequis

- `private/company.json` (profil société via cfo-init)
- Balance comptable (via cfo-comptabilite)
- Données opérationnelles (ventes détaillées, production, achats ventilés)

## Workflows principaux

### 1. Catalogue 32 KPIs + benchmarks

Source : [`data/kpi-catalog.json`](../data/kpi-catalog.json).

**7 catégories** :
- Activité (CA, growth YoY, production)
- Rentabilité (Marge brute, VA, EBE, EBITDA, EBIT, RN, ROCE, ROE)
- Structure financière (FR, Ratio autonomie, Endettement, CAF)
- Trésorerie / BFR (DSO, DPO, DIO, CCC)
- Performance opérationnelle (Cash burn, Runway — mode startup)
- RH / Capital humain (Coût personnel/CA, CA/salarié, VA/salarié)
- Investissement CAPEX (Intensité capitalistique, Taux investissement, Vétusté)

**KPI packs sectoriels** auto-sélectionnés selon `company.secteur.module_sectoriel`.

Renvoi : [references/kpi-catalog-detail.md](references/kpi-catalog-detail.md).

### 2. Analyse de rentabilité produit / client

Workflow détaillé : [references/rentabilite-analyse.md](references/rentabilite-analyse.md).

**Méthodes** :
- **Top-down** : P&L décomposé par segment produit ou client
- **Bottom-up** : allocation des coûts indirects à chaque segment (ABC)
- **Matrice** : combiner dimensions produit × client × canal

**Outputs** :
- Top 10 produits / clients rentables
- Pareto 20/80 (20% des clients = 80% de la marge ?)
- Contribution marginale par segment
- Clients / produits en perte (à traiter : repricer, réduire coûts, abandonner)

### 3. Comptabilité analytique (ABC / Full cost / Direct cost)

Référence : [references/comptabilite-analytique.md](references/comptabilite-analytique.md).

**Méthodes** :
| Méthode | Principe | Usage |
|---------|----------|-------|
| **Direct costing** | Seules charges variables → marge contributive | Décision court terme (accepter une commande) |
| **Full costing** | Toutes charges (variables + fixes réparties) → coût complet | Pricing structurel, reporting produit |
| **ABC (Activity-Based Costing)** | Allocation des coûts par activité / driver | Diagnostic fin des marges produit/client |

### 4. Analyse marges

Référence : [references/analyse-marges.md](references/analyse-marges.md).

- Marge brute (CA - achats directs)
- Marge contributive (CA - charges variables)
- Marge opérationnelle (EBIT / CA)
- Marge nette (RN / CA)
- Décomposition des évolutions (effet volume / prix / mix)

### 5. Variance analysis + investigation

Référence : [references/variance-analysis.md](references/variance-analysis.md).

Script : `scripts/variance_analyzer.py` — décompose chaque variance en effet volume / prix / mix / timing.

### 6. Pricing optimization

Référence : [references/pricing.md](references/pricing.md).

Approches :
- Cost-plus (coût + marge cible)
- Value-based (prix = valeur perçue par le client)
- Competition-based (benchmarking concurrents)
- Dynamic pricing (saaS, tiers, usage)

Calcul de l'élasticité prix + simulation d'impact.

### 7. Break-even & seuil de rentabilité

Référence : [references/break-even.md](references/break-even.md).

Formule : `Seuil = CF / (CA - CV) = CF / taux de marge sur coûts variables`

Utile pour :
- Valider un nouveau produit (combien d'unités pour être rentable ?)
- Décider d'un nouveau site / nouvelle embauche
- Stress-test (à quel niveau de CA on bascule en perte ?)

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/profitability_analyzer.py` | Top/bottom 10 produits ou clients |
| `scripts/variance_analyzer.py` | Décomposition variance budget/réel |
| `scripts/pricing_simulator.py` | Simulation d'impact changement prix |

## Templates

| Template | Usage |
|----------|-------|
| `templates/rentabilite-pareto.html` | Visualisation 20/80 produits ou clients |
| `templates/variance-decomposition.md` | Template commentaire variance |

## Références

| Référence | Sujet |
|-----------|-------|
| [references/kpi-catalog-detail.md](references/kpi-catalog-detail.md) | 32 KPIs avec formules, benchmarks, secteurs |
| [references/rentabilite-analyse.md](references/rentabilite-analyse.md) | Méthodologie analyse rentabilité produit/client |
| [references/comptabilite-analytique.md](references/comptabilite-analytique.md) | ABC, full cost, direct cost |
| [references/analyse-marges.md](references/analyse-marges.md) | Marges (brute, contributive, opérationnelle) |
| [references/variance-analysis.md](references/variance-analysis.md) | Décomposition écarts budget/réel |
| [references/pricing.md](references/pricing.md) | Stratégies de pricing + élasticité |
| [references/break-even.md](references/break-even.md) | Calcul seuil de rentabilité |

## Achievements

- `kpi-master` (+40) : catalogue ≥ 10 KPIs sectoriels personnalisés
- `margin-detective` (+35) : 1ère analyse rentabilité produit/client

## Adaptation par audience

**Mode EC** : mission "diagnostic flash" ou "tableau de bord" en mission contractuelle. Méthodes ABC/full cost maîtrisées.

**Mode PME** : focus **leviers actionnables**. Vulgariser "marge contributive" → "ce qui reste après les coûts directs pour payer les frais fixes et dégager du profit".

## Avertissement

Les analyses produites sont des outils d'aide à la décision. Pour les décisions engageantes (changer les prix, arrêter un produit, licencier), consultez les responsables concernés et votre EC.
