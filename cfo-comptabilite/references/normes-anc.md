# Principaux reglements ANC pour les comptes sociaux francais

Index des normes comptables francaises (French GAAP) applicables aux comptes annuels des societes commerciales. Source primaire : Autorite des Normes Comptables (ANC), anc.gouv.fr.

Ce fichier ne couvre pas les normes IFRS (comptes consolides). Pour les groupes, voir `consolidation-groupes.md`.

## Reglements fondamentaux

### ANC 2014-03 - Plan Comptable General

| Element | Detail |
|---------|--------|
| Objet | Refonte integrale du PCG, remplacant le reglement CRC 99-03 |
| Date | 5 juin 2014, entre en vigueur 1er janvier 2016 |
| Derniere consolidation | 1er janvier 2025 |
| Contenu | Structure du plan de comptes (classes 1 a 8), regles de comptabilisation, regles d'evaluation, modeles de comptes annuels |
| Application | Toutes les entites tenues d'etablir des comptes annuels conformes aux normes francaises |

Articles cles du PCG :

| Article PCG | Sujet | Ce qu'il impose |
|-------------|-------|-----------------|
| 112-2 | Image fidele | Les comptes annuels doivent donner une image fidele du patrimoine, de la situation financiere et du resultat |
| 211-1 | Actif | Definition d'un actif (element identifiable du patrimoine, avantage economique futur) |
| 212-1 | Passif | Definition d'un passif (obligation actuelle, sortie probable de ressources) |
| 214-1 a 214-27 | Amortissements | Regles de calcul, durees, modes (lineaire/degressif), composants |
| 322-1 a 322-5 | Provisions | Conditions de constitution, evaluation, reprise |
| 322-4 | Amortissement des immobilisations | Repartition systematique du montant amortissable sur la duree d'utilite |
| 332-1 | Stocks | Evaluation au cout d'acquisition ou de production |
| 513-1 a 513-5 | Comptes annuels | Bilan, compte de resultat, annexe |

### ANC 2015-06 - Immobilisations incorporelles et corporelles

| Element | Detail |
|---------|--------|
| Objet | Remplace les anciens reglements CRC 2002-10, 2004-06. Unifie le traitement des immobilisations |
| Date | 23 novembre 2015, en vigueur 1er janvier 2016 |
| Contenu cle | Definition du cout d'acquisition, traitement des couts d'emprunt, approche par composants, tests de depreciation |

Points d'attention pour le CFO :

- **Approche par composants** (art. 214-9 PCG) : obligatoire si les composants ont des durees d'utilite significativement differentes
- **Couts d'emprunt** : option d'activation dans le cout de production (art. 213-9 PCG)
- **Depreciation** : test de depreciation obligatoire si indice de perte de valeur (art. 214-17 PCG)
- **Amortissement derogatoire** : ecart entre amortissement fiscal et comptable comptabilise en provision reglementee (compte 145)

### ANC 2023-01 - Modernisation des etats financiers

| Element | Detail |
|---------|--------|
| Objet | Reforme de la presentation du bilan, du compte de resultat et de l'annexe |
| Date | Homologue le 26 decembre 2023 |
| Entree en vigueur | Exercices ouverts a compter du 1er janvier 2025 |
| Impact principal | Nouveau modele de compte de resultat, suppression du resultat exceptionnel remplace par "operations inhabituelles", annexe simplifiee pour les petites entites |

Changements majeurs :

| Avant (PCG classique) | Apres (ANC 2023-01) |
|-----------------------|---------------------|
| 3 niveaux de resultat : exploitation, financier, exceptionnel | 2 niveaux : operationnel (courant + inhabituel), financier |
| Comptes 67x/77x "exceptionnel" | Reclasses en resultat operationnel sous rubrique "Operations inhabituelles" |
| Annexe longue et narrative | Annexe allegee pour les petites entites (art. L. 123-16 C. com.) |
| Pas de tableau de flux obligatoire en comptes sociaux | Toujours pas obligatoire, mais recommande |

