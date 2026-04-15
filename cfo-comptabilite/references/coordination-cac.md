# Coordination avec le Commissaire aux Comptes (CAC)

Guide pour préparer et conduire la mission d'audit légal quand elle est obligatoire.

## Quand un CAC est-il obligatoire ?

### Seuils (depuis loi PACTE 2019)

CAC obligatoire dès que **2 des 3 seuils** sont dépassés à la clôture :

| Critère | Seuil |
|---------|-------|
| Total bilan | **4 M€** |
| Chiffre d'affaires HT | **8 M€** |
| Effectif moyen | **50 salariés** |

Pour les groupes, les seuils sont appliqués aux **comptes consolidés**.

**Exceptions toujours obligatoires** :
- SA à conseil d'administration ou directoire (quel que soit le seuil)
- Sociétés cotées (dès l'introduction)
- Sociétés de taille significative appartenant à un petit groupe

### Durée du mandat

6 exercices (renouvelable). Le CAC peut être nommé :
- Par les statuts (à la constitution)
- Par l'AG (décision ultérieure)
- Par le tribunal (cas exceptionnels, nomination judiciaire)

## Les trois phases de la mission annuelle

### Phase 1, Intérim (T3 année N, typiquement sept-octobre)

Objectifs :
- Évaluer le contrôle interne
- Tests de procédures
- Identification des risques d'audit

Deliverables à préparer :
- Cartographie des risques opérationnels (renvoyer à `cfo-risques-conformite`)
- Matrice de contrôle interne (RACI, procédures clés)
- Dossier permanent à jour (statuts, procès-verbaux, conventions)

### Phase 2, Final (après clôture, janvier-mars)

Objectifs :
- Vérification des comptes annuels
- Tests de substance sur les postes significatifs
- Validation des écritures d'inventaire

Deliverables à préparer :
- Balance définitive + grand livre
- **Dossier de travail** : pour chaque poste, les justifs + le calcul (FAR/FNP/PCA/CCA, provisions, amortissements, dépréciations)
- **Lettre d'affirmation** signée par la direction (voir template)
- Échantillons de factures ventes / achats (période de cut-off ±15 jours)
- Confirmations circularisées (banques, clients, fournisseurs, avocats)

### Phase 3, Émission du rapport + AG

- Rapport général sur les comptes annuels (certification avec ou sans réserve)
- Rapport spécial sur les conventions réglementées (si applicable)
- Présentation en AG (CAC doit être présent)

## Dossier de travail EC / CFO à préparer

```
dossier-cac-exercice-YYYY/
├── 00-synthese/
│   ├── balance-definitive.csv
│   ├── etats-financiers-provisoires.pdf
│   └── note-de-synthese.md
├── 01-actif-immobilise/
│   ├── tableau-immobilisations.xlsx
│   ├── justifs-acquisitions.pdf
│   └── tests-depreciation.md
├── 02-stocks/
│   ├── inventaire-physique.pdf
│   ├── valorisation-cmp.xlsx
│   └── depreciation-stocks-obsoletes.md
├── 03-clients/
│   ├── balance-clients.xlsx
│   ├── creances-douteuses.md
│   ├── confirmations-circularisees.pdf
│   └── provisions-creances.md
├── 04-tresorerie/
│   ├── rapprochements-bancaires.pdf
│   └── confirmations-banques.pdf
├── 05-fournisseurs/
│   ├── balance-fournisseurs.xlsx
│   └── far-fnp-justifs.pdf
├── 06-capital-reserves/
│   ├── historique-capital.md
│   └── proces-verbaux-ag.pdf
├── 07-emprunts/
│   ├── tableau-emprunts.xlsx
│   └── confirmations-banques-emprunts.pdf
├── 08-fiscal/
│   ├── liasse-2065.pdf
│   ├── declarations-tva.pdf
│   └── justifs-credits-impot.pdf
├── 09-social/
│   ├── declarations-dsn.pdf
│   ├── provisions-cp-rtt.md
│   └── intéressement-participation.md
├── 10-cut-off/
│   ├── far-fnp.xlsx
│   ├── pca-cca.xlsx
│   └── tests-cut-off.md
├── 11-provisions-risques/
│   ├── provisions-litiges.md
│   └── confirmations-avocats.pdf
└── 12-lettre-affirmation/
    └── lettre-affirmation-signee.pdf
```

## Lettre d'affirmation

Document par lequel la **direction** atteste que les informations fournies au CAC sont exhaustives et sincères. **Signée par le dirigeant** au moment de l'émission du rapport.

Template : `templates/lettre-affirmation-cac.md`.

Points à affirmer systématiquement :
- Exhaustivité des comptes et opérations
- Pas d'engagement hors bilan non communiqué
- Pas de fraude connue
- Pas d'infraction significative (sociale, fiscale)
- Continuité d'exploitation non remise en cause

## Gestion des findings

En cas de remarques ou recommandations :

1. **Classification** : impact sur la certification ? (mineur, significatif, bloquant)
2. **Plan de remédiation** : action + owner + deadline pour chaque finding
3. **Suivi** en contrôle interne (reprise N+1 des findings N)

## Coordination mensuelle (au-delà du final)

Un bon CAC vient **plusieurs fois dans l'année** :
- Intérim : septembre-octobre
- Revue limitée mi-année : juillet
- Comité d'audit (si applicable) : trimestriel

Établir un **calendrier de coordination** en début d'exercice avec le CAC.

## Budget honoraires

Ordres de grandeur 2026 (indicatifs) :

| Taille société | Honoraires annuels CAC |
|---------------|------------------------|
| Seuils (8M€ CA / 50 sal) | 15 000 - 25 000 € HT |
| PME 20 M€ CA | 25 000 - 45 000 € HT |
| ETI 100 M€ CA | 50 000 - 120 000 € HT |
| ETI groupes complexes | 150 000 - 300 000 € HT |
| Groupes cotés | 500 000 € HT + |

Ces fourchettes varient selon : complexité (filiales étrangères, IFRS, CSRD), réputation du cabinet (Big 4 vs. indépendant), qualité du dossier fourni par le CFO.

## Achievement

Débloquer `audit-ready` (+60 pts) dès que la checklist dossier-cac est 100% cochée avant l'arrivée du CAC pour la phase final.

## Adaptation par audience

**Mode EC** : ce skill vous aide à préparer le dossier pour le CAC de votre client. Le CAC est alors un confrère (relation horizontale). Insister sur les NEP CNCC applicables (NEP 240 fraude, NEP 500 éléments probants, NEP 570 continuité d'exploitation).

**Mode PME** : le dirigeant fournit les justificatifs, l'EC coordonne la relation avec le CAC. Le CFO interne fait le lien opérationnel (extracts, confirmations, tests de cut-off). **Le CAC est une assurance**, bien le briefer en amont évite les surprises.

## Renvoi à d'autres skills

- `cfo-risques-conformite` : cartographie des risques, contrôle interne (entrée matière du CAC en intérim)
- `cfo-fiscalite` : préparation des explications sur la liasse fiscale et les impôts différés
- `paperasse/controleur-fiscal` (externe) : pour les détails liasse et barème pénalités
