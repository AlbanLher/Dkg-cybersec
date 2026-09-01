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
from config import TBOX_MASTER_PATH, SHACL_MASTER_PATH, ABOX_MASTER_PATH, DKG, DKG_DATA

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
    """Vérifie la présence explicite de la classification TLP:RED dans l'ABox."""
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?tlp WHERE {
        ?s a owl:Ontology ;
           dkg:tlpMarking ?tlp .
    }
    """
    res = [str(row[0]) for row in full_graph.query(query)]
    assert "TLP:RED" in res, f"Marquage TLP:RED introuvable dans l'en-tête d'ontologie. Trouvé: {res}"

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
    PREFIX dkg: <http://dkg.cybersec.org/schema#>
    SELECT ?asset ?comp ?cve ?cwe ?capec WHERE {
        ?asset a dkg:Asset ;
               dkg:hasInstalledComponent ?comp .
        ?comp a dkg:SoftwareComponent ;
              dkg:hasVulnerability ?cve .
        ?cve a dkg:Vulnerability ;
             dkg:exploitsWeakness ?cwe .
        ?cwe a dkg:Weakness ;
             dkg:hasThreatPattern ?capec .
        ?capec a dkg:ThreatPattern .
    }
    """
    res = list(full_graph.query(query))
    assert len(res) > 0, "La chaîne complète Asset -> Component -> CVE -> CWE -> CAPEC est absente !"

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
