# Delais de paiement et loi LME

Cadre legal des delais de paiement entre professionnels. Loi n. 2008-776 du 4 aout 2008 de modernisation de l'economie (LME), codifiee aux articles L. 441-10 et suivants du Code de commerce.

## Regles de base

### Delai maximal de droit commun (art. L. 441-10 C. com.)

Deux options au choix des parties :

| Option | Delai | Point de depart |
|--------|-------|-----------------|
| Option 1 | **60 jours** | Date d'emission de la facture |
| Option 2 | **45 jours fin de mois** | Date d'emission de la facture |

A defaut de mention dans le contrat ou les CGV, le delai legal est de **30 jours** a compter de la reception des marchandises ou de l'execution de la prestation (art. L. 441-10 al. 2 C. com.).

### Mode de calcul 45 jours fin de mois

Deux methodes courantes (a preciser dans les CGV) :

- **45 jours fin de mois** : date facture + 45 jours, puis report au dernier jour du mois en cours
- **Fin de mois + 45 jours** : dernier jour du mois de facturation + 45 jours

Exemple : facture emise le 10 mars
- 45 jours fin de mois : 10/03 + 45j = 24/04, fin de mois = **30 avril**
- Fin de mois + 45 jours : 31/03 + 45j = **15 mai**

La methode doit etre contractuellement definie. En l'absence de precision, l'administration retient l'interpretation la plus favorable au debiteur.

### Penalites de retard obligatoires (art. L. 441-10 al. 6)

| Element | Minimum legal |
|---------|---------------|
| Taux des penalites de retard | 3 x le taux d'interet legal (minimum), ou taux BCE + 10 points |
| Indemnite forfaitaire de recouvrement | 40 EUR par facture en retard |
| Exigibilite | De plein droit, sans rappel, le jour suivant la date de paiement |

Les penalites doivent figurer dans les CGV et sur les factures.

## Sanctions (art. L. 441-16 C. com.)

### Amendes administratives (DGCCRF)

| Contrevenant | Amende maximale |
|--------------|-----------------|
| Personne physique | 75 000 EUR |
| Personne morale | 2 000 000 EUR (ou 4 000 000 EUR en cas de recidive dans les 2 ans) |

L'amende est proportionnee a la gravite, la duree, le nombre de manquements, et la taille de l'entreprise.

### Publication de la decision ("name and shame")

Depuis la loi Hamon (2014), la DGCCRF peut ordonner la publication de la decision de sanction aux frais du contrevenant. La publication est systematique pour les grandes entreprises. Elle est faite sur le site de la DGCCRF et peut l'etre dans un journal d'annonces legales.

### Controleurs

La DGCCRF (Direction Generale de la Concurrence, de la Consommation et de la Repression des Fraudes) est l'autorite de controle. Elle peut effectuer des controles sur pieces ou sur place, et acceder aux factures, aux livres comptables, et aux releves bancaires.

## Delais derogatoires sectoriels

Certains secteurs beneficient de delais specifiques, inscrits a l'art. L. 441-11 C. com. :

| Secteur | Delai maximal | Base legale |
|---------|---------------|-------------|
| Transport routier de marchandises | 30 jours date d'emission de la facture | Art. L. 441-11-I, 1. C. com. |
| Location avec option d'achat | 20 jours apres le delai conventionnel | Art. L. 441-11-I, 2. |
| Produits alimentaires perissables | 30 jours apres la fin de la decadaire de livraison | Art. L. 441-11-I, 3. |
| Boissons alcooliques (vins, spiritueux) | 30 jours fin de mois apres le mois de livraison | Art. L. 441-11-I, 4. |
| Produits saisonniers non alimentaires | Delais specifiques par accord interprofessionnel | Art. L. 441-11-II |
| Activites de negoce de gros | Accord derogatoire sectoriel possible via decret | Art. L. 441-11-III |

En cas de doute sur le delai applicable, retenir le delai de droit commun (60 jours date de facture).

## Impact sur le BFR et les indicateurs de tresorerie

### DSO (Days Sales Outstanding) et DPO (Days Payable Outstanding)

Les delais LME contraignent directement le DSO et le DPO :

| Indicateur | Contrainte LME | Impact |
|------------|----------------|--------|
| DSO (delai clients) | Vos clients ne peuvent pas vous payer au-dela de 60 jours facture | DSO maximal theorique : 60 jours |
| DPO (delai fournisseurs) | Vous ne pouvez pas payer vos fournisseurs au-dela de 60 jours facture | DPO maximal theorique : 60 jours |

En pratique :

- Un DSO > 60 jours signale soit des retards de paiement clients (risque), soit des factures emises trop tot (cut-off)
- Un DPO > 60 jours expose a des sanctions DGCCRF et deteriore la relation fournisseur
- La LME compresse le BFR exploitable : on ne peut plus "tirer" sur les fournisseurs pour financer le cycle d'exploitation

