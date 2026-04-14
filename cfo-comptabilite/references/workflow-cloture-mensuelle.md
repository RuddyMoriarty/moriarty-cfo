# Workflow clôture mensuelle J+5

Objectif : produire une clôture comptable mensuelle fiable en 5 jours ouvrés maximum après la fin du mois. C'est le **standard attendu pour une PME+**.

## Pourquoi J+5

- 40% du temps d'un CFO est sur le reporting (cf. `data/cfo-job-corpus.json`)
- Un reporting mensuel en J+15 est trop tard pour piloter
- Les investisseurs / le board attendent la clôture en M+5 à M+7

Pour les TPE, J+10 est acceptable. Pour les ETI, J+3 est souvent exigé (reporting trimestriel au board).

## Checklist J+5 (15 points)

Template complet dans `templates/checklist-cloture-mensuelle.md`.

### Jour 1 (J+1) — Collecte

- [ ] Télécharger tous les relevés bancaires du mois (tous comptes, toutes banques)
- [ ] Export logiciel de facturation (ventes émises)
- [ ] Export logiciel de gestion (commandes, achats validés)
- [ ] Export plateforme de paie (coûts salariaux du mois)

### Jour 2 (J+2) — Catégorisation

- [ ] Catégoriser les flux bancaires non rapprochés → affectation PCG
- [ ] Vérifier les lignes d'achat sans facture reçue → provisionner en FNP
- [ ] Vérifier les factures clients non encaissées → PCA si échéance au-delà du mois
- [ ] Consolider les achats d'immobilisations → ouverture fiches d'immo

### Jour 3 (J+3) — Écritures d'inventaire mensualisées

- [ ] Amortissements du mois (1/12 de l'amortissement annuel)
- [ ] Provisions connues (primes, congés payés, litiges)
- [ ] Charges constatées d'avance (CCA) — assurances, loyers, licences
- [ ] Produits constatés d'avance (PCA) — abonnements SaaS, pré-facturation

### Jour 4 (J+4) — Contrôles

- [ ] Rapprochement bancaire complet — balance = grand livre
- [ ] Pointage TVA (balance TVA déductible vs TVA collectée vs comptes 445)
- [ ] Contrôle cohérence DSN du mois précédent avec comptes 421, 431, 437
- [ ] Vérification cut-off : date de facture ≤ dernier jour du mois ?

### Jour 5 (J+5) — Finalisation

- [ ] Balance définitive du mois (débit = crédit, pas de solde suspect)
- [ ] Top 5 variances vs N-1 identifiées et commentées
- [ ] Reporting généré (appel à `cfo-reporting`)
- [ ] Archivage : balance CSV + journal JSON + PDF dashboard dans `out/cloture-YYYY-MM/`

## Format de sortie

```markdown
# Clôture mensuelle {YYYY-MM}

## Faits
- Société : {denomination} (SIREN {siren})
- Période : du {debut} au {fin}
- Échéance J+5 : {date_j5} ({couleur} — reste {X} jours)

## Hypothèses
- H1 : Pas de transaction passée après {date_fin_mois} (cut-off)
- H2 : Factures fournisseurs reçues : {N} sur {N_total_attendu} → FNP provisionnés
- H3 : Taux d'activité du mois : {heures_prod / heures_contrat}

## Analyse

### KPIs flash
- CA HT : {XX} k€ (+/- {pct}% vs M-1, +/- {pct}% vs budget)
- Marge brute : {pct}% ({+/-} pts vs N-1)
- EBITDA : {XX} k€ ({pct}% du CA)
- BFR : {XX} k€ ({+/-} k€ vs M-1)
- Trésorerie nette : {XX} k€

### Top 3 variances vs budget
1. [Variance 1 — commentaire]
2. [Variance 2 — commentaire]
3. [Variance 3 — commentaire]

## Risques

🟠 {Risque 1 — description + mitigation}
🟡 {Risque 2}

## Actions

- [ ] Transmettre balance à l'EC pour validation des écritures d'inventaire
- [ ] Lancer `cfo-reporting` pour produire le board pack M+5
- [ ] Relancer le top 3 créances clients > 60 jours
- [ ] Préparer l'acompte TVA du {date_echeance} ({lien cfo-fiscalite})

## Limites

Cette clôture mensuelle est un outil de pilotage interne. Les écritures restent
à valider par votre expert-comptable. En cas de contrôle, les écritures définitives
doivent être cohérentes avec la balance annuelle finale.
```

## Erreurs fréquentes à éviter

| Erreur | Symptôme | Correction |
|--------|----------|------------|
| Cut-off raté | Des factures du mois suivant comptées dans le mois | Filtrer strictement sur `date_facture <= date_fin_mois` |
| Double comptabilisation | Balance qui déborde de 10-20% | Vérifier que l'extract bancaire n'est pas réimporté deux fois |
| FNP oubliés | Résultat trop élevé, puis chute en M+1 | Systématiser l'écriture FNP sur ce qu'on sait devoir payer |
| Amortissements non mensualisés | Résultat annuel correct mais mensualité fausse | Diviser l'amortissement annuel par 12 et l'écrire chaque mois |
| TVA non pointée | Acomptes TVA incorrects | Comparer solde compte 44566/44571 avec déclarations |

## Adaptation par audience

**Mode EC** : utiliser le vocabulaire mission OEC → "chronique du mois", "revue des cut-off" (NEP 200 — contrôle de l'exhaustivité).

**Mode PME** : insister sur les 3 KPIs flash, ne pas charger en écritures techniques. Renvoyer à l'EC pour les doutes sur les FAR/FNP.

## Orchestration avec les autres skills

- `cfo-reporting` : prend la relève pour produire le pack mensuel (dashboard HTML + PDF)
- `cfo-tresorerie` : reçoit la balance pour affiner la prévision 13w
- `cfo-controle-gestion` : utilise les données pour l'analyse de rentabilité produit/client
- `paperasse/comptable` (externe) : pour le détail PCG si écriture atypique
