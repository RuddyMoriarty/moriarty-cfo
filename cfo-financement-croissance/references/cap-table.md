# Cap Table & Equity Management

## Cap Table : structure

Tableau récapitulatif de la **répartition du capital** entre les actionnaires.

### Format standard

| Actionnaire | Type | Nb actions | % capital | Date entrée | Prix d'entrée | Investissement |
|-------------|------|------------|-----------|-------------|---------------|----------------|
| Fondateur 1 | Ord. | 250 000 | 25% | 2020-01-15 | 0,01 € | 2 500 € |
| Fondateur 2 | Ord. | 250 000 | 25% | 2020-01-15 | 0,01 € | 2 500 € |
| BSPCE pool | Options | 100 000 | 10% | 2021-06-01 | 0,01 € | — (vesting) |
| Seed VC X | Pref. A | 200 000 | 20% | 2022-09-01 | 5 € | 1 000 000 € |
| Série A VC Y | Pref. B | 200 000 | 20% | 2024-03-01 | 30 € | 6 000 000 € |
| **Total** | | **1 000 000** | **100%** | | | **7 005 000 €** |

## Types d'actions

### Ordinaires

Détenues par les fondateurs, salariés via BSPCE/AGA. Pas de droits préférentiels.

### Préférence (Preferred)

Détenues par les investisseurs. Droits :
- **Liquidation preference** : remboursés en premier en cas de cession
- **Anti-dilution** : protection contre baisse de valorisation
- **Veto** sur certaines décisions stratégiques

### Catégories typiques par tour

- **Série A** : Pref-A (1x non-participating typique)
- **Série B** : Pref-B (1x non-participating ou 1x participating cap 2x)
- **Série C+** : Pref-C, Pref-D...

## BSPCE (Bons de Souscription de Parts de Créateur d'Entreprise)

### Définition

Options d'achat d'actions accordées aux **salariés et dirigeants** de **PME < 15 ans**.

### Avantages

- Pas d'imposition à l'attribution (vs stock options classiques)
- Imposition uniquement à l'exercice (sur la plus-value)
- Régime favorable (forfait + prélèvements sociaux)

### Mécanisme

- **Strike price** : prix d'exercice (typiquement valeur fixée par auditeur)
- **Vesting** : maturation progressive (typiquement 4 ans avec cliff 1 an)
- **Cliff** : période minimum avant qu'aucune option ne mature (1 an typique)
- **Vesting mensuel** : après le cliff, 1/48e des options par mois (pour vesting 4 ans)

### Exemple

Salarié reçoit 4 800 BSPCE en juin 2025. Strike 1 €. Vesting 4 ans, cliff 1 an.

- Juin 2026 (cliff) : 1 200 BSPCE matures
- Juillet 2026 - Mai 2030 : +100 BSPCE / mois
- Juin 2030 : 4 800 BSPCE matures (fin)

Si le salarié part en mars 2027 (1 an et 9 mois après attribution) : 1 200 + 100 × 9 = 2 100 BSPCE matures, le reste annulé.

À l'exercice : achat à 1 € l'unité. Si valeur à 10 €/action → plus-value 9 €/action × 2 100 = 18 900 € imposables.

## AGA (Actions Gratuites)

Alternative aux BSPCE.

- Attribution gratuite d'actions au salarié
- Vesting (typiquement 1 an attribution + 1 an conservation = 2 ans min)
- Imposition à l'attribution (calculée sur valeur à la date attribution) + à la cession

Moins flexible que BSPCE mais possible pour les sociétés > 15 ans.

## Anti-dilution

Mécanisme protégeant les investisseurs contre une **baisse de valorisation** lors d'un futur tour (down round).

### Full ratchet

L'investisseur récupère des actions comme s'il avait investi au nouveau prix.

Très protecteur pour l'investisseur, **dilution massive des fondateurs** en cas de down round. Rare dans les term sheets actuels.

### Weighted Average Broad-Based

Formule pondérée tenant compte du nombre d'actions au moment du down round.

```
Nouveau prix = Ancien prix × (Nb actions avant + Nb actions au prix moyen) / (Nb actions avant + Nb actions au nouveau prix)
```

Standard du marché. Plus équilibré.

### Weighted Average Narrow-Based

Idem mais excluant les options non exercées du calcul. Plus protecteur pour l'investisseur.

## Ratchet (clause sur exit)

Clause permettant à un VC d'augmenter sa part en cas de **performance insuffisante** à l'exit (vs target initial).

Forme :
- Si exit < X M€ → VC reçoit Y% supplémentaire
- Si exit > X M€ → pas de ratchet

Demande agressive des VCs en période difficile. À négocier serré.

## Pre-emption rights (ROFR / ROFO)

### ROFR (Right of First Refusal)

Si un actionnaire veut céder ses titres → les autres actionnaires ont le droit de **racheter en priorité** au même prix.

### ROFO (Right of First Offer)

Si un actionnaire veut céder → il doit d'abord **proposer aux autres actionnaires** avant d'aller chercher un acheteur tiers.

## Drag-along & Tag-along

### Drag-along (entraînement)

Si un actionnaire majoritaire (souvent ≥ 75%) accepte une offre de rachat → **peut forcer les autres** à vendre aussi.

Permet d'éviter les blocages minoritaires lors de l'exit.

### Tag-along (sortie conjointe)

Si un actionnaire majoritaire vend → les minoritaires peuvent se **joindre à la vente** aux mêmes conditions.

Protection des minoritaires.

## Vesting fondateurs

Souvent imposé par les VCs au seed / série A :
- Vesting 4 ans
- Cliff 12 mois
- Si fondateur part avant fin du vesting : actions non vested **rachetées** par la société à la valeur nominale

But : éviter qu'un fondateur parte avec 25% du capital après 6 mois.

## Pacte d'actionnaires

Document juridique consolidant tous les droits/obligations entre actionnaires :
- Composition du board
- Quorum / majorités pour décisions
- Liquidation preference
- Anti-dilution
- ROFR / ROFO / Tag / Drag
- Vesting
- Non-concurrence / non-sollicitation
- Confidentialité
- Sortie / liquidité

**Indispensable** pour toute société avec > 1 actionnaire significatif.

## Outils de cap table management

| Outil | Usage |
|-------|-------|
| **Carta** | Standard US, multi-juridictions |
| **Eqvista** | Alternative Carta |
| **Captable.io** | Outil simple gratuit |
| Excel / Google Sheets | OK pour PME jusqu'à 5-10 actionnaires |

Pour les rounds > 1 M€ : recommandé d'utiliser un outil dédié (track des options, vesting, scenarios).

## Adaptation par audience

**Mode EC** : accompagnement de la structuration cap table en mission contractuelle. Coordination avec l'avocat business.

**Mode PME / fondateur** : votre cap table est **votre santé financière personnelle**. La maintenir à jour, comprendre chaque dilution. **Avocat business obligatoire** pour toute modification structurante.

## Avertissement

Les sujets cap table / equity sont **complexes juridiquement**. Ce skill donne les bases. Pour toute opération réelle (BSPCE, levée, anti-dilution, etc.) : **avocat business spécialisé M&A obligatoire**.
