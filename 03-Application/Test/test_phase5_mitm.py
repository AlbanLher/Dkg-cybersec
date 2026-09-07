"""
03-Application/Tests/test_phase5_mitm.py

Suite de tests automatisés Pytest pour l'Agent MITM & la Consolidation SKOS (Phase 5).
Valide la conformité aux exigences SPEC-TECH-P05 :
- EXG-MITM-01 : Interception & Calcul de Similitude (SentenceTransformers MiniLM)
- EXG-MITM-02 : Réconciliation Seuil 0.85 (skos:exactMatch / owl:sameAs)
- EXG-SKOS-01 : Alignement Taxonomique SKOS (skos:Concept / skos:ConceptScheme)
- EXG-SKOS-02 : Ségrégation TLP en Ingestion Interceptée (Non-pollution de la ABox CTI CLEAR)
- EXG-HW-01   : Temps de réponse local économe (< 100 ms par évaluation d'entité)
"""

import sys
import time
import pytest
from pathlib import Path
from rdflib import Graph, URIRef, Literal, RDF, SKOS, OWL

# Ajout du dossier 03-Application au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import (
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI,
    ABOX_CTI_PATH,
    MITM_SIMILARITY_THRESHOLD
)
from Phase5.mitm_agent import MITMAgent
from Phase5.skos_consolidator import SKOSConsolidator


@pytest.fixture(scope="module")
def setup_mitm_context():
    """
    Fixture initialisant l'Agent MITM, un graphe de connaissances de référence,
    et le Consolidateur SKOS.
    """
    agent = MITMAgent(threshold=MITM_SIMILARITY_THRESHOLD)
    
    # Graphe de connaissance existant pour l'indexation
    knowledge_graph = Graph()
    knowledge_graph.bind("dkg", DKG_TBOX)
    knowledge_graph.bind("dkg-data", DKG_DATA)
    knowledge_graph.bind("skos", SKOS)
    
    # Entités existantes
    host_1 = URIRef(f"{DKG_DATA}server_ad_01")
    knowledge_graph.add((host_1, RDF.type, URIRef(f"{DKG_TBOX}Server")))
    knowledge_graph.add((host_1, SKOS.prefLabel, Literal("Serveur Controleur de Domaine Active Directory")))
    
    actor_1 = URIRef(f"{DKG_DATA}threat_actor_apt29")
    knowledge_graph.add((actor_1, RDF.type, URIRef(f"{DKG_TBOX}ThreatActor")))
    knowledge_graph.add((actor_1, SKOS.prefLabel, Literal("Cozy Bear APT29 Threat Group")))

    # Indexation
    agent.index_existing_knowledge(knowledge_graph)
    
    return {
        "agent": agent,
        "knowledge_graph": knowledge_graph,
        "consolidator": SKOSConsolidator()
    }


def test_exg_mitm_01_vectorization_and_similarity(setup_mitm_context):
    """
    EXG-MITM-01 : Interception & Calcul Similitude
    Critère : Vectorisation via all-MiniLM-L6-v2 et calcul de score de similarité cosinus valide [0, 1].
    """
    agent = setup_mitm_context["agent"]
    candidate_label = "Serveur Contrôleur AD"
    
    match_uri, score = agent.evaluate_candidate(candidate_label)
    
    assert match_uri is not None, "Violation EXG-MITM-01 : Aucun match retourné par le modèle d'embedding."
    assert 0.0 <= score <= 1.0, f"Violation EXG-MITM-01 : Score de similitude invalide ({score})"
    assert "server_ad_01" in match_uri, f"Violation EXG-MITM-01 : Entité incorrecte identifiée ({match_uri})"


