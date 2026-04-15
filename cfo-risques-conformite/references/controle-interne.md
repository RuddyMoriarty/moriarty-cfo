# Contrôle interne

Dispositif visant à fournir une assurance raisonnable sur la maîtrise des opérations, la fiabilité de l'information financière, et la conformité réglementaire.

## Objectifs (COSO Internal Control)

1. **Efficience opérationnelle** — processus efficaces
2. **Fiabilité du reporting financier** — comptes sincères et complets
3. **Conformité réglementaire** — respect lois et règlements

## 5 composantes

1. **Environment de contrôle** — culture, intégrité, valeurs
2. **Évaluation des risques** — voir `coso-erm.md`
3. **Activités de contrôle** — procédures, séparation des fonctions
4. **Information & communication** — flux d'information
5. **Pilotage** — surveillance continue + revue périodique

## Activités de contrôle clés

### Séparation des fonctions

Aucune personne ne doit pouvoir initier + valider + comptabiliser une opération.

Exemples :
- Achat : commande (responsable opérationnel) ≠ validation facture (CFO) ≠ paiement (trésorerie)
- Paie : préparation paie (RH) ≠ validation montants (DG) ≠ versement (trésorerie)
- Note de frais : engagement (collaborateur) ≠ validation N+1 ≠ remboursement (trésorerie)

### Double signature

- Pour les paiements > seuil (souvent 5 000 € ou 10 000 €)
- Pour les engagements de dépenses > seuil
- Pour les contrats commerciaux > seuil

### Réconciliations périodiques

- Bancaire (mensuelle)
- Inter-comptes
- Stocks vs comptabilité
- Paie vs DSN

### Limitations d'accès

- Comptes bancaires : signataires limités
- ERP : profils utilisateurs ségrégués
- Données sensibles (paie, clients) : accès restreint

### Approbations préalables

- CAPEX > seuil (DG)
- Recrutement (DG / DRH)
- Conventions réglementées (CA / CSE)

## Documentation

Pour chaque processus clé :

### 1. Cartographie processus

Diagramme des étapes (input → étapes → output).

### 2. RACI

Pour chaque étape :
- **R**esponsible : exécute
- **A**ccountable : valide (1 seul)
- **C**onsulted : avis
- **I**nformed : informé

### 3. Narrative

Description prose du processus, références aux applications utilisées, contrôles en place.

### 4. Tests de contrôle

Pour chaque contrôle clé :
- Définition (que vérifie-t-on ?)
- Fréquence (chaque opération / mensuel / trimestriel)
- Documentation (preuve du contrôle réalisé)
- Owner

## Maturité du contrôle interne

| Niveau | Description |
|--------|-------------|
| 1. Ad hoc | Contrôles informels, dépendant des personnes |
| 2. Reproductibles | Procédures écrites mais inégalement appliquées |
| 3. Définis | Procédures formalisées, formation, application uniforme |
| 4. Pilotés | KPI sur les contrôles, revue régulière, amélioration continue |
| 5. Optimisés | Automatisation, IA, intégration ERP/BI |

PME typique : niveau 1-2. ETI mature : niveau 3-4.

## Test des contrôles (annuel)

### Échantillonnage

Pour chaque contrôle clé, prélever un échantillon de 5-25 transactions :
- Vérifier l'application du contrôle
- Documenter le résultat (passe / fail)
- Si fail : remédier + ajuster le processus

### Reporting

Synthèse annuelle :
- Top 10 contrôles testés
- Taux de conformité
- Findings + plan de remédiation

## Findings et remédiation

Niveau de gravité :
- **Critique** : faille permettant une fraude majeure → corriger immédiatement (semaines)
- **Significatif** : faiblesse procédurale → plan d'action 1-3 mois
- **Mineur** : amélioration possible → backlog continue

## Script `internal_control_checklist.py`

Génère une checklist de contrôle interne par fonction (Achats, Ventes, Trésorerie, Paie, Stocks, IT, Compliance) avec contrôles standards et niveaux de maturité.

## Avertissement

Le contrôle interne est un **dispositif évolutif** : il doit être adapté à la taille et la complexité de la société. Pour les ETI+, consulter un consultant en risk management (Big 4 ou cabinet spécialisé).
