# Consolidation IFRS T{{qq}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}} (entité consolidante)
**Période** : T{{qq}} {{yyyy}}
**Généré le** : {{date_today}}
**Référentiel** : {{referentiel}} (IFRS ou French GAAP consolidé)

## Faits

- Entité consolidante : {{denomination}}, SIREN {{siren}}
- Nombre d'entités dans le périmètre : {{nb_entites}}
- Périmètre : voir liste détaillée ci-dessous
- Date de clôture consolidée : {{date_cloture_conso}}
- Référentiel : {{referentiel}}
- Devise de consolidation : EUR
- Monnaies de présentation des filiales : {{monnaies_presentation}}
- Commissaire aux comptes consolidé : {{cac_conso}}

## Hypothèses

- H1 : toutes les filiales ont arrêté leurs comptes sociaux à la date de clôture consolidée ({{date_cloture_conso}}) avec les mêmes méthodes comptables
- H2 : les taux de change utilisés sont les taux de clôture pour le bilan et les taux moyens pour le compte de résultat (IAS 21)
- H3 : les retraitements d'homogénéisation entre référentiels nationaux et IFRS sont effectués au niveau de l'entité consolidante

## Analyse

### Périmètre de consolidation

| Entité | SIREN/ID | Pays | Méthode | % Intérêt | % Contrôle | Date entrée |
|--------|----------|------|---------|-----------|------------|-------------|
| {{entite_1_nom}} | {{entite_1_id}} | {{entite_1_pays}} | IG | {{entite_1_int}}% | {{entite_1_ctrl}}% | {{entite_1_entree}} |
| {{entite_2_nom}} | {{entite_2_id}} | {{entite_2_pays}} | IG | {{entite_2_int}}% | {{entite_2_ctrl}}% | {{entite_2_entree}} |
| {{entite_3_nom}} | {{entite_3_id}} | {{entite_3_pays}} | IP | {{entite_3_int}}% | {{entite_3_ctrl}}% | {{entite_3_entree}} |
| {{entite_4_nom}} | {{entite_4_id}} | {{entite_4_pays}} | ME | {{entite_4_int}}% | {{entite_4_ctrl}}% | {{entite_4_entree}} |

Méthodes : IG (intégration globale, contrôle exclusif), IP (intégration proportionnelle, contrôle conjoint, deprecated en IFRS depuis IFRS 11), ME (mise en équivalence, influence notable).

### États financiers consolidés simplifiés

#### Compte de résultat consolidé

| Poste | T{{qq}} {{yyyy}} | T{{qq}} {{yyyy_prev}} | Evolution |
|-------|------------------|-----------------------|-----------|
| CA consolidé | {{ca_conso}} | {{ca_conso_n1}} | {{ca_evo}}% |
| EBITDA consolidé | {{ebitda_conso}} | {{ebitda_n1}} | {{ebitda_evo}}% |
| Résultat d'exploitation | {{rex_conso}} | {{rex_n1}} | {{rex_evo}}% |
| Résultat financier | {{rf_conso}} | {{rf_n1}} | - |
| Quote-part de résultat des ME | {{qp_me}} | {{qp_me_n1}} | - |
| Résultat net part du groupe | {{rn_groupe}} | {{rn_groupe_n1}} | {{rn_evo}}% |
| Résultat net part minoritaires | {{rn_min}} | {{rn_min_n1}} | - |

#### Bilan consolidé

| Poste | Fin T{{qq}} | Fin N-1 | Delta |
|-------|-------------|---------|-------|
| Goodwill | {{goodwill}} | {{goodwill_n1}} | - |
| Actif immobilisé incorporel | {{immo_inc}} | {{immo_inc_n1}} | - |
| Actif immobilisé corporel | {{immo_corp}} | {{immo_corp_n1}} | - |
| Actif immobilisé financier | {{immo_fi}} | {{immo_fi_n1}} | - |
| BFR consolidé | {{bfr_conso}} | {{bfr_n1}} | {{bfr_delta}} |
| Trésorerie consolidée | {{treso_conso}} | {{treso_n1}} | - |
| Capitaux propres part du groupe | {{cp_groupe}} | {{cp_groupe_n1}} | - |
| Intérêts minoritaires | {{min}} | {{min_n1}} | - |
| Dettes financières | {{df_conso}} | {{df_n1}} | - |

### Retraitements de consolidation

| Retraitement | Montant | Référence normative |
|--------------|---------|---------------------|
| Location simple en droits d'utilisation | {{retrait_1}} | IFRS 16 |
| Goodwill et test d'impairment annuel | {{retrait_2}} | IAS 36 |
| Juste valeur des instruments financiers | {{retrait_3}} | IFRS 9 |
| Provisions retraitées selon actuariat | {{retrait_4}} | IAS 19 |
| Impôts différés | {{retrait_5}} | IAS 12 |

### Éliminations intra-groupe

- CA intra-groupe éliminé : {{elim_ca}} k EUR
- Achats intra-groupe éliminés : {{elim_ach}} k EUR
- Créances / Dettes intercos éliminées : {{elim_ccc}} k EUR
- Marge sur stocks intra-groupe éliminée : {{elim_stock}} k EUR
- Dividendes intra-groupe éliminés : {{elim_div}} k EUR

## Risques

- {{risque_1_niveau}} Divergence de méthodes entre filiales : harmonisation post-consolidation source d'erreur
- {{risque_2_niveau}} Test d'impairment du goodwill à déclencher annuellement : si budget dégradé, risque de dépréciation significative
- {{risque_3_niveau}} Traitement IFRS 16 (leases) : revoir le périmètre des contrats de location à la date de clôture

## Actions

- [ ] Valider les balances des filiales avec les contrôleurs de gestion locaux
- [ ] Procéder aux retraitements d'homogénéisation IFRS
- [ ] Réaliser les éliminations intra-groupe (voir routine intercos-eliminations)
- [ ] Effectuer le test d'impairment du goodwill si clôture annuelle ou indice objectif
- [ ] Produire les notes annexes obligatoires IFRS (sous 40 notes minimum)
- [ ] Transmettre les comptes consolidés au CAC consolidé pour certification
- [ ] Déposer les comptes consolidés au greffe avec les comptes sociaux

## Limites

La consolidation IFRS est un exercice technique réservé aux professionnels formés (CFO, responsable consolidation). Les retraitements multinormatifs nécessitent une maîtrise fine des 40+ normes IFRS et leurs interprétations (IFRIC). Cette routine automatise la coordination et le pilotage, mais les arrêtés techniques doivent être validés par un consolideur (interne, EC, ou CAC consolidé). Pour primo-consolidation ou acquisition significative impactant le périmètre, recourir à un consultant spécialisé en consolidation. Les données chiffrées ci-dessus sont indicatives et doivent être certifiées par le CAC avant toute communication externe.
