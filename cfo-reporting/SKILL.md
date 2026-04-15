---
name: cfo-reporting
description: |
  Skill de reporting financier et communication pour PME/TPE françaises et cabinets EC. Produit le reporting mensuel, trimestriel, annuel, le board pack, les lettres investisseurs trimestrielles, et le tableau de bord CFO exécutif (5-8 KPIs) au format HTML/PDF via Chrome headless. Adapte le ton et le contenu selon l'audience (dirigeant, board, investisseurs, CAC). À utiliser pour toute production de reporting financier.
  Triggers: reporting, reporting mensuel, reporting trimestriel, reporting annuel, board, board pack, CA, conseil administration, comité audit, investisseurs, investor relations, lettre trimestrielle, dashboard, tableau de bord, KPI, flash mensuel, rapport gestion, AG, présentation board, présentation directoire, variances budget, financial reporting, quarterly, monthly close review
metadata:
  last_updated: 2026-04-14
  version: 0.1.0
  audience: [ec, pme]
  tier: 1
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

# cfo-reporting, Reporting & communication

Quatrième skill du bundle. Tier 1, production des reportings financiers selon les destinataires.

## Prérequis

Lire `private/company.json` (profil société) + balance comptable à jour (produite par `cfo-comptabilite`). Si absent, lancer `cfo-init` + `cfo-comptabilite` d'abord.

## Types de reporting produits

| Type | Cadence | Destinataire | Format |
|------|---------|--------------|--------|
| **Flash mensuel** | M+5 | CODIR interne | PDF 1-2 pages |
| **Reporting mensuel** | M+5 à M+7 | Direction + CFO | HTML + PDF dashboard |
| **Reporting trimestriel** | T+15j | Board, CA | PDF board pack 15-25 slides |
| **Reporting annuel** | N+1 avril | AG, CAC, publication | Rapport de gestion + annexe |
| **Lettre investisseurs** | Trimestriel | Investisseurs, VCs | PDF 2-4 pages |
| **Dashboard CFO exécutif** | Hebdo ou mensuel | CEO, fondateurs | HTML responsive |
| **Présentation board** | Trimestriel | Members du CA | Slides 12-18 |

## Workflow principal

### 1. Flash mensuel (30 min à préparer)

Workflow détaillé : [references/flash-mensuel.md](references/flash-mensuel.md).

