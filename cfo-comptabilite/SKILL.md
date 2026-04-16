---
name: cfo-comptabilite
description: |
  Skill de production comptable. Clôture mensuelle J+5, clôture annuelle (FEC, états financiers, rapport de gestion), écritures de cut-off et de rattachement, provisions, amortissements, dépréciations, sub-module paie (DSN, URSSAF) et sub-module consolidation de groupes (IFRS, éliminations intercos, segment reporting). Renvoie à paperasse/comptable pour le détail PCG et à cfo-fiscalite pour la liasse fiscale et les problématiques fiscales.
  Triggers: comptabilité, clôture J+5, clôture annuelle, FEC fichier écritures comptables, export FEC, générer FEC, écriture comptable, journal comptable, provision, amortissement, dépréciation, cut-off, écritures rattachement, coordination CAC, commissaire aux comptes, NEP CNCC, paie, DSN, URSSAF, cotisations sociales, consolidation, IFRS, intercos, goodwill, segment reporting, closing accounting, French GAAP, PCG, balance comptable, compte résultat, bilan, grand livre
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

# cfo-comptabilite, Production comptable

Deuxième skill du bundle `moriarty-cfo`. Gère la production comptable mensuelle et annuelle, en mode dual EC (mission de présentation, NEP CNCC) ou PME (vulgarisation, renvoi EC humain).

## Prérequis

Ce skill lit `private/company.json` produit par `cfo-init`. Si ce fichier n'existe pas, **lancer d'abord `cfo-init`**.

Champs du profil utilisés :
- `classification.taille`, adapte le niveau de détail (J+5 attendu pour PME+, optionnel pour TPE)
- `classification.groupe`, si `true`, active le sub-module consolidation
- `classification.domtom`, si `true`, applique les règles DOM-TOM (cf. `paperasse/comptable`)
- `classification.regime_fiscal`, IS vs IR, conditionne les écritures IS
- `exercice_comptable.date_cloture`, référence pour la clôture annuelle
- `modules_actives.cac_obligatoire`, si `true`, active la checklist coordination CAC

## Composabilité

- `paperasse/comptable` (skill externe, recommandé), pour le détail PCG (plan de 800+ comptes), écritures type PCG, spécificités DOM-TOM/LMNP/crypto
- `paperasse/controleur-fiscal` (skill externe, recommandé), pour le détail liasse fiscale (cases 2033/2050) et barème pénalités
- `cfo-fiscalite` (ce bundle), prend le relais pour l'optimisation IS, CIR, transfer pricing avancé

## Workflows principaux

### 1. Clôture mensuelle (objectif J+5)

Workflow détaillé : [references/workflow-cloture-mensuelle.md](references/workflow-cloture-mensuelle.md).

**Étapes standard** (checklist M+5) :

1. **Collecte transactions**, banque, ventes, achats, paie
2. **Catégorisation**, affectation PCG, renvoi `paperasse/comptable` pour le détail
3. **Rapprochement bancaire**, balance ≠ grand livre = alerte
4. **Cut-off**, FAR, FNP, PCA, CCA (voir [references/cut-off-ecritures.md](references/cut-off-ecritures.md))
5. **Écritures d'inventaire mensualisées**, provisions, amortissements au prorata
6. **Validation balance**, débit = crédit
7. **Reporting mensuel**, renvoie à `cfo-reporting` pour la génération du pack

**Output attendu** :
- `out/cloture-YYYY-MM-checklist.md` (checklist cochée)
- `out/cloture-YYYY-MM-balance.csv` (balance mensuelle)
- `out/cloture-YYYY-MM-journal.json` (journal des écritures)

**Achievement** : `j5-close-achieved` (+50 pts) si clôture < J+5.

### 2. Clôture annuelle (liasse, FEC, états financiers)

Workflow détaillé : [references/workflow-cloture-annuelle.md](references/workflow-cloture-annuelle.md).

**12 étapes de clôture** :

