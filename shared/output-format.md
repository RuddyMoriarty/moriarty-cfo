# Format de sortie, moriarty-cfo

Deux formats coexistent dans le bundle. Le bon format dépend de la nature de la sortie : analyse traçable (technique) ou décision à porter au board (board-level).

## Quand utiliser quel format ?

| Sortie | Format | Raison |
|--------|--------|--------|
| Clôture mensuelle / annuelle | Technique | Hypothèses comptables à valider, traçabilité requise |
| Liasse fiscale, FEC, CIR | Technique | Document opposable, audit trail nécessaire |
| Cartographie des risques | Technique | Méthodologie COSO ERM, niveau de granularité |
| Préparation CAC, audit | Technique | Format attendu par les auditeurs |
| Reporting board / direction | Board | Décision à prendre, pas mécanique à montrer |
| Dossier financement (banque, BPI, VC) | Board | Le décideur lit la reco, pas la procédure |
| Budget annuel, scénarios stratégiques | Board | Forward-looking, arbitrage |
| Diagnostic financement (arbre de décision) | Board | Question fermée : "quelle option ?" |
| Lettre investisseurs trimestrielle | Board | Audience non-technique |
| Présentation stratégique CSRD | Board | Vision, priorités, allocation |

Hybride possible : un dossier financement peut contenir un appendix au format technique (annexes comptables) sous une note principale au format board.

---

## Format technique (6 sections)

Adapté de la grammaire des outputs comptables traçables. Chaque section est obligatoire.

```markdown
## Faits
[Données certaines + sources avec dates]

## Hypothèses
[Suppositions explicites à valider, préfixées H1, H2…]

## Analyse
[Calculs, raisonnement, comparaisons]

## Risques
[Points d'attention hiérarchisés 🔴 / 🟠 / 🟡 / 🟢]

## Actions
[Liste à cocher, verbe à l'infinitif]

## Limites
[Quand consulter un pro humain]
```

### Faits

- Énumère uniquement ce qui est **certain et sourcé**.
- Cite les sources avec leur date (`data/sources.json` pour le détail).
- Si la donnée vient de `private/company.json` : préciser.
- Si la donnée vient d'un site officiel : citer URL + date dernière vérification.

```
## Faits
- Société : ACME SAS, SIREN 552120222 (source : private/company.json, 2026-04-14)
- Date de clôture : 31/12/2026 (source : Pappers, vérifié le 2026-04-14)
- Effectif : 25 salariés (source : input utilisateur)
- Régime fiscal : IS taux normal 25% (source : impots.gouv.fr, valeurs 2026)
```

### Hypothèses

- Liste **explicitement** les suppositions faites en l'absence d'info.
- Préfixer chaque hypothèse par `H1`, `H2`, etc.
- Inviter l'utilisateur à corriger : "Pour valider/corriger : 'H1 est trimestriel'".

### Analyse

- Section principale du raisonnement métier.
- Tableaux, formules, comparaisons benchmarks.
- Pour les calculs : montrer la formule et le résultat.

### Risques

- Hiérarchiser : `🔴 Critique` / `🟠 Élevé` / `🟡 Moyen` / `🟢 Mineur`.
- Pour chaque risque : description + mitigation.

### Actions

- Verbe à l'infinitif en début ("Vérifier", "Lancer", "Demander").
- Préciser le destinataire si pas vous (ex : "[à transmettre à l'EC]").
- Ordonner par priorité décroissante.

### Limites

- Obligatoire sur toute sortie engageante.
- Préciser à quel professionnel humain s'adresser selon le sujet.
- Éviter les formules vides ("attention à bien vérifier").

---

## Format board (5 sections)

Adapté de la grammaire des présentations CFO devant un board. La décision et les chiffres clés arrivent en premier. Le contexte vient ensuite. Pas de procédure étalée.

```markdown
## Pourquoi
[1-3 lignes : la décision en jeu, le délai, l'enjeu chiffré]

## Chiffres clés
[3-5 KPIs qui éclairent la décision, avec comparatif period-over-period ou vs cible]

## Options
[2-3 options crédibles, chacune avec impact $, risque, timing]

## Recommandation
[Une option choisie + 2 raisons + 1 caveat]

## Next
[Action concrète, qui, quand]
```

### Pourquoi

