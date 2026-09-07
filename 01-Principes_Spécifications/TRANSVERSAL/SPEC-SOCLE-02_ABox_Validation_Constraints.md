# 📜 SPEC-SOCLE-02 — Spécification des Contraintes & Règles de Validation ABox

> **Classification** : `TLP:AMBER`  
> **Statut** : 🟢 Approuvé[cite: 10]  
> **Niveau d'Abstraction** : 🟢 SOCLE_TRANSVERSAL  
> **Public Cible** : Architectes Ontologues, Data Engineers & Développeurs DevSecOps  
> **Domaine Principal** : Meta-Framework DKG (`QU`, `SH`, `SE`)[cite: 10]  
> **Matrice de Rattachabilité** : `EXG-QU-02`, `EXG-QU-03`, `EXG-TB-04`

---

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif
La présente spécification définit les **règles formelles d'intégrité et de validation génériques de l'ABox** au sein du DKG Framework[cite: 10].  
Elle est **strictement agnostique du domaine d'application** et fixe les critères d'intégrité référentielle, le typage strict des littéraux, la cohérence des relations inverses et le sas de recette qualité sous CWA[cite: 10].

### 1.2 Glossaire Métier & Technique
| Acronyme / Terme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **DKG** | Dynamic Knowledge Graph | Graphe de connaissances dynamique[cite: 10]. |
| **ABox** | Assertional Box | Composante décrivant les individus, données factuelles et instances[cite: 10]. |
| **TBox** | Terminological Box | Schéma et concepts ontologiques[cite: 10]. |
| **SHACL** | Shapes Constraint Language | Langage W3C de validation de contraintes[cite: 10]. |
| **CWA** | Closed World Assumption | Hypothèse du monde fermé[cite: 10]. |

---

## 🎯 2. Périmètre & Rôle de la Spécification

* **Positionnement dans l'Architecture** : Document de niveau **Niveau 1 — Socle Transversal**. Il régit les conditions de recette qualité de toute ABox produite dans le projet[cite: 10].
* **Gouvernance & Validation** : Validé par le Lead Data/Ontologie. Il impose une tolérance zéro aux erreurs de structure RDF et aux pointeurs orphelins[cite: 10].

---

## 📐 3. Spécifications Formelles & Règles Métier

### 3.1 Intégrité Référentielle Inter-Instances
* **Intégrité Référentielle Stricte [`EXG-QU-02`]** : Toute relation binaire `owl:ObjectProperty` instanciée dans l'ABox entre un individu $A$ et un individu $B$ doit pointer vers un individu $B$ obligatoirement déclaré et typé dans le graphe RDF[cite: 10]. Aucun lien vers une URI orpheline non instanciée n'est toléré[cite: 10].

### 3.2 Typage & Restriction des Littéraux (Datatype Properties)
* **Validation des Littéraux & Datatypes [`EXG-QU-02`]** : Tout littéral d'instance doit porter un typage XML Schema explicite (`xsd:string`, `xsd:integer`, `xsd:decimal`, `xsd:dateTime`)[cite: 10]. La validation SHACL associée doit vérifier les critères de cardinalité (`sh:minCount`, `sh:maxCount`), les plages de valeurs (`sh:minInclusive`, `sh:maxInclusive`) et les motifs d'expressions régulières (`sh:pattern`)[cite: 10].

### 3.3 Cohérence RBox & Inverses Factuels
* **Matérialisation des Relations Inverses [`EXG-TB-04`]** : Pour toute assertion d'instance $A \xrightarrow{R} B$ où la propriété $R$ possède un inverse déclaré $R^{-1}$ via `owl:inverseOf` dans la RBox, l'assertion réciproque $B \xrightarrow{R^{-1}} A$ doit être formellement matérialisée dans l'ABox ou dérivable sans ambiguïté par le moteur de raisonnement[cite: 10].

### 3.4 Sanity Check & Tolérance de Recette
* **Sanity Check Zero Violation [`EXG-QU-03`]** : L'ABox est soumise à un contrôle automatisé `pySHACL` exécuté sous *Closed World Assumption* (CWA)[cite: 10]. Le statut d'acceptation de l'ABox exige **$0$ violation** de sévérité `sh:Violation`[cite: 10].

---

## 📊 4. Matrice Synthétique des Exigences (Index de Traçabilité)

| Identifiant | Domaine | Intitulé de l'Exigence | Description & Critères d'Acceptation | Section Parent | Mode de Validation |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **EXG-QU-02** | **`QU`** | **Intégrité & Datatypes CWA** | Interdiction de pointer vers une instance orpheline; contrôle strict des typages `xsd` et plages[cite: 10]. | Section 3.1 & 3.2 | pySHACL CWA |
| **EXG-QU-03** | **`QU`** | **Sanity Check Zero Violation** | $0$ violation `sh:Violation` détectée lors du contrôle automatisé `pySHACL`[cite: 10]. | Section 3.4 | Pytest / SHACL |
| **EXG-TB-04** | **`TB`** | **Matérialisation des Inverses** | Conformité et existence des paires de relations inverses $(R, R^{-1})$ d'instances[cite: 10]. | Section 3.3 | SPARQL / Reasoner |

---

## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest

* **Scripts de Génération / Validation** : `03-Application/validate_abox.py`[cite: 10].
* **Suites de Tests Associées** : `tests/test_phase2_quality.py`.
* **Artefacts Produits** : `DKG_ABox_Master.ttl` validé et snapshots d'immuabilité[cite: 10].

---

## 📚 6. Documents Liés & Références

* **[SPEC-SOCLE-00]** : Gouvernance du Cadre Spécifications & Exigences DKG.
* **[SPEC-SOCLE-01]** : Spécification du Framework TBox, RBox & SHACL.
* **[W3C SHACL]** : [W3C SHACL Core Components](https://www.w3.org/TR/shacl/#core-components)[cite: 10]