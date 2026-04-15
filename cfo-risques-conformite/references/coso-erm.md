# COSO ERM 2017 — Enterprise Risk Management

Framework de référence international pour la gestion des risques d'entreprise. Mis à jour en 2017 (vs 2004).

## 5 composantes

### 1. Governance & Culture (Gouvernance et culture)

- **Gouvernance** : structure du board, comité d'audit, responsabilités
- **Culture** : "tone at the top", valeurs, intégrité
- **Talents** : compétences risque dans l'organisation

### 2. Strategy & Objective Setting (Stratégie et objectifs)

- **Alignement stratégie/risque** : la stratégie doit intégrer le risque
- **Risk appetite** : niveau de risque acceptable, validé par le board
- **Objectifs business** : risques identifiés pour chaque objectif

### 3. Performance (Performance)

- **Identification** : techniques (brainstorming, interviews, ateliers, scénarios)
- **Évaluation** : matrice 5×5 (probabilité × impact)
- **Priorisation** : top 10 risques majeurs
- **Réponse** : éviter / réduire / partager (assurance) / accepter

### 4. Review & Revision (Revue et révision)

- Surveillance continue
- Revue annuelle au minimum
- Adaptation aux changements (réglementaires, marché, organisation)

### 5. Information, Communication & Reporting

- Flux d'information ascendants (terrain → board)
- Communication transverse
- Reporting au CODIR + comité d'audit (si applicable)

## Matrice 5×5 — exemple

```
Impact
  5 |          |          | 🟠 Risque 7 | 🔴 Risque 1 | 🔴 Risque 4 |
  4 |          | 🟠 R5    | 🟠 R3      | 🔴 R2       |              |
  3 |          | 🟡 R8    | 🟡 R6      | 🟠 R9       |              |
  2 | 🟢 R10   |          |            |              |              |
  1 |          |          |            |              |              |
    +----------+----------+------------+--------------+--------------+
       1 (très    2          3            4 (probable)   5 (certain)
       improbable)                                       Probabilité
```

Légende :
- 🔴 Critique (impact 4-5 + proba 4-5) : action immédiate
- 🟠 Élevé (impact 3-4 + proba 3-4) : plan d'action 30-90 jours
- 🟡 Moyen (impact 2-3 + proba 2-3) : surveillance
- 🟢 Faible (impact 1-2 + proba 1-2) : tolérance

## Catégories de risques (taxonomie standard)

### Stratégique
- Concurrence / disruption
- Modèle business obsolète
- Échec stratégique d'acquisition / lancement produit
- Dépendance client (top 1 = X% du CA)

### Opérationnel
- Rupture chaîne d'approvisionnement
- Panne SI / cyber
- Sinistre (incendie, inondation)
- Erreurs humaines

### Financier
- Tension trésorerie
- Risque de change / taux
- Défaut d'un client clé (impayé majeur)
- Évolution coût matières premières

### Compliance / réglementaire
- Évolution réglementaire (CSRD, taxation, social)
- Contrôle fiscal
- Litige client / fournisseur
- Non-conformité RGPD

### Réputationnel
- Crise médiatique
- Réseaux sociaux
- Insatisfaction client virale
- Comportement non éthique exposé

### Cyber / IT
- Ransomware
- Vol de données
- Indisponibilité critique
- Phishing employés

### ESG / climat
- Risque physique climat (sinistre)
- Risque transition (réglementations carbone)
- Risques sociaux (turnover, conflits)
- Litiges environnementaux

### Géopolitique
- Sanctions internationales
- Volatilité marchés
- Conflits armés impactant chaîne logistique
- Cybernormes nationales divergentes

## Workflow de cartographie

### Étape 1 — Brainstorming par fonction

Pour chaque fonction (Commercial, Production, IT, Finance, RH...), identifier les top 5 risques.

### Étape 2 — Consolidation

Tableau commun (souvent 30-60 risques bruts).

### Étape 3 — Évaluation

Pour chaque risque, scorer 1-5 sur :
- **Probabilité** : combien de chances que ça arrive dans les 12 mois ?
- **Impact** : si ça arrive, combien ça coûte (€ + réputation + opérationnel) ?

### Étape 4 — Priorisation

Garder les **top 10-15 risques majeurs** (impact 3+ et proba 3+).

### Étape 5 — Réponse

Pour chaque risque majeur :
- **Stratégie** : éviter / réduire / partager / accepter
- **Actions** : mesures concrètes
- **Owner** : responsable de l'action
- **Deadline** : date cible
- **KRI** (Key Risk Indicator) : métrique de suivi

### Étape 6 — Reporting

- Dashboard mensuel : état des KRI
- Comité d'audit trimestriel : revue cartographie + actions
- Board annuel : top risques + tendance

## Script `risk_mapping_generator.py`

Génère une matrice de risques à partir d'un questionnaire standard (CSV avec ID risque, libellé, fonction, proba, impact). Output : HTML coloré + plan d'action + KRI proposés.

## Bonnes pratiques

- **Faire participer les opérationnels** (pas que le CFO seul)
- **Mise à jour annuelle minimum** (l'environnement change)
- **Ne pas surcharger** : 10-15 risques majeurs suffisent
- **KRI quantifiables** : pas "bonne ambiance" mais "turnover < 10%/an"
- **Stress test** : "que se passe-t-il si les 3 plus grands risques se réalisent simultanément ?"
