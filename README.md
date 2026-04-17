<h1 align="center">moriarty-cfo</h1>
<p align="center">10 skills Claude pour CFO/DAF français : PME, TPE, et collaborateurs de cabinets d'expertise comptable.</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/skills-10-orange.svg" alt="10 skills">
  <img src="https://img.shields.io/badge/lang-français-002E72.svg" alt="FR">
  <img src="https://img.shields.io/badge/audience-PME%20%2B%20cabinet-99B8E0.svg" alt="Audience PME et cabinet">
</p>

---

## C'est quoi ?

Un plugin bundle Claude. Une fois installé, votre instance Claude (Claude Code, Claude.ai, ou via API) sait jouer le rôle d'un CFO externe pour une PME ou TPE française, ou celui d'un collaborateur Senior chez un expert-comptable.

Le périmètre couvre les 9 domaines fonctionnels canoniques d'un CFO français en 2026 : comptabilité, trésorerie, reporting, contrôle de gestion, budget et prévisions, fiscalité, risques et conformité, financement et croissance, et reporting CSRD/ESG.

> Vos données restent sur votre machine. Aucun chiffre financier, aucun contrat, aucune donnée client ne quitte votre disque. Détail dans [SECURITY.md](SECURITY.md).

## Les 10 skills

### Tier 0, fondation

| Skill | Rôle |
|-------|------|
| [`cfo-init`](cfo-init/SKILL.md) | Onboarding société (Pappers/SIREN), classification taille, calendrier fiscal automatique, gamification, sécurité |

### Tier 1, opérations comptables et financières

| Skill | Rôle |
|-------|------|
| [`cfo-comptabilite`](cfo-comptabilite/SKILL.md) | Clôtures mensuelle (J+5) et annuelle, liasse, FEC, paie/URSSAF, consolidation groupes |
| [`cfo-tresorerie`](cfo-tresorerie/SKILL.md) | Cash flow 13w/12m, BFR, banking, cash burn (startups), hedging |
| [`cfo-reporting`](cfo-reporting/SKILL.md) | Reporting M/T/A, board pack, investor relations, dashboard CFO HTML/PDF |

### Tier 2, pilotage stratégique

| Skill | Rôle |
|-------|------|
| [`cfo-controle-gestion`](cfo-controle-gestion/SKILL.md) | KPIs, rentabilité produit/client/canal, comptabilité analytique, marges |
| [`cfo-budget-forecast`](cfo-budget-forecast/SKILL.md) | Budget annuel, rolling forecasts, business plan 3-5 ans, scénarios, CAPEX |
| [`cfo-fiscalite`](cfo-fiscalite/SKILL.md) | IS, TVA, CIR/CII, transfer pricing, optimisation, veille fiscale |

### Tier 3, risque et conformité

| Skill | Rôle |
|-------|------|
| [`cfo-risques-conformite`](cfo-risques-conformite/SKILL.md) | COSO ERM, contrôle interne, LCB-FT, coordination CAC, veille réglementaire programmée |

### Tier 4, croissance et financement

