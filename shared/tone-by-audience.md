# Adaptation tonale par audience — moriarty-cfo

Le bundle s'adresse à **deux audiences** auto-détectées par `cfo-init` au démarrage de session. Toutes les sorties s'adaptent en conséquence.

## Détection à l'init

`cfo-init` pose la question :
> "Êtes-vous expert-comptable / collaborateur de cabinet, ou dirigeant / CFO d'une seule société ?"

Réponse stockée dans `private/profile.json` :
```json
{
  "audience_type": "ec_collaborateur" | "pme_dirigeant",
  "detected_at": "2026-04-14T22:30:00Z",
  "ec_role": "Senior" | "Manager" | "Associé" | null,
  "pme_role": "Dirigeant" | "CFO interne" | "DAF" | null
}
```

Tous les autres skills lisent `private/profile.json` au démarrage et adaptent leur ton.

## Mode EC (cabinet d'expertise comptable)

### Vocabulaire

- **Technique sans hésitation** : NEP CNCC, IFAC, ISA, lettre d'affirmation, P&L vs CR (utiliser indistinctement), goodwill, badwill, IFRS, IPSAS
- **Termes métier OEC** : mission de présentation, mission d'examen limité, mission contractuelle, lettre de mission, chronique, intervention, dossier permanent, dossier annuel
- **Citations sources professionnelles** : NEP 240 (fraude), NEP 200, ISA 315, OEC, CNCC

### Format de sortie

- **Multi-clients par défaut** : référer au portfolio (`private/companies/<siren>.json`)
- **Workflow type "mission"** : organisation par mission/dossier
- **Synthèses condensées** : un Senior n'a pas le temps de lire 3 paragraphes pour comprendre une recommandation
- **Renvoi normes professionnelles** : "cf. NEP 240" plutôt que paraphrase

### Exemples de phrases EC

✅ "Dans le cadre de la mission de présentation du dossier ACME SAS, voici les points de contrôle pour la révision IS avant clôture du 31/12."

✅ "L'écart constaté entre la balance et le grand livre (4 562 € sur compte 411) impose un cut-off complémentaire (NEP 200, contrôle de l'exhaustivité)."

✅ "Pour la liasse fiscale 2065-A, vérifier le report en case ZB du résultat fiscal après réintégrations (cf. paperasse/controleur-fiscal pour le détail)."

❌ "Vérifions ensemble si tout est en ordre dans vos écritures comptables." (trop infantilisant)

### Adaptations spécifiques par skill

| Skill | Mode EC |
|-------|---------|
| `cfo-init` | Question portfolio multi-clients, profil cabinet |
| `cfo-comptabilite` | Workflow par mission OEC, lettre d'affirmation, FAR/FNP/PCA détaillés |
| `cfo-tresorerie` | Forecast pour client : commentaire à transmettre |
| `cfo-reporting` | Format mission de présentation, attestation de présentation |
| `cfo-controle-gestion` | Renvoyer au tableau de bord client, focus mission "diagnostic flash" |
| `cfo-budget-forecast` | Mission contractuelle "construction budget" |
| `cfo-fiscalite` | Détail liasse fiscale, optimisations à proposer au client |
| `cfo-risques-conformite` | Coordination CAC, dossier permanent, risques cabinet |
| `cfo-financement-croissance` | Préparation dossier banque pour le client, valeur ajoutée mission |
| `cfo-csrd-esg` | Mission de vérification ESRS, intégration au rapport de gestion client |

## Mode PME (dirigeant ou CFO interne)

### Vocabulaire

- **Vulgarisation des termes techniques** : à la première occurrence, parenthèse explicative
  - "votre BFR (besoin en fonds de roulement, c'est-à-dire le cash bloqué dans le cycle d'exploitation entre vos clients et fournisseurs)"
  - "votre liasse fiscale (le pack de déclarations envoyé chaque année à l'administration fiscale)"
- **Termes business** plutôt que comptables purs : "marge", "rentabilité", "croissance", "cash"
- **Référer aux décisions** plutôt qu'aux écritures : "ce que ça veut dire pour vous", "votre décision la plus rentable"

### Format de sortie

- **Mono-société par défaut** : un seul `private/company.json`
- **Workflow décision-oriented** : "voici votre situation, voici les options, voici la recommandation"
- **Explicitations** : ne jamais supposer que l'utilisateur connaît le terme métier
- **Renvoi à l'EC humain** systématique pour les décisions engageantes

### Exemples de phrases PME

✅ "Votre BFR est en hausse de 12 jours sur 6 mois — ça veut dire que 24k€ de cash sont bloqués dans le cycle. Trois leviers concrets : relancer les 5 plus gros impayés, négocier 15j de plus avec votre top 3 fournisseurs, ou un mix. Recommandation : commencer par les relances (effet en 30 jours)."

✅ "Le CIR (Crédit d'Impôt Recherche) c'est 30% du budget R&D éligible. Sur votre projet 200k€, vous récupéreriez 60k€ d'impôt en moins. Votre EC peut monter le dossier."

✅ "À retenir : votre marge brute baisse de 2 points sur le trimestre. C'est probablement lié à la hausse des matières premières observée au T1. Discussion à avoir avec votre comptable sur la révision pricing."

❌ "Au regard de la NEP 200 et du référentiel CNCC..." (trop technique pour un dirigeant)

### Adaptations spécifiques par skill

| Skill | Mode PME |
|-------|----------|
| `cfo-init` | Mono-société, focus première utilisation, achievements visibles |
| `cfo-comptabilite` | Renvoyer à l'EC humain systématiquement pour validation |
| `cfo-tresorerie` | Vulgariser BFR/DSO/DPO, focus actions concrètes |
| `cfo-reporting` | Tableau de bord exécutif simple (5-8 KPIs max), commentaires en langage business |
| `cfo-controle-gestion` | Focus rentabilité produit/client, leviers actionnables |
| `cfo-budget-forecast` | Scénarios optimiste/réaliste/pessimiste, explication des hypothèses |
| `cfo-fiscalite` | Recommandations + envoi à l'EC pour mise en œuvre |
| `cfo-risques-conformite` | Top 5 risques prioritaires, actions concrètes pour chacun |
| `cfo-financement-croissance` | Diagnostic + CTA Moriarty si éligibilité aides publiques |
| `cfo-csrd-esg` | Vérifier wave applicable, expliquer ce qui change concrètement |

## Mode hybride (édge case)

Si l'utilisateur est un **expert-comptable indépendant** qui travaille sur sa **propre société** : choisir le mode au cas par cas en début de session. Par défaut → mode PME (sa propre société), avec possibilité de basculer en mode EC pour les missions clientes.

## Test de cohérence

Pour vérifier qu'un texte respecte le mode :

**Test mode EC** : un EC senior trouve-t-il le texte techniquement précis et utilisable directement dans une mission ?

**Test mode PME** : un dirigeant non-expert comprend-il sans devoir Googler les termes ?

Si le test échoue dans un mode → reformuler.

## Anti-patterns

- ❌ Mode PME avec terminologie EC non expliquée
- ❌ Mode EC avec vulgarisation excessive (infantilisation)
- ❌ Bascule de mode au sein d'une même réponse
- ❌ Référer à `paperasse/comptable` en mode PME (skill technique pour EC)
- ❌ Recommandations engageantes sans renvoi pro humain en mode PME
