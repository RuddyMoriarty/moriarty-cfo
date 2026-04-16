# CLAUDE.md, moriarty-cfo

Contexte repo destiné à Claude Code et à toute instance Claude qui intervient dans ce projet. Concentré court, factuel, sans redondance avec README.md.

## Nature du repo

Plugin bundle de 10 skills Claude pour CFO/DAF français. Deux audiences : dirigeant PME/TPE, collaborateur de cabinet d'expertise comptable. Python stdlib only pour les scripts, markdown pour les templates, pas de framework applicatif. Chaque sous-dossier `cfo-*` est un skill autonome au format Anthropic Skills Guide.

## Health Stack

```
typecheck: python -m py_compile (wrapper maison, pas de mypy pour l'instant)
lint: ruff check . (config pyproject.toml, line-length 120, ignore E501)
tests: python evals/run_evals.py --full
```

Pas de shell lint (0 `.sh`). Pas de knip (pas de JS/TS).

## Commandes standard

```
python evals/run_evals.py --quick    # Structure + triggering rapide (30 s)
python evals/run_evals.py --full     # Tout (8 s)
python evals/run_evals.py --skill X  # Filtre sur un skill

ruff check .                          # Lint
ruff format .                         # Format (si souhaité)
python -m py_compile <fichier.py>    # Syntax check
```

## Structure

```
cfo-<nom>/
├── SKILL.md              (frontmatter YAML + workflow)
├── references/           (docs détaillées, progressive disclosure)
├── scripts/              (code exécutable Python stdlib)
└── templates/            (HTML, MD, JSON)

data/                     (JSON mutualisés : catalogue routines, KPIs, calendrier fiscal)
shared/                   (brand-voice, output-format, tone-by-audience)
evals/                    (run_evals.py + triggering-tests.json + functional-tests.json)
private/                  (local-only, gitignored, profils société et tâches programmées)
```

## Conventions d'écriture

Voir [`shared/brand-voice.md`](shared/brand-voice.md) pour le détail. Résumé :

- Pas d'em-dash (—). Virgule, parenthèse, ou point.
- Aucun emoji dans les titres `##` ou `###` sauf `⚠️` structurant.
- `vous` pour l'utilisateur, jamais `tu`. `on` pour le bundle quand il se réfère à lui-même.
- Chiffres précis plutôt que `beaucoup`/`plusieurs`/`significatif`.
- Ne pas écrire de `Co-Authored-By: Claude` dans les commits (politique projet).
- Pas de mention `Moriarty` hors `cfo-financement-croissance/` (passerelle business) et hors `LICENSE`/`SECURITY.md`/footer README.

## Deux formats de sortie

Coexistent dans le bundle. Voir [`shared/output-format.md`](shared/output-format.md) :

- Format technique (6 sections : Faits / Hypothèses / Analyse / Risques / Actions / Limites) pour les analyses traçables (clôture, fiscalité, conformité).
- Format board (5 sections : Pourquoi / Chiffres clés / Options / Recommandation / Next) pour les sorties de décision (reporting, budget, financement).

## Versionnage

Semantic Versioning. CHANGELOG.md maintenu à la main, pas auto-généré. Tags git `vX.Y.Z`. Pas de release notes séparées : le CHANGELOG suffit.

## CI

`.github/workflows/evals.yml`. Trois jobs :
- `triggering-tests` sur PR et push main (rapide, ~3 min)
- `functional-tests` sur PR et push main
- `full-suite` uniquement sur push main (full + benchmark artifact)

Permissions restreintes : `contents: read` uniquement.

## Module Routines (depuis v0.1.2)

Une routine = cycle de production récurrent par entité suivie (clôture mensuelle, reporting trimestriel, veille réglementaire, etc.). 25 routines au catalogue `data/routines-catalog.json`.

Scripts dans `cfo-init/scripts/routines/` :
- `compute_entity_routines.py` : dérive les routines applicables selon profil
- `schedule_routines.py` : génère les payloads scheduled-tasks
- `run_routine.py` : exécute une routine (substitue placeholders, écrit l'artefact)
- `list_routines.py` : affiche les routines actives
- `purge_routines.py` : cleanup

Tasks programmées via `mcp__scheduled-tasks__create_scheduled_task` (persistant cross-session) ou `CronCreate` (one-shot intra-session).

## Données sensibles

Tout ce qui concerne la société de l'utilisateur (CA, effectif, marges, contrats) vit dans `private/` (gitignored). Jamais en dur dans un skill. Pas de télémétrie, pas d'analytics. Voir [`SECURITY.md`](SECURITY.md).

## Skills compagnons supportés

- `paperasse/comptable` et `paperasse/controleur-fiscal` (détail PCG, liasse fiscale)
- Connecteur Qonto MCP (pour `cfo-tresorerie`)
- API Pappers et INSEE Sirene V3 (optionnelles, fallback WebFetch)

## Skill routing

Quand l'utilisateur demande une tâche CFO/DAF, invoquer en priorité le skill `moriarty-cfo/cfo-init` pour initialiser la session, puis laisser Claude router vers le skill approprié selon la demande.

Table de correspondance intents vers skills :

- onboarding, SIREN, SIRET, Pappers, calendrier fiscal, echeances, classification taille, profil societe, achievements, reset → `cfo-init`
- cloture mensuelle/annuelle, FEC, export FEC, ecritures, cut-off, provisions, amortissements, paie, DSN, URSSAF, consolidation, IFRS, intercos, PCG, bilan, grand livre → `cfo-comptabilite`
- tresorerie, cash flow, BFR, DSO/DPO/DIO, covenants, burn/runway, Qonto, cash pooling, hedging, tension tresorerie → `cfo-tresorerie`
- reporting mensuel/trimestriel/annuel, board pack, dashboard CFO, lettre investisseurs, rapport AG, variances vs budget, flash mensuel → `cfo-reporting`
- KPI sectoriels, rentabilite, marges, comptabilite analytique, pricing, ABC, variance analysis, break-even, ROCE/ROE, benchmark → `cfo-controle-gestion`
- budget annuel, rolling forecast, plan strategique, scenarios, atterrissage/landing, CAPEX, ROI/IRR/NPV, sensitivity, business plan, reforecast → `cfo-budget-forecast`
- IS, TVA, CIR, CII, liasse fiscale, transfer pricing, DEB/DES, deductibilite, ruling DGFiP, veille loi de finance → `cfo-fiscalite`
- COSO, cartographie risques, preparation audit CAC, LCB-FT/TRACFIN, controle interne, BCP, findings, RGPD, assurances, veille reglementaire → `cfo-risques-conformite`
- financement, dossier banque, levee de fonds, valorisation DCF, due diligence financiere, M&A, cap table, BSPCE, aides publiques BPI, restructuring, IPO → `cfo-financement-croissance`
- CSRD, ESRS, double materialite, climat 1.5 degC, emissions scope, taxonomie verte, supply chain ESG, rapport durabilite, SBTi, Net-Zero → `cfo-csrd-esg`
