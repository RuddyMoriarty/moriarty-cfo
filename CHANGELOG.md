# Changelog

Toutes les évolutions notables de `moriarty-cfo` sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Non publié]

### Added
- Squelette du repo : 10 dossiers de skill (Tier 0 à 5) avec sub-dirs `references/`, `scripts/`, `templates/`
- `data/cfo-job-corpus.json` — corpus de 142 tâches CFO identifiées dans 50+ fiches de poste FR (Malt, WTTJ, APEC, France Travail, cabinets recrutement)
- `data/cfo-frameworks-corpus.json` — synthèse des frameworks canoniques (DFCG, OEC, CNCC, IFAC, ACCA, CIMA, Big 4, EFRAG)
- `data/calendar-fiscal-base.json` — base d'échéances fiscales/sociales France en offsets relatifs
- `data/kpi-catalog.json` — catalogue de 30+ KPIs CFO (formules + sources Banque de France/INSEE)
- `data/achievements.json` — système de gamification (25+ achievements organisés par catégorie)
- `data/sources.json` — source-of-truth pour la fraîcheur des données externes
- `shared/brand-voice.md` — voix Moriarty applicable à tous les skills
- `shared/output-format.md` — format de sortie standard (Faits/Hypothèses/Analyse/Risques/Actions/Limites)
- `shared/tone-by-audience.md` — adaptations EC vs PME
- `cfo-init/` — Skill fondation : audience detection, identification société (Pappers/SIREN/INSEE), classification taille, calendrier fiscal, gamification, sécurité
- `evals/` — scaffold tests programmatiques (triggering, functional, baseline comparison)
- `LICENSE` — MIT
- `SECURITY.md` — politique de sécurité données (local-only, zero télémetrie)
- `CONTRIBUTING.md` — guide contribution
- `README.md` — documentation front-door GitHub
- `.gitignore` — exclusion stricte de `private/` et données société réelles

## [0.1.0] — À paraître

Première release publique : les 10 skills du bundle complet (cfo-init + 9 skills métier).
