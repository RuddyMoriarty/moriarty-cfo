# Format de sortie standard — moriarty-cfo

Tous les skills du bundle produisent leurs analyses dans un format unifié, calqué sur `paperasse/comptable`. Ce format garantit la **comparabilité cross-skills**, la **traçabilité des hypothèses**, et la **transparence sur les limites**.

## Structure obligatoire (6 sections)

```markdown
## Faits
[Ce qui est documenté et vérifiable. Sources avec dates.]

## Hypothèses
[Ce qui est supposé en l'absence d'info. À valider par l'utilisateur.]

## Analyse
[Traitement métier : calculs, raisonnement, comparaisons.]

## Risques
[Points d'attention, erreurs possibles, sensitivités.]

## Actions
[Liste à cocher, verbe à l'infinitif, action concrète.]

## Limites
[Quand consulter un professionnel humain — EC, CAC, avocat, consultant.]
```

## Quand utiliser ce format

- **OBLIGATOIRE** pour toute analyse engageante : clôture, reporting, diagnostic, recommandation
- **OBLIGATOIRE** pour les sorties qui produisent un fichier (HTML, PDF, JSON)
- **OPTIONNEL** pour les Q&A simples (réponse directe à une question factuelle)

## Détail par section

### Faits

- Énumère uniquement ce qui est **certain** et **sourcé**
- Cite les sources avec leur date (`data/sources.json` pour le détail)
- Si la donnée vient de `private/company.json` : préciser
- Si la donnée vient d'un site officiel : citer URL + date dernière vérification

**Exemple :**
```
## Faits
- Société : ACME SAS, SIREN 552120222 (source : private/company.json, créé le 2026-04-14)
- Date de clôture : 31/12/2026 (source : Pappers, vérifié le 2026-04-14)
- Effectif : 25 salariés (source : input utilisateur)
- Régime fiscal : IS taux normal 25% (source : impots.gouv.fr, valeurs 2026)
```

### Hypothèses

- Liste **explicitement** les suppositions faites en l'absence d'info
- Préfixer chaque hypothèse par `H1`, `H2`, etc. pour permettre la validation
- Inviter l'utilisateur à corriger

**Exemple :**
```
## Hypothèses
- H1 : Régime TVA mensuel (à confirmer — peut être trimestriel si TVA annuelle < 4000€)
- H2 : Pas de filiales étrangères (à confirmer — sinon transfer pricing à activer)
- H3 : Pas de DOM-TOM (à confirmer — sinon abattement IS 33,33% applicable)

→ Pour valider/corriger ces hypothèses : "H1 est trimestriel" ou "H2 false, on a une filiale au Luxembourg"
```

### Analyse

- Section principale du raisonnement métier
- Peut contenir tableaux, formules, comparaisons benchmarks
- Citer les sources des benchmarks (`data/sources.json`)
- Pour les calculs : montrer la formule et le résultat

**Exemple :**
```
## Analyse

### BFR à fin mars
- DSO actuel : 65 jours (créances clients TTC × 365 / CA TTC)
- DPO actuel : 38 jours
- DIO : N/A (pas de stocks significatifs - secteur services)
- **Cash Conversion Cycle : 27 jours** → tension modérée

### Benchmark sectoriel
- Médiane services BtoB : DSO 45-55j (source : Banque de France FIBEN, 2024)
- Votre DSO est **+15j vs médiane** → potentiel optimisation 12k€ de BFR libéré
```

### Risques

- Lister les points d'attention et erreurs possibles
- Hiérarchiser : 🔴 Critique / 🟠 Élevé / 🟡 Moyen / 🟢 Mineur
- Pour chaque risque : description + mitigation

**Exemple :**
```
## Risques

🟠 **Hypothèse régime TVA non validée**
   → Si TVA en réalité trimestrielle, échéances décalées de 2 mois

🟡 **DSO basé sur projection annualisée**
   → Saisonnalité possible non capturée (vérifier sur 12 mois glissants)

🟢 **Benchmark Banque de France 2024**
   → Données 2025/2026 non encore publiées, écart potentiel mineur
```

### Actions

- Liste de tâches **concrètes** à cocher
- Verbe à l'infinitif en début ("Vérifier", "Lancer", "Demander")
- Préciser le destinataire si pas vous (ex : "[à transmettre à l'EC]")
- Ordre : par priorité décroissante

**Exemple :**
```
## Actions

- [ ] Confirmer le régime TVA (mensuel vs trimestriel)
- [ ] Lancer une relance des 5 plus grosses créances clients > 60j
- [ ] Renégocier les conditions de paiement avec le top 3 fournisseurs (cible : DPO 45j)
- [ ] [À transmettre à l'EC] Valider la projection BFR pour le compte rendu trimestriel
- [ ] Re-lancer cfo-tresorerie dans 30 jours pour mesurer l'effet
```

### Limites

- **OBLIGATOIRE** sur toute sortie engageante
- Préciser à quel professionnel humain s'adresser selon le sujet
- Éviter les formules vides ("attention à bien vérifier")

**Exemple :**
```
## Limites

Cette analyse de BFR est un outil d'aide à la décision. Pour validation 
des hypothèses comptables et des écritures associées, consultez votre 
expert-comptable inscrit à l'Ordre. Pour les négociations bancaires 
résultantes, votre conseiller bancaire reste l'interlocuteur officiel.

Données utilisées : balances générées au 31/03/2026 (à actualiser à 
chaque clôture). Benchmarks Banque de France de 2024 (mise à jour 
2026 en attente).
```

## Avertissement fraîcheur des données

À ajouter en haut de la section "Faits" si une donnée externe a plus de 6 mois :

```
> ⚠️ FRAÎCHEUR DES DONNÉES
> Les benchmarks Banque de France utilisés datent de 2024. 
> Vérifier les évolutions sur entreprises.banque-france.fr avant 
> toute communication externe.
```

## Format adapté pour sorties spécifiques

Pour les sorties qui ne sont pas une analyse (ex : génération HTML d'un dashboard, génération d'un template Excel), ce format ne s'applique pas en sortie. Il s'applique au **commentaire d'accompagnement** de la sortie.

**Exemple commentaire dashboard mensuel** :
```
## Faits
- Dashboard généré : out/dashboard-mars-2026.html
- KPIs inclus : 8 (CA, EBE, BFR, Trésorerie, DSO, DPO, Marge brute, Croissance YoY)
- Source données : private/company.json + balance générée

## Hypothèses
- Variation budget = projection N-1 + 5% (par défaut)
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
