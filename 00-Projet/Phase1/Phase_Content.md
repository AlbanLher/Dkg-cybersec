# Phase 1 — Socle Modèle Canonique & Qualité (TBox / RBox / SHACL)
# étape 1 : Cadrage 

> **Fichier** : `00-Projet/Phase1/Phase_Content.md`  
> **Classification TLP** : `TLP:AMBER`  
> **Phase** : Phase 1 — Initialisation Socle Modèle Canonique & Qualité  
> **Étape Actuelle** : Étape 1 : Cadrage (`EXG-PROJ-12`)  
> **Répertoire Code** : `13-Application/Phase_1_Socle/`  
> **Répertoires Données Cibles** :
> * Master Transversal : `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/`
> * Snapshot Phase 1 : `02-Donnees/Snapshots_Phases/Phase_1_Socle/`

## 🎯 1. Analyse du Backlog & Sélection des Concepts / Fonctions (Étape 1 - Cadrage)

Conformément à `EXG-PROJ-12`, cette étape analyse le backlog général pour retenir les concepts et fonctions d'initialisation du socle :

### 🟢 Concepts & Fonctions retenus pour la Phase 1 :
* **TBox (Terminology Box)** : Modélisation des classes de base (`Asset`, `SoftwareComponent`, `Vulnerability`, `Weakness`, `ThreatPattern`, `TLPMarking`) et de leurs propriétés de types de données (Datatypes).
* **RBox (Relationship Box)** : Définition des propriétés d'objets, typologies de relations et relations inverses (ex: `hasInstalledComponent` ↔ `isComponentOf`, `hasVulnerability`, `hasWeakness`).
* **SHACL (Shapes Constraint Language)** : Validation des contraintes de structure et de typage sous Closed World Assumption (CWA) dans un cas simple (validation IP, bornes CVSS 0.0–10.0, typage strict).
* **Documentation & Restitution** : Génération human-readable (`SPEC-01`) avec glossaire des acronymes et diagramme Mermaid.

### 🔴 Concepts & Fonctions laissés dans le Backlog (Phases Ultérieures) :
* Instanciation des données ABox et peuplement interne ➡️ **Phase 2**
* Enrichissement par sources externes & Marquage de Gouvernance TLP complet ➡️ **Phase 3**
* Requêtage SPARQL/Cypher, Base Graphe Neo4j, NER Hybride, Embeddings, RAG & Fine-Tuning ➡️ **Phase 4 (Backlog)**

---

## 📐 2. Analyse de Cohérence & Structure des Spécifications Attendues

* **Spécification Cible** : `SPEC-01` (Norme TBox & RBox, restitution Markdown human-readable, Mermaid & Acronymes).
* **Découpage des spécifications** :
  1. Modèle TBox/RBox au format Turtle (`.ttl`) et JSON-LD (`.json`).
  2. Modèle SHACL (`shapes_abox.ttl`) pour la qualification d'intégrité.
  3. Spécification documentaire Markdown (`.md`) pour la pédagogie et la compréhension des enjeux du socle.

---

## 📦 3. Ébauche des Livrables Data et Script du Pipeline

### Livrable Data (Socle & Snapshots) :
* `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.ttl`
* `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.json`
* `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.md`
* `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/shapes_abox.ttl`
* *(Et leurs répliques miroir dans `02-Donnees/Snapshots_Phases/Phase_1_Socle/`)*

### Livrables Scripts Pipeline (Code & Test) :
* `13-Application/Phase_1_Socle/generate_phase1_socle.py` : Script de génération du triptyque TBox/RBox/SHACL.
* `13-Application/Phase_1_Socle/test_phase1_quality.py` : Suite de validation `pytest` (conformité SHACL sous CWA, complétude TBox, validation `SPEC-01`).

---

## 📝 4. Proposition de Mise à Jour du Fichier `PhasesProjet.md`

Mise à jour du tableau de suivi des phases :
* **Phase 1** : Statut passant à `En Cours (Étape 1 : Cadrage validée)`.
* **Périmètre validé Phase 1** : TBox (Datatypes), RBox (Relations & Inverses), SHACL simple.
* **Backlog Phase 2+** : ABox, Sources Externes, Neo4j, LLM/RAG.

---


# étape 2 : Specification

