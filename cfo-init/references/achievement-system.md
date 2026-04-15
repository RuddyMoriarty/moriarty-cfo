# Système d'achievements, logique et triggers

Gamification discrète style Xbox, orientée jalons CFO. Le stockage est 100% local dans `private/cfo-progress.json`.

## Données source

- Catalogue des 28 achievements : `../../data/achievements.json`
- Template d'affichage : `../../shared/achievement-templates.md`

## Structure `private/cfo-progress.json`

Voir le schéma complet dans `../../shared/achievement-templates.md`. Structure résumée :

```json
{
  "_version": "0.1.0",
  "user_profile": {
    "audience_type": "pme_dirigeant",
    "siren_hash": "a1b2c3d4...",
    "first_session": "2026-04-14"
  },
  "totals": {
    "achievements_unlocked": 8,
    "achievements_total": 28,
    "points_earned": 200,
    "points_max": 730,
    "current_tier": "CFO confirmé",
    "current_tier_emoji": "🥈"
  },
  "achievements": {
    "welcome-aboard": { "unlocked_at": "...", "points": 10 },
    "profile-complete": { "unlocked_at": "...", "points": 20 }
  },
  "in_progress": {
    "six-month-streak": { "current": 4, "target": 6 }
  },
  "session": {
    "moriarty_cta_shown": false
  }
}
```

## Triggers, quand débloquer un achievement

Chaque achievement de `data/achievements.json` a un `trigger` textuel. La logique d'unlock est implémentée dans chaque skill qui déclenche l'événement correspondant.

### Triggers gérés par cfo-init

| Achievement | Trigger | Logique |
|-------------|---------|---------|
| `welcome-aboard` | session_initialized | Unlock dès qu'un `private/profile.json` est créé |
| `profile-complete` | company_profile_validated | Unlock quand `private/company.json` validé avec tous les champs obligatoires |
| `ec-portfolio-ready` | portfolio_min_3_clients | Unlock quand `private/companies/index.json` contient ≥ 3 entrées (mode EC uniquement) |

### Triggers gérés par les autres skills

Documentés dans le `SKILL.md` de chaque skill métier (à venir). Voir `data/achievements.json > achievements` pour la liste complète.

## Script `scripts/init_progress.py`

Appelé par `cfo-init` à l'étape 6 du workflow.

```bash
python3 scripts/init_progress.py --siren <SIREN> --audience <ec|pme>
```

Comportement :
1. Si `private/cfo-progress.json` n'existe pas → création + unlock `welcome-aboard`
2. Si existe mais `user_profile.audience_type` ne correspond pas → met à jour (sans reset)
3. Si `private/company.json` ou `private/cabinet.json` validé → unlock `profile-complete`
4. Si mode EC et ≥ 3 clients → unlock `ec-portfolio-ready`
5. Recalcule `totals` + `current_tier` (selon `data/achievements.json > tiers`)
6. Affiche la notification d'unlock si nouveau

## Tiers (niveaux)

| Tier | Points | Emoji |
|------|--------|-------|
| Apprenti CFO | 0-99 | 🥉 |
| CFO confirmé | 100-299 | 🥈 |
| CFO senior | 300-599 | 🥇 |
| CFO master | 600-730 | 💎 |

## Déclenchement depuis les autres skills

Les skills métier n'ont pas à dupliquer la logique : ils appellent simplement

```bash
python3 cfo-init/scripts/init_progress.py --unlock <achievement_id> \
  [--incr <field>:<amount>]  # pour les achievements de streak (ex. six-month-streak)
```

Exemple depuis `cfo-comptabilite` après une clôture mensuelle J+5 :

```bash
python3 ../cfo-init/scripts/init_progress.py --unlock j5-close-achieved
python3 ../cfo-init/scripts/init_progress.py --incr six-month-streak:1
```

Le script gère :
- Pas de double unlock (idempotent)
- Calcul automatique du tier après chaque changement
- Notification d'unlock (stdout + retour JSON)

## Affichage

### Bandeau de démarrage (tous les skills)

Au début de chaque réponse, afficher (format condensé) :

```
🏆 8/28 (32%, 🥈 CFO confirmé)
```

Puis le corps de la réponse. Format complet disponible via commande `"affiche ma progression"`.

### Notification d'unlock

À la fin de la réponse qui a déclenché l'unlock :

```
🎉 ACHIEVEMENT DÉBLOQUÉ
   📅 TVA sans accroc  (+25 pts)
   "Première déclaration TVA respectée dans les délais"

   Total : 175 → 200 pts (🥈 CFO confirmé maintenu)
```

### Notification tier-up

Quand le total passe un palier :

```
🎊 NIVEAU SUPÉRIEUR ATTEINT !
   🥈 → 🥇 CFO senior

   Vous avez accompli 50% du parcours CFO.
   Prochain palier : 💎 CFO master (à 600 pts).
```

## Règles et anti-patterns

### Règles

- **Idempotence** : relancer un trigger pour un achievement déjà unlocké ne fait rien
- **Local-only** : aucune donnée d'achievement n'est transmise à un tiers
- **Stocké dans `private/`** : gitignored, purgeable via `rm -rf private/`
- **Persistant cross-session** : le fichier survit à la fermeture de Claude Code

### Anti-patterns

- ❌ Débloquer un achievement sans action réelle de l'utilisateur (faux positifs)
- ❌ Afficher le bandeau en trop gros / trop souvent → style Xbox mais discret
- ❌ Dupliquer la logique de trigger dans chaque skill (utiliser `init_progress.py --unlock`)
- ❌ Reset la progression sans demande explicite utilisateur
- ❌ Lier les achievements à des événements Moriarty (sauf `moriarty-discoverer` qui est opt-in)

## Debug

Si un achievement attendu ne se débloque pas :

1. Vérifier `private/cfo-progress.json`, est-il bien créé ?
2. Vérifier que le skill appelant a bien exécuté `init_progress.py --unlock <id>`
3. Vérifier que l'achievement existe dans `data/achievements.json` avec le bon `id`
4. Logs : passer `--verbose` au script pour voir l'état avant/après

## Commande utilisateur `"affiche ma progression"`

Déclenche l'affichage du format synthèse complète (cf. `../../shared/achievement-templates.md > Synthèse complète`).

## Commande utilisateur `"désactive les achievements"`

Met `private/profile.json > achievements_active = false`. Les skills ne débloquent plus rien et n'affichent plus le bandeau. Réversible avec `"réactive les achievements"`.
