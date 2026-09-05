#!/usr/bin/env python3
"""
test_phase2_abox.py
Suite de tests d'intégration et recette SHACL pour l'ABox Phase 2 sous TLP:RED.
"""

import sys
from pathlib import Path
import pytest
from rdflib import Graph, Namespace
from pyshacl import validate

# Import de la configuration centralisée
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
# from config import TBOX_MASTER_PATH, SHACL_MASTER_PATH, ABOX_MASTER_PATH, DKG, DKG_DATA

# import pytest
#  from config import DIR_SNAPSHOT_P2, DIR_MASTER_ABOX

# 1. Ancrage sys.path vers 03-Application/ pour importer config.py
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# from rdflib import Graph, Literal, RDF, RDFS, OWL, XSD
from config import (
    TBOX_MASTER_PATH,
    SHACL_MASTER_PATH,
    ABOX_MASTER_PATH,
    DKG_DATA,
    DIR_SNAPSHOT_P2,
    DIR_MASTER_ABOX
)


@pytest.fixture(scope="module")
def full_graph():
    """Charge l'ensemble TBox + ABox dans un graphe RDF global."""
    g = Graph()
    assert TBOX_MASTER_PATH.exists(), f"Fichier TBox introuvable: {TBOX_MASTER_PATH}"
    assert ABOX_MASTER_PATH.exists(), f"Fichier ABox introuvable: {ABOX_MASTER_PATH}"
    
    g.parse(str(TBOX_MASTER_PATH), format="turtle")
    g.parse(str(ABOX_MASTER_PATH), format="turtle")
    return g

def test_exg_uc_abox_tlp_marking(full_graph):
    """Vérifie la présence explicite du marquage TLP:RED sur les actifs."""
    query = """
    PREFIX dkg:  <http://dkg.cybersec.org/tbox#>
    PREFIX data: <http://dkg.cybersec.org/data#>

    SELECT ?tlp WHERE {
        ?asset a dkg:Asset ;
               dkg:hasTLPMarking ?tlp .
        ?tlp a dkg:TLPMarking .
    }
    """
    res = [str(row[0]) for row in full_graph.query(query)]
    
    # On vérifie que l'URI du TLP:RED est bien présente dans la liste des marquages appliqués
    expected_tlp_red = "http://dkg.cybersec.org/data#TLP-RED"
    assert expected_tlp_red in res, f"Marquage TLP:RED introuvable sur les actifs. Trouvé: {res}"

def test_exg_uc_abox_01_namespace_integrity(full_graph):
    """EXG-UC-ABOX-01: Isolation du namespace dkg-data."""
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/schema#>
    SELECT ?s WHERE {
        ?s a ?type .
        FILTER(STRSTARTS(STR(?type), "http://dkg.cybersec.org/schema#"))
        FILTER(!STRSTARTS(STR(?s), "http://dkg.cybersec.org/data/"))
    }
    """
    res = full_graph.query(query)
    assert len(res) == 0, f"Instances hors namespace dkg-data : {[row[0] for row in res]}"

def test_exg_uc_abox_03_cyber_chain_completeness(full_graph):
    """EXG-UC-ABOX-03: Complétude de la chaîne Asset -> Component -> CVE -> CWE -> CAPEC."""
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?asset ?comp ?cve ?cwe ?capec WHERE {
        ?asset a dkg:Asset ;
               dkg:hasInstalledComponent ?comp .
        ?comp a dkg:SoftwareComponent ;
              dkg:hasVulnerability ?cve .
        ?cve a dkg:Vulnerability ;
             dkg:hasWeakness ?cwe .
        ?cwe a dkg:Weakness ;
             dkg:hasThreatPattern ?capec .
        ?capec a dkg:ThreatPattern .
    }
    """
    res = list(full_graph.query(query))
    assert len(res) > 0, "La chaîne complète Asset -> Component -> CVE -> CWE -> CAPEC est absente !"



# def test_exg_uc_abox_03_cyber_chain_completeness(full_graph):
#    """EXG-UC-ABOX-03: Complétude de la chaîne Asset -> Component -> CVE -> CWE -> CAPEC."""
#    query = """
#    PREFIX dkg: <http://dkg.cybersec.org/schema#>
#    SELECT ?asset ?comp ?cve ?cwe ?capec WHERE {
#        ?asset a dkg:Asset ;
#               dkg:hasInstalledComponent ?comp .
#        ?comp a dkg:SoftwareComponent ;
#              dkg:hasVulnerability ?cve .
#        ?cve a dkg:Vulnerability ;
#             dkg:exploitsWeakness ?cwe .
#        ?cwe a dkg:Weakness ;
#             dkg:hasThreatPattern ?capec .
#        ?capec a dkg:ThreatPattern .
#    }
#    """
#    res = list(full_graph.query(query))
#    assert len(res) > 0, "La chaîne complète Asset -> Component -> CVE -> CWE -> CAPEC est absente !"


def test_exg_fwk_02_01_referential_integrity(full_graph):
    """EXG-FWK-02-01: Intégrité référentielle (0 instance orpheline)."""
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/schema#>
    SELECT ?s ?p ?o WHERE {
        ?s ?p ?o .
        FILTER(isURI(?o))
        FILTER(STRSTARTS(STR(?o), "http://dkg.cybersec.org/data/"))
        FILTER NOT EXISTS { ?o a ?type }
    }
    """
    res = list(full_graph.query(query))
    assert len(res) == 0, f"URIs d'instances orphelines non déclarées trouvées: {res}"

def test_exg_qual_02_03_shacl_validation(full_graph):
    """EXG-QUAL-02 / EXG-QUAL-03: Validation SHACL sous CWA (0 violation)."""
    assert SHACL_MASTER_PATH.exists(), f"Fichier SHACL introuvable: {SHACL_MASTER_PATH}"
    shacl_graph = Graph().parse(str(SHACL_MASTER_PATH), format="turtle")
    
    conforms, report_graph, report_text = validate(
        data_graph=full_graph,
        shacl_graph=shacl_graph,
        inference='rdfs',
        abort_on_first=False,
        meta_shacl=False
    )
    
    assert conforms, f"Violations SHACL détectées lors de la recette ABox:\n{report_text}"

import pytest
from config import DIR_SNAPSHOT_P2, DIR_MASTER_ABOX

def test_exg_org_02_phase2_master_snapshot_parity():
    """Vérifie que les fichiers archivés dans Snapshot Phase 2 sont identiques dans Master."""
    assert DIR_SNAPSHOT_P2.exists(), f"Répertoire snapshot introuvable: {DIR_SNAPSHOT_P2}"

    valid_extensions = {".ttl", ".json", ".md"}
    snapshot_files = [
        f for f in DIR_SNAPSHOT_P2.iterdir() 
        if f.is_file() and f.suffix in valid_extensions
    ]

    assert len(snapshot_files) > 0, "Le dossier Snapshot Phase 2 est vide !"

    for snap_file in snapshot_files:
        master_file = DIR_MASTER_ABOX / snap_file.name
        assert master_file.exists(), f"Fichier {snap_file.name} absent du Master ABox."
        
        # Comparaison normalisée
        snap_content = snap_file.read_text(encoding="utf-8").strip().replace("\r\n", "\n")
        master_content = master_file.read_text(encoding="utf-8").strip().replace("\r\n", "\n")
        
        assert snap_content == master_content, f"Écart de parité détecté sur {snap_file.name}"
