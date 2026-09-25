"""
03-Application/soc_orchestrator.py
Orchestrateur SOC de la Phase 8 (MCP-Ready).
Expose la boucle d'audit incrémental, validable par les agents via des outils standardisés.
"""

import json
from pathlib import Path
from typing import Dict, Any
from rdflib import Graph
import pyshacl

from config import (
    DELTA_BUFFER_PATH,
    SHACL_MASTER_PATH,
    ABOX_MASTER_PATH,
    AUDIT_GOVERNANCE_REPORT_PATH
)
from frugal_filter import run_frugal_filtering
from hitm_gateway import request_human_validation

def run_soc_audit_pipeline() -> Dict[str, Any]:
    """
    [MCP Tool: run_soc_audit_pipeline]
    Exécute le cycle complet d'orchestration SOC :
    1. Filtrage frugal via l'outil dédié.
    2. Validation SHACL du delta.
    3. Contrôle Human-in-the-Middle (HitM).
    4. Fusion incrémentale dans la base cible.
    """
    print("[SOCOrchestrator] Exécution de l'outil MCP : Pipeline d'audit SOC...")
    
    report = {
        "status": "FAILED",
        "delta_file": str(DELTA_BUFFER_PATH),
        "shacl_valid": False,
        "hitm_approved": False,
        "merged": False
    }

    # Étape 1 : Appel de l'outil de filtrage frugal
    filter_result = run_frugal_filtering()
    delta_path = Path(filter_result["delta_path"])
    
    delta_graph = Graph()
    delta_graph.parse(destination=str(delta_path), format="turtle")

    # Étape 2 : Validation SHACL du delta
    shacl_valid = True
    if SHACL_MASTER_PATH.exists():
        print("[SOCOrchestrator] Validation SHACL du delta en cours...")
        shacl_graph = Graph()
        shacl_graph.parse(destination=str(SHACL_MASTER_PATH), format="turtle")
        conforms, _, results_text = pyshacl.validate(
            delta_graph,
            shacl_graph=shacl_graph,
            inference='none',
            advanced=True
        )
        shacl_valid = conforms
        report["shacl_valid"] = shacl_valid
        if not shacl_valid:
            print(f"[SOCOrchestrator] ERREUR : Le delta viole les contraintes SHACL :\n{results_text}")
            return report
    else:
        print("[SOCOrchestrator] Avertissement : Fichier SHACL master absent, validation ignorée.")

    # Étape 3 : Contrôle Human-in-the-Middle (HitM)
    hitm_approved = request_human_validation(delta_path)
    report["hitm_approved"] = hitm_approved
    
    if not hitm_approved:
        print("[SOCOrchestrator] Processus interrompu par l'humain.")
        return report

    # Étape 4 : Fusion Incrémentale
    print("[SOCOrchestrator] Fusion incrémentale du delta dans le graphe cible...")
    target_graph = Graph()
    if ABOX_MASTER_PATH.exists():
        target_graph.parse(destination=str(ABOX_MASTER_PATH), format="turtle")
    
    target_graph += delta_graph
    
    ABOX_MASTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    target_graph.serialize(destination=str(ABOX_MASTER_PATH), format="turtle")
    
    report["status"] = "SUCCESS"
    report["merged"] = True
    print(f"[SOCOrchestrator] Succès. Total triplets : {len(target_graph)}")

    AUDIT_GOVERNANCE_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_GOVERNANCE_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report

if __name__ == "__main__":
    run_soc_audit_pipeline()