# Cash burn et runway, W{{ww}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Semaine** : W{{ww}} {{yyyy}}
**Généré le** : {{date_today}}
**Statut startup** : {{statut_startup}}

## Pourquoi

Suivi hebdomadaire du cash burn et du runway pour les startups et scale-ups. Objectif : détecter toute dérive nécessitant une action (gel OPEX, report CAPEX, prospection investisseurs) au plus tôt. Seuil d'alerte : runway inférieur à 6 mois. Seuil critique : runway inférieur à 3 mois (déclenche préparation d'urgence).

## Chiffres clés

| KPI | Semaine courante | Semaine précédente | Signal |
|-----|------------------|--------------------|--------|
| Cash en banque | {{cash_actuel}} k EUR | {{cash_prev}} k EUR | {{signal_cash}} |
| Burn hebdo net | {{burn_hebdo_net}} k EUR | {{burn_prev}} k EUR | {{signal_burn}} |
| Burn mensuel net moyen (12 semaines) | {{burn_mensuel}} k EUR/mois | {{burn_mensuel_prev}} | {{signal_burn_m}} |
| Runway estimé | {{runway_mois}} mois | {{runway_prev}} mois | {{signal_runway}} |
| Runway inclus hypothèses CA | {{runway_avec_ca}} mois | - | - |

## Analyse détaillée

### Décomposition du burn

| Catégorie | Hebdo moyen (12 sem) | Mensuel équivalent | Part du burn |
|-----------|----------------------|---------------------|--------------|
| Salaires et charges | {{burn_sal}} k | {{burn_sal_m}} k | {{burn_sal_pct}}% |
| Infrastructure (cloud, SaaS) | {{burn_infra}} k | {{burn_infra_m}} k | {{burn_infra_pct}}% |
| Marketing et growth | {{burn_mkt}} k | {{burn_mkt_m}} k | {{burn_mkt_pct}}% |
| Loyer et frais généraux | {{burn_fg}} k | {{burn_fg_m}} k | {{burn_fg_pct}}% |
| Autres OPEX | {{burn_autres}} k | {{burn_autres_m}} k | {{burn_autres_pct}}% |
| **Gross burn total** | {{gross_burn}} k | {{gross_burn_m}} k | 100% |
| Encaissements clients | -{{encaiss}} k | -{{encaiss_m}} k | - |
| **Net burn** | **{{net_burn}} k** | **{{net_burn_m}} k** | - |

### Trajectoire runway

| Scénario | CA projeté/mois | Burn net/mois | Runway |
|----------|------------------|----------------|--------|
| Pessimiste (CA flat) | {{ca_pess}} | {{net_burn_pess}} | {{runway_pess}} mois |
| Réaliste (plan actuel) | {{ca_real}} | {{net_burn_real}} | {{runway_real}} mois |
| Optimiste (accélération) | {{ca_opti}} | {{net_burn_opti}} | {{runway_opti}} mois |

### Alertes et seuils

- Runway actuel : {{runway_mois}} mois
- Seuil d'alerte (6 mois) : {{statut_alerte}}
- Seuil critique (3 mois) : {{statut_critique}}
- Seuil de levée lancée (12 mois avant cash zéro) : {{statut_leveur}}

## Options

**A. Maintien du plan actuel (recommandée si runway supérieur à 9 mois)**
Pas d'action corrective. Monitoring hebdo continu. Vérification mensuelle de la discipline OPEX.

**B. Réduction du burn sans toucher la roadmap produit (runway 6-9 mois)**
Actions : gel des recrutements non-core, renégociation SaaS, suspension marketing top-of-funnel. Impact : économie de {{economie_b}} k EUR/mois, extension runway +{{extension_b}} mois.

**C. Plan de continuité (runway inférieur à 6 mois)**
Actions : préparation pont VC via venture debt, priorisation du pipeline investisseurs, réduction effectif ciblée si plan ABC non suffisant. Déclenchement de la procédure "cash preservation mode".

**D. Levée de fonds (runway inférieur à 12 mois pour série)**
Actions : préparation du data room, sondage du marché investisseurs, brief executive summary. Durée process médiane : 4 à 6 mois en post-Série A.

## Recommandation

Si runway compris entre 6 et 9 mois : activer l'option B immédiatement. Raisons : (1) les mesures sont non-destructives pour la roadmap produit ; (2) elles achètent 2 à 3 mois de runway supplémentaire pour préparer une levée dans de bonnes conditions. Caveat : toute mesure touchant les équipes doit être concertée avec la direction et les co-fondateurs.

## Next

Revue en comité restreint cette semaine. Porteur : CEO + CFO. Si seuil d'alerte franchi ce mois, brief board dans les 15 jours. Action associée : engager le sondage du marché investisseurs si runway inférieur à 12 mois.

## Limites

Les projections de runway reposent sur le burn observé sur 12 semaines et les hypothèses de CA communiquées. Un changement brutal dans l'une des deux variables fausse l'estimation. Le runway n'intègre pas les lignes de crédit potentiellement mobilisables ni les subventions en cours (BPI, CIR) dont le délai d'encaissement est incertain. Pour décision de levée ou restructuration, compléter par une analyse détaillée avec un conseil en corporate finance.
