# TJM et productivité facturée, W{{ww}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Semaine** : W{{ww}} {{yyyy}}
**Généré le** : {{date_today}}
**Modèle** : Services B2B facturés au temps passé

## Pourquoi

Suivi hebdomadaire de la productivité de l'équipe de consultants : taux d'utilisation, TJM moyen, facturation facturée. Décision en jeu : ajustements commerciaux (recrutement, remplacement), arbitrages allocation missions, alertes sur la rentabilité par consultant.

## Chiffres clés

| KPI | Semaine | Cumul 4 sem | Cible {{yyyy}} | Signal |
|-----|---------|-------------|-----------------|--------|
| CA facturable produit | {{ca_fac_sem}} k | {{ca_fac_4sem}} k | {{ca_fac_cible}} k | {{signal_ca}} |
| Jours facturés | {{jours_fac}} j | {{jours_fac_4sem}} j | {{jours_cible}} j | {{signal_jours}} |
| TJM moyen | {{tjm_moyen}} EUR | {{tjm_moyen_4sem}} EUR | sup à {{tjm_cible}} | {{signal_tjm}} |
| Taux d'utilisation | {{tu}}% | {{tu_4sem}}% | sup à {{tu_cible}}% | {{signal_tu}} |
| Nombre de consultants facturés | {{nb_consult_fac}} / {{nb_consult_tot}} | - | - | - |

## Analyse par consultant

| Consultant | TJM | Jours facturés | Taux utilisation | Commentaire |
|------------|-----|----------------|-------------------|-------------|
| {{consult_1_nom}} | {{consult_1_tjm}} | {{consult_1_jours}} j | {{consult_1_tu}}% | {{consult_1_com}} |
| {{consult_2_nom}} | {{consult_2_tjm}} | {{consult_2_jours}} j | {{consult_2_tu}}% | {{consult_2_com}} |
| {{consult_3_nom}} | {{consult_3_tjm}} | {{consult_3_jours}} j | {{consult_3_tu}}% | {{consult_3_com}} |
| {{consult_4_nom}} | {{consult_4_tjm}} | {{consult_4_jours}} j | {{consult_4_tu}}% | {{consult_4_com}} |
| {{consult_5_nom}} | {{consult_5_tjm}} | {{consult_5_jours}} j | {{consult_5_tu}}% | {{consult_5_com}} |

## Analyse par mission

| Mission | Client | Type contrat | Jours semaine | TJM | Statut |
|---------|--------|--------------|----------------|-----|--------|
| {{mission_1_nom}} | {{mission_1_client}} | {{mission_1_type}} | {{mission_1_jours}} | {{mission_1_tjm}} | {{mission_1_statut}} |
| {{mission_2_nom}} | {{mission_2_client}} | {{mission_2_type}} | {{mission_2_jours}} | {{mission_2_tjm}} | {{mission_2_statut}} |
| {{mission_3_nom}} | {{mission_3_client}} | {{mission_3_type}} | {{mission_3_jours}} | {{mission_3_tjm}} | {{mission_3_statut}} |
| {{mission_4_nom}} | {{mission_4_client}} | {{mission_4_type}} | {{mission_4_jours}} | {{mission_4_tjm}} | {{mission_4_statut}} |

### Décomposition du temps (semaine écoulée)

| Catégorie | Jours | Part |
|-----------|-------|------|
| Facturable client | {{jours_fac}} | {{pct_fac}}% |
| Interne projet (R&D, formation, outils) | {{jours_interne}} | {{pct_interne}}% |
| Avant-vente (réponses appels d'offres) | {{jours_av}} | {{pct_av}}% |
| Indisponibilité (congés, maladie, férié) | {{jours_indispo}} | {{pct_indispo}}% |

### Pipeline et charge future

- Missions fermes sur 4 prochaines semaines : {{missions_fermes}} jours
- Missions en attente de signature : {{missions_attente}} jours
- Taux de couverture pipeline 4 semaines : {{couverture_pipe}}%
- Prochaines fins de mission : {{prochaines_fins}}

## Alertes détectées

### Consultants sous-utilisés (TU inférieur à {{tu_cible}}%)

- {{sub_1_consult}} : {{sub_1_raison}}
- {{sub_2_consult}} : {{sub_2_raison}}

### Consultants sur-utilisés (TU supérieur à 95% soutenu)

- {{sur_1_consult}} : risque de burn-out, à surveiller

### TJM sous la cible

- {{tjm_bas_1}} : mission {{tjm_bas_1_mission}}, justification : {{tjm_bas_1_just}}

## Risques

- {{risque_1_niveau}} Baisse du TU sur plus de 3 semaines consécutives : signal avant-coureur de problème commercial
- {{risque_2_niveau}} Concentration excessive sur un client (supérieur à 30% du CA facturable) : risque de dépendance
- {{risque_3_niveau}} TJM dégradé sur les nouveaux contrats : pression concurrentielle ou commercial faible

## Actions

- [ ] Re-positionner les consultants sous-utilisés sur des missions en cours ou accélérer l'avant-vente
- [ ] Vérifier la facturation effective des jours saisis (time tracking vs factures émises)
- [ ] Programmer les entretiens mi-mission pour sécuriser les extensions
- [ ] Anticiper les fins de mission proches sans remplacement identifié
- [ ] Challenger les nouvelles propositions commerciales au TJM sous cible
- [ ] Alerter les managers sur les consultants en sur-utilisation pour risque burn-out

## Limites

Les indicateurs TJM/TU reposent sur le time tracking des consultants. Une saisie approximative fausse les chiffres. Les jours avant-vente peuvent être facturables a posteriori si la mission est signée : retraitement nécessaire en fin de trimestre. Le TJM affiché est le TJM brut facturé ; pour rentabilité réelle, retrancher les coûts de structure (management, outils, locaux) et les coûts commerciaux. Pour pilotage fin des unit economics en services B2B, établir un suivi TJM net par consultant trimestriel.
