---
type: spec
reference: SPC-TEC-P8-soc_orchestrator_agent_01
revision: 2
titre: "Composants Techniques MCP-Ready : Orchestrateur, Filtrage Frugal & Gateway HitM"
titre_court: soc_orchestrator_agent_mcp
description: Spécification technique actualisée des scripts de la Phase 8 conçus comme des outils natifs MCP (Model Context Protocol).
phase_code: P8
phase_nom: Orchestration MCP & Moteurs d'Agents Souverains
statut: 🟡 ACTIVE
portee: USECASE_TECHNIQUE
public_vise:
  - Développeurs DevSecOps
  - Analystes CTI / SOC, Lead Tech
exigences:
  - id: EXG-TEC-P8-soc_1
    code_exigence: EXG-P8-05
    domaine: TEC
    domaine_nom: Technique & Core Framework
    core: true
    phase: P8
    titre: API Asynchrone
    critere: Pilotage asynchrone avec timeout de 30s.
    test: PyTest / AsyncIO Suite
  - id: EXG-TEC-P8-soc_2
    code_exigence: EXG-P8-06
    domaine: TEC
    domaine_nom: Technique & Core Framework
    core: true
    phase: P8
    titre: Pipeline NER Local
    critere: Exécution 100% Air-Gapped du modèle GLiNER.
    test: PyTest / Air-Gapped Check
  - id: EXG-TEC-P8-soc_3
    code_exigence: EXG-P8-07
    domaine: TEC
    domaine_nom: Technique & Core Framework
    core: true
    phase: P8
    titre: Architecture MCP-Ready
    critere: Typage strict et découplage pour wrapper MCP.
    test: PyTest / Interface Check
---

# 📜 Composants Techniques MCP-Ready : Orchestrateur, Filtrage Frugal & Gateway HitM

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif
Spécifier l'implémentation logicielle de la Phase 8 en adoptant une approche **MCP-Ready**. Les fonctions métier sont isolées et typées afin d'être exposées directement comme des outils (`tools`) et des ressources (`resources`) aux agents LLM dans la future Vague 5.

### 1.2 Glossaire Métier & Technique
| Acronyme / Concept | Définition | Contexte DKG |
| :--- | :--- | :--- |
| **MCP** | Model Context Protocol | Protocole standardisé d'exposition d'outils et de données aux LLMs. |
| **Tool** | Fonction exécutable par un agent | Encapsulation d'un script d'audit ou de filtrage. |

## 🏗️ 2. Périmètre & Rôle de la Spécification
* **Positionnement dans l'Architecture :** Implémentation modulaire prête pour l'intégration MCP et l'orchestration locale (*Air-Gapped*).

## 📐 3. Spécifications Formelles & Contrats d'Interface MCP
* **Contrat Frugal :** `run_frugal_filtering()` agit comme un `MCP Tool` retournant le chemin du delta et ses métadonnées.
* **Contrat Orchestrateur :** `run_soc_audit_pipeline()` centralise la boucle d'exécution et renvoie un rapport JSON standardisable.

## 📊 4. Matrice des Exigences & Critères d'Acceptation (EXG-)

| Identifiant   | UID              | Domaine | Core/Non-Core | Intitulé de l'Exigence | Description & Critères d'Acceptation          | Mode de Test / Asset      |
| :------------ | :--------------- | :------ | :------------ | :--------------------- | :-------------------------------------------- | :------------------------ |
| **EXG-P8-05** | EXG-TEC-P8-soc_1 | `TEC`   | Core          | API Asynchrone         | Pilotage asynchrone avec timeout de 30s.      | PyTest / AsyncIO Suite    |
| **EXG-P8-06** | EXG-TEC-P8-soc_2 | `TEC`   | Core          | Pipeline NER Local     | Exécution 100% Air-Gapped du modèle GLiNER.   | PyTest / Air-Gapped Check |
| **EXG-P8-07** | EXG-TEC-P8-soc_3 | `TEC`   | Core          | Architecture MCP-Ready | Typage strict et découplage pour wrapper MCP. | PyTest / Interface Check  |


## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest
* **Scripts associés :** `03-Application/frugal_filter.py`, `03-Application/soc_orchestrator.py`, `03-Application/hitm_gateway.py`.
* **Suites de Tests :** `tests/test_soc_orchestrator.py`.