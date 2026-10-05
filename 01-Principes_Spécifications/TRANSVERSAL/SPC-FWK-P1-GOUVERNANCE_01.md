---
type: spec
reference: SPC-FWK-P1-GOUV_01
revision: 1
titre: SPC-FWK-P1-GOUVERNANCE 01
titre_court: GOUV
phase_code: P1
phase_nom: Socle TBox & SHACL CWA
statut: 🟢 PASSED
portee: TRANSVERSAL
public_vise:
  - Architectes Ontologues
description: La présente spécification établit le cadre de gouvernance documentaire, organisationnel et technique pour le Dynamic Knowledge Graph (DKG) CyberSec. Elle définit le cycle de vie des exigences (`EXG-`), le découpage tripartite des spécifications, fixe la taxonomie officielle des domaines et établit les contraintes de sobriété hardware, d'isolation TLP et de qualité sémantique automatisée.
exigences:
  - id: EXG-FWK-P1-GOU_1
    code_exigence: EXG-OR-01
    domaine: OR
    domaine_nom: Organisation & Processus
    core: true
    phase: P1
    titre: Spec-Driven Development
    critere: Mise à jour SPEC obligatoire avant toute modification de code.
    test: Revue Git / Audit
  - id: EXG-FWK-P1-GOU_3
    code_exigence: EXG-OR-03
    domaine: OR
    domaine_nom: Organisation & Processus
    core: true
    phase: P1
    titre: Standard Traçabilité Phase
    critere: Découpage strict des livrables selon les 4 briques projet.
    test: Inspection Dossiers
  - id: EXG-FWK-P1-GOU_5
    code_exigence: EXG-OR-05
    domaine: OR
    domaine_nom: Organisation & Processus
    core: true
    phase: P1
    titre: Architecture SSOT (config.py)
    critere: Centralisation stricte des répertoires et URIs dans config.py.
    test: Test Python / AST
  - id: EXG-FWK-P1-GOU_6
    code_exigence: EXG-OR-06
    domaine: OR
    domaine_nom: Organisation & Processus
    core: true
    phase: P1
    titre: Double Export Anti-Collision
    critere: Synchronisation Snapshot -> Master sans erreur SameFileError.
    test: Execution Script
  - id: EXG-FWK-P1-GOU_8
    code_exigence: EXG-OR-08
    domaine: OR
    domaine_nom: Organisation & Processus
    core: true
    phase: P1
    titre: Unicité et Conformité des Domaines
    critere: Tout code de domaine utilisé doit obligatoirement figurer dans la taxonomie officielle.
    test: Pytest / Pydantic Enum Check / Linter Spec
  - id: EXG-FWK-P1-GOU_10
    code_exigence: EXG-HW-01
    domaine: HW
    domaine_nom: Hardware & Infrastructures
    core: false
    phase: P1
    titre: Inférence Local Économe
    critere: Exécution PC 16 Go RAM sans GPU dédié, Air-Gapped strict.
    test: Benchmark Resource
  - id: EXG-FWK-P1-GOU_11
    code_exigence: EXG-SE-01
    domaine: SE
    domaine_nom: Sécurité & Isolation
    core: true
    phase: P1
    titre: Marquage TLP Obligatoire
    critere: Tag TLP présent sur tout document ou graphe Turtle.
    test: Linter / Pytest
  - id: EXG-FWK-P1-GOU_13
    code_exigence: EXG-SE-03
    domaine: SE
    domaine_nom: Sécurité & Isolation
    core: true
    phase: P1
    titre: Air-Gapped & Modèles Locaux
    critere: Exécution MLOps/NLP 100% locale sans accès Internet runtime.
    test: Check Réseau / Cache
  - id: EXG-FWK-P1-GOU_14
    code_exigence: EXG-TB-01
    domaine: TB
    domaine_nom: TBox & Ontologies Master
    core: true
    phase: P1
    titre: Espace de Noms & Séparateur URI
    critere: "Namespace TBox unique avec séparateur #."
    test: Parsing RDF
  - id: EXG-FWK-P1-GOU_15
    code_exigence: EXG-TB-02
    domaine: TB
    domaine_nom: TBox & Ontologies Master
    core: true
    phase: P1
    titre: Typage OWL Strict
    critere: Typage formel obligatoire (owl:Class, owl:ObjectProperty).
    test: Parsing OWL / SPARQL
  - id: EXG-FWK-P1-GOU_16
    code_exigence: EXG-TB-03
    domaine: TB
    domaine_nom: TBox & Ontologies Master
    core: true
    phase: P1
    titre: Déclaration Domaine & Portée
    critere: rdfs:domain et rdfs:range obligatoires sur toute propriété.
    test: Requête SPARQL TBox
  - id: EXG-FWK-P1-GOU_17
    code_exigence: EXG-TB-04
    domaine: TB
    domaine_nom: TBox & Ontologies Master
    core: true
    phase: P1
    titre: Sémantique RBox & Inverses
    critere: Rôles inverses obligatoires via owl:inverseOf.
    test: Check Inverses SPARQL
  - id: EXG-FWK-P1-GOU_21
    code_exigence: EXG-QU-03
    domaine: QU
    domaine_nom: Qualité & Conformité
    core: true
    phase: P1
    titre: Sanity Check Automatisé
    critere: 0 violation sh:Violation au contrôle pySHACL.
    test: "Pytest / SHACL[cite: 1]"
  - id: EXG-FWK-P1-GOU_22
    code_exigence: EXG-QU-04
    domaine: QU
    domaine_nom: Qualité & Conformité
    core: true
    phase: P1
    titre: Vocabulaire TBox First
    critere: "0 prédicat hors-TBox Master utilisé dans le projet.[cite: 1]"
    test: "Pytest (test_00)[cite: 1]"
