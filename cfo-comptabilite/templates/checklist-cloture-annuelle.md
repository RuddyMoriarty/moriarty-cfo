# Checklist de clôture annuelle — Exercice {ANNEE}

Société : **{DENOMINATION}** (SIREN {SIREN})
Date de clôture : **{DATE_CLOTURE}**
Échéances clés (dérivées du calendrier fiscal) :
- Liasse fiscale : **{DATE_LIASSE}**
- FEC disponible : **{DATE_FEC}**
- AG d'approbation : **au plus tard {DATE_AG}**
- Dépôt au greffe : **{DATE_GREFFE}**

## Phase 1 — Arrêté des comptes et inventaire

- [ ] **Étape 1** : Arrêté des comptes à la date de clôture (gel du logiciel comptable)
- [ ] **Étape 2** : Rapprochement bancaire définitif (solde relevé = grand livre)
- [ ] **Étape 3** : Inventaire physique
  - [ ] Stocks (matières, en-cours, produits finis)
  - [ ] Immobilisations (contrôle présence + état)

## Phase 2 — Écritures d'inventaire et régularisations

- [ ] **Étape 4** : Écritures d'inventaire complètes
  - [ ] Amortissements annuels (linéaire / dégressif)
  - [ ] Provisions pour risques et charges
  - [ ] Dépréciations (stocks, clients douteux, goodwill)
  - [ ] Provisions pour CP / RTT (solde × coût moyen × 1.45)
- [ ] **Étape 5** : Écritures de cut-off
  - [ ] FAR / FNP (fournisseurs livrés sans facture reçue)
  - [ ] PCA (produits encaissés non acquis)
  - [ ] CCA (charges payées non consommées)
  - [ ] Intérêts courus
- [ ] **Étape 6** : Régularisations fiscales
  - [ ] Écarts de conversion sur devises
  - [ ] Rapprochement TVA CA3 décembre vs compte 445
  - [ ] Taxes assimilées (CFE, CVAE si ETI+, IFER, TASCOM)
- [ ] **Étape 7** : Calcul IS définitif
  - [ ] Passage résultat comptable → résultat fiscal (réintégrations / déductions)
  - [ ] Taux IS (15% réduit PME / 25% normal)
  - [ ] Imputation acomptes + crédits d'impôt (CIR, CII)

## Phase 3 — Consolidation (si groupe)

- [ ] **Étape 7b** : Comptes consolidés (si `classification.groupe = true`)
  - [ ] Homogénéisation des méthodes
  - [ ] Retraitements IFRS (si IFRS)
  - [ ] Éliminations intercos (dettes/créances, ventes/achats, marges internes, dividendes)
  - [ ] Goodwill + test de dépréciation
  - [ ] Segment reporting (IFRS 8)

## Phase 4 — Livrables fiscaux

- [ ] **Étape 8** : Écritures de répartition du résultat (après AG)
  - [ ] Dotation réserve légale
  - [ ] Dotation autres réserves
  - [ ] Dividendes (si décidés)
  - [ ] Report à nouveau
- [ ] **Étape 9** : Balance définitive (après toutes écritures)
- [ ] **Étape 10** : Génération FEC (script `prepare_fec_export.py`)
  - [ ] Format TXT 18 colonnes, pipe ou tabulation
  - [ ] Nom : `{SIREN}FEC{AAAAMMJJ}.txt`
  - [ ] Validation : équilibre, séquence, encodage UTF-8
- [ ] **Étape 11** : Préparation liasse fiscale
  - [ ] Formulaire adapté : 2033 (réel simplifié) / 2065 (réel normal IS)
  - [ ] Toutes les cases remplies (2050-2058)
  - [ ] Cohérence FEC ↔ liasse (total débit = total crédit, résultat identique)

## Phase 5 — Audit et transmission

- [ ] **Étape 12** : Coordination CAC (si obligatoire)
  - [ ] Dossier de travail constitué (cf. `references/coordination-cac.md`)
  - [ ] Lettre d'affirmation signée
  - [ ] Rendez-vous CAC tenus (intérim + final)
  - [ ] Findings remédiés (si applicable)
- [ ] AG d'approbation organisée (dans les 6 mois)
- [ ] Dépôt des comptes au greffe (dans le mois suivant l'AG, ou 2 mois si électronique)
- [ ] Télétransmission TDFC de la liasse (par l'EC)

## Livrables finaux (à archiver dans `out/cloture-annuelle-{YYYY}/`)

- [ ] `balance-definitive.csv`
- [ ] `etats-financiers.html` (Bilan + CR + Annexe)
- [ ] `FEC-{SIREN}-{YYYY}.txt`
- [ ] `liasse-{2033|2065}-brouillon.md`
- [ ] `lettre-affirmation-cac.pdf` (si applicable)
- [ ] `pv-approbation.md`
- [ ] `depot-greffe-checklist.md`
- [ ] `audit-trail.log`

## Synthèse

**Résultat net de l'exercice** : {MONTANT} €
**Impôt sur les sociétés** : {MONTANT_IS} €
**Taux effectif d'imposition** : {PCT_EFFECTIF}%

**Principaux ajustements extra-comptables** :
- Réintégration 1 : {MONTANT} €
- Déduction 1 (CIR) : {MONTANT} €

**Points à signaler en AG** :
- Point 1
- Point 2

---

Généré par moriarty-cfo / cfo-comptabilite v0.1.0
Validation CAC : {OUI/NON}
Télétransmission TDFC : {FAITE/A_FAIRE} le {DATE}
