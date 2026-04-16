# Ratios sectoriels Banque de France - FIBEN et OPALE

## Objet

La Banque de France collecte et publie des ratios financiers sectoriels a partir des bilans deposes par les entreprises francaises. Ces donnees permettent d'ancrer les KPIs d'un controle de gestion sur des benchmarks objectifs plutot que sur des estimations internes.

Deux bases principales :

| Base | Contenu | Perimetre |
|------|---------|-----------|
| **FIBEN** (Fichier Bancaire des Entreprises) | Ratios financiers, cotation credit, donnees bilans | Entreprises dont le CA > 750 000 EUR (environ 300 000 entreprises) |
| **OPALE** (Observatoire des PME et des entreprises de taille intermediaire) | Statistiques agregees par secteur NAF | PME et ETI, ventilation par code NAF rev. 2 |

---

## Ce que FIBEN mesure

FIBEN calcule des ratios a partir des liasses fiscales (bilans et comptes de resultat) deposees aupres des greffes. Les ratios sont ventiles par **code NAF** (niveau 2, 3 ou 4 selon la granularite disponible).

### Principales familles de ratios

| Famille | Ratios types | Unite |
|---------|-------------|-------|
| **Rentabilite** | Taux de marge nette, rentabilite economique (ROA), rentabilite des capitaux propres (ROE), EBE/CA | % |
| **Endettement** | Taux d'endettement (dettes financieres/capitaux propres), leverage, capacite de remboursement (dettes financieres/CAF) | ratio ou annees |
| **Liquidite** | Ratio de liquidite generale (AC/PC), ratio de liquidite reduite, tresorerie nette/CA | ratio ou % |
| **Rotation** | Delai clients (DSO), delai fournisseurs (DPO), rotation des stocks, BFR/CA | jours ou % |
| **Structure** | Fonds de roulement/CA, immobilisations/total bilan, capitaux propres/total bilan | % |

### Distribution statistique

Pour chaque ratio, FIBEN fournit generalement :

- **1er quartile** (Q1) - 25e percentile
- **Mediane** (Q2) - 50e percentile
- **3e quartile** (Q3) - 75e percentile
- Parfois : **1er decile** (D1) et **9e decile** (D9)

---

## Comment acceder aux donnees

### 1. Statistiques publiques (acces libre)

La Banque de France publie des etudes sectorielles gratuites sur son site :

- **Stat Info** : series statistiques sur les entreprises (delais de paiement, taux de marge, defaillances)
- **Bulletin de la Banque de France** : analyses macroeconomiques incluant des donnees sectorielles
- URL : `https://www.banque-france.fr/statistiques/chiffres-cles-france-et-etranger/entreprises`

### 2. Cotation Banque de France (acces restreint)

La cotation Banque de France est attribuee a chaque entreprise FIBEN. Elle comprend :

| Element | Description |
|---------|-------------|
| **Cote d'activite** | Lettre de A a N selon le CA (A = CA > 750 M EUR, N = CA < 750 K EUR) |
| **Cote de credit** | Echelle de 3++ (excellent) a 9 (compromis), P = procedure collective |

L'acces a la cotation individuelle est reserve aux etablissements de credit et aux entreprises elles-memes (droit d'acces via i-FIBEN).

### 3. Base OPALE

OPALE est un outil d'analyse financiere de la Banque de France. Il permet de situer une entreprise par rapport a son secteur. L'acces se fait :

- Via les **succursales departementales** de la Banque de France
- Sur rendez-vous, pour les dirigeants d'entreprise (gratuit)
- Le dirigeant peut demander un **diagnostic financier** comparatif

---

## Utilite pour le controle de gestion

### Ancrer les KPIs sur des references objectives

| Usage | Methode |
|-------|---------|
| Fixer un objectif de marge | Comparer la marge nette de l'entreprise au Q3 du secteur NAF |
| Evaluer le BFR | Comparer DSO et DPO aux medianes sectorielles |
| Negocier avec les banques | Connaitre sa cotation et les ratios attendus pour une cote de credit donnee |
| Preparer un business plan | Justifier les hypotheses financieres par des benchmarks sectoriels |
| Alerter sur les derives | Signaler quand un ratio passe sous le Q1 sectoriel |

### Exemple d'utilisation

Pour une PME en code NAF 62.01Z (Programmation informatique) :

