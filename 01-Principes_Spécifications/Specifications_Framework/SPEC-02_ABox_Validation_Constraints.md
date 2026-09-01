spec_02_content = """
# SPEC-02 — Spécification des Contraintes & Règles de Validation ABox
> **Classification** : `TLP:AMBER` > **Statut** : 🟢 Approuvé 
 > **Domaine** : Meta-Framework DKG (Dynamic Knowledge Graph)
  >**Matrice de Rattachabilité** : `EXG-FWK-02-01`, `EXG-FWK-02-02`, `EXG-FWK-02-03`, `EXG-QUAL-02`, `EXG-QUAL-03` > > 
--- 
## 📖 1. Glossaire des Acronymes 

* **DKG** : Dynamic Knowledge Graph (Graphe de connaissances dynamique) 
* **ABox** : Assertional Box (Composante décrivant les individus, données factuelles et instances) 
* **TBox** : Terminological Box (Schéma et concepts ontologiques) 
* **SHACL** : Shapes Constraint Language (Langage W3C de validation de contraintes) 
* **CWA** : Closed World Assumption (Hypothèse du monde fermé) 

--- 

## 2. Objet & Portée 
La présente spécification définit les **règles formelles d'intégrité et de validation génériques de l'ABox** au sein du DKG Framework. 
Elle est **strictement agnostique du domaine d'application** et fixe : 
1. Les critères d'intégrité référentielle entre individus (liens inter-instances). 
2. Le typage strict et la validation des plages/formats de littéraux. 
3. Les règles d'alignement formel avec les axiomes inverses définis dans la RBox. 
4. Le sas de recette qualité et de tolérance aux violations SHACL. --- 
 
## 3. Spécifications Formelles & Règles Métier 
### 3.1 Intégrité Référentielle Inter-Instances 
* **Intégrité Référentielle Stricte** `[EXG-FWK-02-01]` : Toute relation binaire `owl:ObjectProperty` instanciée dans l'ABox entre un individu $A$ et un individu $B$ doit pointer vers un individu $B$ obligatoirement déclaré et typé dans le graphe RDF. Aucun lien vers une URIs orpheline non instanciée n'est toléré. 
* 
### 3.2 Typage & Restricton des Literaux (Datatype Properties) 
* **Typage et Conformation des Datatypes** `[EXG-FWK-02-02]` : Tout littéral d'instance doit porter un typage XML Schema explicite (`xsd:string`, `xsd:integer`, `xsd:decimal`, `xsd:dateTime`). La validation SHACL associée doit vérifier les critères de cardinalité (`sh:minCount`, `sh:maxCount`), les plages de valeurs (`sh:minInclusive`, `sh:maxInclusive`) et les motifs d'expressions régulières (`sh:pattern`). 
* 
### 3.3 Cohérence RBox & Inverses Factuels 
* **Matérialisation des Relations Inverses** `[EXG-FWK-02-03]` : Pour toute assertion d'instance $A \xrightarrow{R} B$ où la propriété $R$ possède un inverse déclaré $R^{-1}$ via `owl:inverseOf` dans la RBox, l'assertion réciproque $B \xrightarrow{R^{-1}} A$ doit être formellement matérialisée dans l'ABox ou dérivable sans ambiguïté par le moteur de raisonnement. ### 3.4 Sanity Check & Tolérance de Recette 
* **Recette CWA Tolérance Zéro** `[EXG-QUAL-02]` / `[EXG-QUAL-03]` : L'ABox est soumise à un contrôle automatisé pySHACL exécuté sous *Closed World Assumption*. Le statut d'acceptation de l'ABox exige **$0$ violation** de sévérité `sh:Violation`. 

 
--- 
 
##  📊 4. Matrice Synthétique des Exigences (Index de Traçabilité)
 
| Identifiant       | Intitulé de l'Exigence           | Description & Critères d'Acceptation                                   | Section Parent |     |
| :---------------- | :------------------------------- | :--------------------------------------------------------------------- | :------------- | --- |
| **EXG-FWK-02-01** | **Intégrité Référentielle**      | Interdiction de pointer vers une instance non déclarée dans l'ABox.    | Section 3.1    |     |
| **EXG-FWK-02-02** | **Validation des Littéraux**     | Contrôle des typages `xsd`, cardinalités et plages de valeurs.         | Section 3.2    |     |
| **EXG-FWK-02-03** | **Matérialisation des Inverses** | Conformité des paires de relations inverses $(R, R^{-1})$ d'instances. | Section 3.3    |     |
| **EXG-QUAL-02**   | **Conformité des Datatypes**     | Respect strict des datatypes sous validation SHACL.                    | Section 3.4    |     |
| **EXG-QUAL-03**   | **Sanity Check Zero Violation**  | $0$ violation `sh:Violation` détectée lors du contrôle pySHACL.        | Section 3.4    |     |

--- 
## 🛡️ 5. Gouvernance, Outillage & Validation 
* **Validation Automatisée** : Script `03-Application/validate_abox.py` et suite Pytest (`test_phase2_quality.py`). 
* **Artefacts Produits** : `DKG_ABox_Master.ttl` validé et snapshot d'immuabilité Phase 2. 
 --- 
## 📚 6. Pour aller plus loin (Ressources Pédagogiques) 
* **[W3C] SHACL Property Shapes & Constraints** : [W3C SHACL Constraints](https://www.w3.org/TR/shacl/#core-components) 
* **[RDF] RDF 1.1 Concepts and Abstract Syntax** : [W3C RDF 1.1](https://www.w3.org/TR/rdf11-concepts/) """ ^






