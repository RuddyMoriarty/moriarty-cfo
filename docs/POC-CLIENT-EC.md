# POC Client Cabinet EC, guide de test bout en bout

Guide destine a un collaborateur Senior ou Manager de cabinet d'expertise comptable qui veut tester le bundle `moriarty-cfo` en mode portfolio multi-clients. 10 scenarios en 45 minutes, de l'init du cabinet a la generation du dashboard hebdomadaire des alertes.

L'objectif : valider que le bundle tient le stress d'un portfolio de 50 a 200 clients avant de l'utiliser sur votre vraie base.

**Versions validees contre le bundle** : v0.3.6+ (si v0.2.x, certaines commandes differeront).

## Prerequis

```bash
git clone https://github.com/RuddyMoriarty/moriarty-cfo.git
cd moriarty-cfo
python3 evals/run_evals.py --full      # Doit afficher 100 % PASS
```

Aucune cle API requise. Optionnel : `PAPPERS_API_KEY` pour les fiches societe detaillees (500 req / mois gratuits chez Pappers), sinon l'API Annuaire Entreprises (gratuite) suffit.

## Scenario 1, Initialisation du cabinet (1 min)

```bash
./cfo init-cabinet \
  --siren 789456123 \
  --denomination "CABINET DURAND & ASSOCIES" \
  --forme selarl \
  --ville Nancy \
  --fetch
```

**Ce que vous verifiez** :
- `private/cabinet.json` cree, enrichi par l'API Annuaire Entreprises si `--fetch` reussit (sinon warning et continue avec valeurs fournies)
- `private/profile.json` avec `audience_type=ec_collaborateur`
- `private/companies/index.json` initialise : `{"_meta": {...}, "clients": []}`

## Scenario 2, Ajout de 5 clients au portfolio (3 min)

**Missions supportees** : `presentation`, `examen_limite`, `audit_legal_cac`, `cir_cii`, `conseil_financier`, `csrd_esrs`, `m_and_a`, `juridique`, `social_paie`, `aides_publiques`.

```bash
./cfo portfolio-add \
  --siren 552120222 --denomination "BOULANGERIE MARTIN" \
  --taille tpe --secteur commerce --cloture 2026-12-31 \
  --mission presentation --referent "Jean Dupont"

./cfo portfolio-add \
  --siren 451001234 --denomination "MENUISERIE DUBOIS SARL" \
  --taille pe --secteur industrie --cloture 2026-06-30 \
  --mission examen_limite --referent "Marie Lefort"

./cfo portfolio-add \
  --siren 732005678 --denomination "CONSEIL CROISSANCE SAS" \
  --taille pe --secteur services_btob --cloture 2026-12-31 \
  --mission presentation --referent "Pierre Blanc"

./cfo portfolio-add \
  --siren 884009876 --denomination "TECH INNOVATIONS SA" \
  --taille me --secteur saas_techno --cloture 2026-12-31 \
  --mission audit_legal_cac --referent "Sophie Dupuis"

./cfo portfolio-add \
  --siren 555010111 --denomination "GARAGE LEFEVRE" \
  --taille tpe --secteur commerce --cloture 2026-03-31 \
  --mission social_paie --referent "Jean Dupont"
```

**Ce que vous verifiez** : `private/companies/index.json` a 5 entrees `clients[]`, chacune avec son dossier `private/companies/<siren>/` contenant `company.json`.

## Scenario 3, Listing du portfolio (1 min)

```bash
./cfo portfolio-list                     # Vue compacte tableau
./cfo portfolio-list --detailed          # Vue complete par client
./cfo portfolio-list --status actif      # Filtre statut
```

**Ce que vous verifiez** : tableau `SIREN | Denomination | Taille | Mission | Statut | Routines`, vue detaillee liste les routines et la prochaine echeance.

## Scenario 4, Planification batch des routines (3 min)

```bash
./cfo portfolio-schedule-all --dry-run   # Analyse sans ecriture
./cfo portfolio-schedule-all             # Execution reelle
```

**Ce que vous verifiez** : le script itere sur les 5 clients actifs, appelle `compute_entity_routines` + `schedule_routines` pour chacun, affiche `Resume: X/5 OK`. Les `private/companies/<siren>/routines.json` sont mis a jour.

## Scenario 5, Dashboard portfolio hebdomadaire (1 min)

```bash
./cfo portfolio-dashboard --output /tmp/portfolio-dashboard.html

open /tmp/portfolio-dashboard.html       # macOS
# xdg-open /tmp/portfolio-dashboard.html  # Linux
```

