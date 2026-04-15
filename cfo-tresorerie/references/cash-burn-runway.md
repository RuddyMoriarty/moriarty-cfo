# Cash burn & Runway, mode startup / scale-up

Activé si `classification.taille ∈ {tpe, pe}` + `secteur.module_sectoriel = saas_techno` ou si l'utilisateur déclare "startup" / "scale-up" lors de `cfo-init`.

## Métriques clés

### Cash burn mensuel

```
Cash_burn_M = Solde_cash_fin_M-1 - Solde_cash_fin_M
```

Attention :
- Ne pas inclure les augmentations de capital (ce n'est pas de la consommation opérationnelle)
- Ne pas inclure les remboursements de principal d'emprunt (mais inclure les intérêts)
- **Mesurer la vraie consommation opérationnelle** : Cash burn = Cash out opérationnel - Cash in opérationnel

### Gross burn vs Net burn

- **Gross burn** : total des décaissements mensuels
- **Net burn** : décaissements - encaissements = la véritable consommation nette

On préfère le **net burn** pour mesurer la soutenabilité.

### Runway

```
Runway_mois = Cash_actuel / Net_burn_mensuel
```

Le nombre de mois avant d'être à court de cash si rien ne change.

### Burn multiple (Lenny Rachitsky formula)

```
Burn_multiple = Net_burn / Net_new_ARR
```

Mesure l'efficacité capital consommé par euro de croissance ARR.

| Burn multiple | Efficacité |
|---------------|------------|
| < 1 | Excellent (growth efficient) |
| 1 - 1.5 | Bon |
| 1.5 - 2 | Acceptable |
| 2 - 3 | À surveiller |
| > 3 | Inefficace (ratio à améliorer avant toute nouvelle levée) |

## Seuils d'alerte runway

| Runway | Niveau | Action |
|--------|--------|--------|
| 🔴 < 6 mois | Urgence absolue | Pivot ou levée d'urgence (bridge round) |
| 🟠 6-12 mois | Planning levée | Démarrer la levée de fonds MAINTENANT (6-9 mois de cycle typique) |
| 🟡 12-18 mois | Surveillance active | Optimisation burn possible, pipeline levée à construire |
| 🟢 > 18 mois | Healthy | Focus croissance |

## Optimisation du burn

### Ordre de priorité (du moins douloureux au plus douloureux)

1. **Stopper les growth marketing non rentables** (tester avant couper)
2. **Renégocier les contrats SaaS / outils** (15-25% de réduction possible)
3. **Geler les recrutements non critiques**
4. **Réduction temps partiel** ou **congés sans solde volontaires**
5. **Réduction salariale volontaire** des fondateurs / C-level
6. **Layoffs** (dernier recours, coût d'indemnités + perte de compétences + moral)

### Benchmark coûts principaux (SaaS early stage)

| Poste | % du burn | Levier |
|-------|-----------|--------|
| Masse salariale | 50-70% | Recrutement, temps partiel, layoffs |
| Marketing / acquisition | 15-30% | ROAS, canaux, test & learn |
| Infrastructure (AWS, tools) | 5-15% | Rightsizing, optimisation contrats |
| Locaux | 5-15% | Remote, downgrading |
| Services externes (avocat, compta) | 5-10% | Renégociation |

## Trajectoire de fundraising

### Cycle typique de levée

```
Mois -12 : Mise en ordre des KPIs + pitch
Mois -9  : Warm intros VCs
Mois -6  : First meetings
Mois -4  : Term sheet(s)
Mois -2  : Due diligence
Mois 0   : Closing + réception fonds
```

Démarrer la levée **quand il reste 9-12 mois de runway** (jamais quand il reste < 6 mois, sauf bridge round d'urgence).

### Preuves demandées par les VCs

- **Unit economics positifs** : LTV/CAC > 3, payback < 18 mois
- **Croissance constante** : 10-20% MoM minimum pour Series A
- **Burn multiple** < 2 idéalement
- **Runway après investissement** : 18-24 mois minimum

## Écritures comptables

Pas de traitement comptable spécifique, le burn n'est pas un poste du bilan, c'est un **indicateur managérial** calculé sur l'évolution du cash.

## Dashboard startup

Template `templates/cashflow-12m.html` (version startup) inclut :
- Courbe cash disponible + runway projetée
- MRR / ARR mensuels
- Cash burn net
- Burn multiple
- Alerte visuelle seuils (zones rouge / orange / verte)

## Orchestration

- Intègre les données produit (MRR, churn) de **sources externes** (Stripe, Chargebee)
- Coordonne avec `cfo-budget-forecast` pour les scénarios levée / pas levée
- Escalade à `cfo-financement-croissance` pour le pack levée et la stratégie investisseur

## Adaptation par audience

**Mode EC** : accompagnement startup en mission contractuelle. Formation du fondateur aux métriques. Préparation du pack pour VC.

**Mode PME** (startup) : outil de pilotage weekly du fondateur / CEO. Doit être **simple** et **actionnable**. Ne pas surcharger avec des ratios théoriques.

## Renvoi à d'autres skills

- `cfo-financement-croissance` : pack levée de fonds, pitch VC, due diligence
- `cfo-budget-forecast` : scénarios avec / sans levée
- `cfo-controle-gestion` : KPIs produit (MRR, churn, LTV/CAC)
- `cfo-reporting` : investor letter trimestrielle
