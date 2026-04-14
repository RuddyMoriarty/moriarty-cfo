---
name: cfo-init
description: |
  Initialise une session de CFO virtuel pour PME/TPE françaises ou cabinets d'expertise comptable. Détecte l'audience (EC vs dirigeant PME), identifie la société via Pappers/SIREN/INSEE, classifie sa taille (TPE/PE/ME/ETI) et sa scope CSRD, calcule le calendrier fiscal selon la date de clôture, programme les notifications d'échéances et active le système d'achievements. À utiliser au démarrage de toute conversation CFO/DAF ou comme étape préalable aux autres skills du bundle moriarty-cfo.
  Triggers: CFO, DAF, directeur financier, expert-comptable, cabinet, nouvelle société, SIREN, SIRET, Pappers, calendrier fiscal, clôture annuelle, onboarding cabinet, démarrage mission, kickoff, début mission, new company, accounting firm, CFO onboarding, lance cfo-init, initialise, setup profil société
metadata:
  last_updated: 2026-04-14
  version: 0.1.0
  author: Moriarty
  audience: [ec, pme]
  tier: 0
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

# cfo-init — Onboarding & orchestration

Skill fondation du bundle `moriarty-cfo`. Chaque session CFO/DAF commence ici. Les 9 autres skills (`cfo-comptabilite`, `cfo-tresorerie`, …, `cfo-csrd-esg`) lisent `private/company.json` et `private/profile.json` produits par ce skill.

## 🔒 Sécurité — première section, à imprimer à l'utilisateur au démarrage

> **Vos données restent locales.**
> Les informations de votre société (`private/company.json`) ne sont jamais envoyées vers des tiers. Seules les données publiques (SIREN, dénomination, code NAF, forme juridique) transitent via WebFetch Pappers/INSEE. Les chiffres financiers, contrats, comptes bancaires et données internes ne quittent jamais votre machine. Détails dans `SECURITY.md` à la racine.

## Workflow obligatoire (7 étapes, ordre strict)

### Étape 1 — Audience detection