**Contenu** :
- Top 3 highlights (ce qui s'est bien passé)
- Top 3 lowlights (ce qui a dérapé)
- 5 KPIs clés avec trend vs M-1 et vs budget
- Point tréso express (solde, alertes)
- Top action de la semaine

**Format** : 1 page markdown → PDF via Chrome headless.

### 2. Reporting mensuel complet (2-4h)

Workflow détaillé : [references/reporting-mensuel.md](references/reporting-mensuel.md).

**Contenu standard** :
- P&L mensuel (CA, marges, charges, résultat) vs N-1 et vs budget
- Variance analysis top 10 (écart > 5% et > 10k€)
- KPIs sectoriels (depuis `data/kpi-catalog.json`)
- BFR + trésorerie (renvoyer à `cfo-tresorerie` pour le détail)
- Commentaire de gestion 1-2 paragraphes

### 3. Board pack trimestriel (1-2 jours)

Workflow détaillé : [references/board-pack.md](references/board-pack.md).

**Structure standard 15 slides** :
1. Couverture + période
2. Executive summary (3 bullets)
3. KPIs trimestriel YoY
4. P&L trimestriel détaillé
5. Bilan synthétique
6. Trésorerie + runway
7. Commercial / pipeline
8. Produit / opérations
9. RH / effectif
10. Investissements
11. Risques et opportunités
12. Questions stratégiques
13. Décisions demandées au board
14. Annexes
15. Contact / questions

### 4. Lettre investisseurs (trimestrielle)

Workflow détaillé : [references/investor-letter.md](references/investor-letter.md).

**Ton** : transparent, factuel, équilibré (positif + négatif). Les investisseurs détectent le "sugarcoating" rapidement.

**Structure 3 pages** :
1. Highlights du trimestre (3-5 bullets chiffrés)
2. Métriques clés (ARR, churn, burn, runway, cash, MoM/QoQ)
3. Focus sujet (1 sujet creusé : nouveau produit / nouveau marché / défi)
4. Besoins / asks du board

### 5. Tableau de bord CFO exécutif (auto-généré)

Workflow détaillé : [references/dashboard-cfo.md](references/dashboard-cfo.md).

**5-8 KPIs max** (selon secteur via `data/kpi-catalog.json > kpi_packs_par_secteur`) :
- SaaS : ARR, MRR, Net new ARR, Burn, Runway, LTV/CAC, Magic Number, NRR
- Industrie : CA, Marge brute, EBE, BFR, DSO, DIO, CAPEX, Effectif
- Services BtoB : CA, TJM moyen, Utilisation, DSO, Marge, Taux staffing
- Commerce : CA, Panier moyen, Marge brute, Rotation stocks, Same-store growth

Génération HTML responsive via `scripts/generate_dashboard.py` (pattern moriarty-radar-diagnostic-humanino avec Chrome headless pour PDF).

### 6. Rapport de gestion annuel

Workflow détaillé : [references/rapport-gestion-annuel.md](references/rapport-gestion-annuel.md).

**Contenu légal** (art. L. 232-1 C. com.) :
- Activité de la société au cours de l'exercice
- Situation financière
- Evolutions prévisibles
- Evénements postérieurs
- R&D + CIR
- Prise de participations
- Dépenses somptuaires non déductibles
- Activité filiales (si groupe)
- Rapport sur le gouvernement d'entreprise (si SA cotée)
- Rapport de durabilité CSRD (si in-scope, voir `cfo-csrd-esg`)

## Format de sortie

Format standard [shared/output-format.md](../shared/output-format.md) pour le commentaire d'accompagnement. Les livrables HTML/PDF sont archivés dans `out/`.

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/generate_dashboard.py` | Génère dashboard HTML → PDF via Chrome headless |
| `scripts/compute_kpis.py` | Calcule les KPIs depuis la balance + données opérationnelles |
| `scripts/extract_variances.py` | Top 10 variances budget/réel automatiques |

## Templates

| Template | Usage |
|----------|-------|
| `templates/flash-mensuel.md` | Flash 1-page markdown |
| `templates/reporting-mensuel.html` | Reporting complet HTML |
| `templates/board-pack.html` | Board pack trimestriel 15 slides |
| `templates/investor-letter.md` | Lettre investisseurs |
| `templates/dashboard-cfo.html` | Dashboard exécutif responsive |

## Références

| Référence | Sujet |
|-----------|-------|
| [references/flash-mensuel.md](references/flash-mensuel.md) | Flash 1-page M+5 |
| [references/reporting-mensuel.md](references/reporting-mensuel.md) | Reporting mensuel complet |
| [references/board-pack.md](references/board-pack.md) | Board pack trimestriel 15 slides |
| [references/investor-letter.md](references/investor-letter.md) | Lettre trimestrielle investisseurs |
| [references/dashboard-cfo.md](references/dashboard-cfo.md) | Dashboard exécutif 5-8 KPIs |
| [references/rapport-gestion-annuel.md](references/rapport-gestion-annuel.md) | Rapport de gestion légal |

## Adaptation par audience

**Mode EC** : le reporting est un livrable client. Bien documenter les méthodes de calcul et les hypothèses.

**Mode PME** : focus **actionnable**, chaque KPI doit mener à une décision. Éviter la surcharge.

## Achievements

| Achievement | Trigger | Points |
|-------------|---------|--------|
| `first-dashboard` | 1er tableau de bord mensuel généré | 30 |
| `board-reporting-pro` | 1er board pack trimestriel | 60 |
| `investor-letter` | 1ère lettre trimestrielle investisseurs | 40 |

## Avertissement

Les reportings produits sont des outils de pilotage interne. Pour communication externe (AG, CAC, AMF) : validation EC + CAC obligatoire.
