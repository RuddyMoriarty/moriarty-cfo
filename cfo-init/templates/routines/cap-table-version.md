# Cap table versioning T{{qq}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : T{{qq}} {{yyyy}}
**Généré le** : {{date_today}}

## Pourquoi

Actualisation trimestrielle de la table de capitalisation de {{denomination}} : actions en circulation, BSPCE et BSA non exercés, AGA, dilution scenarios. Document fondamental pour la préparation de levée, la communication aux investisseurs et la simulation d'exit.

## Chiffres clés

| KPI | Valeur actuelle | T{{qq_prev_1}} | Evolution |
|-----|-----------------|----------------|-----------|
| Nombre total d'actions en circulation | {{nb_actions}} | {{nb_actions_prev}} | {{delta_actions}} |
| Capital social | {{capital_social}} EUR | {{capital_prev}} EUR | - |
| Valeur nominale par action | {{vn_action}} EUR | - | - |
| BSPCE non exercés | {{nb_bspce}} | {{nb_bspce_prev}} | {{delta_bspce}} |
| AGA en période d'acquisition | {{nb_aga}} | {{nb_aga_prev}} | {{delta_aga}} |
| BSA non exercés | {{nb_bsa}} | {{nb_bsa_prev}} | {{delta_bsa}} |
| Dilution fully diluted | {{dilution_fd}}% | {{dilution_fd_prev}}% | - |
| Dernière valorisation (pre-money dernière levée) | {{valo_premoney}} k EUR | - | - |

## Structure actuelle du capital

### Répartition par catégorie d'actions

| Catégorie | Nombre d'actions | % capital | % fully diluted |
|-----------|------------------|-----------|-----------------|
| Actions ordinaires | {{ao_nb}} | {{ao_pct}}% | {{ao_fd_pct}}% |
| Actions de préférence série A | {{apa_nb}} | {{apa_pct}}% | {{apa_fd_pct}}% |
| Actions de préférence série B | {{apb_nb}} | {{apb_pct}}% | {{apb_fd_pct}}% |
| BSPCE (potentiel) | {{bspce_nb}} | - | {{bspce_fd_pct}}% |
| AGA (acquisition) | {{aga_nb}} | - | {{aga_fd_pct}}% |
| BSA (potentiel) | {{bsa_nb}} | - | {{bsa_fd_pct}}% |
| **Total fully diluted** | {{fd_total}} | - | 100% |

### Répartition par actionnaire (top 10)

| Actionnaire | Catégorie | Nombre d'actions | % capital | % FD |
|-------------|-----------|------------------|-----------|------|
| {{act_1_nom}} | {{act_1_cat}} | {{act_1_nb}} | {{act_1_pct}}% | {{act_1_fd}}% |
| {{act_2_nom}} | {{act_2_cat}} | {{act_2_nb}} | {{act_2_pct}}% | {{act_2_fd}}% |
| {{act_3_nom}} | {{act_3_cat}} | {{act_3_nb}} | {{act_3_pct}}% | {{act_3_fd}}% |
| {{act_4_nom}} | {{act_4_cat}} | {{act_4_nb}} | {{act_4_pct}}% | {{act_4_fd}}% |
| {{act_5_nom}} | {{act_5_cat}} | {{act_5_nb}} | {{act_5_pct}}% | {{act_5_fd}}% |
| {{act_6_nom}} | {{act_6_cat}} | {{act_6_nb}} | {{act_6_pct}}% | {{act_6_fd}}% |
| {{act_7_nom}} | {{act_7_cat}} | {{act_7_nb}} | {{act_7_pct}}% | {{act_7_fd}}% |
| {{act_8_nom}} | {{act_8_cat}} | {{act_8_nb}} | {{act_8_pct}}% | {{act_8_fd}}% |
| {{act_9_nom}} | {{act_9_cat}} | {{act_9_nb}} | {{act_9_pct}}% | {{act_9_fd}}% |
| {{act_10_nom}} | {{act_10_cat}} | {{act_10_nb}} | {{act_10_pct}}% | {{act_10_fd}}% |

## Mouvements du trimestre

- Attributions BSPCE : {{bspce_attribues}} vers {{nb_beneficiaires_bspce}} bénéficiaires
- Exercices BSPCE : {{bspce_exerces}} en augmentation de capital à {{cours_exercice_bspce}} EUR
- Attributions AGA : {{aga_attribuees}}
- Périodes d'acquisition terminées AGA : {{aga_acquises}}
- Nouvelles augmentations de capital : {{ak_montant}} EUR à {{prix_ak}} EUR/action
- Cessions ou transferts de titres : {{cessions_detail}}

## Scénarios de dilution pour levée Série {{lettre_serie_prochain}}

### Scénario 1 : levée {{lettre_serie_prochain}} à {{valo_scn1}} k EUR pre-money

| Élément | Nb actions | % FD après levée |
|---------|------------|-------------------|
| Actionnaires existants | {{sc1_exist_nb}} | {{sc1_exist_pct}}% |
| Nouveaux investisseurs | {{sc1_new_nb}} | {{sc1_new_pct}}% |
| ESOP post-levée (pool) | {{sc1_esop_nb}} | {{sc1_esop_pct}}% |
| Fondateurs cumulés | {{sc1_fond_nb}} | {{sc1_fond_pct}}% |

### Scénario 2 : levée Série à {{valo_scn2}} k EUR pre-money

| Élément | Nb actions | % FD après levée |
|---------|------------|-------------------|
| Actionnaires existants | {{sc2_exist_nb}} | {{sc2_exist_pct}}% |
| Nouveaux investisseurs | {{sc2_new_nb}} | {{sc2_new_pct}}% |
| ESOP post-levée | {{sc2_esop_nb}} | {{sc2_esop_pct}}% |
| Fondateurs cumulés | {{sc2_fond_nb}} | {{sc2_fond_pct}}% |

### Taille du ESOP pool cible post-levée

Cible sectorielle : 10 à 20% du capital fully diluted. ESOP actuel : {{esop_actuel_pct}}%. Ajustement nécessaire : {{esop_ajust}} pt pour atteindre {{esop_cible}}% post-levée.

## Risques

- {{risque_1_niveau}} Drag along non respecté en cas de cession : risque de blocage décisionnel
- {{risque_2_niveau}} Préférences de liquidation (ratchet, participating) défavorables aux fondateurs en scénario d'exit bas
- {{risque_3_niveau}} BSPCE attribués mais non exercés dépassant la fenêtre fiscale (plus de 5 ans post-émission)

## Actions

- [ ] Valider la table à jour avec le cabinet d'avocat de {{denomination}} (Dentons, Gide, Desfilis ou autre)
- [ ] Mettre à jour la plateforme de cap table (Carta, Eagle Tree, Ledgy, Capflow si utilisée)
- [ ] Communiquer la cap table actualisée aux investisseurs (obligation trimestrielle selon pacte)
- [ ] Planifier la revue annuelle du pacte d'actionnaires pour vérifier la cohérence avec la cap table
- [ ] Simuler les scénarios de levée avec le conseil corporate finance si levée dans les 12 prochains mois

## Limites

La cap table est un document juridique. Toute modification doit être validée par un avocat pour cohérence avec les statuts, le pacte d'actionnaires et le règlement des BSPCE/AGA/BSA. Les simulations de dilution sont des projections : la valorisation finale et le ratchet peuvent varier lors de la négociation. Pour transaction significative (levée, cession, fusion, exit), recourir à un conseil corporate finance et un avocat en droit des sociétés. Ne pas communiquer de cap table détaillée à un tiers sans clause de confidentialité signée (NDA).
