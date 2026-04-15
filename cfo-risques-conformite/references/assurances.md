# Gestion des assurances entreprise

## Polices recommandées

### RC Pro (Responsabilité Civile Professionnelle)

**Quand obligatoire** :
- Professions réglementées (EC, avocat, médecin, agent immobilier...)
- Marchés publics
- Certains contrats clients exigent un certificat

**Couverture** :
- Dommages corporels, matériels, immatériels causés à autrui dans le cadre professionnel
- Frais de défense

**Plafond typique** : 500 k€ à 5 M€ selon activité.

### RC Mandataires Sociaux (D&O — Directors & Officers)

**Pour qui** : dirigeants et mandataires sociaux personnellement.

**Couverture** : actions en responsabilité contre le dirigeant (faute de gestion, négligence...).

**Plafond typique** : 1 à 10 M€.

### Multirisque Entreprise

Couvre les **biens** :
- Locaux (incendie, dégât des eaux, vol)
- Matériel
- Stocks
- Pertes d'exploitation consécutives à un sinistre

### Cyber

**Très recommandée** depuis 2020 (boom des ransomwares).

**Couverture** :
- Frais de réponse à incident (forensique, communication)
- Pertes d'exploitation suite à interruption SI
- Cyber-rançon (limite généralement : la payer n'est pas recommandé)
- Responsabilité civile en cas de violation données clients

**Plafond typique** : 250 k€ à 5 M€.

### Crédit / poste clients

Garantit contre l'impayé d'un client. Acteurs : Atradius, Allianz Trade (ex-Coface), Euler Hermes.

Coût : 0,2 - 0,8% du CA assuré. Pertinent si poste clients concentré.

### Transport / marchandises

Pour les sociétés expédiant des marchandises.

### Construction / Tous Risques Chantier

Pour les chantiers > seuils. Garantit le coût de reconstruction en cas de sinistre.

### Garantie décennale

Obligatoire BTP. Garantit pendant 10 ans les défauts de construction.

## Stratégie d'assurance

### 4 étapes

1. **Identifier les risques** (cartographie) → cf. `coso-erm.md`
2. **Évaluer la perte maximale** par risque
3. **Décider** : transférer (assurance), réduire (mitigation interne), accepter, éviter
4. **Souscrire** : comparer au minimum 3 devis chez courtiers indépendants

### Mutualisation des polices

Une police "multirisque PRO" peut couvrir plusieurs risques (multirisque + RC Pro + cyber + D&O) → souvent économique pour les PME.

### Renégociation annuelle

Tous les ans, revoir :
- Montants des plafonds (adaptés à la croissance ?)
- Franchises (impact prime)
- Exclusions (changements ?)
- Sinistres déclarés (peuvent augmenter la prime à terme)

## Tableau de gestion

| Police | Assureur | Date renouvellement | Plafond | Franchise | Prime annuelle |
|--------|----------|---------------------|---------|-----------|----------------|
| Multirisque | Axa | 31/12 | 1 M€ | 1 000 € | 2 500 € |
| RC Pro | Allianz | 30/06 | 2 M€ | 5 000 € | 4 000 € |
| Cyber | Hiscox | 31/12 | 500 k€ | 5 000 € | 3 500 € |
| D&O | AIG | 31/12 | 5 M€ | 10 000 € | 6 000 € |

À tenir à jour dans `private/assurances.json`.

## Bonnes pratiques

- **Courtier indépendant** (vs agent général) : plus d'options, négociation
- **Lire les exclusions** attentivement (la beauté est dans les détails)
- **Déclarer rapidement** tout sinistre (délais contractuels)
- **Conserver les preuves** (photos, factures, témoignages)
- **Audit annuel** par votre courtier (a-t-on les bonnes garanties ?)

## Captives d'assurance (groupes ETI+)

Pour les groupes > 100 M€ CA, créer une captive (assurance interne) peut être économique sur les risques de fréquence.

Réglementation : agrément ACPR + capital minimum + provisions techniques.

## Avertissement

Ce skill aide à **identifier les besoins** et **structurer la stratégie**. La souscription, la négociation et la gestion opérationnelle des polices nécessitent un **courtier ou agent général** compétent.
