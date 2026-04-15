# Changelog

Toutes les évolutions notables de `moriarty-cfo` sont documentées ici.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [0.1.0] — 2026-04-15

🎉 **Première release publique** : 10 skills, 180 fichiers, 160/160 checks structure PASS.

### Added — Infrastructure

- **README.md** front-door GitHub (audience EC + PME, 3 modes d'install, table des 10 skills, exemples, évaluations, sécurité)
- **LICENSE** MIT
- **SECURITY.md** — politique de sécurité données (local-only, zéro télémetrie, hash SHA-256 SIREN dans UTM Moriarty)
- **CONTRIBUTING.md** — guide contribution complet
- **.gitignore** — exclusion stricte de `private/` et données société réelles
- **.env.example** — template clés API optionnelles (Pappers, INSEE Sirene)
- **requirements.txt** — dépendances Python (requests, pandas, jinja2, pyyaml, pytest)
- **company.example.json** + **cabinet.example.json** — templates anonymisés
- **.github/workflows/evals.yml** — CI 3 jobs (structure + triggering + functional + benchmark)

### Added — Data corpus (Phase 0 recherche)

- **data/cfo-job-corpus.json** — 142 tâches CFO identifiées dans 50+ fiches de poste FR (Malt, WTTJ, APEC, France Travail M1205, cabinets recrutement Robert Half/Hays/Walters People/Michael Page, services CFO part-time myDAF/SmashGroup/DigiDAF/Kashflo/Advimotion)
- **data/cfo-frameworks-corpus.json** — synthèse des 9 domaines canoniques (DFCG, OEC, CNCC, IFAC, ACCA, CIMA, AFP, Deloitte/PwC/EY/KPMG, EFRAG) + 4 émergents
- **data/calendar-fiscal-base.json** — échéances fiscales/sociales France en offsets relatifs (IS, TVA, DSN, taxes annuelles, CSRD)
- **data/kpi-catalog.json** — catalogue de 32 KPIs CFO formalisés (formules + benchmarks + secteurs)
- **data/achievements.json** — système de gamification (28 achievements, 4 tiers Apprenti/Confirmé/Senior/Master)
- **data/seuils-classification.json** — TPE/PE/ME/ETI/GE + 4 waves CSRD + régimes fiscaux/TVA + DOM-TOM
- **data/secteurs-naf.json** — codes NAF + modules sectoriels (saas_techno, industrie, commerce_negoce, services_btob, lmnp_airbnb, btp, finance_reglemente, etc.)
- **data/sources.json** — source-of-truth pour la fraîcheur de 32+ sources externes
- **data/moriarty-positioning.json** — politique de redirect vers Moriarty (5 triggers, 4 anti-triggers)

### Added — Shared cross-skills

- **shared/brand-voice.md** — voix Moriarty (Simple/Direct/Chiffré/Chaleureux-pro)
- **shared/output-format.md** — format standard Faits/Hypothèses/Analyse/Risques/Actions/Limites
- **shared/tone-by-audience.md** — adaptations EC vs PME (matrice par skill)
- **shared/achievement-templates.md** — bandeau, notif unlock, tier-up, synthèse complète
- **shared/notification-templates.md** — rappels échéances J-15/J-7/J-1, veille hebdo/mensuelle/PLF

### Added — Evaluation framework

- **evals/run_evals.py** — runner 3 niveaux (structure + triggering statique + functional statique)
- **evals/triggering-tests.json** — 100 tests triggering (10 par skill) + 10 anti-triggers
- **evals/functional-tests.json** — tests cas réels (à enrichir au fur et à mesure)
- **evals/baseline-comparison.md** — métriques avec/sans skill (template à mesurer)
- **evals/aggregate_benchmark.py** — agrégation reports CI
- **evals/config.yaml** — seuils + listes skills + SIREN test

### Added — 10 skills (5 tiers)

#### Tier 0 — Fondation
- **cfo-init** — Onboarding société (Pappers/SIREN/INSEE), classification taille (TPE/PE/ME/ETI), wave CSRD, calendrier fiscal automatique selon date clôture, programmation notifications, achievements, sécurité

#### Tier 1 — Opérations comptables & financières
- **cfo-comptabilite** — Clôtures M (J+5) et A, liasse 2033/2065, FEC DGFiP, coordination CAC, cut-off (FAR/FNP/PCA/CCA), sub-modules HR/Paie + Consolidation groupes IFRS
- **cfo-tresorerie** — Forecast 13 semaines + 12 mois (3 scénarios), BFR (DSO/DPO/DIO), 7 leviers d'optimisation, mode cash burn startup, covenants bancaires, hedging, plan d'action tension 5 étapes
- **cfo-reporting** — Flash mensuel, reporting M/T/A complet, board pack 15 slides, lettre IR trimestrielle, dashboard CFO HTML responsive (Chrome headless PDF), rapport gestion annuel L. 232-1

#### Tier 2 — Pilotage stratégique
- **cfo-controle-gestion** — 32 KPIs détaillés, analyse rentabilité produit/client (Pareto), comptabilité analytique (ABC/full cost/direct cost), variance analysis, pricing optimization, break-even
- **cfo-budget-forecast** — Budget annuel (top-down + bottom-up), rolling forecasts trimestriels, BP 3-5 ans investor-ready, scénarios pondérés 20/60/20, atterrissage mensuel, CAPEX (NPV/IRR/Payback), sensitivity + Monte Carlo
- **cfo-fiscalite** — IS (acomptes + solde + optimisation), TVA (CA3/CA12/DEB/DES), CIR détaillé (244 quater B + dossier justificatif), CII PME, transfer pricing OCDE, BEPS Pillar 2 taxation globale 15%, veille fiscale

#### Tier 3 — Risque & gouvernance
- **cfo-risques-conformite** — Cartographie COSO ERM 2017 (matrice 5x5), contrôle interne (5 composantes), LCB-FT (KYC + TRACFIN), assurances (RC pro/D&O/cyber/multirisque), veille réglementaire programmée (hebdo + mensuelle + annuelle PLF), conformité RGPD/ACPR/AMF, BCP ISO 22301

#### Tier 4 — Croissance & financement (PASSERELLE MORIARTY)
- **cfo-financement-croissance** — Diagnostic financement (arbre de décision), catalogue exhaustif (aides publiques, banques, factoring, dette privée, mezzanine, equity), dossier banque, pack levée fonds (teaser/deck/cap table), M&A et DD financière, valorisation (DCF/multiples/transactions/LBO), cap table & equity (BSPCE/AGA/ratchet), restructuring, IPO, **Passerelle Moriarty** : CTA conditionnel uniquement sur aides publiques éligibles, hash SHA-256 du SIREN, jamais agressif

#### Tier 5 — Émergent 2026 (différenciateur fort)
- **cfo-csrd-esg** — Détermination wave CSRD (1/2/3/4 selon directive Stop-the-Clock 2025/794), mapping ESRS Set 1 (10 standards), méthodologie double matérialité EFRAG IG1, modèle CFO/CSO co-leadership, mesure GES Scope 1/2/3 (GHG Protocol + Bilan Carbone ADEME), climate risk TCFD, supply chain DD (loi vigilance + CSDDD), internal controls audit-grade rigor, external assurance (ISSA 5000), rapport intégré, plan transition climat trajectoire SBTi

### Added — Programmatique

- **30 scripts Python** au total (3 par skill) — tous syntax-valid testés
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

## [Non publié — futur v0.2]

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
