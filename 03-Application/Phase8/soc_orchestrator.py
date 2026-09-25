"""
03-Application/soc_orchestrator.py
Orchestrateur SOC de la Phase 8 : Pilotage de l'audit incrémental et de la conformité.
"""

import json
from pathlib import Path
from rdflib import Graph
import pyshacl

from config import (
    DELTA_BUFFER_PATH,
    SHACL_MASTER_PATH,
    ABOX_MASTER_PATH,
    AUDIT_GOVERNANCE_REPORT_PATH,
    REQUIRE_HITM_FOR_TBOX
)
from frugal_filter import run_frugal_filtering
from hitm_gateway import request_human_validation

def run_soc_audit_pipeline() -> dict:
    """
    Exécute le cycle complet d'orchestration SOC :
    1. Filtrage frugal et création du delta.
    2. Validation SHACL du delta.
    3. Contrôle Human-in-the-Middle (HitM).
    4. Fusion incrémentale dans la base cible.
    """
    print("[SOCOrchestrator] Lancement de la boucle d'orchestration SOC (Phase 8)...")
    
    report = {
        "status": "FAILED",
        "delta_file": str(DELTA_BUFFER_PATH),
        "shacl_valid": False,
        "hitm_approved": False,
        "merged": False
    }

    # Étape 1 : Filtrage Frugal
    delta_path = run_frugal_filtering()
    delta_graph = Graph()
    delta_graph.parse(destination=str(delta_path), format="turtle")

    # Étape 2 : Validation SHACL du delta (si le fichier SHACL existe)
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
        print("[SOCOrchestrator] Avertissement : Fichier SHACL master absent, validation ignorée pour ce test.")

    # Étape 3 : Contrôle Human-in-the-Middle (HitM)
    hitm_approved = request_human_validation(delta_path)
    report["hitm_approved"] = hitm_approved
    
    if not hitm_approved:
        print("[SOCOrchestrator] Processus interrompu par l'humain.")
        return report

    # Étape 4 : Fusion Incrémentale dans le graphe ABox Master
    print("[SOCOrchestrator] Fusion incrémentale du delta dans le graphe cible...")
    target_graph = Graph()
    if ABOX_MASTER_PATH.exists():
        target_graph.parse(destination=str(ABOX_MASTER_PATH), format="turtle")
    
    # Fusion
    target_graph += delta_graph
    
    ABOX_MASTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    target_graph.serialize(destination=str(ABOX_MASTER_PATH), format="turtle")
    
    report["status"] = "SUCCESS"
    report["merged"] = True
    print(f"[SOCOrchestrator] Audit et fusion incrémentale réussis. Triplets totaux dans la cible : {len(target_graph)}")

    # Enregistrement du rapport d'audit
    AUDIT_GOVERNANCE_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_GOVERNANCE_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report

if __name__ == "__main__":
    run_soc_audit_pipeline()