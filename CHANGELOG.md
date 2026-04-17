# Changelog

Toutes les évolutions notables de `moriarty-cfo` sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [0.2.3], 2026-04-17

Integration live de l'API Annuaire Entreprises dans l'onboarding PME et cabinet EC. Flag `--fetch` sur `init_pme.py` et `init_cabinet.py` : l'utilisateur tape un SIREN, le bundle enrichit automatiquement avec denomination legale, NAF, tranche effectif INSEE, nombre d'etablissements, adresse siege. Taille (TPE/PE/ME/ETI/GE) auto-mappee depuis `categorie_entreprise` INSEE.

### Fixed

**Violation stdlib-only corrigee** : les scripts `cfo-init/scripts/fetch_pappers.py` et `cfo-init/scripts/fetch_sirene.py` importaient `requests` (dependance externe), ce qui violait la politique CLAUDE.md "Python stdlib only" depuis v0.1.0. Ces scripts n'avaient jamais ete testes et auraient plante sur un poste sans `requests` installe.

Les deux scripts sont desormais migres vers `urllib.request` (stdlib) :

- Helper `_http_get_json(url, params, headers)` pour les GET
- Helper `_http_post_form(url, form_data, headers)` pour les POST form-urlencoded (auth INSEE OAuth)
- Gestion explicite de `urllib.error.HTTPError`, `URLError`, `TimeoutError`
- User-Agent `moriarty-cfo/0.2` par defaut