### Formule BFR contraint par la LME

```
BFR contraint = (DSO_effectif x CA_jour) + (DIO x Cout_jour) - (DPO_effectif x Achats_jour)

Avec :
- DSO_effectif <= 60 jours (plafond LME)
- DPO_effectif <= 60 jours (plafond LME)
- DIO = rotation des stocks (pas contraint par la LME)
```

Si votre DSO ou DPO depasse 60 jours, le plan de tresorerie doit integrer le risque de mise en conformite (reduction forcee du DPO) ou le risque d'impayes (DSO excessif).

## Rapport annuel de l'Observatoire des delais de paiement

L'Observatoire des delais de paiement (Banque de France) publie chaque annee un rapport analysant les pratiques de paiement en France. Donnees cles du rapport 2024 :

- Delai moyen clients : 44 jours (stable)
- Delai moyen fournisseurs : 51 jours (stable)
- Les grandes entreprises restent les plus mauvais payeurs (retard moyen > 11 jours au-dela du delai contractuel)
- Les PME subissent davantage les retards qu'elles n'en infligent

Le rapport est consultable sur le site de la Banque de France.

## Bonnes pratiques de gestion des delais

### Cote clients (reduction du DSO)

| Action | Impact DSO | Complexite |
|--------|-----------|------------|
| Relances automatiques J+1, J+15, J+30 | -5 a -10 jours | Faible |
| Escompte pour paiement anticipe (ex. 2% si paiement a 10 jours) | -15 a -30 jours | Moyenne |
| Affacturage (cession de creances) | Encaissement immediat (J+2 a J+5) | Moyenne (cout 0,5% a 2% du CA affacture) |
| Scoring client et conditions de credit adaptees | Prevention | Moyenne |
| Penalites de retard effectivement appliquees | Dissuasion | Faible mais culturellement difficile |
| Facture electronique (obligatoire a partir de 2026-2027) | Reduction des litiges et accelere le paiement | A planifier |

### Cote fournisseurs (optimisation du DPO)

| Action | Impact DPO | Contrainte |
|--------|-----------|------------|
| Negocier le delai maximal legal (60 jours facture) | Maximise le DPO | Plafond LME |
| Escompte obtenu (paiement anticipe en echange de remise) | Reduit le DPO mais economise des charges | Calcul cout d'opportunite |
| Centralisation des paiements (run de paiement hebdomadaire) | Optimise la tresorerie | Discipline interne |
| Validation facture acceleree (circuit court, dematerialisation) | Evite les retards involontaires | Organisation interne |

### Affacturage et escompte

| Outil | Principe | Cout indicatif | Quand l'utiliser |
|-------|----------|----------------|------------------|
| Affacturage classique | Cession de creances clients a un factor, encaissement anticipe | 0,5% a 2% du montant cede + commission affacturage | BFR tendu, clients solides mais delais longs |
| Affacturage confidentiel | Idem mais le client ne sait pas que la creance est cedee | Un peu plus cher (prime de confidentialite) | Relation client sensible |
| Escompte commercial | Le factor escompte une traite (LCR, billet a ordre) | Taux escompte = taux bancaire + commission | Creances documentees par effet de commerce |
| Reverse factoring | Le fournisseur est paye tot par la banque du client, le client paye la banque a echeance | Variable, souvent supporte par le client | Grands donneurs d'ordres, supply chain finance |
| Dailly | Cession de creances professionnelles a la banque (bordereau Dailly) | Taux negocies selon le profil | Alternative a l'affacturage, plus souple mais moins automatisee |

## Calendrier reforme facturation electronique

La facturation electronique obligatoire (loi de finances 2024, art. 91) impactera les delais :

| Date | Obligation |
|------|------------|
| 1er septembre 2026 | Grandes entreprises et ETI : emission obligatoire via PDP ou PPF |
| 1er septembre 2027 | PME et micro-entreprises : emission obligatoire |
| A partir de 2026 | Reception de factures electroniques obligatoire pour toutes les entreprises |

La facturation electronique ameliore la tracabilite des delais et facilite le controle DGCCRF.

## Sources

- Code de commerce, art. L. 441-10 a L. 441-16 - https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000005634379/LEGISCTA000006146003/
- Loi n. 2008-776 du 4 aout 2008 de modernisation de l'economie (LME) - https://www.legifrance.gouv.fr/loda/id/JORFTEXT000019283050/
- DGCCRF, FAQ delais de paiement - https://www.economie.gouv.fr/dgccrf/Publications/Vie-pratique/Fiches-pratiques/delais-de-paiement
- Observatoire des delais de paiement, rapport annuel - https://www.banque-france.fr/fr/publications-et-statistiques/publications/rapport-annuel-de-lobservatoire-des-delais-de-paiement
- Reforme facturation electronique (art. 91 LF 2024) - https://www.economie.gouv.fr/cedef/facturation-electronique-entre-entreprises
