# Liasse fiscale et FEC

## FEC — Fichier des Écritures Comptables

### Obligation légale

Depuis 2014, toutes les sociétés qui tiennent une comptabilité informatisée doivent pouvoir produire un FEC sur demande de la DGFiP (art. L. 47 A du LPF).

- **Délai de mise à disposition** : 15 jours après demande
- **Pénalité en cas de non-conformité** : 5 000 € (art. 1729 D CGI), rejet de la comptabilité possible

### Format (arrêté du 29 juillet 2013)

- **Fichier texte** encodé en ASCII ou UTF-8
- **Séparateur** : tabulation ou pipe `|`
- **Nommage** : `<SIREN>FEC<AAAAMMJJ>.txt` (ex. `552120222FEC20261231.txt`)
- **18 colonnes obligatoires** dans cet ordre exact :

| # | Colonne | Description |
|---|---------|-------------|
| 1 | JournalCode | Code du journal (ex. `VT`, `AC`, `BQ`) |
| 2 | JournalLib | Libellé du journal |
| 3 | EcritureNum | Numéro séquentiel de l'écriture |
| 4 | EcritureDate | Date de comptabilisation (AAAAMMJJ) |
| 5 | CompteNum | Numéro de compte PCG |
| 6 | CompteLib | Libellé du compte |
| 7 | CompAuxNum | Numéro auxiliaire (si tiers) |
| 8 | CompAuxLib | Libellé auxiliaire |
| 9 | PieceRef | Référence de la pièce justificative |
| 10 | PieceDate | Date de la pièce (AAAAMMJJ) |
| 11 | EcritureLib | Libellé de l'écriture |
| 12 | Debit | Montant au débit |
| 13 | Credit | Montant au crédit |
| 14 | EcritureLet | Code de lettrage |
| 15 | DateLet | Date de lettrage |
| 16 | ValidDate | Date de validation |
| 17 | Montantdevise | Montant en devise étrangère |
| 18 | Idevise | Code ISO de la devise |

### Script `scripts/prepare_fec_export.py`

Le script prend en entrée un export JSON/CSV du grand livre et produit un FEC conforme DGFiP.

```bash
python3 scripts/prepare_fec_export.py \
  --grand-livre input/grand-livre-2026.csv \
  --siren 552120222 \
  --exercice 2026 \
  --output out/552120222FEC20261231.txt
```

Vérifications automatiques du script :
- Équilibre débit/crédit (tolérance 0,01 €)
- Séquence continue de `EcritureNum`
- Dates valides (AAAAMMJJ)
- Encodage UTF-8 sans BOM

### Conservation

Le FEC doit être conservé **6 ans** (art. L. 102 B du LPF).

## Liasse fiscale

### Quel formulaire ?

| Régime | Formulaire principal | Annexes principales |
|--------|----------------------|---------------------|
| Micro-BIC / micro-BNC | Pas de liasse — uniquement CA dans déclaration IR | — |
| Réel simplifié IS | **2033-SD** | 2033-A à 2033-G |
| Réel simplifié IR (BIC) | 2031-SD | 2033-A à 2033-G |
| Réel normal IS | **2065-SD** | 2050 à 2059 |
| Réel normal IR (BIC) | 2031-SD | 2050 à 2059 |
| BNC déclaration contrôlée | 2035-SD | 2035-A, 2035-B |

### Principales cases de la liasse 2050-2058 (réel normal IS)

**Bilan actif (2050)** :
- Immobilisations incorporelles, corporelles, financières (brut, amortissements, net)
- Actif circulant (stocks, créances, VMP, disponibilités)

**Bilan passif (2051)** :
- Capitaux propres (capital, réserves, RAN, résultat)
- Provisions
- Dettes (financières, fournisseurs, fiscales, sociales)

**Compte de résultat (2052-2053)** :
- Produits d'exploitation (CA HT, production stockée, subventions)
- Charges d'exploitation (achats, services, salaires, charges sociales, amortissements)
- Produits et charges financiers
- Produits et charges exceptionnels
- Impôt sur les bénéfices
- Résultat de l'exercice

**Immobilisations (2054-2055)** :
- Tableau des immobilisations (entrées, sorties, reclassements)
- Tableau des amortissements

**Provisions (2056)** :
- Pour risques et charges
- Pour dépréciation
- Pour impôts

**Créances et dettes (2057)** :
- Échéances des créances et dettes à moins / plus d'un an

**Détermination du résultat fiscal (2058-A, -B, -C)** :
- Résultat comptable → Résultat fiscal
- Réintégrations extra-comptables (amendes, pénalités, IS lui-même)
- Déductions (produits exonérés, quote-part de frais et charges)
- Calcul IS théorique
- Imputation acomptes + crédits d'impôt (CIR, CII)
- Solde à payer ou crédit

### Production du brouillon

Template : `templates/liasse-2065-brouillon.md` (à créer en v0.2, pour l'instant renvoyer à `paperasse/controleur-fiscal > templates/liasse-fiscale-2033.md`).

Le brouillon liasse **n'est pas la liasse définitive** : il sert de support à l'EC pour remplir le formulaire officiel sur le site impots.gouv.fr (TDFC — Transfert des Données Fiscales et Comptables).

### Télétransmission TDFC

Obligatoire depuis 2015 pour toutes les entreprises à l'IS. Filière :
- **EDI-TDFC** : via partenaire agréé (expert-comptable, éditeur logiciel)
- **EFI** (Échanges de Formulaires Informatisés) : via l'espace pro de impots.gouv.fr

Le CFO n'envoie pas lui-même → l'EC le fait via le logiciel comptable.

## Règles de cohérence liasse ↔ FEC

La liasse fiscale doit être **parfaitement cohérente** avec le FEC :
- Total des comptes 7 de la liasse = total des produits du FEC
- Total des comptes 6 de la liasse = total des charges du FEC
- Résultat du FEC = résultat de la liasse (à l'euro près)

En cas de contrôle fiscal, toute discordance peut motiver un rejet de la comptabilité.

## Script de validation croisée

```bash
# Vérifie cohérence liasse + FEC + balance
python3 scripts/validate_close_checklist.py \
  --balance out/cloture-annuelle-2026/balance-definitive.csv \
  --fec out/cloture-annuelle-2026/FEC-552120222-2026.txt \
  --liasse-brouillon out/cloture-annuelle-2026/liasse-2065-brouillon.md
```

Sorties :
- Liste des incohérences détectées
- Suggestions d'écritures de régularisation

## Adaptation par audience

**Mode EC** : vous êtes le producteur de la liasse. Ce skill génère le brouillon, vous validez et transmettez via TDFC.

**Mode PME** : vous préparez les éléments à fournir à votre EC. Le brouillon généré ici est un **support** qui vous aide à vérifier ce que l'EC propose. Ne jamais télétransmettre vous-même sans validation EC.

## Renvoi à d'autres skills

- `cfo-fiscalite` : pour l'optimisation fiscale (CIR, CII, report en arrière, plus-values)
- `paperasse/controleur-fiscal` (externe) : pour le détail des cases liasse + barème pénalités + textes fiscaux de référence
