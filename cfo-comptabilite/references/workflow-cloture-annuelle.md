# Workflow clôture annuelle (12 étapes)

Guide complet de la clôture annuelle pour une société française à l'IS. Calqué sur la checklist de `paperasse/comptable` + enrichi pour le scope CFO (pilotage, board pack, coordination CAC).

## Étape 1, Arrêté des comptes

**Date** : jour de clôture (ex. 31/12).

**Actions** :
- Stop passage de toute transaction à compter de J+1
- Gel du logiciel comptable (ou marquage "exercice clos")
- Archivage de la balance à la date de clôture

**Output** : balance brute à la date de clôture, avant écritures d'inventaire.

## Étape 2, Rapprochement bancaire définitif

- Pour chaque compte 512, rapprocher ligne à ligne le relevé bancaire avec le grand livre
- Toute différence → écriture de régularisation (chèques à l'encaissement, virements en attente, frais bancaires oubliés)
- Obtenir le lettrage final : **solde bancaire = solde comptable** à la date de clôture

## Étape 3, Inventaire physique

**Obligatoire (L. 123-12 C. com.)** au moins une fois par an :
- Inventaire des stocks (matières, en-cours, produits finis)
- Inventaire des immobilisations (contrôle de présence + état)

**Valorisation des stocks** :
- CMP (Coût Moyen Pondéré) : méthode la plus fréquente FR
- PEPS (Premier Entré Premier Sorti) : autorisé
- LIFO : interdit en France (autorisé en fiscalité US)

## Étape 4, Écritures d'inventaire complètes

**Amortissements annuels** :
- Linéaire ou dégressif (voir `paperasse/comptable > references/amortissements.md`)
- Immobilisations incorporelles : amortir sur durée d'utilité
- Immobilisations corporelles : durée fiscale vs durée économique

**Provisions** :
- Pour risques et charges (litiges, garanties, restructuration)
- Pour dépréciation (stocks obsolètes, créances douteuses)
- Pour congés payés (méthode standard : solde CP × coût moyen + charges sociales)

**Dépréciations** :
- Test de dépréciation sur goodwill (IFRS annuel)
- Dépréciation clients douteux (> 6 mois impayé = indice fort)
- Dépréciation stocks obsolètes

## Étape 5, Écritures de cut-off annuel

Voir [cut-off-ecritures.md](cut-off-ecritures.md) pour le détail.

- **FAR** (Factures à Recevoir) : fournisseurs ayant livré mais pas encore facturé à la date de clôture
- **FNP** (Factures Non Parvenues) : variant moins strict de FAR
- **PCA** (Produits Constatés d'Avance) : produits encaissés mais non acquis à la date de clôture
- **CCA** (Charges Constatées d'Avance) : charges payées mais non consommées

## Étape 6, Régularisations fiscales

- Écarts de conversion sur devises (écart de change latent au 31/12)
- Régularisation TVA (rapprochement CA3 de décembre avec compte 445)
- Calcul et écriture des taxes assimilées (CFE, CVAE pour ETI/GE, IFER, TASCOM)

## Étape 7, Calcul IS définitif

Renvoi à `cfo-fiscalite` ou `paperasse/controleur-fiscal`.

Points clés :
- Résultat comptable → réintégrations / déductions extra-comptables
- Résultat fiscal → application du taux IS (15% taux réduit PME sur 42 500€, 25% au-delà)
- Acomptes déjà versés → solde à payer (ou crédit reportable)

## Étape 8, Écritures de répartition du résultat

Effectuée **après approbation par l'AG** (pas à la clôture elle-même) :
- Dotation à la réserve légale (5% jusqu'à 10% du capital)
- Dotation aux autres réserves (si statuts l'imposent)
- Distribution de dividendes (si décidée)
- Report à nouveau

## Étape 9, Balance définitive

Balance finale **après toutes écritures d'inventaire et de répartition** :
- Débit = Crédit (équilibre obligatoire)
- Pas de solde résiduel sur les comptes transitoires (ex. 471)
- Cohérence des comptes à zéro après répartition (ex. 120 Résultat de l'exercice → soldé)

## Étape 10, Génération FEC

Voir [liasse-fec.md](liasse-fec.md).

- Format TXT délimité (pipe `|`)
- Obligatoire : à présenter sous 15 jours sur demande DGFiP
- Pénalité : 5 000 € si non conforme
- Script : `scripts/prepare_fec_export.py`

## Étape 11, Préparation liasse fiscale

**Quelle liasse ?**
- **2033** : régime réel simplifié (petites entreprises à l'IS ou à l'IR BIC)
- **2065** : régime réel normal, sociétés à l'IS

Cases principales à remplir :
- **2050 / 2051** : Actif / Passif du bilan
- **2052 / 2053** : Compte de résultat
- **2054 / 2055** : Immobilisations + amortissements
- **2056** : Provisions
- **2057** : Créances et dettes
- **2058-A, -B, -C** : Détermination du résultat fiscal

Renvoi : `paperasse/controleur-fiscal/references/textes-fiscaux.md` pour le détail.

## Étape 12, Coordination CAC (si applicable)

Voir [coordination-cac.md](coordination-cac.md).

- Dossier de travail du CAC à constituer
- Lettre d'affirmation à signer (template `templates/lettre-affirmation-cac.md`)
- Rendez-vous CAC : explication des principales écritures atypiques
- Plan de remédiation en cas de findings

## Livrables finaux (end of exercise)

À produire dans `out/cloture-annuelle-{YYYY}/` :

```
out/cloture-annuelle-2026/
├── balance-definitive.csv
├── etats-financiers.html        → Bilan + Compte de résultat + Annexe
├── FEC-552120222-2026.txt       → Format DGFiP
├── liasse-2065-brouillon.md     → Brouillon liasse fiscale
├── lettre-affirmation-cac.pdf   → Si CAC
├── pv-approbation.md            → PV d'AG d'approbation
├── depot-greffe-checklist.md    → Checklist dépôt au greffe
└── audit-trail.log              → Trace des opérations effectuées
```

## Achievement

Débloquer `annual-close-mastered` (+75 pts) dès que la checklist 12 étapes est 100% cochée.

## Dates clés post-clôture (si clôture 31/12)

| Jalon | Date standard | Skill |
|-------|---------------|-------|
| Arrêté des comptes | 31/12 | cfo-comptabilite |
| Inventaire physique | Fin décembre / début janvier | cfo-comptabilite |
| Écritures d'inventaire | Janvier-février | cfo-comptabilite |
| Liasse fiscale + solde IS | 15/05 | cfo-fiscalite |
| FEC disponible | 15/05 (théorique) | cfo-comptabilite |
| AG d'approbation | Au plus tard 30/06 | cfo-comptabilite |
| Dépôt au greffe | 30/07 (papier) ou 30/08 (électronique) | cfo-comptabilite |
| Coordination CAC | Mars-avril (si applicable) | cfo-comptabilite |

Ce calendrier est décalé proportionnellement pour les clôtures à d'autres dates. Voir `private/calendar-fiscal.json` pour les dates absolues de votre société.

## Adaptation par audience

**Mode EC** : vocabulaire mission de présentation / examen limité / audit. Référencer NEP CNCC.

**Mode PME** : expliciter les jalons clés, renvoyer à l'EC pour les doutes, insister sur le dépôt au greffe (souvent oublié).
