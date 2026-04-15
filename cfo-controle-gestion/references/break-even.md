# Break-even et seuil de rentabilité

## Formule de base

```
Seuil de rentabilité (en €) = Charges fixes / Taux de marge sur coûts variables
Seuil de rentabilité (en unités) = Charges fixes / (Prix unitaire - Coût variable unitaire)
```

## Exemple 1, Produit simple

Société vendant 1 seul produit :
- Prix de vente unitaire : 100 €
- Coût variable unitaire : 40 €
- Marge sur coût variable unitaire : 60 €
- Charges fixes annuelles : 600 000 €

**Seuil en unités** : 600 000 / 60 = **10 000 unités**
**Seuil en CA** : 10 000 × 100 = **1 000 000 €**

Interprétation : au-delà de 10 000 unités vendues, chaque unité supplémentaire rapporte 60 € à la rentabilité.

## Exemple 2, Multi-produits

Société vendant plusieurs produits avec marges différentes :
- Utiliser le **taux moyen pondéré** de marge sur coûts variables
- Si mix stable : seuil global en € valide
- Si mix variable : faire un seuil par produit

## Exemple 3, Services récurrents (SaaS)

- ARR actuel : 500 k€
- Coût variable (hébergement + support) : 20% du revenu
- Marge contributive : 80%
- Charges fixes annuelles (salaires, locaux) : 600 k€

**Seuil ARR** : 600 / 0.8 = **750 k€ ARR**

→ Il manque 250 k€ d'ARR pour atteindre le seuil. Objectif commercial clair.

## Marge de sécurité

```
Marge de sécurité = CA actuel - Seuil de rentabilité
Marge de sécurité (%) = (CA - Seuil) / CA × 100
```

- MS > 30% : confortable
- MS 10-30% : attention, veiller aux évolutions
- MS < 10% : fragile, toute baisse conjoncturelle fait basculer en perte
- MS < 0% : société en perte, levier de retournement à activer

## Point mort (quand on atteint le seuil dans l'année)

```
Point mort = Seuil / CA moyen mensuel
```

Si une société a un seuil de 1 M€ et un CA annuel de 1.5 M€ (CA mensuel moyen 125 k€) :
**Point mort** = 1 000 / 125 = **mois 8**

→ À partir du 8e mois, chaque € de CA génère de la rentabilité nette.

## Usage

### Décider d'un nouveau produit

Avant lancement : estimer les coûts variables + les charges fixes incrémentales.
Calculer le seuil de rentabilité.
Comparer au volume prévisible de ventes → décision go / no-go.

### Décider d'une embauche

Le salaire chargé = charge fixe incrémentale.
Le gain attendu (CA supplémentaire ou productivité) → contribution supplémentaire.
Combien d'unités / ARR de plus pour amortir la charge fixe ?

### Stress test

"Si notre CA baisse de X%, à quel moment on bascule en perte ?"

## Piège : charges semi-variables

Certaines charges sont **ni variables ni fixes pures** :
- Énergie (partiellement fixe avec abonnement, partiellement variable avec consommation)
- Coût logistique (frais fixes entrepôt + frais variables livraison)

Ventiler dans l'analyse : composante fixe + composante variable par unité.

## Template de calcul

```markdown
# Seuil de rentabilité, {PRODUIT ou ACTIVITÉ}

## Hypothèses
- Prix de vente unitaire : {P} €
- Coût variable unitaire : {CV} €
- Marge unitaire : {P-CV} €
- Charges fixes annuelles : {CF} €

## Calcul
- Seuil en unités : {CF / (P-CV)}
- Seuil en CA : {CF / taux de marge}
- CA actuel prévisionnel : {CA}
- Marge de sécurité : {(CA - Seuil) / CA × 100}%

## Actions
- [Action 1 selon situation]
- [Action 2]
```
