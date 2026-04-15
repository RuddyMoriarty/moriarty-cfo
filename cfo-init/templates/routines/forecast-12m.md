# Forecast 12 mois glissant T{{qq}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Date de production** : {{date_today}}
**Horizon** : 12 mois glissants à partir du {{date_debut_forecast}}

## Pourquoi

Reprojection trimestrielle du P&L, du bilan et du cash flow sur 12 mois glissants. Trois scénarios : pessimiste, réaliste, optimiste. Décision en jeu : validation de la trajectoire par le board, arbitrages OPEX/CAPEX, besoin éventuel de financement complémentaire.

## Chiffres clés

| KPI | Pessimiste | Réaliste | Optimiste | Budget ref |
|-----|------------|----------|-----------|------------|
| CA HT 12 mois | {{ca_pess}} | {{ca_real}} | {{ca_opti}} | {{ca_budget}} |
| Croissance YoY | {{croiss_pess}}% | {{croiss_real}}% | {{croiss_opti}}% | {{croiss_budget}}% |
| EBE (% CA) | {{ebe_pess}}% | {{ebe_real}}% | {{ebe_opti}}% | {{ebe_budget}}% |
| Résultat net | {{rn_pess}} | {{rn_real}} | {{rn_opti}} | {{rn_budget}} |
| Cash fin de période | {{cash_pess}} | {{cash_real}} | {{cash_opti}} | {{cash_budget}} |
| Runway (mois) | {{runway_pess}} | {{runway_real}} | {{runway_opti}} | - |

## P&L détaillé, scénario réaliste

| Poste | M1-M3 | M4-M6 | M7-M9 | M10-M12 | Total 12M |
|-------|-------|-------|-------|---------|-----------|
| CA HT | {{ca_t1}} | {{ca_t2}} | {{ca_t3}} | {{ca_t4}} | {{ca_12m}} |
| Achats | {{ach_t1}} | {{ach_t2}} | {{ach_t3}} | {{ach_t4}} | {{ach_12m}} |
| Marge brute | {{mb_t1}} | {{mb_t2}} | {{mb_t3}} | {{mb_t4}} | {{mb_12m}} |
| Masse salariale | {{ms_t1}} | {{ms_t2}} | {{ms_t3}} | {{ms_t4}} | {{ms_12m}} |
| OPEX autres | {{opex_t1}} | {{opex_t2}} | {{opex_t3}} | {{opex_t4}} | {{opex_12m}} |
| EBE | {{ebe_t1}} | {{ebe_t2}} | {{ebe_t3}} | {{ebe_t4}} | {{ebe_12m}} |
| Dotations | {{do_t1}} | {{do_t2}} | {{do_t3}} | {{do_t4}} | {{do_12m}} |
| Résultat d'exploitation | {{rex_t1}} | {{rex_t2}} | {{rex_t3}} | {{rex_t4}} | {{rex_12m}} |

## Bilan projeté fin de période (réaliste)

| Poste | Fin période | Début période | Delta |
|-------|-------------|---------------|-------|
| Actif immobilisé net | {{aim_fin}} | {{aim_deb}} | {{aim_delta}} |
| Stocks | {{stocks_fin}} | {{stocks_deb}} | - |
| Créances clients | {{cc_fin}} | {{cc_deb}} | - |
| Trésorerie | {{treso_fin}} | {{treso_deb}} | {{treso_delta}} |
| Capitaux propres | {{cp_fin}} | {{cp_deb}} | {{cp_delta}} |
| Dettes financières | {{df_fin}} | {{df_deb}} | {{df_delta}} |
| Dettes fournisseurs | {{df_four_fin}} | {{df_four_deb}} | - |

## Cash flow projeté (réaliste)

| Flux | T1 | T2 | T3 | T4 | Total 12M |
|------|----|----|----|----|-----------|
| Cash opérationnel | {{cfo_t1}} | {{cfo_t2}} | {{cfo_t3}} | {{cfo_t4}} | {{cfo_12m}} |
| CAPEX | {{capex_t1}} | {{capex_t2}} | {{capex_t3}} | {{capex_t4}} | {{capex_12m}} |
| Cash financement | {{cff_t1}} | {{cff_t2}} | {{cff_t3}} | {{cff_t4}} | {{cff_12m}} |
| Variation trésorerie | {{vt_t1}} | {{vt_t2}} | {{vt_t3}} | {{vt_t4}} | {{vt_12m}} |

## Options

**A. Tenir le scénario réaliste (recommandée si pipeline couvert)**
Pas d'ajustement structurel. Surveillance mensuelle des signaux early warning. Pas de besoin de financement complémentaire si cash fin supérieur à {{seuil_cash}}.

**B. Basculer scénario prudent si signaux dégradés**
Gel du CAPEX non engagé ({{capex_gelable}}). Report de {{nb_recrutements_report}} recrutements. Économie générée : {{economie_prudent}} k EUR sur 12 mois.

**C. Pousser le scénario optimiste si accélération commerciale confirmée**
Investissement additionnel CAPEX {{capex_opti}} k EUR. Recrutement anticipé de {{nb_recrutements_opti}} profils. Cash consommé supplémentaire : {{cash_opti_consumption}} k EUR.

## Recommandation

Retenir le scénario réaliste (option A) comme trajectoire de référence. Deux raisons : (1) il est construit sur les données de pipeline confirmées à J0 et une saisonnalité observée sur 3 années ; (2) il préserve la flexibilité d'arbitrage en cours d'année. Caveat : revue trimestrielle obligatoire pour déclencher le pivot vers B ou C selon l'évolution du pipeline et des signaux macro.

## Next

Validation du scénario cible en conseil de direction prochain ({{date_codir}}). Porteur : CFO. Action associée : communiquer aux banques le scénario réaliste si covenants à re-négocier sur les 12 prochains mois.

## Limites

Un forecast 12 mois est une projection, non une promesse. Sa fiabilité décroît fortement au-delà de 6 mois. Les hypothèses macro (croissance, inflation, taux, change, matière première) sont volatiles. Ce document n'engage pas l'entreprise vis-à-vis de tiers (investisseurs, banquiers) sauf formalisation explicite dans un document contractuel. Pour communication externe, précéder d'une revue EC et d'un disclaimer explicite sur les hypothèses.
