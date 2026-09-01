# 📜 SPEC-01 — Spécification du Socle Structurel Framework (TBox, RBox & SHACL)

> **Classification** : `TLP:AMBER`  
> **Statut** : 🟢 Approuvé  
> **Domaine** : Meta-Framework DKG (Dynamic Knowledge Graph)  
> **Matrice de Rattachabilité** : `EXG-TBOX-01`, `EXG-TBOX-02`, `EXG-TBOX-03`, `EXG-TBOX-04`, `EXG-TBOX-05`, `EXG-QUAL-01`, `EXG-SHACL-01`

---

## 📖 1. Glossaire des Acronymes

* **DKG** : Dynamic Knowledge Graph (Graphe de connaissances dynamique)
* **TBox** : Terminological Box (Composante décrivant la structure abstraite : classes et métadonnées)
* **RBox** : Role Box (Composante décrivant les propriétés, rôles, domaines/portées et axiomes d'inversion)
* **SHACL** : Shapes Constraint Language (Langage W3C de validation de contraintes structurelles)
* **SKOS** : Simple Knowledge Organization System (Standard d'alignement et de représentation lexicale)

---

## 🎯 2. Objet & Portée

La présente spécification définit la méta-architecture ontologique du **DKG Framework**.  
Elle est **strictement agnostique du domaine d'application** et fixe les règles formelles de construction :
1. De la couche Terminologique (**TBox** : typage OWL et règles d'héritage).
2. De la couche des Rôles (**RBox** : relations, domaines, portées et inverses formelles).
3. Du socle lexical multilingue (**SKOS**).
4. Des contraintes d'intégrité et de validation d'architecture (**SHACL Shapes**).

---

## 📐 3. Spécifications Formelles & Méta-Règles

### 3.1 Espaces de Noms & Séparateurs Abstraits
* **Séparateur dièse obligatoire** `[EXG-TBOX-01]` : Tout concept du Framework TBox/RBox doit résider sous l'espace de noms racine du framework et utiliser le séparateur `#` afin de garantir un chargement performant en mémoire du schéma d'ontologie.

### 3.2 Directives d'Architecture TBox (Classes & Typage)
* **Typage Formel Explicite** `[EXG-TBOX-02]` : Tout concept du schéma doit être explicitement typé `owl:Class`, `owl:ObjectProperty` ou `owl:DatatypeProperty`.
* **Héritage N-Tiers** : Les sous-classes doivent utiliser `rdfs:subClassOf` de manière stricte sans boucle cyclique.

### 3.3 Directives d'Architecture RBox (Relations & Inverses)
* **Domaine et Portée Explicites** `[EXG-TBOX-03]` : Toute relation entre entités doit être déclarée comme `owl:ObjectProperty` avec attribution stricte de son domaine (`rdfs:domain`) et de sa portée (`rdfs:range`).
* **Axiomes d'Inversion Systématiques** `[EXG-TBOX-04]` : Pour chaque relation binaire $R$, il doit exister une relation inverse $R^{-1}$ explicitée par l'attribut `owl:inverseOf`.

### 3.4 Directives Lexicales SKOS (Couche Multilingue)
* **Couverture Lexicale SKOS** `[EXG-TBOX-05]` : Chaque classe ou propriété abstraite déclarée doit obligatoirement comporter :
  * Un libellé principal `skos:prefLabel` en français (`@fr`) et anglais (`@en`).
  * Une définition textuelle explicite sous `skos:definition`.

### 3.5 Directives SHACL (Validation & Couplage Systématique)
* **Couplage Obligatoire TBox ↔ SHACL** `[EXG-QUAL-01]` : Toute classe déclarée dans la TBox (`owl:Class`) doit obligatoirement posséder une forme SHACL (`sh:NodeShape`) correspondante liée via `sh:targetClass`.
* **Méta-Shapes SHACL** `[EXG-SHACL-01]` : Le socle doit inclure la déclaration de `sh:NodeShape` et `sh:PropertyShape` conformes aux spécifications W3C pour valider sous *Closed World Assumption* (CWA) :
  * La cardinalité des propriétés (`sh:minCount`, `sh:maxCount`).
  * Le typage des valeurs pointées (`sh:class` ou `sh:datatype`).

---

## 📊 4. Matrice Synthétique des Exigences (Index de Traçabilité)

| Identifiant | Intitulé de l'Exigence | Description & Critères d'Acceptation | Section Parent |
| :--- | :--- | :--- | :--- |
| **EXG-TBOX-01** | **Espace de Noms & Séparateur `#`** | Obligation d'utiliser le séparateur `#` pour la TBox/RBox. | Section 3.1 |
| **EXG-TBOX-02** | **Typage OWL Strict** | $100\%$ des classes et propriétés doivent avoir un typage OWL formel. | Section 3.2 |
| **EXG-TBOX-03** | **Domaine et Portée Explicites** | Interdiction de déclarer une `owl:ObjectProperty` sans `rdfs:domain` ni `rdfs:range`. | Section 3.3 |
| **EXG-TBOX-04** | **Symétrie RBox & Inverses** | Toute propriété d'objet possède une propriété inverse liée par `owl:inverseOf`. | Section 3.3 |
| **EXG-TBOX-05** | **Couverture SKOS Complète** | Prescriptions `skos:prefLabel` (FR/EN) et `skos:definition` obligatoires. | Section 3.4 |
| **EXG-QUAL-01** | **Couplage TBox ↔ SHACL** | $100\%$ des classes `owl:Class` possèdent au moins une `sh:NodeShape` dédiée. | Section 3.5 |
| **EXG-SHACL-01** | **Méta-Shapes de Validation** | Présence de contraintes SHACL conformes aux spécifications W3C. | Section 3.5 |

---

## 🛡️ 5. Gouvernance, Outillage & Validation

* **Validation Automatisée** : Script `generate_phase1_socle.py` et contrôles Pytest.
* **Critère d'Acceptation** : Validation syntaxique RDF/Turtle et absence d'orphelins ou de propriétés sans inverse.
* **Artefact Produit** : Fichier TBox master du Framework (`DKG_TBox_Master.ttl`).

---

## 📚 6. Pour aller plus loin (Ressources Pédagogiques)

* **[W3C] OWL 2 Direct Semantics** : [W3C Recommendation](https://www.w3.org/TR/owl2-direct-semantics/)
* **[W3C] SHACL Core Language** : [W3C SHACL Specification](https://www.w3.org/TR/shacl/)