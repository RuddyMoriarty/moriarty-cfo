# Contribuer à moriarty-cfo

Merci de l'intérêt que vous portez à ce projet. `moriarty-cfo` est un plugin bundle Claude open-source destiné à la communauté finance française (PME/TPE et cabinets EC). Toutes les contributions sont les bienvenues.

## Avant de contribuer

1. **Ouvrez d'abord une issue** pour discuter du changement proposé. Cela évite des PR qui seraient refusées pour cause de désalignement.
2. **Lisez le plan d'architecture** dans le commit initial pour comprendre la vision.
3. **Respectez la voix Moriarty** documentée dans `shared/brand-voice.md`.
4. **Aucune donnée client ou société réelle** dans les exemples ou les tests : utilisez `552120222` (Carrefour, donnée publique) ou inventez un SIREN factice.

## Setup local

```bash
git clone https://github.com/moriarty-fr/moriarty-cfo.git
cd moriarty-cfo

# Optionnel : créer un .env avec vos clés API
cp .env.example .env
# Éditez .env si vous avez une clé Pappers / INSEE Sirene

# Installer les dépendances Python (pour les scripts + evals)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Symlink dans Claude Code (chemin user à adapter)
ln -s "$(pwd)" ~/.claude/skills/moriarty-cfo
```

Puis ouvrir Claude Code dans n'importe quel répertoire et tester :
```
> Lance cfo-init pour le SIREN 552120222
```

## Lancer les évaluations

```bash
# Tests rapides (triggering + 3 functional par skill)
python evals/run_evals.py --quick

# Suite complète (long, ~30min)
python evals/run_evals.py --full

# Un seul skill
python evals/run_evals.py --skill cfo-init
```

Les evals comparent les sorties contre les attendus dans `evals/triggering-tests.json` et `evals/functional-tests.json`. Avant toute PR, le score doit rester ≥ 90% sur la suite complète.

## Conventions de code

### Structure de dossier

Chaque skill doit suivre **strictement** :
```
cfo-<nom>/
├── SKILL.md                 # Frontmatter + workflow principal
├── references/              # Documentation détaillée
├── scripts/                 # Code exécutable Python/JS/Bash
└── templates/               # Templates HTML/MD/JSON
```

**Pas de README.md à l'intérieur d'un dossier de skill** (règle Anthropic, voir [Skills Guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)). La documentation visible des humains se concentre dans le `README.md` racine et les `references/*.md`.

### Frontmatter SKILL.md

- `name` : kebab-case, **commence par `cfo-`**, identique au nom du dossier
- `description` : moins de 1024 caractères, contient WHAT + WHEN + Triggers explicites (FR + EN)
- `metadata.last_updated` : date ISO (mise à jour à chaque PR substantielle)
- `metadata.version` : SemVer (bump patch à chaque PR mergée)
- `metadata.tier` : 0 à 5 selon la classification du plan
- `includes` : globs des dossiers à inclure
- `allowed-tools` : minimum nécessaire (principe de moindre privilège)
- `license` : MIT

### Format de sortie standard (cohérence cross-skills)

Toutes les analyses produites par les skills suivent le format de `shared/output-format.md` :
```
## Faits
[Données certaines + sources]

## Hypothèses
[Suppositions explicites à valider]

## Analyse
[Traitement métier]

## Risques
[Points d'attention]

## Actions
[Liste actionnable]

## Limites
[Quand consulter un pro]
```

### Sources et fraîcheur des données

Toute donnée externe citée doit figurer dans `data/sources.json` avec :
- URL canonique
- Date de dernière vérification
- Conditions d'usage (licence, ToS)
- Type (ouverte, API, scraping autorisé)

Avertissement automatique si une donnée a plus de 6 mois (logique calquée sur `paperasse/comptable`).

### Brand voice

Voir `shared/brand-voice.md`. En résumé :
- **Simple, direct, chiffré, chaleureux-pro**
- **"Vous"** pour l'utilisateur EC ou dirigeant. Jamais "tu".
- **"On"** pour Moriarty (jamais "nous")
- **Aucun emoji dans les titres** (sauf icônes structurantes type ⚠️)
- **Pas de jargon vide** ("solution innovante", "dans un monde…", etc.)
- **Chiffres précis** plutôt que "beaucoup"

## Workflow de PR

1. **Branche** depuis `main` : `feat/<skill>-<topic>`, `fix/<skill>-<bug>`, `docs/<topic>`
2. **Commit atomique** par changement logique (un commit = une chose). Format conventional commits :
   - `feat(cfo-tresorerie): add 12-month forecast template`
   - `fix(cfo-init): handle SIREN with leading zero`
   - `docs(README): update install steps`
3. **Tests passent en local** : `python evals/run_evals.py --quick`
4. **Pas de secret commité** : `git diff --staged | grep -i "api_key\|password\|token"` doit retourner vide
5. **`SECURITY.md` respecté** : aucune donnée société réelle dans la PR
6. **PR description** : lien vers l'issue, résumé du changement, captures si UI/HTML, justification si nouvelle dépendance
7. **CI verte** (GitHub Actions `evals.yml`) avant review

## Ajouter une nouvelle source de données

Si votre skill consomme une nouvelle source (par exemple un nouveau référentiel sectoriel) :

1. Ajoutez l'entrée dans `data/sources.json`
2. Documentez la source dans `cfo-<skill>/references/<source>.md`
3. Ajoutez la source à la section "Sources" du SKILL.md concerné
4. Vérifiez les conditions d'usage (ToS) et notez-les

## Licence des contributions

En contribuant, vous acceptez que votre contribution soit publiée sous **licence MIT** (cf. `LICENSE`). Aucune CLA additionnelle n'est requise.

## Questions

- 💬 Discussions : [GitHub Discussions](https://github.com/moriarty-fr/moriarty-cfo/discussions)
- 🐛 Bugs : [GitHub Issues](https://github.com/moriarty-fr/moriarty-cfo/issues)
- 🔒 Sécurité : `security@themoriarty.fr`

Merci pour votre contribution.

- L'équipe Moriarty
