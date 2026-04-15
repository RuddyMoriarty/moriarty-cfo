# Burn multiple, W{{ww}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Semaine** : W{{ww}} {{yyyy}}
**Généré le** : {{date_today}}
**Modèle** : SaaS scale-up, financée en equity

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Statut : {{statut_startup}} (Serie A, B, C, growth stage)
- Cash en banque fin de semaine : {{cash_fin}} k EUR
- Formule burn multiple : Net burn / Net new ARR (mensuel ou trimestriel)

## Hypothèses

- H1 : le net burn est calculé avec une discipline OPEX stable mois sur mois ; toute écriture exceptionnelle est exclue
- H2 : le net new ARR intègre uniquement les mouvements fermés ce mois (new + expansion - contraction - churn)
- H3 : la comparaison au benchmark Capchase/Bessemer utilise la maturité de {{denomination}} (Serie X, ARR dans tranche Y)

## Analyse

### Calcul du burn multiple

| Période | Net burn | Net new ARR | Burn multiple | Benchmark |
|---------|----------|-------------|---------------|-----------|
| T{{qq_prev_3}} | {{burn_t1}} | {{nnarr_t1}} | {{bm_t1}} | {{bench_t1}} |
| T{{qq_prev_2}} | {{burn_t2}} | {{nnarr_t2}} | {{bm_t2}} | {{bench_t2}} |
| T{{qq_prev_1}} | {{burn_t3}} | {{nnarr_t3}} | {{bm_t3}} | {{bench_t3}} |
| T{{qq}} (en cours) | {{burn_t4}} | {{nnarr_t4}} | {{bm_t4}} | {{bench_t4}} |

### Classification Bessemer

| Burn multiple | Qualificatif |
|---------------|--------------|
| inf à 1 | Amazing |
| 1 à 1.5 | Great |
| 1.5 à 2 | Good |
| 2 à 3 | Suspect |
| sup à 3 | Bad |

Position actuelle de {{denomination}} : {{classification_bm}}.

### Décomposition du net burn

| Catégorie | Montant mensuel | Poids |
|-----------|------------------|-------|
| COGS (infrastructure, support) | {{cogs}} k | {{cogs_pct}}% |
| R&D et produit | {{rd}} k | {{rd_pct}}% |
| Sales et marketing | {{sm}} k | {{sm_pct}}% |
| G&A | {{ga}} k | {{ga_pct}}% |
| Autres | {{autres}} k | {{autres_pct}}% |
| **Net burn total** | **{{net_burn}} k** | 100% |

### Analyse de l'efficience

- Magic Number (S&M efficiency) : {{magic_number}} ({{classification_magic}})
- CAC payback : {{cac_payback}} mois ({{classification_cac}})
- LTV/CAC : {{ltv_cac}} ({{classification_ltv}})
- Rule of 40 (croissance + marge EBE) : {{rule_40}}% ({{classification_r40}})

## Risques

- {{risque_1_niveau}} Burn multiple supérieur à 2 pendant plus de 2 trimestres consécutifs : signal de sous-performance que les investisseurs vont challenger en prochaine ronde
- {{risque_2_niveau}} Runway insuffisant vs durée estimée du process de levée (4 à 6 mois) : risque de bridge short
- {{risque_3_niveau}} Dégradation du burn multiple sans ajustement des dépenses : érosion du FCF

## Actions

- [ ] Documenter la trajectoire burn multiple pour le board et les futurs investisseurs
- [ ] Identifier les postes de burn à plus forte dérive vs les cohortes précédentes
- [ ] Challenger la productivité sales (en particulier si Magic Number inférieur à 0.7)
- [ ] Planifier une revue trimestrielle approfondie avec VP Sales, CRO et produit
- [ ] Si burn multiple dégradé : préparer un plan d'ajustement 90 jours

## Limites

Le burn multiple est un KPI d'efficience capitalistique utilisé par les investisseurs VC pour comparer les scale-ups. Il n'est pas adapté aux entreprises profitables ou aux modèles non-SaaS. Les benchmarks Bessemer/ICONIQ portent sur des cohortes post-2019 et peuvent être durcis en contexte de marché tendu (2023-2026). Pour négociation de levée, préparer les trois derniers trimestres de burn multiple avec annotations explicatives sur les écarts. En cas de dégradation non-expliquée par un investissement growth assumé, engager une revue stratégique avec le board.
