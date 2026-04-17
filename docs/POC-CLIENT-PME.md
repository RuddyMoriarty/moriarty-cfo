# POC Client PME, guide de test bout en bout

Guide destine a un dirigeant ou CFO interne de PME qui veut tester le bundle `moriarty-cfo` dans ses conditions reelles. 10 scenarios en 30 a 45 minutes, sans besoin de donnees confidentielles : chaque scenario fournit des valeurs fictives mais realistes.

L'objectif : valider que le bundle repond a vos questions reelles de gestion avant de l'utiliser sur vos vrais chiffres.

**Versions validees contre le bundle** : v0.3.4+ (si v0.2.x, certaines commandes differeront).

## Prerequis

```bash
git clone https://github.com/RuddyMoriarty/moriarty-cfo.git
cd moriarty-cfo
python3 evals/run_evals.py --full   # Doit afficher PASS 100%
```

Aucune cle API requise. Optionnel : `PAPPERS_API_KEY` si vous avez un compte Pappers (500 req / mois gratuits). Sinon on utilise l'API Annuaire Entreprises (gratuite).

## Scenario 1, Initialisation rapide avec `--fetch` (2 min)

**But** : creer votre profil PME avec donnees publiques auto-remplies depuis l'INSEE.

**Note importante** : le SIREN de test 552120222 appartient a Societe Generale. Si vous lancez `--fetch`, l'output affichera "SOCIETE GENERALE" (10 000+ salaries). C'est normal et pedagogique : le `--fetch` interroge vraiment l'API Annuaire Entreprises. Remplacez par votre propre SIREN pour voir vos vraies donnees.

```bash
./cfo init-pme \
  --siren 552120222 \
  --denomination "ACME SAS" \
  --role cfo \
  --cloture 2026-12-31 \
  --fetch
```

**Ce que vous verifiez** :
- Terminal affiche `✓ Annuaire Entreprises : ... (NAF X, tranche Y)`
- `private/companies/552120222/company.json` existe avec `classification.naf_code`, `classification.effectif_tranche_insee`, `annuaire_entreprises.nombre_etablissements`
- Vos donnees restent locales : `private/` est gitignore

## Scenario 2, Calendrier fiscal automatique (1 min)

```bash
./cfo calendar \
  --closing-date 2026-12-31 \
  --tva-regime reel_normal_mensuelle \
  --is-regime is \
  --effectif 25 \
  --output private/companies/552120222/calendar-fiscal.json

python3 -c "
import json
d = json.load(open('private/companies/552120222/calendar-fiscal.json'))
print(f'Total : {len(d[\"echeances\"])} echeances sur 18 mois')
for e in d['echeances'][:5]:
    print(f'  {e[\"date_absolue\"]} : {e[\"label\"]} ({e.get(\"type\",\"?\")})')"
```

**Ce que vous verifiez** : 55+ echeances (TVA mensuelles le 24, DSN le 15, acomptes IS aux 15/03, 15/06, 15/09, 15/12, solde IS le 15/05).

## Scenario 3, BFR + ratios DSO/DPO/DIO (2 min)

```bash
./cfo bfr \
  --creances-clients 200000 --dettes-fournisseurs 100000 \
  --ca-ttc 1200000 --achats-ttc 400000 \
  --stocks 50000 --cout-ventes 300000 \
  --secteur services_btob \
  --output /tmp/bfr.json

python3 -c "
import json
d = json.load(open('/tmp/bfr.json'))
r = d['ratios']
print(f'DSO {r[\"dso\"]:.0f} j | DPO {r[\"dpo\"]:.0f} j | DIO {r[\"dio\"]:.0f} j | BFR {r[\"bfr\"]:,.0f} EUR')
for k, v in d['benchmark'].items():
    if isinstance(v, str):
        print(f'  {k}: {v}')"
```

**Ce que vous verifiez** : DSO 61 j, DPO 91 j, DIO 61 j, BFR 150 k€. Benchmark services B2B affiche ("dans la norme", "meilleur que mediane", etc).

## Scenario 4, Forecast tresorerie 13 semaines (2 min)

**Mode rapide** avec flux hebdomadaires moyens (pratique pour un premier chiffrage) :

