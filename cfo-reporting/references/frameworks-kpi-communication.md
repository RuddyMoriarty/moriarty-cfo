# Frameworks KPI et communication financiere du DAF

Reference sur les cadres de reporting destines aux stakeholders : board, investisseurs, equipe de direction. Oriente pilotage et decision, pas production comptable.

## Perimetre DAF du reporting

Le reporting financier du CFO/DAF couvre la **communication de la performance** aux decideurs. Il ne couvre pas la production des comptes (cfo-comptabilite) ni le depot au greffe.

| Audience | Frequence | Format type | Contenu cle |
|----------|-----------|-------------|-------------|
| COMEX / Directoire | Mensuel (M+5) | Flash 1 page + dashboard | KPIs operationnels, ecarts budget, alertes |
| Conseil d'administration | Trimestriel | Board pack 12-15 slides | Performance, tresorerie, risques, perspectives |
| Investisseurs | Trimestriel | Lettre + KPIs standardises | Metriques cles, milestones, outlook |
| Actionnaires AG | Annuel | Rapport de gestion + resolution | Resultats, dividendes, strategie |
| Equipe operationnelle | Hebdo/Mensuel | Dashboard interactif | KPIs d'action, tendances, objectifs |

## KPIs par categorie (referentiel DFCG)

La DFCG (Association des Directeurs Financiers et de Controle de Gestion) identifie 5 familles de KPIs pour le reporting DAF.

### 1. Rentabilite et performance

| KPI | Formule | Benchmark PME France |
|-----|---------|---------------------|
| Marge brute % | (CA - Achats consommes) / CA | Varie par secteur (FIBEN) |
| EBE / CA | EBE / CA | 8-15 % PME industrielles |
| Resultat d'exploitation / CA | REX / CA | 3-8 % PME |
| ROCE | REX (1-t) / Capitaux employes | > WACC pour creation de valeur |
| ROE | Resultat net / Capitaux propres | > 10 % cible PME rentable |

### 2. Tresorerie et liquidite

| KPI | Formule | Seuil d'alerte |
|-----|---------|----------------|
| Cash runway | Cash disponible / Burn mensuel | < 6 mois = alerte |
| DSO (jours) | (Creances clients / CA TTC) x 365 | > 60j = hors LME |
| DPO (jours) | (Dettes fournisseurs / Achats TTC) x 365 | Aligner sur LME |
| BFR / CA | BFR / CA x 365 | En baisse = positif |
| Ratio de liquidite generale | Actif circulant / Passif circulant | > 1.2 |

### 3. Croissance et activite

| KPI | Formule | Contexte |
|-----|---------|----------|
| Croissance CA organique | (CA N - CA N-1) / CA N-1 | Hors acquisitions |
| MRR / ARR (SaaS) | Revenus recurrents mensuels / annuels | Specifique SaaS |
| Churn rate | Clients perdus / Clients debut de periode | < 5 % annuel cible |
| CAC / LTV | Cout acquisition / Valeur vie client | LTV/CAC > 3 |
| Carnet de commandes | Commandes fermes non livrees | Visibilite forward |

### 4. Structure et endettement

| KPI | Formule | Seuil covenant typique |
|-----|---------|----------------------|
| Gearing | Dettes financieres / Capitaux propres | < 1.0 |
| Leverage (Dette nette / EBITDA) | (Dettes fin. - Cash) / EBITDA | < 3.5x |
| DSCR | EBITDA / (Interets + Remb. capital) | > 1.2x |
| ICR | EBITDA / Interets | > 3.0x |

### 5. ESG et extra-financier (emergent)

| KPI | Source | Applicable |
|-----|--------|-----------|
| Emissions Scope 1+2 (tCO2e) | GHG Protocol | CSRD in-scope |
| Part CA aligne taxonomie | Reg. UE 2020/852 | CSRD in-scope |
| Score egalite F/H (Index Penicaud) | Art. L. 1142-8 C. trav. | > 50 salaries |
| Taux d'accidents du travail | DUERP | Toutes entreprises |

## Cadres de reporting reconnus

### Flash mensuel (M+5)

Structure recommandee DFCG pour un flash CFO a J+5 apres la cloture :

1. **Faits marquants** (3-5 bullets, qualitatif)
2. **P&L synthetique** (reel vs budget vs N-1, ecarts en valeur et %)
3. **Cash position** (solde, variation, prevision 4 semaines)
4. **KPIs operationnels** (3-5 KPIs cles du mois, tendance fleche)
5. **Alertes** (depassements budget > 10 %, risques identifies)
6. **Actions en cours** (decisions prises, suivi)

### Board pack trimestriel

Structure type pour un CA de PME (source : IFA - Institut Francais des Administrateurs) :

1. Synthese executif (1 slide)
2. Performance financiere (P&L, bilan synthetique, cash flow)
3. Analyse des ecarts vs budget et N-1
4. Tresorerie et previsions
5. KPIs operationnels et commerciaux
6. Investissements (CAPEX realise vs plan)
7. Risques et conformite (cartographie actualisee)
8. Perspectives et recommandations

### Lettre investisseurs

Pour les societes avec actionnariat externe (PE/VC, business angels) :

- Metriques cles du trimestre (CA, ARR, cash, burn, runway)
- Milestones atteints et manques
- Utilisation des fonds leves
- Perspectives et besoins
- Annexe chiffree (P&L + bilan + TFT simplifie)

## Regles de presentation

### Principes DFCG de lisibilite

- **Un chiffre = une comparaison** : toujours montrer reel vs budget vs N-1
- **Ecarts en valeur ET en %** : les deux sont necessaires
- **Code couleur** : vert = favorable, rouge = defavorable, gris = neutre
- **Graphiques > tableaux** pour les tendances temporelles
- **Fleches de tendance** pour les KPIs (hausse, baisse, stable)
- **Maximum 8 KPIs** sur un dashboard : au-dela, on perd le focus

### Hierarchie de l'information (pyramide inversee)

1. **Message cle** : "CA +12 % vs budget, marge en recul de 2 points"
2. **Chiffres principaux** : les 3-5 metriques qui soutiennent le message
3. **Detail** : annexes pour ceux qui veulent creuser

## Erreurs frequentes du reporting DAF

| Erreur | Impact | Correction |
|--------|--------|------------|
| Reporting a M+15 au lieu de M+5 | Board ne peut pas agir | Automatiser les sources de donnees |
| Trop de KPIs (15+) | Dilution de l'attention | Selectionner 5-8 KPIs lies a la strategie |
| Pas de comparatif (reel seul) | Impossible de juger la performance | Budget + N-1 systematiquement |
| Format change chaque mois | Impossible de suivre les tendances | Template fixe, actualise semestriellement |
| Chiffres sans commentaire | Le board ne comprend pas le "pourquoi" | 2-3 lignes de narratif par ecart significatif |
| Melange donnees definitives et estimees | Perte de confiance | Marquer clairement les estimations |

## Sources

- DFCG (Association des Directeurs Financiers et de Controle de Gestion) : https://www.dfcg.fr
- IFA (Institut Francais des Administrateurs) : https://www.ifa-asso.com
- IFAC (International Federation of Accountants), Role of the CFO : https://www.ifac.org
- France Invest (ex-AFIC), bonnes pratiques reporting PE/VC : https://www.franceinvest.eu
- Banque de France, FIBEN ratios sectoriels : https://www.banque-france.fr/statistiques
