# Veille réglementaire, semaine {{ww}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Semaine** : W{{ww}} {{yyyy}}
**Généré le** : {{date_today}}
**Secteur** : {{secteur_category}}
**Taille** : {{taille}}

## Faits

- Période de revue : du {{date_debut_semaine}} au {{date_fin_semaine}}
- Sources revuées : ANC (comptable), IASB (IFRS), AMF (marchés), ACPR (banques/assurances), Légifrance (juridique), Bofip (fiscal), URSSAF (social), CNIL (données personnelles), EFRAG (CSRD/ESRS)
- Nombre de publications analysées cette semaine : {{nb_publications}}
- Publications matchant le profil de {{denomination}} : {{nb_publications_match}}

## Hypothèses

- H1 : le profil de {{denomination}} utilisé pour le filtrage est celui de `private/companies/{{siren}}/company.json` au {{date_today}} (taille, secteur, structure, obligations)
- H2 : les publications antérieures de plus de 7 jours ne sont pas rappelées, sauf si l'entrée en vigueur a lieu cette semaine
- H3 : les projets de texte (non publiés au JO) sont signalés comme veille anticipative mais n'engagent pas encore d'action

## Analyse

### Changements à impact direct sur {{denomination}}

| Source | Date | Référence | Objet | Entrée en vigueur | Impact |
|--------|------|-----------|-------|-------------------|--------|
| {{source_1}} | {{date_1}} | {{ref_1}} | {{objet_1}} | {{eev_1}} | {{impact_1}} |
| {{source_2}} | {{date_2}} | {{ref_2}} | {{objet_2}} | {{eev_2}} | {{impact_2}} |
| {{source_3}} | {{date_3}} | {{ref_3}} | {{objet_3}} | {{eev_3}} | {{impact_3}} |

### Changements à impact indirect (secteur ou taille)

| Source | Référence | Objet | Statut |
|--------|-----------|-------|--------|
| {{source_ind_1}} | {{ref_ind_1}} | {{objet_ind_1}} | {{statut_ind_1}} |
| {{source_ind_2}} | {{ref_ind_2}} | {{objet_ind_2}} | {{statut_ind_2}} |

### Veille anticipative (projets de texte, consultations)

- {{veille_antic_1}}
- {{veille_antic_2}}

### Synthèse opérationnelle

- Nombre de processus internes à revoir : {{nb_process_revoir}}
- Délai moyen avant entrée en vigueur : {{delai_moyen_eev}} jours
- Actions urgentes (EEV < 30 jours) : {{nb_urgences}}

## Risques

- {{risque_1_niveau}} {{risque_1_titre}} : {{risque_1_desc}}.
- {{risque_2_niveau}} {{risque_2_titre}} : {{risque_2_desc}}.

## Actions

- [ ] Étudier en détail les publications à impact direct listées ci-dessus
- [ ] Mettre à jour les procédures internes impactées avant l'entrée en vigueur
- [ ] Former les équipes concernées (compta, paie, juridique) sur les changements applicables
- [ ] Consulter l'EC ou l'avocat si le changement remet en cause une option fiscale ou une pratique comptable
- [ ] Noter au calendrier les échéances d'entrée en vigueur pour anticipation
- [ ] Archiver cette veille dans le dossier réglementaire {{yyyy}} pour audit trail

## Limites

Cette veille est produite automatiquement sur la base des publications officielles référencées. Elle ne couvre pas les circulaires internes des administrations (DGFiP, URSSAF) ni les doctrines non publiées. Les commentaires d'application (Bofip, Precis) sont inclus lorsqu'une mise à jour est détectée dans la semaine. Pour interprétation d'un texte complexe ou en cas de contentieux, consulter un avocat fiscaliste ou un juriste spécialisé. La présente veille ne vaut pas conseil juridique et ne se substitue pas à l'accompagnement de votre expert-comptable ou conseil.
