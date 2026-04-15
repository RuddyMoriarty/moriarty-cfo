# Veille réglementaire programmée

Système de monitoring continu des évolutions réglementaires impactant la fonction finance.

## Sources à surveiller

### France — Cadre général

- **Légifrance** (https://www.legifrance.gouv.fr) — codes, lois, décrets
- **JORF** (Journal Officiel) — publications quotidiennes
- **Service Public Pro** (https://www.service-public.fr/professionnels-entreprises)

### Comptable et financier

- **ANC** (https://www.anc.gouv.fr) — règlements comptables français
- **CNCC** (https://www.cncc.fr) — Compagnie Nationale des Commissaires aux Comptes
- **OEC** (https://www.experts-comptables.fr) — Ordre des Experts-Comptables

### Fiscal

- **BoFip** (https://bofip.impots.gouv.fr) — doctrine fiscale
- **impots.gouv.fr** — DGFiP

### International

- **IASB** (https://www.iasb.org) — IFRS
- **OCDE** (https://www.oecd.org) — BEPS, transfer pricing
- **EFRAG** (https://www.efrag.org) — ESRS / CSRD

### Sectoriels (selon société)

- **AMF** (https://www.amf-france.org) — sociétés cotées
- **ACPR** (https://acpr.banque-france.fr) — banque/assurance
- **CNIL** (https://www.cnil.fr) — RGPD
- **ANSSI** (https://www.ssi.gouv.fr) — cybersécurité
- **TRACFIN** (https://www.economie.gouv.fr/tracfin) — LCB-FT

### Veilles privées (newsletters payantes)

- EFL — Editions Francis Lefebvre (Lamy Fiscal, Lamy Société...)
- Editions Législatives
- LexisNexis France
- Dictionnaire Permanent Comptable

## Cadence programmée

### Hebdomadaire (lundi 9h jittered)

Tâche : revue des publications de la semaine sur les sources principales.

Exécution :
```python
# Programmé via mcp__scheduled-tasks
prompt = """
Veille réglementaire hebdomadaire — semaine {numero_semaine}.

Vérifier les publications de la semaine sur :
- ANC (normes comptables)
- IASB (IFRS)
- AMF (marchés)
- ACPR (prudentiel)
- Légifrance (lois de finance, codes)
- BoFip (doctrine fiscale)

Pour chaque publication impactant le profil société (lire private/company.json) :
- Résumer en 2-3 lignes
- Évaluer impact (faible / moyen / fort)
- Proposer action si applicable

Sortie : `out/veille-{date}.md`
"""
```

### Mensuelle (1er du mois 9h)

Synthèse mensuelle :
- Récap des évolutions retenues
- Actions en cours
- Calendrier d'application

### Annuelle (1er octobre)

Veille spéciale Projet de Loi de Finance N+1 :
- Publication PLF prévue mi-septembre
- Impact à analyser pour le budget N+1

### Ad hoc (déclenchée par événement)

- Publication CSRD (impact entité in-scope)
- Décision Conseil d'État majeure
- Modification taux IS / TVA

## Programmation via `scripts/veille_scheduler.py`

Génère le payload pour `mcp__scheduled-tasks__create_scheduled_task` :

Input : `private/company.json` (pour adapter le scope) + niveau de veille (1 à 4)

Output : liste de tâches à programmer (hebdo, mensuel, annuel, événementiel)

## Synthèse mensuelle type

```markdown
# Synthèse veille réglementaire — {Mois} {Année}

## Evolutions majeures du mois

### 1. {TITRE_EVOLUTION_1}
- **Source** : {SOURCE_OFFICIELLE}
- **Date publication** : {DATE}
- **Date application** : {DATE_APPLICATION}
- **Impact pour {COMPANY_NAME}** : {IMPACT_QUALITATIF} / {IMPACT_QUANTITATIF}
- **Action** : {ACTION_RECOMMANDEE}

### 2. ...

## Évolutions à surveiller

- {EVOLUTION_2}
- {EVOLUTION_3}

## Calendrier des prochaines applications

| Date | Évolution | Action |
|------|-----------|--------|
| ... | ... | ... |

## Recommandations

- {RECOMMANDATION_1}
- {RECOMMANDATION_2}
```

## Niveaux de veille (configurable dans `private/profile.json`)

- **Niveau 1 — Base** : France générale uniquement, hebdo
- **Niveau 2 — Standard** (par défaut) : France + UE, hebdo + mensuel
- **Niveau 3 — Renforcé** : France + UE + sectoriel + International, hebdo + mensuel + ad hoc
- **Niveau 4 — Maximum** : tout (utile pour les ETI+/cotées + groupes internationaux)

## Bonnes pratiques

- **Filtrer par pertinence** : ne pas remonter au CFO les évolutions sans impact
- **Quantifier l'impact** quand possible (€ / process / délais)
- **Action timeline** : "à mettre en œuvre avant le {date}"
- **Centralisation** : un seul fichier `private/veille-historique.md` plutôt que 12 fichiers mensuels
- **Revue annuelle** : rétrospective des évolutions de l'année

## Avertissement

La veille programmée par ce skill **ne remplace pas** :
- Un abonnement à une base professionnelle (EFL, Lamy, etc.)
- L'assistance d'un expert-comptable, avocat, ou consultant pour l'analyse d'impact
- La formation continue de l'équipe finance

C'est un outil de **détection** et de **rappel**, pas de **conseil**.
