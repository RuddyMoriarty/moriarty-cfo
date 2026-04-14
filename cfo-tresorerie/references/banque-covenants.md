# Relations bancaires et covenants

Gestion des facilités de crédit, négociation, et monitoring des covenants contractuels.

## Facilités de crédit typiques PME

| Type | Horizon | Usage | Garantie |
|------|---------|-------|----------|
| Découvert autorisé | Permanent | Pic de besoin CT (20-30 jours) | Souvent caution dirigeant |
| Ligne de crédit court terme (< 1 an) | 1 an renouvelable | Variations saisonnières BFR | Caution / nantissement |
| Dailly / cession de créances | Permanent | Mobilisation créances | Créances clients nanties |
| Affacturage (factoring) | Permanent | Transfert créances + financement | Créances cédées |
| Prêt moyen terme (MLT) | 3-7 ans | CAPEX, croissance | Hypothèque, nantissement |
| PGE (Prêt Garanti État) | Jusqu'à 6 ans | Trésorerie covid / crise | Garantie BPI / État |
| Crédit-bail (leasing) | 5-7 ans | Équipements industriels | L'actif lui-même |
| Prêt d'honneur | 5 ans | Création / développement | Sans garantie |

## Covenants financiers typiques

Les **covenants** sont des engagements financiers qui, s'ils sont breachés, peuvent déclencher le remboursement anticipé du prêt ou une renégociation.

### DSCR — Debt Service Coverage Ratio

```
DSCR = EBITDA / (Intérêts + Remboursement principal annuel)
```

**Covenant typique** : DSCR ≥ 1.2 à 1.5

Si DSCR < 1, la société n'arrive pas à rembourser son service de la dette sur son résultat opérationnel.

### Leverage ratio (gearing)

```
Leverage = Dette nette / EBITDA
Dette nette = Dette financière totale - Trésorerie
```

**Covenant typique** :
- PME saine : < 3 × EBITDA
- Scale-up : < 4 × EBITDA
- LBO : < 6 × EBITDA (spécificité)

### Interest coverage

```
ICR = EBITDA / Intérêts financiers nets
```

**Covenant typique** : ICR ≥ 3 à 5

### Gearing (dettes / fonds propres)

```
Gearing = Dette financière / Capitaux propres
```

**Covenant typique** : < 1.5

### Working capital / liquidity

Moins fréquent chez les PME, plus commun pour les grandes entreprises cotées.

## Monitoring mensuel des covenants

### Template simple

```
Covenant: Leverage (Dette nette / EBITDA)
Cible contractuelle: < 3.0
Valeur au {date_reporting}: 2.4 ✓ OK (headroom 20%)

Trend sur 12 mois:
M-12 → 2.8 ⚠️
M-9  → 2.6
M-6  → 2.5
M-3  → 2.4
M    → 2.4
```

Alerter **avant que le covenant soit breaché** — prévenir le banquier en transparence est toujours mieux que d'être pris en défaut.

### Script de monitoring

À ajouter en v0.2 : `scripts/check_covenants.py` qui lit `private/company.json > covenants` et les calcule mensuellement depuis la balance.

## Négociation annuelle

Une fois par an, revoir la relation bancaire :

1. **Préparation du dossier** (1 mois avant RDV) :
   - Liasse fiscale N-1
   - Forecast 12 mois glissant
   - Business plan 3-5 ans
   - Tableau emprunts + DSCR actuels
   - Faits marquants de l'année (positifs + risques gérés)

2. **Brief CEO / fondateur / dirigeant** :
   - Montant demandé
   - Durée
   - Garanties acceptables
   - Alternatives (2+ banques en parallèle)

3. **RDV banquier** :
   - Présentation chiffrée 20 min
   - Q&A 20 min
   - Next steps

4. **Suivi** :
   - Offre dans 2-4 semaines
   - Comparer minimum 2 offres
   - Négocier conditions (taux, commissions, garanties, covenants)

## Ratios de pilotage à monter au CEO

Dashboard mensuel bancaire :

| Métrique | Valeur | Trend | Seuil |
|----------|--------|-------|-------|
| Trésorerie nette | 450 k€ | ↗ | > 1 mois charges |
| DSCR | 2.1 | → | > 1.2 |
| Leverage | 2.4 | ↗ | < 3.0 |
| Gearing | 0.8 | → | < 1.5 |
| Jours de runway | 42 | ↗ | > 30 |

## Scénarios d'urgence

### Si covenant bientôt breaché (< 10% headroom)

1. **Contacter le banquier** en amont (pas de mauvaise surprise)
2. Préparer une **waiver letter** (demande d'exception temporaire)
3. Proposer un plan d'action sur 6 mois (levier identifié pour revenir dans le covenant)
4. Négocier **amendment** si nécessaire (modification définitive du covenant)

### Si covenant breaché

- Le prêt peut être **déclaré exigible** immédiatement
- La banque peut activer les **garanties** (nantissement, hypothèque)
- Possibilité de **cross-default** avec d'autres emprunts de la société
- **Procédure collective** (sauvegarde / redressement) à considérer si plusieurs breachs

## Diversification bancaire

Éviter la **dépendance** à une seule banque :
- Idéalement 2-3 banques partenaires
- Répartition des lignes de crédit
- Différents types de financements (CT vs MLT) chez banques différentes
- Relation d'affaires > 5 ans (loyauté paie lors des difficultés)

## Adaptation par audience

**Mode EC** : souvent vous accompagnez le client vers la banque. Préparer le dossier, faire le pitch avec lui, ne pas signer à sa place.

**Mode PME** : **relation stratégique**. Ne pas négliger les RDV annuels, même en période de bonne santé. Anticiper les besoins de financement 6-12 mois à l'avance.

## Orchestration

- KPIs covenants remontés à `cfo-reporting` (dashboard CFO)
- Si tension détectée → `cfo-financement-croissance` (négociation nouvelles lignes)
- Balance depuis `cfo-comptabilite`

## Outils dédiés

Beaucoup de PME gèrent leurs covenants sur Excel. Pour les ETI+ :
- **Cash forecasting tools** : Agicap, Kyriba, Finaxys
- **Banking portals** : accès centralisé aux comptes pros (ex. BBVA, Boursorama Pro)
- **MCP Qonto** : déjà installé chez l'utilisateur
