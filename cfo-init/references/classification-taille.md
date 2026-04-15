# Classification multi-critères de la société

Règles de classification appliquées par `cfo-init` pour déterminer la **taille**, la **scope CSRD**, le **régime fiscal/TVA**, et les **modules sectoriels** à activer.

Toutes les constantes sont dans `../../data/seuils-classification.json`, modifier ce fichier si les seuils légaux évoluent.

## 1. Classification par taille (INSEE + Code de commerce)

### Source officielle

- INSEE : https://www.insee.fr/fr/metadonnees/definition/c1057
- Code de commerce art. L. 123-16 (catégories d'entreprises)

### Méthode

Une entreprise est dans la catégorie **la plus élevée** dès qu'elle dépasse **2 critères sur 3** parmi effectif / CA / bilan.

| Taille | Effectif | CA HT max | Bilan max |
|--------|----------|-----------|-----------|
| TPE / Microentreprise | < 10 | 2 M€ | 2 M€ |
| Petite Entreprise (PE) | < 50 | 12 M€ | 6 M€ |
| Moyenne Entreprise (ME) | < 250 | 50 M€ | 43 M€ |
| ETI | < 5 000 | 1,5 Md€ | 2 Md€ |
| Grande Entreprise (GE) | ≥ 5 000 | > 1,5 Md€ | > 2 Md€ |

### Prioriser les données API

Les API INSEE (Sirene V3, Annuaire Entreprises) retournent directement `categorie_entreprise` (PME/ETI/GE). Utiliser cette donnée en **priorité** plutôt que re-calculer localement, sauf si l'utilisateur fournit ses propres chiffres.

### Cas des sociétés non employeuses

Si `tranche_effectif = "NN"` (non renseignée) ou `"00"` (0 salarié) : considérer comme **TPE** par défaut, tout en demandant confirmation.

## 2. Scope CSRD

### Vagues d'application

| Wave | Premier exercice reporté | Déclaration | Critères |
|------|--------------------------|-------------|----------|
| Wave 1 | 2024 (déjà) | 2025 | Cotées / PIE, ≥ 500 employés |
| Wave 2 | **2028** (repoussé de 2026) | 2029 | Non cotées, ≥ 250 employés, ≥ 2 des 3 : CA 50M€, bilan 25M€ |
| Wave 3 | 2028 | 2029 | PME cotées marché réglementé, 10-250 employés |
| Wave 4 | 2028 | 2029 | Groupes hors UE avec CA EU > 150M€ |
| Hors scope |, |, | < 250 employés ET < 50M€ CA ET < 25M€ bilan, non cotées |

> ⚠️ **Wave 2 repoussée à 2028** par la directive (UE) 2025/794 du 14 avril 2025 ("Stop-the-Clock"). Anticiper la préparation dès 2026-2027 reste recommandé pour les entités potentiellement in-scope.

### Règle de décision

```python
def compute_csrd_wave(company):
    if company.is_listed and company.is_public_interest and company.effectif >= 500:
        return "wave_1"

    if company.effectif >= 250 and (company.ca_eur >= 50_000_000 or company.bilan_eur >= 25_000_000):
        return "wave_2"  # 2028 (post-stop-the-clock)

    if company.is_listed and 10 <= company.effectif <= 250:
        return "wave_3"

    if company.is_non_eu_group and company.ca_eu_eur >= 150_000_000:
        return "wave_4"

    return "hors_scope"
```

## 3. Multi-entités / groupes

Si la société a **≥ 1 filiale** :
- Activer le sub-module consolidation dans `cfo-comptabilite`
- Activer le sub-module transfer pricing dans `cfo-fiscalite` (si filiales multi-juridictions)
- Activer le cash pooling dans `cfo-tresorerie`
- Activer le segment reporting (IFRS 8) dans `cfo-reporting`

Détection :
- Via Pappers API : champ `filiales` ou liste d'établissements
- Via INSEE : `nombre_etablissements > 1`
- Via input utilisateur : demander "Avez-vous des filiales ?"

## 4. Secteur (code NAF)

Mapping NAF → module sectoriel dans `../../data/secteurs-naf.json`.

Modules sectoriels disponibles :

| Module | Secteurs | Effets |
|--------|----------|--------|
| `saas_techno` | 6201Z, 6202A, 6202B | KPI pack SaaS (MRR, ARR, churn, burn), mode startup |
| `industrie` | Section C, D | Stocks CMP/PEPS/LIFO, compta analytique par centre, amortissements accélérés |
| `commerce_negoce` | Section G | Marge brute key, rotation stocks, saisonnalité |
| `services_btob` | 7022Z, Section M/N | TJM, DSO élevé fréquent, compta analytique par mission |
| `lmnp_airbnb` | 5520Z | BIC, amortissement immo, commission Airbnb 622, CFE |
| `btp` | Section F | Compta par chantier, sous-traitance, TVA autoliquidation |
| `finance_reglemente` | Section K | ACPR/AMF prudentiel (warning : hors scope bundle) |
| `sante` | Section Q | Spécificités cliniques/EHPAD |

## 5. Spécificités géographiques

### DOM-TOM

Si `company.code_postal` commence par **97** ou **98** → activer le module DOM-TOM :

| Territoire | Code | Particularités |
|------------|------|----------------|
| Guadeloupe | 971 | Abattement IS 33,33%, TVA 8,5/2,1% |
| Martinique | 972 | Idem Guadeloupe, octroi de mer |
| Guyane | 973 | Idem |
| Réunion | 974 | Idem |
| Mayotte | 976 | Idem |

Renvoi : `paperasse/comptable > section DOM-TOM` (si skill installé).

### Alsace-Moselle et Corse

Détection via code postal 67, 68, 57, 2A, 2B. Particularités documentées mais moins impactantes.

## 6. Régime fiscal

### IS vs IR

Dérivé de la forme juridique :

| Forme juridique | Régime par défaut | Option |
|-----------------|-------------------|--------|
| SAS, SARL, SA, SCA, SE | IS | Possible IR 5 ans pour SAS |
| EURL | IR | Possible IS |
| SARL famille | IR | Possible IS |
| EI (Entreprise Individuelle) | IR BIC/BNC/BA | Non applicable |

### Taux IS 2026

- Taux normal : **25%**
- Taux réduit PME : **15%** sur les 42 500 premiers € de bénéfices (conditions : CA HT < 10 M€, capital entièrement libéré, détenu à 75% min. par personnes physiques)

## 7. Régime TVA

### Seuils 2026

| Régime | Seuil services HT | Seuil ventes HT | Fréquence |
|--------|-------------------|-----------------|-----------|
| Franchise en base | 36 800 € | 91 900 € | Aucune déclaration |
| Réel simplifié | < 254 000 € | < 840 000 € | Annuelle (CA12) + acomptes semestriels |
| Réel normal mensuel | au-delà | au-delà | Mensuelle (CA3) |
| Réel normal trimestriel |, |, | Trimestriel si TVA annuelle < 4 000 € |

## 8. Agrégation finale

`scripts/fetch_pappers.py` + `scripts/fetch_sirene.py` + input utilisateur → agrégation dans `private/company.json` selon `templates/company.template.json`.

### Ordre de priorité des sources

1. **Input utilisateur** (le plus fiable, valeurs à jour)
2. **API Pappers** (données enrichies, comptes annuels)
3. **API INSEE Sirene V3** (officiel, authoritative)
4. **API Annuaire Entreprises** (public, simple)
5. **WebFetch** (dernier recours)

Si discordance entre sources : **demander à l'utilisateur** quelle valeur retenir. Ne jamais supposer.

## Validation finale

Avant de valider `private/company.json`, `cfo-init` **affiche la synthèse** et demande confirmation :

```
Voici le profil que j'ai constitué :

- Société : CARREFOUR SA (SIREN 552120222)
- Taille : ETI (effectif 320 000, CA ~95 Md€), source : INSEE
- Secteur : 4711F Hypermarchés, module grande_distribution
- Scope CSRD : Wave 1 (cotée, PIE, 500+) → obligation reporting 2024 déjà en place
- Date clôture : 31/12/2026, input utilisateur
- Régime : IS 25% · TVA réel normal mensuelle

Est-ce exact ? (oui / à corriger)
```

Si corrections demandées : ajuster `private/company.json` et re-valider.
