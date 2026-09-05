#!/usr/bin/env python3
"""
test_phase4_ner_validation.py
Validation Pytest - Phase 4 NER & Unstructured CTI.
Contrôle la présence des entités extraites, les scores de confiance (>= 0.85)
et l'absence de violation SHACL.
"""

import pytest
from rdflib import Graph, RDF
import pyshacl

from config import (
    ABOX_CTI_PATH,
    SHACL_MASTER_PATH,
    DKG_TBOX,
    DKG_CTI
)


@pytest.fixture
def cti_graph():
    """Charge le graphe ABox CTI enrichi par le pipeline NER."""
    assert ABOX_CTI_PATH.exists(), f"Fichier ABox CTI introuvable : {ABOX_CTI_PATH}"
    g = Graph()
    g.parse(str(ABOX_CTI_PATH), format="turtle")
    return g


def test_ner_entities_presence(cti_graph):
    """Vérifie la présence des entités extraites depuis le bulletin texte."""
    actor_uri = DKG_CTI["ThreatActor-APT29"]
    cve_uri = DKG_CTI["CVE-2024-21887"]
    pattern_uri = DKG_CTI["Pattern-SpearphishingLink-T1566_002"]

    assert (actor_uri, RDF.type, DKG_TBOX.ThreatActor) in cti_graph, "ThreatActor-APT29 absent ou mal typé"
    assert (cve_uri, RDF.type, DKG_TBOX.Vulnerability) in cti_graph, "CVE-2024-21887 absente ou mal typée"
    assert (pattern_uri, RDF.type, DKG_TBOX.ThreatPattern) in cti_graph, "Pattern T1566_002 absent ou mal typé"


def test_ner_confidence_score_threshold(cti_graph):
    """EXG-NER-02: Vérifie que tous les scores de confiance sont >= 0.85."""
    scores = list(cti_graph.objects(predicate=DKG_TBOX.nerConfidenceScore))
    assert len(scores) > 0, "Aucun score de confiance NER trouvé dans le graphe."

    for score in scores:
        val = float(score)
        assert val >= 0.85, f"Score de confiance insuffisant détecté : {val} < 0.85"


def test_ner_shacl_conformance(cti_graph):
    """EXG-QUAL-03: Validation SHACL du graphe CTI enrichi."""
    shacl_graph = Graph().parse(str(SHACL_MASTER_PATH), format="turtle")

    conforms, results_graph, results_text = pyshacl.validate(
        data_graph=cti_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        debug=False
    )

    assert conforms, f"Violations SHACL détectées post-NER :\n{results_text}"


if __name__ == "__main__":
    pytest.main([__file__])