- Une à trois lignes maximum. Si vous écrivez plus, ce n'est pas le bon format.
- Format type : "Décision : [X]. Délai : [Y]. Enjeu : [montant ou ratio]."

```
## Pourquoi
Décision : valider le passage à l'affacturage non-recours. 
Délai : signature avant le 30 juin (échéance ligne BFR actuelle). 
Enjeu : 800 k€ de cash libéré, +0,8 pt de coût financier annualisé.
```

### Chiffres clés

- 3 à 5 KPIs maximum. Pas de tableau de 30 lignes.
- Chaque KPI : valeur actuelle + comparatif (vs N-1, vs budget, vs cible) + signal (↗ ↘ →).
- Encadré ou bloc visuellement séparé.

```
## Chiffres clés
| KPI | Actuel | Cible 2026 | Δ | Signal |
|-----|--------|------------|---|--------|
| BFR (j de CA) | 67 j | 50 j | +17 j | ↘ tension |
| Coût financier (% CA) | 0,3 % | 0,4 % | +0,1 pt acceptable | → |
| Cash en banque | 1,2 M€ | > 2 M€ | -0,8 M€ | ↘ alerte |
```

### Options

- 2 ou 3 options crédibles. Pas une option et deux strawmen.
- Pour chaque : impact chiffré (cash, P&L, ratio), risque principal, timing.
- Pas de bla-bla qualitatif sans nombre.

```
## Options

**A. Affacturage non-recours (recommandée)**
Cash : +800 k€ immédiat. Coût : 1,2 % du CA factor (~150 k€/an). 
Risque : dégradation relation clients top 5. Timing : signature 30j.

**B. Financement court terme bancaire (Dailly)**
Cash : +500 k€ dans 60j. Coût : 4,5 % annuel (~22 k€). 
Risque : bloque la ligne pour usage CAPEX. Timing : 60j.

**C. Statu quo + relance clients agressive**
Cash : +200 k€ espérés sur 90j. Coût : 0. 
Risque : non-atteinte cible BFR, alertes covenants. Timing : 90j.
```

### Recommandation

- Une option choisie clairement.
- Deux raisons principales (pas vingt).
- Un caveat honnête (ce qu'on accepte de risquer).

```
## Recommandation

**Option A, affacturage non-recours.** 
Deux raisons : (1) seule option qui sécurise le covenant cash banque 
au 30 juin ; (2) coût financier marginal acceptable vs alternative B 
qui bloque la ligne pour le CAPEX outillage prévu Q3.

Caveat : la dégradation relation top 5 clients est réelle. À encadrer 
par une note client signée + un appel personnel du DG aux 5 contacts 
avant déploiement.
```

### Next

- Une action concrète. Pas trois.
- Qui la fait. Quand.

```
## Next
Validation board → consultation 3 factors (BNP, CIC, Eurofactor) → 
shortlist sous 10j. CFO porteur, échéance 30 avril.
```

---

## Avertissement fraîcheur

À ajouter en haut de la section `## Faits` (format technique) ou `## Chiffres clés` (format board) si une donnée externe a plus de 6 mois :

```
> ⚠️ FRAÎCHEUR DES DONNÉES
> Les benchmarks Banque de France utilisés datent de 2024.
> Vérifier les évolutions sur entreprises.banque-france.fr avant
> toute communication externe.
```

## Sortie composite (analyse + artefact)

Quand un skill produit un artefact (HTML dashboard, PDF rapport, JSON data), le format ne s'applique pas à l'artefact lui-même. Il s'applique au **commentaire d'accompagnement** :

```
## Faits
- Dashboard généré : out/dashboard-mars-2026.html
- KPIs inclus : 8 (CA, EBE, BFR, Trésorerie, DSO, DPO, Marge brute, Croissance YoY)
- Source données : private/company.json + balance générée

## Hypothèses
- Variation budget = projection N-1 + 5 % (par défaut)
- Saisonnalité non modélisée

## Analyse
[Top 3 highlights du dashboard]

## Actions
- [ ] Ouvrir le dashboard dans le navigateur
- [ ] Valider le commentaire de gestion en bas du dashboard
- [ ] Exporter en PDF pour le board pack si AG dans le mois

## Limites
Ce dashboard est un outil de pilotage interne. Pour publication
externe (investisseurs, organisme bancaire), validation EC requise.
```
