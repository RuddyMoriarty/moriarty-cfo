# POC Client PME, guide de test bout en bout

Guide destine a un dirigeant ou CFO interne de PME qui veut tester le bundle `moriarty-cfo` dans ses conditions reelles. 10 scenarios en 30 a 45 minutes, sans besoin de donnees confidentielles : chaque scenario fournit des valeurs fictives mais realistes.

L'objectif : valider que le bundle repond a vos questions reelles de gestion avant de l'utiliser sur vos vrais chiffres.

## Prerequis

```bash
# Cloner le repo (public)
git clone https://github.com/RuddyMoriarty/moriarty-cfo.git
cd moriarty-cfo

# Tests auto verifient la sante du bundle (doit repondre PASS)
python3 evals/run_evals.py --full
```

Aucune cle API requise pour ce POC. Optionnel : `PAPPERS_API_KEY` si vous avez un compte Pappers (500 req / mois gratuits) pour les fiches societe detaillees, sinon on utilise l'API Annuaire Entreprises (gratuite, sans compte).

## Scenario 1, Initialisation rapide de votre societe (2 min)

**But** : creer votre profil PME en une commande, avec donnees publiques auto-remplies depuis l'INSEE.

```bash
python3 cfo-init/scripts/init_pme.py \
  --siren 552120222 \
  --denomination "ACME SAS" \
  --role cfo \
  --cloture 2026-12-31 \
  --fetch
```

**Ce que vous verifiez** :
- Le terminal affiche `✓ Annuaire Entreprises : ... (NAF X, tranche effectif Y)`.
- Le fichier `private/companies/552120222/company.json` existe et contient `classification.naf_code`, `classification.effectif_tranche_insee`, `annuaire_entreprises.nombre_etablissements`.
- Vos donnees ne sortent jamais : tout reste dans `private/`, qui est gitignore.

**Variante** : remplacez 552120222 par le SIREN de votre societe pour voir les vraies donnees INSEE de votre entreprise.

## Scenario 2, Calendrier fiscal automatique (1 min)

**But** : obtenir votre calendrier d'echeances fiscales et sociales pour les 18 prochains mois.

```bash
python3 cfo-init/scripts/compute_calendar.py \
  --closing-date 2026-12-31 \
  --tva-regime reel_normal_mensuelle \
  --is-regime is \
  --effectif 25 \
  --output private/companies/552120222/calendar-fiscal.json

# Lire les 5 prochaines echeances
python3 -c "
import json
d = json.load(open('private/companies/552120222/calendar-fiscal.json'))
for e in d['echeances'][:5]:
    print(f\"{e['date']} : {e['label']} ({e.get('nature','?')})\")"
```

**Ce que vous verifiez** : les dates TVA (le 24 du mois), URSSAF/DSN (le 15), acomptes IS (15/03, 15/06, 15/09, 15/12), solde IS (15/05), correspondent bien a votre regime.

## Scenario 3, Calcul BFR et DSO/DPO/DIO (2 min)

**But** : mesurer votre cycle de conversion de cash et le benchmarker.

```bash
python3 cfo-tresorerie/scripts/bfr_calculator.py \
  --creances-clients 200000 --dettes-fournisseurs 100000 \
  --ca-ttc 1200000 --achats-ttc 400000 \
  --stocks 50000 --cout-ventes 300000 \
  --secteur services_btob \
  --output /tmp/bfr.json

python3 -c "
import json
d = json.load(open('/tmp/bfr.json'))
r = d['ratios']
print(f\"DSO {r['dso']:.0f} j | DPO {r['dpo']:.0f} j | DIO {r['dio']:.0f} j | BFR {r['bfr']:,.0f} €\")
for k, v in d['benchmark'].items():
    if isinstance(v, str):
        print(f\"  {k}: {v}\")
"
```

**Ce que vous verifiez** : le bundle calcule DSO = 61 j, DPO = 91 j, BFR = 150 k€ et benchmark versus mediane services B2B (Banque de France).

## Scenario 4, Forecast tresorerie 13 semaines (2 min)

**But** : projeter votre position cash semaine par semaine et identifier un point bas.

```bash
python3 cfo-tresorerie/scripts/forecast_13w.py \
  --solde-initial 150000 \
  --encaissements-moyen 80000 \
  --decaissements-moyen 75000 \
  --output /tmp/fc13.json

python3 -c "
import json
d = json.load(open('/tmp/fc13.json'))
print(f\"Niveau alerte : {d['niveau_alerte']}\")
for s in d['semaines'][::3]:
    print(f\"  S{s['semaine']:2d} ({s['date_fin']}) : {s['solde_fin']:>10,.0f} €\")
"
```