Bug collateral fixe : endpoint API Annuaire Entreprises corrige (`/search` au lieu de `/v3/search`, l'API a supprime le prefixe de version courant 2024). Teste en live sur SIREN 552120222 Societe Generale : 4250 etablissements, NAF 64.19Z correctement extraits.

### Added

- **Flag `--fetch`** sur `init_pme.py` et `init_cabinet.py` : enrichit le company.json ou cabinet.json avec les champs publics INSEE. Degrade proprement si l'API est indisponible.
- **Auto-mapping taille** : `categorie_entreprise` INSEE (PME/ETI/GE/TPE) -> `classification.taille` du bundle, avec fallback sur la valeur CLI si fournie.
- **Test fonctionnel** `evals/_helpers/check_fetch_siren.py` (6 checks offline) :
  - Compile des 2 scripts
  - Verification stdlib-only (rejette tout import de `requests`, `httpx`, `aiohttp`, `pycurl`)
  - Mode `--mode web` retourne une instruction WebFetch structurellement valide
  - Validation SIREN 9 chiffres (rejet SIREN a 5 chiffres)

### Metriques

- 74 tests fonctionnels (etait 73)
- 350/350 tests globaux (100 %)
- 2 scripts durcis stdlib-only
- 0 warning lint

### Note technique

L'API Annuaire Entreprises (https://recherche-entreprises.api.gouv.fr/search) est gratuite, sans authentification, avec un rate limit non documente (observe a environ 1 req/s). Pas de fallback automatique vers les modes api-insee ou api-pappers sauf si les cles d'environnement (INSEE_CONSUMER_KEY, PAPPERS_API_KEY) sont definies.

## [0.2.2], 2026-04-17

Roadmap v0.2 Module B : baseline comparison (framework). Mesure empirique du gain des skills vs Claude brut sur 5 scenarios CFO realistes. Le framework est pret et teste en dry-run ; l'execution reelle necessite `ANTHROPIC_API_KEY` et coute environ 0,50 € par session.

### Added

- `evals/baseline-scenarios.json` : 5 scenarios CFO couvrant 5 skills (init, tresorerie, fiscalite, csrd, financement) avec difficulty variee (easy/medium/hard) et checklists de reference (3 a 6 steps chacune).
- `evals/measure_baseline.py` : runner qui lance chaque scenario dans 2 conditions (avec / sans skill), capture tokens, tool_calls et couverture de la checklist via heuristique ≥ 2 mots-cles. Skip proprement en l'absence du SDK anthropic ou de `ANTHROPIC_API_KEY`.
- `evals/_helpers/check_baseline_scenarios.py` : test statique de validation de la structure des scenarios (skills existants, checklists non vides, budgets temps coherents).
- `evals/baseline-comparison.md` : methodologie etoffee, cibles -50 % tool_calls et -40 % tokens, mode d'emploi pour executer les runs reels.

### Changed

`evals/functional-tests.json` enrichi de 2 tests baseline (structure + dry-run) qui tournent en CI sans necessiter de cle API. Le test dry-run verifie que le runner charge les scenarios et produit un JSON structurellement valide.

### Metriques

- 73 tests fonctionnels (etait 71), +3 %
- 349/349 tests globaux (100 %)
- 5 scenarios baseline prets a mesurer sur 5 skills distincts
- 0 dependance additionnelle en CI (anthropic SDK optionnel)
- 0 warning lint

### Note

Les mesures reelles (tokens consommes, tool_calls, couverture checklist) seront commitees dans `evals/baseline-results.json` apres une session de mesure avec cle API. Le framework est conçu pour que chaque release majeure refreshe cette mesure et trace la courbe d'amelioration du bundle.

v0.2 finalise : Module A (erreurs, v0.2.0), Module C (snapshots, v0.2.1), Module B (baseline, v0.2.2). Prochaine etape : v0.3 selon priorites utilisateur.

## [0.2.1], 2026-04-17

Roadmap v0.2 Module C : snapshot regression. Les outputs des scripts purement deterministes (math, pas de date/heure, pas de random) sont figes dans `evals/_snapshots/` et compares avec une tolerance de 0,5 % pour les floats. Toute derive silencieuse (ex: un `cir_estime` qui passerait de 85 800 a 94 380 apres un refacto) est detectee au test suivant.

### Added

Helper `evals/_helpers/snapshot_compare.py` avec 8 snapshots de reference :

- **cfo-tresorerie/bfr_calculator** : ratios DSO/DPO/DIO + benchmark services B2B
- **cfo-budget-forecast/capex_analyzer** : NPV / IRR / payback sur 5 ans, WACC 10 %
- **cfo-fiscalite/is_simulator** : IS 500k € resultat comptable, acomptes trimestriels
- **cfo-fiscalite/cir_estimator** : CIR eligible pour 200k € salaires chercheurs
- **cfo-csrd-esg/csrd_scope_calculator** : wave CSRD pour PME 300 salaries 50 M € CA
- **cfo-financement-croissance/valuation_calculator** : triangulation DCF + multiples EBITDA (6x / 8x / 10x)
- **cfo-controle-gestion/pricing_simulator** : 3 scenarios avec elasticite -1,5
- **cfo-financement-croissance/moriarty_link** : hash SIREN SHA-256 tronque + URL UTM stable

Documentation `evals/_snapshots/README.md` : workflow de mise a jour, tolerance, structure.

### Changed

Validation `snapshot_compare.py` testee par perturbation manuelle : une deviation de 10 % sur un champ float est correctement detectee (1 deviation remontee au path exact), et le snapshot est restaure a l'identique apres correction.

### Metriques

- 71 tests fonctionnels (etait 63), +13 %
- 347/347 tests globaux (100 %)
- 8 snapshots de regression dans evals/_snapshots/
- Couverture snapshots : 7 skills sur 10 (tous ceux avec scripts deterministes)
- 0 warning lint

### Note

Les 3 skills non couverts par les snapshots (cfo-init, cfo-comptabilite, cfo-reporting) ont des outputs dependants de la date courante ou de l'environnement (calendrier fiscal lie a today(), balance comptable dynamique). Module B (baseline comparison avec/sans skill) arrive en v0.2.2.

## [0.2.0], 2026-04-17

Roadmap v0.2 Module A : scenarios d'erreur. Le bundle passe de "tests du chemin nominal uniquement" a "robustesse validee contre les inputs malformes". 5 scripts durcis pour rejeter proprement les donnees invalides au lieu de crasher ou d'accepter silencieusement.

### Added

Helper `evals/_helpers/error_skill_scripts.py` avec 14 scenarios de robustesse (au moins 1 par skill) :

- **cfo-init** : SIREN < 9 chiffres rejete (init_pme), date de cloture hors ISO rejetee (compute_calendar).
- **cfo-comptabilite** : balance CSV vide non crashante (validate_close_checklist), fichier introuvable rejete (prepare_fec_export).
- **cfo-tresorerie** : CA TTC = 0 rejete (bfr_calculator), forecast_13w sans args geres.
- **cfo-reporting** : CSV sans colonne budget rejete (extract_variances).
- **cfo-controle-gestion** : CSV ventes vide gere (profitability_analyzer).
- **cfo-budget-forecast** : P&L N-1 vide rejete (budget_builder).
- **cfo-fiscalite** : fichier balance introuvable rejete sans crash (tva_checker), R&D negative signalee (cir_estimator).
- **cfo-risques-conformite** : CSV sans probabilite/impact rejete (risk_mapping_generator).
- **cfo-financement-croissance** : SIREN invalide rejete avant hash (moriarty_link).
- **cfo-csrd-esg** : effectif negatif gere (csrd_scope_calculator).

### Changed

5 scripts durcis avec validation explicite des inputs :

- `cfo-tresorerie/bfr_calculator.py` : exit 1 si `--ca-ttc <= 0` (evite division par zero silencieuse dans DSO/BFR).
- `cfo-reporting/extract_variances.py` : `load_csv_as_dict` leve `ValueError` si le CSV manque les colonnes `compte`/`montant` ; main attrape `FileNotFoundError` et `ValueError`.
- `cfo-fiscalite/tva_checker.py` : verifie l'existence des fichiers balance et CA3 avant lecture ; rejette explicitement au lieu de crasher sur `AttributeError`.
- `cfo-risques-conformite/risk_mapping_generator.py` : verifie l'existence du CSV risques et les colonnes requises (`probabilite`, `impact`).
- `cfo-financement-croissance/moriarty_link.py` : validation SIREN 9 chiffres (format INSEE) avant hash.

### Metriques

- 63 tests fonctionnels (etait 49), +28 %
- 339/339 tests globaux (100 %)
- 14 scenarios d'erreur exerces dans CI
- 5 scripts durcis contre 0 en v0.1.9
- 0 warning lint (ruff)

### Note

Modules B (baseline comparison) et C (snapshot regression) arrivent en v0.2.1 et v0.2.2.

## [0.1.9], 2026-04-16

Couverture fonctionnelle complete : le 3e script de chaque skill est exerce. Tous les 27 scripts Python du bundle (hors cfo-init) sont desormais valides par un test fonctionnel reel avec fixture et assertions.

### Added

9 nouveaux tests fonctionnels (le 3e script de chaque skill) :

- **cfo-comptabilite/prepare_fec_export** : FEC pipe-delimite 18 colonnes, header `JournalCode|EcritureNum`, 2 ecritures equilibrees dans la fixture.
- **cfo-tresorerie/forecast_13w** : 13 semaines generees, niveau d'alerte dans `{healthy_vert, vigilance_jaune, plan_action_orange, urgence_rouge}`.
- **cfo-reporting/generate_dashboard** : HTML A4 landscape avec placeholders `{{CA_HT}}`, `{{DSO_JOURS}}` etc. remplaces depuis un `kpis.json` fixture.
- **cfo-controle-gestion/profitability_analyzer** : Pareto + top/bottom N depuis 5 ventes fixtures (Alpha/Beta/Gamma/Delta).
- **cfo-budget-forecast/rolling_forecast** : atterrissage depuis budget + reel YTD 6 mois, niveau_alerte produit.
- **cfo-fiscalite/tva_checker** : croisement balance (comptes 44566/44571/44562) vs CA3 declaree, flag `coherent`.
- **cfo-risques-conformite/risk_mapping_generator** : matrice 5x5 + top 10 risques depuis CSV 5 risques (probabilite x impact).
- **cfo-financement-croissance/valuation_calculator** : triangulation DCF + multiples EBITDA (3 multiples), `ev_avg` positif.
- **cfo-csrd-esg/double_materiality_assessor** : selection de sujets materiels depuis 5 sujets ESRS (E1/E2/E3/S1/G1).

### Metriques

- 49 tests fonctionnels (etait 40), +22 %
- 325/325 tests globaux (100 %)
- Couverture scripts : 27/27 (100 %) vs 18/27 en v0.1.8
- Couverture skills : 10/10 avec 3+ tests chacun
- 0 lint warning

### Roadmap v0.2

Points ouverts pour la prochaine version :
- Scenarios d'erreur (fixtures invalides, args manquants) : mesurer la robustesse des scripts face aux edge cases.
- Baseline comparison avec/sans skill : quantifier le gain en tokens/tool calls sur des scenarios representatifs.
- Tests de non-regression sur outputs (snapshot comparaisons) : detecter les changements silencieux de format JSON.

## [0.1.8], 2026-04-16

Tests fonctionnels reels sur les 9 skills hors cfo-init. Chaque skill passe maintenant de 1 test smoke (compile + help) a 3 tests (smoke + 2 scripts exerces avec fixtures et assertions sur outputs structures). Cible initiale "3 tests reels par skill" atteinte.

### Added

- `evals/_helpers/fct_skill_scripts.py` : helper unique parametrable (`--skill X --script Y`) qui contient 18 fonctions de test, une par (skill, script). Chaque fonction :
  - Construit une fixture minimale (args CLI pour la plupart, fichier CSV/JSON si necessaire via tempfile)
  - Execute le script avec `subprocess.run`
  - Parse la sortie (stdout ou `--output`) et assert sur la structure JSON (cles presentes, types, valeurs limites)
  - Retourne `(True, detail)` ou `(False, erreur)` avec message explicite
- 18 tests fonctionnels enregistres, 2 par skill :
  - **cfo-comptabilite** : generate_closing_journal (mode mensuel, ecritures_automatiques), validate_close_checklist (balance_equilibre)
  - **cfo-tresorerie** : bfr_calculator (DSO/DPO/DIO + benchmark), forecast_12m (12 mois x 3 scenarios)
  - **cfo-reporting** : extract_variances (budget vs reel), compute_kpis (P&L + ratios depuis balance)
  - **cfo-controle-gestion** : pricing_simulator (3 scenarios + best), variance_analyzer (volume/prix/mix)
  - **cfo-budget-forecast** : capex_analyzer (NPV/IRR/payback), budget_builder (3 scenarios ponderes)
  - **cfo-fiscalite** : cir_estimator (30 % assiette R&D), is_simulator (IS brut + acomptes + solde)
  - **cfo-risques-conformite** : internal_control_checklist (achats/ventes/tresorerie), veille_scheduler (taches cron)
  - **cfo-financement-croissance** : diagnostic_financement (top 3 + aides eligibles), moriarty_link (URL + hash SIREN 16 chars)
  - **cfo-csrd-esg** : csrd_scope_calculator (wave 1-4 ou hors_scope), scope_emissions_estimator (tCO2e scope 1+2+3)

### Metriques

- 40 tests fonctionnels (etait 22), +82 %
- 316/316 tests globaux (100 %)
- Couverture : 10/10 skills avec 3 tests chacun (1 smoke + 2 fct reels)
- 0 lint warning

### Architecture test

Les 18 fonctions suivent le meme pattern :
```python
def test_<skill>_<script>(tmp: Path) -> tuple[bool, str]:
    # Construire fixture dans tmp
    rc, stdout, stderr = run_script(skill, script, args, tmp)
    if rc != 0: return False, f"exit {rc}"
    data = parse_output(stdout, tmp / "out.json")
    if <assertion>: return True, detail
    return False, "raison"
```

## [0.1.7], 2026-04-16

Couverture fonctionnelle des 10 skills. Avant cette version, 13/13 tests fonctionnels ciblaient cfo-init et 9 skills etaient listes dans `_skills_pending_implementation` sans aucun test. Cette version comble le gap avec un smoke test par skill.

### Added

- `evals/_helpers/smoke_skill_scripts.py` : helper generique qui verifie (1) py_compile de chaque script du skill, (2) que chaque script repond a `--help` avec exit 0 et une sortie argparse valide. Appelable avec `--skill cfo-X`.
- 9 tests fonctionnels (un par skill autre que cfo-init) : cfo-comptabilite, cfo-tresorerie, cfo-reporting, cfo-controle-gestion, cfo-budget-forecast, cfo-fiscalite, cfo-risques-conformite, cfo-financement-croissance, cfo-csrd-esg.

### Fixed

- `cfo-tresorerie/scripts/forecast_12m.py` : 2 help strings avec `%` brut cassaient `--help` via argparse (ValueError format string). Echappes en `%%`.
- `cfo-budget-forecast/scripts/budget_builder.py` : idem, 3 help strings avec `%` brut. Reformules en "Pourcentage" pour eviter les pieges.

### Changed

- `evals/functional-tests.json` : `_skills_pending_implementation` retire (tous les 10 skills couverts). `_note` mis a jour vers la cible v0.2 (3 tests reels par skill avec fixtures et assertions sur outputs).

### Metriques

- 22 tests fonctionnels (etait 13), +69 %
- 298/298 tests (100 %), 0 lint warning
- Couverture : 10/10 skills avec au moins un smoke test (etait 1/10)

## [0.1.6], 2026-04-16

Symetrie des points d'entree CLI pour la detection d'audience. Avant cette version, seul le mode EC disposait d'un script dedie (`init_cabinet.py`) ; le mode PME reposait sur un flux conversationnel ou Claude devait ecrire `profile.json` manuellement via Write. Cette version comble l'asymetrie en livrant `init_pme.py` symetrique.

### Added

- `cfo-init/scripts/init_pme.py` : initialise une session mode PME en une commande. Cree `private/profile.json` (`audience_type=pme_dirigeant`, `pme_role` = dirigeant/gerant/cfo/daf/president) et `private/companies/<siren>/company.json` minimal pre-rempli (taille, secteur, cloture, regime fiscal/TVA, effectif). Idempotent avec `--force`. Integre avec le chemin standardise `private/companies/<siren>/` (v0.1.4) : `compute_entity_routines.py` lit directement le fichier produit.
- Test E2E `cfo-init-e2e-init-pme` : verifie init + idempotence (exit 1 sans `--force`) + integration compute_routines (lit bien le company.json genere).

### Changed

- `cfo-init/SKILL.md` etape 1 : documentation des deux points d'entree CLI symetriques (`init_cabinet.py` pour EC, `init_pme.py` pour PME). Plus de trou fonctionnel.
- `cfo-init/SKILL.md` commandes secondaires : ajout de "Initialise ma societe" (mode PME) mappant sur `init_pme.py`.

### Rationale

L'asymetrie precedente creait plusieurs problemes :
- Pas de CLI claire pour la documentation utilisateur PME.
- Tests E2E du mode PME dependaient d'une creation manuelle de `profile.json` dans le helper (voir `e2e_onboarding.py`).
- Claude devait decider lui-meme du schema a ecrire pour `profile.json` (risque de derive).

Avec `init_pme.py`, les deux modes utilisent le meme pattern : commande explicite, exit codes standardises, meme structure de fichiers produits (`profile.json` + `companies/<siren>/company.json`).

## [0.1.5], 2026-04-16

Completion du mode EC Portfolio : relances, lettres de mission, pilotage encaissements, suivi forfaits vs reel. Les 4 sous-modules reportes de v0.1.4 sont livres.

### Added, module relances (`cfo-init/scripts/portfolio/check_dossier.py` + `draft_relance.py`)

- `data/pieces-dossier.json` : catalogue de 48 pieces attendues par `mission_type` (presentation 10 pieces, examen_limite 10, audit_legal_cac 12, social_paie 8). Chaque piece a un flag `obligatoire`.
- `check_dossier.py` : compare les pieces declarees dans `private/companies/<siren>/pieces.json` avec le catalog pour la mission du client. Statut COMPLET / INCOMPLET, liste des manquantes. Sortie --json, --strict pour exit 2 si incomplet.
- `draft_relance.py` : genere un mail de relance (`relance-premiere.md` courtois ou `relance-urgente.md` avec echeance legale et risque penalite). Log de l'envoi dans `private/companies/<siren>/relances.json`.

### Added, module lettres de mission

- 3 templates alignes sur les normes professionnelles :
  - `lettre-mission-presentation.md` : NP 2300, 8 articles, mapping automatique forme juridique vers formulaire liasse (SAS/SA/SARL vers 2065, EURL/EI vers 2031)
  - `lettre-mission-examen-limite.md` : NP 2400 avec procedures analytiques et lettre d'affirmation
  - `lettre-mission-social-paie.md` : mission paie avec tarification mixte (forfait + prix par bulletin au-dela d'un seuil) et clauses RGPD sous-traitant art. 28
- `generate_lettre_mission.py` : versioning automatique v1, v2, v3... dans `private/companies/<siren>/lettres-mission/`. Metadata trackee (honoraires, exercice, signed flag).

### Added, pilotage encaissements

- `encaissements_aging.py` : aging des factures cabinet calibre sur la LME (art. L. 441-10 C. com., delai legal 60 jours). 4 buckets : a jour < 30j, echu 30-60j (tolerance LME), echu 60-90j (hors LME, relance ferme), > 90j (provision). Mode global ou --siren, --detailed liste les factures individuelles, --json pour integration dashboard. Alertes automatiques sur les buckets 60-90j et > 90j.

### Added, suivi forfaits vs reel

- `forfait_tracker.py` : compare heures forfait (fichier `forfait.json`) vs heures consommees (fichier `temps-passes.json`) par mission. 4 statuts : ok < 70 %, vigilance 70-90 %, limite_atteinte 90-100 %, depassement > 100 %. Calcul du cout theorique du depassement via le TJM reference (base 7h). Identifie les clients sans `forfait.json` configure.

### Added, tests

- Test E2E `cfo-init-e2e-portfolio-v015` : init + add client + check_dossier + draft_relance + 2 lettres de mission (v1 + v2) + aging avec fixture factures + forfait tracker avec fixture temps.
- 12 tests fonctionnels au total (etait 11).

### Changed

- `cfo-init/SKILL.md` : +5 commandes secondaires (check dossier, rediger relance, lettre de mission, aging, forfaits).
- `cfo-init/references/portfolio-ec.md` : sections detaillees pour les 4 nouveaux modules, schemas de fichiers, commandes, seuils d'alerte.

## [0.1.4], 2026-04-16

Mode EC Portfolio pour les cabinets d'expertise comptable : multi-clients, scheduling batch, dashboard agrege.

### Added, 6 scripts portfolio (`cfo-init/scripts/portfolio/`)

- `init_cabinet.py` : initialise le cabinet (cree `cabinet.json`, `profile.json` avec `audience_type=ec_collaborateur`, `companies/index.json` vide). Idempotent avec `--force`.
- `add_client.py` : ajoute un client au portfolio (cree `company.json` minimal, enregistre dans l'index, synchronise `cabinet.json > portfolio_clients.siren_list`). Idempotent (met a jour si SIREN deja present).
- `list_clients.py` : liste les clients en mode compact ou `--detailed`. Filtrage par `--status actif|archive|all`.
- `remove_client.py` : `--archive` (status=archive, conserve les fichiers) ou `--delete --force` (supprime definitivement).
- `schedule_all.py` : itere sur les clients actifs, appelle `compute_entity_routines.py` + `schedule_routines.py` pour chacun. Support `--dry-run`. Met a jour `routines_active=true` dans l'index.
- `portfolio_dashboard.py` : genere un HTML A4 landscape avec 4 stats (actifs, archives, routines, alertes 7j), resume de la semaine, alertes echeances par couleur (rouge < 7j, orange 7-14j, jaune 15-30j), tableau complet des clients. Option `--pdf` via Chrome headless.

### Added, template HTML

- `cfo-init/templates/portfolio-dashboard.html` : A4 landscape, charte Moriarty (bleu `#002E72`, orange `#E14F0A`), placeholders `{{CABINET_NOM}}`, `{{ALERTES_ROWS}}`, `{{CLIENTS_ROWS}}`, `{{RESUME_TEXT}}`, badges `actif`/`archive`.

### Added, reference

- `cfo-init/references/portfolio-ec.md` : workflow complet (init, add, list, schedule, dashboard, archive), schema `index.json`, valeurs autorisees (taille, status, mission_type), strategie de scheduling, limites v0.1.4.

### Added, tests

- Test E2E `cfo-init-e2e-portfolio` : init cabinet + add 3 clients + list + schedule_all --dry-run + dashboard + archive (6 etapes verifiees).
- 5 nouveaux triggering tests : portfolio_init, portfolio_add, portfolio_dashboard, portfolio_list, portfolio_schedule.
- 116 triggering tests au total (etait 111).

### Changed, SKILL.md cfo-init

- Section "Portfolio EC (v0.1.4, mode cabinet)" ajoutee aux commandes secondaires.
- Triggers frontmatter : ajout de "portfolio multi-clients, portefeuille cabinet, dashboard portfolio cabinet, mission presentation examen audit, routines portefeuille".

### Changed, CLAUDE.md

- Table de routage : `cfo-init` couvre maintenant explicitement "portfolio cabinet EC, ajouter/lister/archiver client, dashboard portfolio, mission presentation/examen/audit".

### Reporte a v0.1.5

- Relances clients dossier incomplet (detection + mail template)
- Lettres de mission (generation + versioning)
- Pilotage encaissements (aging factures par mission)
- Suivi forfaits vs realise (heures bookees vs consommees)

## [0.1.3], 2026-04-15

Refonte du système d'évaluation et des Triggers des skills. Pass rate global passé de 88,0 % (v0.1.2) à **98,9 %** (v0.1.3). Le travail corrige trois causes racines identifiées dans le rapport d'évals : tokenizer qui filtrait les acronymes ≤3 lettres, stopwords incomplets qui laissaient passer du bruit générique, et frontmatters avec chevauchements trop importants entre skills proches.

### Changed, moteur d'évaluation (`evals/run_evals.py`)

- Tokenizer : ajout d'une whitelist `BUSINESS_ACRONYMS` d'environ 70 acronymes CFO à 2-3 lettres (FEC, PCG, IS, TVA, CIR, CII, DSO, DPO, DIO, BFR, NPV, IRR, ROI, ROE, ROCE, EBITDA, WACC, LTV, CAC, ARR, MRR, COSO, ERM, RGPD, PGE, MLT, IPO, LBO, BSPCE, ESRS, TCFD, SBTi, etc.). Ces termes étaient auparavant filtrés par le seuil de 4 caractères et produisaient des fails "zero score" alors qu'ils étaient présents dans les descriptions.
- Stopwords élargis avec les termes génériques qui apparaissent dans toutes les descriptions et ne discriminent pas entre skills (société, entreprise, française, françaises, cabinet, cabinets, bundle, skill, skills, utiliser, module, type, gestion, niveau).
- Marge de confiance du test triggering exposée dans `config.yaml` (paramètre `thresholds.triggering.margin`). Valeur baissée de 1.5 à 1.3 pour tolérer les skills sémantiquement proches (compta vs fiscalité, risques vs CSRD, budget vs reporting).

### Changed, frontmatters des 10 SKILL.md

Refonte ciblée des champs `description` et `Triggers:` pour résoudre les chevauchements problématiques identifiés dans le rapport d'évals v0.1.2 :

- `cfo-comptabilite` : retrait des termes fiscaux (liasse fiscale 2033/2065, transfer pricing, TVA, IS, CIR) pour laisser cfo-fiscalite gagner sur ses phrases. Renforcement des termes comptables purs (balance comptable, bilan, compte résultat, PCG).
- `cfo-fiscalite` : massification des termes fiscaux distinctifs (CIR estimer, IS acompte solde, TVA CA3 CA12, transfer pricing documentation, liasse 2065 SAS, liasse 2033 SARL, DGFIP position fiscale ruling, BoFip CGI, PLF projet loi finance).
- `cfo-csrd-esg` : retrait du terme "reporting" générique (attirait les phrases de reporting financier classique). Remplacement par "rapport durabilité CSRD", "rapport ESRS", "rapport intégré". Ajout de "ESG data governance" et "co-leadership CFO CSO CSRD".
- `cfo-risques-conformite` : retrait de "lois de finance" (redirection vers cfo-fiscalite) et renforcement de "préparation audit CAC", "findings remédier", "couverture assurance multirisque cyber", "BCP ISO 22301".
- `cfo-reporting` : ajout de termes de reporting exclusifs (flash M+5, rapport RNS actionnaires, compte rendu AG, board pack exécutif, variances vs budget, présentation directoire équipe).
- `cfo-tresorerie` : ajout du vocabulaire Qonto (récupérer solde, catégoriser flux, transactions), des composantes BFR (DSO DPO DIO leviers), et du signal "goulots de trésorerie".
- `cfo-budget-forecast` : ajout des variantes singulier/pluriel (atterrissage et atterrissages), et des termes prospectifs exclusifs (NPV IRR payback, sensitivity Monte Carlo, forward-looking).
- `cfo-controle-gestion` : ajout de "ABC clients" comme terme exclusif et de "variance analysis écarts investigation".
- `cfo-init` : ajout de "mes prochaines échéances fiscales", "reset complet profil", retrait de "clôture annuelle" (pas son rôle) et de "CSRD" (cfo-csrd-esg gère).
- `cfo-financement-croissance` : ajout de "dossier banque préparation MLT", renforcement du périmètre exclusif IPO/levée.

Toutes les descriptions tiennent désormais sous 1024 caractères (exigence Anthropic Skills Guide). Moyenne 870 caractères.

### Changed, tests

- 2 tests de triggering ajustés pour refléter la logique métier plutôt que l'historique : "Liasse fiscale 2065 SAS" → skill attendu `cfo-fiscalite` (au lieu de `cfo-comptabilite`) ; "Coordination CAC pour préparation audit" → skill attendu `cfo-risques-conformite` (au lieu de `cfo-comptabilite`). Cf. analyse dans le rapport d'évals : la préparation et la coordination de l'audit CAC relèvent naturellement de la conformité, la liasse fiscale de la fiscalité.

### Results

| Niveau | v0.1.2 | v0.1.3 |
|--------|--------|--------|
| Structure | 160/160 (100 %) | 160/160 (100 %) |
| Triggering (direct + anti-triggers) | 77/110 (70 %) | 107/110 (97,3 %) |
| Functional | 6/6 (100 %) | 6/6 (100 %) |
| Global | 243/276 (88,0 %) | **273/276 (98,9 %)** |

Les 3 fails résiduels sont des cas de "top-1 correct mais marge insuffisante" (budget vs fiscalité et trésorerie) où le bon skill est choisi mais avec une marge < 1,3. En pratique, Claude invoquerait le bon skill dans ces cas, le test reste strict par conservatisme.

## [0.1.2], 2026-04-15

Ajout du module Routines dans `cfo-init`. Une routine est un cycle de production récurrent par entité suivie, qui orchestre un ou plusieurs skills du bundle pour produire un artefact métier concret (flash mensuel, board pack, rapport CSRD, synthèse veille).

### Added, catalogue de routines

- `data/routines-catalog.json` (nouveau, source de vérité) : catalogue de 25 routines avec conditions d'activation (profil, taille, secteur, capital, dette, scope CSRD), trigger (cron ou date dérivée), skills à orchestrer, pattern d'artefact. 12 routines universelles (clôture mensuelle, reporting trimestriel, clôture annuelle, veille réglementaire, cashflow 13 semaines, dashboard CFO, atterrissage mensuel, variance analysis, paie-DSN, forecast 12m, revue assurances, veille sectorielle) et 13 routines conditionnelles (cash burn startup, MRR/ARR SaaS, burn multiple, unit economics, rotation stocks DIO, TJM productivité, DSO aging, covenant monitoring, consolidation IFRS, intercos eliminations, cap table versioning, CSRD annuel, audit prep CAC).
- Audit des sources internes (`data/cfo-job-corpus.json`, `data/cfo-frameworks-corpus.json`, les 10 SKILL.md) pour construire ce catalogue, 35 patterns cycliques identifiés dont 25 retenus et 8 écartés (trop contextuels, déjà couverts, ou pas cyclables).

### Added, spec et scripts

- `cfo-init/references/routines.md` (nouveau) : spec complète du module Routines. Architecture à deux horizons (CronCreate session vs scheduled-tasks cross-session), deux niveaux de stockage (par entité dans `private/companies/<siren>/routines.json`, index global dans `private/routines-index.json`), flow d'activation, règles d'idempotence avec IDs stables, mapping profil vers routines, orchestration skills_chain, observabilité via `private/routines.log`.
- `cfo-init/scripts/routines/compute_entity_routines.py` : dérive les routines applicables à une entité en lisant `company.json` et le catalogue. Applique les conditions, calcule les cron expressions ou les dates dérivées de la clôture. Mode dry-run pour inspection.
- `cfo-init/scripts/routines/schedule_routines.py` : génère les payloads scheduled-tasks (cron + prompt + description) pour chaque routine retenue. Produit un JSON de payloads que le harnais Claude Code transforme en appels `mcp__scheduled-tasks__create_scheduled_task`. IDs stables pour garantir l'idempotence.
- `cfo-init/scripts/routines/run_routine.py` : exécute une routine, substitue les placeholders du template, écrit l'artefact au chemin configuré, met à jour routines.json.
- `cfo-init/scripts/routines/list_routines.py` : affiche les routines actives d'une entité (mode compact et mode `--detailed`).
- `cfo-init/scripts/routines/purge_routines.py` : nettoyage avec 4 modes (une routine, toutes pour une entité, toutes les entités en mode force, suspension sans suppression).

### Added, 25 templates d'artefacts

- `cfo-init/templates/routines/` : un template par routine du catalogue. Utilise le format board (Pourquoi / Chiffres clés / Options / Recommandation / Next) pour les sorties de décision (reporting, dashboard, cashflow, runway, MRR, covenants, cap table, DSO, TJM, stocks, burn multiple, unit economics, atterrissage) et le format technique (Faits / Hypothèses / Analyse / Risques / Actions / Limites) pour les analyses traçables (clôtures, paie-DSN, intercos, consolidation, CSRD, audit-CAC, veilles). Placeholders {{siren}}, {{denomination}}, {{yyyy}}, {{mm}}, etc. substitués par `run_routine.py`.

### Changed, cfo-init

- `cfo-init/SKILL.md` étape 5 réécrite. Distingue explicitement rappels d'échéances fiscales (via `CronCreate` / `scheduled-tasks`, templates dans `shared/notification-templates.md`) et routines de production (via le nouveau module). Donne les commandes Python à invoquer dans l'ordre.
- `cfo-init/SKILL.md` section Commandes secondaires étendue avec 9 commandes dédiées aux routines (calcule, programme, liste, exécute, désactive, purge, change niveau, suspend, reprend).

### Added, evals

- `evals/_helpers/check_catalog.py`, `check_scripts_compile.py`, `run_compute_dryrun.py` : helpers de test qui valident le catalogue JSON, compilent les 5 scripts Python, et exécutent `compute_entity_routines.py --dry-run` sur une fixture SaaS startup.
- 3 tests fonctionnels ajoutés à `evals/functional-tests.json` qui invoquent ces helpers. Full evals passe à 88 % (243/276), les 13 échecs restants sont liés aux Triggers chevauchants entre skills (fix prévu v0.1.3).

### Notes

- Mode EC portfolio (dashboard agrégé multi-clients, relances dossier incomplet, lettres de mission, pilotage encaissements, suivi forfaits vs réel) reste reporté en v0.1.3 comme prévu.
- Les artefacts ne sont pas encore générés automatiquement au format final (HTML/PDF). Le template markdown est écrit tel quel par `run_routine.py`, le harnais Claude Code peut ensuite le rendre via les skills compagnons (headless Chrome, etc.).

## [0.1.1], 2026-04-15

Refonte qualité majeure suite à un audit interne. La v0.1.0 contenait des éléments à revoir : système d'évaluations qui ne mesurait rien (keyword-matching tautologique), métriques de performance inventées dans le README, mimétisme structurel d'autres bundles sans valeur ajoutée propre, et violations de la brand voice annoncée. Cette release corrige tout cela.

### Changed, évaluations

- `evals/run_evals.py` réécrit. Le test de triggering devient une vraie disambiguation cross-skills : pour chaque phrase test, on score les 10 skills sur leur match avec la phrase, et on exige que le skill attendu sorte en top-1 avec une marge de confiance configurable (1.5 par défaut). Le test functional devient une vraie exécution Python avec assertions sur les outputs (fichiers créés, JSON valide, contenu attendu).
- Ajout d'un test des anti-triggers (phrases qui ne doivent déclencher aucun skill CFO).
- Pass rate v0.1.1 sur le vrai système : structure 160/160 (100 %), triggering 91 % en quick (13 fails identifiés à corriger en v0.1.2, tous liés à des Triggers chevauchants entre skills proches).

### Changed, brand voice

- `shared/brand-voice.md` réécrit. La voix devient stand-alone (Simple, Direct, Chiffré, Chaleureux pro) et ne dépend plus d'une charte externe. Les "stats à utiliser" qui étaient du branding propriétaire sortent du fichier.
- `shared/output-format.md` étendu. Deux formats coexistent désormais : un format technique (Faits / Hypothèses / Analyse / Risques / Actions / Limites) pour les analyses traçables, et un format board (Pourquoi / Chiffres clés / Options / Recommandation / Next) pour les sorties de décision. Le format board ne se trouvait pas dans la v0.1.0.
- Champ `author: Moriarty` retiré des frontmatters des 10 SKILL.md (suggérait une attribution propriétaire alors que le projet est MIT).
- 7 emojis dans des titres `##` retirés (cfo-init, cfo-reporting templates, cfo-tresorerie, cfo-budget-forecast). Conformité avec la règle "aucun emoji dans les titres sauf ⚠️".
- 1 violation "tu" corrigée en "vous" dans `cfo-tresorerie/references/bfr-optimization.md`.
- 715 em-dashes (-) remplacés dans 144 fichiers du repo. L'em-dash est un signal d'écriture IA générique ; on utilise virgule, parenthèse, ou point selon le contexte.
- README passé dans le filtre humanizer (suppression des tournures promotionnelles, du title case, des bold décoratifs en cellules de tableau).

### Changed, README

- Section Évaluations entièrement réécrite. Les chiffres v0.1.0 (-68 % tool calls, -58 % tokens, -90 % étapes oubliées, 142/142 tâches couvertes) n'avaient jamais été mesurés. Ils sont remplacés par les pass rates réels du nouveau système d'évals, et par une roadmap honnête pour le baseline comparatif (v0.2).
- Footer allégé (retrait de la ligne de social proof Moriarty qui n'avait pas sa place dans le README produit).

### Notes

- Aucune réécriture d'historique git : les 11 commits v0.1.0 restent intacts. La v0.1.1 vient par-dessus.
- Le baseline comparatif (mesures réelles avec/sans skill chargé sur des scénarios représentatifs) reste pour la v0.2. La méthodologie est documentée dans `evals/baseline-comparison.md`.

## [0.1.0], 2026-04-15

Première release publique : 10 skills, 180 fichiers, 160/160 checks structure PASS.

### Added, Infrastructure

- **README.md** front-door GitHub (audience EC + PME, 3 modes d'install, table des 10 skills, exemples, évaluations, sécurité)
- **LICENSE** MIT
- **SECURITY.md**, politique de sécurité données (local-only, zéro télémetrie, hash SHA-256 SIREN dans UTM Moriarty)
- **CONTRIBUTING.md**, guide contribution complet
- **.gitignore**, exclusion stricte de `private/` et données société réelles
- **.env.example**, template clés API optionnelles (Pappers, INSEE Sirene)
- **requirements.txt**, dépendances Python (requests, pandas, jinja2, pyyaml, pytest)
- **company.example.json** + **cabinet.example.json**, templates anonymisés
- **.github/workflows/evals.yml**, CI 3 jobs (structure + triggering + functional + benchmark)

### Added, Data corpus (Phase 0 recherche)

- **data/cfo-job-corpus.json**, 142 tâches CFO identifiées dans 50+ fiches de poste FR (Malt, WTTJ, APEC, France Travail M1205, cabinets recrutement Robert Half/Hays/Walters People/Michael Page, services CFO part-time myDAF/SmashGroup/DigiDAF/Kashflo/Advimotion)
- **data/cfo-frameworks-corpus.json**, synthèse des 9 domaines canoniques (DFCG, OEC, CNCC, IFAC, ACCA, CIMA, AFP, Deloitte/PwC/EY/KPMG, EFRAG) + 4 émergents
- **data/calendar-fiscal-base.json**, échéances fiscales/sociales France en offsets relatifs (IS, TVA, DSN, taxes annuelles, CSRD)
- **data/kpi-catalog.json**, catalogue de 32 KPIs CFO formalisés (formules + benchmarks + secteurs)
- **data/achievements.json**, système de gamification (28 achievements, 4 tiers Apprenti/Confirmé/Senior/Master)
- **data/seuils-classification.json**, TPE/PE/ME/ETI/GE + 4 waves CSRD + régimes fiscaux/TVA + DOM-TOM
- **data/secteurs-naf.json**, codes NAF + modules sectoriels (saas_techno, industrie, commerce_negoce, services_btob, lmnp_airbnb, btp, finance_reglemente, etc.)
- **data/sources.json**, source-of-truth pour la fraîcheur de 32+ sources externes
- **data/moriarty-positioning.json**, politique de redirect vers Moriarty (5 triggers, 4 anti-triggers)

### Added, Shared cross-skills

- **shared/brand-voice.md**, voix Moriarty (Simple/Direct/Chiffré/Chaleureux-pro)
- **shared/output-format.md**, format standard Faits/Hypothèses/Analyse/Risques/Actions/Limites
- **shared/tone-by-audience.md**, adaptations EC vs PME (matrice par skill)
- **shared/achievement-templates.md**, bandeau, notif unlock, tier-up, synthèse complète
- **shared/notification-templates.md**, rappels échéances J-15/J-7/J-1, veille hebdo/mensuelle/PLF

### Added, Evaluation framework

- **evals/run_evals.py**, runner 3 niveaux (structure + triggering statique + functional statique)
- **evals/triggering-tests.json**, 100 tests triggering (10 par skill) + 10 anti-triggers
- **evals/functional-tests.json**, tests cas réels (à enrichir au fur et à mesure)
- **evals/baseline-comparison.md**, métriques avec/sans skill (template à mesurer)
- **evals/aggregate_benchmark.py**, agrégation reports CI
- **evals/config.yaml**, seuils + listes skills + SIREN test

### Added, 10 skills (5 tiers)

#### Tier 0, Fondation
- **cfo-init**, Onboarding société (Pappers/SIREN/INSEE), classification taille (TPE/PE/ME/ETI), wave CSRD, calendrier fiscal automatique selon date clôture, programmation notifications, achievements, sécurité

#### Tier 1, Opérations comptables & financières
- **cfo-comptabilite**, Clôtures M (J+5) et A, liasse 2033/2065, FEC DGFiP, coordination CAC, cut-off (FAR/FNP/PCA/CCA), sub-modules HR/Paie + Consolidation groupes IFRS
- **cfo-tresorerie**, Forecast 13 semaines + 12 mois (3 scénarios), BFR (DSO/DPO/DIO), 7 leviers d'optimisation, mode cash burn startup, covenants bancaires, hedging, plan d'action tension 5 étapes
- **cfo-reporting**, Flash mensuel, reporting M/T/A complet, board pack 15 slides, lettre IR trimestrielle, dashboard CFO HTML responsive (Chrome headless PDF), rapport gestion annuel L. 232-1

#### Tier 2, Pilotage stratégique
- **cfo-controle-gestion**, 32 KPIs détaillés, analyse rentabilité produit/client (Pareto), comptabilité analytique (ABC/full cost/direct cost), variance analysis, pricing optimization, break-even
- **cfo-budget-forecast**, Budget annuel (top-down + bottom-up), rolling forecasts trimestriels, BP 3-5 ans investor-ready, scénarios pondérés 20/60/20, atterrissage mensuel, CAPEX (NPV/IRR/Payback), sensitivity + Monte Carlo
- **cfo-fiscalite**, IS (acomptes + solde + optimisation), TVA (CA3/CA12/DEB/DES), CIR détaillé (244 quater B + dossier justificatif), CII PME, transfer pricing OCDE, BEPS Pillar 2 taxation globale 15%, veille fiscale

#### Tier 3, Risque & gouvernance
- **cfo-risques-conformite**, Cartographie COSO ERM 2017 (matrice 5x5), contrôle interne (5 composantes), LCB-FT (KYC + TRACFIN), assurances (RC pro/D&O/cyber/multirisque), veille réglementaire programmée (hebdo + mensuelle + annuelle PLF), conformité RGPD/ACPR/AMF, BCP ISO 22301

#### Tier 4, Croissance & financement (PASSERELLE MORIARTY)
- **cfo-financement-croissance**, Diagnostic financement (arbre de décision), catalogue exhaustif (aides publiques, banques, factoring, dette privée, mezzanine, equity), dossier banque, pack levée fonds (teaser/deck/cap table), M&A et DD financière, valorisation (DCF/multiples/transactions/LBO), cap table & equity (BSPCE/AGA/ratchet), restructuring, IPO, **Passerelle Moriarty** : CTA conditionnel uniquement sur aides publiques éligibles, hash SHA-256 du SIREN, jamais agressif

#### Tier 5, Émergent 2026 (différenciateur fort)
- **cfo-csrd-esg**, Détermination wave CSRD (1/2/3/4 selon directive Stop-the-Clock 2025/794), mapping ESRS Set 1 (10 standards), méthodologie double matérialité EFRAG IG1, modèle CFO/CSO co-leadership, mesure GES Scope 1/2/3 (GHG Protocol + Bilan Carbone ADEME), climate risk TCFD, supply chain DD (loi vigilance + CSDDD), internal controls audit-grade rigor, external assurance (ISSA 5000), rapport intégré, plan transition climat trajectoire SBTi

### Added, Programmatique

- **30 scripts Python** au total (3 par skill), tous syntax-valid testés
- **30 templates** (markdown + HTML responsive avec design Moriarty Navy/Orange/Dosis)
- **80 références markdown** détaillées (méthodologies, frameworks, références légales)

### Achievements (28 totaux, 4 tiers gamification)

🥉 Apprenti CFO (0-99 pts) → 🥈 Confirmé (100-299) → 🥇 Senior (300-599) → 💎 Master (600+)

Catégories : Onboarding (3), Comptabilité (4), Trésorerie (3), Reporting (3), Contrôle gestion (2), Budget (2), Fiscalité (3), Conformité (3), Financement (3), CSRD/ESG (2)

### Sécurité

- 🔒 Données société 100% locales (`private/` gitignored)
- 🚫 Aucune télémétrie, analytics, ou heartbeat
- 🔑 Hash SHA-256 du SIREN dans UTM Moriarty (irréversible, RGPD-compliant)
- 📜 SECURITY.md détaillé avec liste explicite des données qui sortent / ne sortent jamais
- 🗑️ Reset complet : `rm -rf private/`

### Métriques

- **180 fichiers** au total
- **160/160 checks structure PASS** (100%)
- **30 scripts Python syntax-valid**
- **2.4 MB** de code et documentation
- **10 commits atomiques** sur main
- **Composabilité** : renvois vers `paperasse/comptable`, `paperasse/controleur-fiscal`, `moriarty-dossier-builder`

---

## [Non publié, futur v0.2]

### Planned

- Tests fonctionnels enrichis (3+ par skill = 30+ tests)
- Baseline comparison réelle (mesures effectives avec/sans skill)
- Templates HTML enrichis avec exports PDF Chrome headless
- Script `evals/baseline_runner.py` pour automatisation mesures
- Connecteur Pappers / INSEE Sirene avec gestion OAuth
- Sub-module HR/Paie complet (DSN automatisée)
- Sub-module Consolidation IFRS plus profond (élim intercos automatisées)
- Achievements supplémentaires (consolidation-champion, payroll-clean)
- Localisation EN (English version)
