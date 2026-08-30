
# 📘 Spécification de la Phase 1 : Socle Canonique & Contrat de Qualité (TBox / RBox / SHACL)

# 📘 Cadrage & Spécification de la Phase 1 : Socle Canonique & Contrat de Qualité (TBox / RBox / SHACL)

> **Classification** : `TLP:AMBER`  
> **Répertoire Snapshot** : `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/`  
> **Répertoire Master** : `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/`  
> **Statut** : Cadrage Méthodologique Validé

---

## 🎯 1. Objectif de la Phase

La Phase 1 établit la fondation sémantique du DKG. Elle définit le **modèle de sens (TBox OWL)**, la **logique des relations inverses et transitives (RBox OWL)** et le **contrat de validation impératif sous monde fermé (SHACL)**.

---

## 📋 2. Spécifications & Exigences Applicables (Matrice de Traçabilité)

La Phase 1 doit satisfaire l'ensemble des spécifications et exigences du projet répertoriées ci-dessous :

### A. Spécifications Fonctionnelles & Techniques
* **`SPEC-01_Norme_TBox_RBox.md`** : Définit la structure ontologique, les acronymes obligatoires, le triptyque de publication et la génération du diagramme Mermaid.
* **`SPEC-04_Validation_SHACL.md`** : Spécifie les contraintes de qualité (IP Regex, bornes CVSS, cardinalités) sous l'hypothèse CWA.

### B. Exigences Transverses (`ExigencesProjet.md`)
* **`EXG-PROJ-01`** : Séparation stricte TBox/RBox (Schéma) vs ABox (Instances).
* **`EXG-PROJ-02`** : Triple-format d'export obligatoire (`.ttl`, `.json`, `.md`).
* **`EXG-PROJ-03`** : Recette et qualification automatisées par `pytest`.
* **`EXG-SEM-01`** : Livraisons indissociables TBox + RBox + SHACL (`TLP:AMBER`).
* **`EXG-QUAL-01`** : Couplage TBox ↔ SHACL Auto-adaptatif.
* **`EXG-QUAL-04`** : Blocage du pipeline en cas de violation SHACL.
* **`EXG-PROJ-07`** : Exécution locale optimisée pour machine ACER 16 Go RAM.

---

## 📦 3. Tableau des Livrables de la Phase 1

L'exécution du script de Phase 1 doit impérativement alimenter le dossier Snapshot de la phase **ainsi que** le Master Transversal :

| Identifiant Livrable | Description                           | Format            | Emplacement Snapshot                                                     | Emplacement Master                                                        |
| :------------------- | :------------------------------------ | :---------------- | :----------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| **LIV-P1-01**        | Ontologie Canonique TBox / RBox       | Turtle (`.ttl`)   | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/DKG_TBox_Master.ttl`     | `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.ttl`  |
| **LIV-P1-02**        | Sérialisation JSON-LD + Context       | JSON-LD (`.json`) | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/DKG_TBox_Master.json`    | `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.json` |
| **LIV-P1-03**        | Doc Humaine + Glossaire + Mermaid     | Markdown (`.md`)  | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/DKG_TBox_Master.md`      | `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_TBox_Master.md`   |
| **LIV-P1-04**        | Règles de Validation SHACL            | Turtle (`.ttl`)   | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/shapes_abox.ttl`         | `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/shapes_abox.ttl`      |
| **LIV-P1-05**        | Données Synthétiques de Qualification | Turtle (`.ttl`)   | `02-Donnees/Snapshots_Phases/Phase_1_TBox_Socle/synthetic_test_data.ttl` | *Non publié en Master* (Interne Tests)                                    |

---

## 🧪 4. Protocole de Qualification & Validation

Avant toute promotion vers la Phase 2, la suite `pytest` (`13-Application/Phase_1_Socle/test_phase1_quality.py`) doit exécuter :
1. **`test_tbox_completeness`** : Vérifie la présence des 6 classes minimales et leurs propriétés.
2. **`test_shacl_coverage`** : Vérifie le couplage `owl:Class` ↔ `sh:NodeShape` (`EXG-QUAL-01`).
3. **`test_spec01_markdown_structure`** : Vérifie la présence de la table des acronymes et du bloc Mermaid dans le fichier `.md`.
4. **`test_shacl_validation_engine`** : Valide le jeu de données synthétiques conformes et confirme le rejet du jeu altéré (`EXG-QUAL-04`).



ètre du Triptyque Modèle (TLP:AMBER)

1. **TBox (OWL - Modèle de Sens)** :
   * Typage des concepts clés : `Asset`, `SoftwareComponent`, `Vulnerability`, `Weakness`, `ThreatPattern`, `TLPMarking`.
   * Propriétés de données (`hostname`, `ipAddress`, `cvssScore`, `severityLabel`, etc.).

2. **RBox (OWL - Logique des Relations)** :
   * Définition des propriétés d'objets : `hasInstalledComponent`, `hasVulnerability`, `hasWeakness`, `hasThreatPattern`, `hasTLPMarking`.
   * Modélisation des relations inverses (ex: `isComponentOf` ↔ `hasInstalledComponent`).

