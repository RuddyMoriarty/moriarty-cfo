# BFR Optimization — Diagnostic + 7 leviers

Le BFR (Besoin en Fonds de Roulement) est le cash **bloqué dans le cycle d'exploitation**. Le libérer, c'est gagner de la trésorerie sans s'endetter ni lever de fonds.

## Calcul BFR

### Formule standard

```
BFR = Stocks
    + Créances clients (TTC)
    + Autres créances court terme
    - Dettes fournisseurs (TTC)
    - Dettes fiscales et sociales court terme
    - Autres dettes CT
```

### BFR en jours de CA

```
BFR_en_jours = BFR × 365 / CA HT
```

Benchmarks indicatifs :
- Services BtoB : 30-60 jours
- Industrie : 60-120 jours
- Négoce / commerce : 15-45 jours (DSO court, DIO géré)
- SaaS / abonnements : négatif si facturation annuelle à l'avance (=trésorerie gratuite)

## Les 4 ratios clés

### DSO — Days Sales Outstanding

```
DSO = Créances clients TTC × 365 / CA TTC
```

Représente le nombre de jours moyens entre la facturation et l'encaissement.

**Benchmarks** :
- Services BtoB France : **45-65 jours** (loi LME : 60 jours max légalement)
- Industrie France : 60-90 jours
- Export : 75-120 jours
- B2C / e-commerce : < 10 jours (paiement à la commande)

### DPO — Days Payable Outstanding

```
DPO = Dettes fournisseurs TTC × 365 / Achats TTC
```

Jours moyens entre la réception de la facture fournisseur et son paiement.

**Benchmarks** :
- PME services : 30-50 jours
- PME industrie : 45-65 jours
- Grands comptes avec pouvoir de négo : 60-90 jours

### DIO — Days Inventory Outstanding

```
DIO = Stocks × 365 / Coût des ventes (achats + variation stocks)
```

Jours moyens de rotation des stocks.

**Benchmarks** :
- Distribution / FMCG : 20-40 jours
- Industrie / fabrication : 60-120 jours
- Automobile / biens d'équipement : 90-180 jours

### CCC — Cash Conversion Cycle

```
CCC = DSO + DIO - DPO
```

Jours entre la sortie de cash (paiement fournisseur) et la rentrée de cash (encaissement client).

**CCC négatif = très bon** (Amazon, Apple, services SaaS abo annuel). Le business tourne sans cash bloqué, et génère même du cash "gratuit".

## Les 7 leviers d'optimisation

### Levier 1 — Relance active des créances

**Gain potentiel** : -10 à -30 jours de DSO
**Difficulté** : ⭐ Facile

**Actions** :
- Automatiser les relances (J+0 confirmation, J+30 rappel amiable, J+45 relance, J+60 mise en demeure)
- Qualifier les clients "mauvais payeurs" dans le CRM
- Prévoir **conditions pénalité de retard** dans les CGV (taux BCE +10 pts + indemnité forfaitaire 40€)
- Suivre DSO top 20 clients mensuellement

### Levier 2 — Acompte / Avance client

**Gain potentiel** : -50 à -80% du DSO
**Difficulté** : ⭐⭐ Moyen (nécessite accord client)

**Actions** :
- Standardiser acompte 30-50% à la commande
- Facturation à l'étape (vs. à la fin de projet)
- Abonnement annuel à la place de mensuel (avec remise 10-15%)

### Levier 3 — Escompte fournisseurs

**Gain potentiel** : pas de réduction DPO mais gain marge
**Difficulté** : ⭐⭐ Moyen

**Actions** :
- Demander un escompte 1-2% en échange d'un paiement à 10 jours
- Arbitrer escompte vs. coût du financement (si escompte > coût = optimisation)

### Levier 4 — Renégociation conditions fournisseurs

**Gain potentiel** : +20 à +45 jours de DPO
**Difficulté** : ⭐⭐⭐ Difficile (rapport de force)

**Actions** :
- Rationaliser le panel fournisseurs (top 20 = 80% du volume)
- Négocier contrats cadres annuels avec paiement 60j
- **Attention loi LME** : 60 jours date d'émission facture ou 45 jours fin de mois — PAS 90 jours

### Levier 5 — Factoring (affacturage)

**Gain potentiel** : -100% des créances éligibles
**Difficulté** : ⭐⭐ Moyen (contrat factor)
**Coût** : 0.5% à 3% du CA cédé

**Types** :
- **Full factoring** : le factor achète la créance (transfert de risque)
- **Confidential factoring** : client n'est pas informé
- **Reverse factoring** : l'acheteur (donneur d'ordre) finance ses fournisseurs

Arbitrage : coût factor vs. coût du financement bancaire alternatif.

### Levier 6 — Optimisation stocks (JIT)

**Gain potentiel** : -30 à -60% du DIO
**Difficulté** : ⭐⭐⭐ (industrie)

**Actions** :
- Passage en Just-In-Time (JIT) avec fournisseurs fiables
- VMI (Vendor Managed Inventory)
- ABC analysis : focus sur 20% de références = 80% de la valeur
- Liquider les stocks obsolètes (dépréciation N en charges plutôt que N+1, N+2)

### Levier 7 — Mobilisation créances (Dailly, Cession Dailly)

**Gain potentiel** : anticipation d'encaissements
**Difficulté** : ⭐⭐ Moyen (ligne bancaire spécifique)

**Actions** :
- Ouverture d'une ligne de mobilisation de créances (Dailly) auprès de la banque principale
- Cession des factures contre avance immédiate (90% typique) — solde à l'encaissement
- Coût : taux bancaire + commissions (généralement 0.3% à 0.6% par cession)

## Calcul du gain potentiel

Exemple PME services, CA 5M€, DSO 65j, DPO 35j, DIO 0j :

- BFR actuel ≈ (65-35) × 5M€ / 365 = **410 k€** de cash bloqué
- Actions combinées :
  - Relance active : -10j DSO → -137k€ BFR
  - Acompte 30% : -15j DSO → -205k€ BFR
  - Renégociation DPO +10j : +137k€ BFR
- **Gain total = 479k€ de cash libéré** en 6 mois

## Script `scripts/bfr_calculator.py`

Prend en entrée la balance comptable + données CA/achats, calcule BFR/DSO/DPO/DIO, benchmark vs secteur, et propose des leviers ciblés.

## Adaptation par audience

**Mode EC** : souvent le premier diagnostic "cash" en mission. Vulgariser les ratios pour le client. Proposer un plan d'action chiffré.

**Mode PME** : focus **actions concrètes chiffrées**. Exemple : "En relançant le top 10 créances > 60j (350k€), tu libères ~250k€ de cash en 30-45 jours."

## Orchestration

- Lecture balance depuis `cfo-comptabilite` (derniers états)
- KPIs BFR remontés à `cfo-reporting` (tableau de bord)
- Si tension détectée → `cfo-financement-croissance` pour options de financement CT complémentaires
