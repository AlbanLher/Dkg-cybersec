#!/usr/bin/env python3
"""
test_phase4_ner_validation.py
Validation Pytest - Phase 4 Ingestion CTI Non Structurée (ABox-U).
Contrôle la présence des entités extraites, le respect du seuil de confiance (>= 0.85)
et la conformité SHACL sous Close World Assumption (CWA).
"""

import pytest
from rdflib import Graph, RDF
import pyshacl

from config import (
    ABOX_CTI_U_PATH,
    TBOX_MASTER_PATH,
    SHACL_MASTER_PATH,
    DKG_TBOX,
    DKG_CTI
)


@pytest.fixture
def cti_u_graph() -> Graph:
    """Charge le graphe ABox CTI-U généré à partir de la source non structurée."""
    assert ABOX_CTI_U_PATH.exists(), f"Fichier ABox CTI-U introuvable : {ABOX_CTI_U_PATH}"
    g = Graph()
    g.parse(str(ABOX_CTI_U_PATH), format="turtle")
    return g


def test_ner_entities_presence(cti_u_graph: Graph) -> None:
    """Vérifie l'existence et le typage des entités extraites du bulletin textuel."""
    actor_uri = DKG_CTI["ThreatActor-APT29"]
    cve_uri = DKG_CTI["CVE-2024-21887"]
    pattern_uri = DKG_CTI["Pattern-SpearphishingLink-T1566_002"]

    assert (actor_uri, RDF.type, DKG_TBOX.ThreatActor) in cti_u_graph, "ThreatActor-APT29 absent ou mal typé"
    assert (cve_uri, RDF.type, DKG_TBOX.Vulnerability) in cti_u_graph, "CVE-2024-21887 absente ou mal typée"
    assert (pattern_uri, RDF.type, DKG_TBOX.ThreatPattern) in cti_u_graph, "Pattern T1566_002 absent ou mal typé"


def test_ner_confidence_score_threshold(cti_u_graph: Graph) -> None:
    """EXG-NER-02: Vérifie que l'intégralité des scores de confiance respecte le seuil min (>= 0.85)."""
    scores = list(cti_u_graph.objects(predicate=DKG_TBOX.nerConfidenceScore))
    assert len(scores) > 0, "Aucun score de confiance trouvé dans le graphe."

    for score in scores:
        val = float(score)
        assert val >= 0.85, f"Score de confiance sous le seuil requis : {val} < 0.85"


def test_ner_shacl_conformance(cti_u_graph: Graph) -> None:
    """EXG-QUAL-03: Validation SHACL de l'union (ABox CTI-U + TBox Master)."""
    data_union = Graph()
    data_union += cti_u_graph

    if TBOX_MASTER_PATH.exists():
        data_union.parse(str(TBOX_MASTER_PATH), format="turtle")

    shacl_graph = Graph().parse(str(SHACL_MASTER_PATH), format="turtle")

    conforms, results_graph, results_text = pyshacl.validate(
        data_graph=data_union,
        shacl_graph=shacl_graph,
        inference="rdfs",
        debug=False
    )

    assert conforms, f"Violations SHACL détectées dans ABox CTI-U :\n{results_text}"


if __name__ == "__main__":
    pytest.main([__file__])
