---
name: cfo-init
description: |
  Initialise une session de CFO virtuel pour dirigeant ou collaborateur de cabinet d'expertise comptable. Détecte l'audience (cabinet vs dirigeant), identifie l'entité via Pappers/SIREN/INSEE, classifie sa taille (TPE/PE/ME/ETI) et sa wave CSRD, calcule le calendrier fiscal depuis la date de clôture, programme les routines de production et les notifications des prochaines échéances, et active le système d'achievements. À utiliser au démarrage de toute conversation CFO/DAF ou comme étape préalable avant les autres skills du bundle.
  Triggers: directeur financier, expert-comptable, nouvelle entité, SIREN, Pappers, calendrier fiscal, onboarding cabinet, kickoff mission, classification taille, échéances fiscales, profil entité, accounting firm, lance cfo-init, reset profil, portfolio multi-clients, portefeuille cabinet, ajouter client cabinet, dashboard portfolio cabinet, mission presentation examen audit, referent collaborateur, routines portefeuille
metadata:
  last_updated: 2026-04-14
  version: 0.1.0
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

# cfo-init, Onboarding & orchestration

Skill fondation du bundle `moriarty-cfo`. Chaque session CFO/DAF commence ici. Les 9 autres skills (`cfo-comptabilite`, `cfo-tresorerie`, …, `cfo-csrd-esg`) lisent `private/company.json` et `private/profile.json` produits par ce skill.

## Sécurité, première section, à imprimer à l'utilisateur au démarrage

> **Vos données restent locales.**
> Les informations de votre société (`private/company.json`) ne sont jamais envoyées vers des tiers. Seules les données publiques (SIREN, dénomination, code NAF, forme juridique) transitent via WebFetch Pappers/INSEE. Les chiffres financiers, contrats, comptes bancaires et données internes ne quittent jamais votre machine. Détails dans `SECURITY.md` à la racine.

## Workflow obligatoire (7 étapes, ordre strict)

### Étape 1, Audience detection

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

### Étape 2, Identification société

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
- [references/pappers-sources.md](references/pappers-sources.md), API Pappers + ToS + modes
- [references/insee-sirene.md](references/insee-sirene.md), API Sirene V3 + OAuth

### Étape 3, Classification multi-critères

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

### Étape 4, Calendrier fiscal automatique

Exécuter :
```bash
python3 scripts/compute_calendar.py \
  --closing-date <YYYY-MM-DD> \
  --tva-regime <franchise|reel_simplifie|reel_normal_mensuelle|reel_normal_trimestrielle> \
  --is-regime <is|ir> \
  --effectif <N> \
  --output private/calendar-fiscal.json
```

Ajouter `--csrd-wave <wave_1|wave_2|hors_scope>` si l'entite est in-scope CSRD.

Output : `private/calendar-fiscal.json` avec les **18 prochains mois d'échéances** (dates absolues) dérivées de `data/calendar-fiscal-base.json`.

**Afficher les 30 prochains jours** à l'utilisateur avec code couleur :

```
⏰ PROCHAINES ÉCHÉANCES (30 jours)
━━━━━━━━━━━━━━━━━━━━━━
🔴 15/05, Solde IS + Liasse fiscale (dans 5 jours)
🟠 20/05, TVA avril CA3 (dans 10 jours)
🟡 01/06, DSN avril (dans 22 jours)
```

Code couleur :
- 🔴 < 7 jours
- 🟠 7-14 jours
- 🟡 15-30 jours

**Renvoi détaillé** : [references/calendrier-fiscal.md](references/calendrier-fiscal.md).

### Étape 5, Calcul et programmation des routines

Deux activités complémentaires pour cette entité :

**A. Rappels d'échéances fiscales** (calendrier généré à l'étape 4)

Pour chacune des 6 prochaines échéances du calendrier fiscal, programmer 3 rappels (J-15, J-7, J-1) :
- Court terme session : via `CronCreate` (one-shot, ne survit pas à la fin de session)
- Long terme cross-session : via `mcp__scheduled-tasks__create_scheduled_task`

Templates des messages : [shared/notification-templates.md](../shared/notification-templates.md).

**B. Routines de production** (cycles de production internes par entité)

Une routine est un cycle récurrent (hebdo, mensuel, trim, annuel) qui produit un artefact métier en orchestrant un ou plusieurs skills du bundle. Le catalogue contient 25 routines (12 universelles + 13 conditionnelles par profil). Source de vérité : [`data/routines-catalog.json`](../data/routines-catalog.json).

Exécuter dans l'ordre :

```bash
# 1. Dérive les routines applicables selon le profil de l'entité
python3 scripts/routines/compute_entity_routines.py --siren <SIREN>

# 2. Génère les payloads scheduled-tasks (cron + prompt) pour chaque routine
python3 scripts/routines/schedule_routines.py --siren <SIREN> --output /tmp/routines_payload.json
```

Le second script produit un JSON de payloads. Le harnais Claude Code les transforme ensuite en appels réels à `mcp__scheduled-tasks__create_scheduled_task` (un par routine).

Les task_ids sont stables et idempotents : relancer `schedule_routines.py` ne crée pas de doublons.

**Spec détaillée** : [references/routines.md](references/routines.md), [references/notifications.md](references/notifications.md).

**Niveau de notifications** (stocké dans `private/profile.json > notifications_level`, 1 à 4) :
- 1, Standard : routines critiques uniquement (clôtures, reporting trim, dashboard)
- 2, Intensif : +veille, variance, atterrissage, forecast 12m, sectoriel (défaut recommandé)
- 3, Maximum : +burn multiple et toutes conditionnelles applicables
- 4, Aucune : rien n'est programmé

