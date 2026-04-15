# Analyse de rentabilité produit / client

Méthodologie pour identifier les produits et clients rentables (ou non).

## Pourquoi l'analyse de rentabilité

**L'illusion du CA** : un client "gros" n'est pas forcément rentable. Un produit "populaire" peut dégrader la marge globale.

**Règle de Pareto** (empirique) :
- 20% des clients = 80% du CA
- Mais souvent : 20% des clients = 150% du profit (les 80% restants le détruisent)

## Méthode 1, Top-down

P&L par segment :
1. Partir du CA HT global
2. Ventiler par segment (produit / client / canal)
3. Affecter les charges directes (achats, commissions)
4. Calculer marge brute par segment
5. Répartir les charges indirectes au prorata (ou via ABC)
6. Calculer marge contributive puis marge opérationnelle

## Méthode 2, Bottom-up (ABC)

Pour chaque transaction / ligne :
1. CA net (prix - remises)
2. Coût direct (COGS ou coût variable)
3. Coûts indirects alloués via drivers ABC
4. Marge par ligne → agrégation par segment

## Dimensions d'analyse

### Par produit

Top/bottom 10 produits par :
- CA
- Marge contributive €
- Marge contributive %

**Actions possibles** :
- Top 10 : sécuriser, défendre (pricing, stock)
- Bottom 10 : repricer, réduire coûts, arrêter si marge négative durable

### Par client

Top/bottom 10 clients par :
- CA
- Marge contributive €
- **Marge contributive après coûts d'acquisition/rétention** (ARR - CAC - CS)

**Actions possibles** :
- Top 10 : KAM dédié, renforcer la relation
- Bottom 10 : négocier prix à la hausse, réduire effort commercial, sortir si marge < 0

### Par canal

Direct vs indirect (revendeurs, marketplace) :
- Direct : marge typiquement plus élevée mais CAC plus élevé
- Indirect : marge réduite mais volume

### Par activité

Dans le cas d'une PME multi-activités : ventiler clairement.

## Piège du coût unitaire

Ne pas se limiter au prix unitaire. Inclure **tous les coûts directs et indirects** imputables :
- Coût d'acquisition du client (CAC)
- Coût de service client (support, CSM)
- Commissions commerciales
- Frais logistiques / emballages
- Coût de non-qualité (retours, garanties)

## Matrice BCG revisitée

| | Marge élevée | Marge faible |
|--|--------------|--------------|
| **Volume élevé** | ⭐ Star (à protéger) | 🐄 Cash cow (optimiser coûts) |
| **Volume faible** | 🎯 Niche premium | ❓ Question (repricer ou arrêter) |

## Script `profitability_analyzer.py`

Input : CSV ventes détaillées avec colonnes `client, produit, date, ca, cout_direct`
Output : top/bottom N par dimension + visualisation Pareto + alertes marges négatives

## Adaptation par audience

**Mode EC** : mission "diagnostic rentabilité" chiffré en euros et pourcentages.

**Mode PME** : dire clairement **quoi faire avec la liste**. "Sortir le client X" est une décision business, pas juste une analyse.

## Limites

- Allocation des coûts indirects : subjective (méthode retenue = approximation)
- Coût marginal vs coût complet : ne pas confondre
- Saisonnalité : analyser sur 12 mois glissants, pas 1 mois isolé