## Regles de provisions (PCG art. 322-1 et suivants)

### Conditions de comptabilisation

Une provision est comptabilisee lorsque les **trois conditions cumulatives** sont remplies (art. 322-1 PCG) :

1. L'entite a une obligation actuelle (juridique ou implicite) resultant d'un evenement passe
2. Il est probable qu'une sortie de ressources sera necessaire pour eteindre l'obligation
3. Le montant peut etre estime de maniere fiable

### Types de provisions

| Type | Comptes | Exemples |
|------|---------|----------|
| Provisions pour risques | 151x | Litiges (1511), garanties donnees (1512), pertes de change (1515) |
| Provisions pour charges | 153x, 154x, 155x | Pensions (153), restructurations (154), impots (155) |
| Provisions pour depreciation d'actifs | 29x, 39x, 49x | Depreciation immobilisations, stocks, creances |

### Evaluation

- Au montant correspondant a la **meilleure estimation** de la sortie de ressources (art. 322-5 PCG)
- Actualisation si l'effet est significatif et la date de sortie fiable
- Revision a chaque cloture : ajustement ou reprise si les conditions ne sont plus remplies

## Regles d'amortissement (PCG art. 214-1 a 214-27)

| Regle | Reference | Detail |
|-------|-----------|--------|
| Duree d'amortissement | Art. 214-1 | Duree d'utilite reelle (pas necessairement la duree fiscale) |
| Mode lineaire | Art. 214-4 | Mode par defaut si le rythme de consommation est regulier |
| Mode degressif | CGI art. 39 A-1 | Option fiscale (coefficients 1,25 / 1,75 / 2,25 selon duree) |
| Amortissement derogatoire | Art. 214-27 | Ecart entre amort. fiscal et comptable en provision reglementee |
| Valeur residuelle | Art. 214-6 | Deduite de la base amortissable si significative et mesurable |
| Composants | Art. 214-9 | Amortissement separe si durees d'utilite differentes et significatives |

### Durees d'amortissement usuelles (comptable / fiscal)

| Bien | Duree comptable | Duree fiscale admise |
|------|-----------------|---------------------|
| Logiciels | 1 a 3 ans | 12 mois (amort. exceptionnel CGI art. 236-II) |
| Brevets | Duree de protection | 5 ans minimum fiscal |
| Constructions | 20 a 50 ans | 20 a 50 ans |
| Materiel industriel | 5 a 10 ans | 5 a 10 ans (degressif possible) |
| Materiel de bureau / informatique | 3 a 5 ans | 3 a 5 ans |
| Vehicules | 4 a 5 ans | 4 a 5 ans (plafond fiscal amort. VP) |
| Mobilier | 10 ans | 10 ans |

## Differences cles French GAAP vs IFRS

Pour les societes qui publient des comptes sociaux en normes francaises et des comptes consolides en IFRS :

