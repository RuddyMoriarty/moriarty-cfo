# Variance analysis {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période analysée** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}

## Faits

- Exercice en cours : {{yyyy}}
- Mois sous revue : {{mm}}/{{yyyy}}
- Budget de référence : budget voté {{date_budget}} (révision MAT incluse)
- Données réelles : balance clôturée au {{date_cloture_balance}}
- Seuil de matérialité retenu : écart supérieur à {{seuil_materialite}} EUR ou {{seuil_pct}}% du poste

## Hypothèses

- H1 : la comparaison est effectuée entre le réel mensuel et la quote-part mensuelle du budget annuel (budget linéarisé sauf ligne saisonnière explicitement pondérée)
- H2 : la saisonnalité appliquée au budget est celle du réel N-1 sauf mention contraire dans le budget voté
- H3 : les écritures exceptionnelles sont identifiées et exclues de l'analyse YTD pour ne pas polluer les tendances

## Analyse

### Top 5 variances positives (favorables)

| Rang | Poste | Budget mensuel | Réel | Ecart | % | Cause identifiée |
|------|-------|----------------|------|-------|---|------------------|
| 1 | {{fav_1_poste}} | {{fav_1_budget}} | {{fav_1_reel}} | +{{fav_1_ecart}} | +{{fav_1_pct}}% | {{fav_1_cause}} |
| 2 | {{fav_2_poste}} | {{fav_2_budget}} | {{fav_2_reel}} | +{{fav_2_ecart}} | +{{fav_2_pct}}% | {{fav_2_cause}} |
| 3 | {{fav_3_poste}} | {{fav_3_budget}} | {{fav_3_reel}} | +{{fav_3_ecart}} | +{{fav_3_pct}}% | {{fav_3_cause}} |
| 4 | {{fav_4_poste}} | {{fav_4_budget}} | {{fav_4_reel}} | +{{fav_4_ecart}} | +{{fav_4_pct}}% | {{fav_4_cause}} |
| 5 | {{fav_5_poste}} | {{fav_5_budget}} | {{fav_5_reel}} | +{{fav_5_ecart}} | +{{fav_5_pct}}% | {{fav_5_cause}} |

### Top 5 variances négatives (défavorables)

| Rang | Poste | Budget mensuel | Réel | Ecart | % | Cause identifiée |
|------|-------|----------------|------|-------|---|------------------|
| 1 | {{def_1_poste}} | {{def_1_budget}} | {{def_1_reel}} | -{{def_1_ecart}} | -{{def_1_pct}}% | {{def_1_cause}} |
| 2 | {{def_2_poste}} | {{def_2_budget}} | {{def_2_reel}} | -{{def_2_ecart}} | -{{def_2_pct}}% | {{def_2_cause}} |
| 3 | {{def_3_poste}} | {{def_3_budget}} | {{def_3_reel}} | -{{def_3_ecart}} | -{{def_3_pct}}% | {{def_3_cause}} |
| 4 | {{def_4_poste}} | {{def_4_budget}} | {{def_4_reel}} | -{{def_4_ecart}} | -{{def_4_pct}}% | {{def_4_cause}} |
| 5 | {{def_5_poste}} | {{def_5_budget}} | {{def_5_reel}} | -{{def_5_ecart}} | -{{def_5_pct}}% | {{def_5_cause}} |

### Investigation des 3 principales variances

#### Variance 1 : {{inv_1_poste}} (écart {{inv_1_ecart}})

- Contexte : {{inv_1_contexte}}
- Cause principale : {{inv_1_cause_principale}}
- Cause secondaire : {{inv_1_cause_secondaire}}
- Impact sur l'atterrissage annuel : {{inv_1_impact_annuel}}
- Caractère : {{inv_1_caractere}} (ponctuel, structurel, cyclique)

#### Variance 2 : {{inv_2_poste}} (écart {{inv_2_ecart}})

- Contexte : {{inv_2_contexte}}
- Cause principale : {{inv_2_cause_principale}}
- Cause secondaire : {{inv_2_cause_secondaire}}
- Impact sur l'atterrissage annuel : {{inv_2_impact_annuel}}
- Caractère : {{inv_2_caractere}}

#### Variance 3 : {{inv_3_poste}} (écart {{inv_3_ecart}})

- Contexte : {{inv_3_contexte}}
- Cause principale : {{inv_3_cause_principale}}
- Cause secondaire : {{inv_3_cause_secondaire}}
- Impact sur l'atterrissage annuel : {{inv_3_impact_annuel}}
- Caractère : {{inv_3_caractere}}

### Synthèse globale

- Impact net des variances sur l'EBE mensuel : {{impact_ebe_mensuel}}
- Impact projeté sur l'EBE annuel : {{impact_ebe_annuel}}
- Variances structurelles (à intégrer dans le MAT) : {{var_structurelles}}
- Variances ponctuelles (sans impact long terme) : {{var_ponctuelles}}

## Risques

- {{risque_1_niveau}} Si les variances défavorables sont structurelles, impact sur les primes variables et les covenants en fin d'exercice
- {{risque_2_niveau}} Si les variances favorables sont ponctuelles, attention à ne pas surcalibrer les prévisions T+1

## Actions

- [ ] Déclencher un plan correctif sur les postes en variance défavorable structurelle (top 3)
- [ ] Confirmer avec les opérationnels les causes identifiées (bris de silo)
- [ ] Mettre à jour le MAT avec les variances structurelles
- [ ] Communiquer les top 3 variances au comité de direction
- [ ] Remonter au contrôle de gestion les erreurs de saisie éventuelles pour correction

## Limites

L'analyse des variances repose sur la qualité de l'imputation comptable et de la linéarisation budgétaire. Un poste mal codifié peut fausser la variance sans refléter une réalité opérationnelle. Les causes identifiées sont des hypothèses de travail à valider auprès des opérationnels. Cette analyse n'est pas un audit : elle signale des écarts, elle ne les explique pas systématiquement. En cas d'écart très significatif inexpliqué, investigation approfondie avec l'EC recommandée.
