"""
03-Application/core/mitm_engine.py
Moteur d'alignement sémantique et d'interception (Core Service).
"""

import logging
import sys
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import numpy as np
from rdflib import Graph, Literal, URIRef, RDF, SKOS, OWL, XSD, RDFS
from sentence_transformers import SentenceTransformer, util

from core.config import (
    DIR_EMBEDDING_MODEL,
    EMBEDDING_MODEL_NAME,
    MITM_SIMILARITY_THRESHOLD,
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI,
    SH
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MITMEngine")

class MITMEngine:
    def __init__(self, threshold: float = MITM_SIMILARITY_THRESHOLD):
        self.threshold = threshold
        self.model = self._load_embedding_model()
        self.existing_entities: List[Dict[str, str]] = []
        self.entity_embeddings = None

    def _load_embedding_model(self) -> SentenceTransformer:
        """Charge le modèle d'embedding en local (Air-Gapped)."""
        logger.info(f"Chargement du modèle SentenceTransformer ({EMBEDDING_MODEL_NAME})...")
        try:
            if DIR_EMBEDDING_MODEL.exists() and any(DIR_EMBEDDING_MODEL.iterdir()):
                model = SentenceTransformer(str(DIR_EMBEDDING_MODEL))
            else:
                model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            return model
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle IA : {e}")
            raise RuntimeError("Impossible d'initialiser le modèle local MiniLM")

    def bind_mandatory_prefixes(self, graph: Graph):
        graph.bind("dkg", DKG_TBOX)
        graph.bind("dkg-data", DKG_DATA)
        graph.bind("dkg-cti", DKG_CTI)
        graph.bind("sh", SH)
        graph.bind("xsd", XSD)
        graph.bind("rdfs", RDFS)
        graph.bind("skos", SKOS)
        graph.bind("owl", OWL)
        graph.bind("rdf", RDF)

    def index_existing_knowledge(self, knowledge_graph: Graph) -> int:
        self.existing_entities = []
        texts_to_embed = []

        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT DISTINCT ?entity ?label WHERE {
            ?entity a ?type .
            OPTIONAL { ?entity rdfs:label ?rdfsLabel . }
            OPTIONAL { ?entity skos:prefLabel ?skosLabel . }
            BIND(COALESCE(?rdfsLabel, ?skosLabel, STR(?entity)) AS ?label)
        }
        """.strip()

        results = knowledge_graph.query(query)
        for row in results:
            self.existing_entities.append({"uri": str(row.entity), "label": str(row.label)})
            texts_to_embed.append(str(row.label))

        if texts_to_embed:
            self.entity_embeddings = self.model.encode(texts_to_embed, convert_to_tensor=True)
        else:
            self.entity_embeddings = None

        return len(self.existing_entities)

    def evaluate_candidate(self, candidate_label: str) -> Tuple[Optional[str], float]:
        if self.entity_embeddings is None or len(self.existing_entities) == 0:
            return None, 0.0

        candidate_embedding = self.model.encode(candidate_label, convert_to_tensor=True)
        cosine_scores = util.cos_sim(candidate_embedding, self.entity_embeddings)[0]

        best_idx = int(np.argmax(cosine_scores.cpu().numpy()))
        raw_score = float(cosine_scores[best_idx])
        best_score = min(1.0, max(0.0, raw_score))
        return self.existing_entities[best_idx]["uri"], best_score