---


## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif

La présente spécification établit le cadre de gouvernance documentaire, organisationnel et technique pour le Dynamic Knowledge Graph (DKG) CyberSec. Elle définit le cycle de vie des exigences (`EXG-`), le découpage tripartite des spécifications, fixe la taxonomie officielle des domaines et établit les contraintes de sobriété hardware, d'isolation TLP et de qualité sémantique automatisée.

### 1.2 Glossaire Métier & Technique

| **Acronyme / Terme** | **Définition Complète**     | **Contextualisation DKG**                                                                                            |
| -------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **DKG**              | Dynamic Knowledge Graph     | Graphe de connaissances dynamique unifiant cartographie SI et CTI.                                                   |
| **SSOT**             | Single Source of Truth      | Centralisation des configurations, URIs et taxonomies dans un référentiel unique.                                   |
| **Air-Gapped**       | Environnement Isolé         | Exécution 100 % hors-ligne, sans aucun accès au réseau externe.                                                      |
| **CWA**              | Closed World Assumption     | Hypothèse du monde clos utilisée pour la validation SHACL stricte.                                                   |
| **TBox / ABox**      | Terminology / Assertion Box | Schéma ontologique master (`dkg:`) vs Graphe d'instances réelles.                                                    |
| **TLP**              | Traffic Light Protocol      | Protocole de partage et de restriction de l'information (CLEAR/AMBER/RED).                                           |
| **Pydantic V2**      | Boundary Validation         | Couche de typage et de validation au runtime garantissant le principe _Fail-Fast_ à la frontière des modules Python. |

## 🎯 2. Périmètre & Principes Directeurs

Cette spécification s'applique de manière **transversale à toutes les phases du projet**. Aucun code Python, graphe Turtle ou pipeline CI/CD ne peut déroger aux principes ci-dessous.

### 2.1 Principes Fondamentaux

1. **Spec-Driven First** : La spécification précède systématiquement le code et l'ontologie (`EXG-OR-01`).
    
2. **Accessibilité & Alignement Métier** : Le découpage documentaire permet au SOC de valider les règles métier (`SPEC-METIER`) sans barrière technique OWL/RDF (`SPEC-TECH`).
    
3. **Souveraineté & Sobriété Hardware** : Exécution locale sur machine standard (16 Go RAM) en mode strictement hermétique (`EXG-HW-01`).
    

## 📐 3. Architecture Documentaire Tripartite

Pour garantir la lisibilité par toutes les parties prenantes, la documentation est structurée selon trois niveaux d'abstraction stricts :

