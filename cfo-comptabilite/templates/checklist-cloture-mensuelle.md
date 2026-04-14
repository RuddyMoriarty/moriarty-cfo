# Checklist de clôture mensuelle — {MOIS} {ANNEE}

Société : **{DENOMINATION}** (SIREN {SIREN})
Objectif : clôture finalisée au **J+5 = {DATE_J5}**

## Jour 1 — Collecte (J+1)

- [ ] Télécharger tous les relevés bancaires du mois (tous comptes, toutes banques)
- [ ] Export logiciel de facturation (ventes émises sur le mois)
- [ ] Export logiciel de gestion (achats, commandes)
- [ ] Export plateforme de paie (coûts salariaux du mois)

## Jour 2 — Catégorisation (J+2)

- [ ] Catégoriser les flux bancaires non rapprochés (affectation PCG)
- [ ] Lister les achats sans facture reçue → provisions FNP à ajouter
- [ ] Lister les factures clients non encaissées sur le mois
- [ ] Acquisitions d'immobilisations → ouverture fiches d'immo

## Jour 3 — Écritures d'inventaire (J+3)

- [ ] Amortissements mensualisés (1/12 de l'annuel par immo)
- [ ] Provisions connues (primes, congés payés, litiges)
- [ ] CCA (Charges Constatées d'Avance) — assurances, loyers, licences
- [ ] PCA (Produits Constatés d'Avance) — abonnements SaaS, pré-facturation

## Jour 4 — Contrôles (J+4)

- [ ] Rapprochement bancaire : solde relevé = solde compte 512
- [ ] Pointage TVA (balance 44566 / 44571 / 4457 vs CA3 déclarée)
- [ ] Cohérence DSN / comptes 421, 431, 437
- [ ] Cut-off : aucune facture du mois suivant dans le mois courant

## Jour 5 — Finalisation (J+5)

- [ ] Balance définitive : débit = crédit, pas de solde suspect
- [ ] Top 5 variances vs N-1 identifiées et commentées
- [ ] Reporting mensuel lancé (via cfo-reporting)
- [ ] Archivage : balance CSV + journal JSON + PDF dashboard dans `out/cloture-{YYYY-MM}/`

## Synthèse

**Résultat du mois** : {MONTANT} € (+/- {PCT}% vs M-1)

**Trésorerie nette** : {MONTANT} € (+/- {DELTA} k€ vs M-1)

**Principaux points d'attention** :
- Point 1
- Point 2
- Point 3

**Prochaine échéance fiscale** : {LABEL_ECHEANCE} le {DATE_ECHEANCE} ({COULEUR})

---

Généré par moriarty-cfo / cfo-comptabilite v0.1.0
Validation recommandée : expert-comptable