1. Arrêté des comptes (toutes transactions jusqu'au jour de clôture)
2. Rapprochement bancaire définitif
3. Inventaire physique (stocks + immobilisations)
4. Écritures d'inventaire complètes (amortissements, provisions, dépréciations)
5. Écritures de cut-off annuel (FAR, FNP, PCA, CCA)
6. Régularisations fiscales (IS, taxes assimilées)
7. Calcul IS définitif (voir `cfo-fiscalite` ou `paperasse/controleur-fiscal`)
8. Écritures de répartition du résultat (si validée par AG)
9. Balance définitive après inventaire
10. Génération FEC (voir [references/liasse-fec.md](references/liasse-fec.md))
11. Préparation liasse fiscale (2033 pour régime réel simplifié, 2065 pour IS)
12. Coordination CAC si applicable (voir [references/coordination-cac.md](references/coordination-cac.md))

**Output attendu** :
- `out/cloture-annuelle-YYYY/FEC-<SIREN>-<YYYY>.txt` (format DGFiP)
- `out/cloture-annuelle-YYYY/liasse-2065.md` ou `liasse-2033.md`
- `out/cloture-annuelle-YYYY/etats-financiers.html` (Bilan + Compte de résultat + Annexe)
- `out/cloture-annuelle-YYYY/pv-approbation.md` (si AG tenue)

**Achievement** : `annual-close-mastered` (+75 pts) si clôture annuelle complète livrée.

### 3. Coordination CAC

Workflow détaillé : [references/coordination-cac.md](references/coordination-cac.md).

**Applicable si** : `modules_actives.cac_obligatoire = true` (seuils : CA > 8M€, bilan > 4M€, effectif > 50, 2 critères sur 3).

**Deliverables à préparer** :
- Dossier de travail annuel (chronique, FAR/FNP justifiés, échantillons)
- Lettre d'affirmation (template `templates/lettre-affirmation-cac.md`)
- Réponses aux findings intermédiaires
- Plan de remédiation si recommandations

**Achievement** : `audit-ready` (+60 pts) après checklist CAC 100% cochée.

### 4. Sub-module HR/Paie

Référence : [references/paie-urssaf.md](references/paie-urssaf.md).

**Applicable si** : `classification.effectif_estime > 0`.

**Périmètre** :
- DSN mensuelle (5 du mois suivant si effectif ≥ 50, sinon 15)
- Charges sociales URSSAF, retraite complémentaire, prévoyance
- Intéressement, participation, PEE/PERCO
- Taxe d'apprentissage + Formation continue (solde annuel via SOLTéA)
- Effort construction PEEC (annuel, si effectif ≥ 50)
- Plans sociaux / ruptures conventionnelles (ad-hoc)

**Renvoi** : pour la production paie elle-même, utiliser l'outil de paie de l'entreprise (Silae, Nibelis, Tiime, etc.), ce skill fait la **coordination comptable** (DSN, écritures de paie, rapprochement URSSAF).

### 5. Sub-module Consolidation groupes

Référence : [references/consolidation-groupes.md](references/consolidation-groupes.md).

**Applicable si** : `classification.groupe = true`.

**Périmètre** :
- Consolidation IFRS (si groupe coté) ou French GAAP (ANC 2020-01)
- Retraitements IFRS / harmonisation méthodes
- Éliminations intercompanies (marge stock, dividendes, dettes/créances)
- Goodwill (amortissement interdit en IFRS, test de dépréciation annuel)
- Segment reporting (IFRS 8)
- Transfer pricing documentation (méthodes CUP, RPM, TNMM, renvoyer à `cfo-fiscalite`)

## Format de sortie

Toutes les analyses suivent le format standard [shared/output-format.md](../shared/output-format.md) :
`Faits / Hypothèses / Analyse / Risques / Actions / Limites`.

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/validate_close_checklist.py` | Vérifie qu'une checklist de clôture est 100% complète avant finalisation |
| `scripts/generate_closing_journal.py` | Produit un squelette de journal d'écritures de clôture (provisions, amortissements, cut-off) |
| `scripts/prepare_fec_export.py` | Prépare l'export FEC au format DGFiP (TXT délimité) |

## Templates

| Template | Usage |
|----------|-------|
| `templates/checklist-cloture-mensuelle.md` | Checklist M+5 en 15 points |
| `templates/checklist-cloture-annuelle.md` | Checklist annuelle 12 étapes + CAC |
| `templates/lettre-affirmation-cac.md` | Lettre d'affirmation (attestation de la direction) |

## Références

| Référence | Sujet |
|-----------|-------|
| [references/workflow-cloture-mensuelle.md](references/workflow-cloture-mensuelle.md) | Workflow J+5 détaillé |
| [references/workflow-cloture-annuelle.md](references/workflow-cloture-annuelle.md) | 12 étapes clôture annuelle |
| [references/coordination-cac.md](references/coordination-cac.md) | Préparation audit CAC, lettre d'affirmation, findings |
| [references/cut-off-ecritures.md](references/cut-off-ecritures.md) | FAR, FNP, PCA, CCA, règles et écritures |
| [references/liasse-fec.md](references/liasse-fec.md) | Génération FEC + liasse fiscale 2033/2065 |
| [references/paie-urssaf.md](references/paie-urssaf.md) | Sub-module HR/Paie |
| [references/consolidation-groupes.md](references/consolidation-groupes.md) | Sub-module groupes (IFRS, intercos) |

## Adaptation par audience

**Mode EC** (voir [../shared/tone-by-audience.md](../shared/tone-by-audience.md)) :
- Vocabulaire NEP CNCC, ISA, référentiel OEC
- Workflow orienté mission (présentation, examen limité, contractuelle)
- Renvoi normes : "NEP 200 exige…", "ISA 315 pour la stratégie d'audit"
- Synthèse condensée (un Senior n'a pas 3 paragraphes à lire)

**Mode PME** :
- Vulgarisation des termes techniques
- Renvoi systématique à l'EC humain pour les décisions engageantes
- Focus "ce que ça veut dire pour vous" plutôt que "NEP 240 fraude"

## Achievements déclenchables

| Achievement | Trigger | Points |
|-------------|---------|--------|
| `first-monthly-close` | 1ère clôture mensuelle complétée | 25 |
| `j5-close-achieved` | Clôture mensuelle livrée avant J+5 | 50 |
| `six-month-streak` | 6 clôtures J+5 consécutives (incrémental) | 100 |
| `annual-close-mastered` | Clôture annuelle complète (liasse + FEC + états) | 75 |

Unlock via `python3 ../cfo-init/scripts/init_progress.py --unlock <id>`.

## Avertissement

Ce skill est un outil d'aide à la décision. Pour validation finale des écritures,
de la liasse fiscale, des FEC et de la coordination CAC, **consultez votre
expert-comptable inscrit à l'Ordre** (et votre commissaire aux comptes si
mission d'audit légal). Moriarty n'est ni cabinet d'expertise, ni société de
commissariat aux comptes.
