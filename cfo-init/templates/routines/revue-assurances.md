# Revue annuelle des assurances {{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Exercice** : {{yyyy}}
**Généré le** : {{date_today}} (cycle J-15 avant renouvellement fin d'année)

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Activité principale : {{activite}}
- Effectif : {{effectif}}
- CA annuel : {{ca_annuel}}
- Taille des locaux : {{m2_locaux}} m², nombre de sites : {{nb_sites}}
- Filiales : {{nb_filiales}}
- Date de revue précédente : {{date_revue_prev}}

## Hypothèses

- H1 : les polices en portefeuille au {{date_today}} reflètent les besoins actuels de {{denomination}}
- H2 : l'évolution de l'activité (CA, effectif, sites) depuis la dernière revue a été communiquée aux assureurs
- H3 : la sinistralité déclarée sur les 12 derniers mois est à jour dans les relevés assureurs

## Analyse

### Matrice des polices en portefeuille

| Police | Assureur | Couverture | Franchise | Prime annuelle | Echéance | Statut |
|--------|----------|------------|-----------|----------------|----------|--------|
| RC pro (exploitation) | {{rc_pro_assureur}} | {{rc_pro_couv}} | {{rc_pro_fr}} | {{rc_pro_prime}} | {{rc_pro_ech}} | {{rc_pro_statut}} |
| RC mandataires sociaux | {{rc_man_assureur}} | {{rc_man_couv}} | {{rc_man_fr}} | {{rc_man_prime}} | {{rc_man_ech}} | {{rc_man_statut}} |
| Multirisque pro | {{mrp_assureur}} | {{mrp_couv}} | {{mrp_fr}} | {{mrp_prime}} | {{mrp_ech}} | {{mrp_statut}} |
| Cyber-risques | {{cyber_assureur}} | {{cyber_couv}} | {{cyber_fr}} | {{cyber_prime}} | {{cyber_ech}} | {{cyber_statut}} |
| Perte d'exploitation | {{pe_assureur}} | {{pe_couv}} | {{pe_fr}} | {{pe_prime}} | {{pe_ech}} | {{pe_statut}} |
| Dommages matériels | {{dm_assureur}} | {{dm_couv}} | {{dm_fr}} | {{dm_prime}} | {{dm_ech}} | {{dm_statut}} |
| Flotte automobile | {{auto_assureur}} | {{auto_couv}} | {{auto_fr}} | {{auto_prime}} | {{auto_ech}} | {{auto_statut}} |
| Homme-clé | {{hc_assureur}} | {{hc_couv}} | {{hc_fr}} | {{hc_prime}} | {{hc_ech}} | {{hc_statut}} |

Prime totale annuelle : {{prime_totale}} EUR, soit {{prime_pct_ca}}% du CA.

### Polices à renouveler dans les 90 prochains jours

1. **{{renew_1_titre}}** (expire le {{renew_1_date}}). Prime en hausse de {{renew_1_evol}}%. Action avant le {{renew_1_action}}.
2. **{{renew_2_titre}}** (expire le {{renew_2_date}}). Prime en hausse de {{renew_2_evol}}%. Action avant le {{renew_2_action}}.

### Sinistralité sur 12 mois

- Nombre de déclarations : {{nb_sinistres}}
- Montant total des déclarations : {{montant_sinistres}}
- Montant remboursé par les assureurs : {{montant_rembourse}}
- Taux de sinistralité : {{taux_sinistralite}}%

### Lacunes de couverture identifiées

| Domaine | Lacune | Impact potentiel | Recommandation |
|---------|--------|------------------|----------------|
| {{lac_1_dom}} | {{lac_1_desc}} | {{lac_1_impact}} | {{lac_1_reco}} |
| {{lac_2_dom}} | {{lac_2_desc}} | {{lac_2_impact}} | {{lac_2_reco}} |

## Risques

- {{risque_1_niveau}} Absence de police cyber en cas d'attaque, coût potentiel {{cout_cyber_estime}}
- {{risque_2_niveau}} Sous-assurance multirisque (capital assuré < valeur réelle des biens) déclenchant la règle proportionnelle en cas de sinistre
- {{risque_3_niveau}} Franchise trop élevée sur perte d'exploitation : impact sur la trésorerie en cas d'interruption
- {{risque_4_niveau}} Clause homme-clé absente alors que {{nb_hommes_cles}} personnes clés identifiées

## Actions

- [ ] Demander 3 devis concurrents avant renouvellement sur les polices en hausse supérieure à 10%
- [ ] Mettre à jour la déclaration d'activité auprès des assureurs (CA actualisé, sites, effectif)
- [ ] Compléter les couvertures manquantes identifiées (cyber, homme-clé si applicable)
- [ ] Vérifier l'alignement entre les franchises et la capacité financière de {{denomination}} à absorber un sinistre
- [ ] Archiver les attestations et contrats dans le dossier assurances {{yyyy}}
- [ ] Former les équipes sur les procédures de déclaration sinistre (délais, pièces)

## Limites

Cette revue est un outil de pilotage et de préparation au renouvellement. Elle ne se substitue pas au conseil d'un courtier en assurances, particulièrement pour l'analyse juridique des exclusions contractuelles et la négociation des clauses. Les garanties effectives dépendent de la rédaction précise de chaque police. Pour une refonte complète du programme d'assurance, travailler avec un courtier grossiste ou un consultant spécialisé. La sinistralité évoquée provient des données assureur et peut différer de l'historique interne de {{denomination}}.
