#!/usr/bin/env python3
"""
Test de Conformité Phase 2 : Ingestion ABox Infrastructure & Gatekeeper SHACL
Contrôle les exigences EXG-ABOX-01 à EXG-ABOX-04 et EXG-GOV-01.
"""

import sys
from pathlib import Path
from rdflib import Graph
from pyshacl import validate

BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_TTL = BASE_DIR / "12-Donnees" / "TLP-RED_ABox_Cybersec" / "ABox_Cybersec.ttl"
SHAPES_TTL = BASE_DIR / "12-Donnees" / "SHACL_Shapes" / "shapes_abox.ttl"


def test_abox_shacl_compliance():
    print("==================================================")
    print("🔍 [PHASE 2] Vérification ABox Infrastructure & SHACL")
    print("==================================================")

    assert ABOX_TTL.exists(), f"❌ [EXG-ABOX-01] Fichier ABox introuvable : {ABOX_TTL}"
    assert SHAPES_TTL.exists(), f"❌ [EXG-GOV-01] Fichier SHACL Shapes introuvable : {SHAPES_TTL}"

    data_graph = Graph().parse(ABOX_TTL, format="turtle")
    shapes_graph = Graph().parse(SHAPES_TTL, format="turtle")

    print(f"ℹ️  Triplets ABox chargés : {len(data_graph)}")

    # EXG-ABOX-02 : Namespace ABox
    abox_ns = "http://dkg.cybersec.org/abox#"
    abox_subjects = [str(s) for s in data_graph.subjects() if str(s).startswith(abox_ns)]
    assert len(abox_subjects) > 0, "❌ [EXG-ABOX-02] Aucun individu identifié sous le namespace ABox http://dkg.cybersec.org/abox#"
    print("✅ [EXG-ABOX-02] Instances d'infrastructure correctement sous le namespace ABox.")

    # EXG-ABOX-01 & 03 : Traçabilité et non-orphelinat via SPARQL
    query_tree = """
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    
    ASK {
        ?asset a dkg:Asset ;
               dkg:hasInstalledComponent ?comp .
        ?comp a dkg:SoftwareComponent .
    }
    """
    assert bool(data_graph.query(query_tree)), "❌ [EXG-ABOX-01/03] Arborescence incomplète : Asset sans Composant détecté."
    print("✅ [EXG-ABOX-01/03] Structure d'arborescence Asset -> Composant présente.")

    # EXG-GOV-01 : Execution du Gatekeeper SHACL (PySHACL)
    print("⏳ Exécution du contrôle PySHACL Gatekeeper...")
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        debug=False,
    )

    if not conforms:
        print(f"\n❌ [EXG-GOV-01] VIOLATION SHACL DÉTECTÉE :\n{results_text}")
        sys.exit(1)

    print("✅ [EXG-GOV-01] Gatekeeper SHACL : Aucune violation de contrainte structurelle.")
    print("\n🎉 PHASE 2 VALIDE : L'ABox Infrastructure est conforme et validée par SHACL.\n")


if __name__ == "__main__":
    try:
        test_abox_shacl_compliance()
    except AssertionError as e:
        print(e)
        sys.exit(1)