3. **SHACL (Shapes - Contraintes de Validation CWA)** :
   * Validation impérative des instances ABox.
   * Formatage par expressions régulières (Regex pour IP et identifiants CVE).
   * Cardinalités (`minCount 1` pour l'IP d'un Asset) et bornes numériques ($0.0 \le \text{CVSS} \le 10.0$).

---

## ⚙️ 3. Stratégie de Génération des Données Synthétiques

Pour éviter le code dur (*hardcoding*) et garantir la robustesse des tests de qualification :
* Un **générateur synthétique paramétrable** basé sur le Cas d'Usage (ex: *Serveur Web vulnérable à Log4j / CVE-2021-44228*) produira un jeu de test léger.
* Ce jeu de test permettra de valider le comportement du moteur SHACL en cas de conformité **et** en cas de non-conformité (injection d'anomalies de test : IP invalide, CVSS out-of-range).

---

## 📦 4. Livrables de la Phase 1

L'exécution du script `13-Application/Phase_1_Socle/generate_phase1_socle.py` doit produire dans `12-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/` :

| Fichier | Format | Rôle |
| :--- | :--- | :--- |
| `DKG_TBox_Master.ttl` | Turtle (`.ttl`) | Ontologie TBox + RBox canonique |
| `DKG_TBox_Master.json` | JSON-LD (`.json`) | Sérialisation machine structurée (Context n10s) |
| `DKG_TBox_Master.md` | Markdown (`.md`) | Dictionnaire de données lisible par l'humain |
| `shapes_abox.ttl` | Turtle (`.ttl`) | Spécification des contraintes de validation SHACL |

---

## 🧪 5. Criteres de Recette & Qualification (Pytest)

* `test_tbox_completeness()` : Vérifie que chaque classe possède ses propriétés associées.
* `test_shacl_coverage()` (`EXG-QUAL-01`) : S'assure que chaque classe critique possède un `sh:NodeShape` correspondant dans `shapes_abox.ttl`.
* `test_synthetic_validation()` : Valide le jeu de test synthétique conforme et confirme le rejet du jeu de test altéré.










initialiser le projet en construisant une première socle structurel TBox-RBox  multiformat minimale correspondant aux cas d'usage 
Le livrable générique correspond aux spécifications : [SPEC-01](../../11-Principes_Architecture/Specifications/SPEC-01_Norme_TBox_RBox.md)
Une bonne partie des données sont en dur dans le premier script.
Les phase suivantes viseront a mettre en place les outils d'évolution

Ce premier socle est disponible en " format dont 1 en markdown (.md) pour que les parties prenantes en garde le controle [TBox_Human](../../12-Donnees/TBox_init/TBox_Cybersec.md)

Cette phase a été reprise suite au [REX-01](REX-01_rigueur_attendue_RDF-OWL.md)   


# Bilan des Actions et Livrables

| Action                                    | livrable                                | Localisation       | Commentaire                   |                       |
| ----------------------------------------- | --------------------------------------- | ------------------ | ----------------------------- | --------------------- |
| Mise en place de la specification du TBox | SPEC-01_Norme_TBox_RBox                 | 11-/Specification/ | sert aux tests                | 🟢 Terminée / Validée |
| Mise a disposition de données sources     | cve_data.ttl                            | 12-/1-/2-          | une seule cve sur le use case | 🟢 Terminée / Validée |
| Script de génération d'un premier ttl     | build_inital_ttl_TBox.py                | 13-/               |                               | 🟢 Terminée / Validée |
| Premier ttl généré par cript précédent    | TBox_Cybersec.ttl                       | 12-/TBox_init      |                               | 🟢 Terminée / Validée |
| Scrip de génération md et json            | generate_TBox_initiale.py               | 13-/               |                               | 🟢 Terminée / Validée |
| generation TBox tout format               | `TBox_Cybersec.jon`, `TBox_Cybersec.md` | 12-/TBox_init      |                               | 🟢 Terminée / Validée |
| test des fichiers TBox % specifications   | `test_phase1_tbox_rbox_spec.py`         | 13-/               |                               | 🟢 Terminée / Validée |
|                                           |                                         |                    |                               |                       |

- 
# Memo didactique

### 5. Explicitation de la Génération de `TBox_Cybersec.ttl`

Pour clarifier le processus de création et de mise à jour de `TBox_Cybersec.ttl` auprès de tous les intervenants (humains et agents IA), le flux de génération s'établit comme suit :

1. **Origine Métier / Modélisation** : Édition des concepts formels dans `TBox_Cybersec.ttl` via des éditeurs d'ontologies (Protégé, TopBraid) ou écriture manuelle en syntaxe Turtle W3C.
    
2. **Enrichissement Lexical (SKOS)** : Ajout systématique des annotations `rdfs:label` (français/anglais) et `skos:altLabel` (synonymes métier et acronymes) directement sur chaque nœud du fichier Turtle.
    
3. **Pipeline de Compilation** : Exécution du script `13-Application/generate_TBox_initiale.py` qui lit la source Turtle et compile automatiquement les fichiers `TBox_Cybersec.json` et `TBox_Cybersec.md`.
    
4. **Contrôle Qualité Automatique** : Exécution de `pytest 13-Application/test_tbox_spec.py` pour valider qu'aucune modification de la TBox n'a enfreint le contrat de spécification.