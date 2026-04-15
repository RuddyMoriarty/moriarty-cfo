# Routines, moriarty-cfo

Une routine est un cycle de production récurrent porté sur une entité suivie. Chaque routine est déclenchée à intervalles réguliers (hebdo, mensuel, trimestriel, annuel) ou à une date dérivée du profil de l'entité (date de clôture, seuil d'effectif, wave CSRD). Elle orchestre un ou plusieurs skills du bundle et produit un artefact métier concret (flash mensuel HTML, board pack, rapport CSRD, synthèse veille).

Ce module vit dans `cfo-init` parce qu'il s'appuie sur `private/companies/<siren>/company.json` produit à l'onboarding.

## Source de vérité

Le catalogue machine-readable est [`data/routines-catalog.json`](../../data/routines-catalog.json). Toute logique de programmation lit ce fichier, jamais des valeurs en dur.

## Architecture

### Deux horizons d'exécution

| Horizon | Outil | Persistance | Cas d'usage |
|---------|-------|-------------|-------------|
| Session courante | `CronCreate` (one-shot, `recurring=false`) | Jusqu'à la fin de la session Claude Code | Rappel d'échéance dans les 7 prochains jours pendant que vous travaillez |
| Cross-session | `mcp__scheduled-tasks__create_scheduled_task` | Persistant tant que l'utilisateur ne supprime pas la tâche | Routines récurrentes (hebdo, mensuel, trim, annuel) |

Règle : toutes les routines du catalogue utilisent `scheduled-tasks`. `CronCreate` n'est utilisé que pour des rappels ponctuels de type "échéance fiscale dans 5 jours" programmés pendant une session courante.

### Deux niveaux de stockage

| Stockage | Fichier | Contenu |
|----------|---------|---------|
| Par entité | `private/companies/<siren>/routines.json` | État des routines actives pour cette entité (IDs, prochain fire, dernier run, état) |
| Index global | `private/routines-index.json` | Index des tasks scheduled-tasks programmées, pour dédup et cleanup |

### Stockage des artefacts produits

Les artefacts (HTML, PDF, MD, XLSX) vivent sous `private/companies/<siren>/artefacts/` avec un nommage temporel stable :

```
private/companies/552120222/artefacts/
├── flash-2026-04.html            (cloture-mensuelle)
├── board-pack-2026-T1.html       (reporting-trimestriel)
├── cashflow-13w-2026-W15.html    (cashflow-13w)
├── dashboard-2026-04.html        (dashboard-cfo)
├── variance-2026-04.md           (variance-analysis)
├── veille-reg-2026-W15.md        (veille-reglementaire)
└── ...
```

## Flow d'activation d'une routine

```
1. À l'onboarding (cfo-init étape 5) ou sur demande explicite :
   └→ compute_entity_routines.py lit company.json + profile.json
      └→ applique les conditions du catalogue
         └→ retient les routines applicables à cette entité
            └→ écrit private/companies/<siren>/routines.json

2. Pour chaque routine retenue :
   └→ schedule_routines.py calcule le prochain fire (cron ou date dérivée)
      └→ génère un task_id stable (idempotent)
         └→ vérifie que task_id n'existe pas déjà dans l'index global
            └→ appelle mcp__scheduled-tasks__create_scheduled_task
               └→ enregistre le task_id dans routines.json + routines-index.json

3. Au moment du fire (déclenchement par scheduled-tasks) :
   └→ Une nouvelle session Claude Code s'ouvre avec le prompt enqueué
      └→ Le prompt invoque run_routine.py avec l'ID routine + siren
         └→ run_routine.py orchestre skills_chain
            └→ produit l'artefact au chemin pattern
               └→ met à jour routines.json (last_run, state=done)
                  └→ planifie la prochaine occurrence (schedule_routines.py en mode refresh)
```

## Règles d'idempotence

### IDs stables

Le pattern d'ID de task est fonction de la routine, de l'entité et de la période :

| Fréquence | Pattern | Exemple |
|-----------|---------|---------|
| Hebdo | `cfo-{routine_id}-{siren}-W{ww}` | `cfo-cashflow-13w-552120222-W15` |
| Mensuel | `cfo-{routine_id}-{siren}-{yyyy}{mm}` | `cfo-cloture-mensuelle-552120222-202604` |
| Trim | `cfo-{routine_id}-{siren}-{yyyy}-T{qq}` | `cfo-reporting-trimestriel-552120222-2026-T1` |
| Annuel | `cfo-{routine_id}-{siren}-{yyyy}` | `cfo-cloture-annuelle-552120222-2026` |