> **Fichier** : `00-Projet/Phase1/Phase_Content.md`  
> **Classification TLP** : `TLP:AMBER`  
> **Phase** : Phase 1 — Initialisation Socle Modèle Canonique & Qualité  
> **Étape Actuelle** : Étape 2 : Specification (`EXG-PROJ-13`)  
> **Spécification Rattachée** : `./01-Principes_Specifications/Specification/SPEC-01_TBox_RBox_SHACL.md`

---

## 📄 1. Contenu des Spécifications Cibles (Spécification `SPEC-01`)

Conformément à `EXG-PROJ-13`, l'Étape 2 définit le contenu détaillé de la spécification **`SPEC-01`** qui gouverne la modélisation du socle canonique.

### 1.1 Norme de Modélisation TBox / RBox (OWL)
* **Ontologie Canonique** : URI de base `<http://dkg.cybersec/ontology/v1#>`
* **Classes TBox principales** :
  * `Asset` : Actif du système d'information.
  * `SoftwareComponent` : Composant logiciel ou brique applicative.
  * `Vulnerability` : Vulnérabilité (ex: entrée CVE).
  * `Weakness` : Faiblesse logicielle sous-jacente (ex: CWE).
  * `ThreatPattern` : Motifs d'attaque ou techniques (ex: CAPEC/ATT&CK).
  * `TLPMarking` : Marquage de gouvernance et de confidentialité TLP (`TLP:CLEAR`, `TLP:GREEN`, `TLP:AMBER`, `TLP:RED`).
* **Propriétés RBox & Inverses** :
  * `hasInstalledComponent` (Domain: `Asset`, Range: `SoftwareComponent`) ↔ Inverse : `isComponentOf`
  * `hasVulnerability` (Domain: `SoftwareComponent`, Range: `Vulnerability`) ↔ Inverse : `isVulnerabilityOf`
  * `hasWeakness` (Domain: `Vulnerability`, Range: `Weakness`)
  * `hasTLPMarking` (Domain: `owl:Thing`, Range: `TLPMarking`)

### 1.2 Regles d'Intégrité SHACL (Closed World Assumption - CWA)
* **Forme SHACL globale** : `shapes_abox.ttl`
* **Contraintes appliquées** :
  * **Chaque `Asset`** doit obligatoirement posséder un identifiant `assetId` (string) et au moins un marquage `hasTLPMarking`.
  * **Chaque `Vulnerability`** doit définir un score CVSS compris strictement entre `0.0` et `10.0` (`sh:minInclusive 0.0`, `sh:maxInclusive 10.0`).
  * **Typage strict des IPs** : `ipAddress` doit respecter un pattern Regex IPv4 conforme.

### 1.3 Format & Rendu des Spécifications (`EXG-PROJ-02`, `SPEC-01`)
Chaque artefact du socle généré doit l'être sous **trois formats synchronisés** :
1. **Turtle (`.ttl`)** : Format RDF natif pour requêtage et raisonneur.
2. **JSON-LD (`.json`)** : Format de transfert d'API et d'intégration web.
3. **Markdown (`.md`)** : Documentation lisible par l'humain, intégrant **obligatoirement** :
   * La table explicative des acronymes utilisés (`TBox`, `RBox`, `ABox`, `SHACL`, `CVSS`, `TLP`, etc.).
   * Un diagramme conceptuel **Mermaid.js** illustrant les classes et leurs relations.

---

## 📊 2. Identification des Données Source Complémentaires à Générer

Pour l'étape suivante (`Étape 3 : Donnees_source`), nous identifions le besoin de générer un jeu de **données synthétiques ABox d'illustration et de test** :

1. **Jeu Conforme (Nominal)** :
   * 1 `Asset` serveur critique avec marquage `TLP:AMBER`.
   * 2 `SoftwareComponent` associés.
   * 1 `Vulnerability` (ex: `CVE-2024-XXXX`) avec score CVSS = `7.8`.
2. **Jeu Non-Conforme (Anomalies pour qualification SHACL)** :
   * 1 `Vulnerability` avec score CVSS = `12.5` (hors borne SHACL 0–10).
   * 1 `Asset` sans identifiant `assetId` obligatoire.
   * 1 `Asset` avec adresse IP invalide (ex: `999.999.999.999`).

---

## 🛠️ 3. Vue à Jour des Livrables Data & Script du Pipeline

