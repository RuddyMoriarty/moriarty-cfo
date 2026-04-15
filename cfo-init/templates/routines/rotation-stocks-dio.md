# Rotation stocks et DIO {{period_label}}, {{denomination}}

**SIREN** : {{siren}}
**Période** : {{mm}}/{{yyyy}}
**Généré le** : {{date_today}}
**Secteur** : {{secteur_category}} (industrie, commerce, négoce)

## Faits

- Société : {{denomination}}, SIREN {{siren}}
- Période analysée : {{mm}}/{{yyyy}}
- Valeur du stock au {{date_today}} : {{stock_valeur}} k EUR
- Nombre de références en portefeuille : {{nb_references}}
- Méthode de valorisation : {{methode_valo}} (CUMP, FIFO, PEPS)

## Hypothèses

- H1 : les inventaires tournants sont à jour au {{date_inventaire}} avec un écart inférieur à 2%
- H2 : les coûts d'achat utilisés intègrent les frais accessoires (transport, douane, packaging)
- H3 : les stocks obsolètes identifiés en inventaire sont provisionnés à leur valeur nette de réalisation

## Analyse

### Indicateurs clés

| KPI | Valeur | Cible {{yyyy}} | Vs N-1 | Signal |
|-----|--------|----------------|--------|--------|
| DIO (Days Inventory Outstanding) | {{dio_jours}} j | {{dio_cible}} j | {{dio_vs_n1}} j | {{signal_dio}} |
| Rotation annuelle | {{rotation_ann}}x | {{rotation_cible}}x | {{rotation_vs_n1}}x | {{signal_rotation}} |
| Valeur stock / CA annuel | {{stock_pct_ca}}% | {{stock_pct_cible}}% | {{stock_pct_vs_n1}} pt | {{signal_stock_pct}} |
| Taux de rupture | {{taux_rupture}}% | inf à 2% | {{rupture_vs_n1}} pt | {{signal_rupture}} |
| Taux d'obsolescence | {{taux_obso}}% | inf à 5% | {{obso_vs_n1}} pt | {{signal_obso}} |
| Coût de possession annuel | {{cout_possession}} k | - | - | - |

### Analyse ABC des références

| Classe | Nb références | Valeur stock | Rotation moyenne | Action |
|--------|----------------|--------------|-------------------|--------|
| A (80% valeur) | {{nb_a}} | {{val_a}} k | {{rot_a}}x | Surveillance hebdo |
| B (15% valeur) | {{nb_b}} | {{val_b}} k | {{rot_b}}x | Revue mensuelle |
| C (5% valeur) | {{nb_c}} | {{val_c}} k | {{rot_c}}x | Revue trimestrielle |

### Références en alerte

| Référence | Catégorie | Valeur stock | Rotation | Alerte |
|-----------|-----------|--------------|----------|--------|
| {{ref_1_nom}} | {{ref_1_cat}} | {{ref_1_valeur}} | {{ref_1_rot}}x | {{ref_1_alerte}} |
| {{ref_2_nom}} | {{ref_2_cat}} | {{ref_2_valeur}} | {{ref_2_rot}}x | {{ref_2_alerte}} |
| {{ref_3_nom}} | {{ref_3_cat}} | {{ref_3_valeur}} | {{ref_3_rot}}x | {{ref_3_alerte}} |
| {{ref_4_nom}} | {{ref_4_cat}} | {{ref_4_valeur}} | {{ref_4_rot}}x | {{ref_4_alerte}} |
| {{ref_5_nom}} | {{ref_5_cat}} | {{ref_5_valeur}} | {{ref_5_rot}}x | {{ref_5_alerte}} |

Types d'alertes : surstock (rotation inférieure à 2x/an), rupture probable (stock sous seuil mini), obsolescence (absence de sortie depuis 6 mois), péremption imminente.

### Vieillissement du stock

| Tranche d'ancienneté | Valeur | % du stock |
|----------------------|--------|------------|
| Moins de 3 mois | {{stock_0_3}} | {{pct_0_3}}% |
| 3 à 6 mois | {{stock_3_6}} | {{pct_3_6}}% |
| 6 à 12 mois | {{stock_6_12}} | {{pct_6_12}}% |
| Plus de 12 mois | {{stock_sup_12}} | {{pct_sup_12}}% |

### Impact sur le BFR

- Stocks : {{stock_valeur}} k EUR
- DIO contribution au BFR : {{dio_bfr}} jours sur {{bfr_total}} jours totaux
- Amélioration possible DIO : {{dio_gain}} jours = {{cash_libere}} k EUR de cash libéré

## Risques

- {{risque_1_niveau}} Surstock sur {{nb_refs_surstock}} références : immobilisation cash de {{cash_surstock}} k EUR, risque obsolescence et coûts de possession
- {{risque_2_niveau}} Rupture sur références classe A : impact direct sur CA, {{nb_refs_rupture}} références concernées
- {{risque_3_niveau}} Provisions pour obsolescence à constituer : {{provision_obso}} k EUR à passer en N+1

## Actions

- [ ] Déclencher une opération de déstockage (remise, vente à un grossiste) sur les références obsolètes identifiées
- [ ] Réviser les seuils mini/maxi des références classe A en rupture
- [ ] Auditer la qualité des prévisions de vente pour les références au DIO dégradé
- [ ] Mettre à jour les paramétrages ERP (point de commande, MOQ, lead time)
- [ ] Passer les provisions pour obsolescence en comptabilité avant clôture
- [ ] Former les équipes achat/supply sur l'arbitrage coût de possession vs coût de rupture

## Limites

L'analyse des stocks dépend de la qualité des inventaires tournants et de la stabilité des codifications produit. Un article mal codifié ou en doublon fausse les analyses. Les DIO sont calculés sur la base du CMV (coût des marchandises vendues) ; pour entreprises mono-produit, ce calcul est fiable ; pour multi-produits, compléter par une analyse par référence. Pour optimisation de la supply chain (MRP, kanban, réassort automatique), recourir à un consultant supply chain ou un logiciel dédié (ERP avec module avancé).
