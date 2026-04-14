# Template Budget Annuel — format markdown (à exporter vers Excel)

Structure standard pour un budget annuel mensualisé avec 3 scénarios.

## Onglet 1 : Hypothèses

| Hypothèse | Optimiste | Réaliste | Pessimiste |
|-----------|-----------|----------|------------|
| Croissance CA | {OPT_CA}% | {REEL_CA}% | {PESS_CA}% |
| Marge EBITDA cible | {OPT_MARGE}% | {REEL_MARGE}% | {PESS_MARGE}% |
| Effectif moyen | {OPT_FTE} | {REEL_FTE} | {PESS_FTE} |
| CAPEX total | {OPT_CAPEX} k€ | {REEL_CAPEX} k€ | {PESS_CAPEX} k€ |

## Onglet 2 : P&L mensualisé (scénario réaliste)

| Poste | Jan | Fév | Mar | Avr | Mai | Jun | Jul | Aoû | Sep | Oct | Nov | Déc | **Total** |
|-------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----------|
| **CA HT** | | | | | | | | | | | | | |
| Ventes produit A | | | | | | | | | | | | | |
| Ventes produit B | | | | | | | | | | | | | |
| Services | | | | | | | | | | | | | |
| **Achats** | | | | | | | | | | | | | |
| Marge brute | | | | | | | | | | | | | |
| Taux MB % | | | | | | | | | | | | | |
| **Charges externes** | | | | | | | | | | | | | |
| Loyer | | | | | | | | | | | | | |
| SaaS / abonnements | | | | | | | | | | | | | |
| Marketing | | | | | | | | | | | | | |
| Autres | | | | | | | | | | | | | |
| **Masse salariale** | | | | | | | | | | | | | |
| Salaires | | | | | | | | | | | | | |
| Charges sociales | | | | | | | | | | | | | |
| **Autres charges fixes** | | | | | | | | | | | | | |
| **EBITDA** | | | | | | | | | | | | | |
| % EBITDA | | | | | | | | | | | | | |
| Amortissements | | | | | | | | | | | | | |
| Frais financiers | | | | | | | | | | | | | |
| **Résultat net** | | | | | | | | | | | | | |

## Onglet 3 : Bilan prévisionnel

(Début + fin d'exercice — postes principaux)

## Onglet 4 : Cash flow prévisionnel

(Méthode indirecte)

## Onglet 5 : Effectif détaillé

| Département | Effectif déc N-1 | Arrivées | Départs | Effectif déc N | Masse salariale |
|-------------|------------------|----------|---------|----------------|-----------------|
| Tech / Produit | | | | | |
| Commercial | | | | | |
| Marketing | | | | | |
| G&A | | | | | |
| **Total** | | | | | |

## Onglet 6 : CAPEX détaillé

| Projet | Montant | Trimestre | Justification | NPV |
|--------|---------|-----------|---------------|-----|
| | | | | |

## Onglet 7 : Comparaison 3 scénarios

| | Opt | Réel | Pess |
|--|-----|------|------|
| CA annuel | | | |
| Marge brute € | | | |
| Marge brute % | | | |
| EBITDA € | | | |
| EBITDA % | | | |
| Résultat net € | | | |
| Cash fin d'année | | | |

**Pondéré 20/60/20** : {PONDERE_CA} CA / {PONDERE_EBITDA} EBITDA

---

_Généré par moriarty-cfo / cfo-budget-forecast v0.1.0 — à exporter vers Excel pour édition_
