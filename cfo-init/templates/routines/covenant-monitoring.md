# Suivi des covenants bancaires T{{qq}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : T{{qq}} {{yyyy}}
**Généré le** : {{date_today}}

## Pourquoi

Monitoring trimestriel des covenants bancaires avant arrêté de clôture. Décision en jeu : validation de la conformité aux engagements pris auprès des banques. En cas de breach imminent (inférieur à 0.5 pt de marge), décision d'engager une discussion waiver avant l'échéance formelle de test.

## Chiffres clés

| Covenant | Formule | Seuil contractuel | Valeur T{{qq}} | Marge | Statut |
|----------|---------|-------------------|----------------|-------|--------|
| DSCR (Debt Service Coverage Ratio) | Flux opérationnel / Service de la dette | sup à {{dscr_seuil}} | {{dscr_valeur}} | {{dscr_marge}} | {{dscr_statut}} |
| Leverage | Dette nette / EBITDA | inf à {{lev_seuil}} | {{lev_valeur}} | {{lev_marge}} | {{lev_statut}} |
| ICR (Interest Coverage Ratio) | EBITDA / Intérêts financiers | sup à {{icr_seuil}} | {{icr_valeur}} | {{icr_marge}} | {{icr_statut}} |
| Gearing | Dette nette / Capitaux propres | inf à {{gear_seuil}} | {{gear_valeur}} | {{gear_marge}} | {{gear_statut}} |

Statuts possibles : conforme (vert), veille (jaune, marge inférieure à 10%), alerte (orange, marge inférieure à 5%), breach (rouge, covenant non respecté).

## Détail des calculs

### DSCR

- EBITDA trimestriel annualisé : {{ebitda_annualise}} k EUR
- Service de la dette annualisé (intérêts + capital) : {{service_dette}} k EUR
- DSCR calculé : {{ebitda_annualise}} / {{service_dette}} = {{dscr_valeur}}

### Leverage (Dette nette / EBITDA)

- Dette financière totale : {{dette_totale}} k EUR
- Trésorerie : {{treso_covenant}} k EUR
- Dette nette : {{dette_nette}} k EUR
- EBITDA 12 mois glissants : {{ebitda_12m}} k EUR
- Leverage : {{dette_nette}} / {{ebitda_12m}} = {{lev_valeur}}

### ICR (Interest Coverage Ratio)

- EBITDA 12 mois glissants : {{ebitda_12m}} k EUR
- Intérêts financiers 12 mois glissants : {{interets_12m}} k EUR
- ICR : {{ebitda_12m}} / {{interets_12m}} = {{icr_valeur}}

## Trajectoire des covenants (4 derniers trimestres)

| Trimestre | DSCR | Leverage | ICR | Gearing |
|-----------|------|----------|-----|---------|
| T{{qq_prev_3}} | {{dscr_t1}} | {{lev_t1}} | {{icr_t1}} | {{gear_t1}} |
| T{{qq_prev_2}} | {{dscr_t2}} | {{lev_t2}} | {{icr_t2}} | {{gear_t2}} |
| T{{qq_prev_1}} | {{dscr_t3}} | {{lev_t3}} | {{icr_t3}} | {{gear_t3}} |
| T{{qq}} | {{dscr_valeur}} | {{lev_valeur}} | {{icr_valeur}} | {{gear_valeur}} |

Tendance : {{tendance_covenants}}. Si dégradation continue, le covenant franchira le seuil dans {{horizon_breach}} trimestres.

## Projection sur les 2 prochains trimestres

| Covenant | T{{qq_next_1}} projeté | T{{qq_next_2}} projeté | Risque breach |
|----------|------------------------|------------------------|----------------|
| DSCR | {{dscr_proj_1}} | {{dscr_proj_2}} | {{dscr_risque}} |
| Leverage | {{lev_proj_1}} | {{lev_proj_2}} | {{lev_risque}} |
| ICR | {{icr_proj_1}} | {{icr_proj_2}} | {{icr_risque}} |
| Gearing | {{gear_proj_1}} | {{gear_proj_2}} | {{gear_risque}} |

Hypothèses de projection : atterrissage consensus, cash flow attendu, remboursements contractuels.

## Options si breach imminent

**A. Waiver temporaire négocié (recommandée si breach ponctuel)**
Négociation d'un accord temporaire avec la banque pour suspendre le test pendant 1 à 2 trimestres. Frais : de 0.5 à 2% du nominal. Utilisable en cas d'événement exceptionnel (investissement one-shot, pic d'OPEX).

**B. Refinancement de la ligne concernée**
Remplacement de la dette existante par une nouvelle ligne aux covenants plus souples. Coût : {{cout_refinancement}} k EUR de frais + potentiel hausse du taux.

**C. Apport en capital ou quasi-capital**
Augmentation de capital ou obligations convertibles pour améliorer le ratio leverage et gearing. Impact : {{impact_capital}} k EUR nécessaires, dilution ou obligation de paiement d'intérêts.

**D. Plan d'action opérationnel**
Gel OPEX, cession actif non-core, relance clients agressive pour améliorer cash flow et EBITDA. Délai : 6 à 12 mois.

## Recommandation

Si breach prévu sous 2 trimestres avec marge inférieure à 5% : préparer le waiver (option A) en amont pour éviter la situation d'urgence. Raisons : (1) les banques sont plus conciliantes quand l'entreprise anticipe ; (2) un breach déclaré cross-defaults sur l'ensemble des lignes si covenants croisés. Caveat : un waiver n'est jamais gratuit, prévoir frais et reporting renforcé.

## Next

Si statut alerte ou breach détecté, contact du banquier avant le {{date_contact_banque}}. Préparer le dossier de communication : plan d'action, hypothèses de reprise, engagement chiffré. Porteur : CFO. Transmission à la direction et au board si breach confirmé.

## Limites

Les covenants sont définis par contrat (clause documentation) : vérifier chaque trimestre la lettre exacte, certains accords prévoient des ajustements d'EBITDA (add-backs) ou des périodes de grace. Les projections reposent sur l'atterrissage consensus et peuvent s'écarter. Pour toute négociation bancaire sensible (waiver, refinancement), recourir à un conseil financier ou un avocat bancaire spécialisé. Le dépassement d'un covenant peut entraîner l'exigibilité anticipée de la dette : traitement d'urgence absolue en cas de breach avéré.
