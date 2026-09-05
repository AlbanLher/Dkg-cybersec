import pytest
# from pathlib import Path
from rdflib import Graph
from config import DIR_MASTER_TBOX, TBOX_MASTER_PATH, SHACL_MASTER_PATH

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


