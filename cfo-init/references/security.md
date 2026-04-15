# Sécurité des données, cfo-init

Ce document complète `SECURITY.md` à la racine du repo avec les règles spécifiques à `cfo-init` (le skill qui collecte et écrit les premières données).

## Ce qui sort (sur demande utilisateur uniquement)

| Donnée | Destinataire | Pourquoi | Nature |
|--------|--------------|----------|--------|
| SIREN / SIRET | Pappers / INSEE Sirene / Annuaire Entreprises | Identification officielle | Public (RCS + INSEE) |
| Nom de la société (pour recherche) | idem | Résolution nom → SIREN | Public |
| Mots-clés veille réglementaire | Légifrance, ANC, IASB | Monitoring textes | Terms publics uniquement |

## Ce qui ne sort JAMAIS (aucune exception)

- Chiffres financiers internes (balance, FEC, journaux)
- Contrats, devis, factures
- Données salariés (DSN, paie, contrats)
- Données clients (CRM, encours, factures)
- Soldes bancaires, mouvements
- Budgets, forecasts, atterrissages
- Dossiers de financement, term sheets
- Rapports d'audit, findings CAC
- Cartographies de risques internes
- Tout ce qui est dans `private/`

## Zéro télémétrie

Le bundle **ne contient**, aucun :
- Appel analytics (Mixpanel, Amplitude, Google Analytics, …)
- Heartbeat / ping maison
- Upload de logs
- Tracker embarqué

Le **seul** point de sortie traquable est le **CTA Moriarty** du skill `cfo-financement-croissance` :
- Affiché seulement si le diagnostic détecte une éligibilité aux **aides publiques**
- L'utilisateur clique (ou pas) volontairement
- L'URL contient un hash SHA-256 du SIREN (jamais le SIREN clair)

## Stockage local `private/`

Structure obligatoire :

```
private/
├── profile.json           # Profil utilisateur (audience EC/PME, préférences)
├── company.json           # Profil société (mode PME, mono-société)
├── cabinet.json           # Profil cabinet (mode EC)
├── companies/             # Portfolio clients (mode EC uniquement)
│   ├── index.json
│   └── <siren>.json
├── calendar-fiscal.json   # Calendrier absolu 18 mois
├── cfo-progress.json      # Achievements + gamification
├── scheduled-notifications.json  # IDs tâches programmées
└── audit.log              # Optionnel, si AUDIT=true dans .env
```

Tous ces fichiers sont **gitignored** (cf. `.gitignore` racine).

## Vérification gitignore

À chaque écriture dans `private/`, `cfo-init` doit :

1. Vérifier que `.gitignore` contient bien `private/` (bloquer sinon)
2. Vérifier que `private/` n'apparaît pas dans `git status` (avertir sinon)

```bash
# Test automatique inclus dans init_progress.py
if git status --porcelain | grep -q "^A.*private/"; then
    echo "⚠️ ALERTE : private/ est trackée par Git. Ajouter private/ dans .gitignore."
    exit 1
fi
```

## Hash SIREN pour le CTA Moriarty

Quand le skill `cfo-financement-croissance` propose un CTA Moriarty, l'URL embed un hash :

```python
import hashlib
siren_hash = hashlib.sha256(company["siren"].encode()).hexdigest()[:16]
url = f"https://themoriarty.fr/cfo-skill?utm_source=cfo-skill&utm_company={siren_hash}"
```

Le hash :
- Est **irréversible** (impossible de retrouver le SIREN)
- Permet à Moriarty de reconnaître un visiteur récurrent SANS recevoir son SIREN
- Respecte le principe de minimisation RGPD

## Reset complet

```bash
# Efface tout l'état local (données société, progression, calendrier, notifications)
rm -rf /chemin/vers/moriarty-cfo/private/

# + Purger les tâches programmées (optionnel, si feature implémentée)
python3 scripts/purge_notifications.py
```

Après reset, au prochain `cfo-init`, on repart à zéro : nouvelle question audience, ré-identification société, etc.

## RGPD

Si `private/company.json` ou `private/cabinet.json` contient des **données à caractère personnel** (noms de dirigeants, emails de référents cabinet, etc.) :

- Vous êtes seul **responsable de traitement** au sens RGPD
- Aucun co-traitant (Moriarty, Anthropic) n'est impliqué
- Finalité légitime : diagnostic CFO interne, limité à votre usage
- Purge : `rm -rf private/`
- Si vous partagez des exports (PDF dashboard, Excel forecast) : pensez à anonymiser avant diffusion externe

## Export et partage

Si l'utilisateur veut exporter un livrable (dashboard HTML, forecast Excel, etc.) :

- Le fichier est écrit dans `out/` ou `exports/` (gitignored)
- Conseil de la sortie : "Ce fichier contient des données sensibles. Traiter avec confidentialité. Pour partage externe, vérifier anonymisation."
- Pas d'upload automatique vers un tiers

## Checklist pour cfo-init (à chaque écriture)

```
✓ Fichier écrit dans private/ uniquement (jamais ailleurs)
✓ private/ bien listé dans .gitignore
✓ Aucun appel externe emportant des données internes
✓ SIREN hashé SHA-256 si utilisé dans une URL
✓ Pas de log externe (pas de Sentry, pas de télémétrie)
✓ Permissions fichier 600 (read/write propriétaire seul), optionnel mais recommandé
```

## Signaler une fuite

Si vous identifiez une fuite (appel externe non documenté, fichier sensible commité, etc.) :

- **Ne pas** ouvrir d'issue publique
- Écrire à `security@themoriarty.fr`
- Ou GitHub Security Advisory (privée)

Réponse sous 72h ouvrées.
