import sys
import time
import pytest
from pathlib import Path
from _pytest.monkeypatch import MonkeyPatch
from rdflib import Graph, URIRef, Literal, RDF, XSD

# Ancrage du chemin racine 03-Application
sys.path.append(str(Path(__file__).resolve().parent.parent))


# Ancrage dynamique du dossier 03-Application dans le PYTHONPATH
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))





from Phase5.reasoning_engine import ReasoningEngine
from config import DKG_TBOX, DKG_DATA, DKG_CTI


@pytest.fixture(scope="module")
def setup_mock_graphs(tmp_path_factory):
    """
    Génère les graphes d'entrée ABox RED et ABox CTI temporaires avec les motifs R-01 et R-02.
    """
    tmp_dir = tmp_path_factory.mktemp("phase5_inference_data")
    mock_abox_red = tmp_dir / "DKG_ABox_Master.ttl"
    mock_abox_cti = tmp_dir / "DKG_ABox_CTI_External.ttl"
    mock_infered = tmp_dir / "DKG_ABox_Infered.ttl"

    # 1. Graphe ABox RED (Interne)
    abox_red_graph = Graph()
    srv_pivot = URIRef(f"{DKG_DATA}server_pivot_01")
    target_db = URIRef(f"{DKG_DATA}db_critical_01")
    vuln_cve = URIRef(f"{DKG_CTI}CVE-2024-21887")

    # Ingestion pour R-01 et R-02
    abox_red_graph.add((srv_pivot, RDF.type, URIRef(f"{DKG_TBOX}Asset")))
    abox_red_graph.add((srv_pivot, URIRef(f"{DKG_TBOX}hasVulnerability"), vuln_cve))
    abox_red_graph.add((srv_pivot, URIRef(f"{DKG_TBOX}connectsTo"), target_db))
    
    abox_red_graph.add((target_db, RDF.type, URIRef(f"{DKG_TBOX}Asset")))
    abox_red_graph.add((target_db, URIRef(f"{DKG_TBOX}criticalityLevel"), Literal("CRITICAL")))
    abox_red_graph.serialize(destination=str(mock_abox_red), format="turtle")

    # 2. Graphe ABox CTI (Externe)
    abox_cti_graph = Graph()
    abox_cti_graph.add((vuln_cve, RDF.type, URIRef(f"{DKG_TBOX}Vulnerability")))
    abox_cti_graph.add((vuln_cve, URIRef(f"{DKG_TBOX}isCisaKev"), Literal(True, datatype=XSD.boolean)))
    abox_cti_graph.serialize(destination=str(mock_abox_cti), format="turtle")

    return {
        "abox_red_path": mock_abox_red,
        "abox_cti_path": mock_abox_cti,
        "infered_path": mock_infered
    }


@pytest.fixture(scope="module")
def execution_context(setup_mock_graphs):
    """
    Surcharge les constantes importées dans Phase5.reasoning_engine,
    exécute le moteur et enregistre le graphe déduit.
    """
    paths = setup_mock_graphs
    mp = MonkeyPatch()
    
    import Phase5.reasoning_engine as re_module
    mp.setattr(re_module, "ABOX_RED_PATH", paths["abox_red_path"], raising=False)
    mp.setattr(re_module, "ABOX_CTI_PATH", paths["abox_cti_path"], raising=False)
    mp.setattr(re_module, "ABOX_INFERED_PATH", paths["infered_path"], raising=False)

    engine = ReasoningEngine()
    exec_duration = engine.run_inference()
    engine.save_and_document()

    yield {
        "engine": engine,
        "execution_time": exec_duration,
        "infered_graph": engine.graph_infered,
        "paths": paths
    }
    
    mp.undo()


def test_exg_hw_01_performance(execution_context):
    """
    EXG-HW-01 : Performance d'exécution (< 5 secondes)
    """
    exec_time = execution_context["execution_time"]
    assert exec_time < 5.0, f"Violation EXG-HW-01 : Inférence trop lente ({exec_time:.2f}s > 5.0s)"


def test_exg_inf_01_high_risk_asset(execution_context):
    """
    EXG-INF-01 : Inférence HighRiskAsset (Règle R-01)
    """
    graph = execution_context["infered_graph"]
    
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    
    ASK {
        ?asset a dkg:HighRiskAsset .
    }
    """.strip()
    has_high_risk_asset = bool(graph.query(query))
    assert has_high_risk_asset, \
        "Violation EXG-INF-01 : Aucune entité 'HighRiskAsset' matérialisée."


def test_exg_inf_02_cascade_materialization(execution_context):
    """
    EXG-INF-02 : Matérialisation Cascade (Règle R-02)
    """
    graph = execution_context["infered_graph"]
    
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    
    ASK {
        ?pivot dkg:exposesToCascade ?target .
    }
    """.strip()
    has_cascade_relation = bool(graph.query(query))
    assert has_cascade_relation, \
        "Violation EXG-INF-02 : La propriété 'exposesToCascade' n'a pas été matérialisée."


def test_exg_se_01_tlp_segregation(execution_context):
    """
    EXG-SE-01 : Isolation TLP & Non-pollution des graphes sources
    """
    paths = execution_context["paths"]
    
    assert paths["infered_path"].exists(), "Violation EXG-SE-01 : Le fichier ABox Infered n'a pas été créé."
    
    cti_graph = Graph()
    cti_graph.parse(str(paths["abox_cti_path"]), format="turtle")
    
    high_risk_class = URIRef(f"{DKG_TBOX}HighRiskAsset")
    assert (None, RDF.type, high_risk_class) not in cti_graph, \
        "Violation EXG-SE-01 : Fuite de données d'inférence TLP:RED vers la source CTI TLP:CLEAR !"
