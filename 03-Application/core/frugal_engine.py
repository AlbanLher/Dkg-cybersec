"""
03-Application/core/frugal_engine.py
Moteur de filtrage frugal et de transformation en deltas RDF (Core Service).
"""

import json
from typing import Dict, Any
from rdflib import Graph, Literal, RDF, URIRef
from core.config import (
    EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH,
    DIR_SNAPSHOT_P8,
    DKG_TBOX,
    DKG_DATA
)

DELTA_BUFFER_PATH = DIR_SNAPSHOT_P8 / "frugal_delta_buffer.ttl"
MAX_TRIPLES_IN_MEMORY = 50000

def run_frugal_filtering() -> Dict[str, Any]:
    """Exécute le filtrage amont et génère le delta RDF."""
    print("[FrugalEngine] Exécution du filtrage frugal...")

    delta_graph = Graph()
    delta_graph.bind("dkg", DKG_TBOX)
    delta_graph.bind("data", DKG_DATA)

    if EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH.exists():
        with open(EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH, "r", encoding="utf-8") as f:
            feed_data = json.load(f)

            # Supporte à la fois "requirements" et "sources" (selon la structure du registre)
            items = feed_data.get("requirements", feed_data.get("sources", []))

            for item in items:
                # Récupère l'identifiant selon la structure (id ou source_id)
                item_id = item.get("id", item.get("source_id", "UnknownSource"))
                # Récupère la description (directe ou dans filter_rules)
                desc = item.get("description")
                if not desc and "filter_rules" in item:
                    desc = item["filter_rules"].get("description", item.get("title", ""))

                req_uri = URIRef(f"{DKG_DATA}RegRequirement_{item_id}")
                delta_graph.add((req_uri, RDF.type, DKG_TBOX.RegulatoryConstraint))
                if desc:
                    delta_graph.add((req_uri, DKG_TBOX.hasDescription, Literal(desc)))

    if len(delta_graph) == 0:
        default_uri = URIRef(f"{DKG_DATA}RegRequirement_GDPR_Art32")
        delta_graph.add((default_uri, RDF.type, DKG_TBOX.RegulatoryConstraint))
        delta_graph.add((default_uri, DKG_TBOX.hasDescription, Literal("Mandatory encryption and resilience.")))

    triple_count = len(delta_graph)
    if triple_count > MAX_TRIPLES_IN_MEMORY:
        raise ValueError(f"[FrugalEngine] Dépassement de seuil mémoire ({triple_count})")

    DELTA_BUFFER_PATH.parent.mkdir(parents=True, exist_ok=True)
    delta_graph.serialize(destination=str(DELTA_BUFFER_PATH), format="turtle")

    return {
        "status": "success",
        "delta_path": str(DELTA_BUFFER_PATH),
        "triple_count": triple_count
    }
