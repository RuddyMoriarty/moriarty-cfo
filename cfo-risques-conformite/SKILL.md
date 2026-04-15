---
name: cfo-risques-conformite
description: |
  Skill de gestion des risques et conformité pour PME/TPE françaises et cabinets EC. Couvre la cartographie des risques (méthodologie COSO ERM 2017), le contrôle interne, la conformité LCB-FT (lutte contre le blanchiment et le financement du terrorisme), la coordination avec le commissaire aux comptes (CAC), la gestion des assurances, l'audit interne, la conformité RGPD/ACPR/AMF, et la veille réglementaire programmée (lois de finance, IFRS, PCG, URSSAF, CSRD). Programme automatiquement des tâches de veille hebdomadaires et mensuelles.
  Triggers: risques, cartographie risques, COSO ERM, contrôle interne, LCB-FT, blanchiment, TRACFIN, CAC, commissaire aux comptes, audit interne, conformité, compliance, RGPD, ACPR, AMF, assurance, BCP, plan continuité, veille réglementaire, lois de finance, monitoring, gouvernance, comité audit, dispositif controle interne, COSO, risk mapping, internal audit
metadata:
  last_updated: 2026-04-14
  version: 0.1.0
  author: Moriarty
  audience: [ec, pme]
  tier: 3
  bundle: moriarty-cfo
includes:
  - references/**
  - scripts/**
  - templates/**
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
  - WebSearch
  - Glob
  - Grep
license: MIT
---

# cfo-risques-conformite — Risk management & internal controls

Huitième skill. Tier 3 (risque & gouvernance).

## Prérequis

- `private/company.json` (cfo-init)
- `private/calendar-fiscal.json` pour les échéances de conformité

## Workflows principaux

### 1. Cartographie des risques (méthodologie COSO ERM 2017)

Référence : [references/coso-erm.md](references/coso-erm.md).

**5 composantes COSO ERM** :
1. **Governance & Culture** — gouvernance, ton du top management
2. **Strategy & Objective Setting** — alignement stratégie/risque
3. **Performance** — identification, évaluation, priorisation des risques
4. **Review & Revision** — surveillance continue
5. **Information, Communication & Reporting** — flux d'information

**Matrice 5×5** : Probabilité × Impact (chacun de 1 à 5).

Catégories de risques typiques :
- Stratégique
- Opérationnel
- Financier
- Compliance / réglementaire
- Réputationnel
- Cyber / IT
- ESG / climat
- Géopolitique

### 2. Contrôle interne

Référence : [references/controle-interne.md](references/controle-interne.md).

- Design (procédures, RACI, narratives)
- Test des contrôles (échantillons)
- Remédiation des findings
- Revue annuelle

### 3. Conformité LCB-FT

Référence : [references/lcb-ft.md](references/lcb-ft.md).

- Politique LCB-FT formalisée
- Désignation responsable LCB-FT
- KYC clients (Customer Due Diligence)
- Surveillance transactions inhabituelles
- Déclarations TRACFIN si soupçon

### 4. Coordination CAC

Voir [`cfo-comptabilite/references/coordination-cac.md`](../cfo-comptabilite/references/coordination-cac.md) pour le détail des 3 phases (intérim / final / AG).

### 5. Gestion des assurances

Référence : [references/assurances.md](references/assurances.md).

- RC pro (responsabilité civile professionnelle)
- RC mandataires sociaux
- Multirisque entreprise
- Cyber
- Dommages aux biens
- Cyber-rançon (extension)

### 6. Veille réglementaire

Référence : [references/veille-reglementaire.md](references/veille-reglementaire.md).

**Programmée automatiquement** :
- Hebdomadaire (lundi 9h jittered) : ANC, IASB, Légifrance, BoFip
- Mensuelle (1er du mois) : synthèse pour CFO + CODIR
- Annuelle (1er octobre) : projet loi de finance N+1

Voir aussi `cfo-fiscalite/references/veille-fiscale.md` pour la partie fiscale.

### 7. Conformité RGPD / sectorielles

Référence : [references/conformite-sectorielle.md](references/conformite-sectorielle.md).

- RGPD : DPO, registre des traitements, breach notification 72h CNIL
- ACPR (banque/assurance), AMF (cotées)
- Sectorielles : santé, défense, sécurité

### 8. Plan de continuité d'activité (BCP)

Référence : [references/bcp.md](references/bcp.md).

- ISO 22301 framework
- Identification activités critiques
- Scénarios de rupture (cyber, sinistre, pandémie)
- Plans de reprise

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/risk_mapping_generator.py` | Génère matrice de risques 5×5 depuis questionnaire |
| `scripts/veille_scheduler.py` | Programme les tâches de veille via mcp__scheduled-tasks |
| `scripts/internal_control_checklist.py` | Génère checklist contrôle interne par fonction |

## Templates

| Template | Usage |
|----------|-------|
| `templates/cartographie-risques.html` | Matrice 5×5 + top 10 risques + plan d'action |
| `templates/politique-lcb-ft.md` | Politique LCB-FT type |
| `templates/bcp-plan.md` | Plan de continuité d'activité |

## Références

| Référence | Sujet |
|-----------|-------|
| [references/coso-erm.md](references/coso-erm.md) | Méthodologie COSO ERM 2017 |
| [references/controle-interne.md](references/controle-interne.md) | Design + test contrôle interne |
| [references/lcb-ft.md](references/lcb-ft.md) | Conformité LCB-FT, TRACFIN |
| [references/assurances.md](references/assurances.md) | Gestion des assurances |
| [references/veille-reglementaire.md](references/veille-reglementaire.md) | Veille programmée |
| [references/conformite-sectorielle.md](references/conformite-sectorielle.md) | RGPD, ACPR, AMF, sectorielles |
| [references/bcp.md](references/bcp.md) | Plan de continuité ISO 22301 |

## Achievements

- `risk-mapper` (+45) : 1ère cartographie des risques
- `audit-ready` (+60) : préparation CAC complétée
- `lcb-ft-champion` (+45) : politique LCB-FT formalisée

## Adaptation par audience

**Mode EC** : mission contractuelle "diagnostic risques" ou "préparation audit". Référencer normes (NEP CNCC, COSO).

**Mode PME** : focus actionnable. Les top 5 risques + actions concrètes prioritaires. Renvoyer à un avocat / consultant pour les sujets pointus (LCB-FT bancaire, ACPR…).

## Avertissement

Ce skill couvre les risques et la conformité **génériques PME/ETI**. Les sujets sectoriels spécifiques (banque, assurance, santé, défense) requièrent un **expert sectoriel**. Pour les contrôles ACPR / AMF, consulter un cabinet spécialisé.
