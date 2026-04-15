# Comptabilité analytique

Décomposer les coûts pour éclairer les décisions de gestion.

## Différence comptabilité générale vs analytique

| Compta générale | Compta analytique |
|-----------------|-------------------|
| Obligatoire légalement | Facultative |
| Orientation externe (AG, EC, DGFiP) | Orientation interne (pilotage) |
| Classification par nature (60 achats, 64 salaires...) | Classification par destination (produit, client, activité) |
| Périodicité annuelle ou mensuelle | Périodicité variable (mensuel à temps réel) |
| Référentiel : PCG | Référentiel : choix de l'entreprise |

## Méthode 1, Direct costing (coûts variables)

**Principe** : seules les charges variables sont imputées aux produits/clients. Les charges fixes restent en charge globale.

**Formule** :
```
Marge contributive = CA - Coûts variables
Résultat = Marge contributive totale - Charges fixes
```

**Usage** : décisions court terme (accepter une commande atypique, fermer une activité...).

**Piège** : peut conduire à sous-pricer (si on oublie de couvrir les charges fixes long terme).

## Méthode 2, Full costing (coûts complets)

**Principe** : toutes les charges (variables + fixes) sont imputées aux produits/clients via des clés de répartition.

**Formule** :
```
Coût complet = Coûts directs + Coûts indirects répartis
Marge = Prix de vente - Coût complet
```

**Usage** : pricing structurel, reporting produit, valorisation des stocks (IAS 2).

**Clés de répartition typiques** :
- Heures machine (industrie)
- Heures main-d'œuvre directe
- Surface au sol (immobilier)
- Nombre de transactions

**Piège** : les clés arbitraires peuvent masquer des coûts réels. Une activité peut apparaître non rentable à cause d'une clé mal choisie.

## Méthode 3, ABC (Activity-Based Costing)

**Principe** : au lieu de clés globales, identifier les **activités** consommées par chaque produit/client et les **drivers** (inducteurs de coûts) spécifiques.

**Étapes** :
1. Identifier les activités (ex: "traiter une commande", "produire une unité", "servir un client")
2. Déterminer le coût de chaque activité (regrouper charges directes et indirectes)
3. Définir un driver par activité (nb commandes, nb unités produites, nb heures de service client)
4. Calculer le coût unitaire par driver
5. Imputer aux produits/clients selon consommation réelle

**Usage** : diagnostic fin des vraies rentabilités (souvent révélateur : les "petits clients" coûtent parfois plus cher que les gros).

## Exemple ABC concret

Société de services informatiques, 2 segments : PME (volume) et Grands comptes (premium).

| Activité | Coût annuel | Driver | Driver PME | Driver GC |
|----------|-------------|--------|------------|-----------|
| Support niveau 1 | 200 k€ | Nb tickets | 5 000 tickets | 500 tickets |
| Onboarding | 100 k€ | Nb nouveaux clients | 150 | 20 |
| Account management | 300 k€ | Nb heures | 800h | 2 000h |
| Dev produit | 500 k€ | Répartition CA | 40% | 60% |

Allocation :
- PME : support 180k€ (90%) + onboarding 87k€ (88%) + AM 86k€ (29%) + dev 200k€ (40%) = **553 k€**
- GC : support 20k€ + onboarding 13k€ + AM 214k€ + dev 300k€ = **547 k€**

Avec CA PME 1.5 M€ et GC 1 M€ :
- Marge PME = 1.5M - 553k = 947k (63%)
- Marge GC = 1M - 547k = 453k (45%)

→ Les GC semblent "premium" mais consomment plus de services. Insight ABC : le segment PME est plus rentable qu'il n'y paraît.

## Script `profitability_analyzer.py`

Implémente une méthode ABC simplifiée avec drivers configurables.

## Quelle méthode choisir ?

| Contexte | Méthode |
|----------|---------|
| TPE / petite PME | Direct costing (suffisant pour 80% des décisions) |
| PME 10-50 sal. | Full costing (avec clés simples) |
| ETI multi-produits | ABC (investissement dans la granularité) |
| Industrie complexe | ABC + coût standard (vs coût réel) |

## Pièges à éviter

- Passer trop de temps sur des allocations théoriques au lieu d'agir
- Changer de méthode tous les ans (perte de comparabilité)
- Appliquer une méthode sophistiquée sans données fiables (garbage in, garbage out)
- Confondre coût complet et coût marginal pour une décision tactique
