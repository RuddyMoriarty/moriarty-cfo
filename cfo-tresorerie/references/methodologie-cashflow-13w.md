# Méthodologie forecast 13 semaines

Le forecast 13 semaines est le **standard de l'industrie** pour la trésorerie court terme. Horizon ~3 mois, granularité hebdomadaire. Utilisé par les CFO de PME, scale-ups, et entreprises en restructuring.

## Pourquoi 13 semaines ?

- Horizon assez long pour **anticiper les tensions** (typiquement 30-60 jours à l'avance)
- Assez court pour rester **fiable** (au-delà, les hypothèses dérapent)
- 13 = 1 trimestre = période standard de reporting au CODIR / investisseurs / banques
- Utilisé obligatoirement dans les **plans de redressement** et négociations bancaires

## Structure du modèle

Tableau à 13 colonnes (une par semaine) + 1 colonne "Total" :

```
                         W1    W2    W3    W4    W5  ...  W13    Total
                         13/04 20/04 27/04 04/05 ...

SOLDE INITIAL            150k  142k  138k  120k  ...
━━━━━━━━━━━━━━━━━━━━━━
ENCAISSEMENTS
├─ Clients (facturation)  80k   60k  100k   40k  ...
├─ Clients (récurrent)    15k   15k   15k   15k  ...  15k    195k
├─ Subventions                              50k  ...          50k
├─ Autres encaissements    5k    0k   10k    5k  ...
━━━━━━━━━━━━━━━━━━━━━━
Total encaissements      100k   75k  125k  110k  ...

DÉCAISSEMENTS
├─ Salaires & charges      0k    0k   80k    0k  ...  80k    480k
├─ URSSAF                              40k  ...         40k   160k
├─ TVA                           25k              ...         75k
├─ Fournisseurs           60k   40k   45k   30k  ...
├─ Loyers                                    8k  ...          24k
├─ CAPEX                                    50k  ...          50k
├─ Remboursement prêts     0k    0k    3k    0k  ...
━━━━━━━━━━━━━━━━━━━━━━
Total décaissements      108k   80k  163k   83k  ...

Flux net de trésorerie    -8k   -5k  -38k  +27k  ...
SOLDE FINAL              142k  138k  120k  140k  ...
```

## Étapes de construction

### Étape 1 — Solde de départ (W0)

Solde bancaire **cumulé** au dernier jour du dimanche précédent (start de W1). Inclure :
- Tous les comptes courants (tous banques, tous pays)
- Les placements de trésorerie disponibles à court terme (SICAV monétaires, comptes à terme < 3 mois)
- **Exclure** les lignes de crédit non tirées (pas du cash disponible)

### Étape 2 — Encaissements

**Clients — factures émises non encore encaissées** :
- Lister toutes les factures avec échéance dans les 13 prochaines semaines
- Appliquer un taux d'encaissement réaliste (95% si portfolio B2B, 85% si B2C, 70% si gros compte public type administration)
- Projeter l'encaissement sur la semaine de l'échéance + 1-2 semaines (retard moyen client)

**Clients — facturation future** :
- Pour les contrats récurrents (SaaS abo) : projeter les prochaines dates de facturation
- Pour les contrats ponctuels : projeter selon carnet de commandes signées

**Subventions / CIR / crédit d'impôt** :
- CIR à recevoir : 4 mois après dépôt du dossier (PME < 150k€) ou 1 an (> 150k€)
- Subventions : vérifier date contractuelle de versement
- Aides publiques : cf. `cfo-financement-croissance` pour le pipeline

**Autres** : cession d'actifs, apport en compte courant, augmentation de capital

### Étape 3 — Décaissements

**Salaires & charges sociales** :
- Salaires nets : semaine de versement (fin de mois la plupart du temps)
- URSSAF : le 5 ou 15 du mois suivant selon effectif
- Retraite complémentaire, prévoyance : trimestriel (typiquement fin de mois)

**TVA** :
- Mensuel : 24 du mois suivant
- Trimestriel : 24 du mois suivant la fin du trimestre
- CA12 (simplifié) : acomptes juillet/décembre + solde 3-5 mois après clôture

**IS** :
- Acomptes trimestriels (15/03, 15/06, 15/09, 15/12 pour clôture 31/12)
- Solde : 15/05 pour clôture 31/12

**Fournisseurs** :
- Factures reçues à payer sous 30/45/60 jours (selon conditions)
- Factures récurrentes (loyers, abonnements, licences)
- Engagements fermes (contrats cadre, commandes validées)

**CAPEX** :
- Investissements décidés avec date de paiement ferme

**Remboursement d'emprunts** :
- Échéancier contractuel (capital + intérêts)

### Étape 4 — Calcul du flux net hebdomadaire

`Flux net W = Encaissements W - Décaissements W`

`Solde final W = Solde initial W + Flux net W = Solde initial W+1`

### Étape 5 — Identification du point bas

Parcourir les 13 colonnes et trouver **la semaine où le solde final est minimal**. C'est **le point critique**.

Si ce minimum < 0 → tension de trésorerie avérée.
Si ce minimum < seuil minimal défini (typiquement 1 mois de charges fixes) → alerte.

## Hypothèses à expliciter

| Hypothèse | Valeur défaut | À valider |
|-----------|--------------|-----------|
| Taux d'encaissement clients | 95% sur 60 jours | Historique société |
| Retard moyen payment clients | +7 à +15 jours vs échéance | Historique société |
| Taux de conversion pipeline | Filtrer ≥ "proposition signée" | CRM |
| Paiement des salaires | J = fin de mois | Contrats |
| Paiement URSSAF | J+15 mois suivant si < 50 sal, J+5 si ≥ 50 | effectif |
| CAPEX | Uniquement les décisions validées | Board |

## Qualité du forecast

Tracking mensuel : **écart entre forecast et réel** :
- < 5% → modèle fiable
- 5-15% → hypothèses à raffiner
- > 15% → revoir la méthodologie

## Adaptation par audience

**Mode EC** : produit le forecast pour le client (mission contractuelle). Bien documenter les hypothèses.

**Mode PME** : focus "actions hebdo" — chaque semaine, relire le forecast, mettre à jour les hypothèses avec la réalité écoulée.

## Orchestration

- `cfo-init` fournit le profil société (taille, secteur, régime TVA) qui affecte les échéances récurrentes
- `cfo-comptabilite` fournit la balance (créances clients, dettes fournisseurs à date)
- `cfo-fiscalite` fournit le planning IS / TVA
- `cfo-financement-croissance` prend le relais si tension détectée → diagnostic financement + CTA Moriarty si aides éligibles

## Achievement

`captain-cashflow` (+50 pts) au 1er forecast 13w livré.