| Sujet | French GAAP (PCG) | IFRS |
|-------|-------------------|------|
| Immobilisations incorporelles | Activation possible du fonds commercial (non amorti sauf depreciation) | IAS 38 : goodwill non amorti, test annuel de depreciation obligatoire |
| Contrats de location | Pas de distinction financement/operationnel au bilan (sauf credit-bail inscrit) | IFRS 16 : tous les contrats >12 mois au bilan (droit d'utilisation + dette) |
| Provisions reglementees | Existent (amort. derogatoire, provisions pour hausse des prix) | N'existent pas en IFRS (pas de notion fiscale dans les etats financiers) |
| Resultat exceptionnel | Existait avant 2025, remplace par "operations inhabituelles" (ANC 2023-01) | N'existe pas. Reclasse en resultat operationnel ou financier |
| Ecarts de conversion | Passif au bilan (476/477), pas d'impact resultat sauf provision pour perte de change | IAS 21 : impact resultat pour les elements monetaires |
| Evaluation des stocks | CUMP ou FIFO (art. 333-2 PCG), LIFO interdit | IAS 2 : CUMP ou FIFO, LIFO interdit |
| Frais de R&D | Option d'activation si conditions reunies (art. 212-3 PCG) | IAS 38 : recherche = charge, developpement = activation si 6 criteres |
| Contrats long terme | Methode a l'achevement ou avancement (art. 380-1 PCG) | IFRS 15 : avancement obligatoire (5 etapes) |
| Instruments financiers | Cout historique (pas de juste valeur pour les comptes sociaux) | IFRS 9 : juste valeur par resultat ou OCI selon classification |
| Credit-bail | Hors bilan (redevances en charges) sauf information en annexe | IFRS 16 : au bilan (droit d'utilisation et dette de loyer) |

## Autres reglements ANC utiles au CFO

| Reglement | Objet | Impact |
|-----------|-------|--------|
| ANC 2014-05 | Comptabilisation des titres | Evaluation initiale, depreciation, cession des titres immobilises et de placement |
| ANC 2015-05 | Instruments financiers a terme | Comptabilisation des couvertures de change et de taux (swaps, options) |
| ANC 2018-01 | Comptes consolides | Methodes de consolidation (integration globale, MEE, proportionnelle) pour les comptes de groupe |
| ANC 2018-06 | Engagements de retraite | Evaluation des engagements (methode actuarielle), information en annexe |
| ANC 2019-09 | Chiffre d'affaires et contrats | Comptabilisation du CA selon la methode de l'achevement ou de l'avancement |

## Obligations annexes selon la taille de l'entite

Le PCG et les reglements ANC prevoient des obligations modulees selon la taille :

| Critere | Micro-entite | Petite entite | Entite moyenne/grande |
|---------|-------------|---------------|----------------------|
| Seuils (C. com. D. 123-200) | CA < 900 000 EUR, bilan < 450 000 EUR, < 10 salaries | CA < 12 M EUR, bilan < 6 M EUR, < 50 salaries | Au-dessus des seuils petite entite |
| Bilan | Abrege | Abrege | Complet |
| Compte de resultat | Abrege | Abrege | Complet |
| Annexe | Dispensee | Simplifiee | Complete |
| Rapport de gestion | Dispense (sauf si SA/SCA) | Requis | Requis |
| Commissaire aux comptes | Non obligatoire (sauf seuils specifiques) | Selon seuils | Obligatoire si 2 seuils sur 3 depasses |

## Regles de depreciation (art. 214-15 a 214-20 PCG)

Les depreciations se distinguent des provisions et des amortissements :

- **Amortissement** : repartition systematique de la valeur d'un actif sur sa duree d'utilite (perte de valeur previsible et irreversible)
- **Depreciation** : perte de valeur d'un actif au-dela de l'amortissement, liee a un indice de perte de valeur (reversible)
- **Provision** : passif dont l'echeance ou le montant est incertain (obligation actuelle)

Test de depreciation :

1. A chaque cloture, verifier s'il existe des indices de perte de valeur (marche, technologie, obsolescence, sous-utilisation)
2. Si indice : comparer la valeur nette comptable a la valeur actuelle (plus elevee entre la valeur venale et la valeur d'usage)
3. Si VNC > valeur actuelle : comptabiliser une depreciation (compte 29x en contrepartie du compte 68x)
4. Si recuperation ulterieure : reprise de depreciation (compte 78x)

## Sources

- ANC, Reglement n. 2014-03 du 5 juin 2014 relatif au plan comptable general (consolide) - https://www.anc.gouv.fr/normes-francaises/le-plan-comptable-general
- ANC, Reglement n. 2015-06 du 23 novembre 2015 relatif aux immobilisations - https://www.anc.gouv.fr/normes-francaises/reglements-anc
- ANC, Reglement n. 2023-01 du 29 juin 2023, homologue le 26 decembre 2023 - https://www.anc.gouv.fr/normes-francaises/reglements-anc
- Code de commerce, art. L. 123-12 a L. 123-28
- Code de commerce, art. D. 123-200 (seuils de taille des entites)
- CGI art. 39 A-1 (amortissement degressif), art. 236-II (amortissement exceptionnel logiciels)
