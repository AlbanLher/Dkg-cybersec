#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_phase3_cti_validation.py
Tests automatisés Pytest pour la Phase 3 (CTI Externe & Ingestion Cross-TLP).
Vérifie la cohérence RDF, les connexions RBox et la conformité SHACL sur l'assemblage TBox + ABox RED + ABox CTI.
"""

import sys
from pathlib import Path
import pytest
from pyshacl import validate
from rdflib import Graph, RDF, XSD

# Ancrage SSOT
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
    """Vérifie la présence et le typage des entités CTI de référence dans le graphe combiné."""
    # Test dynamique sur les vulnérabilités CTI injectées
    vulnerabilities = list(combined_graph.subjects(RDF.type, DKG_TBOX.Vulnerability))
    weaknesses = list(combined_graph.subjects(RDF.type, DKG_TBOX.Weakness))
    threat_patterns = list(combined_graph.subjects(RDF.type, DKG_TBOX.ThreatPattern))

    assert len(vulnerabilities) > 0, "Aucune instance de dkg:Vulnerability trouvée dans l'ABox CTI."
    assert len(weaknesses) > 0, "Aucune instance de dkg:Weakness trouvée dans l'ABox CTI."
    assert len(threat_patterns) > 0, "Aucune instance de dkg:ThreatPattern trouvée dans l'ABox CTI."


def test_cti_multi_hop_chain(combined_graph):
    """
    Vérifie la validité de la chaîne RBox CTI :
    dkg:Vulnerability -> dkg:exploitsWeakness -> dkg:Weakness -> dkg:hasThreatPattern -> dkg:ThreatPattern
    """
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    
    SELECT ?cve ?cwe ?capec WHERE {
        ?cve a dkg:Vulnerability ;
             dkg:exploitsWeakness ?cwe .
        ?cwe a dkg:Weakness ;
             dkg:hasThreatPattern ?capec .
        ?capec a dkg:ThreatPattern .
    }
    """
    results = list(combined_graph.query(query))
    assert len(results) > 0, "La chaîne RBox CTI (CVE -> dkg:exploitsWeakness -> CWE -> CAPEC) est absente ou mal formée."


def test_cross_tlp_chain_link(combined_graph):
    """
    Vérifie le raccordement fonctionnel Cross-TLP (ABox RED -> ABox CLEAR) :
    dkg:SoftwareComponent (TLP:RED) -> dkg:hasVulnerability -> dkg:Vulnerability (TLP:CLEAR)
    """
    query = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    
    SELECT ?comp ?cve ?score WHERE {
        ?comp a dkg:SoftwareComponent ;
              dkg:hasVulnerability ?cve .
        ?cve a dkg:Vulnerability .
        OPTIONAL { ?cve dkg:cvssScore ?score . }
    }
    """
    results = list(combined_graph.query(query))
    assert len(results) > 0, "Aucun composant de l'ABox RED n'est raccordé à une vulnérabilité CTI CLEAR."


def test_shacl_conformance_phase3(combined_graph):
    """Vérifie la conformité SHACL intégrale du graphe d'union vis-à-vis des contraintes SHACL Master."""
    assert SHACL_MASTER_PATH.exists(), f"Fichier SHACL introuvable : {SHACL_MASTER_PATH}"
    shacl_graph = Graph().parse(str(SHACL_MASTER_PATH), format="turtle")

    conforms, results_graph, results_text = validate(
        data_graph=combined_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        serialize_report_graph=False
    )

    assert conforms, f"❌ Violations SHACL détectées lors du test de recette Phase 3 :\n{results_text}"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
