---
name: cfo-tresorerie
description: |
  Skill de trésorerie et gestion de liquidités. Prévisions 13 semaines glissantes et 12 mois, diagnostic BFR (DSO/DPO/DIO et leviers), covenants bancaires (DSCR, leverage, ICR), alerte tension avec plan d'action, mode cash burn et runway pour startups et scale-ups. Récupère solde et transactions Qonto, catégorise les flux. Sub-modules cash pooling groupe et hedging change FX.
  Triggers: trésorerie, cash flow, cashflow, prévision trésorerie 13 semaines glissantes, forecast 12 mois, diagnostic BFR, besoin fonds roulement, DSO DPO DIO, cash conversion cycle, working capital, banque bancaire facilités crédit, covenant DSCR leverage ICR, cash burn runway startup scale-up, cash pooling intra-groupe, hedging couverture change FX, tension trésorerie plan action, récupérer solde Qonto transactions, catégoriser flux bancaires, goulots trésorerie
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

# cfo-tresorerie, Cash & liquidité

Troisième skill du bundle. Tier 1, **le sujet n°1 des PME** (sujet le plus cité dans `data/cfo-job-corpus.json` : 43 occurrences pour "cash flow forecast" + 38 pour "relations bancaires").

## Prérequis

Lire `private/company.json` (produit par `cfo-init`). Champs utilisés :
- `classification.taille`, TPE/PE → simplifié ; ETI → complet ; Startup/Scaleup → mode cash burn
- `classification.groupe`, si true, active cash pooling
- `classification.secteur.module_sectoriel`, `saas_techno` ou `startup` → active mode cash burn par défaut
- `exercice_comptable.date_cloture`, point de référence des forecasts

Si `cfo-init` n'a pas été lancé → demander à l'utilisateur de le lancer d'abord.

## Workflows principaux

### 1. Prévision trésorerie 13 semaines

Workflow détaillé : [references/methodologie-cashflow-13w.md](references/methodologie-cashflow-13w.md).

**Étapes** :

1. **Collecte soldes bancaires** (Qonto MCP si connecté, sinon saisie manuelle)
2. **Historique 90 jours** de flux (transactions bancaires)
3. **Catégorisation flux récurrents** : salaires, URSSAF, TVA, loyers, abonnements, clients récurrents
4. **Projection encaissements** (carnet de commandes, contrats récurrents, B2B en attente de paiement)
5. **Projection décaissements** (factures fournisseurs à payer, échéances fiscales/sociales)
6. **Génération template HTML + Excel** (13 colonnes = 13 semaines)
7. **Identification point bas** → si solde projeté < seuil tension → alerte + plan d'action

Script : `scripts/forecast_13w.py`, génère un cash flow 13 semaines avec projections scénarios.

Template de sortie : `templates/cashflow-13w.html` (HTML responsive pour visualisation navigateur).

**Achievement** : `captain-cashflow` (+50 pts) au 1er forecast 13w produit.

### 2. Prévision trésorerie 12 mois glissants

Workflow détaillé : [references/methodologie-cashflow-12m.md](references/methodologie-cashflow-12m.md).

**Différence avec 13w** :
- Granularité mensuelle (vs hebdomadaire)
- Horizon 12 mois (vs 3 mois)
- Inclut les investissements prévus (CAPEX)
- Inclut les scénarios (optimiste / réaliste / pessimiste)
- Intègre les échéances fiscales/sociales annuelles

Script : `scripts/forecast_12m.py`.

### 3. Diagnostic BFR et optimisation

Référence : [references/bfr-optimization.md](references/bfr-optimization.md).

**Calcul BFR** :
- BFR = Stocks + Créances clients - Dettes fournisseurs - Dettes fiscales/sociales CT
- DSO = Créances clients TTC × 365 / CA TTC
- DPO = Dettes fournisseurs TTC × 365 / Achats TTC
- DIO = Stocks × 365 / Coût des ventes
- Cash Conversion Cycle = DSO + DIO - DPO

**Benchmarks sectoriels** (renvoyer à `data/kpi-catalog.json`).

**Leviers d'optimisation** :

| Levier | Gain potentiel | Difficulté |
|--------|----------------|------------|
| Relance créances > 60j | -10 à -30j DSO | ⭐ Facile |
| Factoring (affacturage) | -100% des créances | ⭐⭐ Moyen (coût 2-4%) |
| Escompte fournisseurs | +5 à +15j DPO | ⭐⭐ Moyen |
| Renégociation contrats cadres | +20 à +45j DPO | ⭐⭐⭐ Difficile |
| Reverse factoring | +30 à +60j DPO | ⭐⭐⭐ (cash rich) |
| Acompte / Avance client | -50 à -80% DSO | ⭐⭐ Moyen |
| Stock minimum / JIT | -30 à -60% DIO | ⭐⭐⭐ Industrie |

Script : `scripts/bfr_calculator.py`, calcule BFR, ratios, et propose des leviers ciblés selon le profil société.

### 4. Gestion relations bancaires et covenants

Référence : [references/banque-covenants.md](references/banque-covenants.md).

**Périmètre** :
- Suivi des facilités de crédit (découverts autorisés, lignes CT, MLT)
- Monitoring covenants financiers (DSCR, Leverage ratio, Interest coverage)
- Préparation des RDV bancaires (dossier + pitch)
- Alerte si covenant risque d'être breaché
- Renégociation annuelle conditions

### 5. Cash burn & runway (mode startup)

