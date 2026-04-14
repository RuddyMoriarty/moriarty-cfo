# Sub-module Consolidation Groupes

Activé automatiquement si `private/company.json > classification.groupe = true`.

## Pourquoi consolider ?

Obligation légale pour les sociétés mères **quand elles dépassent 2 des 3 seuils** (art. L. 233-17 C. com.) :

| Critère | Seuil |
|---------|-------|
| Total bilan (combiné) | **30 M€** |
| Chiffre d'affaires combiné | **60 M€** |
| Effectif total | **500 salariés** |

**Exceptions** :
- Sociétés cotées : toujours obligatoire en IFRS
- Filiales françaises de groupes étrangers : peuvent être dispensées si elles sont consolidées dans les comptes du groupe mère étranger

## Référentiel applicable

| Situation | Référentiel |
|-----------|-------------|
| Groupe coté sur marché réglementé UE | **IFRS** obligatoire |
| Groupe non coté | **ANC 2020-01** (French GAAP consolidé) ou IFRS sur option |
| Sociétés d'assurance / banque | IFRS + spécificités sectorielles |

## Méthodes de consolidation

| Méthode | Quand l'utiliser | Comment |
|---------|------------------|---------|
| **Intégration globale (IG)** | Contrôle exclusif (> 50% droits de vote) | Reprise 100% des actifs/passifs, élimination capital + intérêts minoritaires |
| **Mise en équivalence (ME)** | Influence notable (20-50%) | Remplacement du titre par la quote-part de situation nette |
| **Intégration proportionnelle (IP)** | Contrôle conjoint (50/50) | ANC seulement — IFRS 11 impose la ME |

## Étapes de la consolidation

### 1. Périmètre de consolidation

Déterminer **quelles sociétés consolider** :
- Filiales contrôlées (> 50%)
- Entreprises associées (20-50%)
- Entités ad hoc (SPV, trusts) contrôlées en substance

Documenter dans `private/perimetre-consolidation.json` :
```json
{
  "societe_mere": {"siren": "...", "pourcentage_integration": 100, "methode": "mère"},
  "filiales": [
    {"siren": "...", "denomination": "...", "pourcentage_detention": 75, "methode": "IG"},
    {"siren": "...", "denomination": "...", "pourcentage_detention": 30, "methode": "ME"}
  ]
}
```

### 2. Homogénéisation des méthodes comptables

Toutes les sociétés du groupe doivent appliquer **les mêmes règles** :
- Durées d'amortissement homogènes
- Méthode de valorisation des stocks identique (CMP ou PEPS, pas de mix)
- Provisions calculées selon mêmes critères
- Revenus comptabilisés selon IFRS 15 (pour groupes IFRS)

Retraitements nécessaires pour les filiales qui dévient → journal de retraitement.

### 3. Conversion des comptes des filiales étrangères

- **Méthode du cours de clôture** : actifs/passifs au cours de clôture, P&L au cours moyen
- **Écart de conversion** : constaté en OCI (autres éléments du résultat global) en IFRS

### 4. Éliminations intercompanies (intercos)

Toutes les opérations **internes au groupe** doivent être éliminées :

**Dettes / Créances réciproques** :
```
Société A :  411 Client A sur B    100 000
Société B :  401 Fournisseur B vers A  100 000
→ Élimination : Crédit 411, Débit 401 (pour le montant identique)
```

**Ventes / Achats réciproques** :
```
CA intra-groupe : 70x vente de A à B
Achats intra-groupe : 60x achat de B chez A
→ Élimination : diminution simultanée du CA et des achats consolidés
```

**Marges internes dans les stocks** :
Si B a acheté à A des produits au prix interne 100 et qu'il lui en reste 30 en stock au 31/12, et que A vend à son prix de revient 80, il y a **20 de marge interne dans le stock B** qui doit être éliminée :
```
Débit : Résultat consolidé    20 (annulation de la marge prise par A)
Crédit : Stocks B              20 (diminution du stock au coût réel)
```

