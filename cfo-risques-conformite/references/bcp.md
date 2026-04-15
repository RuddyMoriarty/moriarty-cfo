# BCP, Plan de Continuité d'Activité

Méthodologie ISO 22301. Plan permettant à la société de maintenir ou reprendre ses activités critiques en cas de crise majeure.

## Pourquoi un BCP ?

**Risques couverts** :
- Cyberattaque (ransomware bloquant le SI)
- Sinistre physique (incendie locaux, inondation)
- Pandémie / confinement
- Défaillance fournisseur critique
- Crise géopolitique (sanctions, ruptures supply)
- Perte de personnel clé

**Bénéfices** :
- Réduction du temps d'arrêt
- Limitation des pertes financières
- Confiance des clients / investisseurs / banquiers
- Conformité (exigée pour certains secteurs / certifications)

## Étapes méthodologiques

### Étape 1, Identifier les activités critiques

Lister les processus essentiels au business :
- Production (si industrie)
- Service client (si SaaS)
- Encaissement (toutes sociétés)
- Paie (RH)
- Reporting réglementaire

Pour chaque activité critique : RTO et RPO.

- **RTO (Recovery Time Objective)** : temps maximum d'interruption acceptable
  - Ex. service client : RTO 4h
  - Ex. paie : RTO 1 semaine

- **RPO (Recovery Point Objective)** : perte de données maximum acceptable
  - Ex. transactions : RPO 0 (pas de perte)
  - Ex. mails : RPO 24h

### Étape 2, Analyser l'impact business (BIA)

Pour chaque scénario × chaque activité critique :
- Impact financier (CA perdu / coûts supplémentaires)
- Impact opérationnel (clients impactés)
- Impact réglementaire (pénalités si arrêt)
- Impact réputationnel

### Étape 3, Identifier les ressources nécessaires

- **Humaines** : qui doit être joignable et opérationnel ?
- **Techniques** : quels SI / serveurs sont critiques ?
- **Locaux** : sites de repli ?
- **Fournisseurs** : alternatives possibles ?
- **Données** : sauvegardes localisées ailleurs ?

### Étape 4, Définir les stratégies de continuité

#### Pour le SI (priorité n°1 cyber)

- Sauvegardes hors-ligne (3-2-1 : 3 copies, 2 supports, 1 hors-site)
- Réplication temps réel des données critiques
- Site de repli (datacenter secondaire ou cloud)
- Plan de récupération (DRP) testé annuellement

#### Pour les locaux

- Identification d'un site de repli (autre bureau, télétravail, flex-office)
- Procédure de bascule

#### Pour les fournisseurs

- Identification d'alternatives pour les fournisseurs critiques
- Stocks de sécurité (industrie)

### Étape 5, Documenter le plan

Sections obligatoires :
1. **Pilotage de la crise** : cellule de crise, rôles, escalade
2. **Communication** : interne (employés), externe (clients, fournisseurs, médias, autorités)
3. **Stratégies par scénario** : cyber, sinistre, pandémie...
4. **Plan de reprise par activité critique**
5. **Rôles et responsabilités**
6. **Annuaire de crise** (numéros d'urgence : DG, CFO, CTO, banque, assureur, avocat...)
7. **Procédures pas-à-pas**

### Étape 6, Tester et exercer

**Exercices annuels** au minimum :
- Tabletop (revue théorique en réunion)
- Simulation partielle (test du DRP IT par exemple)
- Simulation complète (rare mais utile pour les ETI+)

Documenter les résultats : ce qui a fonctionné, ce qui doit être amélioré.

### Étape 7, Maintenance et amélioration continue

- Revue annuelle du BCP
- Mise à jour à chaque changement majeur (réorganisation, nouvelle filiale, nouveau site)
- Intégration des leçons apprises (post-incident review)

## Cellule de crise

### Composition typique

- **Chef de crise** : DG ou délégué (décisions stratégiques)
- **CFO** : impact financier, communication banque/investisseurs
- **CTO / DSI** : si crise IT
- **DRH** : impact humain (sécurité, communication employés)
- **Communication** : externe (médias, clients, autorités)
- **Juridique** : conformité, contrats, litiges

### Activation

- Déclenchée par le chef de crise après évaluation
- Réunion immédiate (physique ou visio)
- Compte rendu obligatoire (chronologie, décisions, actions)

## Communication en crise

### Principes

- **Transparence** : ne pas minimiser
- **Rapidité** : 1ère communication < 1h après l'incident majeur
- **Cohérence** : un seul porte-parole, message validé
- **Régularité** : updates fréquents même sans nouveauté

### Audiences

- **Employés** (1ère priorité) : sécurité, instructions
- **Clients** : impact sur les services, ETA résolution
- **Fournisseurs** : impact sur les commandes
- **Banque** : si impact financier
- **Assureur** : déclaration sinistre
- **Autorités** : selon nature (CNIL si données, ANSSI si cyber, gendarmerie)
- **Médias** : si crise visible

## Cyber-spécifique

### En cas d'attaque ransomware

1. **Isoler** les systèmes infectés (déconnexion réseau)
2. **Activer cellule de crise**
3. **NE PAS PAYER la rançon** (recommandation officielle)
4. **Plainte gendarmerie** (cybergend.fr)
5. **Déclaration ANSSI** (https://www.ssi.gouv.fr)
6. **Déclaration CNIL** sous 72h si données personnelles compromises
7. **Déclaration assurance cyber** si police souscrite
8. **Communication** clients dans la transparence
9. **Restauration** depuis sauvegardes hors-ligne
10. **Post-mortem** : analyser comment l'attaquant est entré

### Acteurs publics à connaître

- **ANSSI**, Agence Nationale de la Sécurité des SI : appui technique
- **Cybermalveillance.gouv.fr** : aide aux victimes
- **C3N** : Centre de lutte contre la criminalité numérique (gendarmerie)
- **OCLCTIC** : Office central de lutte contre la criminalité liée aux TIC

## Template `bcp-plan.md`

Squelette à compléter selon votre contexte. Pas de copy-paste automatique : chaque BCP est spécifique.

## Avertissement

Le BCP est un **dispositif vivant**. Le rédiger n'a aucune valeur si on ne le **teste pas** et ne l'**actualise pas**. Pour les ETI+, faire intervenir un consultant BCM (Business Continuity Management) certifié.