```bash
./cfo forecast-13w \
  --solde-initial 150000 \
  --encaissements-moyen 80000 \
  --decaissements-moyen 75000 \
  --output /tmp/fc13.json

python3 -c "
import json
d = json.load(open('/tmp/fc13.json'))
print(f'Niveau alerte : {d[\"alerts\"][\"niveau\"]}')
print(f'Message : {d[\"alerts\"][\"message\"]}')
for w in d['weeks'][::3]:
    print(f'  {w[\"label\"]} : solde final {w[\"solde_final\"]:>10,.0f} EUR')"
```

**Ce que vous verifiez** : 13 semaines, niveau d'alerte dans `{healthy_vert, vigilance_jaune, plan_action_orange, urgence_rouge}`, point bas identifie.

**Mode detaille** (avec fichier de projections ponctuelles) :

```bash
cat > /tmp/projections.csv <<'EOF'
date,type,montant,libelle
2026-04-20,encaissement,50000,Facture client X
2026-05-05,decaissement,25000,Echeance IS
EOF

./cfo forecast-13w \
  --solde-initial 150000 \
  --projections /tmp/projections.csv \
  --seuil-tension 50000 \
  --output /tmp/fc13-detail.json
```

## Scenario 5, Dashboard HTML CFO executif (3 min)

```bash
cat > /tmp/kpis.json <<'EOF'
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
EOF

./cfo dashboard \
  --kpis /tmp/kpis.json \
  --output-html /tmp/dashboard-march.html

open /tmp/dashboard-march.html  # macOS
# xdg-open /tmp/dashboard-march.html  # Linux
```

**Ce que vous verifiez** : HTML A4 landscape avec les 6 KPIs remplis, charte discrete.

**Variante avec variances budget vs reel** :

```bash
# Reutiliser le fichier /tmp/budget.json du scenario 6 + un fichier reel
./cfo dashboard --kpis /tmp/kpis.json --variances /tmp/variances.json --output-html /tmp/dash-full.html
```

## Scenario 6, Budget annuel 3 scenarios ponderes (2 min)

```bash
cat > /tmp/pnl-n1.csv <<'EOF'
poste,montant_annuel
ca_ht,10000000
charge_personnel,4500000
charge_achats,2500000
charge_externes,1200000
charge_amortissements,400000
EOF

./cfo budget \
  --pnl-n1 /tmp/pnl-n1.csv \
  --growth-ca 12 --growth-charges 8 \
  --marge-cible 18 \
  --output /tmp/budget.json

python3 -c "
import json
d = json.load(open('/tmp/budget.json'))
for label, s in d['scenarios'].items():
    print(f'{label:>10} : CA {s[\"ca_ht_annuel\"]:>12,.0f} EUR | EBITDA {s[\"ebitda_annuel\"]:>10,.0f} ({s[\"marge_ebitda_pct\"]:.1f} pct)')
p = d['pondere_20_60_20']
print(f'Pondere 20/60/20 : CA {p[\"ca_ht_annuel\"]:,.0f} / EBITDA {p[\"ebitda_annuel\"]:,.0f}')"
```

**Ce que vous verifiez** : 3 scenarios (realiste/optimiste/pessimiste) avec marge EBITDA cible 18 pct respectee sur le realiste, ponderation 20/60/20 affichee.

## Scenario 7, Estimation CIR (2 min)

```bash
./cfo cir \
  --salaires-chercheurs 200000 \
  --frais-fonctionnement-pct 43 \
  --sous-traitance-agreee 50000 \
  --output /tmp/cir.json

python3 -c "
import json
d = json.load(open('/tmp/cir.json'))
print(f'Total depenses eligibles : {d[\"total_depenses_eligibles\"]:,.0f} EUR')
print(f'Taux applique : {d[\"taux_applique\"]}')
print(f'CIR estime : {d[\"cir_estime\"]:,.0f} EUR')
for w in d.get('warnings', []):
    print(f'  {w}')"
```

**Ce que vous verifiez** : base inclut le forfait fonctionnement 43 pct + sous-traitance agreee (plafond 2 M€), CIR = 30 pct jusqu'a 100 M€ (CGI art. 244 quater B).

## Scenario 8, Cartographie risques COSO ERM (3 min)

```bash
cat > /tmp/risques.csv <<'EOF'
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
EOF

./cfo risk-map \
  --risques /tmp/risques.csv \
  --output /tmp/risk-map.json

python3 -c "
import json
d = json.load(open('/tmp/risk-map.json'))
print(f'Risques traites : {d[\"nb_risques_total\"]}')
print(f'Repartition : {d[\"repartition_severite\"]}')
print('Top 3 :')
for r in d['top_10_risques'][:3]:
    print(f'  {r[\"id\"]} ({r[\"severite\"]}) : {r[\"libelle\"]}')"
```

