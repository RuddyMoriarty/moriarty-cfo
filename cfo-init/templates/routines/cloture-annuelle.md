# Clôture annuelle {{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Exercice** : {{yyyy}}
**Date de clôture** : {{date_cloture}}
**Généré le** : {{date_today}} (J-45 avant échéance fiscale)

## Faits

- Société : {{denomination}}, SIREN {{siren}}, forme juridique {{forme_juridique}}
- Exercice clos : {{date_cloture}}
- Régime fiscal : {{regime_fiscal}} (IS taux normal 25% ou micro, selon configuration)
- Taille : {{taille}} (TPE/PE/ME/ETI)
- Obligation CAC : {{obligation_cac}} (déclenché au-dessus des seuils 2/3 critères)
- Comptes consolidés : {{comptes_consos}} (si groupe)
- Délai liasse fiscale 2033/2065 : 3 mois après clôture (soit {{date_limite_liasse}})
- Délai dépôt comptes annuels au greffe : 7 mois après clôture ({{date_limite_depot}})

## Hypothèses

- H1 : l'exercice {{yyyy}} est de 12 mois (non raccourci, non allongé)
- H2 : aucun changement de méthode comptable par rapport à N-1
- H3 : les provisions pour risques ont été réévaluées en décembre {{yyyy}} sur la base des informations disponibles au 31/12
- H4 : les engagements hors bilan (crédit-bail, cautions, nantissements) sont recensés et annexés
- H5 : les écritures d'inventaire (CCA, PCA, FNP, AAR) sont validées avec l'expert-comptable avant le {{date_validation_ec}}

## Analyse

### Échéances fiscales et légales

| Échéance | Date limite | Statut |
|----------|-------------|--------|
| Liasse fiscale 2033 ou 2065 | {{date_limite_liasse}} | {{statut_liasse}} |
| Déclaration IS (2065) | {{date_limite_is}} | {{statut_is}} |
| Déclaration CVAE | 2ème jour ouvré suivant 1er mai | {{statut_cvae}} |
| FEC (demande contrôle fiscal) | À disposition sous 48h | {{statut_fec}} |
| Dépôt comptes annuels au greffe | {{date_limite_depot}} | {{statut_depot}} |
| Rapport de gestion | Avant AG d'approbation | {{statut_rapport_gestion}} |
| Convocation AG approbation | {{date_convocation_ag}} | {{statut_ag}} |

### Comptes de synthèse provisoires

| KPI | Exercice {{yyyy}} | Exercice {{yyyy_prev}} | Evolution |
|-----|-------------------|------------------------|-----------|
| CA HT annuel | {{ca_annuel}} | {{ca_annuel_n1}} | {{ca_evo}}% |
| Résultat d'exploitation | {{rex_annuel}} | {{rex_n1}} | {{rex_evo}}% |
| Résultat financier | {{rf_annuel}} | {{rf_n1}} | {{rf_evo}}% |
| Résultat exceptionnel | {{rexc_annuel}} | {{rexc_n1}} | - |
| Résultat net | {{rn_annuel}} | {{rn_n1}} | {{rn_evo}}% |
| Total bilan | {{bilan_total}} | {{bilan_n1}} | {{bilan_evo}}% |
| Capitaux propres | {{cp_annuel}} | {{cp_n1}} | {{cp_evo}}% |

### Points d'attention comptables

- Changements de méthode : {{changement_methode}}
- Produits et charges exceptionnels >seuil : {{exceptionnel_signif}}
- Provisions nouvelles ou reprises : {{provisions_evolution}}
- Immobilisations : acquisitions {{acquisitions}}, cessions {{cessions}}, dépréciations {{depreciations}}
- Créances douteuses : {{creances_douteuses}}

### Coordination CAC (si obligation_cac)

- CAC titulaire : {{cac_titulaire}}
- CAC suppléant : {{cac_suppleant}}
- Date de réunion plan d'audit : {{date_plan_audit}}
- Date de réunion des conclusions : {{date_conclusions}}
- Findings précédents à statuer : {{findings_precedents}}

## Risques

- {{risque_1_niveau}} Dépassement délai liasse fiscale : pénalité 10% minimum de l'IS dû. Mitigation : verrouiller la balance avec l'EC avant J-30.
- {{risque_2_niveau}} Non-dépôt des comptes au greffe : amende et demande d'injonction. Mitigation : planifier l'AG 6 mois après clôture.
- {{risque_3_niveau}} Redressement sur exceptionnel significatif : documenter l'ensemble des opérations atypiques. Mitigation : revue juridique et fiscale préalable.
- {{risque_4_niveau}} Covenants bancaires à respecter : validation du ratio sur comptes arrêtés. Mitigation : exécuter la routine covenant-monitoring en parallèle.

## Actions

- [ ] Valider la balance clôturée avec l'EC au plus tard le {{date_validation_ec}}
- [ ] Transmettre la liasse fiscale à l'administration via EDI TVA/EDI TDFC avant le {{date_limite_liasse}}
- [ ] Préparer le rapport de gestion (obligatoire >= seuils SA/SAS)
- [ ] Rédiger la lettre d'affirmation pour le CAC (si applicable)
- [ ] Organiser le CDA puis l'AG d'approbation avant le {{date_limite_depot}}
- [ ] Déposer les comptes annuels au greffe et sur infogreffe.fr
- [ ] Archiver le FEC définitif + sauvegarde hors-site (6 ans minimum)
- [ ] Actualiser le cash-flow forecast avec les données réelles de clôture

## Limites

Cette routine pilote la coordination de clôture annuelle mais ne remplace pas la revue experte. Les comptes arrêtés doivent être validés par l'expert-comptable et, le cas échéant, certifiés par le CAC. Les déclarations fiscales (liasse, CVAE, IS) relèvent de la responsabilité du dirigeant : toute erreur engage sa responsabilité. Pour toute optimisation fiscale (CIR, CII, report déficitaire, intégration), consulter un avocat fiscaliste. La présente checklist est indicative et doit être adaptée aux spécificités de {{denomination}} (structure groupe, opérations exceptionnelles, litiges en cours).
