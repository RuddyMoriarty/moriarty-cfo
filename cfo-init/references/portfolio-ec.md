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

## Limites v0.1.4

Livre dans cette version :
- Portfolio multi-clients (init, add, list, remove, schedule_all)
- Dashboard agrege HTML + PDF

Reporte a v0.1.5 :
- Relances clients dossier incomplet (detection + mail template)
- Lettres de mission (generation + versioning)
- Pilotage encaissements (aging factures par mission)
- Suivi forfaits vs realise (heures bookees vs heures consommees)

## Sources

- Fiches de poste EC : [`data/cfo-job-corpus.json`](../../data/cfo-job-corpus.json) categorie "11_rh_paie" et "12_administratif_juridique"
- Template cabinet : [`cfo-init/templates/cabinet.template.json`](../templates/cabinet.template.json)
- Ordre des Experts-Comptables : https://www.experts-comptables.fr
