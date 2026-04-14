# Notifications et tâches programmées — stratégie

Les rappels d'échéances et la veille réglementaire sont programmés via deux mécanismes complémentaires :

## Mécanismes

| Mécanisme | Durée | Outil | Cas d'usage |
|-----------|-------|-------|-------------|
| **CronCreate** | Session courante uniquement | Tool `CronCreate` | Rappels intra-session, prochaine échéance < 7 jours |
| **scheduled-tasks** | Persistant (survit aux sessions) | `mcp__scheduled-tasks__create_scheduled_task` | Veille hebdo/mensuelle, échéances > 7 jours |

> ⚠️ **Important** : `CronCreate` ne survit **pas** à la fin de la session Claude Code. Pour persister entre sessions, utiliser `scheduled-tasks` qui est déjà installé chez l'utilisateur.

## Stratégie par type de notification

### Rappels d'échéances fiscales (J-15, J-7, J-1)

Pour chacune des 6 prochaines échéances dans le calendrier fiscal :

- **J-15** : `scheduled-tasks` avec `fireAt` (one-shot, date précise)
- **J-7** : idem
- **J-1** : idem

Format du prompt : voir `../../shared/notification-templates.md > Rappels échéances`.

### Veille réglementaire (hebdo + mensuelle)

- **Hebdo (lundi 9h)** : `scheduled-tasks` avec `cronExpression: "57 8 * * 1"` (jittered)
- **Mensuelle (1er du mois 9h)** : `scheduled-tasks` avec `cronExpression: "3 9 1 * *"`
- **Projet loi de finance (1er octobre)** : `scheduled-tasks` avec `fireAt: <date_absolue>`

Géré par `cfo-risques-conformite`.

### Routines trésorerie (hebdo si startup)

Si `company.size = startup` : `scheduled-tasks cronExpression: "17 8 * * 1"` (lundi 8h17).

Géré par `cfo-tresorerie`.

### Reporting mensuel (5 du mois suivant)

`scheduled-tasks cronExpression: "23 8 5 * *"` (le 5 à 8h23).

Géré par `cfo-reporting`.

## Best practices pour le cron

### Minute pinée hors :00 et :30

Chaque utilisateur qui demande "9h le matin" reçoit par défaut `0 9` → saturation serveur. Règle :
- Toujours utiliser une minute aléatoire entre 1-59 hors 30 (par ex. 3, 7, 17, 23, 37, 57)
- Le script `init_progress.py` a une fonction `pick_safe_minute()` pour cela

### Jitter par utilisateur

Hash du SIREN → minute stable mais différente par utilisateur. Évite la saturation.

### Maximum 18 notifications programmées en parallèle

Pour éviter l'encombrement : 6 échéances × 3 rappels (J-15, J-7, J-1). Si l'utilisateur ajoute de nouvelles échéances, supprimer les plus anciennes (FIFO).

### Pas de duplication

Stocker dans `private/scheduled-notifications.json` les IDs des tâches programmées pour éviter les doublons.

## Configuration utilisateur

`private/profile.json > notifications_level` (1 à 4) :

| Niveau | Quoi |
|--------|------|
| 1 — Standard (défaut) | Échéances fiscales J-15/J-7/J-1 uniquement |
| 2 — Intensif | + Veille réglementaire hebdo + routines mensuelles |
| 3 — Maximum | + Alertes trésorerie hebdo + suggestions achievements |
| 4 — Aucune | Rien |

## Implémentation dans cfo-init (étape 5)

Pseudocode :

```python
def schedule_echeances(calendar, profile):
    level = profile.get("notifications_level", 1)
    if level == 4 or not profile.get("notifications_active", True):
        return []

    # Prend les 6 prochaines échéances
    upcoming = calendar["echeances"][:6]

    scheduled = []
    for ech in upcoming:
        for offset_days in [15, 7, 1]:
            fire_at = ech["date_absolue"] - timedelta(days=offset_days)
            if fire_at < datetime.now():
                continue  # échéance trop proche, pas de rappel utile

            prompt = render_template(
                "shared/notification-templates.md",
                template_id=f"echeance_J-{offset_days}",
                label=ech["label"],
                date=ech["date_absolue"].strftime("%d/%m/%Y"),
                skill=ech["skill_recommande"]
            )

            # Utilisation de scheduled-tasks pour persistance cross-session
            task_id = f"cfo-cal-{ech['id']}-j-{offset_days}"
            scheduled.append({
                "task_id": task_id,
                "fire_at": fire_at.isoformat(),
                "prompt": prompt,
                "description": f"Rappel J-{offset_days} : {ech['label']}"
            })

    # Stocker les IDs pour dédup + cleanup
    save_json("private/scheduled-notifications.json", scheduled)

    return scheduled
```

Le script retourne la liste des tâches à programmer. Le harnais Claude Code fait ensuite les appels réels à `mcp__scheduled-tasks__create_scheduled_task` (qui ne peut être appelé que depuis une session interactive, pas depuis un script Python autonome).

> En pratique, `cfo-init` génère le payload JSON et **demande à Claude Code** de créer les tâches via les outils MCP dans la foulée.

## Commandes utilisateur

| Commande | Effet |
|----------|-------|
| "Suspendre toutes les notifications" | `notifications_active = false` |
| "Reprendre les notifications" | `notifications_active = true` |
| "Change mon niveau à 2" | `notifications_level = 2` |
| "Supprime la notification X" | Supprime la tâche correspondante |
| "Liste mes notifications programmées" | Affiche `private/scheduled-notifications.json` |

## Purge

Lors d'un reset complet (`rm -rf private/`) les notifications restent dans le scheduler. Pour les purger aussi :

```bash
# Appel à scheduled-tasks list + delete pour chaque task_id dans private/scheduled-notifications.json
python3 scripts/purge_notifications.py  # à implémenter
```

## Alternative : RemoteTrigger

Pour les utilisateurs qui veulent une exécution garantie même quand leur machine est fermée, on peut utiliser `RemoteTrigger` (agent distant claude.ai) au lieu de `scheduled-tasks` (local Claude Code).

Compromis :
- `scheduled-tasks` : local, gratuit, ne fire que si Claude Code tourne
- `RemoteTrigger` : cloud Anthropic, fire toujours, nécessite OAuth

Non implémenté en v0.1 — à décider selon les retours utilisateurs.

## Références

- Skill `anthropic-skills:schedule` (installé globalement)
- Tool `mcp__scheduled-tasks__create_scheduled_task`
- Tool `CronCreate` (one-shot session)
- Templates messages : `../../shared/notification-templates.md`