import os

# 1. SPEC-02_ABox_Validation_Constraints.md (Framework)
spec_02_content = """# 📜 SPEC-02 — Spécification des Contraintes & Règles de Validation ABox

> **Classification** : `TLP:AMBER`  
> **Statut** : 🟢 Approuvé  
> **Domaine** : Meta-Framework DKG (Dynamic Knowledge Graph)  
> **Matrice de Rattachabilité** : `EXG-FWK-02-01`, `EXG-FWK-02-02`, `EXG-FWK-02-03`, `EXG-QUAL-02`, `EXG-QUAL-03`

---

## 📖 1. Glossaire des Acronymes

* **DKG** : Dynamic Knowledge Graph (Graphe de connaissances dynamique)
* **ABox** : Assertional Box (Composante décrivant les individus, données factuelles et instances)
* **TBox** : Terminological Box (Schéma et concepts ontologiques)
* **SHACL** : Shapes Constraint Language (Langage W3C de validation de contraintes)
* **CWA** : Closed World Assumption (Hypothèse du monde fermé)

---

## 🎯 2. Objet & Portée

La présente spécification définit les **règles formelles d'intégrité et de validation génériques de l'ABox** au sein du DKG Framework.  
Elle est **strictement agnostique du domaine d'application** et fixe :
1. Les critères d'intégrité référentielle entre individus (liens inter-instances).
2. Le typage strict et la validation des plages/formats de littéraux.
3. Les règles d'alignement formel avec les axiomes inverses définis dans la RBox.
4. Le sas de recette qualité et de tolérance aux violations SHACL.

---

## 📐 3. Spécifications Formelles & Règles Métier

### 3.1 Intégrité Référentielle Inter-Instances
* **Intégrité Référentielle Stricte** `[EXG-FWK-02-01]` : Toute relation binaire `owl:ObjectProperty` instanciée dans l'ABox entre un individu $A$ et un individu $B$ doit pointer vers un individu $B$ obligatoirement déclaré et typé dans le graphe RDF. Aucun lien vers une URIs orpheline non instanciée n'est toléré.

### 3.2 Typage & Restricton des Literaux (Datatype Properties)
* **Typage et Conformation des Datatypes** `[EXG-FWK-02-02]` : Tout littéral d'instance doit porter un typage XML Schema explicite (`xsd:string`, `xsd:integer`, `xsd:decimal`, `xsd:dateTime`). La validation SHACL associée doit vérifier les critères de cardinalité (`sh:minCount`, `sh:maxCount`), les plages de valeurs (`sh:minInclusive`, `sh:maxInclusive`) et les motifs d'expressions régulières (`sh:pattern`).

### 3.3 Cohérence RBox & Inverses Factuels
* **Matérialisation des Relations Inverses** `[EXG-FWK-02-03]` : Pour toute assertion d'instance $A \xrightarrow{R} B$ où la propriété $R$ possède un inverse déclaré $R^{-1}$ via `owl:inverseOf` dans la RBox, l'assertion réciproque $B \xrightarrow{R^{-1}} A$ doit être formellement matérialisée dans l'ABox ou dérivable sans ambiguïté par le moteur de raisonnement.

### 3.4 Sanity Check & Tolérance de Recette
* **Recette CWA Tolérance Zéro** `[EXG-QUAL-02]` / `[EXG-QUAL-03]` : L'ABox est soumise à un contrôle automatisé pySHACL exécuté sous *Closed World Assumption*. Le statut d'acceptation de l'ABox exige **$0$ violation** de sévérité `sh:Violation`.

---

## 📊 4. Matrice Synthétique des Exigences (Index de Traçabilité)

| Identifiant | Intitulé de l'Exigence | Description & Critères d'Acceptation | Section Parent |
| :--- | :--- | :--- | :--- |
| **EXG-FWK-02-01** | **Intégrité Référentielle** | Interdiction de pointer vers une instance non déclarée dans l'ABox. | Section 3.1 |
| **EXG-FWK-02-02** | **Validation des Littéraux** | Contrôle des typages `xsd`, cardinalités et plages de valeurs. | Section 3.2 |
| **EXG-FWK-02-03** | **Matérialisation des Inverses** | Conformité des paires de relations inverses $(R, R^{-1})$ d'instances. | Section 3.3 |
| **EXG-QUAL-02** | **Conformité des Datatypes** | Respect strict des datatypes sous validation SHACL. | Section 3.4 |
| **EXG-QUAL-03** | **Sanity Check Zero Violation** | $0$ violation `sh:Violation` détectée lors du contrôle pySHACL. | Section 3.4 |

---

## 🛡️ 5. Gouvernance, Outillage & Validation

* **Validation Automatisée** : Script `03-Application/validate_abox.py` et suite Pytest (`test_phase2_quality.py`).
* **Artefacts Produits** : `DKG_ABox_Master.ttl` validé et snapshot d'immuabilité Phase 2.

---

## 📚 6. Pour aller plus loin (Ressources Pédagogiques)

* **[W3C] SHACL Property Shapes & Constraints** : [W3C SHACL Constraints](https://www.w3.org/TR/shacl/#core-components)
* **[RDF] RDF 1.1 Concepts and Abstract Syntax** : [W3C RDF 1.1](https://www.w3.org/TR/rdf11-concepts/)
"""

