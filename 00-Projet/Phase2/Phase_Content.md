_Initialisation & Peuplement de l'ABox (Graphe d'Instances)_

# Phase 2 : Ingestion ABox & Génération Synthétique

> **Statut** : 🟡 En cours (Cadrage)  
> **Date de début** : 31/08/2026  
> **Date de clôture visée** : À définir  

---

## 🎯 1. Objectifs & Périmètre
* **But principal** : Instancier le graphe de connaissances avec des données factuelles (ABox) représentant le SI d'une organisation, ses composants logiciels, ses vulnérabilités connues (CVE) et ses faiblesses (CWE).
* **Livrables attendus** : 
  1. Spécification `SPEC-02-ABox.md` (règles de nommage des instances, URIs, typage).
  2. Dataset synthétique d'instance `DKG_ABox_Master.ttl`.
  3. Script de génération et d'ingestion `generate_phase2_abox.py`.
  4. Suite de tests Pytest et validation SHACL automatique (`test_phase2_quality.py`).

---

## 🛠️ 2. Traçabilité des Livrables par Brique

### A. Spécification & Gouvernance (SPEC Framework)
* **Spécification associée** : [`SPEC-02-ABox.md`](../../01-Exigences/SPEC-02-ABox.md) *(En rédaction)*
* **Exigences couvertes** : `EXG-QUAL-01` à `EXG-QUAL-03` (Shapes SHACL), `EXG-SEC-01` (TLP Marking).

### B. Instanciation & Use Case Pédagogique (Lisible Humain)
* **Document d'illustration** : [`Human_UseCase_ABox.md`](./Human_UseCase_ABox.md)
* **Description** : Scénario décrivant un incident d'infrastructure (Serveur Web Web-Prod-01 impacté par Log4Shell / CVE-2021-44228).

### C. Données & Ontologies (Data / Graph RDF)
* **Artefacts Master** : `02-Donnees/Master_Transversal/TLP_AMBER_ABox_Master/`
* **Artefacts Snapshot** : `02-Donnees/Snapshots_Phases/Phase_2_ABox/`

### D. Scripts & Outillage (Automation & CI/CD)
* **Générateur** : `03-Application/generate_phase2_abox.py`
* **Tests Qualité** : `03-Application/test_phase2_quality.py`

---

## 🏁 3. Synthèse de Clôture & Ressources

*(Cette section sera complétée à la clôture de la Phase 2)*