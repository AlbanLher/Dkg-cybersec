"""
03-Application/Phase5/mitm_agent.py

Agent MITM (Man-In-The-Middle) - Phase 5 / Vague 2 & 3
Conforme à SPEC-TECH-P05 et config.py.

Rôles principaux :
1. Vectoriser localement les entités candidates via SentenceTransformers (MiniLM).
2. Calculer la similarité cosinus avec le thésaurus / graphe existant.
3. Appliquer le seuil SSOT de réconciliation (MITM_SIMILARITY_THRESHOLD = 0.85)[cite: 2].
4. Générer la structure SKOS (exactMatch) ou proposer la création d'une nouvelle entité.
"""

import logging
import sys
from typing import Dict, List, Optional, Tuple
import numpy as np
from rdflib import Graph, Literal, URIRef, RDF, SKOS, OWL, XSD

from sentence_transformers import SentenceTransformer, util

# Importation obligatoire depuis la SSOT config.py[cite: 2]
from config import (
    DIR_EMBEDDING_MODEL,
    EMBEDDING_MODEL_NAME,
    MITM_SIMILARITY_THRESHOLD,
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI,
    ABOX_RED_PATH,
    ABOX_CTI_PATH
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("MITMAgent")


class MITMAgent:
    def __init__(self, threshold: float = MITM_SIMILARITY_THRESHOLD):
        self.threshold = threshold
        self.model = self._load_embedding_model()
        self.existing_entities: List[Dict[str, str]] = []
        self.entity_embeddings = None

    def _load_embedding_model(self) -> SentenceTransformer:
        """Charge le modèle d'embedding en local (Air-Gapped)[cite: 2]."""
        logger.info(f"Chargement du modèle SentenceTransformer ({EMBEDDING_MODEL_NAME})...")
        try:
            # Tente de charger depuis le cache local s'il existe[cite: 2]
            if DIR_EMBEDDING_MODEL.exists() and any(DIR_EMBEDDING_MODEL.iterdir()):
                model = SentenceTransformer(str(DIR_EMBEDDING_MODEL))
                logger.info(f"Modèle chargé depuis le cache local : {DIR_EMBEDDING_MODEL}")
            else:
                model = SentenceTransformer(EMBEDDING_MODEL_NAME)[cite: 2]
                logger.info(f"Modèle téléchargé / initialisé : {EMBEDDING_MODEL_NAME}")
            return model
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle IA : {e}")
            raise RuntimeError("Impossible d'initialiser le modèle local MiniLM")

    def index_existing_knowledge(self, knowledge_graph: Graph) -> int:
        """
        Extrait et vectorise toutes les entités nommées et labels existants
        dans le graphe de connaissances.
        """
        logger.info("Indexation et vectorisation du graphe de connaissances existant...")
        self.existing_entities = []
        texts_to_embed = []

        query = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
        SELECT DISTINCT ?entity ?label WHERE {{
            ?entity a ?type .
            OPTIONAL {{ ?entity rdfs:label ?rdfsLabel . }}
            OPTIONAL {{ ?entity skos:prefLabel ?skosLabel . }}
            BIND(COALESCE(?rdfsLabel, ?skosLabel, STR(?entity)) AS ?label)
        }}
        """
        results = knowledge_graph.query(query)
        for row in results:
            entity_uri = str(row.entity)
            label = str(row.label)
            self.existing_entities.append({"uri": entity_uri, "label": label})
            texts_to_embed.append(label)

        if texts_to_embed:
            self.entity_embeddings = self.model.encode(texts_to_embed, convert_to_tensor=True)
            logger.info(f"{len(self.existing_entities)} entités indexées avec succès.")
        else:
            logger.warning("Aucune entité trouvée pour l'indexation.")
            self.entity_embeddings = None

        return len(self.existing_entities)

    def evaluate_candidate(self, candidate_label: str) -> Tuple[Optional[str], float]:
        """
        Intercepte un label candidat et calcule la similarité cosinus avec l'existant.
        Retourne (best_match_uri, score).
        """
        if self.entity_embeddings is None or len(self.existing_entities) == 0:
            return None, 0.0

        candidate_embedding = self.model.encode(candidate_label, convert_to_tensor=True)
        cosine_scores = util.cos_sim(candidate_embedding, self.entity_embeddings)[0]

        best_idx = int(np.argmax(cosine_scores.cpu().numpy()))
        best_score = float(cosine_scores[best_idx])
        best_match_uri = self.existing_entities[best_idx]["uri"]

        logger.info(f"Candidat '{candidate_label}' -> Best match : {self.existing_entities[best_idx]['label']} ({best_match_uri}) | Score = {best_score:.4f}")
        return best_match_uri, best_score

    def process_interception(self, candidate_uri: str, candidate_label: str) -> Graph:
        """
        Génère un sous-graphe RDF d'alignement ou de création selon le seuil MITM_SIMILARITY_THRESHOLD[cite: 2].
        EXG-MITM-01 & EXG-MITM-02
        """
        alignment_graph = Graph()
        alignment_graph.bind("dkg", DKG_TBOX)
        alignment_graph.bind("skos", SKOS)
        alignment_graph.bind("owl", OWL)

        match_uri, score = self.evaluate_candidate(candidate_label)
        cand_ref = URIRef(candidate_uri)

        # Ajout des métadonnées du score
        score_prop = URIRef(f"{DKG_TBOX}alignmentScore")
        alignment_graph.add((cand_ref, score_prop, Literal(score, datatype=XSD.float)))

        if match_uri and score >= self.threshold:
            logger.info(f"MATCH VALIDÉ (>= {self.threshold}) : Consolidation SKOS/OWL appliquée.")
            target_ref = URIRef(match_uri)
            alignment_graph.add((cand_ref, SKOS.exactMatch, target_ref))
            alignment_graph.add((cand_ref, OWL.sameAs, target_ref))
        else:
            logger.info(f"PAS DE MATCH (< {self.threshold}) : Entité conservée indépendante.")

        return alignment_graph


if __name__ == "__main__":
    agent = MITMAgent()
    
    # Test à vide / Démo
    test_graph = Graph()
    test_graph.add((URIRef(f"{DKG_DATA}host_01"), RDF.type, URIRef(f"{DKG_TBOX}Server")))
    test_graph.add((URIRef(f"{DKG_DATA}host_01"), SKOS.prefLabel, Literal("Serveur Principal AD")))
    
    agent.index_existing_knowledge(test_graph)
    subgraph = agent.process_interception(f"{DKG_DATA}candidate_99", "Serveur Contrôleur AD")
    print(subgraph.serialize(format="turtle"))
