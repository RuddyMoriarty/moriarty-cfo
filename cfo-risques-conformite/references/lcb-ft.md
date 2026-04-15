# Conformité LCB-FT

Lutte contre le **B**lanchiment de capitaux et le **F**inancement du **T**errorisme.

## Cadre réglementaire

- **Code monétaire et financier** (art. L. 561-1 et suivants)
- **5e Directive UE LCB-FT** (transposition 2020)
- **GAFI** (Groupe d'Action Financière), recommandations internationales
- **TRACFIN** (Service de traitement du renseignement et action contre les circuits financiers clandestins), autorité française
- **ACPR** pour les institutions financières

## Entités assujetties

### Toujours assujetties (Code mon. fin.)

- Banques, établissements de crédit, paiement, monnaie électronique
- Compagnies d'assurance, mutuelles
- Conseillers en investissement (CIF)
- Notaires, huissiers, commissaires-priseurs
- Experts-comptables (EC) inscrits à l'Ordre
- Avocats (limitations selon mission)
- Agents immobiliers
- Casinos / jeux

### Selon activité

- Sociétés de domiciliation, fiducie
- Marchands d'or et de pierres précieuses
- Marchands d'œuvres d'art > seuils
- Vendeurs / loueurs de biens à valeur élevée

### Souvent NON assujetties

- PME industrielles / commerciales standards (sauf si activité spécifique)
- Sociétés de services BtoB classiques

→ Vérifier sur le site **economie.gouv.fr/tracfin** ou via votre EC.

## Obligations

### 1. Désignation d'un responsable LCB-FT

Personne dédiée (CFO, juriste, ou externe). Formé et compétent.

### 2. Approche par les risques

Cartographie des risques LCB-FT spécifiques :
- Type de clientèle (particuliers vs entreprises, France vs international)
- Type de produits / services
- Pays d'opération (sanctions, listes noires)
- Canaux de distribution

### 3. KYC (Know Your Customer)

Identification systématique des clients :
- Personne physique : nom, prénom, date de naissance, adresse, justificatif d'identité
- Personne morale : raison sociale, SIREN, statuts, bénéficiaires effectifs (> 25%)
- **Bénéficiaire effectif** : registre obligatoire au greffe (sociétés FR depuis 2017)

### 4. Surveillance des transactions

Détection des opérations atypiques :
- Montants élevés en cash
- Virements vers / depuis paradis fiscaux
- Transactions sans logique économique apparente
- Variations soudaines de comportement client

### 5. Déclarations TRACFIN

En cas de **soupçon** (pas besoin de preuve) :
- Déclaration via portail TRACFIN
- Confidentialité absolue (interdit d'informer le client)
- Exonération de responsabilité civile et pénale

Volume FR : ~150 000 déclarations/an, dont 70% banques.

### 6. Conservation des données

5 ans après la fin de la relation d'affaires.

### 7. Formation continue

Tout le personnel concerné doit être formé annuellement.

## Sanctions en cas de manquement

- **Sanctions ACPR** (institutions financières) : avertissement → blâme → retrait d'agrément + amendes (jusqu'à 100 M€)
- **Sanctions ordinales** (EC, avocats, notaires) : avertissement → suspension → radiation
- **Pénales** : 5 ans d'emprisonnement et 375 000 € d'amende pour participation à un blanchiment

## Politique LCB-FT type

Template `templates/politique-lcb-ft.md`.

Sections :
1. Engagement de la direction
2. Désignation du responsable LCB-FT
3. Cartographie des risques LCB-FT
4. Procédures KYC
5. Surveillance des transactions
6. Déclaration TRACFIN
7. Conservation des données
8. Formation et sensibilisation
9. Contrôle interne et audit
10. Sanctions internes en cas de manquement

## Sectorial : règles spécifiques

### Banques / Paiement

- Procédures KYC renforcées (CDD, EDD)
- Filtrage transactions en temps réel (sanctions, PEP, Politically Exposed Persons)
- Reporting FATCA / CRS

### Crypto / DASP

- DASP enregistré auprès de l'AMF depuis 2020
- KYC obligatoire pour conversion crypto/fiat
- Travel Rule pour transferts > 1 000 €

### EC (experts-comptables)

- Norme professionnelle "Lutte contre le blanchiment et le financement du terrorisme" (CNCC + OEC)
- Évaluation LCB-FT du client à l'acceptation de mission
- Déclaration TRACFIN possible (pas de soupçon → pas obligatoire)

## Bonnes pratiques

- **Documenter** chaque vérification KYC (preuves : copie pièce identité, statuts, registre BE)
- **Logiciel** dédié pour les volumes importants (NameAccess, World-Check, ComplyAdvantage)
- **Audit annuel** par cabinet spécialisé pour les institutions financières
- **Veille active** sur les nouvelles obligations (5e directive UE, AMLA…)

## Avertissement

La conformité LCB-FT pour une **institution financière** est un sujet professionnel à part entière. Ce skill aide à :
- Identifier si la société est assujettie
- Comprendre les obligations de base
- Préparer une politique LCB-FT générique

**Pour la mise en œuvre opérationnelle**, consulter un avocat / consultant spécialisé.