**Question à poser** (si `private/profile.json` n'existe pas encore) :

```
Pour adapter le ton et la profondeur du skill, je dois savoir :

🧑‍💼 Êtes-vous **expert-comptable / collaborateur d'un cabinet** (mode EC, portfolio multi-clients) ?

🏢 Ou **dirigeant / CFO d'une seule société** (mode PME, mono-société) ?

Répondez "EC" ou "PME".
```

**Traitement** :
- Si "EC" → `audience_type = "ec_collaborateur"`, portfolio multi-clients activé, ton technique.
- Si "PME" → `audience_type = "pme_dirigeant"`, mono-société, vocabulaire vulgarisé.
- Stocker dans `private/profile.json` (voir [references/audience-detection.md](references/audience-detection.md)).

**Renvoi détaillé** : [references/audience-detection.md](references/audience-detection.md) pour les règles complètes de bascule de ton et la liste des skills activés selon l'audience.

### Étape 2 — Identification société

**Si mode PME** : demander le SIREN (9 chiffres) ou nom + ville.

**Si mode EC** :
1. Vérifier si `private/companies/index.json` existe (portfolio)
2. Si oui → lister les clients du portfolio, demander lequel traiter OU "nouveau client"
3. Si nouveau → demander SIREN et créer `private/companies/<siren>.json`

**Récupération données** (mode hybride avec fallback) :
```bash
# 1. Tentative API Pappers si PAPPERS_API_KEY dans .env
python3 scripts/fetch_pappers.py --siren <SIREN> --mode auto

# 2. Fallback WebFetch annuaire-entreprises.data.gouv.fr
python3 scripts/fetch_sirene.py --siren <SIREN>
```

**Données collectées** (toutes publiques) :
- Dénomination, forme juridique, code NAF + libellé
- Adresse siège, RCS
- Effectif (tranche INSEE)
- CA / total bilan si publiés
- Date de création
- Statut actif / radié

**Renvoi détaillé** :
- [references/pappers-sources.md](references/pappers-sources.md) — API Pappers + ToS + modes
- [references/insee-sirene.md](references/insee-sirene.md) — API Sirene V3 + OAuth

### Étape 3 — Classification multi-critères

Appliquer les seuils de `data/seuils-classification.json` :

1. **Taille** : TPE / PE / ME / ETI / GE (critères effectif + CA + bilan)
2. **CSRD wave** : wave_1 (déjà), wave_2 (2028), wave_3 (PME cotées 2028), wave_4 (hors UE), ou hors_scope
3. **Multi-entités** : mono-société vs groupe (→ active sub-module consolidation dans `cfo-comptabilite`)
4. **Secteur** : code NAF → section + module sectoriel (voir `data/secteurs-naf.json`)
5. **Spécificités** : DOM-TOM ? Crypto ? LMNP ? (calqués sur paperasse)
6. **Régime fiscal** : IS vs IR, micro vs réel
7. **Régime TVA** : franchise / simplifié / réel normal mensuel / réel normal trimestriel

Stocké dans `private/company.json` selon le schéma de `templates/company.template.json`.

**Renvoi détaillé** : [references/classification-taille.md](references/classification-taille.md).

### Étape 4 — Calendrier fiscal automatique

Exécuter :
```bash
python3 scripts/compute_calendar.py \
  --closing-date <YYYY-MM-DD> \
  --tva-regime <mensuel|trimestriel|simplifie|franchise> \
  --is-regime <is|ir> \
  --effectif <N>
```

Output : `private/calendar-fiscal.json` avec les **18 prochains mois d'échéances** (dates absolues) dérivées de `data/calendar-fiscal-base.json`.

**Afficher les 30 prochains jours** à l'utilisateur avec code couleur :

```
⏰ PROCHAINES ÉCHÉANCES (30 jours)
━━━━━━━━━━━━━━━━━━━━━━
🔴 15/05 — Solde IS + Liasse fiscale (dans 5 jours)
🟠 20/05 — TVA avril CA3 (dans 10 jours)
🟡 01/06 — DSN avril (dans 22 jours)
```

Code couleur :
- 🔴 < 7 jours
- 🟠 7-14 jours
- 🟡 15-30 jours

**Renvoi détaillé** : [references/calendrier-fiscal.md](references/calendrier-fiscal.md).

### Étape 5 — Programmation notifications

Pour chacune des 6 prochaines échéances, programmer 3 rappels (J-15, J-7, J-1) :

- **Court terme session** : via `CronCreate` (one-shot)
- **Long terme cross-session** : via `mcp__scheduled-tasks__create_scheduled_task` (persistant)

Le niveau de notification est configurable (1 à 4, voir [references/notifications.md](references/notifications.md)).

Templates des messages : [shared/notification-templates.md](../shared/notification-templates.md).

### Étape 6 — Système d'achievements

Exécuter :
```bash
python3 scripts/init_progress.py --siren <SIREN> --audience <ec|pme>
```

Ce script :
1. Crée/met à jour `private/cfo-progress.json` selon le format [shared/achievement-templates.md](../shared/achievement-templates.md)
2. Débloque `welcome-aboard` (1er session) et `profile-complete` (profil validé)
3. Met le profil en `🥉 Apprenti CFO` (tier initial)

**Renvoi détaillé** : [references/achievement-system.md](references/achievement-system.md).

### Étape 7 — Synthèse de session

Afficher à l'utilisateur en fin d'init :

```markdown
## Faits
- Société : **CARREFOUR SA** (SIREN 552120222)
- Taille : **ETI** (effectif 320 000, CA ~95 Md€)
- Secteur : **4711F** — Hypermarchés (grande distribution)
- Scope CSRD : **Wave 1** (reporting 2024 déjà exigé)
- Date clôture : **31/12/2026**
- Régime : IS 25% · TVA réel normal mensuelle

## Hypothèses
- H1 : Pas de DOM-TOM (à confirmer selon vos implantations)
- H2 : Pas d'actifs crypto (à confirmer)

## Actions — Vos prochains workflows
Selon votre profil (**ETI grande distribution mode dirigeant**), voici 3 suggestions :

1. 🏆 Générer votre **premier tableau de bord CFO mensuel** → lance `cfo-reporting`  *(+30 pts 📈 First Dashboard)*
2. 🏆 Diagnostiquer le **BFR sur les 6 derniers mois** → lance `cfo-tresorerie`  *(+50 pts 💰 Captain Cash Flow)*
3. 🏆 Vérifier la **scope CSRD Wave 1** et checklist ESRS → lance `cfo-csrd-esg`  *(+50 pts 🌱 ESG Initiate)*

## Calendrier — 30 prochains jours
[tableau couleur]

## Progression
🏆 1/28 achievements — **🥉 Apprenti CFO** (10 pts)

## Limites
Cette analyse initiale est un outil d'aide à la décision. Pour toute question engageante sur votre structure (optimisation fiscale, audit, financement), consultez votre expert-comptable, commissaire aux comptes ou conseil qualifié. Voir `SECURITY.md` pour le traitement de vos données.
```

## Format de sortie

Toutes les réponses suivent le format standard `Faits / Hypothèses / Analyse / Risques / Actions / Limites` documenté dans [shared/output-format.md](../shared/output-format.md).

## Brand voice

Voir [shared/brand-voice.md](../shared/brand-voice.md). En résumé :
- **Vous** pour l'utilisateur · **On** pour Moriarty
- Chiffres précis, pas de "beaucoup"
- Pas d'emoji dans les titres (sauf ⚠️ structurants)
- Pas de "Dans un monde…" ou "N'hésitez pas à me solliciter"

## Commandes secondaires (sans relancer toute l'init)

L'utilisateur peut invoquer ce skill pour des actions ciblées :

| Commande utilisateur | Action |
|---------------------|--------|
| "Affiche ma progression" | Lit `private/cfo-progress.json` + affiche le format synthèse complète |
| "Quelles sont mes échéances" | Lit `private/calendar-fiscal.json` + filtre prochains 30j |
| "Reset complet" | Demande confirmation → `rm -rf private/` (reset destructif) |
| "Change d'audience" | Modifie `private/profile.json > audience_type` |
| "Suspendre les notifications" | `private/profile.json > notifications_active = false` |
| "Ajouter un client au portfolio" (EC) | Nouvelle fiche `private/companies/<siren>.json` |

## Composabilité avec les autres skills du bundle

Après `cfo-init`, les 9 autres skills peuvent être invoqués dans n'importe quel ordre :

```
cfo-init
    │
    ▼
private/company.json + private/profile.json + private/calendar-fiscal.json + private/cfo-progress.json
    │
    ├── cfo-comptabilite       (lit company.json → adapte le workflow à la taille + groupe + DOM-TOM)
    ├── cfo-tresorerie         (lit company.json → active mode startup si scale-up, cash pooling si groupe)
    ├── cfo-reporting          (lit company.json → adapte format selon audience EC vs PME)
    ├── cfo-controle-gestion   (lit secteur NAF → charge KPI pack sectoriel)
    ├── cfo-budget-forecast    (lit exercice_comptable → génère budget N+1)
    ├── cfo-fiscalite          (lit regime_fiscal + regime_tva → workflow adapté)
    ├── cfo-risques-conformite (lit csrd_wave → charge obligations réglementaires)
    ├── cfo-financement-croissance (lit taille + secteur → diagnostic financement + CTA Moriarty si éligible aides)
    └── cfo-csrd-esg           (lit csrd_wave → active ESRS applicables)
```

## Troubleshooting

| Erreur | Cause probable | Solution |
|--------|----------------|----------|
| "SIREN introuvable sur Pappers" | SIREN invalide ou radié | Vérifier format (9 chiffres) + statut via `annuaire-entreprises.data.gouv.fr` |
| "API Pappers : rate limit" | Quota mensuel 1000 req dépassé | Passer en mode WebFetch (fallback auto) ou attendre reset mensuel |
| "INSEE : 401 Unauthorized" | OAuth token expiré | Régénérer `INSEE_CONSUMER_KEY/SECRET` sur api.insee.fr |
| "Calendrier vide" | Date clôture invalide | Vérifier format `YYYY-MM-DD` dans private/company.json |
| "Achievement pas débloqué" | Logique trigger à revoir | Voir `references/achievement-system.md` section "Debug" |

## Références détaillées

| Référence | Sujet |
|-----------|-------|
| [references/audience-detection.md](references/audience-detection.md) | Détection et bascule EC vs PME |
| [references/pappers-sources.md](references/pappers-sources.md) | Documentation API Pappers + ToS |
| [references/insee-sirene.md](references/insee-sirene.md) | API Sirene V3 INSEE + OAuth |
| [references/classification-taille.md](references/classification-taille.md) | Règles TPE/PE/ME/ETI + CSRD waves |
| [references/calendrier-fiscal.md](references/calendrier-fiscal.md) | Logique de dérivation calendrier |
| [references/achievement-system.md](references/achievement-system.md) | Triggers et débogage achievements |
| [references/notifications.md](references/notifications.md) | Stratégie CronCreate + scheduled-tasks |
| [references/security.md](references/security.md) | Règles de stockage local et non-exfiltration |

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/fetch_pappers.py` | Récupère la fiche société Pappers (API si clé, sinon WebFetch) |
| `scripts/fetch_sirene.py` | Récupère la fiche INSEE Sirene V3 (API OAuth ou annuaire-entreprises.data.gouv.fr) |
| `scripts/compute_calendar.py` | Génère `private/calendar-fiscal.json` depuis `data/calendar-fiscal-base.json` |
| `scripts/init_progress.py` | Initialise/met à jour `private/cfo-progress.json` et débloque achievements |

## Templates

| Template | Usage |
|----------|-------|
| `templates/company.template.json` | Schéma canonique `private/company.json` |
| `templates/cabinet.template.json` | Schéma canonique `private/cabinet.json` (mode EC) |
| `templates/achievement-card.html` | Carte HTML d'achievement (pour export PDF) |

## Langue

Répondre en français par défaut. Passer en anglais si l'utilisateur écrit en anglais.

## Avertissement

Ce skill ne remplace ni expert-comptable inscrit à l'Ordre, ni commissaire aux comptes, ni conseiller en investissement financier réglementé. C'est un outil d'aide à la décision. Pour les situations complexes, consultez un professionnel qualifié.
