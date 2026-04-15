# Clôture mensuelle {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Période de clôture : {{mm}}/{{yyyy}}
- Date de production du flash : {{date_today}} (J+5 théorique)
- Balance source : {{balance_source}} (export FEC ou logiciel comptable)
- Périmètre : comptes sociaux {{denomination}}, hors consolidation si {{is_groupe}}
- Devise : EUR
- Normes : {{normes}} (Plan comptable général ou IFRS)

## Hypothèses

- H1 : écritures d'inventaire standard appliquées (CCA, PCA, FNP, AAR) sur la base des écritures récurrentes des 3 derniers mois
- H2 : cut-off respecté au {{date_cutoff}}, toutes factures d'achats parvenues datées {{mm}}/{{yyyy}} intégrées
- H3 : TVA déductible provisionnée en attendant rapprochement définitif avec la déclaration CA3
- H4 : amortissements mensuels calculés au 1/12ème du budget annuel, ajustement réel en N+3
- H5 : provisions pour risques inchangées depuis la dernière clôture trimestrielle

Pour valider ou corriger : "H2 est trimestriel, cut-off au 10".

## Analyse

### KPIs P&L du mois

| KPI | Valeur | Vs N-1 | Vs budget | Signal |
|-----|--------|--------|-----------|--------|
| CA HT mois | {{ca_mois}} | {{ca_vs_n1}} | {{ca_vs_budget}} | {{signal_ca}} |
| Marge brute | {{mb_mois}} ({{mb_pct}}%) | {{mb_vs_n1}} | {{mb_vs_budget}} | {{signal_mb}} |
| Masse salariale | {{masse_sal}} | {{masse_sal_vs_n1}} | {{masse_sal_vs_budget}} | {{signal_ms}} |
| Autres OPEX | {{opex_mois}} | {{opex_vs_n1}} | {{opex_vs_budget}} | {{signal_opex}} |
| EBE | {{ebe_mois}} ({{ebe_pct}}%) | {{ebe_vs_n1}} | {{ebe_vs_budget}} | {{signal_ebe}} |
| Résultat net | {{rn_mois}} | {{rn_vs_n1}} | {{rn_vs_budget}} | {{signal_rn}} |

### Cumul YTD vs budget

| KPI | Cumul YTD | Budget YTD | Ecart | % atteint |
|-----|-----------|------------|-------|-----------|
| CA HT | {{ca_ytd}} | {{ca_budget_ytd}} | {{ca_ecart}} | {{ca_pct_atteint}}% |
| EBE | {{ebe_ytd}} | {{ebe_budget_ytd}} | {{ebe_ecart}} | {{ebe_pct_atteint}}% |

### Bilan et cash

| KPI | Fin de mois | Fin de mois N-1 | Delta |
|-----|-------------|-----------------|-------|
| Trésorerie (banques + caisse) | {{treso_fin_mois}} | {{treso_n1}} | {{treso_delta}} |
| BFR (j de CA) | {{bfr_jours}} j | {{bfr_jours_n1}} j | {{bfr_delta}} j |
| DSO | {{dso_jours}} j | {{dso_n1}} j | {{dso_delta}} j |
| DPO | {{dpo_jours}} j | {{dpo_n1}} j | {{dpo_delta}} j |

### Top variances vs budget

1. **{{variance_1_titre}}** : écart {{variance_1_montant}} ({{variance_1_pct}}%). Cause probable : {{variance_1_cause}}.
2. **{{variance_2_titre}}** : écart {{variance_2_montant}} ({{variance_2_pct}}%). Cause probable : {{variance_2_cause}}.
3. **{{variance_3_titre}}** : écart {{variance_3_montant}} ({{variance_3_pct}}%). Cause probable : {{variance_3_cause}}.

## Risques

- {{risque_1_niveau}} {{risque_1_titre}} : {{risque_1_desc}}. Mitigation : {{risque_1_mitig}}.
- {{risque_2_niveau}} {{risque_2_titre}} : {{risque_2_desc}}. Mitigation : {{risque_2_mitig}}.
- {{risque_3_niveau}} {{risque_3_titre}} : {{risque_3_desc}}. Mitigation : {{risque_3_mitig}}.

## Actions

- [ ] Valider la balance clôturée avec l'expert-comptable avant J+7
- [ ] Transmettre le flash mensuel à la direction (format PDF, dashboard joint)
- [ ] Lancer les relances sur le top 5 créances >60 j si DSO en tension
- [ ] Rapprocher la TVA déductible avec la CA3 du mois {{mm}}
- [ ] Préparer la note de gestion pour le comité d'entreprise si variance masse salariale >3%
- [ ] Actualiser l'atterrissage annuel avec les chiffres du mois (routine atterrissage-mat)

## Limites

Ce flash est un outil de pilotage interne J+5, produit sur la base de la balance provisoire. Les chiffres définitifs seront arrêtés après écritures d'inventaire complètes (J+15) et validation par l'expert-comptable. Pour toute communication externe (investisseurs, banquiers, administration fiscale), attendre les comptes arrêtés ou consulter votre EC. Les données N-1 utilisées proviennent de la balance de clôture {{yyyy_prev}} ; toute correction rétroactive impactera ces comparatifs.