### Étape 6, Système d'achievements

Exécuter :
```bash
python3 scripts/init_progress.py --siren <SIREN> --audience <ec|pme>
```

Ce script :
1. Crée/met à jour `private/cfo-progress.json` selon le format [shared/achievement-templates.md](../shared/achievement-templates.md)
2. Débloque `welcome-aboard` (1er session) et `profile-complete` (profil validé)
3. Met le profil en `🥉 Apprenti CFO` (tier initial)

**Renvoi détaillé** : [references/achievement-system.md](references/achievement-system.md).

### Étape 7, Synthèse de session

Afficher à l'utilisateur en fin d'init :

```markdown
## Faits
- Société : **CARREFOUR SA** (SIREN 552120222)
- Taille : **ETI** (effectif 320 000, CA ~95 Md€)
- Secteur : **4711F**, Hypermarchés (grande distribution)
- Scope CSRD : **Wave 1** (reporting 2024 déjà exigé)
- Date clôture : **31/12/2026**
- Régime : IS 25% · TVA réel normal mensuelle

## Hypothèses
- H1 : Pas de DOM-TOM (à confirmer selon vos implantations)
- H2 : Pas d'actifs crypto (à confirmer)

## Actions, Vos prochains workflows
Selon votre profil (**ETI grande distribution mode dirigeant**), voici 3 suggestions :

1. 🏆 Générer votre **premier tableau de bord CFO mensuel** → lance `cfo-reporting`  *(+30 pts 📈 First Dashboard)*
2. 🏆 Diagnostiquer le **BFR sur les 6 derniers mois** → lance `cfo-tresorerie`  *(+50 pts 💰 Captain Cash Flow)*
3. 🏆 Vérifier la **scope CSRD Wave 1** et checklist ESRS → lance `cfo-csrd-esg`  *(+50 pts 🌱 ESG Initiate)*

## Calendrier, 30 prochains jours
[tableau couleur]

## Progression
🏆 1/28 achievements, **🥉 Apprenti CFO** (10 pts)

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

L'utilisateur peut invoquer ce skill pour des actions ciblées.

### Profil et progression

| Commande utilisateur | Action |
|---------------------|--------|
| "Affiche ma progression" | Lit `private/cfo-progress.json` et affiche la synthèse |
| "Quelles sont mes échéances" | Lit `private/calendar-fiscal.json` et filtre les 30 prochains jours |
| "Reset complet" | Demande confirmation, puis `python3 scripts/routines/purge_routines.py --all-sirens --force` (purge les scheduled-tasks), puis `rm -rf private/` (reset destructif) |
| "Change d'audience" | Modifie `private/profile.json > audience_type` |

### Portfolio EC (v0.1.4, mode cabinet)

| Commande utilisateur | Script invoqué |
|---------------------|----------------|
| "Initialise mon cabinet" | `scripts/portfolio/init_cabinet.py --siren X --denomination Y` |
| "Ajoute le client SIREN X" | `scripts/portfolio/add_client.py --siren X --denomination Y --taille pe --cloture ...` |
| "Liste mes clients" | `scripts/portfolio/list_clients.py [--detailed] [--status actif]` |
| "Archive le client SIREN X" | `scripts/portfolio/remove_client.py --siren X --archive` |
| "Programme les routines de tout le portfolio" | `scripts/portfolio/schedule_all.py [--dry-run]` |
| "Dashboard portfolio" | `scripts/portfolio/portfolio_dashboard.py --output private/portfolio-dashboard.html [--pdf]` |

Details : [references/portfolio-ec.md](references/portfolio-ec.md).

### Routines et notifications par entité

| Commande utilisateur | Script invoqué |
|---------------------|----------------|
| "Calcule les routines pour SIREN X" | `scripts/routines/compute_entity_routines.py --siren X` |
| "Programme les routines de SIREN X" | `scripts/routines/schedule_routines.py --siren X` |
| "Liste les routines de SIREN X" ou "Statut routines" | `scripts/routines/list_routines.py --siren X [--detailed]` |
| "Exécute la routine X maintenant pour SIREN Y" | `scripts/routines/run_routine.py --siren Y --routine X [--period ...]` |
| "Désactive la routine X pour SIREN Y" | `scripts/routines/purge_routines.py --siren Y --routine X` |
| "Purge toutes les routines de SIREN X" | `scripts/routines/purge_routines.py --siren X --all` |
| "Change mon niveau de notifications à 2" | Met `notifications_level=2`, recompute + reschedule |
| "Suspendre toutes les routines" | `notifications_active=false`, tasks restent mais ne fire pas |
| "Reprendre les routines" | `notifications_active=true` |

Après chaque `compute` ou `schedule`, le script écrit dans `private/routines.log` pour observabilité.

### Workflow type d'invocation des routines

```
Utilisateur : "Calcule les routines pour ma société"
    └→ Lance compute_entity_routines.py --siren <SIREN>
       └→ Affiche les N routines retenues (nom, fréquence, prochain fire)
          └→ Demande : "Je les programme toutes ? [oui/non]"
             └→ Si oui : schedule_routines.py --output /tmp/payloads.json
                └→ Pour chaque payload, appelle mcp__scheduled-tasks__create_scheduled_task
                   └→ Affiche la confirmation : "X routines programmées, prochaines occurrences dans ..."
```

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
