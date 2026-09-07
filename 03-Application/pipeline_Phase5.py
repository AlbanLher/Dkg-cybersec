"""
03-Application/Phase5/pipeline_phase5.py

Pipeline d'Orchestration Globale - Phase 5 / Vague 3
Conforme à SPEC-SOCLE-04 et SPEC-TECH-P05.

Séquence d'exécution :
1. Agent MITM (Vectorisation & Alignment Seuil 0.85)
2. Consolidation SKOS / Master TBox
3. Moteur d'Inférence (CISA KEV & Silent Cascade)
4. Matérialisation & Validation Ségrégation TLP
"""

import logging
import sys
import time
from pathlib import Path
from rdflib import Graph, Literal, URIRef

# Configuration du PYTHONPATH pour l'ancrage SSOT config.py
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import (
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    ABOX_INFERED_PATH,
    TBOX_MASTER_PATH,
    DKG_TBOX,
    DKG_DATA,
    MITM_SIMILARITY_THRESHOLD
)
from Phase5.mitm_agent import MITMAgent
from Phase5.skos_consolidator import SKOSConsolidator
from Phase5.reasoning_engine import ReasoningEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("PipelinePhase5")


def run_pipeline_phase5():
    pipeline_start = time.time()
    logger.info("==================================================")
    logger.info("   Lancement du Pipeline Phase 5 (DKG-CyberSec)  ")
    logger.info("==================================================")

    # ----------------------------------------------------
    # STEP 1 : Interception MITM & Alignement Sémantique
    # ----------------------------------------------------
    logger.info("\n--- [1/3] Exécution de l'Agent MITM ---")
    mitm = MITMAgent(threshold=MITM_SIMILARITY_THRESHOLD)

    # Charger le graphe existant pour vectorisation
    knowledge_base = Graph()
    if Path(ABOX_RED_PATH).exists():
        knowledge_base.parse(str(ABOX_RED_PATH), format="turtle")
    if Path(ABOX_CTI_PATH).exists():
        knowledge_base.parse(str(ABOX_CTI_PATH), format="turtle")

    mitm.index_existing_knowledge(knowledge_base)

    # Simulation d'interception d'entités candidates
    candidates = [
        (f"{DKG_DATA}cand_01", "Serveur Controleur AD Interne"),
        (f"{DKG_DATA}cand_02", "Acteur de menace Cozy Bear APT29")
    ]

    alignment_batch = Graph()
    for cand_uri, cand_label in candidates:
        subgraph = mitm.process_interception(cand_uri, cand_label)
        alignment_batch += subgraph

    # ----------------------------------------------------
    # STEP 2 : Consolidation SKOS / Master TBox
    # ----------------------------------------------------
    logger.info("\n--- [2/3] Consolidation Sémantique SKOS ---")
    consolidator = SKOSConsolidator()
    consolidator.load_base_tbox()
    added_skos = consolidator.consolidate_alignment_graph(alignment_batch)
    consolidator.save_skos_master()

    # ----------------------------------------------------
    # STEP 3 : Exécution Moteur d'Inférence & RBox
    # ----------------------------------------------------
    logger.info("\n--- [3/3] Exécution du Moteur de Raisonnement ---")
    engine = ReasoningEngine()
    exec_time_inf = engine.run_inference()
    engine.save_infered_graph()

    total_duration = time.time() - pipeline_start
    logger.info("\n==================================================")
    logger.info(f" Pipeline Phase 5 Terminé avec Succès ({total_duration:.2f}s)")
    logger.info(f" Artefact Déduit : {ABOX_INFERED_PATH}")
    logger.info("==================================================")


if __name__ == "__main__":
    run_pipeline_phase5()
