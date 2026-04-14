# Reporting mensuel complet

Document détaillé produit à M+5 à M+7 pour la direction.

## Structure (8-15 pages)

### 1. Executive summary (1 page)

- 3 highlights + 3 lowlights
- KPIs flash (5-7 métriques)
- Recommandations prioritaires

### 2. P&L mensuel (2 pages)

Format tableau avec 4 colonnes : Réel M, Budget M, Variance €/%, Réel N-1

| Poste | Réel mars 2026 | Budget mars | Δ | Réel mars 2025 | YoY |
|-------|----------------|-------------|---|----------------|-----|
| CA HT | 1 250 k€ | 1 200 k€ | +50 (+4%) | 1 000 k€ | +25% |
| Achats & charges variables | -420 | -400 | -20 | -350 | — |
| **Marge sur coûts variables** | **830** | **800** | **+30** | **650** | **+28%** |
| Salaires & charges | -650 | -580 | -70 | -500 | — |
| Autres charges fixes | -150 | -140 | -10 | -130 | — |
| **EBITDA** | **30** | **80** | **-50** | **20** | **+50%** |

### 3. Analyse des variances (2-3 pages)

**Méthodologie** : décomposer les écarts entre budget et réel :
- Effet volume (quantités)
- Effet prix (taux, marge)
- Effet mix (produits / clients)
- Effet timing (avance / retard)

Top 10 variances > 10k€ ou > 5% expliquées.

### 4. KPIs sectoriels (1 page)

Selon `private/company.json > secteur.module_sectoriel` :
- Charger le KPI pack correspondant (`data/kpi-catalog.json > kpi_packs_par_secteur`)
- Calculer les KPIs sur le mois écoulé
- Comparer aux benchmarks sectoriels (Banque de France FIBEN)

### 5. Bilan + trésorerie (1-2 pages)

- Bilan synthétique (postes > 5% du total)
- BFR + ratios (DSO/DPO/DIO) — renvoyer à cfo-tresorerie
- Cash flow simplifié + alerte si tension

### 6. Commentaire de gestion (1-2 paragraphes)

Narratif écrit par le CFO (ne pas auto-générer !) :
- Contexte du mois (événements métier, macro)
- Cause des écarts majeurs
- Actions correctives en cours
- Perspectives M+1

### 7. Annexes

- Balance synthétique
- Aging report créances clients
- Tableau emprunts + covenants
- Lettre de mission EC (si applicable)

## Automatisation

Partiel :
- **KPIs** et **variances** : automatisables via `scripts/compute_kpis.py` + `scripts/extract_variances.py`
- **Commentaire de gestion** : MANUEL (le CFO doit écrire)
- **Highlights/lowlights** : pré-remplis par analyse des variances, à valider par le CFO

## Template

`templates/reporting-mensuel.html` — structure responsive imprimable A4 portrait ou paysage.

## Distribution

- **Dirigeant / CEO** : version complète
- **CODIR** : version complète + annexes opérationnelles
- **Board** : version condensée (4-6 pages) — à adapter du trimestriel
- **Banque** (sur demande) : P&L + bilan + commentaire, sans annexes opérationnelles
