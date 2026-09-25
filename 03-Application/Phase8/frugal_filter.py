"""
03-Application/frugal_filter.py
Module de filtrage frugal et de transformation en deltas RDF (Phase 8 - MCP-Ready).
Conçu pour être encapsulé comme un 'MCP Tool'.
"""

import json
from pathlib import Path
from typing import Dict, Any
from rdflib import Graph, Literal, RDF, URIRef
from config import (
    INPUT_PHASE8_REGULATION_PATH,
    DELTA_BUFFER_PATH,
    DKG_TBOX,
    DKG_DATA,
    MAX_TRIPLES_IN_MEMORY
)

def run_frugal_filtering() -> Dict[str, Any]:
    """
    [MCP Tool: run_frugal_filtering]
    Exécute le filtrage amont des données externes (ex: RGPD Art. 32)
    pour ne produire qu'un sous-ensemble minimal de triplets (delta).
    
    Returns:
        Dict contenant les métadonnées d'exécution et le chemin du delta.
    """
    print("[FrugalFilter] Exécution de l'outil MCP : Filtrage frugal...")
    
    delta_graph = Graph()
    delta_graph.bind("dkg", DKG_TBOX)
    delta_graph.bind("data", DKG_DATA)

    if INPUT_PHASE8_REGULATION_PATH.exists():
        with open(INPUT_PHASE8_REGULATION_PATH, "r", encoding="utf-8") as f:
            feed_data = json.load(f)
            for item in feed_data.get("requirements", []):
                req_uri = URIRef(f"{DKG_DATA}RegRequirement_{item.get('id')}")
                delta_graph.add((req_uri, RDF.type, DKG_TBOX.RegulatoryConstraint))
                delta_graph.add((req_uri, DKG_TBOX.hasDescription, Literal(item.get('description'))))
    else:
        default_uri = URIRef(f"{DKG_DATA}RegRequirement_GDPR_Art32")
        delta_graph.add((default_uri, RDF.type, DKG_TBOX.RegulatoryConstraint))
        delta_graph.add((default_uri, DKG_TBOX.hasDescription, Literal("Mandatory encryption and resilience for internal assets.")))

    triple_count = len(delta_graph)
    if triple_count > MAX_TRIPLES_IN_MEMORY:
        raise ValueError(f"[FrugalFilter] Erreur Green Dev : Le delta dépasse le seuil autorisé ({triple_count} > {MAX_TRIPLES_IN_MEMORY})")

    DELTA_BUFFER_PATH.parent.mkdir(parents=True, exist_ok=True)
    delta_graph.serialize(destination=str(DELTA_BUFFER_PATH), format="turtle")
    
    print(f"[FrugalFilter] Succès : {triple_count} triplets générés dans {DELTA_BUFFER_PATH}")
    
    return {
        "status": "success",
        "delta_path": str(DELTA_BUFFER_PATH),
        "triple_count": triple_count
    }

if __name__ == "__main__":
    run_frugal_filtering()