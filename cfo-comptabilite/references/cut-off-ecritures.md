# Cut-off et écritures de rattachement

Principe comptable : **le résultat d'un exercice doit rattacher toutes les charges et tous les produits qui s'y rapportent**, même si la facture est émise avant ou après.

## Les 4 types d'écritures de rattachement

### FAR — Factures à Recevoir

**Définition** : le fournisseur a livré la marchandise ou effectué la prestation **avant** la clôture, mais la facture **n'est pas encore reçue** au jour de la clôture.

**Écriture à la clôture** (31/12/N) :
```
601 Achats de marchandises        100,00
44586 TVA sur factures non parvenues  20,00
    408 Fournisseurs - Factures non parvenues  120,00
```

**Écriture de contre-passation** au 01/01/N+1 :
```
408 Fournisseurs - Factures non parvenues  120,00
    601 Achats de marchandises        100,00
    44586 TVA sur factures non parvenues  20,00
```

### FNP — Factures Non Parvenues

Quasi-synonyme de FAR (certains distinguent : FAR pour marchandises, FNP pour services). En pratique, on utilise le **compte 408** pour les deux.

### PCA — Produits Constatés d'Avance

**Définition** : un produit a été facturé et encaissé **avant** la clôture, mais il concerne une prestation qui sera fournie **après**.

**Exemple** : abonnement SaaS annuel facturé le 01/07/N pour la période 01/07/N → 30/06/N+1. Au 31/12/N, 6 mois seulement sont acquis, 6 mois sont constatés d'avance.

**Écriture à la clôture** :
```
706 Prestations de services           500,00  (6 mois sur 12 à reporter)
    487 Produits constatés d'avance   500,00
```

**Contre-passation au 01/01/N+1** :
```
487 Produits constatés d'avance       500,00
    706 Prestations de services       500,00
```

### CCA — Charges Constatées d'Avance

**Définition** : une charge a été facturée et payée **avant** la clôture, mais elle concerne une période **après**.

**Exemple** : assurance annuelle payée le 01/10/N pour 12 mois. Au 31/12/N, 9 mois sont à reporter en charge de l'exercice suivant.

**Écriture à la clôture** :
```
486 Charges constatées d'avance       900,00
    616 Primes d'assurance             900,00
```

## Matrice de décision rapide

| Situation | Écriture |
|-----------|----------|
| Marchandise livrée, facture pas encore reçue | **FAR / FNP** (débit charge, crédit 408) |
| Prestation reçue (service), facture pas encore reçue | **FNP** (idem) |
| Facture client émise, prestation à fournir après clôture | **PCA** (débit 706, crédit 487) |
| Charge payée pour période future | **CCA** (débit 486, crédit charge) |
| Créance certaine sans facture à émettre (ex. intérêts courus) | **Produits à recevoir** (débit 418, crédit produit) |
| Charge certaine sans facture reçue encore (ex. primes) | **FNP** ou provision spécifique |

## Contrôles qualité

### Checklist cut-off au 31/12

- [ ] **Livraisons reçues sur décembre** sans facture dans le grand livre → FAR
- [ ] **Bons de commande signés** avec livraison avant clôture → vérifier statut facturation
- [ ] **Primes / bonus** connus pour l'exercice N à verser en N+1 → provision
- [ ] **Congés payés** non pris au 31/12 → provision CP (solde × coût moyen × 1,45 pour charges)
- [ ] **Abonnements annuels** (SaaS, assurance, loyers) payés d'avance → CCA au prorata
- [ ] **Contrats clients pluriannuels** → PCA sur la part non acquise
- [ ] **Intérêts courus** sur emprunts → 1688 Intérêts courus sur emprunts
- [ ] **Commissions de CA** à verser au 15/01 pour CA du S2 → FNP

### Signes d'un cut-off raté

- Résultat N+1 qui chute brutalement en janvier (= vous avez pris trop de produits en N)
- Marge brute N+1 en hausse inexpliquée sur janvier (= vous avez oublié des FAR en N)
- Écart CA CA3 TVA décembre vs compte 706 (signe de PCA mal traités)

## Automatisation partielle

### Règles automatisables

Le script `scripts/generate_closing_journal.py` peut générer **automatiquement** les écritures suivantes :

- **Amortissements mensuels** : 1/12 de l'amortissement annuel pour chaque immo
- **CCA des abonnements récurrents** : connaissant la date d'engagement et la durée
- **PCA des contrats SaaS** : connaissant la période de facturation

### Règles non automatisables (input utilisateur requis)

- **FAR** (liste des fournisseurs ayant livré sans facturer) — nécessite revue
- **Provisions pour litiges** — jugement du CFO / avocat
- **Dépréciation clients douteux** — jugement
- **Valorisation stocks obsolètes** — inventaire physique

## Fiscalité

### Déductibilité

- **FAR / FNP** : intégralement déductibles si la prestation / livraison est bien antérieure à la clôture
- **PCA** : reportent le produit imposable à N+1
- **CCA** : reportent la charge déductible à N+1
- **Provisions** : déductibles uniquement si **individualisées**, **probables**, et **non encore certaines** — sinon réintégration fiscale

### Documentation à conserver

Pour chaque écriture d'inventaire :
- Justificatif (bon de livraison, contrat SaaS, échéancier assurance)
- Calcul détaillé (prorata temporis)
- Validation par l'EC (signature dossier ou email)

## Mode EC

Les écritures de cut-off sont **le cœur de la mission de présentation**. Checklist NEP 200 et référentiel OEC détaillé dans `paperasse/comptable > references/closing.md` et `paperasse/comptable > references/cloture-workflow.md`.

## Mode PME

Si vous n'avez pas d'EC : les FAR/FNP et PCA/CCA sont la zone de risque n°1 (le contrôle fiscal adore). **Recommandation forte** : faire valider ces écritures par un EC avant finalisation de la clôture annuelle.