| Typologie         | Fichier / Artefact                             | Localisation Target                                     | Rôle dans le Pipeline                                                   |
| :---------------- | :--------------------------------------------- | :------------------------------------------------------ | :---------------------------------------------------------------------- |
| **Spécification** | `SPEC-01_TBox_RBox_SHACL.md`                   | `./01-Principes_Specifications/Specification/`          | Spécification méthodologique et fonctionnelle du socle (`EXG-PROJ-13`). |
| **Data Master**   | `DKG_TBox_Master.ttl`                          | `./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/` | TBox/RBox canonique format Turtle.                                      |
| **Data Master**   | `DKG_TBox_Master.json`                         | `./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/` | TBox/RBox canonique format JSON-LD.                                     |
| **Data Master**   | `DKG_TBox_Master.md`                           | `./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/` | Doc humaine avec Acronymes et Mermaid (`SPEC-01`).                      |
| **Data Master**   | `shapes_abox.ttl`                              | `./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/` | Formes de validation SHACL.                                             |
| **Data Snapshot** | `DKG_TBox_Phase1.*` / `shapes_abox_Phase1.ttl` | `./02-Donnees/Snapshots_Phases/Phase_1_Socle/`          | Snapshots miroir de livraison de la Phase 1.                            |
| **Script Dev**    | `generate_phase1_socle.py`                     | `./13-Application/Phase_1_Socle/`                       | Generator Python (rdflib / json-ld / md).                               |
| **Script Test**   | `test_phase1_quality.py`                       | `./13-Application/Phase_1_Socle/`                       | Suite `pytest` (SHACL CWA, validation `SPEC-01`).                       |

----

# étape 3 : Données

> **Fichier** : `00-Projet/Phase1/Phase_Content.md`  
> **Classification TLP** : `TLP:AMBER`  
> **Phase** : Phase 1 — Initialisation Socle Modèle Canonique & Qualité  
> **Étape Actuelle** : Étape 3 : Donnees_source (`EXG-PROJ-14`)

---

## 🏗️ 1. Définition Prioritaire du Socle TBox & RBox (Méta-Modèle)

Conformément au périmètre strict de la Phase 1, les données sources principales de cette étape sont les **déclarations de Schéma Ontologique (TBox/RBox)** et leurs **contraintes d'intégrité (SHACL)**.

### 1.1 Classes TBox à Instancier dans le Socle
Les concepts sémantiques canoniques obligatoires définis pour cette phase sont :
* `dkg:Asset` : Classe représentant une ressource informatique.
* `dkg:SoftwareComponent` : Classe représentant un composant logiciel.
* `dkg:Vulnerability` : Classe représentant une vulnérabilité (ex: CVE).
* `dkg:Weakness` : Classe représentant une faiblesse logicielle (ex: CWE).
* `dkg:ThreatPattern` : Classe représentant un mode opératoire d'attaque (ex: CAPEC).
* `dkg:TLPMarking` : Classe représentant le niveau de confidentialité TLP.

### 1.2 Axiomes de Relations & Inverses RBox
Les propriétés d'objets, leurs domaines, leurs portées et leurs symétries/inverses algébriques :
* `dkg:hasInstalledComponent`  
  * `rdfs:domain dkg:Asset` | `rdfs:range dkg:SoftwareComponent`  
  * `owl:inverseOf dkg:isComponentOf`
* `dkg:isComponentOf`  
  * `rdfs:domain dkg:SoftwareComponent` | `rdfs:range dkg:Asset`
* `dkg:hasVulnerability`  
  * `rdfs:domain dkg:SoftwareComponent` | `rdfs:range dkg:Vulnerability`  
  * `owl:inverseOf dkg:isVulnerabilityOf`
* `dkg:hasWeakness`  
  * `rdfs:domain dkg:Vulnerability` | `rdfs:range dkg:Weakness`
* `dkg:hasTLPMarking`  
  * `rdfs:domain owl:Thing` | `rdfs:range dkg:TLPMarking`

---

## 🧪 2. Données Synthétiques Minimales de Qualification TBox/SHACL

Ces fragments de données synthétiques ne constituent pas le peuplement du DKG (réservé à la Phase 2 ABox), mais servent exclusivement de **banc d'essai** pour qualifier la TBox/RBox et tester le blocage SHACL sous CWA :

