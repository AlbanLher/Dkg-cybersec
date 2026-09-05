#!/usr/bin/env python3
"""
test_shacl_conformance.py
Validation SHACL automatisée de l'ABox Master Consolidée (Phase 3).
Utilise exclusivement les constantes SSOT fournies par config.py.
"""

import pytest
from pyshacl import validate
from rdflib import Graph

from config import (
    SHACL_MASTER_PATH,
    ABOX_RED_PATH,
    ABOX_CTI_PATH
)


def test_abox_shacl_conformance():
    """Valide l'ABox RED et l'ABox CTI vis-à-vis des contraintes SHACL Master."""
    assert SHACL_MASTER_PATH.exists(), f"Fichier SHACL introuvable : {SHACL_MASTER_PATH}"
    assert ABOX_RED_PATH.exists(), f"Fichier ABox RED introuvable : {ABOX_RED_PATH}"
    assert ABOX_CTI_PATH.exists(), f"Fichier ABox CTI introuvable : {ABOX_CTI_PATH}"

    # Chargement des données à valider
    data_graph = Graph()
    data_graph.parse(str(ABOX_RED_PATH), format="turtle")
    data_graph.parse(str(ABOX_CTI_PATH), format="turtle")

    # Chargement du schéma de formes
    shacl_graph = Graph().parse(str(SHACL_MASTER_PATH), format="turtle")

    conforms, results_graph, results_text = validate(
        data_graph=data_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        serialize_report_graph=False
    )

    assert conforms, f"❌ Violations SHACL détectées dans le graphe consolidé :\n{results_text}"


if __name__ == "__main__":
    pytest.main([__file__])
