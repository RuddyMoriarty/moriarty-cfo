# Plan de Continuité d'Activité (BCP)

**Société** : {{COMPANY_NAME}} (SIREN {{SIREN}})
**Date** : {{DATE}}
**Version** : 1.0
**Approuvé par** : {{NOM_DG}}, {{ROLE_DG}}
**Révision** : annuelle

## 1. Pilotage de la crise

### Cellule de crise

| Rôle | Nom | Téléphone | Email |
|------|-----|-----------|-------|
| Chef de crise | {{CEO}} | {{TEL_CEO}} | {{EMAIL_CEO}} |
| CFO | {{CFO}} | {{TEL_CFO}} | {{EMAIL_CFO}} |
| CTO / DSI | {{CTO}} | {{TEL_CTO}} | {{EMAIL_CTO}} |
| DRH | {{DRH}} | {{TEL_DRH}} | {{EMAIL_DRH}} |
| Communication | {{COMM}} | {{TEL_COMM}} | {{EMAIL_COMM}} |
| Juridique | {{LEGAL}} | {{TEL_LEGAL}} | {{EMAIL_LEGAL}} |

### Activation

Critères de déclenchement (à valider par chef de crise) :
- Cyber-attaque bloquant le SI > 4h
- Sinistre physique des locaux
- Pandémie / confinement
- Indisponibilité d'un fournisseur critique > 5 jours
- Toute autre situation impactant les activités critiques

Procédure :
1. Identification de la crise
2. Notification au chef de crise
3. Décision d'activation
4. Convocation cellule de crise (visio ou physique)
5. Communication initiale interne (sous 1h)

## 2. Activités critiques

| Activité | RTO (max indispo) | RPO (perte données max) | Owner |
|----------|-------------------|--------------------------|-------|
| Service client / SaaS | 4h | 0 (pas de perte) | {{OWNER_SC}} |
| Encaissement | 24h | < 24h | {{OWNER_ENC}} |
| Paie | 1 semaine | < 1 semaine | {{OWNER_PAIE}} |
| Production / Livraison | {{RTO_PROD}} | {{RPO_PROD}} | {{OWNER_PROD}} |
| Reporting réglementaire | 1 mois | < 1 mois | {{OWNER_REG}} |

## 3. Stratégies par scénario

### Scénario 1 : Cyber-attaque (ransomware)

**Plan d'action** :
1. Isoler les systèmes infectés (déconnecter du réseau)
2. NE PAS PAYER la rançon
3. Activer cellule de crise
4. Plainte gendarmerie (cybergend.fr)
5. Déclaration ANSSI (https://www.ssi.gouv.fr)
6. Si données personnelles : déclaration CNIL sous 72h
7. Activer assurance cyber (police {{NUM_POLICE_CYBER}})
8. Restaurer depuis sauvegardes hors-ligne (procédure DRP-1)
9. Communication clients (transparence)
10. Post-mortem dans les 30 jours

### Scénario 2 : Sinistre physique (incendie, inondation)

**Plan d'action** :
1. Évacuation prioritaire (sécurité humaine)
2. Appel pompiers + autorités
3. Activer cellule de crise
4. Bascule télétravail intégral (procédure DRP-2)
5. Déclaration assurance multirisque ({{NUM_POLICE_MR}})
6. Identifier site de repli ({{ADRESSE_REPLI}})
7. Communication clients sur impact

### Scénario 3 : Pandémie / confinement

**Plan d'action** :
1. Activer cellule de crise
2. Bascule 100% télétravail
3. Politique sanitaire interne
4. Sourcing fournitures essentielles
5. Adaptation des produits/services si nécessaire
6. Suivi quotidien évolution réglementaire

### Scénario 4 : Défaillance fournisseur critique

**Plan d'action** :
1. Identification rapide de l'impact
2. Activation des fournisseurs alternatifs (cf. registre)
3. Communication clients sur retards éventuels
4. Plan B sur production / livraison

## 4. Sauvegardes et restauration

### Politique 3-2-1

- **3 copies** : production + sauvegarde locale + sauvegarde distante
- **2 supports différents** : disque + cloud
- **1 hors-ligne** : protection ransomware

### Tests de restauration

- Trimestriels (vérification intégrité)
- Annuels (test complet DRP)
- Documentation des résultats

## 5. Communication externe

### Audiences et messages clés

**Clients** :
- Premier contact < 4h après crise
- Updates fréquents même sans nouveauté
- Plateforme dédiée (status.{{DOMAIN}})

**Fournisseurs** :
- Notification dans les 24h si impact

**Banques** :
- Notification immédiate si impact financier majeur

**Médias / public** :
- Porte-parole unique : {{NOM_PORTE_PAROLE}}
- Pas de communication non validée

**Autorités** :
- CNIL si données personnelles compromises (72h)
- ANSSI si cyber-attaque
- Autorités sectorielles selon activité

## 6. Annuaire de crise

### Internes
[À compléter avec contacts complets]

### Externes
| Service | Numéro |
|---------|--------|
| Pompiers / SAMU | 18 / 15 / 112 |
| Gendarmerie / Police | 17 |
| Cybermalveillance.gouv.fr | 0 805 805 817 |
| ANSSI | 01 71 75 84 04 |
| CNIL | 01 53 73 22 22 |
| Banque {{NOM_BANQUE}} | {{TEL_BANQUE}} |
| Assureur cyber | {{TEL_CYBER}} |
| Assureur multirisque | {{TEL_MR}} |
| Avocat conseil | {{TEL_AVOCAT}} |
| Cabinet IT (DRP) | {{TEL_IT}} |

## 7. Tests et exercices

| Type | Fréquence | Date prochain | Owner |
|------|-----------|---------------|-------|
| Tabletop (revue théorique) | Annuel | {{DATE_TABLETOP}} | {{OWNER_TT}} |
| Test DRP IT (restauration) | Annuel | {{DATE_DRP}} | {{OWNER_DRP}} |
| Test communication crise | Annuel | {{DATE_COMM}} | {{OWNER_COMM_TEST}} |

## 8. Maintenance du BCP

- Revue annuelle complète : {{DATE_REVUE}}
- Mise à jour ad hoc à chaque changement majeur (organisation, site, fournisseur)
- Intégration des leçons apprises post-incident

---

**Signature direction** : ___________________________

**Date** : {{DATE}}

---

_Document confidentiel, accès restreint à la cellule de crise + responsables identifiés._
_Référence : ISO 22301 (Business Continuity Management Systems)._
