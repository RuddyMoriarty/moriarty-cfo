# Éliminations intercos {{period_label}}, {{denomination}}

**SIREN** : {{siren}} (entité consolidante)
**Période** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}

## Faits

- Entité consolidante : {{denomination}}, SIREN {{siren}}
- Nombre d'entités en périmètre consolidé : {{nb_entites}}
- Période couverte : mouvements du mois {{mm}}/{{yyyy}}, stocks réconciliés au {{date_reconciliation}}
- Nombre de relations bilatérales à réconcilier : {{nb_relations}}

## Hypothèses

- H1 : chaque entité a fourni une balance des comptes tiers intra-groupe arrêtée au {{date_balance_filiales}}
- H2 : les écarts de conversion de change sont isolés et comptabilisés en écart de conversion groupe (IAS 21)
- H3 : les écarts inférieur à 1 k EUR sont tolérés et impactent les réserves consolidées sans investigation

## Analyse

### Matrice des flux intercos (en k EUR)

| Débiteur / Créditeur | {{ent_a}} | {{ent_b}} | {{ent_c}} | {{ent_d}} | Total |
|----------------------|-----------|-----------|-----------|-----------|-------|
| {{ent_a}} | - | {{flux_ab}} | {{flux_ac}} | {{flux_ad}} | {{total_a_deb}} |
| {{ent_b}} | {{flux_ba}} | - | {{flux_bc}} | {{flux_bd}} | {{total_b_deb}} |
| {{ent_c}} | {{flux_ca}} | {{flux_cb}} | - | {{flux_cd}} | {{total_c_deb}} |
| {{ent_d}} | {{flux_da}} | {{flux_db}} | {{flux_dc}} | - | {{total_d_deb}} |

La matrice doit être symétrique : le montant dû par A à B doit égaler le montant à recevoir par B de A.

### Éliminations à passer ce mois

| Type d'élimination | Débiteur / Source | Créditeur / Destination | Montant | Retraité ? |
|---------------------|-------------------|------------------------|---------|------------|
| CA intra-groupe | {{ca_source}} | {{ca_dest}} | {{ca_elim_montant}} | {{ca_retraite}} |
| Achats intra-groupe | {{ach_source}} | {{ach_dest}} | {{ach_elim_montant}} | {{ach_retraite}} |
| Dividendes reçus | {{div_source}} | {{div_dest}} | {{div_elim_montant}} | {{div_retraite}} |
| Intérêts intra-groupe | {{int_source}} | {{int_dest}} | {{int_elim_montant}} | {{int_retraite}} |
| Refacturation management fees | {{mgt_source}} | {{mgt_dest}} | {{mgt_elim_montant}} | {{mgt_retraite}} |
| Créances clients intercos | {{cc_source}} | {{cc_dest}} | {{cc_elim_montant}} | {{cc_retraite}} |
| Dettes fournisseurs intercos | {{df_source}} | {{df_dest}} | {{df_elim_montant}} | {{df_retraite}} |
| Marge en stock | {{ms_source}} | {{ms_dest}} | {{ms_elim_montant}} | {{ms_retraite}} |
| Prêts intra-groupe | {{pret_source}} | {{pret_dest}} | {{pret_elim_montant}} | {{pret_retraite}} |

### Écarts de réconciliation détectés

| Relation | Montant côté A | Montant côté B | Écart | Cause identifiée |
|----------|----------------|----------------|-------|------------------|
| {{ecart_1_relation}} | {{ecart_1_a}} | {{ecart_1_b}} | {{ecart_1_delta}} | {{ecart_1_cause}} |
| {{ecart_2_relation}} | {{ecart_2_a}} | {{ecart_2_b}} | {{ecart_2_delta}} | {{ecart_2_cause}} |
| {{ecart_3_relation}} | {{ecart_3_a}} | {{ecart_3_b}} | {{ecart_3_delta}} | {{ecart_3_cause}} |

Causes fréquentes : cut-off, facture en transit, TVA non retraitée, différence de change, litige commercial, erreur de saisie.

### Synthèse des retraitements

- Total des éliminations de CA : {{total_elim_ca}} k EUR
- Total des éliminations d'achats : {{total_elim_ach}} k EUR
- Impact sur le résultat consolidé : {{impact_resultat}} k EUR
- Marge en stock à éliminer : {{marge_stock_elim}} k EUR
- Créances et dettes intra-groupe éliminées au bilan : {{total_bilan_elim}} k EUR

### Marge en stock sur produits intra-groupe

| Entité détentrice | Produit | Stock valorisé | Marge intra incluse | Retraitement |
|-------------------|---------|----------------|---------------------|---------------|
| {{ms_det_1}} | {{ms_prod_1}} | {{ms_val_1}} | {{ms_marge_1}} | {{ms_retr_1}} |
| {{ms_det_2}} | {{ms_prod_2}} | {{ms_val_2}} | {{ms_marge_2}} | {{ms_retr_2}} |

## Risques

- {{risque_1_niveau}} Écart non réconcilié supérieur à 1 k EUR : suspicion d'erreur de saisie ou de cut-off mal géré
- {{risque_2_niveau}} TVA intra-groupe non neutralisée : impact sur les calculs de CA consolidé
- {{risque_3_niveau}} Opération significative non identifiée (apport, prêt, cession intra-groupe) pouvant fausser le bilan consolidé

## Actions

- [ ] Investiguer les écarts non expliqués avec les contrôleurs de gestion des entités concernées
- [ ] Passer les OD d'éliminations sur l'outil de consolidation (SAP BPC, LucaNet, Tagetik, Oracle HFM ou autre)
- [ ] Valider les éliminations avec le responsable consolidation et l'EC
- [ ] Documenter chaque écart persistant pour audit trail
- [ ] Mettre à jour les procédures intercos si récurrence des mêmes erreurs mois sur mois
- [ ] Transmettre le récapitulatif des éliminations au CAC consolidé si demande

## Limites

Les éliminations sont techniques et nécessitent une connaissance fine des normes de consolidation (PCG section VIII, IFRS 10-11-12). Les écarts persistants doivent être documentés dans une note de revue avant validation. Cette routine ne couvre pas les impôts différés intra-groupe ni les opérations de restructuration (fusion, apport partiel d'actif, cession de titres) qui nécessitent un traitement dédié. Pour primo-consolidation ou acquisition, recourir à un consultant en consolidation pour modéliser correctement la première intégration.
