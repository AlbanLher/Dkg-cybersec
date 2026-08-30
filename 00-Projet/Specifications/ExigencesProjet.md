# 📑 Exigences Transverses et Normes de Qualité DKG

> **Statut** : Approuvé  
> **Application** : Transverse à l'ensemble du projet (Modules 00 à 13)  
> **Méthodologie** : Spec-Driven Development (SDD)

---

## 🏛️ 1. Exigences d'Architecture Sémantique & Traçabilité (EXG-PROJ)

* **`EXG-PROJ-01` (Architecture TBox/ABox)** : Séparation stricte entre le schéma conceptuel (`TBox`/`RBox` + `SHACL` sous `TLP:AMBER`) et les données instanciées (`ABox` sous `TLP:RED`).
* **`EXG-PROJ-02` (Conformité des Artefacts)** : Tout livrable de modélisation Master doit être accompagné de sa source Turtle (`.ttl`), de sa sérialisation machine (`.json`) et de sa documentation humaine (`.md`).
* **`EXG-PROJ-03` (Validation Automatisée)** : Aucun changement d'ontologie, de règle ou de script d'ingestion ne doit être commité sans validation préalable par la suite de tests `pytest` (incluant le passage SHACL).
* **`EXG-PROJ-04` (Gestion de la Traçabilité & Provenance)** : Les données SI (`graph:private` / `TLP:RED`) et les flux OSINT publics (`graph:public` / `TLP:CLEAR`) doivent être isolés dans des sous-graphes étanches.
* **`EXG-PROJ-05` (Données Publiques & Communs)** : Relever et intégrer les standards ouverts de la cybersécurité (NVD CVE, MITRE CWE, MITRE CAPEC) pour enrichir la connaissance sans réinventer l'existant.
* **`EXG-PROJ-06` (Confidentialité & Modalités POC)** : 
  * *Cadre POC* : Les données SI internes sont modélisées sous l'étiquette pseudo-confidentielle `TLP:RED` pour l'exercice didactique.
  * *Ajustement Production* : La documentation architecture (`01_Principes...`) doit expliciter les leviers d'activation pour la production (Anonymisation, Chiffrement au repos, Neo4j RBAC / Row-Level Security).
* **`EXG-PROJ-07` (Contrainte Ressources IT - Client Léger)** : 
  * L'agent et l'ensemble du stack (Python + Graph Database Neo4j) doivent fonctionner en local sur une machine **ACER Aspire 515-40 (16 Go RAM)**.
  * *Consigne mémoire* : Le conteneur Neo4j/DBMS ne doit pas dépasser 4 à 6 Go de Heap/Pagecache RAM.
  * *Délégation Cloud* : Les tâches lourdes d'IA (Fine-tuning de LLM, embeddings massifs) sont déportées vers des ressources cloud/externe si nécessaire.

---
## 🛡️ 2. Exigences Projet-Phases-Etapes (EXG-PROJ)

* **`EXG-PROJ-11` (Etapes)** : Toutes activité doit identifier la phase ainsi que l'étape de la Phase. Les étapes sont : ( Cadrage, Specification, Donnees_source, Script-Test, Bilan )
  **`EXG-PROJ-12` (Livrables Etapes Cadrage)** : A intégrer dans le fichier PhaseContent:  Analyse du backlog listé dans ./00-Projet/PhaseProjet.md et liste des concept et fonctions selectionnées pour la phase avec analyse de cohérence sur le plan de développement.  Structure des spécifications attendues, première vue des livrables data et script du pipeline.  Mise a jour du fichier ./00-Projet/PhaseProjet.md indiquant les principes et fonctions associés à la phase ainsi que ceux laissé dans le backlog
* **`EXG-PROJ-13` (Livrables Etapes Specification)** : A intégrer dans le fichier PhaseContent:  Lien vers les SPEC-XX dans ./01-Principes_Specifications/. Liste des Données complémentaires a synthetiser si besoin.  Mise a jour de la vue livrables data et script du pipeline.
* **`EXG-PROJ-14` (Livrables Etapes Données_sources)** : A intégrer dans le fichier PhaseContent:  identification des fichiers Donnees dans ./02-Donnees/ et proposition de mise a jour du ./Projet/Use_Case.md.  Mise a jour de la vue livrables script du pipeline. 
* **`EXG-PROJ-15` (Livrables Etapes Script-Test)** : A intégrer dans le fichier PhaseContent:  identification des fichiers Donnees et proposition de mise a jour du ./Projet/Use_Case.md.  Mise a jour de la vue livrables script du pipeline.  Scrips dans le repertoire ./03-Application/
* **`EXG-PROJ-16` (Livrables Etapes Bilan)** : une revue du PhaseContent en vérifiant la cohérence technique et projet, en ajoutant un bilan pédagogique.
  Une revue du  fichier ./00-Projet/PhaseProjet.md  pour enrichir le Backlog de point identifié mais non traité dans la phase.



## 🛡️ 3. Exigences Qualité & CI/CD (EXG-QUAL)

* **`EXG-QUAL-01` (Couplage TBox ↔ SHACL Auto-Adaptatif)** : Tout ajout de classe ou propriété dans la TBox doit être couplé à sa règle de validation SHACL (`sh:NodeShape` / `sh:PropertyShape`).
* **`EXG-QUAL-02` (Pipeline Orchestrateur Unifié)** : L'ensemble du cycle de vie (Phase 1 à Phase 3b) doit pouvoir être exécuté d'une seule commande via `13-Application/run_pipeline.py`.
* **`EXG-QUAL-03` (Neo4j / n10s Readiness)** : Les exports Master ABox (`.ttl`, `.json`) doivent comporter des URIs et préfixes nettoyés pour l'ingestion par `neosemantics`.
* **`EXG-QUAL-04` (Blocage sur Violation SHACL)** : Toute non-conformité SHACL lors de l'instanciation (Phase 2) ou de l'enrichissement (Phase 3) stoppe le pipeline (`exit(1)`) et produit un rapport `shacl_violation_report.md`.