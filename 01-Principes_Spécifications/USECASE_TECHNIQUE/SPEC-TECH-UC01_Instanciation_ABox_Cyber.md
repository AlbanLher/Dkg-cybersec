# 📜 SPEC-TECH-UC01 — Spécification d'Instanciation UseCase Cyber (ABox & SI Cyber)

> **Classification** : `TLP:AMBER`  
> **Statut** : 🟢 Approuvé  
> **Niveau d'Abstraction** : 🟡 USECASE_TECHNIQUE  
> **Public Cible** : Architectes Sécurité, Développeurs DevSecOps & Analystes CTI  
> **Domaine Principal** : Ingestion & Instanciation Cyber (`CT`, `QU`, `SE`)  
> **Matrice de Rattachabilité** : `EXG-CT-01`, `EXG-CT-02`, `EXG-CT-03`, `EXG-QU-02`, `EXG-SE-01`

---

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif
La présente spécification encadre la réalisation du **Jeu de Données Factuelles de Synthèse (ABox)** pour le UseCase Cybersécurité (Phase 2).  
Elle définit le namespace, la convention de nommage des URIs, la population de la cartographie du SI et l'intégration des référentiels publics de menaces (CVE, CWE, CAPEC).

> ⚠️ **Clause d'Héritage et Conformité Cadre** :  
> Le présent UseCase s'inscrit en conformité stricte et inconditionnelle avec l'ensemble des exigences transverses, règles d'intégrité et contraintes de qualité définies dans les spécifications du Socle Framework (`SPEC-SOCLE-00`, `SPEC-SOCLE-01`, `SPEC-SOCLE-02`)[cite: 10, 11].

### 1.2 Glossaire Métier & Technique
| Acronyme / Terme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **DKG** | Dynamic Knowledge Graph | Graphe de connaissances dynamique. |
| **ABox** | Assertional Box | Données factuelles et instances du graphe. |
| **CVE** | Common Vulnerabilities and Exposures | Référentiel des vulnérabilités. |
| **CWE** | Common Weakness Enumeration | Référentiel des faiblesses logicielles. |
| **CAPEC** | Common Attack Pattern Enumeration | Modes opératoires d'attaque. |
| **CVSS** | Common Vulnerability Scoring System | Score de sévérité (0.0 à 10.0)[cite: 11]. |

---

## 🎯 2. Périmètre & Rôle de la Spécification

* **Positionnement dans l'Architecture** : Document de niveau **Niveau 3 — Cas d'Usage Technique**[cite: 10]. Il régit la génération de la cartographie SI et des données CTI d'injection dans `DKG_ABox_Master.ttl`[cite: 11].
* **Gouvernance & Validation** : Validé par l'équipe DevSecOps. Il spécifie la structure du générateur Python `generate_phase2_abox.py`[cite: 11].

---

## 📐 3. Spécifications Formelles & Règles Métier

### 3.1 Espaces de Noms & Nommage des Instances
* **Namespace Référentiel Données [`EXG-CT-01`]** : L'espace de noms d'instanciation du UseCase Cyber est strictement fixe à `http://dkg.cybersec.org/data/` (Préfixe : `dkg-data:`)[cite: 11].
* **URIs Déterministes & Normalisées [`EXG-CT-02`]** : Les URIs d'instances doivent employer des identifiants stables et prévisibles (ex: `dkg-data:Asset-Srv-Prod-01`, `dkg-data:CVE-2021-41773`, `dkg-data:CWE-22`, `dkg-data:CAPEC-126`)[cite: 11].

