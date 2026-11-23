# conftest.py — fixtures TBox/SHACL & marquage automatique par domaine officiel.
# Exécute EXG-OR-* (Organisation & Processus : traçabilité Cycle en V / Spec-Driven).
# Révision 2026-11-17 : ajout mapping test_phase8_demonstrator.py (MET, officialisé),
# avertissement explicite pour fichier non mappé (règle « aucune erreur silencieuse »).
import pytest
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
    "test_phase8_demonstrateur.py": "MET",    # Démonstrateur P8 (EXG-MET-P8-DEM_*) — domaine officialisé
    "test_phase8_confrontation.py": "MET",  # pipeline confrontation (DEM_2, RES_1)
    "test_shacl_conformance.py": "SH",      # SHACL Shapes (à ajuster si besoin)
    "test_hitm_gateway.py": "SE",         # Passerelle HITL & régimes (C1/P9)
    "test_dkg_pipeline.py": "TEC",           # Technique & Core Framework
    "test_mcp_server.py": "TEC",             # Technique & Core Framework
}

def pytest_collection_modifyitems(config, items):
    """Associe dynamiquement chaque test à son domaine officiel en fonction de son fichier source.
    Un fichier de test non répertorié déclenche un avertissement visible (jamais de domaine
    par défaut silencieux — règle « aucune erreur silencieuse » du protocole de recette)."""
    mapped_files = set()
    for item in items:
        filename = item.fspath.basename
        domain = FILE_DOMAIN_MAPPING.get(filename)
        if domain is None:
            print(f"\n⚠️  conftest: fichier de test non mappé dans FILE_DOMAIN_MAPPING : {filename} "
                  f"— marqué TEC par défaut, à corriger.")
            domain = "TEC"
        else:
            mapped_files.add(filename)
        item.add_marker(pytest.mark.domain(domain))
