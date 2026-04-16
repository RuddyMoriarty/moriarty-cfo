# Structure du Plan Comptable General

Ossature du PCG telle que definie par le reglement ANC 2014-03 modifie (consolide au 1er janvier 2025). Ce fichier donne la structure de reference pour le bundle. Le detail complet (sous-comptes a 6+ chiffres, regles de fonctionnement par compte) est dans `paperasse/comptable`.

## Principe de numerotation

- **Classe** : 1 chiffre (1 a 7 pour les comptes de bilan et de resultat, 8 pour engagements hors bilan)
- **Sous-classe** : 2 chiffres
- **Compte** : 3 chiffres
- **Sous-compte** : 4+ chiffres (libre, selon plan interne de l'entreprise)

Regle de base : le premier chiffre determine la nature du compte. Les comptes de bilan (classes 1 a 5) sont credites ou debites selon leur nature. Les comptes de gestion (classes 6 et 7) enregistrent les charges et produits de l'exercice.

## Vue d'ensemble des classes

| Classe | Intitule | Nature |
|--------|----------|--------|
| 1 | Comptes de capitaux | Bilan (passif et actif selon sous-compte) |
| 2 | Comptes d'immobilisations | Bilan actif (actif non courant) |
| 3 | Comptes de stocks et en-cours | Bilan actif (actif courant) |
| 4 | Comptes de tiers | Bilan actif ou passif selon solde |
| 5 | Comptes financiers | Bilan actif (tresorerie) |
| 6 | Comptes de charges | Compte de resultat (debit) |
| 7 | Comptes de produits | Compte de resultat (credit) |
| 8 | Comptes speciaux | Engagements hors bilan |

## Classe 1 - Comptes de capitaux

| Compte | Intitule | Usage CFO |
|--------|----------|-----------|
| 10 | Capital et reserves | Capital social, primes d'emission |
| 101 | Capital | Montant du capital social |
| 106 | Reserves | Reserve legale (1061), reserves statutaires (1063) |
| 108 | Compte de l'exploitant | Entreprise individuelle uniquement |
| 11 | Report a nouveau | RAN beneficiaire (110) ou deficitaire (119) |
| 12 | Resultat de l'exercice | Benefice (120) ou perte (129) |
| 13 | Subventions d'investissement | Subventions equipement, a rapporter au resultat |
| 14 | Provisions reglementees | Amortissements derogatoires (145), provisions pour hausse des prix (143) |
| 15 | Provisions pour risques et charges | Provisions pour litiges (1511), garanties (1512), restructurations (154) |
| 16 | Emprunts et dettes assimilees | Emprunts bancaires (164), CBC (519 mais lie), emprunts obligataires (161) |
| 17 | Dettes rattachees a des participations | Comptes courants groupe |
| 18 | Comptes de liaison | Etablissements, succursales |

## Classe 2 - Comptes d'immobilisations

| Compte | Intitule | Usage CFO |
|--------|----------|-----------|
| 20 | Immobilisations incorporelles | Frais d'etablissement (201), R&D (203), concessions/brevets (205), fonds commercial (207) |
| 21 | Immobilisations corporelles | Terrains (211), constructions (213), materiel (215), mobilier (218) |
| 23 | Immobilisations en cours | Immobilisations en cours de production |
| 26 | Participations et creances rattachees | Titres de participation (261), creances (267) |
| 27 | Autres immobilisations financieres | Prets (274), depots et cautionnements (275) |
| 28 | Amortissements des immobilisations | 280x en miroir des comptes 20x-21x |
| 29 | Depreciations des immobilisations | 290x en miroir |

## Classe 3 - Comptes de stocks

| Compte | Intitule | Usage CFO |
|--------|----------|-----------|
| 31 | Matieres premieres | Stock MP |
| 33 | En-cours de production de biens | WIP |
| 34 | En-cours de production de services | Prestation en cours |
| 35 | Stocks de produits | Produits finis (355), intermediaires (351) |
| 37 | Stocks de marchandises | Negoce |
| 39 | Depreciations des stocks | Provisions pour depreciation |

## Classe 4 - Comptes de tiers

| Compte | Intitule | Usage CFO |
|--------|----------|-----------|
| 40 | Fournisseurs et comptes rattaches | Fournisseurs (401), EAP (403), fournisseurs d'immobilisations (404) |
| 41 | Clients et comptes rattaches | Clients (411), EAR (413), clients douteux (416) |
| 42 | Personnel et comptes rattaches | Remuneration due (421), charges a payer (428) |
| 43 | Securite sociale et organismes sociaux | URSSAF (431), retraite complementaire (437) |
| 44 | Etat et collectivites publiques | IS (444), TVA collectee (4457), TVA deductible (4456), CIR/CII (449) |
| 45 | Groupe et associes | Comptes courants d'associes (455) |
| 46 | Debiteurs et crediteurs divers | Creances/dettes diverses |
| 47 | Comptes transitoires ou d'attente | Charges a repartir, produits constates d'avance |
| 48 | Comptes de regularisation | Charges constatees d'avance (486), produits constates d'avance (487) |
| 49 | Depreciations des comptes de tiers | Provisions pour creances douteuses (491) |

## Classe 5 - Comptes financiers

| Compte | Intitule | Usage CFO |
|--------|----------|-----------|
| 50 | Valeurs mobilieres de placement | VMP, OPCVM court terme |
| 51 | Banques, etablissements financiers | Banque (512), caisse (531) |
| 53 | Caisse | Especes |
| 58 | Virements internes | Transferts entre comptes |
| 59 | Depreciations des comptes financiers | Depreciation VMP (590) |

## Classe 6 - Comptes de charges (les plus utilises par le CFO)

| Compte | Intitule | Contenu typique |
|--------|----------|-----------------|
| 60 | Achats | Matieres premieres (601), autres approvisionnements (602), marchandises (607) |
| 61 | Services exterieurs | Sous-traitance (611), locations (613), entretien (615), assurances (616) |
| 62 | Autres services exterieurs | Honoraires (6226), publicite (6231), deplacements (6251), telecom (626) |
| 63 | Impots, taxes et versements assimiles | CFE/CVAE (63511/63512), taxe fonciere (6354), TVS (6354) |
| 64 | Charges de personnel | Salaires (641), charges sociales (645), participation (691) |
| 65 | Autres charges de gestion courante | Redevances (651), pertes sur creances irrecouvrables (654) |
| 66 | Charges financieres | Interets bancaires (6611), pertes de change (666), escomptes accordes (665) |
| 67 | Charges exceptionnelles | VNC immobilisations cedees (675), penalites (6712) |
| 68 | Dotations aux amortissements, depreciations et provisions | DAP exploitation (681), DAP financieres (686), DAP exceptionnelles (687) |
| 69 | Participation, IS et assimiles | Participation salaries (691), IS (695) |

## Classe 7 - Comptes de produits (les plus utilises par le CFO)

| Compte | Intitule | Contenu typique |
|--------|----------|-----------------|
| 70 | Ventes de produits et services | Ventes marchandises (707), prestations de services (706), produits finis (701) |
| 71 | Production stockee | Variation de stocks produits finis/en-cours |
| 72 | Production immobilisee | Immobilisations produites par l'entreprise |
| 74 | Subventions d'exploitation | Subventions recues (CICE historique, aides emploi) |
| 75 | Autres produits de gestion courante | Redevances recues, revenus immobiliers |
| 76 | Produits financiers | Produits de participation (761), revenus VMP (764), gains de change (766) |
| 77 | Produits exceptionnels | Prix de cession immobilisations (775), subventions d'investissement rapportees (777) |
| 78 | Reprises sur amortissements, depreciations et provisions | Reprises exploitation (781), financieres (786), exceptionnelles (787) |
| 79 | Transferts de charges | Transferts de charges d'exploitation (791), financieres (796) |

## Regles pratiques pour le CFO

1. **Coherence PCG/FEC** : le `CompteNum` du FEC doit correspondre exactement au plan de comptes PCG utilise. Toute incoherence declenche un rejet DGFiP potentiel.

2. **Plan de comptes interne** : vous pouvez ajouter des sous-comptes (ex. 6226001 = Honoraires avocat, 6226002 = Honoraires EC) tant que le prefixe respecte le PCG.

3. **Comptes interdits** : ne pas utiliser les comptes de classe 8 dans la comptabilite courante (reserves aux engagements hors bilan).

4. **Symetrie amortissements/depreciations** : les comptes 28x/29x sont toujours le "miroir" des comptes 20x-27x. Idem 39x pour stocks, 49x pour tiers, 59x pour financiers.

5. **Distinction charges/immobilisations** : seuil de 500 EUR HT en dessous duquel les biens peuvent etre charges directement (tolerance fiscale, BOI-BIC-CHG-20-30-10).

## Correspondance PCG - Liasse fiscale

Les tableaux de la liasse fiscale reprennent directement les soldes des comptes PCG :

| Tableau liasse | Comptes PCG correspondants |
|----------------|---------------------------|
| 2050 (Bilan actif) | Classes 2, 3, 4 (debiteurs), 5 |
| 2051 (Bilan passif) | Classe 1, 4 (crediteurs) |
| 2052-2053 (Compte de resultat) | Classes 6 et 7 |
| 2054 (Immobilisations) | Classe 2 (mouvements de l'exercice) |
| 2055 (Amortissements) | Comptes 28x (mouvements de l'exercice) |
| 2056 (Provisions) | Comptes 14x, 15x, 29x, 39x, 49x |
| 2057 (Creances et dettes) | Comptes 4xx, echeances a moins/plus d'un an |

## Erreurs frequentes de codification

| Erreur | Consequence | Correction |
|--------|-------------|------------|
| Charge en 21x au lieu de 60x/61x/62x | Gonfle l'actif, minore les charges | Reclasser si < 500 EUR HT ou si consommable |
| Emprunt en 40x (fournisseur) au lieu de 16x | Fausse le bilan et le ratio d'endettement | Separer dettes financieres des dettes fournisseurs |
| TVA en 60x (incluse dans les achats) | Fausse le montant des achats et la TVA deductible | Toujours enregistrer les achats HT + TVA en 4456x |
| Compte courant associe en 45x au lieu de 16x | Fausse la classification de la dette | 455 si remboursable a vue, 168 si convention a terme |
| Provision en 15x sans justificatif | Risque de rejet fiscal (non deductible) | Documenter le risque, la probabilite et le montant estime |

## Sources

- Reglement ANC n. 2014-03 du 5 juin 2014 relatif au plan comptable general, consolide au 1er janvier 2025 - https://www.anc.gouv.fr/normes-francaises/le-plan-comptable-general
- Code de commerce, art. L. 123-12 a L. 123-28 (obligation de tenue de comptabilite)
- BOI-BIC-CHG-20-30-10 (seuil d'immobilisation des biens de faible valeur) - https://bofip.impots.gouv.fr/bofip/4382-PGP
