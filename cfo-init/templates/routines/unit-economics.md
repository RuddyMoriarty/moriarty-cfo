# Unit economics {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}
**Modèle** : Analyse par unité commerciale (client, utilisateur, commande selon le business)

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Unité commerciale de référence : {{unite_commerciale}} (client actif, utilisateur payant, compte, autre)
- Nombre d'unités en portefeuille au {{date_today}} : {{nb_unites}}
- Devise : EUR

## Hypothèses

- H1 : les coûts d'acquisition (CAC) sont calculés sur les dépenses Sales + Marketing des 12 derniers mois, alloués aux nouveaux logos acquis sur la même période
- H2 : la LTV est calculée avec la formule ARPU x marge brute / churn annuel, sur cohorte 12 mois
- H3 : les coûts R&D ne sont pas inclus dans le CAC (capitalisation conforme au Plan comptable)
- H4 : les coûts de support et d'onboarding sont intégrés au COGS, pas au CAC

## Analyse

### Métriques principales

| KPI | Valeur | Cible sectorielle | Classification |
|-----|--------|-------------------|----------------|
| ARPU mensuel | {{arpu}} EUR | {{arpu_cible}} | {{class_arpu}} |
| CAC (coût acquisition moyen) | {{cac}} EUR | inf à {{cac_cible}} | {{class_cac}} |
| LTV (valeur vie client) | {{ltv}} EUR | sup à {{ltv_cible}} | {{class_ltv}} |
| Ratio LTV/CAC | {{ltv_cac}} | sup à 3 | {{class_ratio}} |
| CAC payback | {{cac_payback}} mois | inf à 12 | {{class_payback}} |
| Marge brute par unité | {{mb_unite}} EUR ({{mb_pct}}%) | sup à 70% | {{class_mb}} |
| Durée de vie moyenne | {{duree_vie}} mois | - | - |
| Churn mensuel | {{churn_mensuel}}% | inf à 2% | {{class_churn}} |

### Décomposition du CAC

| Catégorie | Montant 12M | Répartition |
|-----------|-------------|-------------|
| Salaires Sales | {{sal_sales}} k | {{sal_sales_pct}}% |
| Commissions | {{commissions}} k | {{commissions_pct}}% |
| Marketing paid (Google, LinkedIn, events) | {{mkt_paid}} k | {{mkt_paid_pct}}% |
| Marketing organique (content, SEO) | {{mkt_org}} k | {{mkt_org_pct}}% |
| Outils Sales/Marketing | {{outils_sm}} k | {{outils_sm_pct}}% |
| **Total coûts acquisition** | **{{total_cac}} k** | 100% |
| Nouveaux logos acquis | {{nouveaux_logos}} | - |
| CAC moyen unitaire | {{cac}} EUR | - |

### Décomposition de la LTV

- ARPU mensuel : {{arpu}} EUR
- Marge brute par unité : {{mb_pct}}% (soit {{mb_abs_unite}} EUR/mois)
- Churn mensuel : {{churn_mensuel}}%
- Durée de vie implicite : 1 / {{churn_mensuel}}% = {{duree_implicite}} mois
- LTV brute = ARPU x durée de vie = {{ltv_brute}} EUR
- LTV nette = LTV brute x marge brute = {{ltv}} EUR

### Analyse par cohorte

| Cohorte (mois d'acquisition) | ARPU J+12 | Churn 12M | LTV observée |
|-------------------------------|-----------|-----------|---------------|
| {{cohorte_1}} | {{arpu_c1}} | {{churn_c1}}% | {{ltv_c1}} |
| {{cohorte_2}} | {{arpu_c2}} | {{churn_c2}}% | {{ltv_c2}} |
| {{cohorte_3}} | {{arpu_c3}} | {{churn_c3}}% | {{ltv_c3}} |
| {{cohorte_4}} | {{arpu_c4}} | {{churn_c4}}% | {{ltv_c4}} |

Tendance cohorte à cohorte : {{tendance_cohorte}}.

### Analyse par segment

| Segment | ARPU | CAC | LTV | Ratio |
|---------|------|-----|-----|-------|
| Enterprise | {{arpu_ent}} | {{cac_ent}} | {{ltv_ent}} | {{ratio_ent}} |
| Mid-market | {{arpu_mid}} | {{cac_mid}} | {{ltv_mid}} | {{ratio_mid}} |
| SMB | {{arpu_smb}} | {{cac_smb}} | {{ltv_smb}} | {{ratio_smb}} |

## Risques

- {{risque_1_niveau}} Dégradation du ratio LTV/CAC sous 3 : modèle économique menacé, besoin de travailler le churn ou le pricing
- {{risque_2_niveau}} CAC payback supérieur à 18 mois : dépendance accrue à la capitalisation externe
- {{risque_3_niveau}} Churn mensuel supérieur à 3% : perte de valeur de la base installée, attention retention avant growth

## Actions

- [ ] Identifier les segments au meilleur LTV/CAC pour prioriser l'allocation Sales/Marketing
- [ ] Lancer une analyse churn qualitative si churn dégradé (interviews exit, signaux usage)
- [ ] Tester un ajustement pricing sur le segment au CAC le plus élevé
- [ ] Allouer davantage de ressources Customer Success sur les cohortes au ARPU en baisse
- [ ] Communiquer les unit economics au board avec benchmarks sectoriels

## Limites

Les unit economics sont sensibles à la méthode d'allocation des coûts. Une mauvaise répartition Sales vs Customer Success peut gonfler artificiellement le CAC ou sous-évaluer la LTV. Les cohortes nécessitent 12 à 24 mois de recul pour être robustes ; les cohortes récentes sont indicatives. Le churn mensuel peut masquer une saisonnalité forte (contrats annuels renouvelés en T4) : compléter par une analyse annualisée. Pour benchmarks sectoriels fiables, se référer à OpenView SaaS Benchmarks, Bessemer State of the Cloud, ICONIQ Growth Report.
