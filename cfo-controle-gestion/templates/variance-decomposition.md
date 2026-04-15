# Variance analysis, {{PERIODE}}

Société : {{COMPANY_NAME}} (SIREN {{SIREN}})

## Synthèse

| Indicateur | Valeur |
|------------|--------|
| CA budget | {{CA_BUDGET}} € |
| CA réel | {{CA_REEL}} € |
| **Variance totale** | **{{VARIANCE_TOTALE}} €** ({{VARIANCE_PCT}}%) |
| Dont effet volume | {{EFFET_VOLUME}} € |
| Dont effet prix | {{EFFET_PRIX}} € |
| Dont effet mix | {{EFFET_MIX}} € |

## Top variances par segment

{{POUR_CHAQUE_VARIANCE_SIGNIFICATIVE}}

### {{SEGMENT}} : {{VARIANCE_SEGMENT}} € ({{VARIANCE_PCT_SEGMENT}}%)

**Décomposition** :
- Volume : {{EFFET_VOL_SEGMENT}} € (qty budget {{VOL_BUDGET}} → qty réelle {{VOL_REEL}})
- Prix : {{EFFET_PRIX_SEGMENT}} € (prix budget {{PRIX_BUDGET}} € → prix réel {{PRIX_REEL}} €)

**Cause principale** : [Volume / Prix / Mix / Timing / Périmètre]

**Explication** :
{{EXPLICATION_MANUELLE}}

**Action corrective** :
{{ACTION}}

**Status** : {{STATUS_EMOJI}} {{STATUS_LABEL}}

---

{{FIN_POUR_CHAQUE}}

## Synthèse actions

| Action | Owner | Deadline | Impact attendu |
|--------|-------|----------|----------------|
{{ACTIONS_TABLE}}

## Limites

Ce commentaire de variance est un outil de pilotage interne. Les cause explications
sont proposées par analyse statistique mais **le commentaire final doit être validé**
par le CFO / contrôleur de gestion / EC selon contexte.