1. **Jeu de qualification TBox/RBox (Nominal)** :
   * 1 triplet minimal de chaque classe pour vérifier le typage (`rdf:type`).
   * 1 paire de chaque relation pour vérifier la cohérence des inverses RBox (`hasInstalledComponent` ↔ `isComponentOf`).
2. **Jeu d'anomalies SHACL (Hors-Conformité)** :
   * 1 donnée test violant le typage d'un Datatype (`cvssScore > 10.0`).
   * 1 donnée test violant une cardinalité minimale (absence d'identifiant obligatoire).

---

## 🛠️ 3. Vue à Jour des Livrables Data & Script

| Typologie            | Fichier / Artefact            | Localisation Target                                     | Rôle dans la Phase 1                                |
| :------------------- | :---------------------------- | :------------------------------------------------------ | :-------------------------------------------------- |
| **Socle TBox/RBox**  | `DKG_TBox_Master.ttl`         | `./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/` | Schéma OWL 2 des Classes et Relations inverses.     |
| **Contrat SHACL**    | `shapes_abox.ttl`             | `./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/` | Shapes de validation associées aux Classes TBox.    |
| **Data Synthétique** | `synthetic_qualification.ttl` | `./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/` | Échantillon minimal pour test unitaires TBox/SHACL. |
| **Snapshots Phase**  | *Fichiers Miroirs Phase 1*    | `./02-Donnees/Snapshots_Phases/Phase_1_Socle/`          | Traçabilité et archivage (`EXG-ORG-02`).            |

---



##  étape 4 : Script 

> **Fichier** : `00-Projet/Phase1/Phase_Content.md`  
> **Classification TLP** : `TLP:AMBER`  
> **Phase** : Phase 1 — Initialisation Socle Modèle Canonique & Qualité  
> **Étape Actuelle** : Étape 4 : Script-Test (`EXG-PROJ-15`)  
> **Répertoire applicatif cible** : `13-Application/Phase_1_Socle/`

---

## 🛠️ 1. Structure du Répertoire Applicatif (`13-Application/Phase_1_Socle/`)

Les scripts d'exécution et le harnais de test automatisé sont organisés comme suit :

```text
13-Application/
└── Phase_1_Socle/
    ├── generate_phase1_socle.py    # Script principal de génération du triptyque (TBox/RBox/SHACL)
    ├── test_phase1_quality.py      # Suite de tests automatisés Pytest (Qualité, SHACL CWA, SPEC-01)
    └── conftest.py                 # Fixtures Pytest (chargement des graphes et données de qualification)
```

## ⚙️ 2. Architecture des Scripts de Génération & Qualification

### 2.1 Script de Génération Principal : `generate_phase1_socle.py`

Le script s'appuie sur `rdflib` et exécute la séquence d'instructions suivante :

1. **Construction du Graphe TBox / RBox** :
    
    - Déclaration du namespace unique `http://dkg.cybersec.org/tbox#` (`EXG-TBOX-01`).
        
    - Instanciation explicite des `owl:Class` et `owl:ObjectProperty` (`EXG-TBOX-02`).
        
    - Renseignement strict des `rdfs:domain` et `rdfs:range` pour 100% des propriétés (`EXG-TBOX-03`).
        
    - Déclaration des axiomes RBox d'inversibilité (`owl:inverseOf`) pour les paires de relations (`EXG-TBOX-04`).
        
2. **Construction du Graphe SHACL (`shapes_abox.ttl`)** :
    
    - Association d'au moins une `sh:NodeShape` pour chaque classe TBox (`EXG-QUAL-01`).
        
    - Injection des règles de validation (bornes CVSS float 0.0-10.0, minCount 1 sur les identifiants, Regex IPv4).
        
3. **Sérialisation Triple-Format (`EXG-PROJ-02`, `SPEC-01`)** :
    
    - Génération des formats RDF Turtle (`.ttl`) et JSON-LD (`.json`).
        
    - Génération de la documentation Markdown (`.md`) incorporant **le Glossaire des Acronymes** et **le schéma Mermaid.js**.
        
4. **Double Écriture Synchronisée (`EXG-ORG-02`)** :
    
    - Copie des artefacts dans `./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/`
        
    - Copie miroir dans `./02-Donnees/Snapshots_Phases/Phase_1_Socle/`
        

### 2.2 Suite de Tests Automatisés : `test_phase1_quality.py` (Pytest)

La suite de tests agit comme gatekeeper qualité du pipeline et valide les 5 points de contrôle suivants :

Python

```
# Extrait de la logique de test_phase1_quality.py

def test_exg_tbox_01_to_04_rules(tbox_graph):
    """Vérifie le respect strict des exigences ontologiques EXG-TBOX-01 à 04."""
    # EXG-TBOX-01 : Validation de l'URI de base avec délimiteur '#'
    # EXG-TBOX-02 : Vérification du typage owl:Class / owl:ObjectProperty
    # EXG-TBOX-03 : Vérification que chaque ObjectProperty a un domain ET un range
    # EXG-TBOX-04 : Vérification de la présence d'axiomes owl:inverseOf

def test_exg_qual_01_shacl_coverage(tbox_graph, shacl_graph):
    """Vérifie que 100% des classes TBox ont une sh:NodeShape associée."""
    ...

def test_exg_qual_04_shacl_cwa_validation(shacl_graph, synthetic_valid, synthetic_invalid):
    """Vérifie l'acceptation de la donnée conforme et le rejet de l'anomalie sous CWA."""
    # Valide avec pyshacl que synthetic_valid.ttl passe à 100%
    # Valide que synthetic_invalid.ttl lève un rapport de non-conformité avec arrêt pipeline

def test_spec_01_markdown_requirements(markdown_file_path):
    """Vérifie la présence du Glossaire des Acronymes et du bloc Mermaid dans le MD."""
    ...

def test_exg_org_02_master_snapshot_parity():
    """Vérifie l'identité stricte des contenus entre Master_Transversal et Snapshots_Phases."""
    ...
```

## 📊 3. Vue à Jour des Livrables Data & Script

|**Typologie**|**Fichier / Artefact**|**Localisation Target**|**Rôle dans la Phase 1**|
|---|---|---|---|
|**Script Dev**|`generate_phase1_socle.py`|`./13-Application/Phase_1_Socle/`|Script principal de génération du triptyque TBox/RBox/SHACL.|
|**Script Test**|`test_phase1_quality.py`|`./13-Application/Phase_1_Socle/`|Suite `pytest` de validation des règles `EXG-TBOX-*`, `EXG-QUAL-*` et `SPEC-01`.|
|**Config Test**|`conftest.py`|`./13-Application/Phase_1_Socle/`|Fixtures `pytest` pour le chargement des graphes et données de qualification.|
|**Data Master**|Artefacts Master Transversal|`./02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/`|`DKG_TBox_Master.ttl`, `.json`, `.md` et `shapes_abox.ttl`.|
|**Data Snapshot**|Artefacts Snapshot Phase 1|`./02-Donnees/Snapshots_Phases/Phase_1_Socle/`|Snapshots miroir de la Phase 1 (`EXG-ORG-02`).|







# étape 5 : Bilan 

> **Spécification** : Conforme `EXG-PROJ-16` & `SPEC-01`
> 
> **Classification** : `TLP:AMBER`
> 
> **Statut** : Phase 1 Validée avec Succès

### 1. Synthèse des Livrables Produits

La Phase 1 a posé les fondations formelles du Knowledge Graph Cyber (DKG). Les fichiers suivants ont été générés dans `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox` et synchronisés dans `Snapshots_Phases/Phase_1_Socle` :

- **`DKG_TBox_Master.ttl` / `.json`** : Graphe ontologique OWL / RBox définissant la hiérarchie des concepts et des relations.
    
- **`shapes_abox.ttl`** : Graphe de contraintes de gouvernance SHACL.
    
- **`DKG_TBox_Master.md`** : Documentation exhaustive (glossaire, dictionnaire de classes/propriétés et diagramme Mermaid).
    
- **`synthetic_qualification.ttl`** : Dataset ABox minimal servant de socle pour la qualification.
    

### 2. Focus Didactique : Pourquoi combiner OWL (TBox) et SHACL (Shapes) ?

Une confusion fréquente en ingénierie des connaissances réside dans la séparation des rôles entre **OWL** et **SHACL** :



```
             ┌─────────────────────────────────────────┐
             │       Graphe RDF (ABox / Données)       │
             └────────────────────┬────────────────────┘
                                  │
    ┌─────────────────────────────┼─────────────────────────────┐
    ▼                             ▼                             ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│     OWL (Structure)   │ │    SKOS (Lexique)     │ │   SHACL (Validation)  │
├───────────────────────┤ ├───────────────────────┤ ├───────────────────────┤
│ • Modélisation logique│ │ • multilinguisme      │ │ • Hypothèse Monde     │
│ • Inférences (OWA)    │ │ • skos:prefLabel      │ │   Fermé (CWA)         │
│ • Relations & Axiomes │ │ • skos:altLabel (syn) │ │ • Contrôle de surface │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘
```



#### A. Le rôle d'OWL (Open World Assumption - OWA)

OWL sert à **donner du sens et de l'interopérabilité**.

- Si nous déclarons que `hasInstalledComponent` a pour inverse `isComponentOf`, le raisonneur OWL déduit automatiquement le lien inverse sans qu'il soit écrit explicitement dans la base.
    
- Sous OWA, l'absence d'une information ne signifie pas qu'elle est fausse ou interdite : OWL ne lève pas d'erreur de validation si une donnée manque, il considère simplement qu'elle n'est pas encore connue.
    

#### B. Le rôle de SHACL (Closed World Assumption - CWA)

SHACL sert à **imposer la qualité et la gouvernance**.

- Dans un SI Cybersécurité, nous avons besoin de règles de validation strictes (ex: _"Une vulnérabilité doit impérativement avoir un score CVSS valide"_).
    
- SHACL applique l'hypothèse du monde fermé (CWA) : il contrôle les instances (ABox) par rapport à des contraintes (Shapes) et rejette toute donnée hors-normes.
    

### 3. Illustration Pratique du SHACL

Voici comment s'articule la validation SHACL générée dans `shapes_abox.ttl` :

#### Définition de la Shape (`shapes_abox.ttl`)

Cette contrainte impose que toute instance de la classe `dkg:Vulnerability` possède un score CVSS de type `xsd:float` ne dépassant pas `10.0`.

Extrait de code

```
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix sh:  <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dkg:VulnerabilityShape
    a sh:NodeShape ;
    sh:targetClass dkg:Vulnerability ;
    sh:property [
        sh:path dkg:cvssScore ;
        sh:datatype xsd:float ;
        sh:maxInclusive 10.0 ;
        sh:minInclusive 0.0 ;
        sh:message "Le score CVSS doit être un flottant compris entre 0.0 et 10.0." ;
    ] .
```

#### Cas Pratique de Validation

|**Instance ABox (Donnée)**|**Conforme ?**|**Résultat du contrôle SHACL**|
|---|---|---|
|`:CVE-2023-0001 a dkg:Vulnerability ; dkg:cvssScore 7.5 .`|**Oui**|`Validation Report: Conforms = True`|
|`:CVE-2023-0002 a dkg:Vulnerability ; dkg:cvssScore 11.2 .`|**Non**|**Violation SHACL** : dépasse `sh:maxInclusive 10.0`.|
|`:CVE-2023-0003 a dkg:Vulnerability ; dkg:cvssScore "Critical" .`|**Non**|**Violation SHACL** : type invalide (`xsd:string` au lieu de `xsd:float`).|

### 4. Bilan Qualité & Métriques (`EXG-PROJ-16`)

| **Exigence**    | **Intitulé**             | **Statut** | **Résultat du Contrôle**                                                        |
| --------------- | ------------------------ | ---------- | ------------------------------------------------------------------------------- |
| **EXG-TBOX-01** | Délimiteur URI (`#`)     | **Validé** | All URIs match `[http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)` |
| **EXG-TBOX-02** | Typage OWL               | **Validé** | 6 `owl:Class`, 6 `owl:ObjectProperty`, 6 `owl:DatatypeProperty`                 |
| **EXG-TBOX-03** | Domaine & Portée         | **Validé** | 100% des propriétés disposent de `rdfs:domain` et `rdfs:range`                  |
| **EXG-TBOX-04** | Axiomes RBox             | **Validé** | Relations inverses `owl:inverseOf` opérationnelles                              |
| **EXG-QUAL-01** | Couverture SHACL         | **Validé** | Shapes définies pour la validation ABox des entités majeures                    |
| **EXG-ORG-02**  | Parité Master / Snapshot | **Validé** | Empreinte binaire identique entre Master et Snapshot Phase 1                    |