### 3.2 Structure du Jeu de Données de Synthèse Cyber
* **Complétude du Graphe Cyber [`EXG-CT-03`]** : Le jeu d'instances de synthèse doit obligatoirement inclure et relier la chaîne complète des entités métiers Cybersécurité[cite: 11] :
  * **Actifs du SI** (`dkg:Asset`) : Ex. Serveur Web Prod (`dkg-data:Asset-Srv-Prod-01`)[cite: 11].
  * **Composants Logiques** (`dkg:SoftwareComponent`) : Ex. Service Apache HTTP (`dkg-data:Comp-Apache-2-4`)[cite: 11].
  * **Vulnérabilités NIST** (`dkg:Vulnerability`) : Ex. `dkg-data:CVE-2021-41773` qualifiée par un score CVSS (`dkg:cvssScore "7.5"^^xsd:decimal`)[cite: 11].
  * **Faiblesses Logicielles** (`dkg:Weakness`) : Ex. Traversée de répertoire (`dkg-data:CWE-22`)[cite: 11].
  * **Modes Opératoires Attack** (`dkg:ThreatPattern`) : Ex. `dkg-data:CAPEC-126`[cite: 11].
  * **Marquage TLP** (`dkg:TLPMarking`) : Attribution d'un niveau TLP à chaque actif (`dkg-data:TLP-AMBER`)[cite: 11].

```turtle
# --- Snippet d'illustration de la structure ABox Cyber ---
@prefix dkg: [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#) .
@prefix dkg-data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#) .
@prefix xsd: [http://www.w3.org/2001/XMLSchema#](http://www.w3.org/2001/XMLSchema#) .

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

### 3.3 Contrôles Qualité et Intégrité Données

- **Validation SHACL & Plages CVSS [`EXG-QU-02`]** : Toutes les instances du UseCase doivent satisfaire aux contraintes typiques de datatypes (`xsd:decimal` entre `0.0` et `10.0` pour les CVSS) et de cardinalités minimums sous CWA[cite: 11].
    
- **Intégrité de Recette [`EXG-QU-03`]** : Le fichier généré doit valider le Sanity Check sans aucune erreur `sh:Violation`[cite: 11].
    

## 📊 4. Matrice Synthétique des Exigences Métier (Index de Traçabilité)

|**Identifiant**|**Domaine**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|**Section Parent**|**Mode de Validation**|
|---|---|---|---|---|---|
|**EXG-CT-01**|**`CT`**|**Namespace Instance Dedicated**|Utilisation exclusive de `http://dkg.cybersec.org/data/`[cite: 11].|Section 3.1|Parsing RDF / Code|
|**EXG-CT-02**|**`CT`**|**Identifiants URIs Déterministes**|Format de nommage normé pour Actifs, CVE, CWE, CAPEC[cite: 11].|Section 3.1|Linter / Regex|
|**EXG-CT-03**|**`CT`**|**Instanciation Graphe Complète**|Population de la chaîne complète Asset $\rightarrow$ CVE $\rightarrow$ CWE $\rightarrow$ CAPEC[cite: 11].|Section 3.2|Requête SPARQL|
|**EXG-QU-02**|**`QU`**|**Typage & Plages CVSS**|Strict respect du format CVSS decimal $[0.0, 10.0]$ sous CWA[cite: 11].|Section 3.3|pySHACL CWA|
|**EXG-QU-03**|**`QU`**|**Sanity Check ABox Zero Error**|$0$ erreur de validation sous CWA lors du contrôle Pytest[cite: 11].|Section 3.3|Pytest / SHACL|

## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest

- **Scripts de Génération / Exécution** : `03-Application/generate_phase2_abox.py`[cite: 11].
    
- **Suites de Tests Associées** : `tests/test_phase2_abox.py`.
    
- **Artefacts Produits** : `02-Donnees/Master_Transversal/DKG_ABox_Master.ttl`[cite: 11].
    

## 📚 6. Documents Liés & Références

- **[SPEC-SOCLE-00]** : Gouvernance du Cadre Spécifications & Exigences DKG.
    
- **[SPEC-SOCLE-02]** : Spécification des Contraintes & Règles de Validation ABox[cite: 10].
    
- **[NVD NIST]** : [National Vulnerability Database](https://nvd.nist.gov/)
    
    [cite: 11]
    
- **[MITRE]** : [CWE / CAPEC Frameworks](https://cwe.mitre.org/)
    
    [cite: 11]