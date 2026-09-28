---
type: phase
phase_num: "08"
phase_code: P8
phase_nom: Orchestration MCP & Moteurs d'Agents Souverains
vague: V4
statut: 🟡 ACTIVE
date_debut: 2026-09-09
date_cloture:
---
# 📋 P8 : Orchestration MCP & Moteurs d'Agents Souverains

## 🎯 1. Objectifs & Périmètre
* **But principal** : Implémenter l'orchestration multi-agents via le protocole MCP (`mcp_server.py`) en mode strictement *Air-Gapped* et *Green-by-Design*, recentrée exclusivement sur le **Groupe 1 (Actifs, Vulnérabilités et Menaces)**. Le système capture les flux externes de référence (*Les Communs* comme MITRE/CVE) via un filtrage frugal, les soumet à l'alignement sémantique (MITM) sous validation humaine (*HitM*), et utilise le simulateur pour tracer les abaques de performance.
* **Scénario interactif didactique** : 
  1. *Cas Laboratoire / Pédagogique :* Analyse d'une liste de composants logiciels d'une même famille pour illustrer la réconciliation sémantique.
  2. *Cas Contextuel Étendu :* Modélisation d'un environnement réaliste de foyer ou de petite entreprise (postes de travail, routeur, zone DMZ, pare-feu) dans l'ABox (`TLP:RED`). Le simulateur de charge génère une montée en volume de menaces et de vulnérabilités pour stresser l'architecture locale et rechercher empiriquement le point de rupture des moteurs standard (RAM < 85 Mo).

---

## 🛠️ 2. Traçabilité des Livrables par Brique

### A. Spécification & Gouvernance (SPEC Framework)
* **Spécifications associées** : 
  * `SPC-FWK-P8-agent_gardien_references_externes_01.md`[cite: 5]
  * `SPC-FWK-P8-soc_orchestration_governance_01.md`[cite: 6]
  * `SPC-TEC-P08_Green_Development_Framework_01.md`[cite: 9]
  * `SPC-TEC-P8-simulator_and_abaques_01.md`[cite: 10]
  * `SPC-TEC-P8-soc_orchestrator_agent_01.md`[cite: 11]

### B. Données & Ontologies (Data / Graph RDF)
* **Artefacts Master** : `Master_Transversal/` (Segmentation TLP:CLEAR pour les flux externes filtrés et TLP:RED pour les actifs et la DMZ du foyer).
* **Artefacts Snapshot** : `Snapshot_Phase_08/` (Tampons de deltas frugaux et registres de test de charge).

### C. Scripts & Outillage (Automation & CI/CD)
* **Orchestration MCP** : `mcp_server.py`
* **Moteurs d'Agents** : `frugal_engine.py`, `tbox_guardian.py`, `mitm_engine.py`, `hitm_gateway.py`
* **Simulateur & Benchmarks** : `simulator.py` (Génération de charge et abaques de performance *Green-by-Design*)
* **Tests Qualité** : `test_phase08_quality.py` et suite `pytest` dédiée.

