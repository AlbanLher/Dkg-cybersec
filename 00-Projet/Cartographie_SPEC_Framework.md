# 🗺️ Cartographie & Matrice des Spécifications (SPEC Framework)

> **Classification** : `TLP:AMBER`  
> **Méthodologie** : *Spec-Driven Development* (SDD) — `EXG-ORG-01`  
> **Règle de Gouvernance** : Tout ajout de nouvelle spécification (`SPEC-XX`) implique la mise à jour immédiate de ce document.

---

## 📌 1. Vue d'Ensemble & Arbre de Dépendances

```text
                        ┌──────────────────────────────────────────┐
                        │ SPEC-00_Exigences_Projet.md (Cadre Mère) │
                        └────────────────────┬─────────────────────┘
                                             │
            ┌────────────────────────────────┴────────────────────────────────┐
            ▼                                                                 ▼
┌───────────────────────────────┐                                 ┌───────────────────────────────┐
│ SPEC-01-TBox.md               │                                 │ SPEC-02-ABox.md               │
│ (Structure OWL & SKOS)        │                                 │ (Données, URIs & SHACL)       │
└───────────┬───────────────────┘                                 └───────────┬───────────────────┘
            │                                                                 │
            └────────────────────────────────┬────────────────────────────────┘
                                             │
                                             ▼
                                ┌─────────────────────────┐
                                │ SPEC-03-Neo4j_RAG.md    │ (Planifiée - Phase 3)
                                │ (Graph RAG & Agent SOC) │
                                └─────────────────────────┘
                                
```

## 🔗 2. Matrice Répertoire des Spécifications

|**Code SPEC**|**Titre de la Spécification**|**Type / Nature**|**Statut**|**Spécification Mère / Dépendances**|**Liens Directs**|
|---|---|---|---|---|---|
|**`SPEC-00`**|**Exigences Cadre & Gouvernance**|👑 _Cadre Mère_|🟢 Approuvé|_Aucune (Spécification Racine)_|[`SPEC-00_Exigences_Projet.md`](https://www.google.com/search?q=./SPEC-00_Exigences_Projet.md)|
|**`SPEC-01`**|**Socle Ontologique (TBox/SKOS)**|🧬 _Autonome / Transversal_|🟢 Approuvé|[`SPEC-00`](https://www.google.com/search?q=./SPEC-00_Exigences_Projet.md)|[`SPEC-01-TBox.md`](https://www.google.com/search?q=../01-Exigences/SPEC-01.md)|
|**`SPEC-02`**|**Données Factuelles (ABox & SHACL)**|📦 _Dépendante_|🟢 Approuvé|[`SPEC-00`](https://www.google.com/search?q=./SPEC-00_Exigences_Projet.md), [`SPEC-01`](https://www.google.com/search?q=../01-Exigences/SPEC-01.md)|[`SPEC-02-ABox.md`](https://www.google.com/search?q=../01-Exigences/SPEC-02-ABox.md)|
|**`SPEC-03`**|**Ingestion Neo4j, Vectorization & RAG**|🚀 _Applicative_|⚪ Planifié|[`SPEC-01`](https://www.google.com/search?q=../01-Exigences/SPEC-01.md), [`SPEC-02`](https://www.google.com/search?q=../01-Exigences/SPEC-02-ABox.md)|_(Fichier à créer en Phase 3)_|

## 💡 3. Typologie des Spécifications

### 🟢 A. Spécifications Génériques & Framework (Réutilisables)

Ces spécifications définissent la méthodologie globale et le canevas de gouvernance. Elles sont transposables à n'importe quel domaine d'application (Finance, Santé, Aéronautique) :

- [`SPEC-00_Exigences_Projet.md`](https://www.google.com/search?q=./SPEC-00_Exigences_Projet.md) — Matrice des exigences organisationnelles et de qualité.
    
- [`SPEC_Template.md`](https://www.google.com/search?q=./SPEC_Template.md) — Canevas normé pour l'écriture de nouvelles spécifications.

### 🔵 B. Spécifications Métier DKG-CyberSec (Spécifiques SOC)

Ces spécifications traduisent la connaissance sémantique du domaine Cyber :

- [`SPEC-01-TBox.md`](https://www.google.com/search?q=../01-Exigences/SPEC-01.md) — Ontologie TBox/SKOS (Classes `Asset`, `Vulnerability`, `Weakness`, `ThreatPattern`).
    
- [`SPEC-02-ABox.md`](https://www.google.com/search?q=../01-Exigences/SPEC-02-ABox.md) — Instanciation ABox, conventions d'URIs (`dkg-data:`) et règles SHACL.





# 🗺️ Cartographie & Matrice des Spécifications (Framework & UseCase) 

> **Classification** : `TLP:AMBER` > 
> **Méthodologie** : *Spec-Driven Development* (SDD) — `EXG-ORG-01` 
> **Concept Clé** : DKG = **Dynamic Knowledge Graph** --- 
> 
## 🏗️ 1. Spécifications Framework (`01-Principes_Specifications/Specifications_Framework/`) 

Spécifications **abstraites, génériques et réutilisables**, indépendantes de tout jeu de données d'instances. 

| Code SPEC | Titre | Contenu / Portée | Statut | Fichier |
| :--- | :--- | :--- | :---: | :--- | 
| **`SPEC-00`** | **Exigences Cadre & Gouvernance** | Règles projet, SDD, CI/CD, Gatekeeper | 🟢 Approuvé | [`SPEC-00_Exigences_Projet.md`](05-Bin/SPEC-00_Exigences_Projet.md) |
| **`SPEC-01`** | **Socle Structurel (TBox/RBox/SHACL)** | Métaclasses OWL, RBox inverses, Shapes SHACL | 🟢 Approuvé | [`SPEC-01_TBox_RBox_SHACL.md`](../01-Principes_Specifications/Specifications_Framework/SPEC-01_TBox_RBox_SHACL.md) | 
| **`SPEC-TPL`** | **Gabarit Standard** | Template normé en 6 sections | 🟢 Approuvé | [`SPEC_Template.md`](05-Bin/SPEC_Template.md) | 


--- 
## 🎯 2. Spécifications UseCase Cyber (`01-Principes_Specifications/Specifications_UseCase/`) 

Spécifications **d'application concrète au UseCase Cybersécurité** (règles de nommage des données factuelles ABox, requêtes et ingestion). 

| Code SPEC | Titre | Périmètre Données / UseCase | Dépend de | Statut | Fichier |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`SPEC-UC-01`** | **ABox & Instanciation SI Cyber** | Nommage URIs (`dkg-data:`), instances CVE/CWE, validation CWA | `SPEC-00`, `SPEC-01` | 🟢 Approuvé | [`SPEC-UC-01_ABox_Instances.md`](../01-Principes_Specifications/Specifications_UseCase/SPEC-UC-01_ABox_Instances.md) | 
| **`SPEC-UC-02`** | **Ingestion Neo4j & Graph RAG** | Modèle Cypher, indexation vectorielle, requêtes RAG hybrides | `SPEC-01`, `SPEC-UC-01` | ⚪ Planifié | *(Phase 3)* |