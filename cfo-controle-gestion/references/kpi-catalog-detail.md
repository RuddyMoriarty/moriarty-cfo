# Catalogue détaillé des 32 KPIs CFO

Catalogue maître dans `../../data/kpi-catalog.json`. Ce document explique la pertinence, le calcul et les benchmarks.

## Catégorie 1, Activité

### CA HT
```
CA HT = Σ comptes 70 (produits)
```
- Fréquence : mensuelle
- Secteurs : all
- Benchmark : selon sous-secteur (Banque de France FIBEN)

### Growth YoY
```
Growth = (CA_N - CA_N-1) / CA_N-1
```
- Fréquence : mensuelle
- **Benchmarks typiques** :
  - PME mature : 2-8% / an
  - Startup early-stage : 100%+ / an
  - Scale-up : 40-100% / an
  - Cotée : 5-15% / an

### Production de l'exercice
```
Production = CA + Production stockée + Production immobilisée
```
- Usage : industrie, fabrication
- Permet de mesurer l'activité réelle de production (vs ventes)

## Catégorie 2, Rentabilité

### Marge brute (commerce/négoce)
```
MB = CA HT - Coût d'achat des marchandises vendues
Taux MB = MB / CA HT × 100
```
- Benchmarks :
  - Grande distribution : 18-25%
  - Commerce spécialisé : 30-45%
  - E-commerce : 20-50%

### Valeur ajoutée
```
VA = Production - Consommations en provenance des tiers
```
- Usage : industrie, services
- Mesure de la création de valeur propre (hors achats externes)

### Excédent Brut d'Exploitation (EBE)
```
EBE = VA - Charges de personnel - Impôts et taxes + Subventions d'exploitation
```
- **Cœur de la rentabilité opérationnelle**, indépendant de la politique d'amortissement et de financement

### Taux d'EBE / CA
```
Taux EBE = EBE / CA HT × 100
```
- Benchmarks PME :
  - Services : 8-15%
  - Industrie : 10-18%
  - Commerce : 3-8%
  - SaaS mature : 20-40%

### EBITDA
```
EBITDA = Résultat d'exploitation + Dotations aux amortissements (+ provisions si ajusté)
```
- Pendant US de l'EBE avec petites différences (pas de subventions, pas de taxes sauf IS)

### EBIT / Résultat d'exploitation
```
EBIT = Produits d'exploitation - Charges d'exploitation
```

### Résultat net
```
RN = Résultat avant impôt - IS
```

### Rentabilité économique (ROCE)
```
ROCE = EBIT × (1 - Taux IS) / Capitaux investis
Capitaux investis = Capitaux propres + Dettes financières
```
- **Benchmark** : ≥ 8% = acceptable, ≥ 15% = excellent
- Cible > coût du capital (WACC)

### Rentabilité financière (ROE)
```
ROE = Résultat net / Capitaux propres
```
- **Benchmark PME** : 10-20% selon secteur

## Catégorie 3, Structure financière

### Fonds de roulement (FR)
```
FR = Capitaux permanents - Actif immobilisé
```
- FR > 0 → la société finance correctement ses immos avec des ressources stables

### Ratio autonomie financière
```
Ratio = Capitaux propres / Total bilan
```
- Benchmark : > 30% (sociétés saines), < 20% (fragilité)

### Ratio d'endettement (gearing)
```
Gearing = Dettes financières / Capitaux propres
```
- Benchmark : < 1.0 (sain), > 1.5 (levier élevé)

### Capacité d'autofinancement (CAF)
```
CAF = RN + DAP + VNC sorties - Reprises - Quote-part subvention
```
- Proxy du cash généré avant variations BFR

### Capacité de remboursement
```
Cap remb = Dettes financières / CAF
```
- Benchmark : < 4 ans (banques apprécient), > 6 ans (stress)

## Catégorie 4, Trésorerie / BFR

(Voir cfo-tresorerie pour le détail)

- **DSO** : Créances clients TTC × 365 / CA TTC
- **DPO** : Dettes fournisseurs TTC × 365 / Achats TTC
- **DIO** : Stocks × 365 / Coût des ventes
- **CCC** : DSO + DIO - DPO

## Catégorie 5, Performance opérationnelle (startups)

### Cash burn mensuel
```
Burn = Variation trésorerie nette mensuelle (négative)
```

### Runway
```
Runway = Cash actuel / Cash burn mensuel
```
- Seuils : <6m urgent, 6-12m préparer levée, 12-18m surveiller, >18m healthy

## Catégorie 6, RH

### Coût du personnel / CA
```
Ratio = (Salaires + Charges sociales) / CA HT
```
- Benchmarks services : 40-65%
- Industrie : 20-40%

### CA / salarié
```
CA/salarié = CA HT / Effectif moyen
```
- Benchmarks PME : 100-300 k€

### VA / salarié
```
VA/salarié = VA / Effectif moyen
```
- Mesure la productivité réelle

## Catégorie 7, Investissement CAPEX

### Intensité capitalistique
```
Intensité = Immo corporelles brutes / CA HT
```

### Taux d'investissement
```
Taux invest = Investissements année / VA
```

### Vétusté de l'outil productif
```
Vétusté = Amortissements cumulés / Immobilisations brutes amortissables
```
- < 50% : parc récent
- 50-70% : équilibré
- > 70% : vétuste, renouvellement à anticiper

## Orchestration

- Ces 32 KPIs sont lus/calculés par `cfo-reporting/scripts/compute_kpis.py`
- Affichés dans le dashboard CFO (`cfo-reporting/templates/dashboard-cfo.html`)
- Benchmarks Banque de France FIBEN à intégrer en v0.2 (nécessite accès données FIBEN)

## Sources

- Banque de France FIBEN (benchmarks sectoriels payants)
- INSEE Esane (open data, https://www.insee.fr/fr/information/3210767)
- Études DFCG Vision Finance
- Big 4 CFO publications
