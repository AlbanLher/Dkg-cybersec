#!/usr/bin/env python3
"""
mitm_agent.py
Agent MITM (Gouvernance Sémantique & Alignement TBox).
Conforme aux exigences d'exécution Air-Gapped / Offline.
"""

import sys
from pathlib import Path
from rdflib import Graph, RDFS

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from config import (
    TBOX_MASTER_PATH,
    DIR_EMBEDDING_MODEL,
    EMBEDDING_MODEL_NAME,
    MITM_SIMILARITY_THRESHOLD,
    DKG_TBOX,
    RDFS
)

class MITMAlignmentAgent:
    def __init__(self):
        print("[+] Initialisation de l'Agent MITM (Gouvernance Sémantique)...")
        self.threshold = MITM_SIMILARITY_THRESHOLD
        self.tbox_graph = Graph()
        self.embedding_model = None
        self.known_concepts = {}
        
        self._load_tbox()
        self._load_local_embedding_model()
        self._index_tbox_concepts()

    def _load_tbox(self):
        if Path(TBOX_MASTER_PATH).exists():
            self.tbox_graph.parse(str(TBOX_MASTER_PATH), format="ttl")
            print(f"[✓] TBox Master chargée ({len(self.tbox_graph)} triples) depuis : {TBOX_MASTER_PATH}")

    def _load_local_embedding_model(self):
        model_path = Path(DIR_EMBEDDING_MODEL)
        print(f"[*] Chargement du modèle SentenceTransformers local depuis : {model_path}")
        
        try:
            from sentence_transformers import SentenceTransformer
            if model_path.exists() and any(model_path.iterdir()):
                self.embedding_model = SentenceTransformer(str(model_path))
                print("[✓] Modèle d'embeddings local chargé avec succès.")
            else:
                print(f"[!] Cache local vide sous {model_path}. Chargement de secours ({EMBEDDING_MODEL_NAME})...")
                self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        except Exception as e:
            print(f"[❌] Erreur lors du chargement du modèle d'embeddings : {e}")
            raise e

    def _index_tbox_concepts(self):
        concepts = []
        uris = []

        for s, p, o in self.tbox_graph.triples((None, RDFS.label, None)):
            concept_label = str(o).lower()
            concepts.append(concept_label)
            uris.append(s)

        if concepts and self.embedding_model:
            embeddings = self.embedding_model.encode(concepts, convert_to_tensor=True)
            for uri, label, emb in zip(uris, concepts, embeddings):
                self.known_concepts[str(uri)] = {
                    "label": label,
                    "embedding": emb,
                    "uri": uri
                }
            print(f"[✓] Indexation vectorielle terminée : {len(self.known_concepts)} concepts TBox indexés.")

    def _cosine_similarity(self, tensor_a, tensor_b):
        from sentence_transformers import util
        return float(util.cos_sim(tensor_a, tensor_b)[0][0])

    def align_entity(self, extracted_entity: str, predicted_type: str = "Concept") -> dict:
        if not self.embedding_model or not self.known_concepts:
            return {
                "entity": extracted_entity,
                "status": "ERROR",
                "reason": "Modèle ou indexation non disponible"
            }

        entity_emb = self.embedding_model.encode(extracted_entity.lower(), convert_to_tensor=True)
        best_match = None
        highest_score = -1.0

        for uri, data in self.known_concepts.items():
            score = self._cosine_similarity(entity_emb, data["embedding"])
            if score > highest_score:
                highest_score = score
                best_match = data

        if highest_score >= self.threshold:
            return {
                "entity": extracted_entity,
                "status": "ACCEPTED",
                "aligned_uri": str(best_match["uri"]),
                "matched_label": best_match["label"],
                "confidence_score": round(highest_score, 4),
                "action": "Mapped to existing TBox concept"
            }
        else:
            suggested_uri = DKG_TBOX[extracted_entity.replace(" ", "")]
            return {
                "entity": extracted_entity,
                "status": "PROPOSE_EXTENSION",
                "suggested_uri": str(suggested_uri),
                "highest_similarity": round(highest_score, 4),
                "action": "Requires Human Validation / TBox Extension Proposal"
            }

def main():
    print("======================================================================")
    print("🛡️ DKG-CyberSec — Test unitaire de l'Agent MITM (Air-Gapped)")
    print("======================================================================")

    agent = MITMAlignmentAgent()
    test_entities = ["Asset", "Vulnerability", "UnknownCyberAttackVector", "SoftwareComponent"]
    
    print("[+] Exécution des tests d'alignement sémantique :")
    for entity in test_entities:
        result = agent.align_entity(entity)
        print(f"Entité : '{entity}' | Status : {result['status']} | Action : {result['action']}")

if __name__ == "__main__":
    main()