1. Recuperer les medianes sectorielles (marge nette, BFR/CA, taux d'endettement)
2. Positionner l'entreprise sur chaque ratio par rapport aux quartiles
3. Identifier les ecarts significatifs (> 1 quartile d'ecart)
4. Definir les objectifs de progression en ciblant la mediane ou le Q3

---

## Mises en garde

- **Les ratios sont des medianes sectorielles, pas des cibles.** Une entreprise en forte croissance peut legitimement avoir un BFR superieur a la mediane.
- **Le code NAF est declaratif.** Certaines entreprises sont mal classees, ce qui peut biaiser les comparaisons.
- **Les donnees FIBEN ne couvrent que les entreprises > 750 K EUR de CA.** Les TPE ne sont pas representees.
- **Decalage temporel.** Les ratios publies portent sur l'exercice N-1 ou N-2 (delai de depot et de traitement des liasses).
- **Effet taille.** Au sein d'un meme code NAF, les ratios varient significativement entre PME et ETI. Privilegier les comparaisons a taille comparable.
- **Les ratios FIBEN sont calcules sur la base des comptes sociaux**, pas des comptes consolides. Pour les groupes, les ratios individuels peuvent etre trompeurs.

---

## Ratios cles par grande categorie (ordres de grandeur medianes - tous secteurs confondus)

Ces valeurs sont indicatives et varient fortement selon le secteur NAF :

| Ratio | Mediane indicative tous secteurs | Interpretation |
|-------|----------------------------------|----------------|
| Marge nette | 2 a 5 % | Tres variable selon le secteur (services vs industrie) |
| ROE | 8 a 15 % | Rentabilite des fonds propres |
| Taux d'endettement | 60 a 120 % | Dettes financieres / capitaux propres |
| Capacite de remboursement | 3 a 5 ans | Dettes financieres / CAF |
| DSO (delai clients) | 40 a 60 jours | Art. L. 441-10 C. com. : plafond legal 60 jours |
| DPO (delai fournisseurs) | 45 a 65 jours | Art. L. 441-10 C. com. : plafond legal 60 jours |
| BFR/CA | 5 a 25 % | Tres variable (negatif dans la grande distribution) |
| Liquidite generale | 1,1 a 1,5 | Actif circulant / Passif circulant |

---

## Ratios par grands secteurs (medianes indicatives - objectifs climat et 2)

A titre d'illustration, voici des ordres de grandeur par grands secteurs. Ces chiffres sont des approximations ; les valeurs exactes sont disponibles dans les publications Stat Info de la Banque de France.

| Secteur (NAF) | Marge nette | Taux d'endettement | BFR/CA | DSO (jours) |
|---------------|------------|-------------------|--------|-------------|
| Commerce de detail (47) | 1 a 3 % | 80 a 150 % | -5 a 5 % | 5 a 15 |
| Industrie manufacturiere (10-33) | 2 a 5 % | 60 a 100 % | 15 a 30 % | 50 a 70 |
| Construction (41-43) | 2 a 4 % | 50 a 90 % | 10 a 25 % | 60 a 80 |
| Services informatiques (62) | 4 a 8 % | 30 a 70 % | 10 a 20 % | 50 a 70 |
| Hebergement-restauration (55-56) | 1 a 4 % | 100 a 200 % | -10 a 0 % | 5 a 15 |
| Transport et entreposage (49-53) | 1 a 3 % | 80 a 150 % | 5 a 15 % | 40 a 60 |
| Activites de conseil (70) | 5 a 10 % | 20 a 60 % | 5 a 20 % | 45 a 65 |

**Rappel :** ces chiffres sont des ordres de grandeur. Toujours se referer aux publications officielles de la Banque de France pour des donnees actualisees et ventilees par code NAF precis.

---

## Sources

- Banque de France - Statistiques entreprises : `https://www.banque-france.fr/statistiques/chiffres-cles-france-et-etranger/entreprises`
- Banque de France - FIBEN : `https://www.banque-france.fr/stabilite-financiere/cotation-des-entreprises`
- Banque de France - Delais de paiement (Stat Info) : `https://www.banque-france.fr/publications-et-statistiques/statistiques/stat-info`
- Banque de France - Diagnostics en succursale : `https://particuliers.banque-france.fr/votre-banque-de-france/nos-services-aux-entreprises`
- Code de commerce, art. L. 441-10 (delais de paiement) : `https://www.legifrance.gouv.fr`