**Ce que vous verifiez** : une colonne `solde_fin` evolue coherente, un `niveau_alerte` dans `{healthy_vert, vigilance_jaune, plan_action_orange, urgence_rouge}`.

## Scenario 5, Reporting mensuel avec dashboard HTML (3 min)

**But** : produire un tableau de bord 5 KPIs pret a envoyer au board ou a imprimer.

```bash
# Fournir un JSON de KPIs (fictif pour le POC)
cat > /tmp/kpis.json <<'JSON'
{
  "CA_HT": 850000,
  "MARGE_BRUTE_PCT": 42,
  "EBITDA": 95000,
  "EBITDA_PCT": 11.2,
  "DSO_JOURS": 58,
  "TRESORERIE": 180000,
  "MOIS": "Mars 2026",
  "DENOMINATION": "ACME SAS"
}
JSON

python3 cfo-reporting/scripts/generate_dashboard.py \
  --kpis /tmp/kpis.json \
  --output /tmp/dashboard-march.html

# Ouvrir dans votre navigateur
open /tmp/dashboard-march.html  # macOS
# xdg-open /tmp/dashboard-march.html  # Linux
```

**Ce que vous verifiez** : un HTML A4 landscape avec les 5 KPIs en chiffres et placeholders remplis, charte discrete.

## Scenario 6, Budget annuel 3 scenarios (2 min)

**But** : batir un budget N+1 avec croissance reglable + scenario optimiste/realiste/pessimiste.

```bash
cat > /tmp/pnl-n1.csv <<'CSV'
poste,montant_annuel
ca_ht,10000000
charge_personnel,4500000
charge_achats,2500000
charge_externes,1200000
charge_amortissements,400000
CSV

python3 cfo-budget-forecast/scripts/budget_builder.py \
  --pnl-n1 /tmp/pnl-n1.csv \
  --growth-ca 12 \
  --growth-charges 8 \
  --marge-cible 18 \
  --output /tmp/budget.json

python3 -c "
import json
d = json.load(open('/tmp/budget.json'))
for label, s in d['scenarios'].items():
    print(f\"{label:>10} : CA {s['ca_ht_annuel']:>12,.0f} € | EBITDA {s['ebitda_annuel']:>10,.0f} € ({s['marge_ebitda_pct']:.1f} %)\")
p = d['pondere_20_60_20']
print(f\"Pondere 20/60/20 : CA {p['ca_ht_annuel']:,.0f} € / EBITDA {p['ebitda_annuel']:,.0f} €\")
"
```

**Ce que vous verifiez** : 3 scenarios coherents, marge EBITDA cible respectee sur le scenario realiste, ponderation 20/60/20 affichee.

## Scenario 7, Estimation CIR (2 min)

**But** : estimer le Credit Impot Recherche eligible a partir de vos salaires chercheurs.

```bash
python3 cfo-fiscalite/scripts/cir_estimator.py \
  --salaires-chercheurs 200000 \
  --frais-fonctionnement-pct 43 \
  --sous-traitance-agreee 50000 \
  --output /tmp/cir.json

python3 -c "
import json
d = json.load(open('/tmp/cir.json'))
print(f\"Base CIR : {d['base_cir_eligible']:,.0f} €\")
print(f\"CIR 30 % : {d['cir_estime']:,.0f} €\")
print(f'Articles CGI cites : {d.get(\"references_cgi\", [])[:3]}')
"
```

**Ce que vous verifiez** : base incluant le forfait 43 % fonctionnement + sous-traitance, CIR = 30 % jusqu'a 100 M€ (CGI art. 244 quater B).

## Scenario 8, Cartographie risques (COSO ERM) (3 min)

**But** : obtenir une matrice 5x5 risques + top 10 priorise.

