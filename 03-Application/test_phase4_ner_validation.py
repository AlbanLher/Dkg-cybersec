#!/usr/bin/env python3
"""
Validation Pytest - Phase 4 NER & Unstructured CTI
Contrôle la présence des entités extraites, les scores de confiance (>= 0.85)
et l'absence de violation SHACL.
"""

import pytest
from rdflib import Graph, Literal, Namespace, RDF, XSD
import pyshacl
from config import ABOX_CTI_PATH, TBOX_MASTER_PATH

DKG = Namespace("http://dkg.cybersec.org/schema#")
DKG_CTI = Namespace("http://dkg.cybersec.org/cti#")


@pytest.fixture
def cti_graph():
    """Charge le graphe ABox CTI enrichi."""
    g = Graph()
    g.parse(ABOX_CTI_PATH, format="turtle")
    return g


def test_ner_entities_presence(cti_graph):
    """Vérifie la présence des entités extraites depuis le bulletin texte."""
    actor_uri = DKG_CTI["ThreatActor-APT29"]
    cve_uri = DKG_CTI["CVE-2024-21887"]
    pattern_uri = DKG_CTI["Pattern-SpearphishingLink-T1566_002"]

    assert (actor_uri, RDF.type, DKG.ThreatActor) in cti_graph
    assert (cve_uri, RDF.type, DKG.Vulnerability) in cti_graph
    assert (pattern_uri, RDF.type, DKG.ThreatPattern) in cti_graph


def test_ner_confidence_score_threshold(cti_graph):
    """EXG-NER-02: Vérifie que tous les scores de confiance sont >= 0.85."""
    scores = list(cti_graph.objects(predicate=DKG.nerConfidenceScore))
    assert len(scores) > 0, "Aucun score de confiance NER trouvé dans le graphe."

    for score in scores:
        val = float(score)
        assert val >= 0.85, f"Score de confiance insuffisant détecté : {val} < 0.85"


def test_ner_shacl_conformance():
    """EXG-QUAL-03: Validation SHACL du graphe CTI enrichi."""
    data_graph = Graph().parse(ABOX_CTI_PATH, format="turtle")
    shacl_graph = Graph().parse(TBOX_MASTER_PATH, format="turtle")

    conforms, results_graph, results_text = pyshacl.validate(
        data_graph=data_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        debug=False
    )

    assert conforms, f"Violations SHACL détectées post-NER :\n{results_text}"
