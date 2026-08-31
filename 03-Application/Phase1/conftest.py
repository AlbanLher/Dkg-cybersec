import pytest
from pathlib import Path
from rdflib import Graph

# Résolution dynamique et absolue des chemins
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MASTER_DIR = BASE_DIR / "02-Donnees" / "Master_Transversal" / "TLP_AMBER_Socle_TBox"

@pytest.fixture(scope="session")
def master_dir():
    return MASTER_DIR

@pytest.fixture(scope="session")
def tbox_graph(master_dir):
    g = Graph()
    tbox_file = master_dir / "DKG_TBox_Master.ttl"
    assert tbox_file.exists(), f"Le fichier TBox {tbox_file} n'existe pas. Lancez generate_phase1_socle.py d'abord."
    g.parse(tbox_file, format="turtle")
    return g

@pytest.fixture(scope="session")
def shacl_graph(master_dir):
    g = Graph()
    shacl_file = master_dir / "shapes_abox.ttl"
    assert shacl_file.exists(), f"Le fichier SHACL {shacl_file} n'existe pas."
    g.parse(shacl_file, format="turtle")
    return g
