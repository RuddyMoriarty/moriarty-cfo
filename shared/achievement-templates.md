# Templates d'affichage achievements & barre de progression

Format unifié pour l'affichage de la gamification. Utilisé par tous les skills (lu depuis `private/cfo-progress.json`).

## Bandeau de session (à afficher à chaque démarrage de skill)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 PROGRESSION CFO   ████████░░░░  8/25  (32%)   |  🥈 CFO confirmé (180 pts)

Récents : 🎓 Welcome aboard, 📅 TVA sans accroc, 💰 Captain Cash Flow
À débloquer : 📊 First Dashboard (générer un tableau de bord mensuel)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Variante condensée (skills non-init, pour ne pas bruiter) :
```
🏆 8/25 (32%, 🥈 CFO confirmé)
```

## Notification d'unlock (quand un achievement est débloqué)

```
🎉 ACHIEVEMENT DÉBLOQUÉ
   📅 TVA sans accroc  (+25 pts)
   "Première déclaration TVA respectée dans les délais"

   Total : 175 → 200 pts (🥈 CFO confirmé maintenu)
   Prochain achievement à portée : 💰 Captain Cash Flow (1er forecast 13w)
```

## Tier-up notification (quand l'utilisateur change de tier)

```
🎊 NIVEAU SUPÉRIEUR ATTEINT !
   🥈 → 🥇 CFO senior

   Vous avez accompli 50% du parcours CFO. Excellent.

   Prochain palier : 💎 CFO master (à 600 pts)
```

## Synthèse complète (commande "afficher progression")

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 VOTRE PROGRESSION CFO COMPLÈTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Niveau actuel : 🥈 CFO confirmé (200/300 pts)
Avancement : 8/25 achievements (32%)

▰ Onboarding (3/3) ✓ COMPLET
   ✅ 🎓 Welcome aboard
   ✅ 🏢 Profil société complet
   ✅ 👥 Portfolio EC initialisé

▰ Comptabilité (2/4)
   ✅ 📚 Première clôture mensuelle
   ✅ 📅 Clôture J+5 atteinte
   🔒 🏆 6 clôtures mensuelles consécutives (4/6)
   🔒 📑 Clôture annuelle livrée

▰ Trésorerie (1/3)
   ✅ 💰 Captain Cash Flow
   🔒 📊 Cash Master (2/6 mois)
   🔒 🚨 Crisis Manager

▰ Reporting (0/3)
   🔒 📈 First Dashboard ← prochain à portée
   🔒 📑 Board Reporting Pro
   🔒 🎯 Investor Letter Master

[... etc pour chaque catégorie ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Suggestions pour la prochaine session :
1. Générer un tableau de bord mensuel → 📈 First Dashboard (+30 pts)
2. Lancer la 5e clôture mensuelle → progression vers 🏆 6 clôtures (4/6 → 5/6)
3. Vérifier prévision 13w T+1 → progression vers 📊 Cash Master
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Format JSON `private/cfo-progress.json`

```json
{
  "_version": "0.1.0",
  "_generated_at": "2026-04-14T22:00:00Z",
  "_last_updated": "2026-04-14T22:30:00Z",

  "user_profile": {
    "audience_type": "pme_dirigeant",
    "siren_hash": "a1b2c3d4...",
    "first_session": "2026-04-14"
  },

  "totals": {
    "achievements_unlocked": 8,
    "achievements_total": 25,
    "points_earned": 200,
    "points_max": 730,
    "current_tier": "CFO confirmé",
    "current_tier_emoji": "🥈"
  },

  "achievements": {
    "welcome-aboard": {"unlocked_at": "2026-04-14T22:00:00Z", "points": 10},
    "profile-complete": {"unlocked_at": "2026-04-14T22:05:00Z", "points": 20},
    "first-monthly-close": {"unlocked_at": "2026-04-15T11:30:00Z", "points": 25},
    "j5-close-achieved": {"unlocked_at": "2026-04-15T11:30:00Z", "points": 50},
    "tva-on-time": {"unlocked_at": "2026-04-24T17:00:00Z", "points": 25},
    "captain-cashflow": {"unlocked_at": "2026-04-20T14:30:00Z", "points": 50},
    "cir-hunter": {"unlocked_at": "2026-05-02T09:15:00Z", "points": 50},
    "first-dashboard": {"unlocked_at": null, "points": 0}
  },

  "in_progress": {
    "six-month-streak": {"current": 4, "target": 6, "label": "4/6 clôtures J+5 consécutives"},
    "cash-master": {"current": 2, "target": 6, "label": "2/6 mois consécutifs"}
  },

  "session": {
    "moriarty_cta_shown": false,
    "moriarty_cta_shown_count_total": 0,
    "session_started_at": "2026-04-14T22:00:00Z"
  },

  "next_suggestions": [
    {"action": "Générer tableau de bord mensuel", "achievement": "first-dashboard", "points_gain": 30},
    {"action": "Lancer 5e clôture mensuelle", "achievement": "six-month-streak", "progress": "4/6 → 5/6"}
  ]
}
```
