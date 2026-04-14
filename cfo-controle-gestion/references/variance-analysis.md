# Variance analysis

Identifier et expliquer les écarts entre budget (ou N-1) et réel.

## Pourquoi

- Budget = **engagement** de la direction
- Réel = **résultat**
- Variance = écart à expliquer et **à corriger si possible**

Sans variance analysis, on ne sait pas **pourquoi** on performe ou contre-performe, donc on ne peut pas **décider d'action corrective**.

## Méthodologie standard

### Étape 1 — Segmentation

Au minimum :
- Par poste (CA, achats, salaires, charges externes…)
- Par période (mois, trimestre, YTD)

Pour les PME+ :
- Par segment (produit / client / canal)
- Par centre de coût / responsabilité

### Étape 2 — Calcul des variances

Pour chaque poste :
- Variance € = Réel - Budget
- Variance % = Variance € / Budget

### Étape 3 — Seuils de matérialité

Ne commenter QUE les variances **significatives** :
- > 5 000 € ET
- > 5% du poste

Sinon on se noie dans le bruit.

### Étape 4 — Investigation

Pour chaque variance significative, identifier la cause :

1. **Effet volume** — ventes ou quantités différentes du prévu
2. **Effet prix** — tarifs ou coûts unitaires différents
3. **Effet mix** — répartition différente (produits, clients)
4. **Effet timing** — avance / retard (la variance se reverse)
5. **Effet de périmètre** — nouveau produit, nouveau client, acquisition

### Étape 5 — Actions correctives

Pour chaque variance défavorable non résolue :
- **Action immédiate** possible ?
- **Action structurelle** requise (changer le processus, repricer, etc.) ?
- **Acceptation** si variance ponctuelle hors du contrôle

## Template de commentaire

```markdown
## Variance {POSTE} : {DIFF_EUR} € ({DIFF_PCT}%)

**Cause principale** : [Effet volume / prix / mix / timing / périmètre]

**Décomposition** :
- Effet volume : {EUR} € — [explication]
- Effet prix : {EUR} € — [explication]
- Effet mix : {EUR} € — [explication]

**Impact cumulé YTD** : {EUR} €

**Action** : [Action corrective si applicable, owner, deadline]

**Statut** : [🟢 résolu / 🟠 en cours / 🔴 à traiter]
```

## Pièges fréquents

### Variance favorable ≠ bonne gestion

Si le budget était pessimiste (sous-dimensionné), la variance favorable vient du budget, pas de la performance.

### Variance défavorable ≠ mauvaise gestion

Si le budget était ambitieux (sur-dimensionné), la variance défavorable ne reflète pas un problème de pilotage.

→ **Challenger le budget** aussi régulièrement que le réel.

### Ne pas compenser les variances

Si vente produit A en hausse (+50k) et produit B en baisse (-40k), ne pas dire "net +10k, tout va bien". Commenter **chaque segment** séparément.

### Ne pas se perdre dans les détails

Commenter les top 10 variances, pas les 200 postes du P&L.

## Intégration reporting

Le reporting mensuel (cfo-reporting) inclut une section "variance analysis" avec le top 10 + commentaires.

Le script `scripts/variance_analyzer.py` de `cfo-controle-gestion` prépare le tableau + décomposition automatique volume/prix.

## Exemple concret

**Poste** : Salaires et charges sociales
**Budget** : 80 000 €
**Réel** : 95 000 €
**Variance** : +15 000 € (+19%) — DÉFAVORABLE

**Décomposition** :
- Effet volume : +10 000 € (1 recrutement non budgété démarré en M-2)
- Effet prix : +3 000 € (NAO salariales effet masse)
- Effet timing : +2 000 € (prime versée ce mois au lieu de M+1)

**Action** :
- Intégrer le recrutement dans le budget révisé Q2 (already approved by CEO)
- NAO : impact intégré dans forecast Q3-Q4

**Statut** : 🟡 vigilance (structurel, continuer le suivi)