**Ce que vous verifiez** : HTML A4 landscape avec :

- En-tete cabinet (denomination, SIREN, date generation)
- Alertes : echeances < 7 j (rouge), 7-14 j (orange), 15-30 j (jaune)
- Resume textuel : "Cette semaine : X clotures, Y relances..."
- Tableau portfolio : 5 clients triables par echeance
- Footer : version bundle

Pour export PDF (necessite Chrome/Chromium installe) :

```bash
./cfo portfolio-dashboard --output /tmp/portfolio-dashboard.html --pdf
```

## Scenario 6, Verification dossier client (2 min)

Le bundle lit les pieces deja recues depuis `private/companies/<siren>/pieces.json` et les compare au catalogue `data/pieces-dossier.json` selon la mission.

```bash
# Declarer les pieces recues pour BOULANGERIE MARTIN (mission presentation, 10 pieces attendues)
cat > private/companies/552120222/pieces.json <<'EOF'
{
  "pieces_recues": {
    "balance_comptable": {"recu": true},
    "grand_livre": {"recu": true},
    "fec": {"recu": true},
    "contrats_cles": {"recu": true},
    "inventaires": {"recu": true}
  }
}
EOF

./cfo portfolio-check-dossier --siren 552120222 --json
```

**Ce que vous verifiez** : JSON avec `total_attendues`, `recues`, `manquantes_obligatoires` (liste d'IDs), `dossier_complet` (bool). Mode sans `--json` donne une sortie texte plus lisible.

**Mode strict** pour CI/audit :

```bash
./cfo portfolio-check-dossier --siren 552120222 --strict    # Exit 2 si incomplet
```

## Scenario 7, Generation relance mail (1 min)

Le bundle calcule les pieces manquantes depuis `pieces.json` (scenario 6) et genere le mail.

```bash
./cfo portfolio-relance \
  --siren 552120222 \
  --type premiere \
  --date-echeance 2026-05-15 \
  --jours-delai 15 \
  --output /tmp/relance.txt

cat /tmp/relance.txt
```

**Ce que vous verifiez** : mail court, vouvoiement, pieces manquantes listees, delai implicite. Variante :

```bash
./cfo portfolio-relance --siren 552120222 --type urgente --date-echeance 2026-05-15 --jours-delai 5 --output /tmp/relance-urgente.txt
```

## Scenario 8, Lettre de mission versionnee (2 min)

```bash
./cfo portfolio-lettre-mission \
  --siren 552120222 \
  --honoraires 4500 \
  --exercice 2026 \
  --representant-client "Jean Dupont"
```

**Ce que vous verifiez** : fichier `private/companies/552120222/lettres-mission/v1.md` + `metadata.json`. La version s'auto-incremente : relancer pour une v2 :

```bash
./cfo portfolio-lettre-mission --siren 552120222 --honoraires 5000 --exercice 2026 --new-version
```

**Templates disponibles en v0.3.6** : `presentation`, `examen-limite`, `social-paie`. Pour les 7 autres missions (`audit_legal_cac`, `cir_cii`, `conseil_financier`, `csrd_esrs`, `m_and_a`, `juridique`, `aides_publiques`), le bundle utilise le template `presentation` en fallback avec un warning qui pointe vers les normes a consulter manuellement (NEP 2300 pour CAC, CGI 244 quater B pour CIR, etc).

## Scenario 9, Suivi encaissements LME (1 min)

Le bundle lit `private/companies/<siren>/factures.json` (format : liste de factures avec `numero`, `date_emission`, `montant_ht`, `statut`) et classe par bucket LME (< 30 j, 30-60 j, 60-90 j, > 90 j).

```bash
cat > private/companies/552120222/factures.json <<'EOF'
{
  "factures": [
    {"numero": "F001", "date_emission": "2026-01-15", "montant_ht": 3500, "statut": "encaissee"},
    {"numero": "F002", "date_emission": "2026-02-10", "montant_ht": 8200, "statut": "en_attente"},
    {"numero": "F003", "date_emission": "2025-12-20", "montant_ht": 15000, "statut": "en_attente"},
    {"numero": "F004", "date_emission": "2025-11-30", "montant_ht": 22000, "statut": "en_attente"}
  ]
}
EOF

./cfo portfolio-aging --json --ref-date 2026-04-17
```

**Ce que vous verifiez** : JSON avec 4 buckets (`a_jour`, `echu_30_60`, `echu_60_90`, `echu_sup_90`), chaque bucket avec `count` et `montant_ht`, plus `total_non_encaisse_ht` et `encaissees`. Conforme L. 441-10 du Code de commerce.

**Mode texte** avec alertes visibles :

```bash
./cfo portfolio-aging --ref-date 2026-04-17
./cfo portfolio-aging --siren 552120222 --detailed --ref-date 2026-04-17
```

## Scenario 10, Suivi forfaits vs temps passe (2 min)

Le bundle lit deux fichiers par client :
- `private/companies/<siren>/forfait.json` : `{forfait_heures: N, mission_type: "..."}`
- `private/companies/<siren>/temps-passes.json` : `{saisies: [{date, collaborateur, heures, tache}, ...]}`

Les heures consommees sont sommees sur l'annee courante depuis les saisies.

```bash
# 1. Declarer les forfaits annuels par client
cat > private/companies/552120222/forfait.json <<'EOF'
{"mission_type": "presentation", "forfait_heures": 40, "annee": "2026"}
EOF
cat > private/companies/451001234/forfait.json <<'EOF'
{"mission_type": "examen_limite", "forfait_heures": 60, "annee": "2026"}
EOF

# 2. Declarer les temps passes par saisies
cat > private/companies/552120222/temps-passes.json <<'EOF'
{
  "saisies": [
    {"date": "2026-01-15", "collaborateur": "Alice", "heures": 10, "tache": "cloture decembre"},
    {"date": "2026-02-20", "collaborateur": "Alice", "heures": 15, "tache": "TVA janvier"},
    {"date": "2026-03-10", "collaborateur": "Bob",   "heures": 8, "tache": "paie fevrier"}
  ]
}
EOF

# 3. Lancer le tracker
./cfo portfolio-forfait --json
```

**Ce que vous verifiez** : JSON avec une entree par client `{siren, denomination, forfait_heures, heures_consommees, pct_consomme, statut}`. Statuts : `ok` (< 70 %), `vigilance` (70-90 %), `limite_atteinte` (90-100 %), `depassement` (>= 100 %).

**Mode texte** avec tableau :

```bash
./cfo portfolio-forfait
./cfo portfolio-forfait --detailed --siren 552120222    # Detail saisies
```

## Ce qui devrait fonctionner a 100 %

Si les 10 scenarios passent sans erreur, le bundle est pret pour votre vrai portfolio. Remplacer les SIREN et fixtures fictifs par vos vrais clients.

## Deploiement en cabinet

### Phase 1, un collaborateur, 10 clients (semaine 1)
- Choisir un collaborateur Senior pilote qui connait bien 10 clients varies.
- Deployer le bundle sur son poste, initialiser le cabinet et importer 10 clients.
- Mesurer le temps gagne sur la preparation du dashboard hebdomadaire (reference : combien de minutes actuellement ?).

### Phase 2, toute l'equipe, 50-100 clients (semaines 2 a 4)
- Dupliquer le repo sur les postes des Seniors et Managers.
- Ecrire une procedure interne cabinet pour l'ajout d'un nouveau client (10 min pour le faire proprement).
- Integrer le dashboard hebdomadaire dans le COMEX du lundi matin.

### Phase 3, portfolio complet (mois 2)
- Migrer les 200+ clients du cabinet.
- Automatiser la synchro depuis votre outil de facturation via un import CSV hebdomadaire.
- Creer un referentiel cabinet de `references/*.md` specifiques (charte honoraires, modeles lettres de mission internes).

## Ce qu'il faut signaler

- **Error "Traceback"** : bug script → issue https://github.com/RuddyMoriarty/moriarty-cfo/issues avec stderr complete
- **Donnees clients confidentielles exposees** : incident critique, fermer une issue en mode prive et contacter ruddy@workcuts.fr
- **Calcul juridique ou fiscal errone** (ex: seuil LME incorrect, norme OEC mal citee) : issue prioritaire avec texte de reference
- **Template lettre de mission manquant** : pour les 7 missions non encore specialisees (v0.3.6), le fallback presentation est utilise avec warning. Contribuer un template specialise via PR accelere la maturite du bundle.

## Securite

Toutes vos donnees clients (CA, salaires, contrats, comptes bancaires) vivent dans `private/` qui est gitignore. Rien ne quitte votre poste sauf les donnees publiques SIREN via l'API Annuaire. Voir [SECURITY.md](../SECURITY.md) pour la politique complete, notamment la procedure de reset / purge.

## Contact

Issues techniques : https://github.com/RuddyMoriarty/moriarty-cfo/issues

Demande d'accompagnement au deploiement cabinet : ruddy@workcuts.fr (reponse sous 48 h ouvrees).
