# Atterrissage mensuel (MAT) {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}
**Méthode** : Most Accurate Track (actualisation glissante de l'atterrissage annuel)

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Exercice en cours : {{yyyy}}
- Mois de production : {{mm}}/{{yyyy}} (M+{{mois_ecoules}} depuis début d'exercice)
- Budget initial voté le : {{date_budget}}
- Dernière révision MAT : {{date_mat_prev}}
- Source données réelles : balance clôturée J+5 (flash mensuel)
- Périmètre : comptes sociaux {{denomination}}

## Hypothèses

- H1 : les {{mois_restants}} mois restants suivent la tendance YTD ajustée de la saisonnalité N-1
- H2 : aucun événement exceptionnel non anticipé pour la fin d'exercice (cession, acquisition, one-shot)
- H3 : la masse salariale projetée intègre les recrutements planifiés dans le plan d'embauche {{yyyy}}
- H4 : le budget CAPEX est exécuté selon le plan validé en début d'année
- H5 : les hypothèses macro (inflation, cours matière première, taux de change) sont actualisées sur la base des consensus au {{date_today}}

## Analyse

### P&L atterrissage vs budget

| Poste | Budget {{yyyy}} | Réel YTD | Projection {{mois_restants}} mois | Atterrissage {{yyyy}} | Ecart vs budget |
|-------|-----------------|----------|-----------------------------------|------------------------|-----------------|
| CA HT | {{ca_budget}} | {{ca_ytd}} | {{ca_proj}} | {{ca_mat}} | {{ca_ecart}} ({{ca_ecart_pct}}%) |
| Achats consommés | {{ach_budget}} | {{ach_ytd}} | {{ach_proj}} | {{ach_mat}} | {{ach_ecart}} |
| Marge brute | {{mb_budget}} | {{mb_ytd}} | {{mb_proj}} | {{mb_mat}} | {{mb_ecart}} |
| Masse salariale | {{ms_budget}} | {{ms_ytd}} | {{ms_proj}} | {{ms_mat}} | {{ms_ecart}} |
| OPEX hors salaires | {{opex_budget}} | {{opex_ytd}} | {{opex_proj}} | {{opex_mat}} | {{opex_ecart}} |
| EBE | {{ebe_budget}} | {{ebe_ytd}} | {{ebe_proj}} | {{ebe_mat}} | {{ebe_ecart}} ({{ebe_ecart_pct}}%) |
| Résultat net | {{rn_budget}} | {{rn_ytd}} | {{rn_proj}} | {{rn_mat}} | {{rn_ecart}} |

### Cash flow atterrissage

| KPI | Budget {{yyyy}} | Atterrissage {{yyyy}} | Ecart |
|-----|-----------------|------------------------|-------|
| Cash opérationnel | {{cf_ope_budget}} | {{cf_ope_mat}} | {{cf_ope_ecart}} |
| Cash investissement | {{cf_inv_budget}} | {{cf_inv_mat}} | {{cf_inv_ecart}} |
| Cash financement | {{cf_fin_budget}} | {{cf_fin_mat}} | {{cf_fin_ecart}} |
| Variation trésorerie | {{var_treso_budget}} | {{var_treso_mat}} | - |

### Bilan fin d'exercice projeté

| Poste | Budget | Atterrissage | Ecart |
|-------|--------|--------------|-------|
| Trésorerie fin d'année | {{treso_budget}} | {{treso_mat}} | {{treso_ecart}} |
| BFR | {{bfr_budget}} | {{bfr_mat}} | {{bfr_ecart}} |
| Capitaux propres | {{cp_budget}} | {{cp_mat}} | {{cp_ecart}} |
| Gearing | {{gearing_budget}}% | {{gearing_mat}}% | {{gearing_ecart}} pt |

### Décomposition de la variance vs budget

Variance totale EBE : {{ebe_ecart}} EUR soit {{ebe_ecart_pct}}%.

- Effet volume (CA) : {{effet_volume}} EUR
- Effet mix et prix : {{effet_mix_prix}} EUR
- Effet marge brute : {{effet_mb}} EUR
- Effet masse salariale : {{effet_ms}} EUR
- Effet OPEX : {{effet_opex}} EUR
- Résidu / inexpliqué : {{residu}} EUR

## Risques

- {{risque_1_niveau}} Degradation commerciale T{{qq_next}} si pipeline inférieur à {{seuil_pipeline}}% de couverture
- {{risque_2_niveau}} Dépassement masse salariale si les recrutements planifiés ne sont pas priorisés
- {{risque_3_niveau}} Tension covenants si atterrissage EBE en dessous du seuil {{seuil_covenant}}%

## Actions

- [ ] Présenter l'atterrissage au comité de pilotage mensuel
- [ ] Réviser le plan d'action commercial si atterrissage CA inférieur à -5% vs budget
- [ ] Geler ou retarder le CAPEX non engagé si atterrissage cash dégradé
- [ ] Actualiser le forecast 12 mois glissant avec ces chiffres
- [ ] Informer les banques si covenants menacés à plus ou moins 3 mois
- [ ] Mettre à jour la lettre trimestrielle investisseurs

## Limites

L'atterrissage est une projection, pas un engagement. Sa fiabilité diminue avec l'horizon (M+{{mois_restants}} est moins précis que M+3). Les hypothèses macro utilisées peuvent évoluer rapidement (chocs sectoriels, changements fiscaux). Ce MAT ne se substitue pas au budget voté et ne sert pas de base pour les calculs de primes variables sans validation direction. Pour communication externe (banques, investisseurs), précéder d'une revue EC et d'un paragraphe d'hypothèses explicites.
