# Obligations RGPD specifiques au perimetre du DAF/CFO

## Objet

Le Reglement (UE) 2016/679 (RGPD) et la loi n. 78-17 du 6 janvier 1978 modifiee (loi Informatique et Libertes) imposent des obligations aux responsables de traitement pour toute collecte et utilisation de donnees personnelles. Le perimetre du DAF/CFO est particulierement concerne car il manipule des donnees sensibles : paie, coordonnees bancaires, donnees fiscales, KYC.

---

## Base legale

| Texte | Contenu |
|-------|---------|
| Reglement (UE) 2016/679 du 27 avril 2016 | RGPD - reglement general sur la protection des donnees |
| Loi n. 78-17 du 6 janvier 1978 modifiee | Loi Informatique et Libertes |
| Decret n. 2019-536 du 29 mai 2019 | Decret d'application de la loi Informatique et Libertes modifiee |
| Code du travail, art. L. 1222-4 | Information du salarie sur les traitements de donnees |

---

## Traitements de donnees concernes dans le perimetre DAF

| Domaine | Types de donnees personnelles | Exemples |
|---------|-------------------------------|----------|
| **Paie et RH** | Donnees salariales, conges, arrets maladie, situation familiale, numero de securite sociale (NIR) | Bulletins de paie, DPAE, DSN |
| **Comptabilite** | Donnees fournisseurs (contacts, RIB), donnees clients (noms, adresses, SIREN) | Factures, bons de commande, fichier tiers |
| **Tresorerie** | Coordonnees bancaires (IBAN/BIC), autorisations de prelevement | Virements, rapprochements bancaires |
| **Controle de gestion** | Donnees de performance individuelle, objectifs, primes | Tableaux de bord RH, suivi des couts salariaux |
| **KYC / LCB-FT** | Pieces d'identite, justificatifs de domicile, beneficiaires effectifs | Formulaires KYC, registre des beneficiaires effectifs |
| **Audit et conformite** | Logs d'acces aux systemes financiers, pistes d'audit | ERP, logiciel comptable |

---

## Obligations cles du RGPD pour le DAF

### 1. Registre des traitements (art. 30 RGPD)

Toute organisation de plus de 250 salaries doit tenir un registre. En dessous de 250, le registre est obligatoire si les traitements sont reguliers (ce qui est toujours le cas pour la paie et la comptabilite).

Le registre doit contenir pour chaque traitement :

