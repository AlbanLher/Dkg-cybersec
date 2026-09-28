"""
03-Application/Phase5/mitm_agent.py

Agent MITM (Man-In-The-Middle) - Phase 5
Conforme à SPEC-TECH-P05, config.py, Principe de Replay et Auto-Documentation.
"""

import logging
import sys
import shutil
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import numpy as np
from rdflib import Graph, Literal, URIRef, RDF, SKOS, OWL, XSD, RDFS
from sentence_transformers import SentenceTransformer, util

# Ancrage dynamique du dossier 03-Application dans le PYTHONPATH
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from Phase5.schemas import InterceptionPayload, AlignmentResult
from config import (
    DIR_EMBEDDING_MODEL,
    EMBEDDING_MODEL_NAME,
    MITM_SIMILARITY_THRESHOLD,
    DIR_SNAPSHOT_P5,
    DIR_TBOX_AMBER,
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI,
    SH
)

TB = "`" * 3  # Évite toute rupture de bloc Markdown

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
        """Charge le modèle d'embedding en local (Air-Gapped)."""
        logger.info(f"Chargement du modèle SentenceTransformer ({EMBEDDING_MODEL_NAME})...")
        try:
            if DIR_EMBEDDING_MODEL.exists() and any(DIR_EMBEDDING_MODEL.iterdir()):
                model = SentenceTransformer(str(DIR_EMBEDDING_MODEL))
                logger.info(f"Modèle chargé depuis le cache local : {DIR_EMBEDDING_MODEL}")
            else:
                model = SentenceTransformer(EMBEDDING_MODEL_NAME)
                logger.info(f"Modèle téléchargé / initialisé : {EMBEDDING_MODEL_NAME}")
            return model
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle IA : {e}")
            raise RuntimeError("Impossible d'initialiser le modèle local MiniLM")

    def bind_mandatory_prefixes(self, graph: Graph):
        """Binds mandatory prefixes."""
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
        """Extrait et vectorise toutes les entités nommées et labels existants."""
        logger.info("Indexation et vectorisation du graphe de connaissances existant...")
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
        """Intercepte un label candidat et calcule la similarité cosinus avec l'existant."""
        if self.entity_embeddings is None or len(self.existing_entities) == 0:
            return None, 0.0

        candidate_embedding = self.model.encode(candidate_label, convert_to_tensor=True)
        cosine_scores = util.cos_sim(candidate_embedding, self.entity_embeddings)[0]

        best_idx = int(np.argmax(cosine_scores.cpu().numpy()))
        raw_score = float(cosine_scores[best_idx])
        # Borne la valeur entre 0.0 et 1.0 pour prévenir les imprécisions de calcul flottant float32
        best_score = min(1.0, max(0.0, raw_score))
        best_match_uri = self.existing_entities[best_idx]["uri"]

        logger.info(
            f"Candidat '{candidate_label}' -> Best match : "
            f"{self.existing_entities[best_idx]['label']} ({best_match_uri}) | Score = {best_score:.4f}"
        )
        return best_match_uri, best_score

    def _build_alignment_subgraph(self, result: AlignmentResult) -> Graph:
        """Construit le sous-graphe d'alignement à partir d'un AlignmentResult validé."""
        alignment_graph = Graph()
        self.bind_mandatory_prefixes(alignment_graph)

        cand_ref = URIRef(result.candidate_uri)
        score_prop = URIRef(f"{DKG_TBOX}alignmentScore")
        alignment_graph.add((cand_ref, score_prop, Literal(result.similarity_score, datatype=XSD.float)))

        if result.is_matched and result.target_uri:
            logger.info(f"MATCH VALIDÉ (>= {self.threshold}) : Consolidation SKOS/OWL appliquée.")
            target_ref = URIRef(result.target_uri)
            alignment_graph.add((cand_ref, SKOS.exactMatch, target_ref))
            alignment_graph.add((cand_ref, OWL.sameAs, target_ref))
        else:
            logger.info(f"PAS DE MATCH (< {self.threshold}) : Entité conservée indépendante.")

        return alignment_graph

    def process_interception(self, candidate_uri: str, label: str) -> Graph:
        """Point d'entrée principal : valide le payload via Pydantic puis génère les déductions."""
        payload = InterceptionPayload(candidate_uri=candidate_uri, label=label)
        match_uri, score = self.evaluate_candidate(payload.label)

        result = AlignmentResult(
            candidate_uri=payload.candidate_uri,
            target_uri=match_uri,
            similarity_score=score,
            is_matched=(score >= self.threshold)
        )
        return self._build_alignment_subgraph(result)

    def save_and_document(self, alignment_graph: Graph, filename_base: str = "DKG_MITM_Alignment"):
        """Sauvegarde les artefacts TTL et MD selon le principe de Replay & Auto-Doc."""
        DIR_SNAPSHOT_P5.mkdir(parents=True, exist_ok=True)

        ttl_snapshot = DIR_SNAPSHOT_P5 / f"{filename_base}.ttl"
        md_snapshot = DIR_SNAPSHOT_P5 / f"{filename_base}.md"

        ttl_master = DIR_TBOX_AMBER / f"{filename_base}.ttl"
        md_master = DIR_TBOX_AMBER / f"{filename_base}.md"

        # 1. Écriture Turtle
        self.bind_mandatory_prefixes(alignment_graph)
        alignment_graph.serialize(destination=str(ttl_snapshot), format="ttl")

        # 2. Écriture Documentation Markdown Miroir
        md_content = f"""# 📑 Documentation Alignment Agent MITM - {filename_base}

**Classification :** `TLP:AMBER`  
**Seuil de Similarité Cosinus :** `{self.threshold}`  
**Nombre de triplets produits :** `{len(alignment_graph)}`

---

## 📖 Glossaire & Table des Acronymes Métier

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **MITM** | Man-In-The-Middle | Agent d'interception et d'alignement sémantique IA. |
| **NLP** | Natural Language Processing | Traitement automatique du langage via MiniLM. |
| **SKOS** | Simple Knowledge Organization System | Thésaurus d'alignement d'entités (`skos:exactMatch`). |
| **SSOT** | Single Source of Truth | Source unique de vérité (`config.py`). |

---

## 🔄 Flux d'Interception & Vectorisation IA

{TB}mermaid
flowchart LR
    CAND[Label Candidat] --> VECT[MiniLM Embedding]
    VECT --> COS[Cosine Similarity]
    COS -->|Score >= {self.threshold}| EXACT[skos:exactMatch / owl:sameAs]
    COS -->|Score < {self.threshold}| INDEP[Entité Indépendante]
{TB}

*Document généré automatiquement post-alignement MITM.*
"""
        with open(md_snapshot, "w", encoding="utf-8") as f:
            f.write(md_content)

        # 3. Replay / Capitalisation vers Master
        shutil.copy(ttl_snapshot, ttl_master)
        shutil.copy(md_snapshot, md_master)
        logger.info(f"[✅] Artefacts MITM Replay & Auto-Doc synchronisés dans {DIR_TBOX_AMBER}")


if __name__ == "__main__":
    agent = MITMAgent()

    test_graph = Graph()
    test_graph.add((URIRef(f"{DKG_DATA}host_01"), RDF.type, URIRef(f"{DKG_TBOX}Server")))
    test_graph.add((URIRef(f"{DKG_DATA}host_01"), SKOS.prefLabel, Literal("Serveur Principal AD")))

    agent.index_existing_knowledge(test_graph)
    subgraph = agent.process_interception(f"{DKG_DATA}candidate_99", "Serveur Contrôleur AD")
    agent.save_and_document(subgraph, "DKG_MITM_Test_Alignment")