**Ce que vous verifiez** : matrice 5x5, top 10 trie par score = proba x impact, severite calibree critique/eleve/moyen/faible.

## Scenario 9, Scope CSRD (1 min)

```bash
./cfo csrd-scope \
  --effectif 300 \
  --ca-eur 50000000 \
  --bilan-eur 30000000 \
  --output /tmp/csrd.json

python3 -c "
import json
d = json.load(open('/tmp/csrd.json'))
print(f'Wave CSRD : {d[\"wave\"]}')
print(f'Label : {d[\"label\"]}')
print(f'Premier exercice reporte : {d.get(\"premier_exercice_reporté\", \"?\")}')
print(f'Premier rapport publie : {d.get(\"premier_rapport_publié\", \"?\")}')
print(f'Statut : {d.get(\"statut\", \"?\")}')"
```

**Ce que vous verifiez** : wave calculee selon vos 3 criteres (effectif, CA, bilan), directive 2022/2464 + Stop-the-Clock 2025/794 prise en compte.

Pour une societe cotee, ajouter `--coté` :

```bash
./cfo csrd-scope --effectif 600 --ca-eur 60000000 --bilan-eur 35000000 --coté
```

## Scenario 10, Diagnostic financement (2 min)

Arbre de decision selon montant + horizon + dilutif-ok :

```bash
./cfo diag-financement \
  --montant 200000 \
  --horizon mlt \
  --projet-rd \
  --output /tmp/diag.json

python3 -c "
import json
d = json.load(open('/tmp/diag.json'))
print(f'Solutions eligibles : {d[\"solutions_eligibles_count\"]}')
print('Top 3 :')
for s in d.get('top_3', []):
    montant = s['max_montant']
    montant_s = f'{montant/1e6:.1f} M EUR' if montant >= 1e6 else f'{montant:,.0f} EUR'
    print(f'  - {s[\"nom\"]} ({s[\"horizon\"]}, {s[\"cout_pct\"]}%, {s[\"delai_jours\"]} j) : plafond {montant_s}')
if d.get('aides_publiques_eligibles'):
    print('Aides publiques eligibles → passerelle Moriarty recommandee')
if d.get('moriarty_cta_recommande'):
    print(f'CTA : ./cfo moriarty-link --siren <SIREN>')"
```

**Ce que vous verifiez** : top 3 avec BPI subvention (R&D), aides publiques eligibles (flag `true`), CTA Moriarty recommande.

**Flags disponibles** :
- `--horizon {ct|mlt|lt}` : court / moyen long / long terme
- `--projet-rd` : projet R&D (active BPI subvention + CIR)
- `--projet-industriel` : projet industriel (active aides ADEME/region)
- `--dilutif-ok` : accepte les solutions dilutives (BA, VC, PE)
- `--urgence-jours N` : filtre sur delai d'obtention

## Ce qui devrait fonctionner a 100 %

Si les 10 scenarios passent sans erreur, le bundle est pret pour vos vrais chiffres. Remplacer les fixtures `/tmp/*.csv` / `/tmp/*.json` par vos fichiers dans `private/`.

## Ce qu'il faut signaler

- **Error "Traceback"** : bug script → issue https://github.com/RuddyMoriarty/moriarty-cfo/issues avec stderr complete
- **Exit non-zero silencieux** : scenario de robustesse insuffisant → issue avec input fourni
- **Output faux** (chiffre incorrect, calcul legal errone) : issue critique avec article legal de reference

## Prochaine etape

1. Saisir vos vrais chiffres (balance comptable, P&L, facturation clients) dans des CSV locaux dans `private/`
2. Programmer vos routines recurrentes : `./cfo routine-compute --siren <SIREN>`
3. Generer votre premier reporting mensuel reel : `./cfo dashboard` avec vos KPIs reels
4. Ecrire un retour de POC (ce qui a bien fonctionne, ce qui manque) avant de deployer plus largement

## Contact

Issues techniques : https://github.com/RuddyMoriarty/moriarty-cfo/issues

Questions de conformite ou de droit : expert-comptable inscrit a l'Ordre. Ce bundle donne une premiere lecture operationnelle, ne se substitue pas a un professionnel du chiffre ou du droit.