| Champ | Exemple (traitement paie) |
|-------|---------------------------|
| Finalite | Gestion de la paie et des obligations sociales |
| Categories de personnes | Salaries, stagiaires, mandataires sociaux |
| Categories de donnees | Etat civil, NIR, remuneration, conges, arrets |
| Destinataires | URSSAF (DSN), DGFIP, organisme de prevoyance, editeur de paie |
| Transferts hors UE | Oui/Non (verifier si l'editeur de paie est heberge hors UE) |
| Duree de conservation | Voir tableau ci-dessous |
| Mesures de securite | Chiffrement, controle d'acces, journalisation |

### 2. Bases legales (art. 6 RGPD)

| Traitement | Base legale applicable | Reference |
|------------|----------------------|-----------|
| Paie et DSN | **Obligation legale** (Code du travail, Code de la securite sociale) | Art. 6.1.c RGPD |
| Comptabilite et facturation | **Obligation legale** (PCG, CGI) | Art. 6.1.c RGPD |
| KYC / LCB-FT | **Obligation legale** (Code monetaire et financier) | Art. 6.1.c RGPD |
| Controle de gestion (suivi individuel) | **Interet legitime** du responsable de traitement | Art. 6.1.f RGPD |
| Prospection commerciale B2B | **Interet legitime** | Art. 6.1.f RGPD |
| Prospection commerciale B2C | **Consentement** | Art. 6.1.a RGPD |
| Emailing salaries (avantages sociaux tiers) | **Consentement** | Art. 6.1.a RGPD |

**Le NIR (numero de securite sociale)** fait l'objet d'un encadrement specifique en droit francais (art. 30 de la loi Informatique et Libertes modifiee). Son utilisation est limitee aux finalites listees par decret (paie, protection sociale, fiscalite).

### 3. Durees de conservation

| Type de donnee | Duree de conservation | Fondement |
|----------------|----------------------|-----------|
| **Pieces comptables** (factures, journaux, grand livre) | 10 ans a compter de la cloture de l'exercice | Art. L. 123-22 C. com. |
| **Bulletins de paie** | 5 ans (employeur) | Art. L. 3243-4 C. trav. |
| **Donnees de paie** (elements de calcul) | 5 ans apres le depart du salarie | Recommandation CNIL |
| **Donnees fiscales** (declarations, liasses) | 6 ans a compter de la derniere operation | Art. L. 102 B LPF |
| **Contrats de travail** | 5 ans apres la fin du contrat | Art. 2224 C. civ. (prescription) |
| **Documents KYC / LCB-FT** | 5 ans apres la fin de la relation d'affaires | Art. L. 561-12 CMF |
| **Registre des beneficiaires effectifs** | 5 ans apres la fin de la relation ou la radiation | Art. L. 561-12 CMF |
| **Logs d'acces aux systemes** | 1 an (maximum recommande par la CNIL) | Recommandation CNIL, art. 5.1.e RGPD |
| **Donnees de prospection B2B** | 3 ans apres le dernier contact actif | Recommandation CNIL |

**Regle generale :** au-dela de la duree de conservation active, les donnees doivent etre archivees en base intermediaire (acces restreint) ou supprimees. L'archivage definitif n'est justifie que pour les obligations legales.

### 4. Analyse d'impact (DPIA) - art. 35 RGPD

Une DPIA (Data Protection Impact Assessment) est obligatoire si le traitement est susceptible d'engendrer un risque eleve pour les droits et libertes. Dans le perimetre DAF, une DPIA peut etre requise pour :

| Situation | Necessaire ? |
|-----------|-------------|
| Traitement de paie standard (< 250 salaries) | Non (traitement courant, base legale obligation legale) |
| Traitement de paie a grande echelle (> 250 salaries ou donnees de sante) | **Oui** (traitement a grande echelle de donnees sensibles) |
| Systeme de controle des notes de frais avec geolocalisation | **Oui** (surveillance systematique) |
| Credit scoring interne des clients | **Oui** (profilage avec effets juridiques) |
| ERP avec module RH integre (suivi performance + paie + conges) | A evaluer (cumul de finalites, volume) |

La CNIL publie une liste de traitements necessitant une DPIA (deliberation n. 2018-327 du 11 octobre 2018).

---

## Droits des personnes (art. 15 a 22 RGPD)

| Droit | Application au perimetre DAF | Reserves |
|-------|------------------------------|----------|
| **Acces** (art. 15) | Le salarie peut demander une copie de toutes ses donnees de paie, evaluations, logs | Droit absolu, delai de reponse 1 mois |
| **Rectification** (art. 16) | Correction d'une erreur d'adresse, de RIB, de situation familiale | Droit absolu |
| **Effacement** (art. 17) | Suppression des donnees personnelles | **Reserve** : l'effacement ne s'applique pas si une obligation legale impose la conservation (ex. 10 ans comptables, 5 ans paie) |
| **Limitation** (art. 18) | Gel du traitement pendant une contestation | Applicable |
| **Portabilite** (art. 20) | Export des donnees dans un format structure | Uniquement pour les traitements fondes sur le consentement ou le contrat |
| **Opposition** (art. 21) | Refus du traitement fonde sur l'interet legitime | Ne s'applique pas aux traitements fondes sur une obligation legale |

**Point d'attention :** un salarie ne peut pas exiger l'effacement de son bulletin de paie avant l'expiration du delai legal de conservation. Le DAF doit documenter ce refus en citant la base legale.

---

## Notification de violation (art. 33-34 RGPD)

En cas de violation de donnees (fuite, acces non autorise, ransomware) :

| Etape | Delai | Destinataire | Reference |
|-------|-------|-------------|-----------|
| Notification a la CNIL | **72 heures** apres en avoir pris connaissance | CNIL (`https://www.cnil.fr/notifier-une-violation`) | Art. 33 RGPD |
| Notification aux personnes concernees | Dans les meilleurs delais si risque eleve | Personnes concernees | Art. 34 RGPD |
| Documentation interne | Immediate | Registre interne des violations | Art. 33.5 RGPD |

**Dans le perimetre DAF, les violations les plus courantes :**
- Envoi d'un bulletin de paie au mauvais salarie
- Fuite de fichier de virements (IBAN salaries)
- Ransomware sur le serveur comptable
- Acces non autorise au logiciel de paie

---

## Mesures de securite recommandees (art. 32 RGPD)

| Mesure | Application DAF |
|--------|-----------------|
| Chiffrement des donnees au repos | Bases de donnees paie, fichiers de virements |
| Chiffrement en transit (TLS) | Echanges avec les organismes sociaux (DSN), banques |
| Controle d'acces par roles | Separation comptabilite / paie / tresorerie dans l'ERP |
| Journalisation des acces | Logs d'acces au logiciel de paie et a l'ERP |
| Pseudonymisation | Tableaux de bord de controle de gestion (remplacer noms par identifiants) |
| Sauvegardes regulieres | Plan de sauvegarde et test de restauration |
| Sensibilisation du personnel | Formation annuelle RGPD pour l'equipe finance |

---

## Sanctions

| Type | Montant maximum | Reference |
|------|----------------|-----------|
| Manquements aux obligations du responsable de traitement (registre, DPIA, securite) | 10 M EUR ou 2 % du CA mondial | Art. 83.4 RGPD |
| Manquements aux principes fondamentaux (bases legales, droits des personnes, transferts) | 20 M EUR ou 4 % du CA mondial | Art. 83.5 RGPD |

---

## Sources

- Reglement (UE) 2016/679 (RGPD) : `https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679`
- Loi n. 78-17 du 6 janvier 1978 modifiee : `https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000886460`
- CNIL - Guide pratique RGPD : `https://www.cnil.fr/fr/rgpd-de-quoi-parle-t-on`
- CNIL - Liste des traitements necessitant une DPIA : `https://www.cnil.fr/fr/liste-des-traitements-pour-lesquels-une-analyse-dimpact-est-requise`
- CNIL - Durees de conservation : `https://www.cnil.fr/fr/les-durees-de-conservation-des-donnees`
- Code du travail, art. L. 3243-4 (conservation bulletins de paie) : `https://www.legifrance.gouv.fr`
- Livre des procedures fiscales, art. L. 102 B : `https://www.legifrance.gouv.fr`
