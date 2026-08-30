#!/usr/bin/env python3
"""
Test de conformité SHACL pour l'ABox Master Consolidée (Phase 3).
Vérifie que les instances de 12-Donnees/Master_Transversal/TLP_RED_Consolidation_ABox/
respectent les règles dynamiques de 12-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/shapes_abox.ttl
"""

from pathlib import Path
from pyshacl import validate
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SHACL_FILE = BASE_DIR / "12-Donnees" / "Master_Transversal" / "TLP_AMBER_Socle_TBox" / "shapes_abox.ttl"
ABOX_MASTER_FILE = BASE_DIR / "12-Donnees" / "Master_Transversal" / "TLP_RED_Consolidation_ABox" / "DKG_ABox_Master.ttl"


def test_abox_shacl_conformance():
    assert SHACL_FILE.exists(), f"Fichier SHACL introuvable : {SHACL_FILE}"
    assert ABOX_MASTER_FILE.exists(), f"Fichier ABox Master introuvable : {ABOX_MASTER_FILE}"

    data_graph = Graph().parse(str(ABOX_MASTER_FILE), format="turtle")
    shacl_graph = Graph().parse(str(SHACL_FILE), format="turtle")

    conforms, results_graph, results_text = validate(
        data_graph=data_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        serialize_report_graph=False
    )

    if not conforms:
        print("❌ ECHEC : Violations SHACL détectées dans l'ABox Master :")
        print(results_text)
    else:
        print("✅ SUCCÈS : L'ABox Master TLP:RED est 100% conforme aux règles SHACL TLP:AMBER.")

    assert conforms, "Le graphe ABox Master ne respecte pas les contraintes SHACL !"


if __name__ == "__main__":
    test_abox_shacl_conformance()