```text
docs/specs/
├── 01_TRANSVERSAL/
│   ├── SPEC-FWK-P1_Gouvernance_01.md
│   ├── SPEC-FWK-P1_T-RBox_SHACL_01.md
│   └── SPEC-FWK-P2_ABox_01.md
│   └── .....
├── 02_USECASE_METIER/
│   ├ SPEC-MET-P2_CARTO_01_Cartographie_Infractructure.md
│   └── .....
└── 03_USECASE_TECHNIQUE/
    ├── SPEC-TEC-P2_ABOX_01_Instanciation_ABox_Cyber.md
    └── ....
```
- **Niveau 1 — Socle Transversal (`SPEC-SOCLE-[NUM]`)** : Invariants applicables à tous les cas d'usage (Règles d'organisation, TBox Master, contraintes SHACL globales et politiques TLP).
    
- **Niveau 2 — Cas d'Usage Métier (`SPEC-METIER-[UC]`)** : Déclinaison fonctionnelle dédiée aux analystes SOC et CTI (Kill Chains, scénarios d'attaque, requêtes SPARQL de détection).
    
- **Niveau 3 — Cas d'Usage Technique (`SPEC-TECH-[UC]`)** : Spécification d'implémentation pour l'équipe DevSecOps (triplets RDF, règles SWRL/Inférence, scripts Python et assertions Pytest).
    

## 📐 4. Spécifications Formelles & Règles Métier

### 4.1 Organisation, Architecture & Sobriété Hardware

- **Spec-Driven First [`EXG-OR-01`]** : Aucun code, script ou fichier ontologique ne peut être produit ou modifié sans une spécification formelle préalable (`SPEC-FWK`, `SPEC-MET` ou `SPEC-TEC`).
    
- **Parité Binaire Master/Snapshot [`EXG-OR-02`]** : Les données maîtres dans `02-Donnees/Master_Transversal/` doivent posséder une empreinte identique aux snapshots figés dans `02-Donnees/Snapshots_Phases/`.
    
- **Traçabilité par Phase [`EXG-OR-03`]** : Chaque phase dispose de son dossier dédié avec traçabilité complète à travers 4 briques (Framework, Instanciation, Data, Scripts).
    
- **Gatekeeper Inter-Phase [`EXG-OR-04`]** : L'ouverture d'une Phase N est conditionnée par la validation du formulaire de cadrage et le contrôle de clôture de la Phase N-1.
    
- **Source Unique de Vérité (SSOT) [`EXG-OR-05`]** : L'intégralité des chemins, namespaces RDF et seuils applicatifs doivent être importés exclusivement depuis `03-Application/config.py`. Aucun chemin _hardcodé_ n'est toléré.
    
- **Double Export Safe Sync [`EXG-OR-06`]** : Chaque pipeline produit d'abord son livrable dans `Snapshots_Phases/`, puis le synchronise vers `Master_Transversal/` en vérifiant l'impossibilité de conflit (`if snapshot.resolve() != master.resolve():`).
    
- **Inférence Économe & Air-Gapped [`EXG-HW-01`]** : L'inférence du POC (graphe, règles, NER, agent vectoriel) doit s'exécuter localement sur un PC standard (16 Go RAM, sans GPU dédié). Les accès externes au runtime sont strictly interdits.
    
- **Validation aux Frontières (Boundary Validation) [`EXG-OR-07`]** : Toute donnée structurée ou semi-structurée entrant dans l'application doit être validée et typée par un modèle Pydantic V2 (`BaseModel` ou `BaseSettings`) avant d'être convertie en triplets RDF/RDFLib ou consommée par les moteurs d'inférence.
    
- **Unicité et Conformité des Domaines [`EXG-OR-08`]** : Tout code de domaine utilisé dans le coffre Obsidian, le code Python ou les graphes RDF doit obligatoirement figurer dans la table de la section 4.4.
    
- **Formatage des Identifiants d'Exigences [`EXG-OR-09`]** : Tout identifiant d'exigence doit respecter la forme `EXG-[CODE_DOMAINE]-[INDEX]` où `CODE_DOMAINE` est un domaine officiel validé.
    

### 4.2 Sécurité & Cloisonnement TLP

- **Marquage TLP Obligatoire [`EXG-SE-01`]** : Tout artefact (document Markdown, graphe Turtle) doit arborer son tag TLP explicite (`TLP:CLEAR`, `TLP:AMBER`, `TLP:RED`).
    
