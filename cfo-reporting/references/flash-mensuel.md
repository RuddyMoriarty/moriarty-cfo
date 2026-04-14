# Flash mensuel M+5

Document d'une page livré **5 jours ouvrés après la fin du mois**. Destiné au CODIR interne. Format court, actionnable.

## Structure

```markdown
# Flash {MOIS} {ANNEE} — {SOCIETE}

📅 Arrêté au {DATE_ARRETE} · Publié le {DATE_PUB}

## 3 highlights
- {HIGHLIGHT_1}
- {HIGHLIGHT_2}
- {HIGHLIGHT_3}

## 3 lowlights
- {LOWLIGHT_1}
- {LOWLIGHT_2}
- {LOWLIGHT_3}

## KPIs flash
| KPI | Valeur | vs M-1 | vs Budget |
|-----|--------|--------|-----------|
| CA HT | {CA} k€ | {DELTA_M1}% | {DELTA_BUDGET}% |
| EBITDA | {EBITDA} k€ | {DELTA} | {DELTA} |
| Marge brute | {MB}% | {DELTA} pts | {DELTA} pts |
| Cash | {CASH} k€ | {DELTA} | — |
| Runway (si startup) | {RUNWAY} mois | {DELTA} | — |

## Trésorerie
- Solde : {SOLDE} k€
- Alertes : {ALERTES_ACTIVE}
- Prochaines échéances critiques : {ECHEANCES_CRITIQUES}

## Action de la semaine
→ {ACTION_PRIORITAIRE}
```

## Règles de rédaction

- **Chiffres précis** : jamais "environ 100k", toujours "98,3 k€"
- **Delta explicite** : toujours vs M-1 et vs budget si budget existe
- **Couleur trend** : 🟢 meilleur / 🟠 stable / 🔴 pire (vs cible attendue)
- **Action unique** : **une seule** action prioritaire, pas 5

## Automatisation

Le script `scripts/generate_dashboard.py --flash` génère le flash automatiquement depuis :
- `private/company.json` pour le profil
- Balance mensuelle CSV pour les KPIs
- Forecast 13w pour la trésorerie (via cfo-tresorerie)

## Exemple rempli

```markdown
# Flash Mars 2026 — Acme SAS

📅 Arrêté au 31/03/2026 · Publié le 07/04/2026

## 3 highlights
- CA mars : 1,250 M€ (+8% vs M-1, +3% vs budget)
- Signature contrat cadre avec BigCo (500k€ ARR)
- Runway passe de 14 à 18 mois suite à la levée

## 3 lowlights
- Churn client B : -2 comptes en mars (12k€ MRR perdu)
- DSO en hausse : 68j vs 55j cible → 80k€ de cash bloqué supplémentaire
- Dérive masse salariale : +15% vs budget (2 postes non-budgétisés)

## KPIs flash
| KPI | Valeur | vs M-1 | vs Budget |
|-----|--------|--------|-----------|
| CA HT | 1 250 k€ | +8% 🟢 | +3% 🟢 |
| EBITDA | -85 k€ | +25% 🟢 | -50% 🔴 |
| Marge brute | 68% | -2 pts 🟠 | -3 pts 🔴 |
| Cash | 2 450 k€ | -120 k€ | — |
| Runway | 18 mois | +4 🟢 | — |

## Trésorerie
- Solde : 2 450 k€
- Alertes : aucune
- Prochaines échéances critiques : Solde IS 15/05 (~180k€)

## Action de la semaine
→ Relance top 5 créances > 60j par appel direct (potentiel 150k€ encaissés)
```
