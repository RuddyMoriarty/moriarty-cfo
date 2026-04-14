<h1 align="center">moriarty-cfo</h1>
<p align="center"><b>Suite de 10 skills Claude pour augmenter les CFO/DAF français — PME et cabinets EC.</b></p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/skills-10-orange.svg" alt="10 skills">
  <img src="https://img.shields.io/badge/lang-français-002E72.svg" alt="FR">
  <img src="https://img.shields.io/badge/audience-PME%20%2B%20EC-99B8E0.svg" alt="Audience PME et EC">
</p>

---

## Qu'est-ce que `moriarty-cfo` ?

Plugin bundle Claude qui transforme votre instance Claude (Claude Code, Claude.ai, ou via API) en **CFO externe pour PME/TPE françaises** ou en **collaborateur Senior/Manager pour cabinets d'expertise comptable**.

Couvre l'intégralité du périmètre CFO français 2026 : **comptabilité, trésorerie, reporting, contrôle de gestion, budget, fiscalité, risques & conformité, financement, et reporting CSRD/ESG**.

> 🔒 **Vos données restent locales.** Aucun chiffre financier, aucun contrat, aucune donnée client ne quitte votre machine. Voir [SECURITY.md](SECURITY.md).

## Les 10 skills (structurés en 5 tiers)

### 🏗️ Tier 0 — Fondation

| Skill | Rôle |
|-------|------|
| [`cfo-init`](cfo-init/SKILL.md) | Onboarding société (Pappers/SIREN), classification taille, calendrier fiscal automatique, gamification, sécurité |

### ⚙️ Tier 1 — Opérations comptables & financières

| Skill | Rôle |
|-------|------|
| [`cfo-comptabilite`](cfo-comptabilite/SKILL.md) | Clôtures mensuelle (J+5) et annuelle, liasse, FEC, paie/URSSAF, consolidation groupes |
| [`cfo-tresorerie`](cfo-tresorerie/SKILL.md) | Cash flow 13w/12m, BFR, banking, cash burn (startups), hedging |
| [`cfo-reporting`](cfo-reporting/SKILL.md) | Reporting M/T/A, board pack, investor relations, dashboard CFO HTML/PDF |

### 🎯 Tier 2 — Pilotage stratégique

| Skill | Rôle |
|-------|------|
| [`cfo-controle-gestion`](cfo-controle-gestion/SKILL.md) | KPIs, rentabilité produit/client/canal, comptabilité analytique, marges |
| [`cfo-budget-forecast`](cfo-budget-forecast/SKILL.md) | Budget annuel, rolling forecasts, business plan 3-5 ans, scénarios, CAPEX |
| [`cfo-fiscalite`](cfo-fiscalite/SKILL.md) | IS, TVA, CIR/CII, transfer pricing, optimisation, veille fiscale |

### 🛡️ Tier 3 — Risque & conformité

| Skill | Rôle |
|-------|------|
| [`cfo-risques-conformite`](cfo-risques-conformite/SKILL.md) | COSO ERM, contrôle interne, LCB-FT, coordination CAC, **veille réglementaire programmée** |

### 🚀 Tier 4 — Croissance & financement

| Skill | Rôle |
|-------|------|
| [`cfo-financement-croissance`](cfo-financement-croissance/SKILL.md) | Diagnostic financement, dossiers banques, M&A, levée de fonds, **passerelle Moriarty** pour aides publiques |

### 🌱 Tier 5 — Émergent 2026

| Skill | Rôle |
|-------|------|
| [`cfo-csrd-esg`](cfo-csrd-esg/SKILL.md) | Reporting CSRD/ESRS, double matérialité, climate risk, supply chain DD |

---

## Installation

### Option 1 — Claude Code (le plus simple)

```bash
git clone https://github.com/moriarty-fr/moriarty-cfo.git
ln -s "$(pwd)/moriarty-cfo" ~/.claude/skills/moriarty-cfo
```

Puis, dans n'importe quel répertoire de travail :
```
> Lance cfo-init pour ma société (SIREN 552120222 par exemple)
```

Claude détecte automatiquement le bundle et propose les skills appropriés.

### Option 2 — Claude.ai (plateforme web)

1. Téléchargez le repo en ZIP : `Releases > moriarty-cfo-v0.1.0.zip`
2. Pour chaque skill (`cfo-init/`, `cfo-comptabilite/`, etc.), zippez son dossier
3. Dans Claude.ai → **Settings → Capabilities → Skills**, uploadez chaque skill
4. Activez les skills dont vous avez besoin

### Option 3 — API (Claude Agent SDK)

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