- **Isolation des Snapshots [`EXG-SE-02`]** : Les snapshots de jalons validés sont figés et conservés de façon immuable.
    
- **Souveraineté & Modèles Locaux [`EXG-SE-03`]** : Les modèles d'embeddings et de NER s'exécutent entièrement hors-ligne via le cache local `03-Application/models/cache/`.
    

### 4.3 Normes Sémantiques, TBox & Qualité

- **Namespace & Séparateur [`EXG-TB-01`]** : Espace de noms racine unique avec séparateur `#` pour la TBox.
    
- **Typage OWL Strict [`EXG-TB-02`]** : Typage formel obligatoire (`owl:Class`, `owl:ObjectProperty`, etc.).
    
- **Domaine & Portée Explicites [`EXG-TB-03`]** : Interdiction de déclarer une propriété sans `rdfs:domain` ni `rdfs:range`.
    
- **Inverses RBox [`EXG-TB-04`]** : Déclaration obligatoire de la propriété inverse via `owl:inverseOf`.
    
- **Couche Lexicale SKOS [`EXG-TB-05`]** : Présence obligatoire de `skos:prefLabel` (FR/EN) et `skos:definition`.
    
- **Couverture SHACL [`EXG-QU-01`]** : Validation SHACL couvrante sur l'ensemble du schéma.
    
- **Conformité Données CWA [`EXG-QU-02`]** : Validation des datatypes, longueurs et plages sous Closed World Assumption.
    
- **Sanity Check Automatisé [`EXG-QU-03`]** : Absence totale de violation de sévérité `sh:Violation`.
    
- **Vocabulaire TBox First [`EXG-QU-04`]** : Zéro prédicat ou classe hors-TBox Master utilisé dans le projet (contrôlé par `test_00`).
    
- **Shapes Structurales [`EXG-SH-01`]** : Méta-shapes de validation intégrées au schéma.
    

### 4.4 Taxonomie Officielle des Domaines & Conventions ID

#### 4.4.1 Référentiel des Domaines Autorisés (SSOT)

Tout composant, fichier de spécification, dictionnaire YAML ou code Python **doit obligatoirement** rattacher ses exigences à l'un des domaines officiels ci-dessous [`EXG-OR-08`]. L'ajout d'un nouveau domaine nécessite un amendement de cette spécification de Gouvernance.

| **Code Domaine** | **Nom Complet**             | **Description & Périmètre**                                                      | **Exemples de Périmètre**                                        |
| ---------------- | --------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **`CT`**         | Cyber Threat Intelligence   | Modélisation des données CTI externes, vulnérabilités et menaces.                | CVE, CWE, CAPEC, CISA KEV, scores CVSS.                          |
| **`HW`**         | Hardware & Infrastructures  | Contraintes matérielles, d'exécution locale et de performance système.           | Limites RAM 16 Go, absence de GPU, mode Air-Gapped.              |
| **`IN`**         | Inférence & Graph Analytics | Règles de raisonnement sémantique, déduction de liens et calculs de propagation. | Détection de cascade de risque, classe `HighRiskAsset`.          |
| **`OR`**         | Organisation & Processus    | Gouvernance du projet, méthodologie Spec-Driven et standards de livraison.       | Traçabilité des phases, conventions Git, parité Master/Snapshot. |
| **`QU`**         | Qualité & Conformité        | Règles de validation de la qualité des données et métriques d'intégrité.         | Contrôles pySHACL, fermetures CWA, 0 violation SHACL.            |
| **`SE`**         | Sécurité & Isolation        | Étanchéité, marquage TLP et politiques de contrôle d'accès aux graphes.          | Ségrégation TLP:CLEAR vs TLP:RED, isolation des snapshots.       |
| **`SH`**         | SHACL Shapes                | Modélisation abstraite et concrète des formes de validation de structures.       | `sh:NodeShape`, `sh:PropertyShape`, méta-shapes.                 |
| **`TB`**         | TBox & Ontologies Master    | Définition formelle des classes, propriétés, relations inverses et SKOS.         | Classes OWL, `rdfs:domain`/`range`, `owl:inverseOf`, SKOS.       |
| **`TEC`**        | Technique & Core Framework  | Socle applicatif, gestion des types de données, immutabilité et bas niveau.      | Schemas Pydantic V2, horodatage UTC, immutabilité payloads.      |

