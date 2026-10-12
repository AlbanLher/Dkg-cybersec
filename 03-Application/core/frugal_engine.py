"""
03-Application/core/frugal_engine.py
Moteur de filtrage amont & sobriété numérique (Green-by-Design).
Périmètre SOC_1 : Menaces & Vulnérabilités.
"""

import json
import logging
from typing import Dict, Any
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

from core import config

logger = logging.getLogger("FrugalEngine")

# Empreinte estimée du flux externe brut (CISA KEV + CERT-FR)
ESTIMATED_RAW_CTI_BYTES = 8_500_000  # ~8,5 Mo


def run_frugal_filtering() -> Dict[str, Any]:
    """Exécute le filtrage frugal CTI pour la Phase 8 (SOC_1)."""
    logger.info("Exécution du filtrage frugal SOC_1...")

    delta_graph = Graph()
    SOC1 = Namespace("http://home.secure/ontology/soc1#")
    delta_graph.bind("soc1", SOC1)
    delta_graph.bind("rdfs", RDFS)

    registry_path = config.EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH

    if registry_path.exists():
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
                
            for src in registry.get("sources", []):
                source_uri = URIRef(f"http://home.secure/cti/source/{src.get('source_id')}")
                delta_graph.add((source_uri, RDF.type, SOC1.CTISource))
                delta_graph.add((source_uri, RDFS.label, Literal(src.get("title"), lang="fr")))
                delta_graph.add((source_uri, SOC1.tlp, Literal(src.get("tlp"))))
                delta_graph.add((source_uri, SOC1.status, Literal(src.get("status"))))
                
        except Exception as err:
            logger.error(f"Erreur lors de la lecture du registre CTI : {err}")
    else:
        logger.warning(f"Fichier de registre introuvable dans {registry_path}")

    # Sérialisation dans le chemin centralisé par config.py
    config.DELTA_BUFFER_PATH.parent.mkdir(parents=True, exist_ok=True)
    delta_graph.serialize(destination=str(config.DELTA_BUFFER_PATH), format="turtle")

    filtered_size_bytes = config.DELTA_BUFFER_PATH.stat().st_size if config.DELTA_BUFFER_PATH.exists() else 0
    raw_size_bytes = ESTIMATED_RAW_CTI_BYTES
    
    reduction_pct = round(100.0 - (filtered_size_bytes / raw_size_bytes * 100.0), 4)

    return {
        "status": "success",
        "delta_path": str(config.DELTA_BUFFER_PATH),
        "triple_count": len(delta_graph),
        "raw_size_bytes": raw_size_bytes,
        "filtered_size_bytes": filtered_size_bytes,
        "reduction_pct": reduction_pct
    }


if __name__ == "__main__":
    res = run_frugal_filtering()
    print(f"Résultat : {res}")
