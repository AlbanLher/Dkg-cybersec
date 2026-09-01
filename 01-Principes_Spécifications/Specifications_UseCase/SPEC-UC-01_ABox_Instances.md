# 📜 SPEC-UC-01 — Spécification d'Instanciation UseCase Cyber (ABox & SI Cyber) 

> **Classification** : `TLP:AMBER` > **Statut** : 🟢 Approuvé 
 > **Domaine** : Dynamic Knowledge Graph — UseCase Cyber 
 >  **Matrice de Rattachabilité** : `EXG-UC-ABOX-01`, `EXG-UC-ABOX-02`, `EXG-UC-ABOX-03`
--- 
 ## 📖 1. Glossaire des Acronymes 
* **DKG** : Dynamic Knowledge Graph (Graphe de connaissances dynamique) 
* **ABox** : Assertional Box (Données factuelles et instances du graphe) 
* **CVE** : Common Vulnerabilities and Exposures (Référentiel des vulnérabilités) 
* **CWE** : Common Weakness Enumeration (Référentiel des faiblesses logicielles) 
* **CAPEC** : Common Attack Pattern Enumeration and Classification (Modes opératoires d'attaque) 
* **CVSS** : Common Vulnerability Scoring System (Score de sévérité de 0.0 à 10.0) 

   --- 
## 🎯 2. Objet, Portée & Conformité Globale 

 La présente spécification encadre la réalisation du **Jeu de Données Factuelles de Synthèse (ABox)** pour le UseCase Cybersécurité (Phase 2). > ⚠️ **Clause d'Héritage et Conformité Cadre** : 
 Le présent UseCase s'inscrit en conformité stricte et inconditionnelle avec l'ensemble des exigences transverses, règles d'intégrité et contraintes de qualité définies dans les spécifications du Framework (`SPEC-01`, `SPEC-02`, notamment les règles `EXG-FWK-*` et `EXG-QUAL-*`). Les exigences listées ci-après constituent les spécificités strictes du domaine métier Cyber. Elle définit : 1. La structure du namespace et la convention de nommage des URIs d'instances. 2. Le modèle de population de la cartographie du Système d'Information (Actifs, Composants). 3. L'intégration des Référentiels Publics de Menaces et Vulnérabilités (CVE, CWE, CAPEC, TLP). 4. Les règles d'export et d'assemblage du fichier maître `DKG_ABox_Master.ttl`. 

 --- 
 
## 📐 3. Spécifications Formelles & Règles Métier 
### 3.1 Espaces de Noms & Nommage des Instances 
 * **Namespace Référentiel Données** `[EXG-UC-ABOX-01]` : L'espace de noms d'instanciation du UseCase Cyber est strictement fixe à `http://dkg.cybersec.org/data/` (Préfixe : `dkg-data:`). 
 * **URIs Déterministes & Normalisées** `[EXG-UC-ABOX-02]` : Les URIs d'instances doivent employer des identifiants stables et prévisibles (ex: `dkg-data:Asset-Srv-Prod-01`, `dkg-data:CVE-2021-41773`, `dkg-data:CWE-22`, `dkg-data:CAPEC-126`). 
 
### 3.2 Structure du Jeu de Données de Synthèse Cyber 
  * **Complétude du Graphe Cyber** `[EXG-UC-ABOX-03]` : Le jeu d'instances de synthèse doit obligatoirement inclure et relier la chaîne complète des entités métiers Cybersécurité : 
  * **Actifs du SI** (`dkg:Asset`) : Ex. Serveur Web Prod (`dkg-data:Asset-Srv-Prod-01`). 
  * **Composants Logiques** (`dkg:SoftwareComponent`) : Ex. Service Apache HTTP (`dkg-data:Comp-Apache-2-4`). 
  * **Vulnérabilités NIST** (`dkg:Vulnerability`) : Ex. `dkg-data:CVE-2021-41773` qualifiée par un score CVSS (`dkg:cvssScore "7.5"^^xsd:decimal`). 
  * **Faiblesses Logicielles** (`dkg:Weakness`) : Ex. Traversée de répertoire (`dkg-data:CWE-22`). 
  * **Modes Opératoires Attack** (`dkg:ThreatPattern`) : Ex. `dkg-data:CAPEC-126`. 
  * **Marquage TLP** (`dkg:TLPMarking`) : Attribution d'un niveau TLP à chaque actif (`dkg-data:TLP-AMBER`). 
 
```turtle 
 # --- Snippet d'illustration de la structure ABox Cyber --- 
dkg-data:Asset-Srv-Prod-01 a dkg:Asset ; 
    rdfs:label "Serveur Web de Production"@fr ; 
    dkg:hasInstalledComponent dkg-data:Comp-Apache-2-4 ; 
    dkg:hasTLPMarking dkg-data:TLP-AMBER . 
dkg-data:Comp-Apache-2-4 a dkg:SoftwareComponent ; 
    rdfs:label "Apache HTTP Server 2.4.41"@fr ; 
    dkg:hasVulnerability dkg-data:CVE-2021-41773 . 
dkg-data:CVE-2021-41773 a dkg:Vulnerability ; 
    dkg:cvssScore "7.5"^^xsd:decimal ; 
    dkg:exploitsWeakness dkg-data:CWE-22 . 
dkg-data:CWE-22 a dkg:Weakness ; 
    rdfs:label "Path Traversal"@en ; 
    dkg:hasThreatPattern dkg-data:CAPEC-126 .
```
---
## 📊 4. Matrice Synthétique des Exigences Métier (Index de Traçabilité UseCase)

| **Identifiant**    | **Intitulé de l'Exigence**          | **Description & Critères d'Acceptation**                       | **Section Parent** |
| ------------------ | ----------------------------------- | -------------------------------------------------------------- | ------------------ |
| **EXG-UC-ABOX-01** | **Namespace Instance Dedicated**    | Utilisation exclusive de `http://dkg.cybersec.org/data/`.      | Section 3.1        |
| **EXG-UC-ABOX-02** | **Identifiants URIs Déterministes** | Format de nommage normé pour Actifs, CVE, CWE, CAPEC.          | Section 3.1        |
| **EXG-UC-ABOX-03** | **Instanciation Graphe Complète**   | Population de la chaîne complète Asset -> CVE -> CWE -> CAPEC. | Section 3.2        |

---
## 🛡️ 5. Gouvernance, Outillage & Validation

- **Validation Automatisée** : Exécution du script Python `03-Application/generate_phase2_abox.py`.
- **Artefact Produit** : Fichier maître `02-Donnees/Master_Transversal/DKG_ABox_Master.ttl`.
    

## 📚 6. Pour aller plus loin (Ressources Pédagogiques)

- **[NVD] National Vulnerability Database** : [NVD NIST](https://nvd.nist.gov/)
    
- **[MITRE] CWE / CAPEC Frameworks** : [MITRE Cyber](https://cwe.mitre.org/)