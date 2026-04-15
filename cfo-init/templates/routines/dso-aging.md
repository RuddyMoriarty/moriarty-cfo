# DSO et aging des créances {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}

## Pourquoi

Analyse mensuelle du vieillissement des créances clients et du DSO. Décision en jeu : intensification des relances, mise en contentieux des top débiteurs, passage en créances douteuses, ajustement des conditions de règlement pour les nouveaux contrats.

## Chiffres clés

| KPI | Valeur actuelle | Vs M-1 | Cible {{yyyy}} | Signal |
|-----|-----------------|--------|-----------------|--------|
| DSO (Days Sales Outstanding) | {{dso}} j | {{dso_vs_m1}} j | inf à {{dso_cible}} j | {{signal_dso}} |
| Créances clients totales | {{cc_total}} k EUR | {{cc_vs_m1}}% | - | - |
| Créances supérieur à 60 jours de retard | {{cc_sup_60}} k | {{cc_sup_60_pct}}% | inf à 5% | {{signal_60}} |
| Créances douteuses provisionnées | {{cc_douteuses}} k | - | - | - |
| Nombre de clients supérieur à 90j de retard | {{nb_clients_90}} | - | - | - |

## Aging buckets

| Tranche | Montant | % des créances | Nb factures |
|---------|---------|----------------|-------------|
| Non échues | {{bucket_0}} k | {{bucket_0_pct}}% | {{nb_0}} |
| 0 à 30 jours de retard | {{bucket_30}} k | {{bucket_30_pct}}% | {{nb_30}} |
| 31 à 60 jours de retard | {{bucket_60}} k | {{bucket_60_pct}}% | {{nb_60}} |
| 61 à 90 jours de retard | {{bucket_90}} k | {{bucket_90_pct}}% | {{nb_90}} |
| Supérieur à 90 jours de retard | {{bucket_sup_90}} k | {{bucket_sup_90_pct}}% | {{nb_sup_90}} |
| **Total** | **{{cc_total}} k** | 100% | {{nb_factures_tot}} |

## Top 10 débiteurs

| Rang | Client | Montant dû | Part | Tranche la plus ancienne | Action prévue |
|------|--------|------------|------|--------------------------|----------------|
| 1 | {{deb_1_nom}} | {{deb_1_montant}} | {{deb_1_pct}}% | {{deb_1_anciennete}} | {{deb_1_action}} |
| 2 | {{deb_2_nom}} | {{deb_2_montant}} | {{deb_2_pct}}% | {{deb_2_anciennete}} | {{deb_2_action}} |
| 3 | {{deb_3_nom}} | {{deb_3_montant}} | {{deb_3_pct}}% | {{deb_3_anciennete}} | {{deb_3_action}} |
| 4 | {{deb_4_nom}} | {{deb_4_montant}} | {{deb_4_pct}}% | {{deb_4_anciennete}} | {{deb_4_action}} |
| 5 | {{deb_5_nom}} | {{deb_5_montant}} | {{deb_5_pct}}% | {{deb_5_anciennete}} | {{deb_5_action}} |
| 6 | {{deb_6_nom}} | {{deb_6_montant}} | {{deb_6_pct}}% | {{deb_6_anciennete}} | {{deb_6_action}} |
| 7 | {{deb_7_nom}} | {{deb_7_montant}} | {{deb_7_pct}}% | {{deb_7_anciennete}} | {{deb_7_action}} |
| 8 | {{deb_8_nom}} | {{deb_8_montant}} | {{deb_8_pct}}% | {{deb_8_anciennete}} | {{deb_8_action}} |
| 9 | {{deb_9_nom}} | {{deb_9_montant}} | {{deb_9_pct}}% | {{deb_9_anciennete}} | {{deb_9_action}} |
| 10 | {{deb_10_nom}} | {{deb_10_montant}} | {{deb_10_pct}}% | {{deb_10_anciennete}} | {{deb_10_action}} |

Concentration top 10 : {{concentration_top10}}% des créances totales. Top client : {{top_client_pct}}% seul.

## Plan de relances du mois

### Niveau 1 (retard 0 à 30j) : relance douce

- Nombre de clients concernés : {{nb_relance_1}}
- Canal : email automatique J+3 après échéance
- Montant concerné : {{montant_relance_1}} k EUR

### Niveau 2 (retard 31 à 60j) : relance commerciale

- Nombre de clients concernés : {{nb_relance_2}}
- Canal : email nominatif + appel téléphonique
- Montant concerné : {{montant_relance_2}} k EUR
- Porteur : équipe commerciale

### Niveau 3 (retard 61 à 90j) : mise en demeure

- Nombre de clients concernés : {{nb_relance_3}}
- Canal : LRAR avec mise en demeure formelle
- Montant concerné : {{montant_relance_3}} k EUR
- Porteur : CFO ou juridique

### Niveau 4 (retard supérieur à 90j) : contentieux

- Nombre de clients concernés : {{nb_contentieux}}
- Action : transmission avocat ou société de recouvrement
- Montant concerné : {{montant_contentieux}} k EUR
- Provision à constituer : {{provision_contentieux}} k EUR

## Options

**A. Intensification des relances internes (recommandée si sous 8% de créances plus 60j)**
Renforcement de l'équipe AR (accounts receivable) ou outillage (Upflow, Sidetrade). Coût estimé : {{cout_ar}} k EUR. Gain DSO attendu : {{gain_dso_a}} jours.

**B. Mise en place d'un escompte commercial**
Escompte 2/10 Net 30 sur les nouvelles factures. Coût : {{cout_escompte}} k EUR/an (2% du CA). Gain DSO attendu : {{gain_dso_b}} jours.

**C. Affacturage des créances top débiteurs**
Cession des créances avec ou sans recours. Cash libéré : {{cash_affact}} k EUR. Coût : {{cout_affact}}% sur montant factoré.

## Recommandation

Retenir l'option A en priorité. Deux raisons : (1) les pratiques internes de relance peuvent être professionalisées sans coût externe important ; (2) l'affacturage est une solution de bridge, pas de fond. Caveat : si DSO supérieur à 90 jours constants et impact sur la trésorerie, l'option C en ponctuel peut être justifiée.

## Next

Lancer les relances niveau 2 et 3 cette semaine. Revoir le top 10 débiteurs avec l'équipe commerciale. Porteur : CFO + responsable AR. Prochaine revue : {{date_prochaine_revue}}.

## Limites

Le DSO calculé est un indicateur moyen ; il ne reflète pas la distribution réelle des retards (un gros client en retard peut masquer une base saine). Pour décision de provision douteuse ou passage en perte, validation de l'EC nécessaire (critères comptables PCG article 312-5). La mise en contentieux doit être coordonnée avec un avocat spécialisé pour éviter les erreurs de procédure (prescription, délai de contestation). L'affacturage engage une relation durable avec un factor : l'analyser comme une décision structurelle.
