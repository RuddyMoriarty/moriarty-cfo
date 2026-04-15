# Dashboard CFO exécutif {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : {{period_label}}
**Généré le** : {{date_today}}
**Cadence** : {{cadence}} (hebdo startup, mensuel PME/ETI)

## Pourquoi

Dashboard exécutif condensé destiné au pilotage du CFO et de la direction. 6 à 8 KPIs pour une lecture en 2 minutes. Décisions en jeu : ajustements commerciaux, pilotage des OPEX, alertes early warning sur trésorerie et conformité.

## Chiffres clés

| KPI | Valeur | Cible {{yyyy}} | Vs N-1 | Vs cible | Signal |
|-----|--------|----------------|--------|----------|--------|
| CA HT {{period_label}} | {{ca_period}} | {{ca_cible}} | {{ca_vs_n1}}% | {{ca_vs_cible}}% | {{signal_ca}} |
| Marge brute | {{mb_pct}}% | {{mb_cible}}% | {{mb_vs_n1}} pt | {{mb_vs_cible}} pt | {{signal_mb}} |
| EBE | {{ebe_pct}}% | {{ebe_cible}}% | {{ebe_vs_n1}} pt | {{ebe_vs_cible}} pt | {{signal_ebe}} |
| Trésorerie | {{treso}} k EUR | {{treso_cible}} k EUR | {{treso_vs_n1}}% | {{treso_vs_cible}}% | {{signal_treso}} |
| BFR (j de CA) | {{bfr_jours}} j | {{bfr_cible}} j | {{bfr_vs_n1}} j | {{bfr_vs_cible}} j | {{signal_bfr}} |
| DSO | {{dso}} j | {{dso_cible}} j | {{dso_vs_n1}} j | {{dso_vs_cible}} j | {{signal_dso}} |
| Productivité ETP | {{prod_etp}} | {{prod_cible}} | {{prod_vs_n1}}% | {{prod_vs_cible}}% | {{signal_prod}} |
| Pipeline commercial | {{pipeline}} k EUR | {{pipeline_cible}} | {{pipeline_vs_n1}}% | {{pipeline_vs_cible}}% | {{signal_pipeline}} |

## Alertes et signaux

### Signaux forts (cible dépassée positivement)

- {{signal_fort_1}}
- {{signal_fort_2}}

### Signaux d'alerte (seuil franchi négativement)

- {{alerte_1_titre}} : {{alerte_1_desc}}. Seuil : {{alerte_1_seuil}}.
- {{alerte_2_titre}} : {{alerte_2_desc}}. Seuil : {{alerte_2_seuil}}.

### Early warnings (tendance à 4-6 semaines)

- {{ew_1_titre}} : {{ew_1_desc}}. Action préventive : {{ew_1_action}}.
- {{ew_2_titre}} : {{ew_2_desc}}. Action préventive : {{ew_2_action}}.

## Options d'action prioritaire

**A. Ajustement OPEX ciblé (recommandée si EBE sous cible)**
Levier : {{opex_levier}}. Économie potentielle : {{opex_economie}} k EUR / an.

**B. Accélération recouvrement clients (recommandée si DSO dégradé)**
Action : relances top 10, mise en place escompte 2/10 Net 30. Cash libéré : {{cash_relance}} k EUR.

**C. Ajustement pricing ou mix produit (recommandée si marge brute dégradée)**
Action : revue tarifs sur segment {{segment_pricing}}, revalorisation {{pct_pricing}}%.

## Recommandation

Prioriser l'option {{option_recommandee}} sur les 4 prochaines semaines. Raisons : {{raison_1}} et {{raison_2}}. Caveat : {{caveat}}.

## Next

Revue dashboard au prochain cycle {{cadence}} ({{date_prochain}}). Porteur : CFO. Action associée : partager les signaux forts et alertes avec la direction en comité de pilotage.

## Limites

Ce dashboard est un outil de pilotage interne. Les données affichées sont extraites automatiquement de la balance comptable et du CRM, sans retraitement manuel. Pour décisions stratégiques majeures (acquisition, levée de fonds, restructuration), compléter par une analyse approfondie avec l'EC et le conseil d'administration. Les benchmarks sectoriels (si affichés) proviennent de {{source_benchmark}} et peuvent avoir jusqu'à 12 mois de décalage.
