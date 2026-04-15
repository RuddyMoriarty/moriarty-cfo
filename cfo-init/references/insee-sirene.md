# INSEE Sirene V3, API officielle

Source officielle et authoritative pour l'identification des entreprises françaises. Utilisée en **fallback** quand Pappers n'est pas disponible, ou en complément pour valider les données.

## Endpoints

### API Sirene V3 (OAuth, gratuit)

- URL : `https://api.insee.fr/entreprises/sirene/V3.11`
- Auth : OAuth 2.0 Client Credentials (`INSEE_CONSUMER_KEY` + `INSEE_CONSUMER_SECRET`)
- Tarif : **gratuit** avec inscription sur https://api.insee.fr
- Quota : 500 requêtes/heure par clé

### Annuaire Entreprises (API publique, sans clé)

- URL : `https://recherche-entreprises.api.gouv.fr/v3`
- Auth : **aucune** (API publique data.gouv.fr)
- Tarif : **gratuit**
- Quota : **7 requêtes/seconde, 7 000/jour**
- Docs : https://recherche-entreprises.api.gouv.fr/docs

Cet endpoint est le **plus simple** pour un usage sans authentification : pas de token à gérer, quota confortable. C'est le choix par défaut quand aucune clé API n'est fournie et quand Pappers échoue.

### WebFetch annuaire-entreprises.data.gouv.fr (dernier recours)

- URL : `https://annuaire-entreprises.data.gouv.fr/entreprise/<siren>`
- Auth : aucune
- Type : HTML → parser + extraire

## Script `scripts/fetch_sirene.py`

Essaie dans l'ordre :
1. API Sirene V3 INSEE si clés OAuth fournies
2. API Annuaire Entreprises (`recherche-entreprises.api.gouv.fr`) si pas de clé
3. WebFetch annuaire-entreprises.data.gouv.fr en dernier recours

```bash
python3 scripts/fetch_sirene.py --siren 552120222
# Options :
#   --mode {api-insee|api-annuaire|web|auto}
#   --output private/552120222.sirene.json
```

## Exemple API Annuaire Entreprises (par défaut)

```
GET https://recherche-entreprises.api.gouv.fr/v3/search?q=552120222
```

Extrait de réponse :

```json
{
  "results": [
    {
      "siren": "552120222",
      "nom_complet": "CARREFOUR",
      "nom_raison_sociale": "CARREFOUR",
      "nombre_etablissements": 8,
      "activite_principale": "4711F",
      "tranche_effectif_salarie": "51",
      "categorie_entreprise": "GE",
      "etat_administratif": "A",
      "date_creation": "1959-07-11",
      "siege": {
        "siret": "55212022200013",
        "adresse": "93 AVENUE DE PARIS, 91300 MASSY"
      }
    }
  ],
  "total_results": 1
}
```

**Champs clés pour cfo-init** :
- `categorie_entreprise` : `PME`, `ETI`, `GE` (classification INSEE officielle, utilisée prioritairement)
- `tranche_effectif_salarie` : code INSEE (00 = 0 salarié, 01 = 1-2, …, 53 = 10 000+)
- `activite_principale` : code NAF
- `etat_administratif` : `A` (active) ou `F` (fermée)

## Tranches d'effectif INSEE

| Code | Tranche |
|------|---------|
| NN | Non employeuse ou non renseignée |
| 00 | 0 salarié (pas de DSN) |
| 01 | 1 ou 2 salariés |
| 02 | 3 à 5 salariés |
| 03 | 6 à 9 salariés |
| 11 | 10 à 19 salariés |
| 12 | 20 à 49 salariés |
| 21 | 50 à 99 salariés |
| 22 | 100 à 199 salariés |
| 31 | 200 à 249 salariés |
| 32 | 250 à 499 salariés |
| 41 | 500 à 999 salariés |
| 42 | 1 000 à 1 999 salariés |
| 51 | 2 000 à 4 999 salariés |
| 52 | 5 000 à 9 999 salariés |
| 53 | 10 000 salariés et plus |

## Gestion des erreurs

| Erreur | Cause | Gestion |
|--------|-------|---------|
| 401 INSEE | Token OAuth expiré ou clés invalides | Regénérer token via OAuth flow |
| 429 | Rate limit INSEE 500/h ou Annuaire 7/s | Attendre, changer de source |
| 404 | SIREN n'existe pas | Vérifier format (9 chiffres exactement) |
| 5xx | Panne service | Fallback source suivante |

## OAuth Flow (API INSEE uniquement)

1. Créer un compte sur https://api.insee.fr
2. Créer une application et récupérer `CONSUMER_KEY` + `CONSUMER_SECRET`
3. Obtenir un token :
   ```bash
   curl -X POST https://api.insee.fr/token \
     -H "Authorization: Basic $(echo -n $INSEE_CONSUMER_KEY:$INSEE_CONSUMER_SECRET | base64)" \
     -d "grant_type=client_credentials"
   ```
4. Le token est valable 7 jours, régénérer automatiquement si expiré.

## Comparatif Pappers vs INSEE vs Annuaire Entreprises

| Critère | Pappers API | INSEE Sirene V3 | Annuaire Entreprises |
|---------|-------------|-----------------|----------------------|
| Auth requise | Clé API | OAuth 2.0 | Non |
| Gratuit | 1 000 req/mois | Oui (500/h) | Oui (7 000/jour) |
| Données enrichies (comptes annuels, dirigeants) | ✓ | partiel | partiel |
| Catégorie entreprise officielle | ✓ | ✓ | ✓ |
| Simplicité onboarding | Bonne | Moyenne (OAuth) | Excellente |
| Fiabilité long terme | Dépend Pappers | Officiel | Officiel |

**Recommandation** par défaut :
- Utilisateur qui veut la simplicité → Annuaire Entreprises (aucune clé)
- Utilisateur avancé avec besoin enrichi → Pappers API (1000 req gratuites)
- Production à volume élevé → INSEE Sirene V3 (500/h, gratuit)

## Références

- INSEE Sirene V3 : https://api.insee.fr/catalogue/
- Annuaire Entreprises : https://recherche-entreprises.api.gouv.fr/docs
- Licence Ouverte 2.0 : https://www.etalab.gouv.fr/licence-ouverte-open-licence
- Voir aussi : `../../data/sources.json > categories > identification_societe`