**Dividendes internes** :
Si une filiale verse des dividendes à la mère (comptabilisés en 761 produits financiers chez la mère), ils sont éliminés à la consolidation (c'est le même résultat qui circule).

### 5. Goodwill (écart d'acquisition)

**Naissance** : lors d'une acquisition, si le prix payé > quote-part de situation nette de la cible.

**Traitement** :
- **IFRS 3 / IAS 36** : **pas d'amortissement**, mais **test de dépréciation annuel** obligatoire
- **ANC 2020-01** : amortissement possible sur durée d'utilité (sinon non-amortissable + test annuel)

**Test de dépréciation** (IAS 36) :
1. Identifier les UGT (Unités Génératrices de Trésorerie)
2. Allouer le goodwill à une UGT ou un groupe d'UGT
3. Calculer la valeur recouvrable de l'UGT (DCF ou valeur de marché)
4. Si valeur recouvrable < valeur comptable → dépréciation irréversible

### 6. Segment reporting (IFRS 8)

Pour les groupes cotés, reporting obligatoire par **segment opérationnel** :
- CA par segment
- Résultat par segment
- Actifs identifiables par segment
- Réconciliation avec les états financiers consolidés

Alignement avec le reporting interne au CODIR / CEO (approche managériale).

### 7. Transfer pricing (prix de transfert)

Réglementation fiscale internationale (OCDE + art. 57 CGI) :
- Principe de **pleine concurrence** (arm's length)
- Documentation obligatoire pour les groupes > 400 M€ CA consolidé (art. 223 quinquies B CGI)
- Méthodes OCDE : CUP, RPM, Cost+, TNMM, Profit Split

**Documentation** :
- **Master File** : documentation groupe (stratégie, entités, intangibles)
- **Local File** : documentation pays par pays (transactions intra-groupe, méthode, benchmarks)
- **CbCR (Country by Country Reporting)** : obligatoire au-delà de 750 M€ CA consolidé

**Renvoi** : `cfo-fiscalite > references/transfer-pricing.md` pour l'approfondissement.

## Outils de consolidation

En v0.1 de ce skill, pas d'outil intégré (scope trop large). Renvoyer :
- **Groupes PME / ETI** : Sage X3, Cegid Y2 Consolidation, FluenceCC, Tagetik
- **Big 4** : Hyperion, SAP Business Planning and Consolidation, CCH Tagetik
- **Consolidation par Excel** : faisable en PME (< 10 filiales) mais fragile — recommander d'investir dès 3+ filiales

## Calendrier type d'une consolidation (clôture 31/12)

| Jalon | Date | Action |
|-------|------|--------|
| J+5 | 05/01 | Remontée des balances filiales |
| J+15 | 15/01 | Homogénéisation et retraitements |
| J+25 | 25/01 | Éliminations intercos + marges internes |
| J+35 | 05/02 | Goodwill + tests de dépréciation |
| J+45 | 15/02 | Segment reporting |
| J+60 | 28/02 | Comptes consolidés pré-audit |
| J+90 | 31/03 | Audit + certification CAC |

## Segment reporting et IR

Les groupes cotés doivent publier un **rapport annuel consolidé** avec :
- Comptes consolidés (bilan, compte de résultat, tableau de flux, variations de capitaux propres)
- Annexe conformément IAS 1
- Rapport de gestion consolidé
- Rapport sur le gouvernement d'entreprise
- **Rapport de durabilité CSRD** si in-scope (voir `cfo-csrd-esg`)

## Achievement

Pas d'achievement dédié consolidation en v0.1. À ajouter en v0.2 : `consolidation-champion` (+100 pts, première consolidation complète livrée).

## Adaptation par audience

**Mode EC** : vous pilotez la consolidation pour un client (mission contractuelle). Le scope et les honoraires se négocient en amont. Utiliser ce skill pour vérifier la complétude du dossier.

**Mode PME** : si vous n'avez pas d'expertise conso en interne, **sous-traiter à un cabinet spécialisé** (BDO, Mazars, Deloitte Private). La conso est un métier à part entière — ne pas la faire vous-même si plus de 3 filiales.

## Renvoi à d'autres skills

- `cfo-fiscalite` : transfer pricing détaillé
- `cfo-reporting` : segment reporting, rapport annuel consolidé
- `cfo-csrd-esg` : rapport de durabilité intégré
- `paperasse/comptable` (externe) : détails PCG pour la société mère
