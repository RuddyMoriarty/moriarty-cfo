# Calendrier fiscal automatique

Logique de génération du calendrier fiscal à partir de la date de clôture de la société, des régimes appliqués, et des offsets relatifs définis dans `../../data/calendar-fiscal-base.json`.

## Principe

Chaque échéance est stockée dans `calendar-fiscal-base.json` sous forme d'**offset relatif** (nombre de jours depuis la clôture, ou mois/trimestre glissant, ou date calendaire fixe). Le script `scripts/compute_calendar.py` calcule les **dates absolues** pour les 18 prochains mois.

## Types d'offsets supportés

### 1. `offset_from_closing` : N jours après la clôture

Exemple : Liasse fiscale = `+135d` → si clôture au 31/12/2026, déposée au **15/05/2027**.

Applicable à : IS (acomptes + solde), liasse fiscale, dépôt greffe, approbation AG.

### 2. `offset_each_month` : N jours après chaque fin de mois

Exemple : TVA mensuelle CA3 = `+24d` → TVA de mars à déposer au **24/04**, TVA d'avril au **24/05**, etc.

Applicable à : TVA mensuelle, DSN mensuelle.

### 3. `offset_each_quarter` : N jours après chaque fin de trimestre

Exemple : TVA trimestrielle = `+24d` → T1 (jan-fév-mars) déposée au 24/04, T2 au 24/07, etc.

### 4. `offset_calendar` : date fixe annuelle

Exemple : Taxe apprentissage = `annual:05/05` → chaque année au 5 mai, indépendamment de la clôture.

Applicable à : taxes calendaires annuelles (apprentissage, formation, PEEC).

### 5. `offset_recurring` : pattern récurrent

Exemple : `weekly:lundi:09:00` ou `monthly:1er:09:00` pour les veilles programmées.

## Règles d'applicabilité

Chaque échéance a un champ `_applicable_si` ou `obligation` qui filtre si elle s'applique à la société :

- `is_regime` : uniquement si la société est à l'IS
- `effectif > 0` : uniquement si au moins 1 salarié
- `effectif >= 50` : uniquement si 50+ salariés (ex. effort construction PEEC)
- `regime_tva == 'reel_normal'` : selon régime TVA
- `csrd_wave != 'hors_scope'` : uniquement si in-scope CSRD

`scripts/compute_calendar.py` applique ces filtres avant d'écrire l'échéance dans `private/calendar-fiscal.json`.

## Code couleur à l'affichage

```
🔴 < 7 jours    — urgence critique, s'y mettre maintenant
🟠 7-14 jours   — élevé, préparer cette semaine
🟡 15-30 jours  — moyen, sur la roadmap du mois
🟢 > 30 jours   — standard, sur le planning
```

## Exemples de calculs

### Exemple 1 — SAS à l'IS, clôture 31/12/2026, TVA mensuelle, 40 salariés

Échéances dans les 30 prochains jours (au 14/04/2026) :

| Date | Label | Couleur | Type |
|------|-------|---------|------|
| 24/04/2026 | TVA mars 2026 (CA3) | 🟠 J+10 | TVA mensuelle |
| 05/05/2026 | DSN avril 2026 | 🟡 J+21 | Social |
| 05/05/2026 | Taxe apprentissage (solde) | 🟡 J+21 | Social |

### Exemple 2 — SARL à l'IR BIC, clôture 30/06/2026, TVA réel simplifié

| Date | Label | Couleur | Type |
|------|-------|---------|------|
| 31/07/2026 | Acompte TVA juillet (CA12) | 🟡 J+108 depuis aujourd'hui | TVA |
| 12/11/2026 | Liasse fiscale (offset +135j vs 30/06) | | Fiscal |
| 12/11/2026 | Solde IS | | Fiscal |
| 31/12/2026 | Acompte TVA décembre (CA12) | | TVA |

### Exemple 3 — ETI cotée CSRD Wave 1, clôture 31/12

Échéances spécifiques CSRD :
- 30/06/2027 : Rapport de durabilité CSRD (offset +180j) — à publier intégré au rapport de gestion

## Fichier généré `private/calendar-fiscal.json`

Format :

```json
{
  "_version": "0.1.0",
  "_generated_at": "2026-04-14T22:30:00Z",
  "_inputs": {
    "closing_date": "2026-12-31",
    "tva_regime": "reel_normal_mensuelle",
    "is_regime": true,
    "effectif": 40,
    "csrd_wave": "hors_scope"
  },
  "echeances": [
    {
      "id": "tva_mensuelle_2026-04",
      "label": "TVA avril 2026 (CA3)",
      "date_absolue": "2026-05-24",
      "type": "tva",
      "categorie_calendrier": "fiscal",
      "skill_recommande": "cfo-fiscalite",
      "days_from_now": 40,
      "couleur": "🟢",
      "source": "data/calendar-fiscal-base.json > tva_mensuelle"
    }
  ],
  "_next_30_days_count": 3,
  "_next_90_days_count": 8,
  "_next_18_months_count": 45
}
```

## Cas particuliers

### Clôture au 31/12 vs autre date

Si la clôture est le **31/12** (cas le plus fréquent), les échéances IS sont des "dates pivotées" classiques :
- Acompte 1 : 15/03 (+75j)
- Acompte 2 : 15/06 (+165j)
- Acompte 3 : 15/09 (+255j)
- Acompte 4 : 15/12 (+345j)
- Solde + liasse : 15/05 (+135j)

Si la clôture est à une autre date (30/06, 30/09, 31/03, etc.), toutes les échéances sont décalées proportionnellement. Le script fait ce calcul automatiquement.

### Exercice de durée non standard

Si `company.exercice_comptable.duree_mois != 12` (exercice raccourci ou allongé, par ex. première clôture ou changement) :
- Prévenir l'utilisateur que le calendrier peut être non-standard
- Référer à l'EC humain pour validation des échéances transitoires

### Dates exactes TVA mensuelle selon SIREN

La date exacte de dépôt TVA dépend du **premier digit du SIREN** (cf. bofip) :
- 0, 1, 2 → 16-17 du mois suivant
- 3, 4, 5, 6, 7 → 19-20
- 8, 9 → 21-24

`scripts/compute_calendar.py` applique cette logique si l'option est activée.

### Jours ouvrés

Si une échéance tombe un week-end ou jour férié, la date légale est reportée au **prochain jour ouvré**. Le script gère les jours fériés français standards (1er jan, lundi de Pâques, 1er mai, 8 mai, Ascension, Pentecôte, 14 juillet, 15 août, 1er nov, 11 nov, 25 déc).

## Mise à jour

Si l'utilisateur change sa date de clôture (`"change ma date de clôture au 30/06"`) :
1. Mettre à jour `private/company.json > exercice_comptable.date_cloture`
2. Relancer `python3 scripts/compute_calendar.py`
3. Re-programmer les notifications (cf. `notifications.md`)
4. Afficher le nouveau calendrier

## Références

- Source officielle : https://www.impots.gouv.fr/professionnel/calendrier-fiscal
- Bofip TVA : https://bofip.impots.gouv.fr
- URSSAF DSN : https://www.net-entreprises.fr/declaration/dsn/
- Voir aussi : `../../data/calendar-fiscal-base.json`