> ⚠️ **Règle de nettoyage 5S (Remplacement des codes obsolètes) :**
> 
> - Remplacer **`SEC`** par **`SE`** (Sécurité & Isolation).
>     
> - Remplacer **`IA`** par **`IN`** (Inférence) ou **`CT`** selon le cas d'usage.
>     
> - Le code temporaire **`XX`** est strictement interdit en version approuvée.
>     

#### 4.4.2 Convention de Nommage des IDs [`EXG-OR-09`]

Toute exigence doit respecter la forme regex : `^EXG-([A-Z]{2,4})-[0-9]{2,3}$` (exemples : `EXG-TB-01`, `EXG-SE-03`, `EXG-OR-08`).

## 📊 5. Matrice Synthétique des Exigences (Index de Traçabilité)

| **Identifiant** | UID               | **Domaine** | Core/Non-Core | **Intitulé de l'Exigence**           | **Description & Critères d'Acceptation**                                                | **Mode de Validation**                     |
| --------------- | ----------------- | ----------- | ------------- | ------------------------------------ | --------------------------------------------------------------------------------------- | ------------------------------------------ |
| **EXG-OR-01**   | EXG-FWK-P1-GOU_1  | `OR`        | Core          | Spec-Driven Development              | Mise à jour SPEC obligatoire avant toute modification de code.                          | Revue Git / Audit                          |
| **EXG-OR-02**   | EXG-FWK-P1-GOU_2  | `OR`        | Core          | Parité Master / Snapshot             | Empreinte binaire identique entre Master et Snapshot.                                   | Control Hash / CI                          |
| **EXG-OR-03**   | EXG-FWK-P1-GOU_3  | `OR`        | Core          | Standard Traçabilité Phase           | Découpage strict des livrables selon les 4 briques projet.                              | Inspection Dossiers                        |
| **EXG-OR-04**   | EXG-FWK-P1-GOU_4  | `OR`        | Core          | Gatekeeper Inter-Phase               | Validation préalable du formulaire de cadrage inter-phase.                              | Validation Cadrage                         |
| **EXG-OR-05**   | EXG-FWK-P1-GOU_5  | `OR`        | Core          | Architecture SSOT (`config.py`)      | Centralisation stricte des répertoires et URIs dans `config.py`.                        | Test Python / AST                          |
| **EXG-OR-06**   | EXG-FWK-P1-GOU_6  | `OR`        | Core          | Double Export Anti-Collision         | Synchronisation Snapshot -> Master sans erreur `SameFileError`.                         | Execution Script                           |
| **EXG-OR-07**   | EXG-FWK-P1-GOU_7  | `OR`        | Core          | Validation aux Frontières (Pydantic) | Validation stricte des données entrantes/configs via Pydantic V2 avant conversion RDF.  | Pytest / Pydantic `ValidationError`        |
| **EXG-OR-08**   | EXG-FWK-P1-GOU_8  | `OR`        | Core          | Unicité et Conformité des Domaines   | Tout code de domaine utilisé doit obligatoirement figurer dans la taxonomie officielle. | Pytest / Pydantic Enum Check / Linter Spec |
| **EXG-OR-09**   | EXG-FWK-P1-GOU_9  | `OR`        | Core          | Formatage des IDs                    | Format strict `^EXG-([A-Z]{2,4})-[0-9]{2,3}$` rattaché à un domaine officiel.           | Linter Regex / CI AST Check                |
| **EXG-HW-01**   | EXG-FWK-P1-GOU_10 | `HW`        | Non-Core      | Inférence Local Économe              | Exécution PC 16 Go RAM sans GPU dédié, Air-Gapped strict.                               | Benchmark Resource                         |
| **EXG-SE-01**   | EXG-FWK-P1-GOU_11 | `SE`        | Core          | Marquage TLP Obligatoire             | Tag TLP présent sur tout document ou graphe Turtle.                                     | Linter / Pytest                            |
| **EXG-SE-02**   | EXG-FWK-P1-GOU_12 | `SE`        | Core          | Isolation des Snapshots              | Immuabilité des snapshots de jalons validés.                                            | Droits Fichiers                            |
| **EXG-SE-03**   | EXG-FWK-P1-GOU_13 | `SE`        | Core          | Air-Gapped & Modèles Locaux          | Exécution MLOps/NLP 100% locale sans accès Internet runtime.                            | Check Réseau / Cache                       |
| **EXG-TB-01**   | EXG-FWK-P1-GOU_14 | `TB`        | Core          | Espace de Noms & Séparateur URI      | Namespace TBox unique avec séparateur `#`.                                              | Parsing RDF                                |
| **EXG-TB-02**   | EXG-FWK-P1-GOU_15 | `TB`        | Core          | Typage OWL Strict                    | Typage formel obligatoire (`owl:Class`, `owl:ObjectProperty`).                          | Parsing OWL / SPARQL                       |
| **EXG-TB-03**   | EXG-FWK-P1-GOU_16 | `TB`        | Core          | Déclaration Domaine & Portée         | `rdfs:domain` et `rdfs:range` obligatoires sur toute propriété.                         | Requête SPARQL TBox                        |
| **EXG-TB-04**   | EXG-FWK-P1-GOU_17 | `TB`        | Core          | Sémantique RBox & Inverses           | Rôles inverses obligatoires via `owl:inverseOf`.                                        | Check Inverses SPARQL                      |
| **EXG-TB-05**   | EXG-FWK-P1-GOU_18 | `TB`        | Core          | Couche Lexicale SKOS                 | Labels multilingues (FR/EN) et définitions SKOS.                                        | Validation SKOS                            |
| **EXG-QU-01**   | EXG-FWK-P1-GOU_19 | `QU`        | Core          | Couverture SHACL                     | Validation SHACL couvrante sur l'ensemble du schéma.                                    | Execution pySHACL                          |
| **EXG-QU-02**   | EXG-FWK-P1-GOU_20 | `QU`        | Core          | Contrôle Conformité Données          | Datatypes, plages et formats validés sous CWA.                                          | pySHACL CWA                                |
| **EXG-QU-03**   | EXG-FWK-P1-GOU_21 | `QU`        | Core          | Sanity Check Automatisé              | 0 violation `sh:Violation` au contrôle pySHACL.                                         | Pytest / SHACL[cite: 1]                    |
| **EXG-QU-04**   | EXG-FWK-P1-GOU_22 | `QU`        | Core          | Vocabulaire TBox First               | 0 prédicat hors-TBox Master utilisé dans le projet.[cite: 1]                            | Pytest (`test_00`)[cite: 1]                |
| **EXG-SH-01**   | EXG-FWK-P1-GOU_23 | `SH`        | Core          | Shapes Structurales Abstraites       | Méta-shapes de validation intégrées au schéma.[cite: 1]                                 | Execution SHACL[cite: 1]                   |

