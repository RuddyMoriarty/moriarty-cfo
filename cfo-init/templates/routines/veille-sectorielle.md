# Veille sectorielle {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}
**Secteur NAF** : {{code_naf}} ({{libelle_naf}})
**Catégorie** : {{secteur_category}}

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Secteur : {{libelle_naf}} (code NAF {{code_naf}})
- Taille : {{taille}}
- Sources revuées ce mois : Xerfi, Insee, Banque de France, fédérations professionnelles, presse économique spécialisée, notes de conjoncture sectorielles
- Nombre de publications analysées : {{nb_publications}}

## Hypothèses

- H1 : les benchmarks sectoriels publiés (marges, rotations, ratios) reflètent la situation observée 6 à 12 mois avant la publication
- H2 : les données concurrentielles sont issues des dépôts de comptes au greffe et peuvent avoir 12 à 18 mois de décalage
- H3 : les projections de marché sont des scénarios, pas des engagements

## Analyse

### Indicateurs macro-sectoriels

| Indicateur | Valeur actuelle | Evolution YoY | Source |
|------------|-----------------|---------------|--------|
| Taille de marché (France) | {{taille_marche}} | {{taille_yoy}}% | {{source_marche}} |
| Croissance sectorielle | {{croiss_secteur}}% | - | {{source_croiss}} |
| Indice des prix du secteur | {{indice_prix}} | {{prix_yoy}}% | Insee |
| Taux de défaillance | {{taux_def}}% | {{def_yoy}} pt | Banque de France |
| Délais de paiement moyens | {{delai_paiement}} j | {{delai_yoy}} j | Observatoire DPE |

### Mouvements concurrentiels du mois

| Acteur | Événement | Date | Impact potentiel |
|--------|-----------|------|------------------|
| {{concu_1_nom}} | {{concu_1_event}} | {{concu_1_date}} | {{concu_1_impact}} |
| {{concu_2_nom}} | {{concu_2_event}} | {{concu_2_date}} | {{concu_2_impact}} |
| {{concu_3_nom}} | {{concu_3_event}} | {{concu_3_date}} | {{concu_3_impact}} |

Types d'événements suivis : levées de fonds, M&A, changements de direction, lancements produits, restructurations, mises en liquidation.

### Benchmarks financiers sectoriels

| KPI sectoriel | Médiane secteur | {{denomination}} | Position |
|---------------|-----------------|-------------------|----------|
| Marge brute | {{mb_med}}% | {{mb_moi}}% | {{position_mb}} |
| Marge EBE | {{ebe_med}}% | {{ebe_moi}}% | {{position_ebe}} |
| DSO | {{dso_med}} j | {{dso_moi}} j | {{position_dso}} |
| DPO | {{dpo_med}} j | {{dpo_moi}} j | {{position_dpo}} |
| BFR (% CA) | {{bfr_med}}% | {{bfr_moi}}% | {{position_bfr}} |
| Croissance YoY | {{croiss_med}}% | {{croiss_moi}}% | {{position_croiss}} |

### Réglementations sectorielles du mois

- {{reg_1_titre}} : {{reg_1_desc}}. EEV : {{reg_1_eev}}.
- {{reg_2_titre}} : {{reg_2_desc}}. EEV : {{reg_2_eev}}.

### Signaux faibles à surveiller

- {{signal_1}}
- {{signal_2}}
- {{signal_3}}

## Risques

- {{risque_1_niveau}} Consolidation sectorielle accélérée : {{risque_1_desc}}
- {{risque_2_niveau}} Entrée d'un nouvel acteur international sur le marché : {{risque_2_desc}}
- {{risque_3_niveau}} Changement de régulation pesant sur les marges : {{risque_3_desc}}

## Actions

- [ ] Intégrer les benchmarks actualisés dans le prochain dashboard CFO
- [ ] Analyser les décisions stratégiques des concurrents directs (top 3) et leurs implications
- [ ] Communiquer les mouvements significatifs au comité de direction
- [ ] Surveiller la base clients pour détecter les signes de changement de comportement
- [ ] Mettre à jour le SWOT de {{denomination}} si signaux forts détectés
- [ ] Adapter la stratégie pricing si position concurrentielle dégradée sur le mois

## Limites

Cette veille agrège des informations publiques ou semi-publiques. Elle ne permet pas de connaître les stratégies internes des concurrents (pricing privé, politique salariale, R&D). Les benchmarks sectoriels sont des médianes ou moyennes et ne reflètent pas la diversité des modèles économiques d'un secteur. Pour une étude concurrentielle approfondie ou un positionnement stratégique, recourir à un cabinet de conseil spécialisé (Xerfi, Precepta, cabinets sectoriels). Les signaux faibles restent par nature incertains : ils méritent surveillance mais ne justifient pas d'action unilatérale.
