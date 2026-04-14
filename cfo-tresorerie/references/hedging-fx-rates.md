# Hedging / couverture change et taux

Gestion du risque de change (FX) et du risque de taux (intérêts).

## Risque de change (FX risk)

### Quand en parler ?

Si la société a des flux en **devises étrangères** (USD, GBP, CHF, etc.) :
- Ventes export facturées en devises
- Achats import payés en devises
- Filiales étrangères (conversion des comptes)
- Emprunts libellés en devises

### Types de risque

1. **Risque de transaction** : entre la commande et l'encaissement, le taux a bougé
2. **Risque de conversion (translation)** : conversion des comptes des filiales étrangères
3. **Risque économique** : impact à long terme sur la compétitivité (indirect)

### Instruments de couverture

| Instrument | Description | Coût | Flexibilité |
|------------|-------------|------|-------------|
| **Change à terme** | Fixer le taux pour une date future | Faible (différentiel de taux) | Peu flexible (date fixe) |
| **Option de change** | Droit d'acheter/vendre à un taux donné | Prime à payer (2-5%) | Flexible (choix d'exercer ou non) |
| **Swap de devises** | Échange de flux en 2 devises pendant une période | Différentiel de taux | Peu flexible (long terme) |
| **Natural hedge** | Aligner recettes et dépenses dans la même devise | Gratuit | Dépend de la structure |

### Exemple concret

Société B2B export, CA 5 M€/an dont 30% en USD (1.5M USD à encaisser sous 6 mois).

**Scénario sans couverture** :
- Taux spot aujourd'hui : 1 EUR = 1.10 USD → 1.5M USD = 1.36M EUR
- Si USD se renforce à 1.05 dans 6 mois : 1.5M USD = 1.43M EUR (+70k€ gagné)
- Si USD s'affaiblit à 1.15 : 1.5M USD = 1.30M EUR (-60k€ perdu)

**Avec change à terme** :
- Fixer le taux à terme (ex. 1.08)
- 1.5M USD → 1.39M EUR certain
- Pas de surprise

**Trade-off** : paix d'esprit vs. upside potentiel. Pour une PME, **mieux vaut la certitude**.

### Règle d'or

- **Ne jamais spéculer** sur les devises si ce n'est pas le métier de la société
- Couvrir 50-80% de l'exposition, laisser 20-50% en ouvert (flexibilité)
- Fixer une **politique de hedging** validée par le board (% à couvrir, instruments autorisés)
- Revoir la politique annuellement

## Risque de taux (interest rate risk)

### Quand en parler ?

Si la société a des emprunts à **taux variable** (ex. Euribor + marge) et que l'environnement de taux est incertain.

### Instruments

| Instrument | Description |
|------------|-------------|
| **IRS (Interest Rate Swap)** | Échanger un taux variable contre un taux fixe (ou inverse) |
| **Cap** | Plafonner le taux variable (paiement d'une prime) |
| **Floor** | Plancher (garantir un taux min sur placements) |
| **Collar** | Cap + Floor combinés (tunnel) |

### Exemple

PME avec 500 k€ de PGE à taux variable Euribor 3M + 1.5% :
- Taux aujourd'hui : ~3.5% + 1.5% = 5% → 25 k€ d'intérêts annuels
- Si Euribor passe à 4.5% : intérêts = 6% = 30 k€ (+5 k€/an)
- **IRS à 4%** fixerait le taux à 4% + 1.5% = 5.5% pour 5 ans

Coût de l'IRS : différentiel entre taux fixe et taux variable anticipé, souvent nul si aligné avec courbe des taux.

## Comptabilisation (IFRS 9 / French GAAP)

### IFRS 9 (groupes IFRS)

3 catégories de couverture :
1. **Cash flow hedge** : couverture de flux futurs (ex. change à terme sur ventes export)
2. **Fair value hedge** : couverture d'un élément du bilan (ex. IRS sur emprunt)
3. **Net investment hedge** : couverture d'un investissement net en devises

**Documentation obligatoire** :
- Relation de couverture identifiée dès le démarrage
- Efficacité démontrée (80-125% test prospectif)
- Documentation écrite des hypothèses

**Comptabilisation** :
- Cash flow hedge : variation de juste valeur du dérivé en **OCI** (autres éléments du résultat global), recycled en P&L quand le flux couvert se réalise
- Fair value hedge : variation en P&L + ajustement symétrique de l'élément couvert

### French GAAP (ANC)

Moins strict que IFRS, possibilité de conserver le dérivé hors bilan (engagements de hors-bilan) tant qu'il est en couverture.

## Politique de hedging recommandée

Document à faire valider par le board, revoir annuellement :

```
POLITIQUE DE HEDGING — [SOCIÉTÉ]

1. Objectif
   Réduire la volatilité du résultat lié aux variations de change/taux.
   Pas de spéculation.

2. Périmètre
   - Change : EUR/USD sur les flux B2B export
   - Taux : sur les emprunts > 500k€ à taux variable

3. Seuils
   - Couvrir 70% de l'exposition identifiée en change
   - Couvrir 100% des emprunts > 1M€ à taux variable

4. Instruments autorisés
   - Change à terme (pas d'option en v1)
   - IRS receveur de taux fixe contre payeur variable

5. Validation
   - CFO : tout hedging < 500k€ notional
   - CFO + CEO : 500k€ - 2M€
   - Board : > 2M€ OU nouveau type d'instrument

6. Revue
   - Mensuelle : reporting exposition + MTM positions
   - Annuelle : revue de politique + changement de contreparties
```

## Contreparties bancaires

Pour les PME, les instruments sont proposés par les **banques commerciales** (BNP, Crédit Agricole, Société Générale, LCL, etc.). Ne jamais utiliser :
- Brokers non régulés
- Plateformes FX "grand public" (pour entreprise)
- Instruments exotiques non compris du CFO

## Fiscalité

Les gains/pertes sur dérivés de couverture sont traités fiscalement en **symétrie** avec l'élément couvert :
- Gains change sur vente export : imposable en N (année de réalisation)
- Pertes change sur emprunt devises : déductible en N

Attention aux **dérivés spéculatifs** (non affectés à une couverture) : règles fiscales différentes, risque de non-déductibilité.

## Adaptation par audience

**Mode EC** : accompagnement de la mise en place de la politique + aide à la valorisation annuelle des positions en MTM.

**Mode PME** : souvent zone de risque **sous-traitée à la banque** sans expertise CFO. Insister sur la nécessité de comprendre les instruments avant signature.

## Orchestration

- Positions de couverture valorisées mensuellement et reportées à `cfo-reporting`
- Risque de change / taux inclus dans la cartographie `cfo-risques-conformite`
- Pour les groupes : renvoyer à `cfo-fiscalite` pour le transfer pricing des swaps intragroupe

## Limites de ce skill

Ce skill **n'exécute pas** les opérations de couverture. Il aide à :
- Identifier l'exposition
- Rédiger la politique
- Valoriser les positions existantes

**Pour l'exécution** : contacter la salle des marchés de votre banque. Pour les groupes avec exposition significative : recruter un trésorier dédié ou externaliser à un cabinet spécialisé (ex. Cap Hedge, Quote).
