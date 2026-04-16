# Portfolio EC (mode cabinet multi-clients)

Reference technique du mode portfolio pour les cabinets d'expertise comptable (introduit en v0.1.4).

## Contexte

Un cabinet EC gere typiquement 50 a 200+ clients PME/TPE. Le mode portfolio structure le suivi multi-clients :

- Un cabinet = une entite (stockee dans `private/cabinet.json`)
- Chaque client = un dossier independant dans `private/companies/<siren>/`
- Un index central `private/companies/index.json` liste tous les clients avec leur statut

## Workflow type

### 1. Initialisation du cabinet (une fois)

```bash
python3 cfo-init/scripts/portfolio/init_cabinet.py \
  --siren 123456789 --denomination "CABINET DURAND" \
  --forme selarl --ville Paris
```

Cree :
- `private/cabinet.json` depuis `cabinet.template.json`
- `private/profile.json` avec `audience_type=ec_collaborateur`
- `private/companies/index.json` (liste vide)

### 2. Ajout de clients (repete)

```bash
python3 cfo-init/scripts/portfolio/add_client.py \
  --siren 552120222 --denomination "BOULANGERIE MARTIN SAS" \
  --taille pe --secteur commerce --cloture 2026-12-31 \
  --mission presentation --referent "Jean Dupont"
```

Pour chaque client :
- Cree `private/companies/<siren>/company.json` minimal
- Ajoute l'entree dans `index.json` avec `status=actif`
- Synchronise `cabinet.json > portfolio_clients.siren_list[]`

Idempotent : si le SIREN existe deja, met a jour sans doubler.

### 3. Listing et suivi

```bash
python3 cfo-init/scripts/portfolio/list_clients.py
python3 cfo-init/scripts/portfolio/list_clients.py --detailed
python3 cfo-init/scripts/portfolio/list_clients.py --status archive
```

### 4. Programmation batch des routines

```bash
python3 cfo-init/scripts/portfolio/schedule_all.py --dry-run
python3 cfo-init/scripts/portfolio/schedule_all.py --level 2
```

Itere sur chaque client actif et appelle :
- `compute_entity_routines.py --siren X` (derivation des routines applicables)
- `schedule_routines.py --siren X` (generation des payloads scheduled-tasks)

Met a jour `routines_active=true` dans l'index pour les clients OK.

### 5. Dashboard agrege

```bash
python3 cfo-init/scripts/portfolio/portfolio_dashboard.py
python3 cfo-init/scripts/portfolio/portfolio_dashboard.py --pdf
```

Genere un HTML A4 landscape avec :
- 4 stats (clients actifs/archives, routines programmees, alertes 7 jours)
- Resume de la semaine
- Liste d'alertes par couleur : rouge < 7 jours, orange 7-14 jours, jaune 15-30 jours
- Tableau complet trie par denomination (SIREN, taille, mission, referent, routines, prochaine echeance, statut)

Les echeances sont lues depuis `private/companies/<siren>/calendar-fiscal.json` (genere par `compute_calendar.py`).

### 6. Archivage ou suppression

```bash
# Archive (conserve les fichiers, status=archive)
python3 cfo-init/scripts/portfolio/remove_client.py --siren X --archive

# Suppression definitive (destructif)
python3 cfo-init/scripts/portfolio/remove_client.py --siren X --delete --force
```

## Schema `private/companies/index.json`

```json
{
  "_meta": {
    "cabinet_siren": "123456789",
    "last_updated": "2026-04-16T10:00:00+02:00",
    "count": 2
  },
  "clients": [
    {
      "siren": "552120222",
      "denomination": "BOULANGERIE MARTIN SAS",
      "taille": "pe",
      "status": "actif",
      "mission_type": "presentation",
      "referent": "Jean Dupont",
      "added_at": "2026-04-16",
      "routines_active": true,
      "next_deadline": null
    }
  ]
}
```

## Valeurs autorisees

