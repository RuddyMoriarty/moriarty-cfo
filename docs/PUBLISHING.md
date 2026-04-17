# Publication moriarty-cfo

Document de reference pour la soumission du bundle aux distributions publiques : Anthropic Skills Marketplace, registres de plugins Claude, referentiels sectoriels (DFCG, OEC, etc.).

## Etat actuel

- **GitHub public** : https://github.com/RuddyMoriarty/moriarty-cfo (v0.3.2 a l'heure actuelle)
- **Licence** : MIT
- **Releases taguees** : v0.1.0 a v0.3.2 (15 versions)
- **CI** : verte, 342 / 342 tests
- **Couverture** : 77.5 % sur 3608 lignes
- **Anthropic Skills Marketplace** : **non soumis** (specs marketplace en cours d'elaboration cote Anthropic)

## Manifest

Le fichier `plugin.json` a la racine decrit toutes les metadonnees du bundle. A tenir a jour a chaque release majeure :

- Bumper `version`
- Mettre a jour `quality.tests_total` et `quality.scripts_coverage_pct`
- Refresh `last_release`
- Verifier que les 10 skills declares sont toujours presents

## Ce qui est pret

- [x] README.md complet (installation, usage, exemples, composabilite, securite, contrib, licence, avertissement)
- [x] SECURITY.md avec politique de donnees + procedure de reset
- [x] CONTRIBUTING.md
- [x] CHANGELOG.md maintenu a la main (15 versions)
- [x] LICENSE (MIT)
- [x] 10 SKILL.md avec frontmatter YAML conforme au guide Anthropic
- [x] CLI unifiee `./cfo` avec 51 commandes
- [x] 2 guides POC client (`docs/POC-CLIENT-PME.md`, `docs/POC-CLIENT-EC.md`)
- [x] Snapshot coverage (`docs/coverage-snapshot.md`)
- [x] Release notes consolidees (`docs/release-notes-v0.2.2.md`)
- [x] `plugin.json` a la racine
- [x] install.sh une ligne
- [x] Evals CI automatiques sur PR + push main

## Ce qui reste pour la soumission finale

### Captures d'ecran (priorite 1)

Les 2 HTML de demonstration dans `docs/demo/` sont sauvegardes mais necessitent d'etre screenshotes en PNG pour l'affichage marketplace :

```bash
# Prerequis : Chrome ou Chromium installe
./cfo unified-dashboard --siren 552120222  # Genere l'HTML sample
./cfo portfolio-dashboard                   # Genere le dashboard portfolio
# Puis screenshoter via :
#   - Chrome headless : chrome --headless --screenshot ...
#   - Ou ouvrir dans le navigateur et Cmd+Shift+4 (macOS)
```

Placer les PNG dans `docs/demo/` en :

- `screenshot-unified-dashboard.png` (mode PME)
- `screenshot-portfolio-dashboard.png` (mode EC)
- `screenshot-cli-help.png` (sortie de `./cfo --help`)

### Video demo 2 minutes (priorite 2)

Scenario :

1. 10 s : intro slide moriarty-cfo
2. 30 s : `./cfo init-pme --fetch` + `./cfo calendar` + `./cfo bfr`
3. 30 s : `./cfo dashboard` ouverture dans navigateur
4. 30 s : mode EC, `./cfo init-cabinet` + 3 `portfolio-add` + `./cfo portfolio-dashboard`
5. 20 s : conclusion avec lien GitHub

Outils : asciinema pour le terminal, screen recorder pour l'HTML.

### Baseline comparison reelle (priorite 2)

`evals/measure_baseline.py` necessite `ANTHROPIC_API_KEY` et coute ~0,50 € par session. Executer une fois pour commiter `evals/baseline-results.json` avec les vraies mesures (-X % tokens, -Y % tool_calls). Argument commercial fort pour le marketplace.

### Anthropic Skills Marketplace

Les specs du marketplace sont en cours d'elaboration cote Anthropic. Dès qu'elles sont publiques :

1. Verifier que `plugin.json` respecte le schema attendu
2. Remplir le formulaire de soumission (URL GitHub, description, captures, categorie)
3. Repondre aux retours de review

En attendant, le bundle est distribue via :

- GitHub (clone + install.sh)
- Mention dans `moriarty-skills` README (repo Moriarty)
- Landing page Moriarty `https://themoriarty.fr/cfo-skill`

### Communication

- **LinkedIn** : post d'annonce Moriarty a la v0.3.2 ou v0.4 (chiffres cles : 10 skills, 51 commandes CLI, 342 tests, 77 % coverage, stdlib-only)
- **Reddit** : `r/france_tech`, `r/accounting_france`, `r/startups_fr` (pas d'autopromo, privilegier les threads ou le bundle repond a une question reelle)
- **Twitter / X** : compte Moriarty
- **Newsletter Moriarty** : si existante
- **Presse specialisee** : Capital, Les Echos, Maddyness, Frenchweb (email personalise au journaliste qui a couvert une sortie similaire recemment)
- **Forums comptables** : Compta Online, Apca, UNASA

## Quality gates

Avant toute soumission, verifier :

- [ ] `python3 evals/run_evals.py --full` retourne 100 %
- [ ] `python3 -m ruff check .` retourne 0 warning
- [ ] `python3 evals/run_coverage.py` retourne >= 75 %
- [ ] `./cfo --help` affiche toutes les 12 categories sans typo
- [ ] `./cfo --version` affiche la version du `pyproject.toml`
- [ ] `git status` est clean, pas de fichier prive qui traine
- [ ] `git log --oneline -5` montre des commits signifiants en francais
- [ ] Le tag correspondant a la version est pousse

## Suivi post-publication

Metriques a mesurer a 30 / 60 / 90 jours :

- Stars GitHub
- Clones / downloads
- Issues ouvertes + resolues
- Pull requests externes
- Mentions Reddit / LinkedIn / Twitter
- Clicks sur la passerelle Moriarty (via UTM hash)
- Conversions leads Moriarty

## Contact

ruddy@workcuts.fr pour toute question de publication ou de co-soumission.
