#!/usr/bin/env python3
from pathlib import Path
from pyshacl import validate
from rdflib import Graph

BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_TTL = BASE_DIR / "12-Donnees" / "TLP-RED_ABox_Cybersec" / "ABox_Cybersec.ttl"
SHAPES_TTL = BASE_DIR / "12-Donnees" / "shapes_abox.ttl"


def verify_abox():
    data_graph = Graph()
    data_graph.parse(ABOX_TTL, format="turtle")

    shapes_graph = Graph()
    shapes_graph.parse(SHAPES_TTL, format="turtle")

    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        debug=False,
    )

    if conforms:
        print("✅ PHASE 2 VALIDÉE : L'ABox respecte l'ensemble des contraintes de structure.")
    else:
        print("❌ ÉCHEC DE LA PHASE 2 : Violations SHACL détectées dans l'ABox !")
        print(results_text)
        exit(1)


if __name__ == "__main__":
    verify_abox()
