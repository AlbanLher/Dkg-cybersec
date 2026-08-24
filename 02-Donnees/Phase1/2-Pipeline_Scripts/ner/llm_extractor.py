import json
import os
from typing import Dict, Any
from rdflib import Graph, Literal, Namespace, RDF, RDFS

EX = Namespace("http://example.org/dkg/ontology#")
INST = Namespace("http://example.org/dkg/instance#")

class LLMTripletExtractor:
    """Extraction d'entités complexes et de triplets RDF guidée par le schéma TBox."""

    SYSTEM_PROMPT = """Tu es un expert en cybersécurité.
Ta mission est d'extraire les entités et leurs relations à partir du texte sous forme d'un objet JSON strict.

### Ontologie Autorisée (Phase 0) :
- Classes : [Equipment, Software, Vulnerability, ThreatActor, Service]
- Predicats : [hasSoftware, suffersFrom, hostsService, communicatesWith, runsOn]

### Structure JSON attendue :
{
  "entities": [
    {"id": "ent_1", "label": "Apache HTTP Server", "type": "Software"},
    {"id": "ent_2", "label": "SRV-WEB-01", "type": "Equipment"}
  ],
  "triplets": [
    {"subject": "ent_2", "predicate": "hasSoftware", "object": "ent_1"}
  ]
}
"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def extract_to_graph(self, text: str, graph: Graph) -> Graph:
        # Appel LLM (OpenAI / Local LLM) retournant le JSON structuré
        llm_response = self._call_llm_api(text)
        entity_map = {}

        # 1. Instanciation des Entités Extraites
        for ent in llm_response.get("entities", []):
            ent_type = ent.get("type", "Asset")
            label = ent.get("label", "Unknown")
            clean_id = re.sub(r'[^a-zA-Z0-9_]', '_', label)
            
            node_uri = INST[f"{ent_type}_{clean_id}"]
            entity_map[ent["id"]] = node_uri
            
            graph.add((node_uri, RDF.type, EX[ent_type]))
            graph.add((node_uri, RDFS.label, Literal(label)))

        # 2. Instanciation des Relations (Triplets RDF)
        for trip in llm_response.get("triplets", []):
            sub_uri = entity_map.get(trip.get("subject"))
            obj_uri = entity_map.get(trip.get("object"))
            pred_name = trip.get("predicate")

            if sub_uri and obj_uri and pred_name:
                graph.add((sub_uri, EX[pred_name], obj_uri))

        return graph

    def _call_llm_api(self, text: str) -> Dict[str, Any]:
        # À raccorder à votre client OpenAI / Ollama
        return {}
