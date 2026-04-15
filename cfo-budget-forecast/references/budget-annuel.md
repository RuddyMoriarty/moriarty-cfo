# Budget annuel, méthodologie

Le budget annuel est l'engagement chiffré de la direction pour l'année à venir. Il sert de base au reporting mensuel (variance analysis) et à la communication externe (board, investisseurs, banquiers).

## Calendrier type (clôture 31/12)

| Mois | Action |
|------|--------|
| **Oct N-1** | Cadrage stratégique par le CODIR (objectifs CA, marge, EBITDA) |
| **Nov N-1** | Remontée bottom-up des besoins (OPEX, RH, CAPEX par BU / CdC) |
| **Déc N-1** | Consolidation + arbitrages + validation board |
| **Jan N** | Communication aux équipes, mise en place en compta, premier reporting |

Pour les clôtures autres que 31/12, décaler proportionnellement.

## Structure standard d'un budget annuel

### 1. Cadrage stratégique (top-down)

Le CODIR fixe :
- Objectif de CA : croissance X% vs N-1 (ou valeur absolue)
- Objectif de marge EBITDA : X% du CA
- Objectif d'effectif : N → N+X
- Objectif de CAPEX : M€ total

### 2. Budget P&L (bottom-up + top-down)

**Produits (Classe 7)** :
- Budget CA par segment / produit / canal / client majeur
- Justifier le mix et la croissance
- Validation commerciale (le VP Sales signe)

**Charges (Classe 6)** :
- **60 Achats** : selon hypothèse d'activité (COGS % du CA)
- **61 Services extérieurs** : sous-traitance, loyers
- **62 Autres services** : honoraires, déplacements, formations
- **63 Impôts et taxes** : CFE, taxe d'apprentissage, etc.
- **64 Salaires** : effectif × salaire moyen + charges + NAO + recrutements
- **65 Autres charges** : licences, abonnements
- **68 Dotations** : amortissements selon plan d'immo

### 3. Budget bilan

Projection des postes principaux :
- Immobilisations : +CAPEX -amortissements -cessions
- Stocks : selon ratio DIO × CA
- Créances clients : selon ratio DSO × CA TTC
- Dettes fournisseurs : selon ratio DPO × achats TTC
- Capitaux propres : CP N-1 + RN - dividendes
- Dettes financières : tableau emprunts existants + nouvelles facilités prévues

### 4. Budget cash flow (tableau de flux de trésorerie)

Méthode **indirecte** :
```
CAF =                             RN + DAP - PNVC + Reprises - Transferts
Cash flow d'exploitation =        CAF - Variation BFR
Cash flow d'investissement =      - CAPEX + Cessions
Cash flow de financement =        + Emprunts - Remboursements + Augmentations capital - Dividendes
Variation trésorerie =            Σ des trois ci-dessus
```

### 5. Mensualisation

Le budget annuel est **ventilé par mois** selon :
- Saisonnalité historique (ex. commerce : pic décembre)
- Événements non récurrents connus (ex. nouveau produit lancé en mai)
- Jours ouvrés du mois (pour les coûts liés à l'activité)

## Bonnes pratiques

### DO
- **Baser sur le réel N-1** comme point de départ (pas une feuille blanche)
- **Challenger chaque ligne** (pourquoi +X% sur ce poste ?)
- **Documenter les hypothèses** clés (nouveau client attendu, prix matière en hausse, recrutement planifié)
- **Timer les hypothèses** (quand le nouveau contrat démarre, pas juste "dans l'année")
- **Faire valider par le CODIR** avant la remontée board

### DON'T
- Copier-coller N-1 avec +5% sans challenge
- Ignorer les engagements externes connus (renouvellements de contrats, hausse loyers indexée)
- Faire un budget "optimiste" pour plaire au board (crédibilité détruite en 3 mois)
- Oublier les coûts de compliance / légal / audit (souvent sous-estimés)
- Bâcler la partie cash flow (le plus important !)

## Script `budget_builder.py`

Génère un squelette de budget annuel à partir de :
- P&L réel N-1 (CSV)
- Hypothèses simples (croissance CA, taux de marge cible, CAPEX, recrutements)

Output : CSV avec 12 colonnes mensuelles + total annuel.

## Ajustement du budget en cours d'année

- **T1 ou T2** : si dérive significative, proposer un **budget révisé** au board (plutôt que de persister sur un budget irréaliste)
- **T3-T4** : rolling forecast plutôt que budget révisé (moins formel)

## Intégration avec les autres skills

- Utilise les données réelles N-1 de `cfo-reporting`
- Génère les prévisions utilisées par `cfo-tresorerie` (forecast 12 mois)
- Alimente les scénarios de `cfo-budget-forecast` lui-même (cohérence interne)
- Compare vs réel via variance analysis dans `cfo-controle-gestion`

## Achievement

`budget-builder` (+50 pts) au 1er budget annuel construit.
