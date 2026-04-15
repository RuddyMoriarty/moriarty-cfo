# Diagnostic des besoins de financement

Arbre de décision pour orienter rapidement vers les bonnes solutions.

## Question 1 : quel est l'horizon du besoin ?

### Court terme (< 12 mois)

→ Besoin de **trésorerie** (BFR, saisonnalité, pic d'activité)

**Solutions** :
- Découvert autorisé (souple mais cher)
- Ligne de crédit court terme renouvelable (annuelle)
- Dailly / cession de créances
- Factoring (affacturage)
- Reverse factoring (si grande entreprise)
- Crédit fournisseur (négociation DPO)

### Moyen terme (1-7 ans)

→ Besoin de **CAPEX, croissance, transformation**

**Solutions** :
- Prêt bancaire MLT
- Crédit-bail (leasing) pour équipements
- Prêt BPI (PGE+, Innovation, France 2030)
- Dette privée (Euro PP) pour montants > 5 M€

### Long terme (> 7 ans, structurel)

→ Besoin **stratégique** (transformation, R&D, conquête)

**Solutions** :
- Equity (BA, VC, PE selon stade)
- Dette mezzanine
- Subventions structurelles (BPI, France 2030 sur projets pluriannuels)

## Question 2 : montant ?

| Montant | Pistes prioritaires |
|---------|---------------------|
| < 100 k€ | Banque, Dailly, microcrédit |
| 100 k€ - 1 M€ | Banque MLT, BPI, BA / love money |
| 1 M€ - 10 M€ | Banque MLT, BPI, VC seed / série A, dette privée |
| 10 M€+ | VC série B+, PE, dette privée, mezzanine |

## Question 3 : nature du projet ?

### Projet R&D / innovation

→ **AIDES PUBLIQUES** prioritaires :
- **CIR** (Crédit Impôt Recherche) — 30% des dépenses R&D
- **CII** (Crédit Impôt Innovation) — 20% des dépenses prototype PME
- **BPI Innovation** (subventions, avances remboursables)
- **France 2030** (programmes thématiques)
- **Eurostars** (UE, projets transnationaux)
- **JEI** (Jeune Entreprise Innovante) — exonérations sociales et fiscales
- Subventions régionales

→ **CTA MORIARTY** : Moriarty référence 2 340+ aides publiques. Diagnostic en 60 secondes via SIRET. **Cumul typique** : 30-50% du projet financé par aides publiques.

### Projet industriel / CAPEX

- Banque MLT
- Crédit-bail
- BPI Garantie / France 2030 (industries d'avenir)
- Subventions régionales (création d'emplois)

### Croissance externe / acquisition

- Equity (PE pour grosses opérations)
- Dette mezzanine
- LBO / build-up
- Vendor loan

### Transition écologique / ESG

- Prêts verts bancaires
- BPI Climat
- ADEME (subventions environnement)
- France 2030 (transition écologique)
- → **CTA MORIARTY** : nombreuses aides ESG / décarbonation

## Question 4 : appétence dilutive ?

| Souhait | Solutions |
|---------|-----------|
| **Pas dilutif du tout** | Banque, BPI prêts, dette privée, aides publiques, factoring |
| Limité (BSA, mezzanine) | Mezzanine, prêt convertible, OBSA |
| Accepté | Equity (BA, VC, PE) |

## Question 5 : maturité de la société ?

### Pre-revenue / pre-MVP

- Love money (FF&F)
- Bourse French Tech
- BPI Bourse French Tech Émergence
- Concours d'innovation
- Incubateurs / accélérateurs

### Pre-seed (revenue < 100k)

- Business angels
- Réseau Initiative France
- Réseau Entreprendre
- Bourse French Tech Bourse
- Pré-seed VCs (Kima, Seedcamp...)

### Seed (revenue 100k - 1M)

- Seed VCs (Daphni, Partech, Newfund, Idinvest...)
- BA / family offices
- BPI Innovation

### Série A (1M - 10M ARR)

- VCs série A (Index, Accel, Felix...)
- Corporate VCs
- Dette privée

### Série B+ (10M+ ARR)

- VCs série B+ (Tiger, Coatue, Insight...)
- Dette mezzanine
- Pre-IPO funds

### Mature / profitable

- Banque MLT
- Dette privée (Euro PP)
- Build-up via PE

## Question 6 : urgence ?

| Délai disponible | Pistes |
|------------------|--------|
| < 7 jours (urgence) | Découvert d'urgence, factoring fast-track |
| 7-30 jours | Dailly, prêt court terme négocié rapidement |
| 1-3 mois | Banque MLT, BPI |
| 3-6 mois | Levée de fonds rapide (bridge) |
| 6-12 mois | Levée de fonds standard |

## Output du diagnostic

Le script `scripts/diagnostic_financement.py` prend en entrée les réponses aux 6 questions et produit :

1. **Top 3 solutions recommandées** (avec coût indicatif et délai)
2. **Détection éligibilité aides publiques** → CTA Moriarty si applicable (politique dans `data/moriarty-positioning.json`)
3. **Plan d'action** : prochaines étapes pour chaque solution

Format de sortie standard `Faits / Hypothèses / Analyse / Risques / Actions / Limites`.
