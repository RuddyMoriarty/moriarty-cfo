# POC Client Cabinet EC, guide de test bout en bout

Guide destine a un collaborateur Senior ou Manager de cabinet d'expertise comptable qui veut tester le bundle `moriarty-cfo` en mode portfolio multi-clients. 10 scenarios en 45 minutes, de l'init du cabinet a la generation du dashboard hebdomadaire des alertes.

L'objectif : valider que le bundle tient le stress d'un portfolio de 50 a 200 clients avant de l'utiliser sur votre vraie base.

## Prerequis

```bash
# Cloner le repo (public)
git clone https://github.com/RuddyMoriarty/moriarty-cfo.git
cd moriarty-cfo

# Sante du bundle
python3 evals/run_evals.py --full      # Doit afficher 350/350 PASS
```

Aucune cle API requise. Optionnel : `PAPPERS_API_KEY` si compte Pappers (500 req / mois gratuits) pour les fiches detaillees, sinon l'API Annuaire Entreprises (gratuite) suffit.

## Scenario 1, Initialisation du cabinet (1 min)

**But** : creer la fiche cabinet et l'index portfolio vide.

```bash
./cfo init-cabinet \
  --siren 123456789 \
  --denomination "CABINET DURAND & ASSOCIES" \
  --forme selarl \
  --ville Nancy \
  --fetch
```

**Ce que vous verifiez** :
- `private/cabinet.json` cree avec le squelette depuis `cabinet.template.json`, enrichi par les donnees INSEE si `--fetch` reussit.
- `private/profile.json` avec `audience_type=ec_collaborateur`.
- `private/companies/index.json` vide (`[]`) pret a recevoir les clients.

## Scenario 2, Ajout de 5 clients au portfolio (3 min)

**But** : alimenter l'index avec une base de test variee (TPE / PE / ME, secteurs varies, missions differentes).

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
  --mission audit --referent "Sophie Dupuis"

./cfo portfolio-add \
  --siren 555010111 --denomination "GARAGE LEFEVRE" \
  --taille tpe --secteur commerce --cloture 2026-03-31 \
  --mission social_paie --referent "Jean Dupont"
```

**Ce que vous verifiez** : `private/companies/index.json` a desormais 5 entrees, chacune avec son `company.json` cree dans `private/companies/<siren>/`.

## Scenario 3, Listing du portfolio (1 min)

**But** : afficher la vue compacte et la vue detaillee.

```bash
# Vue compacte
./cfo portfolio-list

# Vue detaillee
./cfo portfolio-list --detailed

# Filtrer sur un statut
./cfo portfolio-list --status actif
```

**Ce que vous verifiez** : tableau avec colonnes `SIREN | Denomination | Taille | Mission | Prochaine echeance | Routines`. La vue detaillee liste les routines par client.

## Scenario 4, Planification batch des routines (3 min)

**But** : calculer et programmer les routines recurrentes pour tous les clients actifs.

```bash
# Dry-run d'abord (aucune ecriture)
./cfo portfolio-schedule-all --dry-run

# Execution reelle
./cfo portfolio-schedule-all
```

**Ce que vous verifiez** : le script itere sur les 5 clients, appelle `compute_entity_routines.py` + `schedule_routines.py` pour chacun, affiche un resume `X clients, Y routines programmees, Z deja a jour`. Les `private/companies/<siren>/routines.json` sont mis a jour.

## Scenario 5, Dashboard portfolio HTML (1 min)

**But** : generer la vue d'ensemble hebdomadaire pour le Manager.

```bash
./cfo portfolio-dashboard \
  --output /tmp/portfolio-dashboard.html

open /tmp/portfolio-dashboard.html      # macOS
# xdg-open /tmp/portfolio-dashboard.html  # Linux
```

**Ce que vous verifiez** : HTML A4 landscape avec :

- **Alertes** : echeances < 7 jours (rouge), 7-14 j (orange), 15-30 j (jaune).
- **Resume** : "Cette semaine : X clotures, Y relances, Z audits en cours".
- **Tableau portfolio** : 5 clients triables par echeance, mission, referent.
- **Footer** : version bundle + date de generation.

## Scenario 6, Verification d'un dossier client incomplet (2 min)

**But** : lister les pieces manquantes avant une cloture ou un examen limite.

```bash
# Scenario : le client BOULANGERIE MARTIN declare 5 pieces sur 8 attendues pour une presentation
cat > /tmp/pieces-declarees.csv <<'CSV'
piece,present
balance_comptable,oui
grand_livre,oui
fec,oui
pv_ag,non
lettre_affirmation,non
contrats_cles,oui
inventaires,oui
rapprochements_bancaires,non
CSV

./cfo portfolio-check-dossier \
  --siren 552120222 \
  --mission presentation \
  --pieces-declarees /tmp/pieces-declarees.csv \
  --output /tmp/check-dossier.json

