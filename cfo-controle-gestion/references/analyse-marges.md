# Analyse des marges

## Les 4 niveaux de marge

### Marge brute (secteurs commerce / industrie)

```
MB = CA HT - Coût d'achat des marchandises vendues (ou production)
Taux MB = MB / CA HT × 100
```

**Cohérence** : la MB mesure la performance "produit pur" avant les frais généraux.

### Marge contributive (MC)

```
MC = CA - Coûts variables (directs + indirects variables)
```

**Usage** : combien chaque vente contribue à couvrir les frais fixes + générer du profit.

### Marge opérationnelle (EBIT / CA)

```
Marge OP = EBIT / CA HT
```

**Mesure la profitabilité globale** de l'activité hors financement.

### Marge nette (RN / CA)

```
Marge nette = Résultat net / CA HT
```

**Après tout** (impôts, intérêts, exceptionnels).

## Décomposition des évolutions (effet volume / prix / mix)

Quand la marge évolue entre 2 périodes, identifier **quelle est la cause** :

### Effet volume

```
Effet volume = (Qté_N - Qté_N-1) × Marge_unitaire_N-1
```

→ Hausse des ventes en quantité, à marge unitaire constante.

### Effet prix

```
Effet prix = (Prix_N - Prix_N-1) × Qté_N × (1 - taux coût variable)
```

→ Hausse des prix de vente (ou baisse des coûts unitaires) à quantité constante.

### Effet mix

```
Effet mix = Évolution de la répartition des ventes entre produits / clients de marges différentes
```

Exemple : on vend toujours 1000 unités mais plus de produit A (marge 30%) et moins de B (marge 20%) → effet mix positif.

### Effet timing / saisonnalité

Si analyse non annualisée : une commande décalée d'un trimestre peut créer une variance artificielle.

## Exemple concret

Société de services BtoB, marge brute 2025 = 60%, 2026 = 58% (-2 pts).

Investigation :
- Effet volume : neutre (+/- 2% de CA)
- **Effet prix : -3 pts** (grosses remises accordées pour fidéliser clients clés)
- **Effet mix : +1 pt** (plus de clients premium dans le mix)
- Effet timing : neutre

**Conclusion** : la baisse vient des remises. Décision : re-basculer vers la facturation standard au renouvellement, accepter une perte de 2 clients prêts à partir plutôt que de baisser encore la marge globale.

## Benchmarks sectoriels

Source Banque de France FIBEN + INSEE Esane :

| Secteur | Marge brute médiane | Taux EBE médian |
|---------|---------------------|-----------------|
| SaaS | 70-85% | 20-40% |
| Services BtoB | 35-55% | 8-15% |
| Industrie (PME) | 25-40% | 8-12% |
| Commerce spécialisé | 30-45% | 4-8% |
| Grande distribution | 18-25% | 2-4% |
| BTP | 20-35% | 3-8% |
| Restaurant (indépendant) | 65-75% | 5-12% |

## Leviers d'amélioration

### Lever la marge brute

- Augmenter les prix (élasticité)
- Renégocier les achats
- Mix produit premium
- Éliminer produits marge négative

### Lever la marge contributive

- Idem MB
- Réduire les coûts variables (commissions, logistique)

### Lever la marge opérationnelle

- Levier **structure** : réduire les frais fixes (locaux, masse salariale)
- Levier **productivité** : faire plus de CA avec les mêmes coûts fixes

## Piège : la marge en % vs en €

**Attention au focus "% pur"** : une PME de 1M€ CA à 30% de marge (300k€) ≠ 10M€ CA à 20% de marge (2M€). Le deuxième cas est plus rentable en absolu.

Pour les arbitrages : raisonner en **€ absolus** de marge, pas seulement en %.
