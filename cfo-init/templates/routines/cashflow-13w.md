# Prévision trésorerie 13 semaines, W{{ww}}/{{yyyy}}, {{denomination}}

**SIREN** : {{siren}}
**Semaine de production** : W{{ww}} {{yyyy}}
**Généré le** : {{date_today}}
**Horizon** : 13 semaines glissantes à partir du {{date_debut_horizon}}

## Pourquoi

Actualisation hebdomadaire de la trésorerie projetée sur 13 semaines. Décision en jeu : besoin d'activer une ligne de crédit court terme, affacturage ou levée de fonds si le solde projeté descend sous le seuil de sécurité de {{seuil_securite}} k EUR.

## Chiffres clés

| KPI | Valeur actuelle | vs semaine précédente | Signal |
|-----|-----------------|-----------------------|--------|
| Cash actuel (banques + caisse) | {{cash_actuel}} k EUR | {{cash_delta}} | {{signal_cash}} |
| Solde projeté mini (13 sem) | {{solde_mini}} k EUR | {{solde_mini_delta}} | {{signal_mini}} |
| Semaine du solde mini | W{{semaine_mini}} | - | - |
| Encaissements projetés 13 sem | {{encaiss_total}} k EUR | {{encaiss_delta}} | - |
| Décaissements projetés 13 sem | {{decaiss_total}} k EUR | {{decaiss_delta}} | - |
| Cash burn hebdo moyen | {{burn_hebdo}} k EUR | {{burn_delta}} | {{signal_burn}} |

## Vue 13 semaines

| Semaine | Solde début | Encaissements | Décaissements | Solde fin |
|---------|-------------|---------------|---------------|-----------|
| W{{w1}} | {{solde_w1_deb}} | {{enc_w1}} | {{dec_w1}} | {{solde_w1_fin}} |
| W{{w2}} | {{solde_w2_deb}} | {{enc_w2}} | {{dec_w2}} | {{solde_w2_fin}} |
| W{{w3}} | {{solde_w3_deb}} | {{enc_w3}} | {{dec_w3}} | {{solde_w3_fin}} |
| W{{w4}} | {{solde_w4_deb}} | {{enc_w4}} | {{dec_w4}} | {{solde_w4_fin}} |
| W{{w5}} | {{solde_w5_deb}} | {{enc_w5}} | {{dec_w5}} | {{solde_w5_fin}} |
| W{{w6}} | {{solde_w6_deb}} | {{enc_w6}} | {{dec_w6}} | {{solde_w6_fin}} |
| W{{w7}} | {{solde_w7_deb}} | {{enc_w7}} | {{dec_w7}} | {{solde_w7_fin}} |
| W{{w8}} | {{solde_w8_deb}} | {{enc_w8}} | {{dec_w8}} | {{solde_w8_fin}} |
| W{{w9}} | {{solde_w9_deb}} | {{enc_w9}} | {{dec_w9}} | {{solde_w9_fin}} |
| W{{w10}} | {{solde_w10_deb}} | {{enc_w10}} | {{dec_w10}} | {{solde_w10_fin}} |
| W{{w11}} | {{solde_w11_deb}} | {{enc_w11}} | {{dec_w11}} | {{solde_w11_fin}} |
| W{{w12}} | {{solde_w12_deb}} | {{enc_w12}} | {{dec_w12}} | {{solde_w12_fin}} |
| W{{w13}} | {{solde_w13_deb}} | {{enc_w13}} | {{dec_w13}} | {{solde_w13_fin}} |

## Détail des flux récurrents

### Encaissements

- Clients récurrents (abonnements, contrats cadres) : {{enc_recurrent}} k EUR / semaine
- Clients ponctuels attendus (pipeline) : {{enc_ponctuel}} k EUR sur 13 semaines, couverture {{couverture_pipe}}%
- Subventions et aides attendues : {{enc_subvention}} k EUR
- Remboursements fiscaux ou sociaux : {{enc_rembst}} k EUR

### Décaissements

- Masse salariale mensuelle (paie + charges) : {{dec_paie}} k EUR / mois, échéance autour du {{echeance_paie}}
- Loyers et charges fixes : {{dec_loyer}} k EUR / mois
- Fournisseurs récurrents : {{dec_four_recur}} k EUR / semaine
- Échéances fournisseurs à 30/60/90 j : {{dec_four_ponc}} k EUR total
- Échéances fiscales (TVA, IS acompte) : {{dec_fiscal}} k EUR
- Échéances bancaires (intérêts, capital) : {{dec_bancaire}} k EUR / mois
- Investissements CAPEX planifiés : {{dec_capex}} k EUR

## Options si tension trésorerie

**A. Activation ligne crédit existante (recommandée si ligne dispo)**
Cash mobilisable : {{ligne_dispo}} k EUR. Coût : {{cout_ligne}}% annuel sur montant tiré. Délai : 2 jours ouvrés.

**B. Affacturage ponctuel**
Cash mobilisable : {{affacturage_cash}} k EUR (70 à 90% créances éligibles). Coût : {{cout_affact}}% sur 30 jours. Délai : 10 jours.

**C. Report d'échéance fiscale**
Cash économisé : {{report_fiscal_cash}} k EUR. Coût : intérêts de retard 0,20% par mois. Procédure DGFiP, délai 15 jours.

## Recommandation

Si solde mini projeté inférieur à {{seuil_securite}} k EUR, activer l'option A en priorité pour couvrir l'échéance {{echeance_critique}}. Deux raisons : (1) la ligne est déjà négociée, donc pas de délai d'instruction ; (2) le coût financier est marginal sur une durée courte. Caveat : surveiller la reconstitution du cash dès W+4 pour éviter de laisser la ligne tirée trop longtemps.

## Next

Valider l'activation de la ligne (si applicable) avec le banquier. Porteur : CFO. Échéance : avant W{{semaine_mini}} soit le {{date_action}}.

## Limites

Cette prévision repose sur les données connues au {{date_today}}. Les encaissements futurs dépendent du taux de recouvrement réel (DSO), les décaissements planifiés peuvent varier selon les arbitrages OPEX en cours. Pour négociation d'un financement externe, consulter votre banquier ou courtier. Si solde mini projeté négatif sur plus de 2 semaines, faire une revue complète avec l'EC et envisager un plan de continuité.
