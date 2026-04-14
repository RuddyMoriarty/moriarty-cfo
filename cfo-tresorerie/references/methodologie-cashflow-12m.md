# Méthodologie forecast 12 mois glissants

Prévision de trésorerie à horizon 12 mois, granularité mensuelle. Complément du forecast 13 semaines (plus long terme, plus stratégique).

## Pourquoi 12 mois

- Horizon aligné avec le **budget annuel** et les arbitrages stratégiques
- Vision suffisante pour **anticiper la levée de fonds** ou les besoins de financement structurel
- Standard demandé par les banques pour toute demande de financement à moyen terme
- Intègre les effets saisonniers (cycles d'activité annuels)

## Différences vs forecast 13w

| Dimension | 13 semaines | 12 mois |
|-----------|-------------|---------|
| Granularité | Hebdomadaire | Mensuelle |
| Horizon | 3 mois | 12 mois |
| Usage | Pilotage opérationnel | Stratégie / financement |
| Hypothèses | Fermes (contrats signés) | Mix fermes + scénarios |
| CAPEX | Uniquement engagés | Tous (y compris prévus non engagés) |
| Scénarios | Pas nécessaire | Optimiste / réaliste / pessimiste **obligatoire** |

## Structure du modèle

Tableau à 12 colonnes (M1 à M12) + colonne "Total" + scénarios.

```
                         M1    M2    M3    M4  ...  M12    Total
                         mai   juin  juil  août       avril

SOLDE INITIAL            150k  130k  145k  110k  ...

ENCAISSEMENTS
├─ CA prévisionnel       200k  220k  180k  150k  ...
├─ Variation créances     30k   20k  -10k  -40k  ...
├─ Subventions / CIR                  80k                 80k
├─ Apports extérieurs                             200k   200k
━━━━━━━━━━━━━━━━━━━━━━
Encaissements totaux

DÉCAISSEMENTS
├─ Achats & charges      130k  140k  150k  120k  ...
├─ Salaires (y.c. charges) 80k   80k   80k   80k  ...
├─ Impôts (IS, taxes)     15k          30k   15k  ...
├─ CAPEX                             50k        200k    250k
├─ Remboursement emprunts  3k    3k    3k    3k  ...    36k
━━━━━━━━━━━━━━━━━━━━━━
Décaissements totaux

Flux net mensuel
SOLDE FINAL
```

## Étapes de construction

### Étape 1 — Scénario de base

Hypothèses centrales :
- Croissance CA : aligner sur le budget annuel validé
- Taux de marge : historique des 3 derniers mois stable
- Conditions de paiement : conditions actuelles maintenues
- Embauches : uniquement celles déjà validées

### Étape 2 — Scénario optimiste (+X%)

Hypothèses upside :
- Croissance CA +15% vs base (nouveau contrat majeur, nouveau produit réussi)
- Amélioration taux de marge (+2 pts)
- Accélération encaissements (DSO -10j)
- Subventions obtenues en avance

### Étape 3 — Scénario pessimiste (-X%)

Hypothèses downside :
- Croissance CA -10% (perte d'un client clé, retard produit)
- Dégradation marge (-3 pts)
- Dégradation DSO (+15j)
- CAPEX maintenu (fixe)
- Aucune subvention ni aide reçue

### Étape 4 — Probabilité pondérée

Ne pas utiliser la moyenne simple. Appliquer des **probabilités** :
- Pessimiste : 20-30% (plus en contexte incertain)
- Réaliste : 50-60%
- Optimiste : 10-20%

Le scénario pondéré donne une vision plus honnête du "cas probable".

## Intégrer les éléments non récurrents

- **Augmentation de capital prévue** : mois de réception (typiquement ~4-6 mois après démarrage négo)
- **Remboursement de prêt garanti État (PGE)** : selon le plan d'amortissement
- **Cessions d'actifs** : seulement si engagements fermes
- **Crédit d'impôt (CIR, CII)** : 4 mois après dépôt
- **Paiement différé subventions** : vérifier les conditions
- **Dividendes à verser** : si décidés par l'AG

## Scénarios stress test

Pour une société en croissance, toujours tester :
- **Ralentissement** : CA stagne pendant 6 mois
- **Crise** : CA -30% pendant 3 mois, puis recovery lent
- **Chute client majeur** : perte du top 1 client (souvent 20-40% du CA en PME)

## Visualisation

Template `templates/cashflow-12m.html` :
- Graph ligne du solde final par mois (3 courbes : opt/réel/pess)
- Zone rouge si solde < seuil minimal
- Commentaire automatique du mois le plus critique

## Qualité

Retravailler le modèle **chaque trimestre** (après le reporting trimestriel) pour :
- Valider les hypothèses du trimestre écoulé
- Recaler les projections
- Ajuster les scénarios à la lumière des nouveaux événements

## Usage externe

Le forecast 12 mois est souvent **demandé par** :
- Banques (pour demande de financement MLT)
- Investisseurs (avant un tour de table)
- Acheteurs potentiels (en due diligence)
- Consultants de restructuring

Dans ces cas : **adapter le format** au demandeur (ex. banque = focus sur DSCR et liquidité ; investisseur = focus sur runway et trajectoire de croissance).

## Adaptation par audience

**Mode EC** : souvent demandé en mission contractuelle pour un client en croissance ou en difficulté. Scénarios obligatoires.

**Mode PME** : l'outil idéal pour **convaincre sa banque** ou son board. Bien expliciter les hypothèses et rester réaliste (l'upside doit être crédible, pas du wishful thinking).

## Orchestration

- Le forecast 12m s'appuie sur le **budget annuel** produit par `cfo-budget-forecast`
- Les hypothèses de CA viennent de `cfo-controle-gestion` (prévisions commerciales)
- Si tension détectée → escalade à `cfo-financement-croissance`
