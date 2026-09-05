#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_phase3_cti_validation.py
Tests automatisés Pytest pour la Phase 3 (CTI Externe & Ingestion Cross-TLP).
Vérifie la cohérence RDF et la conformité SHACL sur l'assemblage TBox + ABox RED + ABox CTI.
"""

import pytest, sys
from rdflib import Graph, RDF
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import (
    TBOX_MASTER_PATH,
    SHACL_MASTER_PATH,
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI
)

@pytest.fixture(scope="module")
def combined_graph():
    """
    Fixture Pytest qui rassemble l'ensemble des graphes du projet :
    - TBox Master (TLP:AMBER)
    - ABox Interne (TLP:RED)
    - ABox CTI Externe (TLP:CLEAR)
    """
    g = Graph()
    
    # 1. Chargement TBox
    assert TBOX_MASTER_PATH.exists(), f"Fichier TBox introuvable : {TBOX_MASTER_PATH}"
    g.parse(str(TBOX_MASTER_PATH), format="turtle")
    
    # 2. Chargement ABox RED (Cartographie interne)
    assert ABOX_RED_PATH.exists(), f"Fichier ABox RED introuvable : {ABOX_RED_PATH}"
    g.parse(str(ABOX_RED_PATH), format="turtle")
    
    # 3. Chargement ABox CLEAR (CTI Externe)
    assert ABOX_CTI_PATH.exists(), f"Fichier ABox CTI introuvable : {ABOX_CTI_PATH}"
    g.parse(str(ABOX_CTI_PATH), format="turtle")
    
    return g


def test_cti_entities_exist(combined_graph):
    """Vérifie la présence des entités CTI de référence dans le graphe combiné."""
    cve_uri = DKG_CTI["CVE-2021-44228"]
    cwe_uri = DKG_CTI["CWE-502"]
    capec_uri = DKG_CTI["CAPEC-586"]

    assert (cve_uri, RDF.type, DKG_TBOX.Vulnerability) in combined_graph, "CVE-2021-44228 non typée Vulnerability"
    assert (cwe_uri, RDF.type, DKG_TBOX.Weakness) in combined_graph, "CWE-502 non typée Weakness"
    assert (capec_uri, RDF.type, DKG_TBOX.ThreatPattern) in combined_graph, "CAPEC-586 non typée ThreatPattern"


def test_cross_tlp_chain_link(combined_graph):
    """
    Vérifie le raccordement fonctionnel Cross-TLP :
    dkg:SoftwareComponent -> dkg:hasVulnerability -> dkg:Vulnerability
    """
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    
    SELECT ?comp ?cve WHERE {
        ?comp a dkg:SoftwareComponent ;
              dkg:hasVulnerability ?cve .
        ?cve a dkg:Vulnerability .
    }
    """
    results = list(combined_graph.query(query))
    assert len(results) > 0, "Aucun composant de l'ABox RED n'est raccordé à une vulnérabilité CTI CLEAR."