| Champ | Valeurs |
|-------|---------|
| `taille` | tpe, pe, me, eti, ge |
| `status` | actif, archive |
| `mission_type` | presentation, examen_limite, audit_legal_cac, social_paie, juridique, conseil_financier, cir_cii, aides_publiques, m_and_a, csrd_esrs |

## Strategie de scheduling

`schedule_all.py` execute les clients **en sequentiel** (pas en parallele). Pour un portfolio de 100 clients avec 5-10 routines chacun, compter 2-3 minutes d'execution. Rationale : les scripts font des appels MCP scheduled-tasks qui doivent etre ordonnances pour eviter les collisions de cron minute.

Le parallelisme via `multiprocessing` est envisageable pour les grands cabinets (500+ clients) mais reporte a une version ulterieure.

## Modules v0.1.5 (pilotage operationnel)

### Relances dossier incomplet

```bash
python3 cfo-init/scripts/portfolio/check_dossier.py --siren X
python3 cfo-init/scripts/portfolio/draft_relance.py --siren X --type premiere --output private/companies/X/relance-v1.txt
```

Le catalogue des pieces attendues par `mission_type` vit dans `data/pieces-dossier.json` (4 missions : presentation, examen_limite, audit_legal_cac, social_paie). Les pieces recues se declarent dans `private/companies/<siren>/pieces.json` :

```json
{"pieces_recues": {"balance_generale": {"recu": true, "date": "2026-03-10"}}}
```

Deux templates de mail disponibles : `relance-premiere.md` (courtois) et `relance-urgente.md` (avec echeance legale et risque penalite). Historique dans `private/companies/<siren>/relances.json`.

### Lettres de mission

```bash
python3 cfo-init/scripts/portfolio/generate_lettre_mission.py --siren X --honoraires 4500 --exercice 2026
python3 cfo-init/scripts/portfolio/generate_lettre_mission.py --siren X --honoraires 4800 --exercice 2027 --new-version
```

3 templates alignes sur les normes professionnelles : NP 2300 (presentation), NP 2400 (examen limite), et missions sociales/paie (avec clauses RGPD sous-traitant art. 28). Versioning automatique v1, v2, v3... stocke dans `private/companies/<siren>/lettres-mission/`. Metadata trackee dans `metadata.json`.

### Pilotage encaissements

```bash
python3 cfo-init/scripts/portfolio/encaissements_aging.py
python3 cfo-init/scripts/portfolio/encaissements_aging.py --siren X --detailed
```

Aging base sur la LME (art. L. 441-10 C. com., delai legal 60 jours) : a jour < 30j, echu 30-60j (tolerance), echu 60-90j (hors LME), > 90j (provision). Le fichier `private/companies/<siren>/factures.json` contient la liste des factures emises :

```json
{"factures": [{"numero": "F2026-001", "date_emission": "2026-04-10", "montant_ht": 1500, "statut": "emise"}]}
```

Statuts possibles : `emise` (non encaissee) ou `encaissee`.

### Suivi forfaits vs reel

```bash
python3 cfo-init/scripts/portfolio/forfait_tracker.py
python3 cfo-init/scripts/portfolio/forfait_tracker.py --siren X --detailed
```

Compare les heures consommees avec le forfait contractuel. Deux fichiers par client :

```json
# forfait.json
{"forfait_heures": 40, "tjm_reference": 680, "annee": 2026}

# temps-passes.json
{"saisies": [{"date": "2026-04-01", "collaborateur": "Jean", "heures": 3.5, "tache": "..."}]}
```

4 statuts : `ok` < 70 %, `vigilance` 70-90 %, `limite_atteinte` 90-100 %, `depassement` > 100 %. Calcul du cout theorique du depassement via le TJM reference.

## Sources

- Fiches de poste EC : [`data/cfo-job-corpus.json`](../../data/cfo-job-corpus.json) categorie "11_rh_paie" et "12_administratif_juridique"
- Template cabinet : [`cfo-init/templates/cabinet.template.json`](../templates/cabinet.template.json)
- Ordre des Experts-Comptables : https://www.experts-comptables.fr
