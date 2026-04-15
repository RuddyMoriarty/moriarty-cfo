# Tracking MRR/ARR, W{{ww}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Semaine** : W{{ww}} {{yyyy}}
**Généré le** : {{date_today}}
**Modèle** : SaaS éditeur

## Pourquoi

Suivi hebdomadaire des indicateurs clés SaaS (ARR, NRR, churn, CAC payback) pour le pilotage opérationnel et investisseur. Décisions en jeu : allocation growth (acquisition vs expansion), détection précoce du churn, signalement au board des écarts par rapport aux OKRs.

## Chiffres clés

| KPI | Semaine | Mois glissant | Cible {{yyyy}} | Signal |
|-----|---------|---------------|-----------------|--------|
| ARR total | {{arr}} k EUR | {{arr_fin_mois}} k | {{arr_cible}} k | {{signal_arr}} |
| MRR | {{mrr}} k EUR | {{mrr_moy_mois}} k | {{mrr_cible}} k | {{signal_mrr}} |
| Net new ARR | {{nnarr_semaine}} k | {{nnarr_mois}} k | {{nnarr_cible}} k | {{signal_nnarr}} |
| Gross MRR churn | {{gross_churn}}% | {{gross_churn_mois}}% | inf à {{gross_churn_cible}}% | {{signal_gross}} |
| Net Revenue Retention (NRR) | {{nrr}}% | {{nrr_mois}}% | sup à {{nrr_cible}}% | {{signal_nrr}} |
| Gross Revenue Retention (GRR) | {{grr}}% | {{grr_mois}}% | sup à {{grr_cible}}% | {{signal_grr}} |
| CAC payback (mois) | {{cac_pb}} mois | {{cac_pb_mois}} mois | inf à {{cac_pb_cible}} mois | {{signal_cac_pb}} |
| CAC / ACV | {{cac_acv}} | {{cac_acv_mois}} | inf à {{cac_acv_cible}} | {{signal_cac_acv}} |

## Décomposition ARR

### Mouvements ARR de la semaine

| Mouvement | Nombre | Montant |
|-----------|--------|---------|
| New ARR (nouveaux logos) | {{new_logos_nb}} | {{new_logos_arr}} k EUR |
| Expansion ARR (upsell + cross-sell) | {{expansion_nb}} | {{expansion_arr}} k EUR |
| Contraction ARR (downsell, downgrade) | {{contraction_nb}} | -{{contraction_arr}} k EUR |
| Churn ARR (résiliations totales) | {{churn_nb}} | -{{churn_arr}} k EUR |
| **Net new ARR semaine** | - | **{{nnarr_semaine}} k EUR** |

### Cohortes NRR (par trimestre d'acquisition)

| Cohorte | ARR initial | ARR actuel | NRR cumulé |
|---------|-------------|------------|------------|
| T{{qq_prev_4}} ({{yyyy_n2}}) | {{coh1_init}} | {{coh1_actuel}} | {{coh1_nrr}}% |
| T{{qq_prev_3}} ({{yyyy_n2}}) | {{coh2_init}} | {{coh2_actuel}} | {{coh2_nrr}}% |
| T{{qq_prev_2}} ({{yyyy_prev}}) | {{coh3_init}} | {{coh3_actuel}} | {{coh3_nrr}}% |
| T{{qq_prev_1}} ({{yyyy_prev}}) | {{coh4_init}} | {{coh4_actuel}} | {{coh4_nrr}}% |

### Structure ARR par segment

| Segment | ARR | Poids | Croissance YoY |
|---------|-----|-------|----------------|
| {{seg_1_nom}} (Enterprise) | {{seg_1_arr}} | {{seg_1_pct}}% | {{seg_1_croiss}}% |
| {{seg_2_nom}} (Mid-market) | {{seg_2_arr}} | {{seg_2_pct}}% | {{seg_2_croiss}}% |
| {{seg_3_nom}} (SMB) | {{seg_3_arr}} | {{seg_3_pct}}% | {{seg_3_croiss}}% |

### Efficacité commerciale

- Nombre de customers : {{nb_customers}} (vs {{nb_customers_prev}} semaine précédente)
- ACV moyen : {{acv_moyen}} k EUR
- Sales cycle médian : {{sales_cycle}} jours
- Win rate : {{win_rate}}%
- Quick ratio (new + expansion / churn + contraction) : {{quick_ratio}}

## Alertes détectées

- {{alerte_1_type}} : {{alerte_1_desc}}
- {{alerte_2_type}} : {{alerte_2_desc}}

## Options d'arbitrage growth

**A. Maintenir le mix acquisition/expansion actuel (recommandée si NRR supérieur à 100%)**
Allocation inchangée. Focus expansion sur top 20% clients.

**B. Accélérer l'expansion sur la base installée (si NRR inférieur à 100%)**
Renforcer le Customer Success, lancer un programme outbound upsell, créer des playbooks expansion. Investissement : {{invest_cs}} k EUR. Impact attendu : +{{impact_b}} pt de NRR sur 6 mois.

**C. Diversifier acquisition vers un nouveau segment (si pipeline saturé sur segment actuel)**
Tester la viabilité du segment {{nouveau_segment}} avec un pilote. Budget test : {{budget_pilote}} k EUR sur 3 mois.

## Recommandation

Retenir l'option A si NRR est au-dessus de 105%, sinon basculer vers B. Raisons : (1) l'expansion consomme 3x moins de CAC que l'acquisition ; (2) elle preserve la dynamique d'ARR sans dépendre de l'aléa de la conversion commerciale. Caveat : tout pivot expansion/acquisition doit être validé avec la CRO/VP Sales pour ne pas cannibaliser les équipes.

## Next

Revue des KPIs au conseil de direction hebdo. Si alertes déclenchées, escalader en comité ARR immédiatement. Porteur : CFO + CRO. Prochaine revue : {{date_prochain}}.

## Limites

Les KPIs SaaS dépendent de la qualité des données CRM et du CMR (Contract Management Repository). Les cohortes NRR sont sensibles aux ajustements manuels ; toute correction rétroactive doit être auditée. Le CAC payback est calculé sur les coûts sales + marketing alloués à l'acquisition nouveaux logos : s'il inclut des coûts d'expansion, il est artificiellement gonflé. Pour benchmarks externes fiables, se référer aux études OpenView, SaaStr ou ICONIQ mises à jour annuellement.