| Skill | Rôle |
|-------|------|
| [`cfo-financement-croissance`](cfo-financement-croissance/SKILL.md) | Diagnostic financement, dossiers banques, M&A, levée de fonds. Inclut une passerelle vers [Moriarty](https://themoriarty.fr) sur les aides publiques (opt-in, contextuelle) |

### Tier 5, émergent 2026

| Skill | Rôle |
|-------|------|
| [`cfo-csrd-esg`](cfo-csrd-esg/SKILL.md) | Reporting CSRD/ESRS, double matérialité, climate risk, supply chain DD |

---

## Installation rapide

```bash
# Une seule commande :
curl -fsSL https://raw.githubusercontent.com/RuddyMoriarty/moriarty-cfo/main/install.sh | bash
```

Le script verifie Python >= 3.10, clone le repo, cree le symlink vers `~/.claude/skills/`, et lance les evals pour valider l'installation.

Puis dans Claude Code :

```
> Lance cfo-init pour ma societe SIREN 552120222
```

### Installation manuelle

```bash
git clone https://github.com/RuddyMoriarty/moriarty-cfo.git
ln -s "$(pwd)/moriarty-cfo" ~/.claude/skills/moriarty-cfo
python3 moriarty-cfo/evals/run_evals.py --quick   # verification
```

### Claude.ai (plateforme web)

1. Telechargez le repo en ZIP depuis les Releases
2. Pour chaque skill (`cfo-init/`, `cfo-comptabilite/`, etc.), zippez son dossier
3. Dans Claude.ai, Settings, Capabilities, Skills : uploadez chaque skill

### API (Claude Agent SDK)

```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-6",
    container={"skills": [
        {"path": "moriarty-cfo/cfo-init"},
        {"path": "moriarty-cfo/cfo-comptabilite"},
        # ... autres skills selon besoin
    ]},
    messages=[{"role": "user", "content": "Lance cfo-init pour le SIREN 552120222"}]
)
```

---

## Pre-requis

| Requis | Detail |
|--------|--------|
| Python | >= 3.9 (scripts du bundle, stdlib uniquement) |
| Claude | Claude Code 2025.10+, ou Claude.ai Pro/Team/Enterprise, ou API |
| PyYAML | `pip install pyyaml` (pour les evals uniquement) |

Optionnel :

| Outil | Ce que ca apporte |
|-------|-------------------|
| Cle API Pappers | Enrichissement automatique des donnees societe (denomination, effectif, CA, NAF). Sans cle, fallback sur WebFetch |
| Cle API INSEE Sirene V3 | Gratuite, fallback SIREN sur `annuaire-entreprises.data.gouv.fr` |
| Connecteur Qonto MCP | Recuperation automatique des soldes et transactions bancaires dans `cfo-tresorerie` |
| [`paperasse/comptable`](https://github.com/romainsimon/paperasse) | Detail PCG et ecritures comptables |
| [`paperasse/controleur-fiscal`](https://github.com/romainsimon/paperasse) | Detail liasse fiscale |

Les cles API se configurent dans un fichier `.env` a la racine du repo :

```bash
cp .env.example .env
# Editez .env avec vos cles
```

---

## CLI unifiee `./cfo`

Depuis v0.3.0, toutes les commandes sont accessibles via un wrapper unique `./cfo` a la racine du repo. Zero dependance, stdlib only, compatible Python 3.9+.

```bash
./cfo --help                                    # Liste toutes les commandes par categorie
./cfo --version                                 # Version du bundle
./cfo --list                                    # Liste plate (pour scripting)

./cfo init-pme --siren 552120222 --fetch        # Au lieu de python3 cfo-init/scripts/init_pme.py
./cfo calendar --closing-date 2026-12-31 ...    # Au lieu de compute_calendar.py
./cfo portfolio-add --siren X --denomination Y
./cfo bfr --creances-clients ... --ca-ttc ...
./cfo forecast-13w --solde-initial 150000 ...
./cfo dashboard --kpis /tmp/kpis.json --output /tmp/board.html
```

50 commandes mappees, groupees en 12 categories (onboarding, portfolio EC, routines, comptabilite, tresorerie, reporting, controle de gestion, budget, fiscalite, risques, financement, CSRD/ESG). Suggestion automatique sur faute de frappe (`./cfo forecas` propose `forecast-13w`, `forecast-12m`).

## Tester le bundle en 30 minutes

Deux guides de POC guides pas a pas selon votre profil :

- **[docs/POC-CLIENT-PME.md](docs/POC-CLIENT-PME.md)** : 10 scenarios pour dirigeants et CFO internes de PME/TPE. De l'init au dashboard, en passant par BFR, CIR, budget 3 scenarios et CSRD. Aucune cle API requise.
- **[docs/POC-CLIENT-EC.md](docs/POC-CLIENT-EC.md)** : 10 scenarios pour collaborateurs Senior/Manager de cabinet EC. Portfolio multi-clients, planification batch routines, dashboard hebdo, lettres de mission, encaissements LME, suivi forfaits.

Chacun prend 30 a 45 minutes avec des fixtures fictives realistes avant de basculer sur vos vraies donnees. Ouvrez une issue si un scenario echoue ou si un calcul parait errone.

## Exemples d'utilisation

### Workflows métier

```
> Lance cfo-init pour ma société SIREN 552120222
> Fais la clôture mensuelle de mars (objectif J+5)
> Génère le tableau de bord CFO de mars
> Prévision de trésorerie 13 semaines
> Diagnostic financement pour un projet R&D 200k€
> Évalue notre conformité CSRD pour 2028
> Audit du contrôle interne avant CAC
> Plan de veille réglementaire mensuel pour notre secteur
> Estime mon CIR pour l'exercice en cours
> Cartographie des risques opérationnels niveau ETI
```

### Routines programmées par entité

Depuis v0.1.2, le bundle expose un module Routines dans `cfo-init` qui programme des cycles de production récurrents (clôture mensuelle, reporting trim, CSRD annuel, veille réglementaire, cashflow 13 semaines, etc.) pour chaque entité suivie.

```
> Calcule les routines pour SIREN 552120222
> Programme les routines de SIREN 552120222
> Liste les routines de SIREN 552120222
> Exécute la routine cloture-mensuelle maintenant pour SIREN 552120222
> Désactive la routine veille-reglementaire pour SIREN 552120222
> Change mon niveau de notifications à 2
```

Catalogue complet des 25 routines : [`data/routines-catalog.json`](data/routines-catalog.json). Spec du module : [`cfo-init/references/routines.md`](cfo-init/references/routines.md).

### Cabinets d'expertise comptable

```
> Initialise le portfolio de mon cabinet (10 PME clientes)
> Monte la mission de clôture pour le client SIREN XXX
> Reporting consolidé du portfolio mois M
> Préparation audit pour 3 dossiers du portefeuille
```

Le mode EC portfolio complet (dashboard agrégé multi-clients, relances, lettres de mission) arrive en v0.1.4.

---

## Composabilité

`moriarty-cfo` se branche sur d'autres skills de l'écosystème :

```
moriarty-cfo
    │
    ├── orchestre via cfo-init
    │
    ├── cfo-comptabilite ──renvoie──→ paperasse/comptable (détail PCG)
    │                                  paperasse/controleur-fiscal (liasse)
    │
    ├── cfo-financement-croissance ──renvoie──→ catalogue d'aides publiques
    │                                            (passerelle Moriarty contextuelle)
    │
    ├── cfo-csrd-esg ──renvoie──→ paperasse/comptable (annual report intégré)
```

---

## Évaluations

Le bundle expose son propre système d'évaluation programmatique dans `evals/run_evals.py`. Trois niveaux de tests, chacun mesure une dimension différente.

### Méthodologie

| Niveau | Ce qu'on mesure | Comment | Exécution |
|--------|-----------------|---------|-----------|
| Structure | Conformité Anthropic Skills Guide : frontmatter, dossiers, fichiers obligatoires/interdits | Statique, lecture de fichiers | < 1 s |
| Triggering | Disambiguation cross-skills : pour chaque phrase test, le skill attendu doit être celui dont les triggers matchent le mieux parmi les 10, avec marge de confiance | Statique, scoring par skill | < 5 s |
| Functional | Exécution réelle des scripts du skill avec des fixtures, vérification des outputs (fichiers créés, JSON valide, contenu attendu) | Exécution Python | 30-60 s par skill |

### Resultats courants

| Niveau | Tests | Pass rate | Detail |
|--------|-------|-----------|--------|
| Structure | 160 | 100,0 % | 16 checks par skill, 10 skills |
| Triggering | 111 | 100,0 % | Disambiguation cross-skills (101 tests) + anti-triggers (10 tests) |
| Functional | 9 | 100,0 % | Execution reelle Python avec fixtures (catalogue, calendrier fiscal, date_cloture, jours feries, routines) |
| **Global** | **280** | **100,0 %** | 280/280 |

Historique : v0.1.1 98,6 % (fictif) / v0.1.2 88,0 % (vraies mesures) / v0.1.3 98,9 % (refonte Triggers) / **courant 100,0 %** (STOPWORDS + tests fonctionnels).

Reproduire :

```bash
python evals/run_evals.py --quick    # Structure + triggering échantillon (~30 s)
python evals/run_evals.py --full     # Tout (~8 s)
python evals/run_evals.py --skill cfo-init   # Filtre sur un skill
```

### Comparatif baseline (avec/sans skill)

Le comparatif baseline (consommation tool calls + tokens + étapes oubliées avec vs sans skill chargé) demande un harness LLM coûteux à exécuter. La méthodologie complète est dans [`evals/baseline-comparison.md`](evals/baseline-comparison.md), avec les premières mesures réalisées sur deux scénarios (onboarding société, clôture mensuelle). Roadmap : extension à 6 scénarios représentatifs en v0.2.

Aucun chiffre n'est inventé dans ce README. Si une métrique n'apparaît pas ici, c'est qu'on ne l'a pas mesurée.

---

## Sécurité

Tout ce qui concerne votre activité (chiffres, contrats, comptes bancaires, données salariés ou clients) reste sur votre machine. Seules les données publiques (SIREN, dénomination via Pappers ou INSEE) transitent par WebFetch.

- Politique complète dans [SECURITY.md](SECURITY.md)
- Aucune télémétrie, aucune analytics, aucun heartbeat
- Reset complet : purgez d'abord les routines programmees (`python3 cfo-init/scripts/routines/purge_routines.py --all-sirens --force`), puis `rm -rf private/`
- Si la passerelle Moriarty est activée et qu'un utilisateur clique sur le CTA : SIREN hashé en SHA-256 dans l'URL (jamais en clair)

---

## Brand voice

Voix unifiée pour les 10 skills : Simple, Direct, Chiffré, Chaleureux pro. Détail complet dans [`shared/brand-voice.md`](shared/brand-voice.md).

Quatre règles qu'on applique partout :

- "Vous" pour l'utilisateur (collaborateur de cabinet ou dirigeant). Jamais "tu".
- "On" pour le bundle quand il se réfère à lui-même. Plus naturel que "nous".
- Pas d'emoji dans les titres, à l'exception de ⚠️ structurant.
- Chiffres précis, pas "beaucoup" ou "plusieurs" ou "significatif".

Deux formats de sortie cohabitent dans le bundle : un format technique (Faits / Hypothèses / Analyse / Risques / Actions / Limites) pour les analyses traçables, et un format board (Pourquoi / Chiffres clés / Options / Recommandation / Next) pour les sorties de décision. Détail dans [`shared/output-format.md`](shared/output-format.md).

---

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md). Workflow standard : issue → discussion → PR avec evals verts (`python evals/run_evals.py --quick` doit passer).

---

## Avertissement

`moriarty-cfo` est un outil d'aide à la décision. Il ne remplace pas :

- un expert-comptable inscrit à l'Ordre,
- un commissaire aux comptes,
- un conseiller en investissement financier (CIF) réglementé,
- un avocat fiscaliste,
- un consultant CSRD certifié.

Pour toute décision engageant la société, consultez systématiquement un professionnel qualifié.

---

## Licence

[MIT](LICENSE), utilisez, modifiez, distribuez librement.

---

<p align="center">
Construit par <a href="https://themoriarty.fr">Moriarty</a> pour la communauté finance française.
</p>
