
# 📘 Document de Phase : Phase 1 — Socle Modèle Canonique & Qualité (TBox / RBox / SHACL)

> **Fichier** : `00-Projet/Phase1/Phase_Content.md`  
> **Classification TLP** : `TLP:AMBER`  
> **Phase** : Phase 1 — Initialisation Socle Modèle Canonique & Qualité  
> **Étape Actuelle** : Étape 1 : Cadrage (`EXG-PROJ-12`)  
> **Répertoire Code** : `13-Application/Phase_1_Socle/`  
> **Répertoires Données Cibles** :
> * Master Transversal : `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/`
> * Snapshot Phase 1 : `02-Donnees/Snapshots_Phases/Phase_1_Socle/`

---

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


# 📘 Document de Phase : Phase 1 — Socle Modèle Canonique & Qualité

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





---

## 1. Objectif de la Phase

La Phase 1 établit la fondation sémantique du DKG. Elle définit le **modèle de sens (TBox OWL)**, la **logique des relations inverses et transitives (RBox OWL)** et le **contrat de validation impératif sous monde fermé (SHACL)**.

---

## 2.  Spécifications & Exigences Applicables (Matrice de Traçabilité)

La Phase 1 doit satisfaire l'ensemble des spécifications et exigences du projet répertoriées ci-dessous :

### 2.1.   Spécifications Fonctionnelles & Techniques
* **`SPEC-01_Norme_TBox_RBox.md`** : Définit la structure ontologique, les acronymes obligatoires, le triptyque de publication et la génération du diagramme Mermaid.
* **`SPEC-04_Validation_SHACL.md`** : Spécifie les contraintes de qualité (IP Regex, bornes CVSS, cardinalités) sous l'hypothèse CWA.

### 2.2.    Exigences Transverses (`ExigencesProjet.md`)
* **`EXG-PROJ-01`** : Séparation stricte TBox/RBox (Schéma) vs ABox (Instances).
* **`EXG-PROJ-02`** : Triple-format d'export obligatoire (`.ttl`, `.json`, `.md`).
* **`EXG-PROJ-03`** : Recette et qualification automatisées par `pytest`.
* **`EXG-SEM-01`** : Livraisons indissociables TBox + RBox + SHACL (`TLP:AMBER`).
* **`EXG-QUAL-01`** : Couplage TBox ↔ SHACL Auto-adaptatif.
* **`EXG-QUAL-04`** : Blocage du pipeline en cas de violation SHACL.
* **`EXG-PROJ-07`** : Exécution locale optimisée pour machine ACER 16 Go RAM.

---
## 3.    Données et Génération des Données Synthétiques
### 3.1.   Données d'entrée existantes

### 3.2.   Nouvelles données d'entrée ( Externes , synthetisées avec le Use_Case,..)

Pour éviter le code dur (*hardcoding*) et garantir la robustesse des tests de qualification :
* Un **générateur synthétique paramétrable** basé sur le Cas d'Usage (ex: *Serveur Web vulnérable à Log4j / CVE-2021-44228*) produira un jeu de test léger.
* Ce jeu de test permettra de valider le comportement du moteur SHACL en cas de conformité **et** en cas de non-conformité (injection d'anomalies de test : IP invalide, CVSS out-of-range).

### 3.3.   Nouvelles données générées  ( pour les .md mettre le lien)
L'exécution du script de Phase 1 doit impérativement alimenter le dossier Snapshot de la phase **ainsi que** le Master Transversal :

| Identifiant Livrable | Description                           | Format            | Emplacement Snapshot                                                     | Emplacement Master                                                        |
| :------------------- | :------------------------------------ | :---------------- | :----------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| **LIV-P1-01**        | Ontologie Canonique TBox / RBox       | Turtle (`.ttl`)   | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/DKG_TBox_Master.ttl`     | `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.ttl`  |
| **LIV-P1-02**        | Sérialisation JSON-LD + Context       | JSON-LD (`.json`) | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/DKG_TBox_Master.json`    | `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.json` |
| **LIV-P1-03**        | Doc Humaine + Glossaire + Mermaid     | Markdown (`.md`)  | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/DKG_TBox_Master.md`      | `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.md`   |
| **LIV-P1-04**        | Règles de Validation SHACL            | Turtle (`.ttl`)   | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/shapes_abox.ttl`         | `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/shapes_abox.ttl`      |
| **LIV-P1-05**        | Données Synthétiques de Qualification | Turtle (`.ttl`)   | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/synthetic_test_data.ttl` | *Non publié en Master* (Interne Tests)                                    |




---

## 4. Script 
### 4.1.   scripts operations

### 4.2.   Protocole de Qualification & Validation

Avant toute promotion vers la Phase 2, la suite `pytest` (`13-Application/Phase_1_Socle/test_phase1_quality.py`) doit exécuter :
1. **`test_tbox_completeness`** : Vérifie la présence des 6 classes minimales et leurs propriétés.
2. **`test_shacl_coverage`** : Vérifie le couplage `owl:Class` ↔ `sh:NodeShape` (`EXG-QUAL-01`).
3. **`test_spec01_markdown_structure`** : Vérifie la présence de la table des acronymes et du bloc Mermaid dans le fichier `.md`.
4. **`test_shacl_validation_engine`** : Valide le jeu de données synthétiques conformes et confirme le rejet du jeu altéré (`EXG-QUAL-04`).




---





## 5.   Criteres de Recette & Qualification (Pytest)

* `test_tbox_completeness()` : Vérifie que chaque classe possède ses propriétés associées.
* `test_shacl_coverage()` (`EXG-QUAL-01`) : S'assure que chaque classe critique possède un `sh:NodeShape` correspondant dans `shapes_abox.ttl`.
* `test_synthetic_validation()` : Valide le jeu de test synthétique conforme et confirme le rejet du jeu de test altéré.


# 6.   Memo didactique

### 6.1 . Explicitation de la Génération de `TBox_Cybersec.ttl`

Pour clarifier le processus de création et de mise à jour de `TBox_Cybersec.ttl` auprès de tous les intervenants (humains et agents IA), le flux de génération s'établit comme suit :

1. **Origine Métier / Modélisation** : Édition des concepts formels dans `TBox_Cybersec.ttl` via des éditeurs d'ontologies (Protégé, TopBraid) ou écriture manuelle en syntaxe Turtle W3C.
    
2. **Enrichissement Lexical (SKOS)** : Ajout systématique des annotations `rdfs:label` (français/anglais) et `skos:altLabel` (synonymes métier et acronymes) directement sur chaque nœud du fichier Turtle.
    
3. **Pipeline de Compilation** : Exécution du script `13-Application/generate_TBox_initiale.py` qui lit la source Turtle et compile automatiquement les fichiers `TBox_Cybersec.json` et `TBox_Cybersec.md`.
    
4. **Contrôle Qualité Automatique** : Exécution de `pytest 13-Application/test_tbox_spec.py` pour valider qu'aucune modification de la TBox n'a enfreint le contrat de spécification.
### 6.2.  Pour aller plus loin