```bash
cat > /tmp/risques.csv <<'CSV'
id,libelle,categorie,probabilite,impact,owner
R001,Perte client majeur > 20% CA,commercial,3,5,dir_commercial
R002,Cyberattaque ransomware,cyber,2,5,dsi
R003,Depart CTO,rh,3,4,dg
R004,Rupture approvisionnement matiere premiere,achats,4,3,directeur_operations
R005,Non-conformite RGPD,juridique,2,4,dpo
R006,Redressement URSSAF,fiscal,2,3,daf
R007,Rappel produit qualite,qualite,1,5,qualite
R008,Changement loi de finance defavorable,fiscal,3,3,daf
R009,Greve transporteur,logistique,3,2,logistique
R010,Litige client,juridique,3,3,juridique
CSV

python3 cfo-risques-conformite/scripts/risk_mapping_generator.py \
  --risques /tmp/risques.csv \
  --output /tmp/risk-map.json

python3 -c "
import json
d = json.load(open('/tmp/risk-map.json'))
print(f\"Risques traites : {d['nb_risques_total']}\")
print(f\"Repartition : {d['repartition_severite']}\")
print('Top 3 :')
for r in d['top_10_risques'][:3]:
    print(f\"  {r['id']} ({r['severite']}) : {r['libelle']}\")
"
```

**Ce que vous verifiez** : matrice 5x5 (25 cellules), top 10 trie par score = proba x impact, severite calibree critique / eleve / moyen / faible.

## Scenario 9, Determination scope CSRD (1 min)

**But** : savoir si votre societe est concernee par la CSRD et dans quelle wave.

```bash
python3 cfo-csrd-esg/scripts/csrd_scope_calculator.py \
  --effectif 300 \
  --ca-eur 50000000 \
  --bilan-eur 30000000 \
  --output /tmp/csrd.json

python3 -c "
import json
d = json.load(open('/tmp/csrd.json'))
print(f\"Wave CSRD : {d['wave']}\")
print(f\"Directive : {d.get('directive_applicable')}\")
print(f\"Premier exercice : {d.get('premier_exercice_reporting')}\")
"
```

**Ce que vous verifiez** : wave calculee selon vos 3 criteres (effectif, CA, bilan), conformement a la directive 2022/2464 et a ses mises a jour.

## Scenario 10, Diagnostic financement + passerelle Moriarty (2 min)

**But** : identifier les solutions de financement eligibles pour un projet chiffre.

```bash
python3 cfo-financement-croissance/scripts/diagnostic_financement.py \
  --besoin-eur 200000 \
  --duree-mois 36 \
  --projet "R&D machine-outil 4.0" \
  --effectif 25 \
  --secteur industrie \
  --dilutif-ok non \
  --output /tmp/diag.json

python3 -c "
import json
d = json.load(open('/tmp/diag.json'))
print(f\"Top 3 solutions :\")
for s in d.get('solutions_top_3', [])[:3]:
    print(f\"  - {s.get('nom')} ({s.get('type')}) : {s.get('montant_max_eur', '?')} €\")
print(f\"Aides publiques potentielles : {len(d.get('aides_publiques_eligibles', []))}\")
"
```

**Ce que vous verifiez** : top 3 avec BPI France 2030 ou aides ADEME/region selon secteur, plus un lien vers Moriarty pour audit approfondi (hash SIREN, pas d'expo du SIREN brut).

## Ce qui devrait fonctionner a 100 %

Si les 10 scenarios passent sans erreur, le bundle est pret a etre utilise sur vos vrais chiffres. Remplacer simplement les fixtures `/tmp/*.csv` et `/tmp/*.json` par vos fichiers reels dans `private/`.

## Ce qu'il faut signaler

Si un scenario echoue :

- **Error "Traceback"** : bug script, ouvrir une issue https://github.com/RuddyMoriarty/moriarty-cfo/issues avec la stderr complete.
- **Exit non-zero silencieux** : scenario de robustesse insuffisant, ouvrir une issue avec l'input fourni et l'output attendu.
- **Output faux** (chiffre incorrect, calcul legal errone) : issue critique, signaler avec l'article legal de reference.

## Prochaine etape

Apres ce POC :

1. Saisir vos vrais chiffres (balance comptable, P&L, facturation clients) dans des CSV locaux places dans `private/`.
2. Programmer vos routines recurrentes : `python3 cfo-init/scripts/routines/compute_entity_routines.py --siren <SIREN>`.
3. Generer votre premier reporting mensuel reel : cfo-reporting avec vos vrais KPIs.
4. Ecrire une issue ou un retour de POC (ce qui a bien fonctionne, ce qui manque) avant de deployer plus largement.

## Contact

Issues techniques : https://github.com/RuddyMoriarty/moriarty-cfo/issues

Questions de conformite ou de droit : demander a un expert-comptable inscrit a l'Ordre ou a un commissaire aux comptes. Ce bundle donne une premiere lecture operationnelle, il ne se substitue pas a un professionnel du chiffre ou du droit.