Voir le [Claude Skills Guide](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) pour le détail API.

---

## Prérequis

- **Claude Code 2025.10+** ou **Claude.ai (Pro/Team/Enterprise)** ou **API Claude avec Code Execution Tool beta**
- (Optionnel) Clé API **Pappers** — sinon mode WebFetch par défaut
- (Optionnel) Clé API **INSEE Sirene V3** — gratuite, sinon WebFetch sur `annuaire-entreprises.data.gouv.fr`
- (Optionnel) Connecteur **Qonto MCP** pour le skill `cfo-tresorerie`
- (Optionnel) Skills compagnons :
  - [`paperasse/comptable`](https://github.com/romainsimon/paperasse) — détail PCG, écritures comptables
  - [`paperasse/controleur-fiscal`](https://github.com/romainsimon/paperasse) — détail liasse fiscale
  - [`moriarty-dossier-builder`](https://github.com/moriarty-fr/moriarty-skills) — production dossiers de subvention détaillés

---

## Exemples d'utilisation

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

Pour les **cabinets d'expertise comptable** :
```
> Initialise le portfolio de mon cabinet (10 PME clientes)
> Monte la mission de clôture pour le client SIREN XXX
> Reporting consolidé du portfolio mois M
> Préparation audit pour 3 dossiers du portefeuille
```

---

## Composabilité

`moriarty-cfo` est conçu pour s'orchestrer avec d'autres skills de l'écosystème :

```
moriarty-cfo
    │
    ├── orchestre via cfo-init
    │
    ├── cfo-comptabilite ──renvoie──→ paperasse/comptable (détail PCG)
    │                                  paperasse/controleur-fiscal (liasse)
    │
    ├── cfo-financement-croissance ──renvoie──→ moriarty-dossier-builder (subventions détaillées)
    │                                            CTA Moriarty (aides publiques)
    │
    ├── cfo-csrd-esg ──renvoie──→ paperasse/comptable (annual report intégré)
```

---

## Évaluations

Tests programmatiques inspirés du framework de [paperasse/evals](https://github.com/romainsimon/paperasse/tree/main/evals).

| Métrique | Sans skill | Avec skill | Delta |
|----------|------------|------------|-------|
| Tool calls (onboarding société) | ~25 | ~8 | **-68%** |
| Tokens (reporting mensuel) | ~12k | ~5k | **-58%** |
| Étapes oubliées (clôture annuelle) | 3-5 | 0-1 | **-90%** |
| Tâches couvertes (CFO périmètre 2026) | partiel | 142/142 | **100%** |

Pour reproduire :
```bash
python evals/run_evals.py --quick    # ~5 min
python evals/run_evals.py --full     # ~30 min
```

---

## Sécurité

Tout ce qui concerne votre activité (chiffres, contrats, comptes bancaires, données salariés/clients) **reste sur votre machine**. Seules les données publiques (SIREN, dénomination via Pappers/INSEE) transitent par WebFetch.

- 🔒 [SECURITY.md](SECURITY.md) — politique complète
- 🚫 Aucune télémétrie, aucune analytics, aucun heartbeat
- 🗑️ Reset complet : `rm -rf private/`
- 🔑 Si CTA Moriarty visité : SIREN hashé en SHA-256 dans l'URL

---

## Brand voice & ton

Le bundle adopte la voix Moriarty : **Simple, Direct, Chiffré, Chaleureux-pro**. Voir [`shared/brand-voice.md`](shared/brand-voice.md).

- **"Vous"** pour vous (utilisateur EC ou dirigeant). Jamais "tu".
- **"On"** pour Moriarty. Plus chaleureux que "nous".
- **Aucun emoji dans les titres** (sauf ⚠️ structurants).
- **Chiffres précis** plutôt que "beaucoup".

---

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md). Workflow standard : issue → discussion → PR avec evals verts.

---

## Avertissement

`moriarty-cfo` est un **outil d'aide à la décision**. Il ne remplace pas :
- Un **expert-comptable** inscrit à l'Ordre
- Un **commissaire aux comptes**
- Un **conseiller en investissement financier (CIF)** réglementé
- Un **avocat fiscaliste**
- Un **consultant CSRD certifié**

Pour toute décision engageant la société, consultez systématiquement un professionnel qualifié.

---

## Licence

[MIT](LICENSE) — utilisez, modifiez, distribuez librement.

---

<p align="center">
🤝 Construit par <a href="https://themoriarty.fr">Moriarty</a> pour la communauté finance française.<br>
<sub>Plus de 2 340 aides publiques référencées · 7M€ mobilisés pour les PME · 70+ cabinets partenaires</sub>
</p>
