# Revue paie et DSN {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période de paie** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}
**Effectif** : {{effectif}} salariés

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Période de déclaration DSN : {{mm}}/{{yyyy}}
- Échéance DSN mensuelle : 5 ou 15 du mois M+1 selon effectif (seuil 50 ETP)
- Date de paie : {{date_paie}} ({{jour_paie_theorique}})
- Effectif en paie ce mois : {{nb_bulletins}} bulletins
- Nombre de CDI : {{nb_cdi}}
- Nombre de CDD : {{nb_cdd}}
- Nombre d'alternants : {{nb_alternants}}
- Nombre d'entrées / sorties du mois : {{nb_entrees}} / {{nb_sorties}}

## Hypothèses

- H1 : les bulletins du mois {{mm}}/{{yyyy}} ont été produits sur la base des variables de paie communiquées avant le {{date_cutoff_paie}} (pointages, primes, absences, tickets restaurant)
- H2 : les taux AT/MP appliqués sont ceux notifiés par la CARSAT pour {{yyyy}} (section {{section_atmp}}, taux {{taux_atmp}}%)
- H3 : la DSN est générée par le logiciel de paie {{logiciel_paie}} et contrôlée avant dépôt

## Analyse

### Masse salariale du mois

| Composante | Montant mois | Vs N-1 | Vs budget |
|------------|--------------|--------|-----------|
| Salaires bruts | {{salaires_bruts}} | {{sal_vs_n1}}% | {{sal_vs_budget}}% |
| Cotisations patronales | {{cot_patronales}} | - | - |
| Masse salariale chargée | {{masse_chargee}} | {{masse_vs_n1}}% | {{masse_vs_budget}}% |
| Taux de charges patronales | {{taux_charges}}% | {{taux_n1}}% | - |
| Cotisations salariales | {{cot_salariales}} | - | - |
| Net à payer salariés | {{net_a_payer}} | - | - |

### Cotisations à verser ce mois

| Organisme | Assiette | Montant | Échéance |
|-----------|----------|---------|----------|
| URSSAF | {{urssaf_assiette}} | {{urssaf_montant}} | {{urssaf_echeance}} |
| AGIRC-ARRCO | {{arrco_assiette}} | {{arrco_montant}} | {{arrco_echeance}} |
| Prévoyance | {{prev_assiette}} | {{prev_montant}} | {{prev_echeance}} |
| Mutuelle | {{mutuelle_assiette}} | {{mutuelle_montant}} | {{mutuelle_echeance}} |
| Taxe apprentissage | {{ta_assiette}} | {{ta_montant}} | Annuelle, mai N+1 |
| Effort formation | {{effort_assiette}} | {{effort_montant}} | Annuelle, mai N+1 |

Total à verser ce mois : {{total_cotisations}}.

### Contrôles de conformité DSN

| Contrôle | Statut | Commentaire |
|----------|--------|-------------|
| Nombre de salariés déclarés = paie | {{ctrl_1}} | - |
| Cohérence bases CSG/CRDS vs bruts | {{ctrl_2}} | - |
| Cotisations URSSAF calculées correctement | {{ctrl_3}} | - |
| Blocs individuels complets (naissance, NIR, contrat) | {{ctrl_4}} | - |
| Arrêts maladie, congés maternité déclarés | {{ctrl_5}} | - |
| Absences saisies en type DSN correct | {{ctrl_6}} | - |
| Fin de contrat avec bloc 62 rempli | {{ctrl_7}} | - |

### Alertes détectées sur les bulletins du mois

- {{alerte_1_type}} : {{alerte_1_nb}} bulletin(s) concerné(s). {{alerte_1_detail}}.
- {{alerte_2_type}} : {{alerte_2_nb}} bulletin(s) concerné(s). {{alerte_2_detail}}.

## Risques

- {{risque_1_niveau}} Retard DSN : pénalité 7,50 EUR par salarié non déclaré et par mois de retard (article L 244-1 CSS)
- {{risque_2_niveau}} Erreur de calcul de cotisations : redressement URSSAF lors du contrôle sur 3 ans
- {{risque_3_niveau}} Non-versement des cotisations dans les délais : majoration de 5% + intérêts de retard 0,20%/mois
- {{risque_4_niveau}} Non-respect de l'obligation d'information CSE si licenciement économique annoncé

## Actions

- [ ] Transmettre la DSN mensuelle à net-entreprises.fr avant le {{date_limite_dsn}}
- [ ] Procéder au versement URSSAF avant le {{date_limite_urssaf}}
- [ ] Valider les bulletins avec RH ou dirigeant avant diffusion aux salariés
- [ ] Corriger les anomalies détectées ({{nb_anomalies}} identifiées ce mois)
- [ ] Archiver les bulletins et la DSN sur coffre-fort électronique (durée de conservation : 50 ans pour les bulletins)
- [ ] Préparer la DSN événementielle si départs en cours de mois ({{dsn_evenementielle}} à faire)

## Limites

Cette revue contrôle la cohérence de la paie et de la DSN mais ne constitue pas une validation juridique définitive. Les bulletins sont la responsabilité de l'employeur. Pour toute situation complexe (licenciement, rupture conventionnelle, dispositif Emploi senior, IFC, saisie-arrêt), consulter un juriste en droit social ou l'avocat social de {{denomination}}. Les taux URSSAF et AGIRC-ARRCO sont mis à jour chaque 1er janvier et 1er juillet, vérifier leur actualité. La DSN reste l'outil opposable en cas de contrôle.
