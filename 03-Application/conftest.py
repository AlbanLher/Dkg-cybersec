import pytest
# from pathlib import Path
from rdflib import Graph
from core.config import DIR_MASTER_TBOX, TBOX_MASTER_PATH, SHACL_MASTER_PATH

@pytest.fixture(scope="session")
def master_dir():
    return DIR_MASTER_TBOX

@pytest.fixture(scope="session")
def tbox_graph():
    g = Graph()
    assert TBOX_MASTER_PATH.exists(), f"Fichier TBox introuvable : {TBOX_MASTER_PATH}"
    g.parse(str(TBOX_MASTER_PATH), format="ttl")
    return g

@pytest.fixture(scope="session")
def shacl_graph():
    g = Graph()
    assert SHACL_MASTER_PATH.exists(), f"Fichier SHACL introuvable : {SHACL_MASTER_PATH}"
    g.parse(str(SHACL_MASTER_PATH), format="ttl")
    return g


# --- Extension : Ségrégation automatique par Domaine (Cycle en V / Spec-Driven) ---

FILE_DOMAIN_MAPPING = {
    "test_phase1_quality.py": "QU",          # Qualité & Conformité
    "test_phase2_abox.py": "SH",             # SHACL Shapes
    "test_phase3_cti_validation.py": "CT",   # Cyber Threat Intelligence
    "test_phase4_ner_validation.py": "TEC",  # Technique & Core Framework
    "test_phase5_inference.py": "IN",        # Inférence & Graph Analytics
    "test_phase5_mitm.py": "SE",             # Sécurité & Isolation
    "test_phase6_gateway.py": "TEC",         # Technique & Core Framework
    "test_phase7_residential.py": "HW",      # Hardware & Infrastructures
    "test_phase8_compliance.py": "QU",       # Qualité & Conformité
    "test_phase8_soc_orchestrator.py": "OR", # Organisation & Processus
    "test_dkg_pipeline.py": "TEC",           # Technique & Core Framework
    "test_mcp_server.py": "TEC",             # Technique & Core Framework
}

def pytest_collection_modifyitems(config, items):
    """Associe dynamiquement chaque test à son domaine officiel en fonction de son fichier source."""
    for item in items:
        filename = item.fspath.basename
        domain = FILE_DOMAIN_MAPPING.get(filename, "TEC")  # 'TEC' par défaut
        item.add_marker(pytest.mark.domain(domain))
