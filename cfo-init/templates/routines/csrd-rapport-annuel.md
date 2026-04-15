# Rapport CSRD/ESRS annuel {{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Exercice** : {{yyyy}}
**Généré le** : {{date_today}} (J-180 avant clôture)
**Wave CSRD** : {{csrd_wave}} (wave 1 = 2024, wave 2 = 2025, wave 3 = 2026)

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Taille : {{taille}} (ETI, GE)
- Obligation CSRD applicable à compter de l'exercice : {{exercice_premier_csrd}}
- Date limite publication 1er rapport : {{date_limite_publication}}
- Périmètre de reporting : {{perimetre_reporting}} (conso, social)
- Assurance externe obligatoire : {{assurance_obligatoire}} (limited assurance puis reasonable)
- Référentiel : ESRS (European Sustainability Reporting Standards)

## Hypothèses

- H1 : la double matérialité a été réalisée sur la base d'une consultation des parties prenantes effectuée entre le {{date_consultation_debut}} et le {{date_consultation_fin}}
- H2 : les données chiffrées ESG sont collectées via {{outil_collecte}} et auditables
- H3 : la méthodologie de calcul des émissions GES suit le protocol GHG scope 1, 2 et 3 selon ESRS E1

## Analyse

### Double matérialité

#### Matérialité d'impact (inside-out)

Identifie les impacts positifs et négatifs de {{denomination}} sur l'environnement et la société.

| Enjeu | Intensité | Portée | Caractère irréversible | Matérialité |
|-------|-----------|--------|------------------------|-------------|
| {{imp_1_enjeu}} | {{imp_1_intensite}} | {{imp_1_portee}} | {{imp_1_irrev}} | {{imp_1_materialite}} |
| {{imp_2_enjeu}} | {{imp_2_intensite}} | {{imp_2_portee}} | {{imp_2_irrev}} | {{imp_2_materialite}} |
| {{imp_3_enjeu}} | {{imp_3_intensite}} | {{imp_3_portee}} | {{imp_3_irrev}} | {{imp_3_materialite}} |

#### Matérialité financière (outside-in)

Identifie comment les facteurs ESG impactent {{denomination}}.

| Enjeu | Impact financier potentiel | Horizon | Probabilité | Matérialité |
|-------|----------------------------|---------|-------------|-------------|
| {{fin_1_enjeu}} | {{fin_1_impact}} | {{fin_1_horizon}} | {{fin_1_proba}} | {{fin_1_materialite}} |
| {{fin_2_enjeu}} | {{fin_2_impact}} | {{fin_2_horizon}} | {{fin_2_proba}} | {{fin_2_materialite}} |
| {{fin_3_enjeu}} | {{fin_3_impact}} | {{fin_3_horizon}} | {{fin_3_proba}} | {{fin_3_materialite}} |

### ESRS environnement

#### E1 - Changement climatique

- Scope 1 (émissions directes) : {{scope1}} tCO2e
- Scope 2 (électricité achetée, location-based) : {{scope2}} tCO2e
- Scope 3 (chaîne de valeur) : {{scope3}} tCO2e (catégories couvertes : {{scope3_cat}})
- Total émissions : {{total_ges}} tCO2e
- Intensité carbone (tCO2e / M EUR de CA) : {{intensite_carbone}}
- Trajectoire 1.5°C : {{traj_1_5}} (SBTi validée ou alignée)
- Plan de transition : {{plan_transition}}

#### E2 - Pollution

- Substances inscrites à REACH : {{substances_reach}}
- Émissions dans l'air / l'eau / les sols : {{emissions_autres}}

#### E3 - Ressources en eau

- Consommation d'eau : {{conso_eau}} m3
- Zones de stress hydrique : {{zones_stress}}

#### E4 - Biodiversité et écosystèmes

- Sites dans/proches d'aires protégées : {{sites_protegees}}
- Espèces menacées impactées : {{especes_menacees}}

#### E5 - Économie circulaire

- Volume de déchets : {{volume_dechets}} t
- Taux de valorisation / recyclage : {{taux_recyclage}}%
- Part de matières recyclées dans les intrants : {{matiere_recyclee}}%

### ESRS social

#### S1 - Personnel de l'entreprise

- Effectif : {{effectif}} ETP
- Taux de turnover : {{turnover}}%
- Taux d'accidents du travail : {{taux_accidents}}%
- Écart salarial femmes/hommes : {{ecart_salaire}}%
- Part des femmes au CODIR : {{femmes_codir}}%

#### S2 - Travailleurs de la chaîne de valeur

- % fournisseurs évalués ESG : {{fourn_evalues}}%
- Audits sociaux réalisés : {{audits_sociaux}}

#### S3 - Communautés affectées

- Projets à impact sur communautés locales : {{projets_impact}}

#### S4 - Consommateurs et utilisateurs

- Incidents de sécurité produit : {{incidents_secu}}
- Procédures de protection des données : {{protection_donnees}}

### ESRS gouvernance

#### G1 - Conduite des affaires

- Présence d'un code de conduite : {{code_conduite}}
- Procédures anticorruption (Sapin II si applicable) : {{sapin2}}
- Nombre de signalements lanceurs d'alerte : {{signalements}}
- Contentieux éthiques en cours : {{contentieux_ethiques}}

## Roadmap de mise en conformité

### Actions T-12 mois

- {{action_t12_1}}
- {{action_t12_2}}

### Actions T-6 mois

- {{action_t6_1}}
- {{action_t6_2}}

### Actions T-3 mois

- {{action_t3_1}}
- {{action_t3_2}}

### Actions finales T-1 mois

- Validation par la direction
- Contrôle interne avant envoi CAC
- Préparation du rapport publiable

## Risques

- {{risque_1_niveau}} Non-publication dans les délais : amendes jusqu'à 3% du CA (article L 232-23 du Code de commerce)
- {{risque_2_niveau}} Assurance limitée défavorable du CAC : impact réputationnel majeur
- {{risque_3_niveau}} Divergence matérialité évaluée vs perception des parties prenantes : dossier attaquable
- {{risque_4_niveau}} Manque de données historiques fiables sur les indicateurs ESRS : baseline difficile à construire

## Actions

- [ ] Valider les indicateurs ESRS matériels avec la direction développement durable
- [ ] Coordonner avec le CAC l'accompagnement sur l'assurance limited sur le premier rapport
- [ ] Compléter les outils de collecte de données ESG (EcoVadis, Sweep, Net0, autre)
- [ ] Former les équipes opérationnelles sur les points de collecte
- [ ] Lancer les audits fournisseurs prioritaires (top 20% du CA achats)
- [ ] Déployer le plan de transition climat (scope 1, 2, 3) avec engagements chiffrés
- [ ] Présenter un état d'avancement au board trimestriel (dashboard CSRD)

## Limites

La CSRD est une réglementation nouvelle (applicable à partir de 2024 pour les grandes entreprises), en évolution constante (clarifications EFRAG, délégués Commission). Les interprétations des ESRS peuvent diverger entre CAC et cabinets. Cette routine coordonne le processus mais ne remplace pas l'expertise d'un cabinet spécialisé en reporting durabilité (Big 4, cabinets ESG). Pour première publication, budget conseil externe à prévoir (de 80 à 300 k EUR selon complexité). Les données ESG chiffrées ici doivent être vérifiées et validées par les fonctions opérationnelles concernées (environnement, RH, supply chain, juridique) avant inclusion au rapport final.
