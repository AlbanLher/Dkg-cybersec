"""
03-Application/frugal_filter.py
Module de filtrage frugal et de transformation en deltas RDF (Phase 8).
Respecte les contraintes Green Dev et Air-Gapped.
"""

import json
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef
from config import (
    INPUT_PHASE8_REGULATION_PATH,
    DELTA_BUFFER_PATH,
    DKG_TBOX,
    DKG_DATA,
    MAX_TRIPLES_IN_MEMORY
)

def run_frugal_filtering() -> Path:
    """
    Simule ou exécute un filtrage amont des données externes (ex: RGPD Art. 32)
    pour ne produire qu'un sous-ensemble minimal de triplets (delta).
    """
    print("[FrugalFilter] Début du filtrage frugal des données externes...")
    
    delta_graph = Graph()
    delta_graph.bind("dkg", DKG_TBOX)
    delta_graph.bind("data", DKG_DATA)

    # Chargement du flux source si disponible, sinon création d'un delta par défaut
    if INPUT_PHASE8_REGULATION_PATH.exists():
        with open(INPUT_PHASE8_REGULATION_PATH, "r", encoding="utf-8") as f:
            feed_data = json.load(f)
            # Traitement frugal des exigences (ex: chiffrement, intégrité)
            for item in feed_data.get("requirements", []):
                req_uri = URIRef(f"{DKG_DATA}RegRequirement_{item.get('id')}")
                delta_graph.add((req_uri, RDF.type, DKG_TBOX.RegulatoryConstraint))
                delta_graph.add((req_uri, DKG_TBOX.hasDescription, Literal(item.get('description'))))
    else:
        # Fallback par défaut pour test unitaire autonome
        default_uri = URIRef(f"{DKG_DATA}RegRequirement_GDPR_Art32")
        delta_graph.add((default_uri, RDF.type, DKG_TBOX.RegulatoryConstraint))
        delta_graph.add((default_uri, DKG_TBOX.hasDescription, Literal("Mandatory encryption and resilience for internal assets.")))

    # Vérification de la contrainte Green Dev (Plafond RAM)
    triple_count = len(delta_graph)
    if triple_count > MAX_TRIPLES_IN_MEMORY:
        raise ValueError(f"[FrugalFilter] Erreur Green Dev : Le delta dépasse le seuil autorisé ({triple_count} > {MAX_TRIPLES_IN_MEMORY})")

    # Sauvegarde du delta dans le tampon
    DELTA_BUFFER_PATH.parent.mkdir(parents=True, exist_ok=True)
    delta_graph.serialize(destination=str(DELTA_BUFFER_PATH), format="turtle")
    print(f"[FrugalFilter] Delta frugal généré avec succès : {triple_count} triplets stockés dans {DELTA_BUFFER_PATH}")
    
    return DELTA_BUFFER_PATH

if __name__ == "__main__":
    run_frugal_filtering()