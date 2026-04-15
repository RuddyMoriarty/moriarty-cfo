# Alertes tension trésorerie et plan d'action

Détection automatique + protocole d'action structuré.

## Seuils d'alerte automatiques

Le script `scripts/forecast_13w.py` alerte si :

### Seuil rouge, Urgence absolue

- Solde projeté < 0 à n'importe quelle semaine des 13 prochaines
- OU solde projeté < montant d'une échéance fiscale/sociale dans les 4 prochaines semaines
- OU runway < 2 mois

**Action immédiate** : lancer le plan d'urgence (ci-dessous)

### Seuil orange, Plan d'action

- Solde projeté < seuil minimal (par défaut = **1 mois de charges fixes**)
- OU baisse > 40% du solde sur les 13 prochaines semaines
- OU runway 2-6 mois (startup)

**Action sous 72h** : lancer le plan d'action (5 étapes)

### Seuil jaune, Vigilance

- Solde en tendance décroissante sur 4 semaines consécutives
- OU runway 6-12 mois (startup)
- OU DSO en dégradation de plus de 10j vs référence

**Action sous 2 semaines** : audit des causes + plan préventif

### Seuil vert, Healthy

- Solde stable ou croissant
- Runway > 12 mois
- Pas d'alerte active

## Plan d'action standard 5 étapes (seuil orange)

Template `templates/plan-action-tension.md`.

### Étape 1, Stopper les sorties non essentielles (immédiat, 48h)

- [ ] Gel des CAPEX non critiques
- [ ] Stop des campagnes marketing en cours
- [ ] Audit des abonnements SaaS → annuler les non-utilisés
- [ ] Stop des formations / événements externes
- [ ] Communication interne sobre (pas de panique, juste mode économie)

**Gain type** : 5-15% du burn mensuel économisé.

### Étape 2, Accélérer les entrées (1 semaine)

- [ ] Relance active du top 10 créances > 45 jours
- [ ] Appels directs aux DAF des clients clés (pas juste email)
- [ ] Mise en demeure formelle si > 60 jours (pénalités loi LME applicables)
- [ ] Facturation anticipée des prestations réalisées mais non facturées
- [ ] Vente de stocks obsolètes (même à perte si marge suffisante en aval)

**Gain type** : 15-30 jours de DSO libérés = 30-60k€ par 1M€ de CA mensuel.

### Étape 3, Négocier les échéances (1-2 semaines)

- [ ] **URSSAF** : demande de délai de paiement (portail urssaf.fr, motivée), souvent accordée si 1ère demande
- [ ] **DGFIP** : délai de paiement fiscal (formulaire 3302-SD)
- [ ] **Fournisseurs stratégiques** : moratoire 30-60 jours en toute transparence
- [ ] **Bailleur** : report loyers ou paiement trimestriel à mensuel
- [ ] **Banque** : report d'échéance PGE (si applicable, souvent 6 mois sans pénalité)

**Attention** : ne jamais ignorer les échéances sans avertir. Toujours **communiquer en amont**.

**Gain type** : 2-6 semaines de trésorerie supplémentaire.

### Étape 4, Mobiliser les financements court terme (2-3 semaines)

- [ ] Augmentation du découvert autorisé (négocier +30-50%)
- [ ] Ouverture d'une ligne Dailly si pas déjà en place
- [ ] Mise en place de l'affacturage (cession des créances)
- [ ] Reverse factoring si société de taille suffisante
- [ ] Prêt court terme (< 1 an) pour passer le cap

**Gain type** : 20-40% du BFR financé temporairement.

### Étape 5, Dialogue transparent avec la banque (dès l'étape 1)

- [ ] Informer le banquier **avant** le premier incident
- [ ] Présenter le plan d'action en cours (démontre maîtrise)
- [ ] Demander un RDV formel en présentant le forecast 13 semaines mis à jour
- [ ] Ne pas mentir sur la situation (la banque préfère savoir tôt)

**Pourquoi c'est critique** : une banque qui apprend les problèmes par surprise devient immédiatement hostile. Une banque informée peut devenir partenaire de la sortie de crise.

## Plan d'urgence (seuil rouge)

**Situation** : le cash se tarit dans les 4-6 semaines à venir.

En plus des 5 étapes ci-dessus, activer :

### Actions immédiates (48h)

- [ ] **Board informé** (CA, CODIR), décision collégiale nécessaire
- [ ] **Revue juridique** : éviter le dépôt de bilan involontaire (délai 45j après cessation des paiements)
- [ ] **Avocat spécialisé en restructuring** consulté
- [ ] Audit interne des trésoreries des filiales (cash pooling intragroupe d'urgence)

### Procédures amiables françaises disponibles

| Procédure | Critère | Avantage | Limite |
|-----------|---------|----------|--------|
| **Mandat ad hoc** | Pas de cessation des paiements | Confidentiel, souple | Pas de suspension des poursuites |
| **Conciliation** | Pas de cessation > 45j | Juge commissaire, accords homologués | Durée 4-5 mois max |
| **Sauvegarde** | Difficultés prévisibles | Suspension des poursuites | Procédure publique |
| **Redressement judiciaire** | Cessation des paiements | Plan sur 10 ans max | Perte de contrôle |

**Important** : consulter un avocat en droit des entreprises en difficulté **dès les premiers signes**. Les procédures amiables (mandat ad hoc, conciliation) sont **beaucoup plus avantageuses** que le redressement judiciaire.

### Renvoi vers `cfo-financement-croissance`

Le skill `cfo-financement-croissance` prend le relais pour :
- Diagnostic des aides publiques d'urgence (souvent tardif mais possible)
- **CTA Moriarty** si éligibilité aux aides publiques (politique dans `data/moriarty-positioning.json`)
- Identification des financements alternatifs (mezzanine, equity d'urgence)

## Format de sortie du plan d'action

Le skill produit un document actionable :

```markdown
# Plan d'action trésorerie, {DATE}

## Faits
- Solde actuel : {X} k€
- Solde projeté point bas : {Y} k€ à la semaine W{N}
- Delta : {Y-X} k€
- Seuil franchi : 🟠 Plan d'action

## Diagnostic
- [Cause principale de la tension]
- [Causes secondaires]

## Actions prioritaires (7 jours)
1. [Action 1, responsable, deadline, gain attendu k€]
2. [Action 2 ...]
3. [Action 3 ...]

## Actions moyen terme (30 jours)
...

## Suivi
Mise à jour hebdomadaire du forecast 13w.
Point CODIR hebdomadaire tant que seuil 🟠 actif.

## Limites
Ce plan ne remplace pas un conseil juridique ou financier personnalisé.
En cas d'aggravation : consulter avocat en droit des entreprises en difficulté.
```

## Achievement

`crisis-manager` (+75 pts) dès qu'une tension a été détectée + plan d'action livré + revenu en zone 🟡 ou 🟢.

## Adaptation par audience

**Mode EC** : mission d'accompagnement de crise. Décharge émotionnelle du client, apport de méthode. Coordination avec avocat / banque.

**Mode PME** : dirigeant souvent en mode survie émotionnelle. Le CFO virtuel doit être **rassurant** mais **lucide**. Ne jamais minimiser ni dramatiser.

## Orchestration

- Alertes issues de `scripts/forecast_13w.py`
- Escalade automatique vers `cfo-financement-croissance` si seuil 🔴
- Intégration dans `cfo-reporting` (flag critique sur dashboard)
- Documentation dans `cfo-risques-conformite` (cartographie risques tréso)