# 2. SPEC-UC-01_ABox_Instances.md (UseCase Cyber)
spec_uc_01_content = """# 📜 SPEC-UC-01 — Spécification d'Instanciation UseCase Cyber (ABox & SI Cyber)

> **Classification** : `TLP:AMBER`  
> **Statut** : 🟢 Approuvé  
> **Domaine** : Dynamic Knowledge Graph — UseCase Cyber  
> **Matrice de Rattachabilité** : `EXG-ABOX-01`, `EXG-ABOX-02`, `EXG-ABOX-03`, `EXG-QUAL-01`, `EXG-QUAL-02`, `EXG-QUAL-03`

---

## 📖 1. Glossaire des Acronymes

* **DKG** : Dynamic Knowledge Graph (Graphe de connaissances dynamique)
* **ABox** : Assertional Box (Données factuelles et instances du graphe)
* **CVE** : Common Vulnerabilities and Exposures (Référentiel des vulnérabilités)
* **CWE** : Common Weakness Enumeration (Référentiel des faiblesses logicielles)
* **CAPEC** : Common Attack Pattern Enumeration and Classification (Modes opératoires d'attaque)
* **CVSS** : Common Vulnerability Scoring System (Score de sévérité de 0.0 à 10.0)

---

## 🎯 2. Objet & Portée

La présente spécification encadre la réalisation du **Jeu de Données Factuelles de Synthèse (ABox)** pour le UseCase Cybersécurité (Phase 2).  
Elle définit :
1. La structure du namespace et la convention de nommage des URIs d'instances.
2. Le modèle de population de la cartographie du Système d'Information (Actifs, Composants).
3. L'intégration des Référentiels Publics de Menaces et Vulnérabilités (CVE, CWE, CAPEC, TLP).
4. Les règles d'export et d'assemblage du fichier maître `DKG_ABox_Master.ttl`.

---

## 📐 3. Spécifications Formelles & Règles Métier

### 3.1 Espaces de Noms & Nommage des Instances
* **Namespace Référentiel Données** `[EXG-ABOX-01]` : L'espace de noms d'instanciation du UseCase Cyber est strictement fixe à `http://dkg.cybersec.org/data/` (Préfixe : `dkg-data:`).
* **URIs Déterministes & Normalisées** `[EXG-ABOX-02]` : Les URIs d'instances doivent employer des identifiants stables et prévisibles (ex: `dkg-data:Asset-Srv-Prod-01`, `dkg-data:CVE-2021-41773`, `dkg-data:CWE-22`, `dkg-data:CAPEC-126`).

### 3.2 Structure du Jeu de Données de Synthèse Cyber
* **Compleétude du Graph Cyber** `[EXG-ABOX-03]` : Le jeu d'instances de synthèse doit obligatoirement inclure et relier la chaîne complète des entités métiers Cybersécurité :
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

### 3.3 Contrôles Qualité et Intégrité Données

- **Validation SHACL ABox** `[EXG-QUAL-01]` / `[EXG-QUAL-02]` : Toutes les instances du UseCase doivent satisfaire aux contraintes typiques de datatypes (`xsd:decimal` entre `0.0` et `10.0` pour les CVSS) et de cardinalités minimums sous CWA.
    
- **Intégrité de Recette** `[EXG-QUAL-03]` : Le fichier généré doit valider le Sanity Check sans aucune erreur `sh:Violation`.
    

## 📊 4. Matrice Synthétique des Exigences (Index de Traçabilité)

|**Identifiant**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|**Section Parent**|
|---|---|---|---|
|**EXG-ABOX-01**|**Namespace Instance Dedicated**|Utilisation exclusive de `http://dkg.cybersec.org/data/`.|Section 3.1|
|**EXG-ABOX-02**|**Identifiants URIs Déterministes**|Format de nommage normé pour Actifs, CVE, CWE, CAPEC.|Section 3.1|
|**EXG-ABOX-03**|**Instanciation Graphe Complète**|Population de la chaîne complète Asset $\rightarrow$ CVE $\rightarrow$ CWE $\rightarrow$ CAPEC.|Section 3.2|
|**EXG-QUAL-01**|**Couverture SHACL ABox**|Validation SHACL sur l'ensemble des individus du graphe.|Section 3.3|
|**EXG-QUAL-02**|**Typage & Plages CVSS**|Strict respect du format CVSS decimal $[0.0, 10.0]$.|Section 3.3|
|**EXG-QUAL-03**|**Sanity Check ABox Zero Error**|$0$ erreur de validation sous CWA lors du contrôle Pytest.|Section 3.3|

## 🛡️ 5. Gouvernance, Outillage & Validation

- **Validation Automatisée** : Execution du script Python `03-Application/generate_phase2_abox.py`.
    
- **Artefacts Produit** : Fichier maître `02-Donnees/Master_Transversal/DKG_ABox_Master.ttl`.
    

## 📚 6. Pour aller plus loin (Ressources Pédagogiques)

- **[NVD] National Vulnerability Database** : [NVD NIST](https://nvd.nist.gov/)
    
- **[MITRE] CWE / CAPEC Frameworks** : [MITRE Cyber](https://cwe.mitre.org/)