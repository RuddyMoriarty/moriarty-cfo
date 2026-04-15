# Valorisation entreprise

## 4 méthodes principales

### 1. DCF (Discounted Cash Flow)

**Principe** : la valeur d'une entreprise = somme actualisée de ses cash flows futurs.

```
EV = Σ [FCF_t / (1 + WACC)^t] + Valeur terminale / (1 + WACC)^n
```

Composantes :
- **FCF (Free Cash Flow)** : EBITDA - IS - CAPEX - ΔBFR
- **WACC (Weighted Average Cost of Capital)** : coût moyen pondéré du capital
- **Valeur terminale** : Gordon Shapiro = FCF_(n+1) / (WACC - g)

**WACC indicatif** :
- PME stable : 10-12%
- PME en croissance : 12-15%
- Startup : 15-25%

**g (taux croissance perpétuelle)** : 1-3% en zone euro mature.

**Avantages** : approche fondamentale, intègre la croissance.
**Limites** : très sensible aux hypothèses (WACC, g, durée projection).

### 2. Multiples comparables

**Principe** : valoriser comme des sociétés comparables cotées ou récemment vendues.

Multiples typiques :
- **EV / Revenue** : SaaS = 5-15x ARR (selon growth + marge), industrie = 0,5-2x
- **EV / EBITDA** : services BtoB = 6-12x, SaaS = 10-25x, industrie = 5-9x
- **EV / EBIT** : utilisé si CAPEX significatif
- **P / E** : prix / résultat net (sociétés cotées)

**Sources** :
- Société cotées comparables (Bloomberg, Capital IQ)
- Transactions précédentes (Mergermarket, S&P Capital IQ, Pitchbook)
- Études sectorielles (Argos Wityu, Coface, Bain, BCG)

**Avantages** : reflète la réalité du marché.
**Limites** : trouver vraiment des "comparables" est difficile pour PME.

### 3. Transactions précédentes

**Principe** : valoriser comme des transactions M&A récentes dans le secteur.

Critères de comparabilité :
- Secteur d'activité
- Taille (CA, EBITDA)
- Géographie
- Date (< 18 mois pour rester pertinent)
- Type de transaction (PE, industriel, IPO)

**Sources** : bases payantes (Mergermarket, Pitchbook), publications BPI / France Invest.

### 4. LBO model (pour cible PE)

**Principe** : déterminer le prix maximum que peut payer un PE en fonction du **TRI cible** (typiquement 20-25%) sur 5 ans.

Mécanisme :
- Hypothèse de structure : 60-70% dette, 30-40% equity
- Hypothèse de croissance EBITDA + multiple de sortie
- Calcul du TRI sur l'equity investi

**Usage** : prix maximum que peut offrir un PE → plafond de la valorisation pour les sociétés rentables.

## Calcul détaillé : Equity Value

```
Enterprise Value (EV)            = valorisation par méthode (DCF, multiples...)
- Net Debt                       = (Dettes financières - Cash - Equivalents)
- Provisions                     = Engagements de retraite, litiges...
- Earn-out vendeur               = Si payable
+ Cash excédentaire              = Si > working capital normalisé
+ Actifs non opérationnels       = Immobilier non utilisé, participations
= Equity Value (prix payé aux actionnaires)
```

## Triangulation

**Bonne pratique** : utiliser **3 méthodes en parallèle** et triangulariser :
- DCF : valeur fondamentale
- Multiples : ce que le marché paie
- Transactions : ce qui s'est passé récemment

Si les 3 sont cohérents (±20%) → confiance forte.
Si écarts importants → comprendre pourquoi (croissance différente, risques perçus...).

## Script `valuation_calculator.py`

Calcule en parallèle :
- DCF (avec WACC + g paramétrables)
- Valorisation par multiple EBITDA (multiple paramétrable)
- Valorisation par multiple Revenue (pour SaaS)

Output : fourchette de valorisation + sensibilités.

## Cas particulier : startups pre-revenue

Méthodes alternatives :
- **Berkus Method** : 0-500 k$ par critère qualitatif (équipe, prototype, market, etc.)
- **Scorecard Method** : valorisation moyenne du marché × score sur 6 critères
- **Risk Factor Summation** : ajustements positifs / négatifs sur valorisation moyenne
- **Venture Capital Method** : valeur de sortie / IRR cible × multiple

## Adaptation par audience

**Mode EC** : missions "valorisation" en mission contractuelle. Cohérence des hypothèses → critique. Justifier chaque hypothèse.

**Mode PME / fondateur** : sachez que la valorisation **se négocie**. Avoir une fourchette de référence (basée sur multiples + DCF) vous donne du **leverage**. Faire valider par un cabinet de **transaction services** si tour > 5 M€.

## Avertissement

La valorisation est **un art**, pas une science exacte. Les chiffres sortis dépendent fortement des **hypothèses retenues**. Toute valorisation doit être **challengée** et présentée avec des sensibilités (±10%, ±20%).

Pour les opérations engageantes (cession, levée > 1 M€), consulter un **cabinet de transaction services** (Big 4 valuation, ou boutique spécialisée).
