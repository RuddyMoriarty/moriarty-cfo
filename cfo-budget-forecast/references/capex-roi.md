# CAPEX planning + ROI / NPV / IRR / Payback

## Définitions

### CAPEX (Capital Expenditure)

Investissement dont le bénéfice s'étale sur plusieurs années :
- Matériel industriel
- Bâtiments
- Logiciels (dev interne activé)
- Véhicules
- Brevets
- Acquisitions de sociétés

Comptabilisé en immobilisation (pas en charge), amorti sur la durée d'utilisation.

### OPEX (Operating Expenditure)

Charge courante consommée dans l'exercice :
- Loyers, abonnements SaaS
- Salaires
- Matière première
- Frais généraux

Enregistrée directement en charge.

## Métriques de décision

### Payback (durée de retour sur investissement)

```
Payback = Investissement / Cash flow annuel additionnel
```

- Simple à comprendre
- Ne tient pas compte de la valeur temps de l'argent
- Critère d'exclusion : Payback > 5 ans = souvent refusé

**Exemple** : Machine 100 k€, cash flow additionnel 40 k€/an
→ Payback = 2.5 ans

### NPV (Net Present Value / Valeur actuelle nette)

```
NPV = Σ [CF_t / (1 + r)^t] - Investissement
```

- Actualise les cash flows futurs au taux de rendement exigé (WACC typique : 8-12% pour PME)
- **NPV > 0** : investissement crée de la valeur
- Prend en compte la valeur temps

**Exemple** avec r = 10% :
```
Année 0 : -100 k€
Année 1 : 40 k€ / 1.10 = 36.4 k€
Année 2 : 40 k€ / 1.21 = 33.1 k€
Année 3 : 40 k€ / 1.331 = 30.1 k€
Année 4 : 40 k€ / 1.464 = 27.3 k€
Année 5 : 40 k€ / 1.611 = 24.8 k€
Total = 151.7 - 100 = +51.7 k€ NPV
```

### IRR (Internal Rate of Return / Taux de rentabilité interne)

Taux qui annule la NPV. Se résout par itération (Excel : `=IRR(...)` ou Python `numpy-financial.irr`).

- **IRR > WACC** : investissement profitable
- **IRR > WACC + 5 pts** : excellent
- Simple à comparer entre projets

### ROI simple

```
ROI annuel = Cash flow annuel / Investissement × 100
```

- Indicateur rapide mais grossier

## Décision CAPEX

### Seuils typiques PME

| Critère | Seuil OK | Excellent |
|---------|----------|-----------|
| Payback | < 4 ans | < 2 ans |
| NPV (r=10%) | > 0 | > 20% de l'investissement |
| IRR | > 10% | > 25% |

### Priorisation si budget limité

Classer les projets par IRR décroissant → retenir ceux > seuil jusqu'à épuisement budget.

## Types de CAPEX

### CAPEX de maintenance

Remplacement d'équipement existant en fin de vie.
→ Décision : nécessaire pour maintenir l'activité. Pas de ROI explicite, mais risque de rupture d'activité si non investi.

### CAPEX de croissance

Nouveau produit, nouveau site, nouvelle capacité.
→ Décision : ROI / NPV / IRR à calculer.

### CAPEX réglementaire

Mise en conformité environnement, sécurité, accessibilité.
→ Décision : obligatoire. Pas de ROI explicite, mais évite les pénalités.

### CAPEX stratégique

Acquisition de société, JV, participation.
→ Décision : analyse stratégique + financière combinée.

## Script `capex_analyzer.py`

Calcule Payback, NPV, IRR, ROI pour un projet CAPEX :

Input : Investissement initial + cash flows annuels + WACC
Output : tous les indicateurs + go/no-go recommandé

## Template `capex-fiche.md`

Fiche individuelle par projet CAPEX :
- Description
- Montant
- Cash flows attendus
- Métriques financières
- Risques
- Décision + owner + deadline

## Pièges à éviter

- **Oublier la maintenance et le coût total de possession** (TCO) : l'investissement initial n'est souvent que 30-50% du coût total sur la durée d'usage
- **Ignorer les impôts** : amortissement = déduction fiscale → cash flow net d'IS
- **Optimisme sur les cash flows** : tendance à surestimer les gains (+50% typique vs réel observé)
- **Fausse précision** : donner un IRR à 0.1% près quand les cash flows sont estimés à ±30%
