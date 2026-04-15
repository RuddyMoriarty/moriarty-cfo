# Reporting trimestriel T{{qq}} {{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : T{{qq}} {{yyyy}}
**Généré le** : {{date_today}}
**Destinataires** : Board, actionnaires, direction

## Pourquoi

Board pack T{{qq}} {{yyyy}} à destination du conseil et des investisseurs. Présente la performance du trimestre, la position financière et les risques clés. Décisions attendues : validation de l'atterrissage annuel, arbitrages OPEX/CAPEX, plan de financement si cash inférieur à 6 mois.

## Chiffres clés

| KPI | T{{qq}} {{yyyy}} | T{{qq}} {{yyyy_prev}} | Budget T{{qq}} | Signal |
|-----|------------------|-----------------------|----------------|--------|
| CA HT trimestre | {{ca_trim}} | {{ca_trim_n1}} ({{ca_yoy}}%) | {{ca_budget_trim}} | {{signal_ca}} |
| Marge brute | {{mb_trim}} ({{mb_pct}}%) | {{mb_pct_n1}}% | {{mb_pct_budget}}% | {{signal_mb}} |
| EBE | {{ebe_trim}} ({{ebe_pct}}%) | {{ebe_pct_n1}}% | {{ebe_pct_budget}}% | {{signal_ebe}} |
| Cash en banque fin T{{qq}} | {{cash_fin_t}} | {{cash_n1}} | - | {{signal_cash}} |
| BFR (j de CA) | {{bfr_jours}} j | {{bfr_n1}} j | {{bfr_cible}} j | {{signal_bfr}} |
| Runway (mois) | {{runway_mois}} mois | - | - | {{signal_runway}} |

## Performance commerciale

### CA par segment

| Segment | T{{qq}} | Poids | Croissance YoY |
|---------|---------|-------|----------------|
| {{segment_1}} | {{ca_seg_1}} | {{poids_seg_1}}% | {{yoy_seg_1}}% |
| {{segment_2}} | {{ca_seg_2}} | {{poids_seg_2}}% | {{yoy_seg_2}}% |
| {{segment_3}} | {{ca_seg_3}} | {{poids_seg_3}}% | {{yoy_seg_3}}% |

Top clients : {{top_clients}}. Nouveaux logos : {{new_logos}}. Churn : {{churn_clients}}.

### Opérations

- Effectif fin T{{qq}} : {{effectif_fin_t}} (vs {{effectif_n1}} N-1, delta {{effectif_delta}})
- Productivité par ETP (CA/ETP) : {{productivite_etp}}
- Taux de marge opérationnelle : {{marge_ope}}%

## Position financière

### Bilan simplifié

| Poste | Fin T{{qq}} | Fin T{{qq}} N-1 | Delta |
|-------|-------------|-----------------|-------|
| Actif immobilisé | {{actif_immo}} | {{actif_immo_n1}} | {{actif_immo_delta}} |
| Actif circulant | {{actif_circ}} | {{actif_circ_n1}} | {{actif_circ_delta}} |
| Trésorerie | {{treso}} | {{treso_n1}} | {{treso_delta}} |
| Capitaux propres | {{cp}} | {{cp_n1}} | {{cp_delta}} |
| Dettes financières | {{dettes_fi}} | {{dettes_fi_n1}} | {{dettes_fi_delta}} |

Gearing (dette nette / CP) : {{gearing}}%. Cible : inférieur à {{gearing_cible}}%.

### Cash flow trimestriel

- Cash flow opérationnel : {{cf_ope}}
- Cash flow investissement : {{cf_invest}}
- Cash flow financement : {{cf_fin}}
- Variation de trésorerie : {{var_treso}}

## Options d'atterrissage annuel

**A. Atterrissage consensus (recommandée)**
CA annuel : {{atterrissage_ca_cons}}, EBE : {{atterrissage_ebe_cons}}, cash fin d'année : {{cash_fin_cons}}.
Hypothèses : maintien de la dynamique T{{qq}}, OPEX maîtrisés au budget.

**B. Atterrissage prudent**
CA annuel : {{atterrissage_ca_prud}}, EBE : {{atterrissage_ebe_prud}}.
Hypothèses : dégradation de 10% sur T{{qq_next}} si signaux macro négatifs.

**C. Atterrissage optimiste**
CA annuel : {{atterrissage_ca_opti}}, EBE : {{atterrissage_ebe_opti}}.
Hypothèses : accélération T4 sur pipeline commercial validé.

## Recommandation

Retenir l'atterrissage consensus (option A). Deux raisons : (1) le pipeline T{{qq_next}} est couvert à {{pipeline_couverture}}% de la cible, réduisant le risque d'exécution ; (2) le cash fin d'année reste au-dessus du seuil covenant de {{seuil_covenant}} mois de CA. Caveat : la saisonnalité T4 peut décaler +/- {{saisonnalite_pct}}% selon la conversion commerciale.

## Next

Validation du board sur l'atterrissage retenu. Porteur : CFO. Échéance : {{date_board}}. Action associée : diffusion de la lettre trimestrielle investisseurs sous 15 jours après validation.

## Limites

Ce board pack consolide les chiffres de clôture trimestrielle mais ne constitue pas un arrêté comptable formel. Les états définitifs sont produits semestriellement (situation au 30/06) et annuellement (comptes arrêtés). Pour communication externe engagée (prospectus, document de référence), validation CAC requise. Les données de benchmark sectoriel utilisées proviennent de {{source_benchmark}} et peuvent avoir 3 à 6 mois de décalage.