def test_exg_mitm_02_reconciliation_threshold(setup_mitm_context):
    """
    EXG-MITM-02 : Réconciliation Seuil 0.85
    Critères :
    1. Si score >= 0.85 -> Génération skos:exactMatch et owl:sameAs.
    2. Si score < 0.85 -> Pas d'alignement exactMatch.
    """
    agent = setup_mitm_context["agent"]
    
    # Cas 1 : Candidat avec forte similarité (Score >= 0.85)
    cand_high_uri = f"{DKG_DATA}candidate_high_match"
    cand_high_label = "Serveur Controleur de Domaine Active Directory"
    subgraph_high = agent.process_interception(cand_high_uri, cand_high_label)
    
    cand_ref = URIRef(cand_high_uri)
    target_ref = URIRef(f"{DKG_DATA}server_ad_01")
    
    assert (cand_ref, SKOS.exactMatch, target_ref) in subgraph_high, \
        "Violation EXG-MITM-02 : Alignement 'skos:exactMatch' manquant pour un match >= 0.85."
    assert (cand_ref, OWL.sameAs, target_ref) in subgraph_high, \
        "Violation EXG-MITM-02 : Alignement 'owl:sameAs' manquant pour un match >= 0.85."

    # Cas 2 : Candidat avec faible similarité (Score < 0.85)
    cand_low_uri = f"{DKG_DATA}candidate_low_match"
    cand_low_label = "Imprimante Réseau Bureau L2"
    subgraph_low = agent.process_interception(cand_low_uri, cand_low_label)
    
    low_cand_ref = URIRef(cand_low_uri)
    assert (low_cand_ref, SKOS.exactMatch, None) not in subgraph_low, \
        "Violation EXG-MITM-02 : Alignement 'skos:exactMatch' induement créé pour un score < 0.85 !"


def test_exg_skos_01_taxonomic_consolidation(setup_mitm_context):
    """
    EXG-SKOS-01 : Alignement Taxonomique SKOS
    Critère : Intégration et déduction des triplets réconciliés dans le consolidateur SKOS.
    """
    agent = setup_mitm_context["agent"]
    consolidator = setup_mitm_context["consolidator"]
    
    cand_uri = f"{DKG_DATA}candidate_apt29"
    cand_label = "Cozy Bear APT29 Threat Group"
    
    alignment_subgraph = agent.process_interception(cand_uri, cand_label)
    added_count = consolidator.consolidate_alignment_graph(alignment_subgraph)
    
    assert added_count > 0, "Violation EXG-SKOS-01 : Aucun triplet n'a été intégré lors de la consolidation."
    assert (URIRef(cand_uri), SKOS.exactMatch, URIRef(f"{DKG_DATA}threat_actor_apt29")) in consolidator.master_graph, \
        "Violation EXG-SKOS-01 : La relation skos:exactMatch n'est pas présente dans le graphe consolidé."


def test_exg_skos_02_tlp_segregation_mitm():
    """
    EXG-SKOS-02 : Ségrégation TLP en Ingestion Interceptée
    Critère : Les déductions et alignements ne doivent pas écrire ni altérer la ABox CTI CLEAR.
    """
    cti_path = Path(ABOX_CTI_PATH)
    if cti_path.exists():
        cti_graph = Graph()
        cti_graph.parse(str(cti_path), format="turtle")
        
        cand_ref = URIRef(f"{DKG_DATA}candidate_high_match")
        assert (cand_ref, None, None) not in cti_graph, \
            "Violation EXG-SKOS-02 : Infiltration d'entités candidates interceptées dans ABOX_CTI_PATH (TLP:CLEAR) !"


def test_exg_hw_01_mitm_performance(setup_mitm_context):
    """
    EXG-HW-01 : Temps de Réponse Offline (< 100 ms)
    Critère : Le calcul de similarité pour un candidat doit s'exécuter en moins de 100 millisecondes en local.
    """
    agent = setup_mitm_context["agent"]
    candidate_label = "Serveur AD Secondaire"
    
    start_time = time.time()
    agent.evaluate_candidate(candidate_label)
    execution_time_ms = (time.time() - start_time) * 1000.0
    
    assert execution_time_ms < 100.0, \
        f"Violation EXG-HW-01 : Inférence MITM trop lente ({execution_time_ms:.2f} ms > 100 ms)"
