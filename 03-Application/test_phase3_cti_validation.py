#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests automatisés Pytest pour la Phase 2.5 (CTI Externe & Ingestion Cross-TLP).
Vérifie la cohérence RDF et la conformité SHACL du graphe combiné.
"""

import pytest
from rdflib import Graph, RDF
from pyshacl import validate

# Imports alignés à 100% sur config.py
from config import (
    TBOX_MASTER_PATH,
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    DKG,
    DKG_DATA,
    DKG_CTI
)


@pytest.fixture(scope="module")
def combined_graph():
    """
    Fixture Pytest qui charge l'ensemble des graphes du projet :
    - TBox Master + Contraintes SHACL (TLP:AMBER)
    - ABox Cartographie Interne (TLP:RED)
    - ABox CTI Externe (TLP:CLEAR)
    """
    g = Graph()
    
    # 1. Chargement TBox & SHACL
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
    """
    Vérifie la présence des instances CTI clés du scénario 'Silent Cascade' dans le graphe combiné.
    """
    cve_uri = DKG_CTI["CVE-2021-41773"]
    cwe_uri = DKG_CTI["CWE-22"]
    capec_uri = DKG_CTI["CAPEC-126"]

    # Vérification des typages RDF
    assert (cve_uri, RDF.type, DKG.Vulnerability) in combined_graph, "CVE-2021-41773 n'est pas typée Vulnerability"
    assert (cwe_uri, RDF.type, DKG.Weakness) in combined_graph, "CWE-22 n'est pas typée Weakness"
    assert (capec_uri, RDF.type, DKG.ThreatPattern) in combined_graph, "CAPEC-126 n'est pas typée ThreatPattern"


def test_cross_tlp_link(combined_graph):
    """
    Vérifie le raccordement Cross-TLP entre le composant local (TLP:RED) et la CTI (TLP:CLEAR).
    """
    apache_uri = DKG_DATA["Apache-2.4.49"]
    cve_uri = DKG_CTI["CVE-2021-41773"]
    
    # Vérification de l'existence du lien dkg:hasVulnerability
    has_vuln_triples = list(combined_graph.triples((apache_uri, DKG.hasVulnerability, cve_uri)))
    assert len(has_vuln_triples) > 0, "Le composant Apache-2.4.49 n'est pas relié à CVE-2021-41773 via dkg:hasVulnerability"


def test_shacl_validation_cti(combined_graph):
    """
    Exécute la validation SHACL sur le graphe combiné.
    """
    conforms, results_graph, results_text = validate(
        data_graph=combined_graph,
        shacl_graph=combined_graph,  # Formes SHACL combinées dans la TBox Master
        inference='rdfs',
        debug=False
    )
    
    assert conforms, f"❌ Échec de la validation SHACL sur le graphe CTI combiné :\n{results_text}"
