"""
DKG-CyberSec - Test de Qualité & Conformité Phase 5 (Vague 3)
Valide le fonctionnement offline, l'Agent MITM, l'Inférence Sémantique et le cloisonnement TLP.
"""

import os
import sys
import pytest
from pathlib import Path
from rdflib import Graph, RDF, RDFS

# Ancrage dynamique du dossier '03-Application' dans le sys.path
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Import unifié des constantes SSOT
from config import (
    TBOX_MASTER_PATH,
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    RULES_MASTER_PATH,
    ABOX_INFERED_PATH,
    DIR_MODELS,
    DIR_EMBEDDING_MODEL,
    MITM_SIMILARITY_THRESHOLD,
    DKG_TBOX,
    DOC_INFERED_MD_PATH,
    DIR_TBOX_AMBER,
    DIR_ABOX_RED,
    DIR_CTI_CLEAR,
    DIR_INFERED_RED
)

from Phase5.mitm_agent import MITMAlignmentAgent
from Phase5.generate_phase5_inference import run_pipeline


def test_00_strict_tbox_vocabulary_compliance():
    """Vérifie qu'aucun prédicat non-déclaré dans la TBox Master n'est utilisé dans les règles et ABox."""
    g_tbox = Graph().parse(str(TBOX_MASTER_PATH), format="ttl")
    
    # Extraire toutes les URIs définies dans la TBox
    declared_terms = set(g_tbox.subjects()) | set(g_tbox.predicates()) | set(g_tbox.objects())
    
    # Charger l'ABox Interne pour contrôle du vocabulaire
    g_abox = Graph().parse(str(ABOX_RED_PATH), format="ttl")
    used_predicates = set(g_abox.predicates())

    # Exclure les termes standards du W3C (RDF, RDFS, OWL, XSD)
    custom_predicates = {
        p for p in used_predicates 
        if str(p).startswith(str(DKG_TBOX))
    }

    for pred in custom_predicates:
        assert pred in declared_terms, f"Prédicat non-déclaré dans la TBox Master : {pred}"


def test_01_offline_cache_structure():
    """Vérifie que le répertoire du cache des modèles IA locaux existe pour l'exécution offline."""
    assert Path(DIR_MODELS).exists(), f"Le répertoire de cache {DIR_MODELS} doit exister."
    assert Path(DIR_EMBEDDING_MODEL).exists(), f"Le répertoire d'embeddings {DIR_EMBEDDING_MODEL} doit exister."


def test_02_mitm_alignment_agent():
    """Valide l'initialisation et la capacité d'alignement de l'Agent MITM."""
    agent = MITMAlignmentAgent()
    assert agent.embedding_model is not None, "Le modèle d'embeddings doit être chargé."
    
    # Test d'alignement sur un concept connu
    result_known = agent.align_entity("Asset")
    assert result_known["status"] == "ACCEPTED"
    assert result_known["confidence_score"] >= MITM_SIMILARITY_THRESHOLD

    # Test sur un concept inconnu (Proposition d'extension ontologique)
    result_unknown = agent.align_entity("UnknownZeroDayAttackVector")
    assert result_unknown["status"] == "PROPOSE_EXTENSION"


def test_03_tlp_isolation_and_artifacts():
    """Valide la présence des artéfacts RDF et le respect du découpage TLP."""
    assert Path(TBOX_MASTER_PATH).exists(), f"TBox introuvable sous {TBOX_MASTER_PATH}"
    assert Path(RULES_MASTER_PATH).exists(), f"Fichier de règles introuvable sous {RULES_MASTER_PATH}"
    
    # Vérification que le dossier d'inférence TLP:RED est bien séparé des données TLP:CLEAR
    assert DIR_INFERED_RED != DIR_CTI_CLEAR
    assert "TLP_RED" in str(DIR_INFERED_RED)


def test_04_inference_execution():
    """Valide l'exécution du pipeline d'inférence et la production de la ABox Infered."""
    # Exécution du pipeline Phase 5
    run_pipeline()

    # Vérification de la création du fichier Turtle enrichi
    assert Path(ABOX_INFERED_PATH).exists(), f"Fichier ABox Inferred introuvable sous {ABOX_INFERED_PATH}"
    
    g_inferred = Graph().parse(str(ABOX_INFERED_PATH), format="ttl")
    assert len(g_inferred) > 0, "Le graphe déduit ne doit pas être vide."


def test_05_documentation_artifacts():
    """Valide la présence du rapport Markdown et la structure du graphe Mermaid."""
    assert Path(DOC_INFERED_MD_PATH).exists(), f"Documentation introuvable sous {DOC_INFERED_MD_PATH}"
    
    content = Path(DOC_INFERED_MD_PATH).read_text(encoding="utf-8")
    assert "# 📑 Livrable Phase 5" in content
    assert "```mermaid" in content
    assert "flowchart TD" in content