Une tentative de reprogrammation avec le même ID doit être détectée avant l'appel à `scheduled-tasks` et retourner `already_scheduled` sans erreur.

### Jitter par entité

Pour éviter les pics de charge sur les serveurs de scheduling, la minute de cron est choisie dans un pool stable (voir `routines-catalog.json > routines[].trigger.minute_pool`) par hash du SIREN :

```python
idx = int(hashlib.sha256(siren.encode()).hexdigest(), 16) % len(minute_pool)
minute = minute_pool[idx]
```

Deux entités tombant sur la même routine auront des minutes différentes, mais les deux seront déterministes et reproductibles.

### Minutes interdites

`:00` et `:30` sont exclues des minute_pool du catalogue. Raison : tout le monde demande 9h et 9h30, les serveurs saturent.

## Niveaux de notification

L'utilisateur configure un niveau (1 à 4) dans `private/profile.json > notifications_level` :

| Niveau | Routines activées |
|--------|-------------------|
| 1, Standard (défaut) | Clôture mensuelle, Reporting trim, Clôture annuelle, Dashboard CFO, Paie/DSN, Cashflow 13w, Runway startup, Covenants, Clôture annuelle CSRD, Audit CAC |
| 2, Intensif | Niveau 1 + Veille réglementaire, Veille sectorielle, Atterrissage MAT, Variance analysis, Forecast 12m, Revue assurances, ARR tracking, Unit economics, Stocks DIO, TJM, DSO aging, Consolidation IFRS, Intercos, Cap table |
| 3, Maximum | Niveau 2 + Burn multiple + toutes les routines conditionnelles quand applicables |
| 4, Aucune | Aucune routine programmée (mais le catalogue reste calculé et affichable) |

Chaque routine du catalogue a un champ `level_min` qui indique le niveau minimum pour être activée.

## Mapping profil → routines applicables

Le script `compute_entity_routines.py` applique les conditions suivantes depuis `private/companies/<siren>/company.json` :

| Condition catalogue | Champ `company.json` |
|---------------------|----------------------|
| `always: true` | Appliqué à toutes les entités |
| `size_in: [ETI, GE]` | `classification.taille` dans la liste |
| `secteur_category: saas` | `classification.secteur_category == "saas"` (dérivé du code NAF) |
| `is_startup: true` | `classification.is_startup == true` |
| `has_investors: true` | `classification.has_investors == true` |
| `has_covenants: true` | `classification.has_covenants == true` |
| `is_groupe: true` | `classification.groupe == true` |
| `has_employees: true` | `classification.effectif > 0` |
| `csrd_wave_in: [wave_1, wave_2, wave_3]` | `classification.csrd_wave` dans la liste |
| `seuil_audit: true` | `classification.seuil_audit == true` |
| `has_stocks: true` | `classification.secteur_category in ["industrie", "commerce", "negoce"]` |

Si une condition est absente du catalogue d'une routine, elle est ignorée (logique AND sur les conditions présentes).

## Orchestration skills_chain

Une routine peut chaîner plusieurs skills. Le champ `skills_chain` du catalogue liste les skills dans l'ordre d'invocation.

Exemple pour `cloture-mensuelle` : `["cfo-comptabilite", "cfo-reporting"]` signifie que quand la routine s'exécute, la session Claude Code invoque d'abord le skill `cfo-comptabilite` pour produire la clôture, puis le skill `cfo-reporting` pour produire le flash.

Le prompt enqueué par scheduled-tasks guide explicitement Claude :

```
Exécute la routine "cloture-mensuelle" pour la société SIREN 552120222.

Étapes :
1. Invoque le skill cfo-comptabilite pour la clôture du mois {mm}/{yyyy}.
2. Invoque le skill cfo-reporting pour produire le flash mensuel.
3. Écris l'artefact dans private/companies/552120222/artefacts/flash-{yyyy}-{mm}.html.
4. Mets à jour private/companies/552120222/routines.json : last_run = maintenant, state = done.
5. Planifie la prochaine occurrence via schedule_routines.py.
```

