# Sources Pappers, documentation API + WebFetch

Pappers est le principal fournisseur de données d'identification société en France. Le bundle utilise Pappers en **mode hybride** : API si une clé est fournie, sinon WebFetch (sans clé).

## Mode hybride

### Mode API (recommandé si usage intensif)

- URL : `https://api.pappers.fr/v2`
- Authentification : `PAPPERS_API_KEY` dans `.env` (header `api-key` ou paramètre `?api_token=`)
- Quota gratuit : **1 000 requêtes/mois** (https://www.pappers.fr/api/tarifs)
- ToS : https://www.pappers.fr/cgu

Avantages :
- Données structurées JSON
- Quota plus élevé et prévisible
- Conditions d'usage formelles
- Pas de risque de scraping cassé par refonte du site

### Mode WebFetch (par défaut, sans clé)

- URL : `https://www.pappers.fr/entreprise/<DENOMINATION-SIREN>`
- Pas d'authentification requise
- ToS : https://www.pappers.fr/cgu, usage non commercial massif interdit, requête raisonnable OK
- Rate limit à respecter : **≤ 1 requête / seconde**

Avantages :
- Zéro configuration pour l'utilisateur
- Permet la démo immédiate

Limitations :
- Dépend du format HTML (risque de parsing qui casse)
- Quota moins généreux en pratique
- Moins de champs structurés

## Données récupérables

| Champ | API | WebFetch | Toujours public |
|-------|-----|----------|-----------------|
| Dénomination | ✓ | ✓ | ✓ |
| SIREN / SIRET | ✓ | ✓ | ✓ |
| Forme juridique | ✓ | ✓ | ✓ |
| Code NAF + libellé | ✓ | ✓ | ✓ |
| Adresse du siège | ✓ | ✓ | ✓ |
| RCS | ✓ | ✓ | ✓ |
| Date de création | ✓ | ✓ | ✓ |
| Statut actif / radié | ✓ | ✓ | ✓ |
| Tranche d'effectif | ✓ | ✓ | ✓ (INSEE) |
| Dirigeants principaux | ✓ | partiel | ✓ |
| Comptes annuels publiés (CA, résultat, bilan) | ✓ | ✓ | ✓ quand publiés |
| Bénéficiaires effectifs | ✓ payant | ✗ | ✓ registre BE |

Tous les champs ci-dessus sont **publics** (RCS, INSEE). Aucun accès à des données internes confidentielles.

## Endpoint API principal

```
GET https://api.pappers.fr/v2/entreprise?siren=552120222&api_token=<API_KEY>
```

Réponse (extrait normalisé) :

```json
{
  "siren": "552120222",
  "nom_entreprise": "CARREFOUR",
  "forme_juridique": "SA à conseil d'administration (s.a.i.)",
  "date_creation": "1959-07-11",
  "code_naf": "4711F",
  "libelle_code_naf": "Hypermarchés",
  "siege": {
    "adresse_ligne_1": "93 AVENUE DE PARIS",
    "code_postal": "91300",
    "ville": "MASSY"
  },
  "tranche_effectif": "10000+",
  "capital": 1855000000,
  "etablissement_cesse": false,
  "finances": [
    {"annee": 2024, "ca": 94880000000, "resultat_net": 1255000000}
  ]
}
```

## Script `scripts/fetch_pappers.py`

Le script détecte automatiquement le mode :
- Si `PAPPERS_API_KEY` dans environnement → mode API
- Sinon → mode WebFetch (avec avertissement sur quota)

```bash
python3 scripts/fetch_pappers.py --siren 552120222 --mode auto
# ou forcer : --mode api / --mode web
```

Output : JSON structuré écrit dans `private/<siren>.pappers.json` ou stdout.

## Gestion des erreurs

| Erreur | Cause | Gestion |
|--------|-------|---------|
| 401 Unauthorized | Clé API invalide ou expirée | Proposer fallback WebFetch |
| 429 Rate limit | Quota mensuel dépassé | Fallback WebFetch + avertir user |
| 404 Not found | SIREN invalide ou radié | Vérifier format SIREN (9 chiffres), tester INSEE |
| 5xx | Panne Pappers | Fallback INSEE Sirene ou annuaire-entreprises.data.gouv.fr |

## Alternative INSEE Sirene

Si Pappers échoue, fallback vers `scripts/fetch_sirene.py` (voir `insee-sirene.md`).

## Conformité RGPD

Les données récupérées via Pappers sont des **données publiques d'entreprise** (RCS + INSEE).

- **Personnes physiques (dirigeants)** : leurs noms sont publics au RCS mais leur utilisation doit rester dans le périmètre légitime du diagnostic CFO. Aucun stockage long-terme au-delà de `private/company.json`.
- **Purge** : `rm -rf private/` supprime toutes les données récupérées.

## Références

- Pappers API docs : https://www.pappers.fr/api/documentation
- CGU Pappers : https://www.pappers.fr/cgu
- Tarifs : https://www.pappers.fr/api/tarifs
- Voir aussi : `../../data/sources.json > categories > identification_societe`
