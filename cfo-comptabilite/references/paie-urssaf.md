# Sub-module HR / Paie / URSSAF

Activé si `private/company.json > classification.effectif_estime > 0`.

Ce skill **coordonne** la comptabilité paie ; la production paie elle-même reste dans l'outil dédié (Silae, Nibelis, Tiime, ADP, etc.).

## DSN, Déclaration Sociale Nominative

### Obligation

Déclaration **mensuelle unique** qui remplace la quasi-totalité des déclarations sociales antérieures (DADS-U, DUCS, AE…).

### Échéances

| Effectif | Échéance mensuelle |
|----------|---------------------|
| < 50 salariés | **15 du mois suivant** |
| ≥ 50 salariés | **5 du mois suivant** |

Pour une DSN de mars, l'échéance tombe :
- 5 avril (si ≥ 50 salariés)
- 15 avril (si < 50 salariés)

Ces échéances sont générées automatiquement par `cfo-init/scripts/compute_calendar.py` selon l'effectif et incluses dans `private/calendar-fiscal.json`.

### Événements à déclarer

Dans la DSN mensuelle :
- Rémunérations et cotisations (URSSAF, retraite complémentaire, prévoyance)
- Fin de contrat (départ de salarié, licenciement, rupture conventionnelle)
- Arrêts de travail (maladie, accident, maternité)
- Reprise du travail après arrêt

**DSN événementielle** pour : arrêt de travail > 3 jours, fin de contrat.

## URSSAF

### Cotisations principales 2026 (taux indicatifs)

| Cotisation | Taux employeur | Taux salarié | Assiette |
|------------|----------------|--------------|----------|
| Maladie, maternité, invalidité, décès | 7% (ou 13% si rémunération > 2,5 SMIC) | 0% | Salaire brut |
| Vieillesse plafonnée | 8,55% | 6,90% | Salaire brut jusqu'à PSS |
| Vieillesse déplafonnée | 2,02% | 0,40% | Salaire brut total |
| Allocations familiales | 3,45% (ou 5,25% si > 3,5 SMIC) | 0% | Salaire brut |
| AT/MP | Variable (code risque) | 0% | Salaire brut |
| CSG-CRDS | 0% | 9,70% | 98,25% du salaire brut |
| FNAL | 0,10% ou 0,50% | 0% | Salaire brut |
| Dialogue social | 0,016% | 0% | Salaire brut |
| Versement transport | Variable (commune) | 0% | Salaire brut, si effectif ≥ 11 |
| Formation continue | 0,55% (< 11 sal) / 1% (≥ 11 sal) | 0% | Masse salariale |
| Taxe d'apprentissage | 0,68% | 0% | Masse salariale |

### Plafond de la Sécurité Sociale (PSS)

- **2026** : 3 925 €/mois (soit 47 100 €/an), **valeurs 2025, à vérifier**
- Le PSS sert d'assiette pour certaines cotisations (vieillesse plafonnée, retraite ARRCO tranches)

> ⚠️ **Fraîcheur** : ces taux et montants sont **à actualiser chaque année**. Vérifier sur urssaf.fr et boss.gouv.fr avant toute communication.

## Écritures comptables de paie

### Modèle standard (sous ventilation)

```
641 Rémunérations du personnel           10 000,00
645 Charges de sécurité sociale          4 500,00
    421 Personnel - Rémunérations dues   8 000,00  (net à payer)
    431 Sécurité sociale                 4 000,00
    437 Autres organismes sociaux        1 500,00
    4421 Impôt sur le revenu (PAS)        1 000,00  (prélèvement à la source)
```

Puis à la date de paiement :
```
421 Personnel - Rémunérations dues       8 000,00
    512 Banques                          8 000,00
```

Et pour les cotisations sociales (aux échéances URSSAF) :
```
431 Sécurité sociale                     4 000,00
437 Autres organismes sociaux            1 500,00
4421 Impôt sur le revenu (PAS)            1 000,00
    512 Banques                          6 500,00
```

## Intéressement, participation, PEE / PERCO

### Intéressement (art. L. 3312-1 C. trav.)

- Dispositif **facultatif**
- Formule de calcul défini par accord (prime individuelle selon CA, résultat, objectifs)
- Exonéré de cotisations sociales (sauf CSG-CRDS + forfait social 20% au-delà de 250 sal)
- Écriture :
  ```
  647 Autres charges sociales    2 000,00
      424 Intéressement à payer  2 000,00
  ```

### Participation (art. L. 3321-1 C. trav.)

- Dispositif **obligatoire** pour les entreprises de **50+ salariés** (seuil atteint pendant 5 ans consécutifs)
- Formule légale : RSP = 0,5 × (B - 0,05 × C) × (S / VA) avec :
  - B = bénéfice net fiscal
  - C = capitaux propres
  - S = salaires
  - VA = valeur ajoutée
- Distribuée aux salariés ou affectée à un PEE/PERCO
- Exonérée d'IS et de cotisations sociales (sauf CSG-CRDS + forfait social)

### PEE / PERCO

- Plan d'Épargne Entreprise (PEE) : blocage 5 ans, sauf cas de déblocage anticipé
- PERCO (ex-PERCO, aujourd'hui PER Collectif) : blocage jusqu'à la retraite
- Abondement employeur possible (jusqu'à 3 × versement salarié, plafond PSS)

## Taxes annuelles liées à la paie

### Taxe d'apprentissage

- **0,68% de la masse salariale** (dont 0,59% via SOLTéA + 0,09% via la CUFPA)
- Échéance **solde** : **5 mai** de l'année suivante
- Plateforme SOLTéA pour la répartition aux établissements de formation

### Participation à la Formation Professionnelle Continue (FPC)

- **< 11 salariés** : 0,55% de la masse salariale
- **≥ 11 salariés** : 1% de la masse salariale (voire plus selon accord de branche)
- Échéance : 5 mai (via CUFPA)

### Effort de construction (PEEC, "1% logement")

- **Effectif ≥ 50 salariés** : 0,45% de la masse salariale (rien si < 50)
- Échéance : 30 avril de l'année suivante
- Versement à un organisme collecteur (Action Logement Services)

## Plans sociaux / ruptures conventionnelles

Scope ad-hoc. Ce skill peut :
- Aider à **quantifier le coût d'un licenciement** (indemnités légales ou conventionnelles)
- Préparer les **écritures de provision pour restructuration** (si décision prise avant clôture)
- Coordonner avec le service juridique / l'avocat social

**Non couvert** : rédaction des documents RH (convocations, lettres de rupture, PSE). Renvoyer à un avocat social.

## Achievement

Pas d'achievement dédié HR/Paie en v0.1. À ajouter en v0.2 : `payroll-clean` (3 DSN consécutives sans anomalie).

## Adaptation par audience

**Mode EC** : votre cabinet a probablement une spécialité sociale / paie dédiée. Ce skill sert à **coordonner** la partie comptable (écritures de paie) avec la partie sociale (DSN, URSSAF).

**Mode PME** : si vous avez un prestataire paie externe, ce skill vous aide à vérifier la cohérence mensuelle. Si paie en interne, renforcer la formation continue du collaborateur paie.

## Renvoi

- Valeurs 2026 à vérifier : urssaf.fr, boss.gouv.fr, legifrance
- Pour les questions RH complexes : avocat social
- Pour la paie opérationnelle : outil dédié (Silae, Nibelis, Tiime, Pennylane Paie)