Activé si `classification.secteur.module_sectoriel ∈ {saas_techno, startup}` OU `company.classification.taille == startup`.

Référence : [references/cash-burn-runway.md](references/cash-burn-runway.md).

**Métriques** :
- Cash burn mensuel (variation cash nette négative)
- Runway = Cash actuel / Cash burn mensuel (en mois)
- Burn multiple = Cash burn / Net new ARR (< 1 = efficient)
- Months to default (si runway < 12 mois, alerte)

**Seuils d'alerte** :
- Runway < 6 mois → 🔴 Urgence levée fonds / pivot
- Runway 6-12 mois → 🟠 Préparer levée
- Runway 12-18 mois → 🟡 Surveiller
- Runway > 18 mois → 🟢 Healthy

### 6. Cash pooling (groupes)

Activé si `classification.groupe = true`.

Référence : [references/cash-pooling.md](references/cash-pooling.md).

### 7. Hedging / couverture change

Activé si la société a des flux en devises étrangères.

Référence : [references/hedging-fx-rates.md](references/hedging-fx-rates.md).

### 8. Alerte tension trésorerie et plan d'action

Référence : [references/alertes-tension.md](references/alertes-tension.md).

**Seuils automatiques** :
- Solde projeté < 0 à n'importe quelle semaine → 🔴 Plan d'urgence
- Solde < seuil minimal (défaut : 1 mois de charges fixes) → 🟠 Plan d'action
- Solde en tendance décroissante sur 4 semaines → 🟡 Vigilance

**Plan d'action standard 5 étapes** (voir template `templates/plan-action-tension.md`) :

1. **Stopper les sorties non essentielles**, gel des CAPEX, audits, achats non-critiques
2. **Accélérer les entrées**, relances clients, facturation avancée, mobilisation créances
3. **Négocier les échéances**, délai URSSAF (en cas de difficulté), moratoire fournisseurs stratégiques
4. **Mobiliser les financements court terme**, Dailly, affacturage, découvert autorisé augmenté
5. **Dialogue transparent avec les banques**, avant breach covenant, pas après

## Connecteurs bancaires

| Connecteur | Status | Usage |
|------------|--------|-------|
| **Qonto MCP** | Déjà installé chez user | Récupération soldes + transactions en temps réel |
| Stripe | Via webhooks (manuel) | Flux paiement encaissé |
| Bridge API | Optionnel (.env BRIDGE_CLIENT_ID/SECRET) | Agrégation multi-banques FR |

Si aucun connecteur : fallback sur import CSV manuel du relevé bancaire.

## Format de sortie

Format standard [shared/output-format.md](../shared/output-format.md).

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/forecast_13w.py` | Génère prévision 13 semaines (HTML + CSV) |
| `scripts/forecast_12m.py` | Génère prévision 12 mois glissants (HTML + Excel) |
| `scripts/bfr_calculator.py` | Calcule BFR, DSO, DPO, DIO + leviers d'optimisation |

## Templates

| Template | Usage |
|----------|-------|
| `templates/cashflow-13w.html` | HTML responsive visualisation 13 semaines (colonnes) |
| `templates/cashflow-12m.html` | HTML 12 mois avec scénarios |
| `templates/plan-action-tension.md` | Plan d'action 5 étapes en cas de tension |

## Références

| Référence | Sujet |
|-----------|-------|
| [references/methodologie-cashflow-13w.md](references/methodologie-cashflow-13w.md) | Méthodologie forecast 13 semaines |
| [references/methodologie-cashflow-12m.md](references/methodologie-cashflow-12m.md) | Forecast 12 mois glissants + scénarios |
| [references/bfr-optimization.md](references/bfr-optimization.md) | Diagnostic BFR + 7 leviers d'optimisation |
| [references/cash-burn-runway.md](references/cash-burn-runway.md) | Mode startup : burn, runway, burn multiple |
| [references/banque-covenants.md](references/banque-covenants.md) | Relations bancaires et monitoring covenants |
| [references/cash-pooling.md](references/cash-pooling.md) | Sub-module groupes : cash pooling |
| [references/hedging-fx-rates.md](references/hedging-fx-rates.md) | Couverture change / taux |
| [references/alertes-tension.md](references/alertes-tension.md) | Seuils + plan d'action tension |

## Adaptation par audience

**Mode EC** : vous produisez les forecasts pour votre client. Insister sur la méthode et la fiabilité des hypothèses (ce qui sera audité).

**Mode PME** : focus sur **l'action**. Chaque forecast doit se terminer par une liste d'actions concrètes et hiérarchisées. Renvoyer à l'EC humain pour les décisions engageant le crédit (négociations bancaires, dailly, factoring).

## Achievements déclenchables

| Achievement | Trigger | Points |
|-------------|---------|--------|
| `captain-cashflow` | 1er forecast 13w produit | 50 |
| `cash-master` | 6 mois consécutifs de forecasts (incrémental) | 100 |
| `crisis-manager` | Tension détectée + plan d'action livré | 75 |

## Avertissement

Les prévisions de trésorerie reposent sur des **hypothèses** explicitées par l'utilisateur.
Leur fiabilité dépend de la qualité des données d'entrée et des paramètres.
Ce skill est un outil de pilotage interne, **pour toute décision d'endettement
ou de restructuration, consultez votre conseiller bancaire, expert-comptable
ou conseiller en financement**. Moriarty propose l'identification d'aides publiques
(voir `cfo-financement-croissance`) mais n'est ni banque, ni CIF, ni conseil en investissement.