## Commandes utilisateur

Le skill `cfo-init` expose les commandes suivantes pour gérer les routines d'une entité :

| Commande | Effet | Script |
|----------|-------|--------|
| "Calcule les routines pour SIREN X" | Dérive les routines applicables selon le profil, écrit `routines.json` | `compute_entity_routines.py` |
| "Programme les routines de SIREN X" | Planifie les tasks scheduled-tasks | `schedule_routines.py` |
| "Liste mes routines" ou "Statut routines SIREN X" | Affiche les routines actives, prochain fire, dernier run | `list_routines.py` |
| "Désactive la routine X pour SIREN Y" | Supprime la task scheduled-tasks, marque désactivé | `purge_routines.py --routine X --siren Y` |
| "Purge toutes les routines SIREN X" | Supprime toutes les tasks de l'entité | `purge_routines.py --siren X --all` |
| "Change mon niveau à 2" | `notifications_level = 2`, recalcule les routines | compute + schedule |
| "Suspendre toutes les routines" | `notifications_active = false`, les tasks restent mais ne fire pas | `purge_routines.py --suspend` |
| "Exécute la routine X maintenant" | Invoque run_routine.py hors schedule | `run_routine.py --routine X --siren Y` |

## Stratégie de purge

À chaque reprogrammation (`schedule_routines.py`), le script :

1. Lit les task_ids existants depuis `private/routines-index.json`.
2. Identifie les tasks obsolètes (routine plus applicable après changement de profil, ou période révolue).
3. Supprime les tasks obsolètes via `mcp__scheduled-tasks__update_scheduled_task` (avec `enabled: false`) ou via le tool de suppression côté harnais Claude Code.
4. Recrée les nouvelles tasks.

Lors d'un `rm -rf private/` (reset complet), les tasks scheduled-tasks restent en mémoire côté user. Pour les purger aussi :

```bash
python3 cfo-init/scripts/routines/purge_routines.py --all-sirens --force
```

Ce script lit l'index global, émet les ordres de suppression, puis vide l'index.

## Observabilité

Chaque exécution de script écrit une ligne dans `private/routines.log` :

```
2026-04-15T09:23:07+0200 | compute | siren=552120222 | 12 routines retenues (profile=pme_dirigeant size=ETI csrd=wave_1)
2026-04-15T09:23:08+0200 | schedule | siren=552120222 | 12 tasks programmées, 0 doublons, 0 échec
2026-04-15T09:23:09+0200 | schedule | task_id=cfo-cloture-mensuelle-552120222-202605 | fire_at=2026-05-05T08:23:00
2026-05-05T08:23:15+0200 | run | routine=cloture-mensuelle siren=552120222 | skills_chain=[cfo-comptabilite, cfo-reporting] | artefact=flash-2026-04.html
```

## Relation avec le calendrier fiscal

Le calendrier fiscal de `cfo-init étape 4` (`data/calendar-fiscal-base.json` → `private/companies/<siren>/calendar-fiscal.json`) reste séparé des routines.

- Le calendrier fiscal liste les **échéances légales** (TVA, IS, DSN, taxes annuelles). Pour chacune, le flow cfo-init programme 3 rappels (J-15, J-7, J-1) via `CronCreate` en mode session.
- Les routines sont les **cycles de production interne** (flash mensuel, board pack, veille). Elles produisent un artefact, le calendrier ne produit qu'un rappel.

Les deux peuvent coexister : la routine `cloture-mensuelle` produit le flash M+5 ; le calendrier rappelle la TVA CA3 à déposer le 24 du mois.

## Pseudocode de référence

Voir [routines-pseudocode.md](routines-pseudocode.md) pour le détail des 5 scripts.

## Limites v0.1.2 connues

- Mode EC portfolio non livré en v0.1.2, reporté v0.1.3.
- Les artefacts HTML utilisent des templates markdown convertis côté harnais, pas une génération HTML native par les scripts (le harnais Claude Code gère le rendu).
- Pas de mécanisme de "retry" si un run de routine échoue : l'utilisateur doit relancer manuellement via `run_routine.py`.
- Pas de dashboard HTML agrégé "mes routines" côté utilisateur, juste un output texte de `list_routines.py`. v0.1.3.