python3 -c "
import json
d = json.load(open('/tmp/check-dossier.json'))
print(f\"Completude : {d['completude_pct']:.0f} %\")
print(f\"Pieces manquantes ({len(d['manquantes'])}):\")
for p in d['manquantes']:
    print(f\"  - {p}\")
"
```

**Ce que vous verifiez** : le script compare aux pieces declarees au catalogue (`data/pieces-dossier.json`) pour la mission `presentation`, calcule un % de completude, liste les manquantes.

## Scenario 7, Generation d'une relance mail (1 min)

**But** : produire un mail de relance formule professionnellement pour un client en retard sur ses pieces.

```bash
./cfo portfolio-relance \
  --siren 552120222 \
  --type premiere \
  --pieces-manquantes "PV AG" "Lettre d'affirmation" "Rapprochements bancaires" \
  --echeance-mission 2026-05-15 \
  --output /tmp/relance.txt

cat /tmp/relance.txt
```

**Ce que vous verifiez** : un mail court, factuel, en vouvoiement, avec les 3 pieces listees et un delai implicite. Deuxieme execution avec `--type urgente` donne une formulation plus ferme.

## Scenario 8, Lettre de mission versionnee (2 min)

**But** : generer une lettre de mission NP 2300 ou 2400 pret a signer.

```bash
./cfo portfolio-lettre-mission \
  --siren 884009876 \
  --type np_2400 \
  --honoraires 18000 \
  --duree-annees 1 \
  --output /tmp/lettre-mission.md

head -40 /tmp/lettre-mission.md
```

**Ce que vous verifiez** : lettre conforme aux normes OEC (Ordre des Experts-Comptables), avec clauses obligatoires (renouvellement, honoraires, facturation, confidentialite, protection des donnees, resiliation). Fichier versionne en `private/companies/884009876/lettres-mission/NP2400-v1.md`.

## Scenario 9, Suivi encaissements LME (1 min)

**But** : detecter les factures client en retard de paiement selon les seuils LME art. L. 441-10.

```bash
cat > /tmp/factures.csv <<'CSV'
id_facture,client,date_emission,montant_ht,date_reglement_attendue,statut
F001,Boulangerie Martin,2026-01-15,3500,2026-02-14,paye
F002,Menuiserie Dubois,2026-02-10,8200,2026-03-12,en_attente
F003,Conseil Croissance,2025-12-20,15000,2026-01-19,en_attente
F004,Tech Innovations,2025-11-30,22000,2025-12-30,en_attente
F005,Garage Lefevre,2026-03-01,1200,2026-03-31,en_attente
CSV

./cfo portfolio-aging \
  --factures /tmp/factures.csv \
  --ref-date 2026-04-17 \
  --output /tmp/aging.json

python3 -c "
import json
d = json.load(open('/tmp/aging.json'))
print(f\"Buckets LME :\")
for bucket, data in d.get('buckets', {}).items():
    print(f\"  {bucket}: {data.get('nb', 0)} factures / {data.get('total_ht', 0):,.0f} €\")
"
```

**Ce que vous verifiez** : 4 buckets (`a_jour`, `echu_0_30`, `echu_30_60`, `echu_60_90`, `echu_sup_90`), avec les montants en retard. Conforme a l'article L. 441-10 du Code de commerce.

## Scenario 10, Suivi forfaits vs reel (2 min)

**But** : tracer la consommation temps vs forfait commercial pour chaque client, detecter les depassements.

```bash
cat > /tmp/forfaits.csv <<'CSV'
siren,denomination,forfait_heures,heures_consommees,statut
552120222,Boulangerie Martin,40,32,actif
451001234,Menuiserie Dubois,60,67,actif
732005678,Conseil Croissance,30,15,actif
884009876,Tech Innovations,120,95,actif
555010111,Garage Lefevre,20,20,actif
CSV

./cfo portfolio-forfait \
  --forfaits /tmp/forfaits.csv \
  --seuil-vigilance 80 \
  --seuil-limite 100 \
  --output /tmp/forfaits.json

python3 -c "
import json
d = json.load(open('/tmp/forfaits.json'))
for c in d.get('clients', []):
    print(f\"{c['denomination']:<30} {c['heures_consommees']:>3}/{c['forfait_heures']:>3} h ({c['statut']})\")
"
```

**Ce que vous verifiez** : 4 statuts possibles (`ok`, `vigilance`, `limite_atteinte`, `depassement`), calcules selon les seuils 80 % et 100 %. Menuiserie Dubois doit apparaitre en `depassement` (67 / 60 h).

## Ce qui devrait fonctionner a 100 %

Si les 10 scenarios passent sans erreur, le bundle est pret pour votre vrai portfolio. Remplacer simplement les SIREN et denominations fictifs par vos vrais clients.

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

Si un scenario echoue :

- **Error "Traceback"** : bug script, ouvrir une issue https://github.com/RuddyMoriarty/moriarty-cfo/issues.
- **Donnees clients confidentielles exposees** : incident critique, fermer une issue en mode prive et contacter ruddy@workcuts.fr.
- **Calcul juridique ou fiscal errone** (ex: seuil LME incorrect, norme OEC mal citee) : issue prioritaire avec le texte de reference.

## Securite

Toutes vos donnees clients (CA, salaires, contrats, comptes bancaires) vivent dans `private/` qui est gitignore. Rien ne quitte votre poste sauf les donnees publiques SIREN via l'API Annuaire. Voir [SECURITY.md](../SECURITY.md) pour la politique complete, notamment la procedure de reset / purge.

## Contact

Issues techniques : https://github.com/RuddyMoriarty/moriarty-cfo/issues

Demande d'accompagnement au deploiement cabinet : ruddy@workcuts.fr (reponse sous 48 h ouvrees).
