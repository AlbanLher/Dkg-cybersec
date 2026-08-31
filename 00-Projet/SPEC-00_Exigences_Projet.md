# 📑 Exigences Transverses et Normes de Qualité DKG

> **Statut** : Approuvé  
> **Application** : Transverse à l'ensemble du projet (Modules 00 à 13)  
> **Méthodologie** : Spec-Driven Development (SDD)

## 📐 1. Exigences d'Architecture & Ontologie TBox (`EXG-TBOX`)

| **Identifiant** | **Intitulé de l'Exigence**           | **Description & Critères d'Acceptation**                                                                                                                                          |
| --------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EXG-TBOX-01** | **Espace de Noms & Séparateur URI**  | L'ensemble des concepts TBox doit partager l'espace de noms `[http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)` et utiliser exclusivement le séparateur dièse (`#`). |
| **EXG-TBOX-02** | **Typage OWL Strict**                | Chaque entité déclarée doit posséder un typage OWL formel (`owl:Class`, `owl:ObjectProperty`, ou `owl:DatatypeProperty`).                                                         |
| **EXG-TBOX-03** | **Déclaration Domaine & Portée**     | Toute propriété doit définir explicitement son domaine (`rdfs:domain`) et sa portée (`rdfs:range`).                                                                               |
| **EXG-TBOX-04** | **Sémantique RBox & Inverses**       | Les relations bidirectionnelles doivent obligatoirement déclarer leur propriété inverse via `owl:inverseOf`.                                                                      |
| **EXG-TBOX-05** | **Couche Lexicale SKOS Obligatoire** | Toute entité TBox doit comporter au moins un `skos:prefLabel` (FR et EN), une `skos:definition`, et des `skos:altLabel` si applicables.                                           |

## 🛡️ 2. Exigences de Gouvernance & Validation SHACL (`EXG-QUAL`)

|**Identifiant**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|
|---|---|---|
|**EXG-QUAL-01**|**Couverture SHACL ABox**|Les instances d'entités majeures (`dkg:Asset`, `dkg:Vulnerability`, etc.) doivent faire l'objet de contraintes SHACL (`NodeShape`, `PropertyShape`).|
|**EXG-QUAL-02**|**Contrôle de Conformité des Données**|Les types de données (`xsd:datatype`), longueurs et plages de valeurs (ex: score CVSS entre 0.0 et 10.0) doivent être strictement validés sous CWA.|
|**EXG-QUAL-03**|**Sanity Check Automatisé**|Tout graphe ABox produit doit passer la validation SHACL sans lever de violation de sévérité `sh:Violation`.|

## 🔒 3. Exigences de Sécurité & Classification (`EXG-SEC`)

|**Identifiant**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|
|---|---|---|
|**EXG-SEC-01**|**Marquage TLP Obligatoire**|Tout fichier de données ou document produit doit porter une classification TLP explicite (ex: `TLP:AMBER`).|
|**EXG-SEC-02**|**Isolation des Snapshots**|Les snapshots de phases doivent être figés en lecture seule afin d'empêcher toute altération rétrospective des jalons.|

## 🔄 4. Exigences Organisationnelles & Qualité (`EXG-ORG`)

|**Identifiant**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|
|---|---|---|
|**EXG-ORG-01**|**Spécification Avant Code (Spec-Driven)**|Toute évolution d'ontologie ou d'architecture doit faire l'objet d'une mise à jour formelle des spécifications (`SPEC-XX`) avant modification des scripts.|
|**EXG-ORG-02**|**Parité Master / Snapshot**|Les artefacts générés dans `02-Donnees/Master_Transversal/` doivent avoir une empreinte binaire strictement identique à leur version dans `02-Donnees/Snapshots_Phases/`.|
|**EXG-ORG-03**|**Standard Traçabilité Phase_Content**|Le fichier `Phase_Content.md` de chaque phase doit obligatoirement structurer ses livrables selon les 4 briques (Framework, Instanciation, Data, Scripts/Tests).|
|**EXG-ORG-04**|**Gatekeeper & Checklist de Cadrage**|L'ouverture d'une Phase $N$ est conditionnée par la validation de `00-Projet/Cadrage_Checklist.md` et le contrôle de la clôture complète de la Phase $N-1$.|