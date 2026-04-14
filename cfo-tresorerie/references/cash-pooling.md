# Cash pooling groupes

Activé si `classification.groupe = true`.

## Principe

**Centralisation de la trésorerie** d'un groupe de sociétés pour :
- Optimiser les conditions bancaires (un seul négociateur, volumes cumulés)
- Équilibrer automatiquement les excédents et les besoins entre filiales
- Réduire les frais de découvert
- Améliorer le reporting groupe de trésorerie

## Types de cash pooling

### Nominal / Notional pooling

- Pas de transfert physique de fonds entre comptes
- La banque calcule un **solde net global** pour fixer les intérêts
- Chaque société garde son autonomie juridique
- Pas de convention intragroupe complexe
- **Moins de montage** mais moins efficace

### Physical pooling (ZBA — Zero Balance Account)

- **Transferts automatiques quotidiens** vers un compte central (compte pivot)
- Chaque filiale est **ramenée à zéro** en fin de journée
- Intérêts calculés sur le solde global
- Nécessite une **convention de trésorerie** intragroupe
- **Plus efficace** mais plus complexe

### Physical pooling (avec seuil)

Variante : les filiales gardent un seuil minimal (ex. 10k€) pour leurs besoins quotidiens, seul l'excédent remonte au compte pivot.

## Convention de trésorerie intragroupe

**Obligatoire** pour le cash pooling physical. Éléments à inclure :

1. **Parties** : société pivot + filiales adhérentes
2. **Principes** : centralisation, remontée automatique, avance pivot → filiale si besoin
3. **Taux d'intérêt** : taux de rémunération (quand la filiale place) et taux d'emprunt (quand la filiale reçoit de l'avance)
4. **Plafonds** : limite par filiale pour éviter les dérives
5. **Durée** : renouvelable annuellement
6. **Dénonciation** : clause de sortie

### Taux d'intérêt — respect du prix de transfert

Article 57 CGI : les taux pratiqués doivent être **au prix de pleine concurrence**.

**Benchmark** : taux monétaire de référence (EURIBOR 3M, ESTER) + marge acceptable (spread de 50 à 150 bps selon le risque de la filiale).

**Piège fiscal** : si le taux est **trop avantageux** pour la filiale (avance gratuite), l'administration peut requalifier en subvention déguisée ou abandon de créance. Si le taux est **trop élevé**, transfert indirect de bénéfices.

### Conformité réglementaire

- **Code monétaire et financier art. L. 511-7** : cash pooling intragroupe autorisé sans agrément bancaire
- **Conditions** : lien capitalistique direct ou indirect (majoritaire ou < 50% sur option)
- **Documentation** : conserver la convention + les justificatifs de flux 6 ans (L. 102 B LPF)

## Mise en œuvre pratique

### Étape 1 — Cartographier les besoins

- Liste des filiales adhérentes (périmètre)
- Soldes bancaires actuels par filiale
- Besoins saisonniers par filiale (pic / creux)
- Banques impliquées (multi-banques possible)

### Étape 2 — Choisir la structure

- Notional ou physical ?
- Compte pivot : banque existante ou dédiée ?
- Fréquence des sweeps (quotidien, hebdomadaire)

### Étape 3 — Négocier avec la banque

- Frais de mise en place (souvent 5-15 k€ pour les groupes moyens)
- Frais récurrents (abonnement mensuel)
- Taux d'intérêt sur le solde cumulé

### Étape 4 — Rédiger et signer les conventions

- Convention entre la société pivot et chaque filiale
- Validation juridique (notaire/avocat si international)
- Inscription au registre des conventions réglementées si parties liées

### Étape 5 — Déployer et suivre

- Outil de reporting groupe trésorerie (ex. Kyriba, Agicap pour petits groupes)
- Revue trimestrielle des soldes et des flux
- Audit annuel par le CAC

## Avantages quantifiables

Pour un groupe de 5 filiales avec 2-5 M€ de solde chacune :

| Sans pooling | Avec pooling |
|--------------|--------------|
| 5 négociations bancaires | 1 négociation |
| Agios sur découverts ponctuels (~30k€/an) | Optimisés |
| Placements à 0-0.5% | Placements groupe à 1-2% |
| Reporting manuel filiale par filiale | Reporting automatisé |

**Gain type** : 50-150 k€/an pour un groupe moyen de 10-50 M€ de CA consolidé.

## Limites et risques

- **Complexité juridique** : si groupes internationaux, respecter les règles de chaque pays
- **Coût d'entrée** : 10-50 k€ de setup
- **Risque de requalification fiscale** : toujours respecter le pricing arm's length
- **Risque de dépendance** : si une filiale vit sur le pooling, elle masque ses problèmes propres
- **Cybersécurité** : un compte pivot concentre le risque cybercriminalité (ex. faux ordre de virement)

## Adaptation par audience

**Mode EC** : accompagnement en mission contractuelle d'un groupe. Rédaction de la convention + validation fiscale + mise en œuvre avec la banque.

**Mode PME** (groupes < 3 filiales) : souvent non rentable. Préférer la gestion manuelle des flux intragroupe + facturation de prestations (transfer pricing).

## Orchestration

- `cfo-comptabilite` (sub-module groupes) : éliminations intercos incluent les prêts/emprunts intragroupe
- `cfo-fiscalite` : transfer pricing des taux d'intérêt
- `cfo-reporting` : reporting groupe de trésorerie consolidé
- `cfo-risques-conformite` : risque cyber, risque de concentration

## Outils recommandés

| Taille groupe | Outils |
|---------------|--------|
| < 5 filiales, < 20 M€ CA | Excel / Google Sheets + Qonto MCP + consolidation mensuelle manuelle |
| 5-20 filiales, 20-100 M€ CA | Agicap, Nomentia, Embat |
| 20+ filiales, 100 M€+ CA | Kyriba, Finaxys, Trax |
| Cotées / internationales | Kyriba, Sage XRT, SAP TRM |
