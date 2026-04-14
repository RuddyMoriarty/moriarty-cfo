# Pricing optimization

Stratégies de prix et leur impact sur la rentabilité.

## 4 approches

### 1. Cost-plus

Prix = Coût complet × (1 + Marge cible)

**Avantages** : simple, assure la rentabilité unitaire.
**Inconvénients** : ignore la valeur perçue et le marché.

### 2. Value-based

Prix = Valeur que le client retire - Marge de négociation

**Avantages** : aligne le prix sur la valeur, maximise la marge.
**Inconvénients** : difficile à quantifier, nécessite des études clients.

**Exemple SaaS** : si le SaaS fait gagner 10 000 €/an au client, prix acceptable ≤ 3 000 €/an (typiquement 10-30% de la valeur).

### 3. Competition-based

Prix = Prix des concurrents ± Différentiel de valeur perçue

**Avantages** : simple à observer, crédible dans un marché mature.
**Inconvénients** : course au moins-disant, ignore la structure de coûts propre.

### 4. Dynamic pricing

Prix variable selon : période, client, usage, saison.

**Modèles typiques** :
- SaaS : freemium + tiers (starter / pro / enterprise)
- Hôtellerie / aérien : yield management
- E-commerce : prix temps réel selon trafic / stock / concurrents

## Élasticité prix

```
Élasticité = (% variation quantité) / (% variation prix)
```

- Élasticité > 1 : produit élastique (hausse 10% du prix → baisse > 10% des ventes, CA baisse)
- Élasticité < 1 : produit inélastique (hausse de prix absorbée, CA augmente)
- Élasticité = 1 : neutre

**Cas inélastiques** :
- Produits de nécessité (santé, énergie, alimentaire de base)
- Produits de luxe (image)
- Monopoles / quasi-monopoles
- Produits à forte valeur ajoutée perçue (SaaS critique)

**Cas élastiques** :
- Commodities (achat basé sur le prix)
- Concurrence forte
- Produits de consommation non essentiels

## Tests pricing

Approche recommandée :
1. Définir 2-3 variantes de prix
2. Tester sur un segment limité (nouveau client, géographie spécifique)
3. Mesurer : taux de conversion, CA, marge
4. Ajuster selon les résultats

## Script `pricing_simulator.py`

Simule l'impact d'un changement de prix selon une élasticité estimée :

Input : prix actuel, volume, coût variable unitaire, élasticité estimée, nouveau prix
Output : scénario CA + marge avec le nouveau prix + point-break

## Quand réévaluer les prix ?

- Annuellement (révision systématique)
- Lors d'une inflation significative (> 3%)
- Lors d'un changement significatif de coûts (matières premières, salaires)
- Au lancement d'un nouveau produit / SKU
- Après perte ou gain de position concurrentielle

## Psychology pricing

Quelques principes :
- **99 au lieu de 100** : perception d'un prix inférieur (fonctionne toujours en B2C)
- **Ancrage** : prix de référence (barré) fait apparaître le prix réel comme avantageux
- **Bundle** : packager (ex. pro pack) réduit la sensibilité au prix unitaire
- **Décomposition temporelle** : "1 € par jour" > "30 €/mois"

## Limites de l'optimization pricing

- Pas de magie : si le coût complet > prix concurrent, la société n'est pas compétitive
- Risque éthique : dynamic pricing peut être perçu comme injuste (ex. prix pendant catastrophe naturelle)
- Complexité : trop de variantes de prix = confusion client + charge opérationnelle
