_Initialisation & Peuplement de l'ABox (Graphe d'Instances)_
# Phase 2 : Ingestion ABox & Génération Synthétique Cyber

> **Statut** : 🟡 En cours (Refactoring Pydantic V2 & Alignement SSOT)
> **Classification** : `TLP:RED`
> **Date de début** : 31/08/2026

---

## 🎯 1. Objectifs & Périmètre
* **But principal** : Instancier le graphe de connaissances ABox avec des données factuelles représentant le SI d'une organisation, ses composants logiciels, ses vulnérabilités connues (CVE), faiblesses (CWE) et modes opératoires (CAPEC).
* **Livrables attendus** :
  1. Spécification : `docs/specs/03_USECASE_TECHNIQUE/SPEC-TECH-UC01_Instanciation_ABox_Cyber.md`
  2. Dataset synthétique d'instance : `DKG_ABox_Master.ttl`
  3. Script de génération et d'ingestion : `03-Application/generate_phase2_abox.py`
  4. Suite de tests Pytest et validation SHACL : `tests/test_phase2_abox.py`

---

## 🛠️ 2. Traçabilité des Livrables par Brique

### A. Spécification & Gouvernance (SPEC Framework)
* **Spécification associée** : `SPEC-TECH-UC01_Instanciation_ABox_Cyber.md`
* **Exigences couvertes** : `EXG-CT-01` à `EXG-CT-03`, `EXG-QU-02`, `EXG-QU-03`, `EXG-SE-01`, `EXG-OR-07`.

### B. Instanciation & Use Case Pédagogique
* **Document de référence** : `00-Projet/Phase2_ABox/Memo_Use-Case_Phase2.md`

### C. Données & Ontologies (Data / Graph RDF)
* **Artefacts Master** : `02-Donnees/Master_Transversal/TLP_RED_Instances_ABox/DKG_ABox_Master.ttl`
* **Artefacts Snapshot** : `02-Donnees/Snapshots_Phases/Phase2_ABox/DKG_ABox_Master.ttl`

### D. Scripts & Outillage (Automation & CI/CD)
* **Générateur / Ingesteur** : `03-Application/generate_phase2_abox.py`
* **Tests Qualité** : `tests/test_phase2_abox.py`