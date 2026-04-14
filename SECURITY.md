# Politique de sécurité — moriarty-cfo

> 🔒 **Vos données financières restent locales. Aucune ne quitte votre machine.**

## Principe fondamental

`moriarty-cfo` est conçu pour traiter des **données sensibles** (chiffres financiers, contrats, comptes bancaires, données salariés, données clients). Le seul endroit où ces données peuvent être lues, écrites et conservées est **votre machine locale**.

## Données qui transitent à l'extérieur

Seules les **données publiques** sont consultées en ligne, uniquement pour identifier votre société :

| Donnée | Source | Pourquoi |
|--------|--------|----------|
| SIREN / SIRET | Pappers (`api.pappers.fr` ou `pappers.fr`) | Identification légale |
| Dénomination, forme juridique, code NAF | INSEE Sirene V3 (`api.insee.fr` ou `annuaire-entreprises.data.gouv.fr`) | Classification |
| Comptes annuels publiés (le cas échéant) | Pappers / Annuaire Entreprises | Constitution profil |
| Veille réglementaire | Légifrance, Bofip, ANC, IASB, EFRAG | Monitoring textes (skill `cfo-risques-conformite`) |

Toutes ces sources sont **publiques** et l'envoi se limite au numéro SIREN ou aux mots-clés réglementaires. Aucune donnée interne à votre société n'accompagne ces requêtes.

## Données qui restent strictement locales

Tout ce qui touche à votre activité réelle reste dans `private/` :

- Chiffres comptables (balances, journaux, FEC)
- Contrats, factures, devis
- Données salariés, paie, DSN
- Données clients (CRM, factures, encours)
- Comptes bancaires (soldes, mouvements)
- Prévisions de trésorerie, budgets, forecasts
- Cartographies de risques, audits, contrôles
- Dossiers de financement, valorisations

Le dossier `private/` est :
1. **Gitignored** (voir `.gitignore`) — impossible de le commiter par erreur
2. **Hors-champ** des appels externes — aucun outil du bundle n'envoie son contenu en ligne
3. **Effaçable** d'un seul coup via `bash scripts/purge.sh` (à venir)

## Mode hybride API/Web — votre choix

Par défaut, `cfo-init` utilise `WebFetch` (sans clé API) pour Pappers et l'Annuaire Entreprises. Vous pouvez **opter pour les API officielles** en fournissant des clés dans `.env` (gitignored) :

```bash
PAPPERS_API_KEY=votre-clé-pappers
INSEE_API_KEY=votre-clé-insee-sirene
```

Avantages des clés API :
- Quota plus élevé
- Données plus structurées
- Conditions d'usage formelles

Aucune autre clé n'est utilisée. Aucun service tiers n'est appelé sans votre consentement explicite.

## Aucune télémétrie

`moriarty-cfo` ne contient :
- Aucun appel à un serveur d'analytics
- Aucun tracker (Mixpanel, Amplitude, etc.)
- Aucun heartbeat / ping
- Aucun upload de logs

Le seul lien de tracking est le **CTA Moriarty** (skill `cfo-financement-croissance`), affiché uniquement quand le diagnostic financement détecte une éligibilité aux **aides publiques**, et qui contient une **URL pré-construite** que vous pouvez (ou non) visiter manuellement. Le SIREN dans l'URL est **hashé (SHA-256)** pour respecter votre vie privée.

## RGPD

Si votre profil société (`private/company.json`) contient des données à caractère personnel (par exemple noms d'associés mineurs ou informations sensibles sur des salariés) :

- Vous êtes seul **responsable de traitement** au sens du RGPD
- Aucun co-traitant Moriarty ou Anthropic n'intervient sur ce contenu
- Pour purger l'ensemble : `bash scripts/purge.sh` (à venir) ou `rm -rf private/`

## Audit trail (optionnel)

Vous pouvez activer un journal local des opérations dans `private/audit.log` en plaçant `AUDIT=true` dans `.env`. Ce log reste local et n'est jamais transmis.

## Reset complet

```bash
# Efface l'ensemble des données société/cabinet/progression
rm -rf private/
# Relance l'init pour repartir de zéro
# (puis dans Claude : "Lance cfo-init")
```

## Signaler une vulnérabilité

Si vous identifiez une faille de sécurité (fuite de données, appel non documenté, contournement du gitignore, etc.), merci de **ne pas ouvrir d'issue publique**. Écrivez-nous à :

📧 **security@themoriarty.fr** ou via [GitHub Security Advisory](https://github.com/moriarty-fr/moriarty-cfo/security/advisories/new)

Réponse sous 72h ouvrées.

## Limitations & responsabilité

Ce bundle de skills est un **outil d'aide à la décision**. Il ne remplace pas :
- Un expert-comptable inscrit à l'Ordre
- Un commissaire aux comptes
- Un conseiller en investissement financier (CIF) réglementé
- Un avocat fiscaliste
- Un consultant CSRD certifié

Pour toute décision engageant la société (clôture, déclaration fiscale, audit, financement, conformité réglementaire), **consultez systématiquement un professionnel qualifié**.

---

*Dernière mise à jour : 2026-04-14 — moriarty-cfo v0.1.0*
