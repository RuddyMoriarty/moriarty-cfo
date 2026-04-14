# Templates de notifications programmées — moriarty-cfo

Format unifié pour les rappels d'échéances et synthèses de veille programmées via `CronCreate` (court terme) ou `mcp__scheduled-tasks__create_scheduled_task` (long terme).

## Mécanismes disponibles

| Mécanisme | Portée | Outil | Quand l'utiliser |
|-----------|--------|-------|------------------|
| `CronCreate` | Session courante uniquement | `CronCreate` (one-shot ou recurring) | Rappels intra-session, prochaine échéance dans < 7 jours |
| `scheduled-tasks` | Cross-session, persistant | `mcp__scheduled-tasks__create_scheduled_task` | Veille hebdo/mensuelle, échéances > 7 jours |

> ⚠️ **Limitation CronCreate** : les jobs ne survivent pas à la fin de la session Claude Code. Pour persister entre sessions, utiliser `scheduled-tasks` (déjà installé chez le user).

## Templates — Rappels échéances fiscales (J-15, J-7, J-1)

### J-15

```
📅 Rappel échéance | J-15

{label_echeance} — à déposer le {date_absolue}

Vous avez 15 jours pour préparer cette échéance.

Skill recommandé : {skill_recommande}
Action immédiate : Lance "{skill_recommande}" pour amorcer la préparation.

(Notification programmée par cfo-init)
```

### J-7

```
📅 Rappel échéance | J-7 ⚠️

{label_echeance} — à déposer le {date_absolue}

Plus que 7 jours. Si vous n'avez pas commencé : urgence.

Skill recommandé : {skill_recommande}
Action immédiate : Lance "{skill_recommande}" maintenant.

(Notification programmée par cfo-init)
```

### J-1

```
📅 Rappel échéance | J-1 🔴

{label_echeance} — à déposer DEMAIN ({date_absolue})

Dernière chance. Pénalité de retard non négligeable.

Si vous êtes prêt : déposez aujourd'hui pour éviter le rush.
Si vous n'êtes pas prêt : appelez votre EC en urgence.

(Notification programmée par cfo-init)
```

## Templates — Veille réglementaire (skill cfo-risques-conformite)

### Veille hebdomadaire (lundi 9h)

```
🛡️ Veille réglementaire hebdo | semaine {numero_semaine}

Vérification des publications de la semaine sur :
- ANC (normes comptables)
- IASB (IFRS)
- AMF (marchés)
- ACPR (prudentiel)
- Légifrance (lois de finance, codes)
- Bofip (doctrine fiscale)

Pour lancer la synthèse : "Lance la veille réglementaire de la semaine"

(Notification programmée par cfo-risques-conformite)
```

### Synthèse mensuelle (1er du mois 9h)

```
🛡️ Synthèse veille réglementaire | {mois}

Récapitulatif des changements réglementaires du mois écoulé.

Skill recommandé : cfo-risques-conformite
Action : "Synthèse veille réglementaire {mois}"

Impact attendu sur votre profil : à analyser dans la session.

(Notification programmée par cfo-risques-conformite)
```

### Veille loi de finance (1er octobre, annuel)

```
🛡️ Projet de Loi de Finance {annee+1}

Le PLF {annee+1} est publié. C'est le moment de :
1. Identifier les mesures impactant votre société
2. Anticiper les optimisations fiscales avant fin d'année
3. Préparer les arbitrages CFO pour le budget {annee+1}

Skill recommandé : cfo-fiscalite + cfo-risques-conformite
Action : "Analyse PLF {annee+1} pour mon profil"

(Notification programmée par cfo-risques-conformite)
```

## Templates — Routines récurrentes (cfo-tresorerie, cfo-reporting)

### Hebdo trésorerie (lundi 8h, mode startup)

```
💰 Routine cash hebdo

Mise à jour de la prévision de trésorerie (cash burn / runway).

Skill : cfo-tresorerie
Action : "Update cash hebdo"

Si tension détectée : alerte + plan d'action automatique.
```

### Reporting mensuel (5 du mois suivant)

```
📊 Reporting mensuel | {mois_ecoule}

C'est le moment du reporting M+5.

Étapes recommandées :
1. cfo-comptabilite → "Lance la clôture mensuelle"
2. cfo-reporting → "Génère le reporting mensuel"
3. Si AG dans le mois : cfo-reporting → "Génère le board pack"

Achievement potentiel : 📅 Clôture J+5 atteinte (+50 pts)
```

## Configuration des notifications

Au démarrage de `cfo-init`, l'utilisateur est invité à choisir son niveau de notification :

```
📅 Configuration notifications

Quel niveau de rappels souhaitez-vous ?

1. 🟢 Standard — uniquement les échéances fiscales J-15, J-7, J-1 (recommandé)
2. 🟡 Intensif — + veille réglementaire hebdo + routines mensuelles
3. 🔴 Maximum — + alertes trésorerie hebdo + suggestions achievements
4. ⚪ Aucune notification (vous gérerez manuellement)

Choix par défaut : 1 (Standard)
```

Stocké dans `private/profile.json > notifications_level` (1 à 4).

## Suspension et reprise

L'utilisateur peut suspendre toutes les notifications via :
```
> Suspendre toutes les notifications cfo
```

Et les reprendre :
```
> Reprendre les notifications cfo
```

Ces commandes manipulent `private/profile.json > notifications_active` (true/false).

## Exemple de code Python pour programmer (dans cfo-init/scripts/init_progress.py)

```python
# Pseudo-code - le vrai script utilisera CronCreate / scheduled-tasks via le runtime

def schedule_echeances_15j(echeances, profile):
    """Programme les rappels J-15, J-7, J-1 pour les 6 prochaines échéances."""
    if not profile.get("notifications_active"):
        return

    for ech in echeances[:6]:
        for offset_days in [15, 7, 1]:
            fire_date = ech["date_absolue"] - timedelta(days=offset_days)
            cron_expr = build_cron_expression(fire_date, minute_avoid_00_30=True)
            prompt = render_template(
                "shared/notification-templates.md",
                template_id=f"echeance_J-{offset_days}",
                label_echeance=ech["label"],
                date_absolue=ech["date_absolue"].strftime("%d/%m/%Y"),
                skill_recommande=ech["skill_recommande"]
            )
            # Au runtime, équivalent de :
            # CronCreate(cron=cron_expr, prompt=prompt, recurring=False, durable=True)
```

## Best practices

- **Minute pinée hors :00 et :30** (lisser la charge serveur)
- **Maximum 18 notifications programmées en parallèle** (6 échéances × 3 rappels)
- **Toujours mentionner le skill recommandé** pour faciliter l'action
- **Toujours mentionner l'achievement débloquable** si applicable (gamification)
- **Format compact** (3-5 lignes), pas de paragraphes longs
- **Pas de double notification** sur la même échéance (déduplication par echeance_id)