## 🛡️ 6. Outillage, CI/CD & Traçabilité Pytest

L'ensemble des exigences est vérifié automatiquement à chaque commit via la suite de tests unitaires et d'intégration[cite: 1] :

- **Centralisation de Configuration** : `03-Application/config.py`
    
    [cite: 1]
    
- **Moteur de Validation SHACL** : Executé via `pyshacl` sur la TBox Master et les ABox d'instances[cite: 1].
    
- **Suites de Tests Pytest** :
    
    - `tests/test_00_governance_and_tbox.py` (Vérifie `EXG-OR-*`, `EXG-TB-*`, `EXG-QU-04`)[cite: 1]
        
    - `tests/test_01_shacl_and_quality.py` (Vérifie `EXG-QU-01` à `03`, `EXG-SH-01`)[cite: 1]
        
    - `tests/test_02_security_and_tlp.py` (Vérifie `EXG-SE-01` à `03`)[cite: 1]
        

## 📚 7. Documents Liés & Références

- **[TEMPLATE_SPECIFICATION]** : Modèle unifié de rédaction des spécifications du projet.[cite: 1]
    
- **[SPEC-FWK-01]** : Spécification du Framework TBox, RBox et Contraintes SHACL Globale.[cite: 1]
    
- **[SPEC-MET-UC02]** : Scénario d'Attaque Silent Cascade (Description Métier SOC).[cite: 1]
    
- **[SPEC-TEC-UC03]** : Instanciation & Raisonnement (Propagation Silent Cascade).[cite: 1]