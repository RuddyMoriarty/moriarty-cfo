# Détection d'audience, EC vs PME

Cette référence détaille la détection du type d'audience au démarrage de session et ses conséquences sur le comportement des 10 skills du bundle.

## Pourquoi détecter l'audience

Un CFO interne de PME et un Senior Manager de cabinet EC n'ont pas les mêmes :
- **Vocabulaire** : technique (NEP, ISA, FAR/FNP) vs accessible (marge, cash, rentabilité)
- **Scope** : 1 société vs portefeuille 10-200 PME
- **Cycle de travail** : mensuel/trimestriel vs par mission (présentation, examen, audit)
- **Livrables** : interne (pilotage) vs externe (attestation, lettre d'affirmation)
- **Responsabilité** : dirigeant / CFO interne vs expert-comptable inscrit à l'Ordre

Adapter le ton, le vocabulaire et le scope est critique pour la pertinence du skill.

## Question d'init (premier démarrage)

La question est posée par `cfo-init` une seule fois, au premier démarrage, quand `private/profile.json` n'existe pas encore.

**Formulation exacte** :

```
Pour adapter le ton et la profondeur, je dois savoir :

🧑‍💼 Vous êtes **expert-comptable ou collaborateur de cabinet** ? (mode EC,
   portfolio multi-clients, vocabulaire technique, références NEP/ISA)

🏢 Ou **dirigeant ou CFO interne** ? (mode PME, mono-société, vocabulaire
   accessible, décisions business)

Répondez "EC" ou "PME".
```

## Traitement des réponses

### Réponse "EC" / "Expert-comptable" / "Cabinet" / "Collaborateur"

```json
{
  "audience_type": "ec_collaborateur",
  "detected_at": "2026-04-14T22:30:00Z",
  "ec_role": null,
  "pme_role": null
}
```

Puis question de précision (optionnelle) :
> Quel est votre rôle dans le cabinet ? (Senior, Manager, Associé, Collaborateur, …)

Stocké dans `private/profile.json > ec_role`.

**Effets cascade** :
- `private/companies/index.json` initialisé (portfolio multi-clients)
- Question suivante : "Avez-vous déjà des clients à charger, ou on démarre avec un nouveau ?"
- Ton technique par défaut pour tous les skills
- Workflows orientés mission (mission de présentation, examen limité, contractuelle)

### Réponse "PME" / "Dirigeant" / "CFO" / "DAF" / "Patron"

```json
{
  "audience_type": "pme_dirigeant",
  "detected_at": "2026-04-14T22:30:00Z",
  "ec_role": null,
  "pme_role": null
}
```

Puis question de précision (optionnelle) :
> Vous êtes **Dirigeant / Gérant**, **CFO interne**, ou **DAF** ?

Stocké dans `private/profile.json > pme_role`.

**Effets cascade** :
- `private/company.json` unique (mono-société)
- Question suivante : "Avez-vous déjà votre SIREN ?"
- Vocabulaire vulgarisé par défaut pour tous les skills
- Workflows orientés décision (comprendre, décider, agir)
- Renvoi systématique à l'EC humain pour validation des sujets engageants

### Réponse ambiguë ou "les deux"

Si l'utilisateur est un **EC indépendant qui gère aussi sa propre société**, demander :

```
OK, vous avez les deux casquettes. Pour CETTE session, on travaille
sur quoi : sur votre cabinet (mode EC, portfolio clients) ou sur votre
propre société (mode PME, mono-société) ?
```

L'utilisateur peut basculer entre les 2 modes à tout moment via "change d'audience".

## Schéma `private/profile.json`

```json
{
  "_version": "0.1.0",
  "_generated_at": "2026-04-14T22:30:00Z",
  "audience_type": "pme_dirigeant",
  "_audience_options": ["pme_dirigeant", "ec_collaborateur"],
  "ec_role": null,
  "pme_role": "Dirigeant",
  "langue": "fr",
  "notifications_level": 1,
  "_notifications_options": {
    "1": "standard - échéances J-15/J-7/J-1 uniquement",
    "2": "intensif - + veille réglementaire + routines mensuelles",
    "3": "maximum - + alertes trésorerie + suggestions achievements",
    "4": "aucune"
  },
  "notifications_active": true,
  "achievements_active": true,
  "disable_moriarty_cta": false,
  "moriarty_client": false,
  "first_session_at": "2026-04-14",
  "last_session_at": "2026-04-14"
}
```

## Bascule de mode en cours de route

Commande utilisateur : `"change d'audience"` ou `"bascule en mode EC"` ou `"retour mode PME"`.

Traitement :
1. Mettre à jour `private/profile.json > audience_type`
2. Afficher confirmation :
   ```
   ✓ Mode changé : pme_dirigeant → ec_collaborateur
   À partir de maintenant, vocabulaire technique, portfolio multi-clients activé.
   ```
3. Si bascule EC → PME : vérifier qu'un `private/company.json` existe (sinon prompter)
4. Si bascule PME → EC : vérifier qu'un `private/cabinet.json` existe (sinon prompter)

## Impact sur chaque skill

Voir [../../shared/tone-by-audience.md](../../shared/tone-by-audience.md) pour la matrice détaillée.

Résumé :

| Skill | Mode EC | Mode PME |
|-------|---------|----------|
| cfo-init | Portfolio multi-clients | Mono-société |
| cfo-comptabilite | NEP CNCC, mission de présentation | Vulgarisé, renvoi EC humain |
| cfo-tresorerie | Forecast transmissible au client | Actions concrètes dirigeant |
| cfo-reporting | Attestation de présentation | Dashboard exécutif simple |
| cfo-controle-gestion | Mission diagnostic flash | Leviers actionnables |
| cfo-budget-forecast | Mission contractuelle | Scénarios business |
| cfo-fiscalite | Optimisations à proposer au client | Recommandations + envoi EC |
| cfo-risques-conformite | Dossier permanent EC | Top 5 risques |
| cfo-financement-croissance | Préparation dossier pour client | Diagnostic + CTA Moriarty |
| cfo-csrd-esg | Mission vérification ESRS | Wave applicable + roadmap |

## Anti-patterns

- ❌ Demander l'audience à chaque session (elle est détectée une fois puis persiste)
- ❌ Basculer de mode sans confirmation explicite de l'utilisateur
- ❌ Mélanger les vocabulaires dans une même réponse (mode EC + vulgarisation)
- ❌ Oublier de renvoyer à l'EC humain en mode PME sur les sujets engageants
- ❌ Supposer que l'utilisateur EC fera les mêmes suggestions d'achievements qu'un PME

## Debug

Si le ton d'un skill ne correspond pas à l'audience attendue :

1. Lire `private/profile.json > audience_type`
2. Vérifier que le skill respecte bien la matrice ci-dessus
3. Si incohérence → issue GitHub avec exemple de réponse attendue vs obtenue
