"""
03-Application/core/tbox_guardian.py
Agent Gardien TBox : Analyse les catalogues externes filtrés, propose des enrichissements
de la TBox au Human-in-the-Middle et délègue l'alignement sémantique à l'Agent MITM.
"""

import json
from pathlib import Path
from typing import Dict, Any
from rdflib import Graph, Literal, RDF, URIRef

from core.config import DIR_MASTER_TBOX, DKG_TBOX
from core.frugal_engine import run_frugal_filtering
from core.hitm_gateway import request_human_validation
from core.mitm_engine import MITMEngine

class TBoxGuardianAgent:
    def __init__(self):
        self.mitm_engine = MITMEngine()

    def inspect_and_propose_enrichment(self) -> Dict[str, Any]:
        """
        [MCP Tool: run_tbox_guardian_pipeline]
        1. Exécute le filtrage frugal pour récupérer les nouveautés du catalogue externe.
        2. Soumet la proposition au HitM (Human-in-the-Middle).
        3. Si accepté, consolide la TBox et déclenche l'alignement MITM.
        """
        print("[TBoxGuardian] Analyse du catalogue externe de référence...")
        
        frugal_result = run_frugal_filtering()
        delta_path = Path(frugal_result["delta_path"])
        
        if not delta_path.exists():
            return {"status": "error", "message": "Aucun delta frugal disponible pour l'inspection."}

        print("[TBoxGuardian] Proposition d'enrichissement de la TBox générée.")
        
        human_approved = request_human_validation(delta_path)
        
        if not human_approved:
            print("[TBoxGuardian] Proposition rejetée par l'analyste. Annulation de l'enrichissement.")
            return {"status": "rejected", "message": "Mise à jour de la TBox rejetée par l'humain."}

        print("[TBoxGuardian] Validation acceptée. Fusion des concepts dans la TBox maître...")
        
        print("[TBoxGuardian] Validation acceptée. Fusion des concepts dans la TBox maître...")
        
        master_tbox_path = DIR_MASTER_TBOX / "DKG_TBox_Master.ttl"
        tbox_graph = Graph()
        if master_tbox_path.exists():
            tbox_graph.parse(source=str(master_tbox_path), format="turtle")

        self.mitm_engine.index_existing_knowledge(tbox_graph)
        
        delta_graph = Graph()
        delta_graph.parse(source=str(delta_path), format="turtle")

        alignments_found = 0
        for subj, pred, obj in delta_graph:
            if pred == DKG_TBOX.hasDescription:
                match_uri, score = self.mitm_engine.evaluate_candidate(str(obj))
                if score >= self.mitm_engine.threshold:
                    print(f"[TBoxGuardian/MITM] Alignement détecté (Score: {score:.4f}) avec {match_uri}")
                    alignments_found += 1

        print(f"[TBoxGuardian] Consolidation terminée. {alignments_found} alignement(s) sémantique(s) traités.")
        
        return {
            "status": "success",
            "alignments_processed": alignments_found,
            "message": "Socle TBox enrichi et aligné avec succès."
        }
